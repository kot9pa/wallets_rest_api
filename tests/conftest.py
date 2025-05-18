import os
import sys
import pytest_asyncio
import alembic.command
from httpx import ASGITransport, AsyncClient
from alembic.config import Config

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from src.config import settings
from src.database import Database
from src.main import app


alembic_config = Config("alembic.ini")
alembic_config.set_main_option("sqlalchemy.url", settings.get_db_url())
db_test = Database(echo=True)


def run_upgrade(connection):
    alembic_config.attributes["connection"] = connection
    alembic.command.upgrade(alembic_config, "head")


def run_downgrade(connection):
    alembic_config.attributes["connection"] = connection
    alembic.command.downgrade(alembic_config, "base")


@pytest_asyncio.fixture(scope='session', autouse=True)
async def apply_migrations():
    async with db_test.engine.begin() as conn:
        await conn.run_sync(run_upgrade)
    # If needed, run downgrade migrations after tests
    # yield
    # async with db_test.engine.begin() as conn:
    #     await conn.run_sync(run_downgrade)


@pytest_asyncio.fixture(autouse=True)
async def db_session():
    async with db_test.session_dependency() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app, raise_app_exceptions=False),
        base_url=f"http://{settings.SERVER_DOMAIN}:{settings.SERVER_PORT}"
    ) as client:
        yield client
