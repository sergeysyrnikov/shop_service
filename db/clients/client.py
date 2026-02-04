from sqlalchemy import BigInteger, Column, DateTime, String, func
from sqlalchemy.orm import relationship

from db.base import BaseModel


class ClientModel(BaseModel):
    __tablename__ = "clients"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    address = Column(String(100), default="")
    created_at = Column(DateTime, default=func.now(), nullable=False)

    orders = relationship("OrderModel", back_populates="client", lazy="selectin")

    def __repr__(self):
        return f"<Client id: {self.id}, name: {self.name}>"
