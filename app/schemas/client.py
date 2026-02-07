import decimal

from pydantic import BaseModel


class ClientResponse(BaseModel):
    client_name: str
    total_sum: decimal.Decimal
