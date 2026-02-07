import pytest
from httpx import AsyncClient
from sqlalchemy import text

from app.schemas.product import AddProductRequest


@pytest.mark.asyncio
async def test_add_product_into_order(session, client: AsyncClient, add_seed_test_data):
    await add_seed_test_data

    order_id = 1
    product_id = 1
    count = 2

    req = AddProductRequest(order_id=order_id, product_id=product_id, count=count)
    response = await client.post("/products/add", json=req.model_dump())

    assert response.status_code == 200
    data = response.json()
    assert data["created"] is False
    assert data["message"] == "Product added successfully"
