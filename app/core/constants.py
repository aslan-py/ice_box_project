CAPACITY = 20


class BookingMessage:
    """Коснатнты для сообщений Booking."""

    full_slot = 'На выбранный сеанс мест нет.'
    slot_in_past = 'Нельзя забронировать сеанс в прошлом.'
    no_booking = 'У тебя нет ни одной брони.'
    no_booking_for_del = 'Бронь не найдена.'
    not_yours_booking = 'Нельзя удалять чужие брони.'
    success_delete = {'message': 'Бронь удалена'}
    double_booking = 'У тебя уже есть бронь на данный слот'


class ResponseMessage:
    """Константы для swagger."""

    no_slot = 'Такого слота не существет.'
    slot_already_exists = 'Слот на это время и дату уже существует'
    slot_delete_success = 'Слот успешно удален'
    error_401 = 'Нужно авторизироваться'
    error_403 = 'Необходимо зайти под нужными правами'
    error_404 = 'Нет такого объекта'
    error_422 = 'Введены некорректные данные'
    error_user_400 = (
        'Пользователь с таким номером телефона или почтой уже существует'
    )


class AuthConstants(ResponseMessage):
    """Константы авторизации."""

    OTP_EXPIRY = 300
    NEW_DEFAULT_NAME = 'Новичок'
    error_auth_400 = 'Код истек или не запрашивался'
    error_auth_400_wrong = 'Неверный код'
    request_summary = 'Запросить СМС-код'
    verify_summary = 'Проверить код и получить токен'
    sms_status_msg = 'Код отправили на почту и по смс(ожидание смс до 5 минут)'
    sms_status_code = 'succes'
    sms_status = {'status': sms_status_code, 'message': sms_status_msg}
    subject_msg = 'Код подтверждения — IceBox'
    security_error = 'Данные принадлежат разным пользователям.'
    already_used = 'Указанная почта или телефон уже заняты другим аккаунтом'
    canseled_lot_msg = cancellation_msg = (
        'Информируем вас, что сеанс на {} в {} '
        'отменен по техническим причинам.'
    )
    code_msg = 'Ваш код доступа {}'
    sms_error_msg = 'СМС-задача вызвана без кода и сообщения'
    subject = 'Отмена записи на каток'
    all_chanel_sent = 'ALL_CHANNELS_SENT'
    sucess_notify = 'Successfully dispatched notifications for {} users'


class UserConstants:
    """Константы для модели User."""

    PHONE_PATTERN = r'^7\d{10}$'
    NAME_ERR = (
        'Имя должно содержать только буквы русского или латинского алфавита'
    )
    NAME_PATTERN = r'^[a-zA-Zа-яА-ЯёЁ]+$'
    USERNAME_MIN_LENGTH = 3
    USERNAME_MAX_LENGTH = 100
    USERNAME = 'Имя пользователя'
    PASSWORD_NAME = 'Пароль пользователя'
    NEW_PASS_NAME = 'Новый пароль пользователя'
    DESCR_PHONE = 'Номер телефона в формате 7XXXXXXXXXX'
    PASS_LENGTH = 6
    ROLE_UPDATE = 'Новая роль пользователя'
    STATUS_UPDATE = 'Изменение статуса активации'
    ROLE = 'Роль пользователя в системе'
    IS_ACTIVE = 'Статус активности аккаунта'
    USER_ID = 'Уникальный идентификатор пользователя'
    USER_EXAMPLE = {
        'example': {
            'id': 1,
            'name': 'Алексей',
            'phone': '+79991234567',
            'role': 'USER',
            'is_active': True,
        }
    }
    PHONE_ERR = 'Номер телефона должен быть в формате +7XXXXXXXXXX'
    PASS_EASY_MSG = 'Пароль слишком простой {}'
    GET_ME_SUM = 'Посмотреть свои данные'
    DEL_ME_SUM = 'Декативировать себя'
    PATCH_ME_SUM = 'Изменить свои данные'
    PATCH_USER = 'Изменить данные юзера'
    GET_ALL = 'Посмотреть всех юзеров'
    MAKE_ADMIN = 'Превратить себя в админа '


