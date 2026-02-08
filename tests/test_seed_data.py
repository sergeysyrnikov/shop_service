import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import OrderItemModel
from app.utils.db.fixtures_seed_data import seed_test_data


@pytest.mark.asyncio
async def test_seed_test_data(session: AsyncSession):
    await seed_test_data(session)

    result = await session.execute(select(OrderItemModel))
    order_items = result.scalars().all()

    assert len(order_items) > 0
