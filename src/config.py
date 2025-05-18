from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Класс настроек приложения.

    Attributes:
        DB_USER (str): Имя пользователя базы данных.
        DB_PASSWORD (str): Пароль пользователя базы данных.
        DB_HOST (str): Хост базы данных.
        DB_PORT (int): Порт базы данных.
        DB_NAME (str): Имя базы данных.
        DB_ECHO (bool): Включает или отключает вывод SQL-запросов.
        LOG_LEVEL (str): Уровень логирования.
        SERVER_HOST (str): Хост сервера.
        SERVER_DOMAIN (str): Домен сервера.
        SERVER_PORT (int): Порт сервера.
        WORKERS (int): Количество рабочих процессов.
        api_v1_prefix (str): Префикс API.
    """
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    DB_ECHO: bool = False
    LOG_LEVEL: str = "warning"
    SERVER_HOST: str = "0.0.0.0"
    SERVER_DOMAIN: str = "localhost"
    SERVER_PORT: int = 8000
    WORKERS: int = 1

    api_v1_prefix: str = "/api/v1"
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

    def get_db_url(self):
        """
        Возвращает URL базы данных.

        Returns:
            URL базы данных.
        """
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")


settings = Settings()
