from asyncio import current_task
from fastapi.concurrency import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session
)

from src.config import settings


class Database:
    def __init__(self, url: str = None, echo: bool = False):
        """
        Инициализирует объект базы данных.

        Args:
            url (str): URL базы данных.
            echo (bool): Включает или отключает вывод SQL-запросов.
        """
        self.engine = create_async_engine(
            url=url if url is not None else settings.get_db_url(),
            echo=echo,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        """
        Возвращает сессию базы данных, привязанную к текущей задаче.

        Returns:
            Сессия базы данных.
        """
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    @asynccontextmanager
    async def session_dependency(self):
        """
        Возвращает контекстный менеджер для сессии базы данных.

        Yields:
            Сессия базы данных.
        """
        async with self.session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def scoped_session_dependency(self):
        """
        Возвращает сессию базы данных, привязанную к текущей задаче.

        Yields:
            Сессия базы данных.
        """
        session = self.get_scoped_session()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


db_helper = Database(echo=settings.DB_ECHO)
