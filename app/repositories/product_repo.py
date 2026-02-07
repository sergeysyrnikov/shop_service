from sqlalchemy import select

from app.interfaces import Repository
from app.models import ProductModel


class ProductRepo(Repository):
    async def get_by_id(self, id: int) -> ProductModel:
        res = await self.session.execute(
            select(ProductModel).where(ProductModel.id == id)
        )
        return res.scalar_one_or_none()

    async def get_for_update(self, product_id: int) -> ProductModel | None:
        result = await self.session.execute(
            select(ProductModel).where(ProductModel.id == product_id).with_for_update()
        )
        return result.scalar_one_or_none()
