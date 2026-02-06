import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from categories.routers import category_router
from clients.routers import client_router
from core.db.conf_db import engine, async_session
from db.scripts.create_report_view import create_report_view
from db.scripts.fixtures_seed_data import seed_test_data
from products.routers import product_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app):
    logger.info("Starting lifespan")

    logger.info("Checking database connection")

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection established")
        print("Database connection established")
    except Exception:
        logger.exception("Database connection failed")
        raise
    async with async_session() as session:
        await seed_test_data(session)
        await create_report_view(session)

    yield

    await engine.dispose()


shop_app = FastAPI(title="Shop App", description="Shop App", lifespan=lifespan)
shop_app.include_router(client_router)
shop_app.include_router(category_router)
shop_app.include_router(product_router)
