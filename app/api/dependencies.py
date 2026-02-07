import os
from fastapi import Depends, Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.product import ProductService
from app.db import get_db

API_KEY = os.getenv("SECRET_KEY", None)
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:
    return ProductService(db)


def get_api_key(api_key: str = Security(API_KEY_HEADER)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key
