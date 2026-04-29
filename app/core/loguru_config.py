import sys
from pathlib import Path

from loguru import logger

# 1. Определяем путь (на 2 уровня выше: app/core -> корень проекта)
BASE_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'log.log'

# 2. Создаем папку, если её нет
LOG_DIR.mkdir(exist_ok=True)


def setup_logging() -> None:
    """Настройка глобального логирования для всего приложения.

    Methods:
    logger.remove — удаляет стандартный обработчик
        (чтобы не дублировать в консоль).
    logger.add — добавляет новые пути вывода
        (консоль и файл) с нужным форматом.

    """
    logger.remove()

    # Формат: Дата Время | Уровень | Функция - Сообщение
    log_format = (
        '<green>{time:YYYY-MM-DD HH:mm:ss}</green> | '
        '<level>{level: <8}</level> | '
        '<cyan>{function}</cyan> - <level>{message}</level>'
    )

    # Вывод в консоль (красивый, цветной)
    logger.add(sys.stdout, format=log_format, colorize=True, level='DEBUG')

    # Вывод в файл (без цветов, но с ротацией, чтобы файл не весил гигабайты)
    logger.add(
        LOG_FILE,
        format='{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {function} - {message}',  # noqa: E501
        level='INFO',
        rotation='10 MB',
        retention='7 days',
        compression='zip',
        encoding='utf-8',
    )


setup_logging()
