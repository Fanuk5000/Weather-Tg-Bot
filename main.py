import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import routers
from app.handlers import set_bot

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
    set_bot(bot)  # Set the bot in the handlers
    
    for router in routers:
        dp.include_router(router)
    
    await dp.start_polling(bot)  # Start polling

if __name__ == "__main__":
    try:
        print("Bot is on")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot is off")
    except Exception as e:
        print(e)