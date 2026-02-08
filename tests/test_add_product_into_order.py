import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models import OrderItemModel, ProductModel
from app.schemas.product import AddProductRequest


@pytest.mark.asyncio
async def test_add_product_into_order(
    session,
    client: AsyncClient,
    add_seed_test_data,
):
    order_item = (
        (
            await session.execute(
                select(OrderItemModel)
                .options(
                    joinedload(OrderItemModel.order),
                    joinedload(OrderItemModel.product),
                )
                .limit(1)
            )
        )
        .scalars()
        .first()
    )

    assert order_item is not None

    req = AddProductRequest(
        order_id=order_item.order_id,
        product_id=order_item.product_id,
        count=order_item.product.count - 1,
    )

    async def post_and_assert(payload, status, body_key, body_value):
        response = await client.post("/products/add", json=payload)
        assert response.status_code == status
        data = response.json()
        assert data[body_key] == body_value
        return data

    data = await post_and_assert(
        req.model_dump(),
        200,
        "message",
        "Product added successfully",
    )
    assert data["created"] is False

    req.count = 1
    data = await post_and_assert(
        req.model_dump(),
        200,
        "message",
        "Product added successfully",
    )
    assert data["created"] is False

    for invalid_count in (4, 2):
        req.count = invalid_count
        await post_and_assert(
            req.model_dump(),
            400,
            "detail",
            "Product with current product_id is less than quantity",
        )

    new_product_id = (
        (
            await session.execute(
                select(ProductModel.id).where(
                    ProductModel.id.not_in(
                        select(OrderItemModel.product_id).where(
                            OrderItemModel.order_id == order_item.order_id
                        )
                    )
                )
            )
        )
        .scalars()
        .first()
    )

    if new_product_id:
        req.product_id = new_product_id
        req.count = 1
        data = await post_and_assert(
            req.model_dump(),
            201,
            "message",
            "Product added successfully",
        )
        assert data["created"] is True

    req.order_id = 100
    await post_and_assert(
        req.model_dump(),
        400,
        "detail",
        "Order with current order_id not found",
    )

    req.order_id = order_item.order_id
    req.product_id = 100
    await post_and_assert(
        req.model_dump(),
        400,
        "detail",
        "Product with current product_id not found",
    )
