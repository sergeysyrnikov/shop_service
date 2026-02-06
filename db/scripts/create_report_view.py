from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def create_report_view(session: AsyncSession):
    result = await session.execute(
        text("""
             SELECT 1
             FROM information_schema.views
             WHERE table_schema = 'public'
               AND table_name = :view_name
             """),
        {"view_name": "report_view"},
    )

    if result.scalar():
        print("Report view already exists")
        return

    await session.execute(
        text("""
        CREATE OR REPLACE VIEW report_view AS
            WITH RECURSIVE category_tree AS (
                SELECT id, name, parent_id, name AS root_name
                FROM categories
                WHERE depth = 1
            
                UNION ALL
            
                SELECT c.id, c.name, c.parent_id, ct.root_name
                FROM categories c
                JOIN category_tree ct ON c.parent_id = ct.id
            ),
            sales_last_month AS (
                SELECT
                    p.name,
                    ct.root_name AS main_category,
                    SUM(oi.count) AS total_count,
                    DENSE_RANK() OVER (ORDER BY SUM(oi.count) DESC) AS rank
                FROM order_items oi
                JOIN products p ON p.id = oi.product_id
                JOIN category_tree ct ON ct.id = p.category_id
                WHERE oi.created_at >= date_trunc('month', now())
                GROUP BY p.name, ct.root_name
            )
            SELECT *
            FROM sales_last_month
            WHERE rank <= 5
            ORDER BY rank""")
    )

    await session.commit()
    print("Report view created successfully")
