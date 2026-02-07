import os

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, func, Integer
from sqlalchemy.orm import relationship

from app.models import BaseModel
from app.utils.db import get_type_pk


class OrderModel(BaseModel):
    __tablename__ = "orders"

    id = Column(get_type_pk(), primary_key=True, autoincrement=True)
    client_id = Column(
        BigInteger,
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    updated_at = Column(DateTime, default=func.now(), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    client = relationship("ClientModel", back_populates="orders")
    order_items = relationship(
        "OrderItemModel", back_populates="order", lazy="selectin"
    )

    def __repr__(self):
        return f"<Order id: {self.id}, client_id: {self.client_id}>"
