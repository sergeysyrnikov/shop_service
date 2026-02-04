from sqlalchemy import BigInteger, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func

from db.base import BaseModel


class OrderItemModel(BaseModel):
    __tablename__ = "order_items"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(
        BigInteger,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_id = Column(
        BigInteger,
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at = Column(DateTime, default=func.now(), nullable=False)

    order = relationship("OrderModel", back_populates="order_items")
    product = relationship("ProductModel", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem id: {self.id}, order_id: {self.order_id}, product_id: {self.product_id}>"
