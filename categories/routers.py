from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from categories.category_repo import CategoryRepo
from core.db.conf_db import get_db

category_router = APIRouter(prefix="/categories", tags=["categories"])


@category_router.get("/count-child")
async def get_count_child(db: AsyncSession = Depends(get_db), with_orm: bool = False):
    repo = CategoryRepo(db)
    await repo.get_count_child(with_orm=with_orm)
