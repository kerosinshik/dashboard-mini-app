import asyncio
import random
from datetime import datetime, timedelta
from sqlalchemy import select
from database.models import init_db, async_session, User, Sale


# Список товаров для демо-данных
DEMO_PRODUCTS = [
    "Ноутбук MacBook Pro",
    "Смартфон iPhone 15",
    "Планшет iPad Air",
    "Наушники AirPods Pro",
    "Умные часы Apple Watch",
    "Клавиатура Magic Keyboard",
    "Мышь MX Master 3",
    "Монитор LG UltraWide",
    "Веб-камера Logitech",
    "Микрофон Blue Yeti",
    "SSD накопитель Samsung",
    "Внешний HDD Seagate",
    "Роутер Wi-Fi 6",
    "Принтер HP LaserJet",
    "Графический планшет Wacom"
]

# Статусы продаж
STATUSES = ["completed", "pending", "cancelled"]
STATUS_WEIGHTS = [0.75, 0.15, 0.10]  # 75% completed, 15% pending, 10% cancelled


async def create_demo_data(telegram_id: int, username: str = None, first_name: str = None):
    """Создание демо-данных для пользователя"""
    async with async_session() as session:
        # Проверяем, существует ли пользователь
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            # Создаем нового пользователя
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                is_demo=True
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
        else:
            # Удаляем старые демо-данные, если они были
            result = await session.execute(
                select(Sale).where(Sale.user_id == user.id)
            )
            old_sales = result.scalars().all()
            for sale in old_sales:
                await session.delete(sale)
            await session.commit()

        # Генерируем 50 случайных продаж за последние 30 дней
        sales = []
        for _ in range(50):
            # Случайная дата за последние 30 дней
            days_ago = random.randint(0, 30)
            sale_date = datetime.utcnow() - timedelta(days=days_ago)

            # Случайный товар
            product = random.choice(DEMO_PRODUCTS)

            # Случайная цена в зависимости от товара
            base_prices = {
                "Ноутбук MacBook Pro": 150000,
                "Смартфон iPhone 15": 90000,
                "Планшет iPad Air": 60000,
                "Наушники AirPods Pro": 25000,
                "Умные часы Apple Watch": 35000,
                "Клавиатура Magic Keyboard": 12000,
                "Мышь MX Master 3": 8000,
                "Монитор LG UltraWide": 45000,
                "Веб-камера Logitech": 15000,
                "Микрофон Blue Yeti": 18000,
                "SSD накопитель Samsung": 10000,
                "Внешний HDD Seagate": 6000,
                "Роутер Wi-Fi 6": 8000,
                "Принтер HP LaserJet": 20000,
                "Графический планшет Wacom": 30000
            }
            base_price = base_prices.get(product, 10000)
            amount = base_price * random.uniform(0.9, 1.1)  # ±10% от базовой цены

            # Случайное количество (обычно 1, иногда больше)
            quantity = random.choices([1, 2, 3], weights=[0.8, 0.15, 0.05])[0]

            # Случайный статус
            status = random.choices(STATUSES, weights=STATUS_WEIGHTS)[0]

            sale = Sale(
                user_id=user.id,
                product_name=product,
                amount=round(amount, 2),
                quantity=quantity,
                date=sale_date,
                status=status
            )
            sales.append(sale)

        # Сохраняем все продажи
        session.add_all(sales)
        await session.commit()

        print(f"✅ Создано {len(sales)} демо-продаж для пользователя {telegram_id}")
        return len(sales)


async def main():
    """Инициализация БД и создание тестовых данных"""
    await init_db()
    print("✅ База данных инициализирована")

    # Создание демо-данных для тестового пользователя
    await create_demo_data(
        telegram_id=123456789,
        username="test_user",
        first_name="Test"
    )


if __name__ == "__main__":
    asyncio.run(main())
