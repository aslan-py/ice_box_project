from datetime import date
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.celery.tasks.orchestrator import send_cancellation_flow
from app.core.constants import IceBoxSlotConstants, LoguruSettings
from app.core.loguru_config import logger
from app.crud.booking import booking_crud
from app.crud.ice_box_slot import ice_box_slot_crud
from app.models.ice_box_slot import IceBoxSlot
from app.schemas.ice_box_slot import (
    IceBoxSlotCreate,
    IceBoxSlotUpdate,
)


class IceBoxSlotService:
    """Логика работы с созданием слотов."""

    async def get_all_slots(
        self,
        session: AsyncSession,
        date: date | None,
        is_active: bool | None = None,
    ) -> Sequence[IceBoxSlot]:
        """Возвращает список слотов, учитывая фильтр активности и даты.

        Methods:
        ice_box_slot_crud.deactivate_expired — деактивирует в базе данных
            слоты с прошедшей датой/временем.
        ice_box_slot_crud.get_multi_by_date — запрашивает отфильтрованный
            список слотов из базы данных

        """
        await ice_box_slot_crud.deactivate_expired(session)
        await session.commit()
        return await ice_box_slot_crud.get_multi_by_date(
            session, target_date=date, is_active=is_active
        )

    async def create_slot(
        self, session: AsyncSession, obj_in: IceBoxSlotCreate
    ) -> IceBoxSlot:
        """Создает новый временной слот для катка.

        Methods:
        ice_box_slot_crud.get_by_date_and_time — проверяет, не занято ли
            выбранное время другим слотом.
        ice_box_slot_crud.create — осуществляет запись нового
            объекта слота в базу данных.

        """
        slot = await ice_box_slot_crud.get_by_date_and_time(session, obj_in)
        if slot:
            logger.warning(LoguruSettings.SLOT_DUPLICATE)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=IceBoxSlotConstants.ERR_400_DUBLE_SLOTS,
            )
        logger.info(
            LoguruSettings.SLOT_CREATED.format(
                obj_in.week_day, obj_in.time_slot
            )
        )
        return await ice_box_slot_crud.create(
            session=session, schemas_in=obj_in
        )

    async def update_slot(
        self, session: AsyncSession, slot_id: int, obj_in: IceBoxSlotUpdate
    ) -> IceBoxSlot:
        """Обновляет параметры существующего слота.

        Methods:
        ice_box_slot_crud.get — получает текущий объект слота из базы данных.
        ice_box_slot_crud.get_by_date_and_time — проверяет наличие другого
            слота на то же время.
        booking_crud.get_notifiable_clients — собирает контакты пользователей
            с активной бронью.
        send_cancellation_flow.delay — запускает фоновую задачу рассылки
            уведомлений об отмене.
        ice_box_slot_crud.update — сохраняет измененные данные слота в базу.

        """
        db_obj = await ice_box_slot_crud.get(session, obj_id=slot_id)

        if not db_obj:
            logger.warning(LoguruSettings.SLOT_NOT_FOUND.format(slot_id))
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=IceBoxSlotConstants.ERR_404_SLOTS,
            )
        if obj_in.week_day or obj_in.time_slot:
            check_data = IceBoxSlotCreate(
                week_day=obj_in.week_day or db_obj.week_day,
                time_slot=obj_in.time_slot or db_obj.time_slot,
                capacity=db_obj.capacity,
            )

            duplicate = await ice_box_slot_crud.get_by_date_and_time(
                session, schemas_in=check_data, exclude_id=slot_id
            )
            if duplicate:
                logger.error(
                    LoguruSettings.SLOT_UPDATE_CONFLICT.format(slot_id)
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=IceBoxSlotConstants.ERR_400_SLOTS,
                )

        if obj_in.is_active is False and db_obj.is_active is True:
            if db_obj.week_day >= date.today():
                raw_clients = await booking_crud.get_notifiable_clients(
                    session, slot_id
                )

                if raw_clients:
                    logger.info(
                        LoguruSettings.SLOT_DEACTIVATION_FLOW.format(
                            slot_id, len(raw_clients)
                        )
                    )
                    clients_for_celery = []
                    for client in raw_clients:
                        data = {'phone': client.phone, 'email': client.email}
                        clients_for_celery.append(data)
                    date_str = db_obj.week_day.strftime('%d.%m.%Y')
                    time_str = str(db_obj.time_slot)
                    send_cancellation_flow.delay(
                        users_data=clients_for_celery,
                        date_str=date_str,
                        time_str=time_str,
                    )
        logger.info(LoguruSettings.SLOT_UPDATED.format(slot_id))
        return await ice_box_slot_crud.update(
            session, schemas_in=obj_in, db_obj=db_obj
        )


icebox_service = IceBoxSlotService()
