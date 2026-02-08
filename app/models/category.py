from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models import BaseModel
from app.utils.db import get_type_pk


class CategoryModel(BaseModel):
    __tablename__ = "categories"

    id = Column(get_type_pk(), primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    parent_id = Column(
        BigInteger,
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    depth = Column(Integer, nullable=False, default=1)

    products = relationship("ProductModel", back_populates="category", lazy="selectin")

    def __repr__(self):
        return f"<Category id: {self.id}, name: {self.name}>"
