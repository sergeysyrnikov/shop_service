from typing import Sequence, Any

from sqlalchemy import select, func, RowMapping, text, Result

from app.interfaces import Repository
from app.models import ClientModel, ProductModel, OrderModel, OrderItemModel


class ClientRepo(Repository):
    async def get_by_id(self, id: int) -> ClientModel | None:
        raise NotImplementedError()

    async def get_total_per_client(
        self,
        with_orm: bool = False,
    ) -> Sequence[RowMapping]:
        res: Result[Any]
        if with_orm:
            res = await self.session.execute(
                select(
                    ClientModel.name.label("client_name"),
                    func.sum(OrderItemModel.count * ProductModel.price).label(
                        "total_sum"
                    ),
                )
                .join(OrderModel, OrderModel.client_id == ClientModel.id)
                .join(OrderItemModel, OrderItemModel.order_id == OrderModel.id)
                .join(ProductModel, ProductModel.id == OrderItemModel.product_id)
                .group_by(ClientModel.name)
                .order_by(ClientModel.name)
            )
        else:
            res = await self.session.execute(
                text("""
                    SELECT
                        c.name AS client_name,
                        SUM(oi.count * p.price) AS total_sum
                    FROM clients c
                             JOIN orders o
                                  ON o.client_id = c.id
                             JOIN order_items oi
                                  ON oi.order_id = o.id
                             JOIN products p
                                  ON p.id = oi.product_id
                    GROUP BY c.name
                    ORDER BY c.name
                    """)
            )
        return res.mappings().all()