class IceBoxSlotConstants:
    """Константы для модели слотов катка."""

    DEFAULT_CAPACITY = 20
    MIN_CAPACITY = 0

    # Описания для Swagger
    DESCR_WEEK_DAY = 'Дата проведения сеанса'
    DESCR_TIME_SLOT = 'Временной интервал'
    DESCR_CAPACITY = 'Количество свободных мест'
    DESCR_IS_ACTIVE = 'Доступен ли слот для бронирования'
    DESCR_ID = 'Идентификатор слота'

    # Ошибки
    ERR_PAST_DATE = 'Нельзя создать или изменить слот на прошедшую дату'
    ERR_MAX_CAPACITY = (
        f'Вместимость не может превышать {DEFAULT_CAPACITY} человек'
    )
    ERR_MIN_CAPACITY = 'Вместимость не может быть меньше 1'
    ICE_EXAMPLE = {
        'example': {
            'id': 10,
            'week_day': '2026-12-01',
            'time_slot': '10:00-11:00',
            'capacity': 15,
            'is_active': True,
        }
    }
    ERR_400_SLOTS = 'Слот на это время уже занят'
    ERR_400_DUBLE_SLOTS = 'Слот уже был создан ранее.'
    ERR_404_SLOTS = 'Слот не найден'
    GET_SUM = 'Посмотреть все доступные слоты'
    POST_SUM = 'Создать новый слот'
    GET_ADMIN = 'Посмотреть слоты с возможностью фильтрации'
    PATCH_SUM = 'Изменить слоты'
    DESCRIPT_GET = 'Дата сеанса'
    DESCRIPT_IS_ACTIVE = 'Статус активности'


class BookingConstants:
    """Константы для модели бронирования."""

    # Описания для Swagger
    DESCR_SLOT_ID = 'Идентификатор временного слота'
    DESCR_USER_ID = 'Идентификатор пользователя'
    DESCR_BOOKING_ID = 'Уникальный номер брони'
    DESCR_IS_ACTIVE = 'Статус активности брони'
    DESCR_WEEK_DAY = 'Дата сеанса'
    DESCR_TIME_SLOT = 'Время сеанса'

    # Примеры для схем
    BOOKING_EXAMPLE = {
        'example': {
            'id': 1,
            'slot_id': 10,
            'user_id': 5,
            'is_active': True,
            'week_day': '2026-05-15',
            'time_slot': '14:00-15:00',
        }
    }
    ERR_BOOK_NOT_FOUND = 'Слот не найден'
    ERR_BOOK_NOT_AVAILABLE = 'Слот недоступен для бронирования'
    ERR_BOOK_NOT_FREE = 'Нет свободных мест'
    ERR_BOOK_DOUBLE = 'Вы уже забронировали этот сеанс'
    ERR_404_BOOK = 'Бронирование не найдено'
    ERR_403_BOOK = 'Вы не можете отменить чужое бронирование'
    SUM_GET_ALL_BOOK = 'Посмотреть все заброненые слоты'
    SUM_DEL_BOOK = 'Удалить ранее заброненый слот'
    SUM_GET_MУ = 'Просмотр своих броней'
    SUM_POST_BOOK = 'Забронировать слот'


