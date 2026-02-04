import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from core.db.conf_db import engine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app):
    logger.info("Starting lifespan")

    logger.info("Checking database connection")

    try:
        async with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection established")
        print("Database connection established")
    except Exception:
        logger.exception("Database connection failed")
        raise

    yield

    await engine.dispose()


shop_app = FastAPI(title="Shop App", description="Shop App", lifespan=lifespan)
