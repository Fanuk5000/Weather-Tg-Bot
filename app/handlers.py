from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
 
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


import app.keyboard as kb
import app.database.requests as rq

from app.weather import get_current_weather, get_city_coordinates, get_tomorrow_weather, get_weather_for_3_days

router = Router()


class Register(StatesGroup):
    name = State()
    city = State()

class Changecity(StatesGroup):
    new_city = State()

class Askweather(StatesGroup):
    city = State() 

@router.message(lambda message: message.from_user.id == 1094008377 and message.text == "admin")
async def answer_not_registered(message:Message):
    await message.answer("Ви ще не зареєстровані\nЩоб це зробити напишіть /register", reply_markup=kb.main)

'''Commands'''

@router.message(CommandStart())
async def cmd_start(message:Message):
    await message.answer("Ласкаво просимо до погодного боту \"FaneraWeather\"!\nВи можете зареєструватись через(/register) ", reply_markup=kb.main)

@router.message(Command("test"))
async def cmd_start(message:Message):
    # await message.answer(str(await get_city_coordinates("Kyiv")))
    await get_city_coordinates("Kyiv")

@router.message(Command("help"))
async def cmd_help(message: Message):
    await answer_not_registered(message)
    # await message.answer("You pressed help")



@router.message(Command("changecity"))
async def change_city(message: Message, state: FSMContext):
    if await rq.check_user(message.from_user.id):
        await state.set_state(Changecity.new_city)
        await message.answer("Напишіть нове місто")
    else:
        await answer_not_registered(message)



@router.message(Command("weather"))
async def register(message: Message, state: FSMContext):
    await state.set_state(Askweather.city)
    await message.answer("Напишіть місто, в якому хочете дізнатись погоду")


@router.message(Command("register"))
async def register(message: Message, state: FSMContext):
    if await rq.check_user(message.from_user.id):
        await message.answer("Ви вже зареєстровані\nЯкщо хочете змінити місто \"/change_city\"")
    else:
        await state.set_state(Register.name)
        await message.answer("Напишіть нікнейм")


'''States'''

#Ask_weather state
@router.message(Askweather.city)
async def register(message: Message, state: FSMContext):
    await state.update_data(city = message.text)
    
    data = await state.get_data()
    temperature = await get_current_weather(data["city"])
    
    await message.answer(f"Зараз температура {temperature} у {data["city"]} °C")
    await state.clear()




#change_city state
@router.message(Changecity.new_city)
async def changing(message: Message, state: FSMContext):
    await state.update_data(new_city = message.text)
    data = await state.get_data()
    await rq.change_city(message.from_user.id ,data["new_city"])
    
    await state.clear()
    await message.answer("Місто було успішно змінено")



#register state
@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(Register.city)
    await message.answer("Напишіть місто, де хочете бачити погоду")

#register state
@router.message(Register.city)
async def register_city(message: Message, state: FSMContext):
    await state.update_data(city = message.text)
    data = await state.get_data()
    
    
    await rq.set_user(message.from_user.id, data["name"], data["city"])

    await message.answer(f'Ваш нікнейм: {data["name"]}\nВи обрали город: {data["city"]}')
    await state.clear()


'''Buttons'''
@router.message(F.text == "Поточна")
async def register(message: Message):
    if await rq.check_user(message.from_user.id):
        city = await rq.get_user_city(message.from_user.id)
        temperature = await get_current_weather(city)
        
        await message.answer(f"Зараз температура {temperature} у {city} °C")
    else:
        await answer_not_registered(message)
    
@router.message(F.text == "Завтрашня")
async def register(message: Message):
    if await rq.check_user(message.from_user.id):
        city = await rq.get_user_city(message.from_user.id)
        temperature = await get_tomorrow_weather(city)
        
        
        await message.answer(f"Завтрашня температура у {city}:")
        if isinstance(temperature, list):
            concatenated = "\n".join(temperature[::3])
            await message.answer(concatenated)
    else:
        await answer_not_registered(message)
        
@router.message(F.text == "3 дні")
async def register(message: Message):
    if await rq.check_user(message.from_user.id):
        city = await rq.get_user_city(message.from_user.id)
        temperature = await get_weather_for_3_days(city)
        
        if isinstance(temperature, dict):
            for date, weather in temperature.items():
                await message.answer(f"{date}:\n {weather}")
        
        
    else:
        await answer_not_registered(message)

# @router.callback_query(F.data.startswith('category_'))
# async def category(callback: CallbackQuery):
#     await callback.answer('You`ve choosen category')
#     await callback.message.answer('Choose product by category',
#                                   reply_markup=await kb.items(callback.data.split('_')[1]))
    
# @router.callback_query(F.data == "weather")
# async def weather(callback: CallbackQuery):
#     await callback.answer("Weather")#show_alert
#     await callback.message.answer("You`ve choosen weather")
