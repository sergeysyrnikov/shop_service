from sqlalchemy import (
    Column,
    BigInteger,
    ForeignKey,
    String,
    Integer,
    DECIMAL,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship

from db.base import BaseModel


class ProductModel(BaseModel):
    __tablename__ = "products"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    category_id = Column(BigInteger, ForeignKey("categories.id"), index=True)
    name = Column(String(50), nullable=False)
    count = Column(Integer, default=0, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    updated_at = Column(DateTime, default=func.now(), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    category = relationship("CategoryModel", back_populates="products", lazy="joined")
    order_items = relationship(
        "OrderItemModel", back_populates="product", lazy="selectin"
    )

    def __repr__(self):
        return f"<Product id: {self.id}, name: {self.name}, category_id: {self.category_id}>"
