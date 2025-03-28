import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.database.models import async_main


async def main():
    await async_main()
    bot = Bot(token = '7875015875:AAGPT2nyFrSh6rt5I25R7YHMaZV4ZL9oQl0')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot) #polling checks if something happend in chat with bot
    
if __name__ == "__main__":
    try:    
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot is off")