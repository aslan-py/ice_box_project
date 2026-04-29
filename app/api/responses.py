from typing import Any

from fastapi import status

from app.core.constants import ResponseMessage


class ResponsesSettings:
    """Корректировка вывода ошибок swagger."""

    ERROR_401: dict[int | str, dict[str, Any]] = {
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Не авторизированный пользователь',
            'content': {
                'application/json': {
                    'example': {'detail': ResponseMessage.error_401}
                }
            },
        }
    }

    ERROR_403: dict[int | str, dict[str, Any]] = {
        status.HTTP_403_FORBIDDEN: {
            'description': 'Недостаточно прав',
            'content': {
                'application/json': {
                    'example': {'detail': ResponseMessage.error_403}
                }
            },
        }
    }

    ERROR_404: dict[int | str, dict[str, Any]] = {
        status.HTTP_404_NOT_FOUND: {
            'description': 'Пользователь не найден',
            'content': {
                'application/json': {
                    'example': {'detail': ResponseMessage.error_404}
                }
            },
        }
    }

    ERROR_422: dict[int | str, dict[str, Any]] = {
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            'description': 'Ошибка ввода данных',
            'content': {
                'application/json': {
                    'example': {'detail': ResponseMessage.error_422}
                }
            },
        }
    }
