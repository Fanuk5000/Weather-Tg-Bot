import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import routers

from app.database.models import async_database

from os import getenv
from dotenv import load_dotenv





async def main():
    load_dotenv("config.env")
    token = getenv("TELEGRAM_BOT_TOKEN")
    
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables.")
    
    await async_database()
    global bot
    bot = Bot(token)
    dp = Dispatcher()
    
    for router in routers:
        dp.include_router(router)
    
    await dp.start_polling(bot)  # Start polling

async def end_message_to_users():
    await bot.send_message(1094008377, "⚠️ Бота було вимкнено. Всі таймери не працюють після повторного запуску!\n\n")
    
if __name__ == "__main__":
    try:
        print("Bot is on")
        asyncio.run(main())
    except KeyboardInterrupt:
        asyncio.run(end_message_to_users())
        asyncio.run(bot.session.close())
        print("Bot is off")
    except Exception as e:
        print(e)