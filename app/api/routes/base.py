from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .category import category_router
from .client import client_router
from .product import product_router
from ...db import get_db
from ...schemas.app import AppResponse

app_router = APIRouter(prefix="/app", tags=["app"])
app_router.include_router(category_router)
app_router.include_router(client_router)
app_router.include_router(product_router)


@app_router.get(
    "/ping", response_model=AppResponse, summary="Проверка состояния сервера"
)
async def ping(db: AsyncSession = Depends(get_db)):
    """Проверка сервера"""
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "db_connected": True}
    except Exception:
        return {"status": "error", "db_connected": False}
