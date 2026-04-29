from datetime import date
from typing import Sequence

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import SessionDep, get_admin_authorizer
from app.api.responses import ResponsesSettings
from app.core.constants import IceBoxSlotConstants
from app.models.ice_box_slot import IceBoxSlot
from app.schemas.ice_box_slot import (
    IceBoxSlotCreate,
    IceBoxSlotResponse,
    IceBoxSlotUpdate,
)
from app.services.ice_box_slot import icebox_service

router = APIRouter()


@router.get(
    '',
    response_model=list[IceBoxSlotResponse],
    summary=IceBoxSlotConstants.GET_SUM,
    responses=ResponsesSettings.ERROR_422,
)
async def get_slots(
    session: SessionDep,
    date: date = Query(None, description=IceBoxSlotConstants.DESCRIPT_GET),
) -> Sequence[IceBoxSlot]:
    """Просмотр расписания катка, только активные и можно выбрать дату.

    Доступно всем.
    """
    return await icebox_service.get_all_slots(
        session, date=date, is_active=True
    )


@router.get(
    '/admins',
    response_model=list[IceBoxSlotResponse],
    dependencies=[Depends(get_admin_authorizer)],
    summary=IceBoxSlotConstants.GET_ADMIN,
    responses={
        **ResponsesSettings.ERROR_401,
        **ResponsesSettings.ERROR_422,
        **ResponsesSettings.ERROR_403,
        **ResponsesSettings.ERROR_404,
    },
)
async def get_slots_for_admin(
    session: SessionDep,
    date: date = Query(None, description=IceBoxSlotConstants.DESCRIPT_GET),
    is_active: bool = Query(
        None, description=IceBoxSlotConstants.DESCRIPT_IS_ACTIVE
    ),
) -> Sequence[IceBoxSlot]:
    """Просмотр расписания катка, с фильтрами даты и статуса активности.

    Только Админам.
    """
    return await icebox_service.get_all_slots(
        session, date=date, is_active=is_active
    )


@router.post(
    '',
    response_model=IceBoxSlotResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_admin_authorizer)],
    summary=IceBoxSlotConstants.POST_SUM,
    responses={
        **ResponsesSettings.ERROR_401,
        **ResponsesSettings.ERROR_422,
        **ResponsesSettings.ERROR_403,
        **ResponsesSettings.ERROR_404,
    },
)
async def create_slot(
    obj_in: IceBoxSlotCreate, session: SessionDep
) -> IceBoxSlot:
    """Создание нового слота администратором.

    Только админы.
    """
    return await icebox_service.create_slot(session, obj_in)


@router.patch(
    '/{slot_id}',
    response_model=IceBoxSlotResponse,
    dependencies=[Depends(get_admin_authorizer)],
    summary=IceBoxSlotConstants.PATCH_SUM,
    responses={
        **ResponsesSettings.ERROR_401,
        **ResponsesSettings.ERROR_422,
        **ResponsesSettings.ERROR_403,
        **ResponsesSettings.ERROR_404,
    },
)
async def update_slot(
    slot_id: int, obj_in: IceBoxSlotUpdate, session: SessionDep
) -> IceBoxSlot:
    """Частичное обновление данных слота.

    Только админы.
    """
    return await icebox_service.update_slot(session, slot_id, obj_in)
