from pydantic import BaseModel


class CategoryResponse(BaseModel):
    name: str
    count_child: int
    depth: int
