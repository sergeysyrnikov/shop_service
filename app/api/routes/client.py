from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.client_repo import ClientRepo
from app.db.conf_db import get_db
from app.schemas.client import ClientResponse

client_router = APIRouter(prefix="/clients", tags=["clients"])


@client_router.get(
    "/total-spent",
    response_model=List[ClientResponse],
    summary="Сумма трат по клиентам",
)
async def get_spent_per_client(
    db: AsyncSession = Depends(get_db), with_orm: bool = False
):
    """Получает информацию о сумме товаров заказанных под каждого клиента
    (Наименование клиента, сумма)"""
    repo = ClientRepo(db)
    return await repo.get_total_per_client(with_orm=with_orm)