class LoguruSettings:
    """Константы для логирования событий системы."""

    USER_NOT_FOUND = 'Попытка доступа к несуществующему пользователю с ID: {}'
    UPDATE_CONFLICT = (
        'Конфликт данных при обновлении профиля пользователя ID: {}'
    )
    ADMIN_PROMOTED = (
        'ВНИМАНИЕ: Пользователю с именем: {} назначены права АДМИНИСТРАТОРА'
    )
    UPDATE_SUCCESS = 'Профиль пользователя ID: {} успешно обновлен'
    USER_DEACTIVATED = (
        'Пользователь ID: {} деактивировал свой аккаунт (soft delete)'
    )
    SLOT_CREATED = 'Создан новый слот на дату: {} время: {}'
    SLOT_UPDATED = 'Параметры слота ID: {} успешно изменены'
    SLOT_DUPLICATE = 'Попытка создания дубликата слота (дата/время заняты)'
    SLOT_NOT_FOUND = 'Слот с ID: {} не найден для выполнения операции'
    SLOT_UPDATE_CONFLICT = 'Конфликт при смене времени слота ID: {} (занято)'
    SLOT_DEACTIVATION_FLOW = (
        'Деактивация слота ID: {}. Запуск оповещения для {} клиентов'  # noqa: E501
    )
    BOOK_CREATED = 'Пользователь ID: {} успешно забронировал слот ID: {}'
    BOOK_SLOT_NOT_FOUND = 'Ошибка: Слот ID: {} не найден для юзера ID: {}'
    BOOK_SLOT_INACTIVE = (
        'Попытка бронирования неактивного слота ID: {} юзером ID: {}'  # noqa: E501
    )
    BOOK_NO_CAPACITY = 'Попытка бронирования слота ID: {}. Места закончились'
    BOOK_DUPLICATE = 'Повторная бронь: юзер ID: {} уже записан на слот ID: {}'

    CANCEL_SUCCESS = 'Бронирование ID: {} успешно удалено пользователем ID: {}'
    CANCEL_NOT_FOUND = 'Попытка отмены несуществующей брони ID: {}'
    CANCEL_FORBIDDEN = 'ALERT: Юзер ID: {} пытался удалить чужую бронь ID: {}'
    AUTH_CODE_SENT = 'Код успешно сгенерирован и отправлен на номер: {}'
    AUTH_OTP_EXPIRED = (
        'Попытка входа с несуществующим или просроченным кодом: {}'  # noqa: E501
    )
    AUTH_INVALID_CODE = 'ВНИМАНИЕ: Введен неверный код для номера: {}'
    AUTH_SUCCESS = 'Пользователь с номером {} успешно авторизован'
    AUTH_USER_CREATED = 'Зарегистрирован новый пользователь по номеру: {}'
    AUTH_SECURITY_WARN = (
        'ALERT: Конфликт уникальности данных (phone: {}, email: {})'  # noqa: E501
    )
    AUTH_ALREADY_USED = 'Попытка привязки занятых данных к номеру: {}'
    SMS_ATTEMPT = 'Запрос на отправку СМС для номера: {}'
    AUTH_TOKEN_CREATED = 'Сгенерирован новый access-token для юзера ID: {}'
    AUTH_TOKEN_INVALID_PAYLOAD = (
        'Ошибка JWT: в полезной нагрузке отсутствует "sub"'  # noqa: E501
    )
    AUTH_TOKEN_EXPIRED = 'Предоставленный JWT токен просрочен'
    AUTH_TOKEN_ERROR = 'Критическая ошибка валидации JWT: {}'
    SMS_TASK_STARTED = 'Celery-задача: запуск отправки СМС для номера: {}'
    SMS_TASK_PARAMS_ERROR = (
        'Ошибка Celery: задача для {} вызвана без текста (no code/msg)'
    )
    FLOW_VERIFY_START = 'Запуск верификации для phone: {} и email: {}'
    FLOW_SMS_ERROR = 'Ошибка во флоу СМС для номера {}: {}'
    FLOW_EMAIL_ERROR = 'Ошибка во флоу Email: письмо на {} не отправлено'
    FLOW_CANCEL_START = 'Запуск массовой рассылки отмены на {} клиентов'
    FLOW_INVALID_PHONE = 'Пропущен некорректный номер телефона во флоу: {}'
    EMAIL_ATTEMPT = 'Попытка отправки Email на адрес: {}'
    EMAIL_SENT_SUCCESS = 'Письмо успешно доставлено на адрес: {}'
    EMAIL_ERROR = 'Ошибка при отправке письма на {}: {}'
