from typing import Sequence, Any

from sqlalchemy import text, RowMapping, Result, select, literal, func
from sqlalchemy.orm import aliased

from app.interfaces import Repository
from app.models import CategoryModel


class CategoryRepo(Repository):
    async def get_by_id(self, id: int) -> CategoryModel | None:
        raise NotImplementedError()

    async def get_count_child(self, with_orm: bool) -> Sequence[RowMapping]:
        res: Result[Any]

        if with_orm:
            # --- базовая часть CTE ---
            parent = (
                select(
                    CategoryModel.id,
                    CategoryModel.name,
                    CategoryModel.depth,
                    CategoryModel.id.label("root_id"),
                    literal(None).cast(CategoryModel.name.type).label("root_name"),
                )
                .where(CategoryModel.parent_id.is_(None))
                .cte("parent", recursive=True)
            )

            c = aliased(CategoryModel)
            p = aliased(parent)

            # --- рекурсивная часть ---
            parent = parent.union_all(
                select(
                    c.id,
                    c.name,
                    c.depth,
                    p.c.id.label("root_id"),
                    p.c.name.label("root_name"),
                ).join(p, c.parent_id == p.c.id)
            )

            # алиас для детей
            ch = aliased(CategoryModel)

            # --- финальный запрос ---
            stmt = (
                select(
                    parent.c.name,
                    func.count(ch.id).label("count_child"),
                    func.min(parent.c.depth).label("depth"),
                )
                .select_from(parent)
                .outerjoin(ch, ch.parent_id == parent.c.id)
                .group_by(parent.c.id, parent.c.name, parent.c.root_name)
                .order_by(parent.c.id)
            )

            res = await self.session.execute(stmt)

        else:
            res = await self.session.execute(
                text("""
                    WITH RECURSIVE parent AS (
                        SELECT
                            c.id,
                            c.name,
                            c.depth,
                            c.id AS root_id,
                            NULL::text AS root_name
                        FROM categories c
                        WHERE parent_id IS NULL

                        UNION ALL

                        SELECT
                            c.id,
                            c.name,
                            c.depth,
                            p.id AS root_id,
                            p.name AS root_name
                        FROM categories c
                                 JOIN parent p ON c.parent_id = p.id
                    )

                    SELECT
                        p.name,
                        COUNT(ch.id) AS count_child,
                        MIN(p.depth) AS depth
                    FROM parent p
                             LEFT JOIN categories ch
                                       ON ch.parent_id = p.id
                    GROUP BY p.id, p.name, p.root_name
                    ORDER BY p.id
                    """)
            )

        return res.mappings().all()
