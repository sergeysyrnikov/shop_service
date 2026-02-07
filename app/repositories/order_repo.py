from sqlalchemy import select

from app.interfaces import Repository
from app.models import OrderModel


class OrderRepo(Repository):
    async def get_by_id(self, id: int) -> OrderModel | None:
        res = await self.session.execute(select(OrderModel).where(OrderModel.id == id))
        return res.scalar_one_or_none()
