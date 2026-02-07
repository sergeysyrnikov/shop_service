import os

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func

from app.models import BaseModel
from app.utils.db import get_type_pk


class OrderItemModel(BaseModel):
    __tablename__ = "order_items"

    id = Column(get_type_pk(), primary_key=True, autoincrement=True)
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
    count = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    order = relationship("OrderModel", back_populates="order_items")
    product = relationship("ProductModel", back_populates="order_items")

    __table_args__ = (
        UniqueConstraint("order_id", "product_id", name="uq_order_product"),
    )

    def __repr__(self):
        return f"<OrderItem id: {self.id}, order_id: {self.order_id}, product_id: {self.product_id}>"
