from http.client import responses

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response

from app.api.dependencies import get_product_service
from app.schemas.product import AddProductRequest, AddProductResponse
from app.services.product import ProductService

product_router = APIRouter(prefix="/products", tags=["products"])


@product_router.post(
    "/add",
    summary="Добавить товар",
    response_description="Информация о товаре",
    response_model=AddProductResponse,
)
async def add_product_into_order(
    response: Response,
    req: AddProductRequest,
    service: ProductService = Depends(get_product_service),
):
    """Добавляет товар в заказ"""
    error, is_created = await service.add_product_into_order(
        req.order_id, req.product_id, req.count
    )
    if error:
        raise HTTPException(status_code=400, detail=error.args[0])
    else:
        response.status_code = 201 if is_created else 200
        return {"message": "Product added successfully", "created": is_created}
