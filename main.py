import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import routers

from app.database.models import async_main

from os import getenv
from dotenv import load_dotenv



async def main():
    load_dotenv("config.env")
    token = getenv("TELEGRAM_BOT_TOKEN")
    
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables.")
    
    await async_main()
    bot = Bot(token)
    dp = Dispatcher()
    
    for router in routers:
        dp.include_router(router)
    
    #await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot) #polling checks if something happend in chat with bot

if __name__ == "__main__":
    try:
        print("Bot is on")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot is off")
    except Exception as e:
        print(e)