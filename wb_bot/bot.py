import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from bot.handlers import register_handlers
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
import os
from bot.data import load_user_data, save_user_data

# Загружаем переменные окружения
load_dotenv()

# Получаем API_TOKEN из переменных окружения
API_TOKEN = os.getenv('API_TOKEN')

if not API_TOKEN:
    raise ValueError("API_TOKEN не найден в .env файле")

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)


# Главная функция для запуска бота
async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    # Планировщик
    scheduler = AsyncIOScheduler()

    # Загрузка данных пользователей при старте
    load_user_data()

    # Регистрируем обработчики
    register_handlers(dp, bot, scheduler)

    # Запускаем планировщик
    scheduler.start()

    # Запускаем long-polling
    try:
        await dp.start_polling(bot)
    finally:
        # Сохранение данных пользователей при завершении работы
        save_user_data()


# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
