import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from decimal import Decimal

from db import CategoryModel, ClientModel, ProductModel, OrderModel, OrderItemModel


async def seed_test_data(session: AsyncSession):
    # --- Проверка: есть ли уже данные ---
    existing = await session.scalar(select(CategoryModel.id))
    if existing:
        print("Test data already exists!")
        return

    categories = []

    # --- Уровень 1 (3 категории) ---
    electronics = CategoryModel(name="Electronics", parent_id=None, depth=1)
    home_appliances = CategoryModel(name="Home Appliances", parent_id=None, depth=1)
    gaming = CategoryModel(name="Gaming", parent_id=None, depth=1)
    session.add_all([electronics, home_appliances, gaming])
    await session.flush()
    categories.extend([electronics, home_appliances, gaming])

    # --- Уровень 2 ---
    computers = CategoryModel(name="Computers", parent_id=electronics.id, depth=2)
    phones = CategoryModel(name="Phones", parent_id=electronics.id, depth=2)
    tv_audio = CategoryModel(name="TV & Audio", parent_id=electronics.id, depth=2)

    kitchen = CategoryModel(name="Kitchen", parent_id=home_appliances.id, depth=2)
    laundry = CategoryModel(name="Laundry", parent_id=home_appliances.id, depth=2)

    consoles = CategoryModel(name="Consoles", parent_id=gaming.id, depth=2)
    accessories = CategoryModel(name="Accessories", parent_id=gaming.id, depth=2)

    session.add_all(
        [computers, phones, tv_audio, kitchen, laundry, consoles, accessories]
    )
    await session.flush()
    categories.extend(
        [computers, phones, tv_audio, kitchen, laundry, consoles, accessories]
    )

    # --- Уровень 3 ---
    laptops = CategoryModel(name="Laptops", parent_id=computers.id, depth=3)
    desktops = CategoryModel(name="Desktops", parent_id=computers.id, depth=3)
    smartphones = CategoryModel(name="Smartphones", parent_id=phones.id, depth=3)
    feature_phones = CategoryModel(name="Feature Phones", parent_id=phones.id, depth=3)
    headphones = CategoryModel(name="Headphones", parent_id=tv_audio.id, depth=3)
    tvs = CategoryModel(name="TVs", parent_id=tv_audio.id, depth=3)

    microwaves = CategoryModel(name="Microwaves", parent_id=kitchen.id, depth=3)
    fridges = CategoryModel(name="Fridges", parent_id=kitchen.id, depth=3)
    washing_machines = CategoryModel(
        name="Washing Machines", parent_id=laundry.id, depth=3
    )

    ps5 = CategoryModel(name="PlayStation 5", parent_id=consoles.id, depth=3)
    xbox = CategoryModel(name="Xbox Series X", parent_id=consoles.id, depth=3)
    gaming_accessories = CategoryModel(
        name="Gaming Accessories", parent_id=accessories.id, depth=3
    )

    session.add_all(
        [
            laptops,
            desktops,
            smartphones,
            feature_phones,
            headphones,
            tvs,
            microwaves,
            fridges,
            washing_machines,
            ps5,
            xbox,
            gaming_accessories,
        ]
    )
    await session.flush()
    categories.extend(
        [
            laptops,
            desktops,
            smartphones,
            feature_phones,
            headphones,
            tvs,
            microwaves,
            fridges,
            washing_machines,
            ps5,
            xbox,
            gaming_accessories,
        ]
    )

    # --- Продукты ---
    products_data = [
        {
            "name": "MacBook Pro",
            "category": laptops,
            "count": 5,
            "price": Decimal("2500.00"),
        },
        {
            "name": "Dell XPS 13",
            "category": laptops,
            "count": 10,
            "price": Decimal("1200.00"),
        },
        {
            "name": "iPhone 14",
            "category": smartphones,
            "count": 15,
            "price": Decimal("999.00"),
        },
        {
            "name": "Samsung Galaxy S23",
            "category": smartphones,
            "count": 20,
            "price": Decimal("850.00"),
        },
        {
            "name": "Gaming Desktop",
            "category": desktops,
            "count": 7,
            "price": Decimal("1800.00"),
        },
        {"name": "Sony TV", "category": tvs, "count": 8, "price": Decimal("1100.00")},
        {
            "name": "Bose Headphones",
            "category": headphones,
            "count": 12,
            "price": Decimal("300.00"),
        },
        {
            "name": "Nokia 3310",
            "category": feature_phones,
            "count": 50,
            "price": Decimal("50.00"),
        },
        {
            "name": "Microwave X200",
            "category": microwaves,
            "count": 6,
            "price": Decimal("200.00"),
        },
        {
            "name": "PS5 Console",
            "category": ps5,
            "count": 5,
            "price": Decimal("499.00"),
        },
    ]

    products = []
    for pdata in products_data:
        product = ProductModel(
            name=pdata["name"],
            category_id=pdata["category"].id,
            count=pdata["count"],
            price=pdata["price"],
        )
        session.add(product)
        products.append(product)

    await session.flush()

    # --- Клиенты ---
    clients = []
    for i in range(1, 11):
        client = ClientModel(name=f"Client {i}", address=f"{i} Main Street")
        session.add(client)
        clients.append(client)

    await session.flush()

    # --- Заказы ---
    orders = []
    for _ in range(10):
        client = random.choice(clients)
        order = OrderModel(client_id=client.id)
        session.add(order)
        orders.append(order)

    await session.flush()

    # --- Элементы заказов ---
    for order in orders:
        products_in_order = random.sample(products, k=random.randint(2, 4))
        for prod in products_in_order:
            order_item = OrderItemModel(
                order_id=order.id, product_id=prod.id, count=random.randint(1, 3)
            )
            session.add(order_item)

    await session.commit()
    print("Test data seeded successfully")
