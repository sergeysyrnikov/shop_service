from app.interfaces.base_service import BaseService
from app.repositories.order_item_repo import OrderItemRepo
from app.repositories.order_repo import OrderRepo
from app.repositories.product_repo import ProductRepo
from app.models import OrderItemModel


class ProductService(BaseService):
    def __init__(self, session):
        super().__init__(session)
        self.order_repo = OrderRepo(session)
        self.product_repo = ProductRepo(session)
        self.order_item_repo = OrderItemRepo(session)

    async def add_product_into_order(
        self, order_id: int, product_id: int, quantity: int
    ) -> tuple[ValueError | None, bool]:
        order = await self.order_repo.get_by_id(order_id)
        if order is None:
            return ValueError("Order with current order_id not found"), False
        product = await self.product_repo.get_for_update(product_id)
        if product is None:
            return ValueError("Product with current product_id not found"), False

        if product.count < quantity:
            return (
                ValueError("Product with current product_id is less than quantity"),
                False,
            )

        product.count -= quantity

        order_item = await self.order_item_repo.get_by_order_id_and_product_id(
            order_id, product_id
        )
        is_created = True
        if order_item is None:
            order_item = OrderItemModel(
                order_id=order_id, product_id=product_id, count=quantity
            )
            self.session.add(order_item)
        else:
            is_created = False
            order_item.count += quantity

        await self.session.commit()
        return None, is_created
