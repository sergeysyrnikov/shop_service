from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class CategoryRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_count_child(self, with_orm: bool):
        if with_orm:
            print("lala")
            pass
        else:
            res = await self.session.execute(text("""with recursive parent as (
                            select c.name, c.id, c.depth, c.name::text as path from categories c where parent_id is null
                                union all
                            select c.name, c.id, c.depth, p.path || ' > ' || c.name as path from categories c join parent p on c.parent_id = p.id
                            ) select * from parent"""))
            print(res.mappings().all())
