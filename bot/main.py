import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from bot.handlers import router

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Главная функция запуска бота"""
    # Получение токена бота
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        logger.error("BOT_TOKEN не найден в переменных окружения!")
        return

    # Инициализация бота и диспетчера
    bot = Bot(token=bot_token)
    dp = Dispatcher()

    # Регистрация роутера с обработчиками
    dp.include_router(router)

    # Удаление webhook и запуск polling
    await bot.delete_webhook(drop_pending_updates=True)

    logger.info("Бот запущен и готов к работе!")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
