from pydantic import BaseModel


class AddProductRequest(BaseModel):
    order_id: int
    product_id: int
    count: int


class AddProductResponse(BaseModel):
    message: str
    created: bool
