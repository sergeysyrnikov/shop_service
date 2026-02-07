from pydantic import BaseModel


class AppResponse(BaseModel):
    message: str
    db_connected: bool
