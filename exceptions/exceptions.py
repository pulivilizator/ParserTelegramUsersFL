class CreateSessionException(Exception):
    """Ошибка создания сессии"""

class EnvException(Exception):
    """Обишка считывания окружения"""

class GetFileExeption(Exception):
    """Ошибка считывания файла на входе(файл не найден)"""


class WriteFileExeption(Exception):
    """Ошибка записи в файл(файл не найден)"""


class CreateFileExeption(Exception):
    """Ошибка создания файла"""

class GetUserDataException(Exception):
    """Ошибка обработки/получения данных пользователя"""

