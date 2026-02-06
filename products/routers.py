from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.conf_db import get_db
from products.schemas import AddProductRequest

product_router = APIRouter(prefix="/products", tags=["products"])


@product_router.post("/add")
def add_product_into_order(req: AddProductRequest, db: AsyncSession = Depends(get_db)):
    pass
