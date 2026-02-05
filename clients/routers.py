from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from clients.client_repo import ClientRepo
from core.db.conf_db import get_db

client_router = APIRouter(prefix="/clients", tags=["clients"])


@client_router.get("/total-spent")
async def get_spent_per_client(
    db: AsyncSession = Depends(get_db), with_orm: bool = False
):
    repo = ClientRepo(db)
    return await repo.get_total_per_client(with_orm=with_orm)
