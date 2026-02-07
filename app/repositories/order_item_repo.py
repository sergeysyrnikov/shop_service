from sqlalchemy import select

from app.interfaces import Repository
from app.models import OrderItemModel


class OrderItemRepo(Repository):
    async def get_by_id(self, id: int) -> OrderItemModel | None:
        res = await self.session.execute(
            select(OrderItemModel).where(OrderItemModel.id == id)
        )
        return res.scalar_one_or_none()

    async def get_by_order_id_and_product_id(
        self, order_id: int, product_id: int
    ) -> OrderItemModel | None:
        res = await self.session.execute(
            select(OrderItemModel).where(
                OrderItemModel.order_id == order_id,
                OrderItemModel.product_id == product_id,
            )
        )
        return res.scalar_one_or_none()
