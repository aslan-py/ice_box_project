from fastapi import APIRouter

from app.api.endpoints import (
    aup_router,
    auth_router,
    booking_router,
    icebox_router,
    user_router,
)

main_router = APIRouter()

main_router.include_router(
    booking_router, prefix='/booking', tags=['Бронировния']
)

main_router.include_router(
    icebox_router, prefix='/icebox', tags=['Слоты ледового катка']
)

main_router.include_router(user_router, prefix='/user', tags=['Пользователи'])

main_router.include_router(
    auth_router, prefix='/auth', tags=['Аутентификация']
)

main_router.include_router(
    aup_router, prefix='/make_admin_me', tags=['Преврати себя в админа']
)
