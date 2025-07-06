import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers.basic import router as basic_router
from filters.is_admin import IsAdmin
from utils.db import init_db

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

async def main():
    # Проверяем токен
    if not BOT_TOKEN:
        logging.error("BOT_TOKEN не найден в переменных окружения!")
        return
    
    # Инициализируем бота и диспетчер
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Регистрируем роутеры
    dp.include_router(basic_router)
    
    # Инициализируем базу данных
    await init_db()
    logging.info("База данных инициализирована")
    
    # Запускаем бота
    logging.info("Бот запускается...")
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logging.info("Бот остановлен")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
