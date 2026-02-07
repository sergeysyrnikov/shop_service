import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.api.routes import app_router
from app.db import engine, async_session
from app.utils.db.create_report_view import create_report_view
from app.utils.db.fixtures_seed_data import seed_test_data

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
        print("lfksdjflkjsdklfjskldjflds")
        if os.getenv("ENV") == "dev":
            await seed_test_data(session)
        await create_report_view(session)

    yield

    await engine.dispose()


shop_app = FastAPI(
    title="Shop Service API",
    description="API для управления заказами и продуктами",
    version="1.0.0",
    contact={"name": "Sergey", "email": "sergeysyrnikov91@gmail.com"},
    license_info={"name": "MIT"},
    lifespan=lifespan,
)
shop_app.include_router(app_router)
