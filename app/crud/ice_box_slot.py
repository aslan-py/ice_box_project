from datetime import date, datetime
from typing import Sequence

from sqlalchemy import or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.ice_box_slot import IceBoxSlot
from app.schemas.ice_box_slot import IceBoxSlotCreate, IceBoxSlotUpdate


class CRUDIceBoxSlot(CRUDBase[IceBoxSlot, IceBoxSlotCreate, IceBoxSlotUpdate]):
    """Управление слотами катка."""

    async def get_by_date_and_time(
        self,
        session: AsyncSession,
        schemas_in: IceBoxSlotCreate | IceBoxSlotUpdate,
        exclude_id: int | None = None,
    ) -> IceBoxSlot | None:
        """Поиск слота по уникальному сочетанию даты и времени.

        Удобно для проверки наличия дублирования слотов на указанное время.
        """
        slot_data = schemas_in.model_dump(exclude_unset=True)

        filters = [
            self.model.week_day == slot_data.get('week_day'),
            self.model.time_slot == slot_data.get('time_slot'),
        ]
        query = select(self.model).where(*filters)
        if exclude_id:
            query = query.where(self.model.id != exclude_id)
        result = await session.execute(query)

        return result.scalar_one_or_none()

    async def get_multi_by_date(
        self,
        session: AsyncSession,
        *,
        is_active: bool | None = None,
        target_date: date | None = None,
    ) -> Sequence[IceBoxSlot]:
        """Получение списка активных слотов.

        удобно для показа пользователю всех слотов по датам.
        """
        query = select(self.model)

        if is_active is not None:
            query = query.where(self.model.is_active.is_(is_active))
        if target_date:
            query = query.where(self.model.week_day == target_date)

        query = query.order_by(self.model.week_day, self.model.time_slot)

        result = await session.execute(query)
        return result.scalars().all()

    async def deactivate_expired(self, session: AsyncSession) -> None:
        """Отключает слоты, которые уже прошли по времени."""
        now = datetime.now()

        await session.execute(
            update(self.model)
            .where(self.model.is_active.is_(True))
            .where(
                or_(self.model.week_day < now.date(), self.model.capacity <= 0)
            )
            .values(is_active=False)
        )


ice_box_slot_crud = CRUDIceBoxSlot(IceBoxSlot)
