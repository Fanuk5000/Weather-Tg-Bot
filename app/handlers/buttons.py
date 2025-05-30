from .common_imports import *

from app.weather import get_current_weather, get_city_coordinates, get_tomorrow_weather, get_weather_for_3_days, get_weather_to_end

buttons_router = Router()

#-------------answer not registered-----------------
@buttons_router.message(lambda message: message.from_user.id == 1094008377 and message.text == "admin")
async def answer_not_registered(message:Message):
    await message.answer("Щоб користуватись кнопками, вкажіть город город(/setcity) button", reply_markup=kb.main)

@buttons_router.message(F.text == "Поточна")
async def register(message: Message):
    if await rq.check_user(message.from_user.id):
        city = await rq.get_user_city(message.from_user.id)
        weather = await get_current_weather(city)
        
        await message.answer(weather)
    else:
        await answer_not_registered(message)

@buttons_router.message(F.text == "До кінця дня")
async def register(message: Message):
    if await rq.check_user(message.from_user.id):
        city = await rq.get_user_city(message.from_user.id)
        weather = await get_weather_to_end(city)
        
        await message.answer(f"Погода до кінця дня у {city}:")
        await message.answer(weather)
    else:
        await answer_not_registered(message)

@buttons_router.message(F.text == "Завтрашня")
async def register(message: Message):
    if await rq.check_user(message.from_user.id):
        city = await rq.get_user_city(message.from_user.id)
        weather = await get_tomorrow_weather(city)
        
        await message.answer(f"Завтрашня температура у {city}:")
        await message.answer(weather)
    else:
        await answer_not_registered(message)
        
@buttons_router.message(F.text == "3 дні")
async def register(message: Message):
    if await rq.check_user(message.from_user.id):
        city = await rq.get_user_city(message.from_user.id)
        weather = await get_weather_for_3_days(city)
        
        await message.answer(f"Погода на 3 дні у {city}:")
        await message.answer(weather)
    else:
        await answer_not_registered(message)