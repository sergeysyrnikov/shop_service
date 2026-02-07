import os

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.api.dependencies import get_product_service
from app.main import shop_app
from app.services import ProductService
from app.utils.db.fixtures_seed_data import seed_test_data

os.environ["TESTING"] = "1"
from app.models import BaseModel

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def session() -> AsyncSession:
    engine = create_async_engine(TEST_DB_URL, echo=False)
    async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest_asyncio.fixture
async def client(session):

    async def override_get_product_service():
        return ProductService(session)

    shop_app.dependency_overrides[get_product_service] = override_get_product_service

    transport = ASGITransport(app=shop_app)
    async with AsyncClient(transport=transport, base_url="http://test/app") as ac:
        yield ac

    shop_app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def add_seed_test_data(session):
    await seed_test_data(session)
