from pathlib import Path

from fastapi_mail import ConnectionConfig
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Класс базовых настроек проекта."""

    app_title: str = 'Бронирование ледового катка'
    description: str = 'Управление работой ледового катка.'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 300
    SECRET_KEY: str = ''
    REDIS_URL: str = ''

    # email settings
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_from_name: str

    mail_starttls: bool
    mail_ssl_tls: bool
    mail_use_credentials: bool
    mail_validate_certs: bool

    # Настройки Rabbit
    rabbitmq_user: str
    rabbitmq_pass: str
    rabbitmq_host: str
    rabbitmq_port: int

    # Flower
    flower_port: int
    flower_host: str
    flower_user: str
    flower_password: str

    # sms settings
    smsaero_email: str
    smsaero_api_key: str

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    @property
    def database_url(self) -> str:
        """Создание папки для БД на 2 уровня выше корня."""
        base_dir = Path(__file__).resolve().parents[2]
        data_folder = base_dir / 'data'
        data_folder.mkdir(exist_ok=True)
        data = data_folder / 'ice_skating.db'
        return f'sqlite+aiosqlite:///{data}'

    @property
    def mail_config(self) -> ConnectionConfig:
        """Динамически собираем конфиг для почты после загрузки настроек."""
        return ConnectionConfig(
            MAIL_USERNAME=self.mail_username,
            MAIL_PASSWORD=self.mail_password,
            MAIL_FROM=self.mail_from,
            MAIL_PORT=self.mail_port,
            MAIL_SERVER=self.mail_server,
            MAIL_FROM_NAME=self.mail_from_name,
            MAIL_STARTTLS=self.mail_starttls,
            MAIL_SSL_TLS=self.mail_ssl_tls,
            USE_CREDENTIALS=self.mail_use_credentials,
            VALIDATE_CERTS=self.mail_validate_certs,
        )

    @property
    def celery_broker_url(self) -> str:
        """Формируем ссылку для Rabbit."""
        return (
            f'amqp://{self.rabbitmq_user}:'
            f'{self.rabbitmq_pass}@{self.rabbitmq_host}:{self.rabbitmq_port}//'
        )

    @property
    def flower_auth(self) -> list[str]:
        """Формируем список для Basic Auth во Flower."""
        return [f'{self.flower_user}:{self.flower_password}']


settings = Settings()
