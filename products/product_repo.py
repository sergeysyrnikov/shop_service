from sqlalchemy.ext.asyncio import AsyncSession


class ProductRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
