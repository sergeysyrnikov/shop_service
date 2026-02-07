import os

from sqlalchemy import Integer, BigInteger


def get_type_pk() -> type[Integer | BigInteger]:
    if os.environ.get("TESTING") == "1":
        return Integer
    return BigInteger
