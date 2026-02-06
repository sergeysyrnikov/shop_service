import decimal

from pydantic import BaseModel


class AddProductRequest(BaseModel):
    id_order: int
    id_category: int
    count: decimal.Decimal
