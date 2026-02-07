from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.repositories import CategoryRepo
from app.schemas.category import CategoryResponse

category_router = APIRouter(prefix="/categories", tags=["categories"])


@category_router.get(
    "/count-child",
    response_model=List[CategoryResponse],
    summary="Кол-во дочерних категорий",
)
async def get_count_child(db: AsyncSession = Depends(get_db), with_orm: bool = False):
    """Находит количество дочерних элементов первого уровня вложенности для всех категорий
    продуктов"""
    repo = CategoryRepo(db)
    return await repo.get_count_child(with_orm=with_orm)
