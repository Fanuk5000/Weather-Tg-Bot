from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
 
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


import app.keyboard as kb
import app.database.requests as rq

from app.weather import get_weather

router = Router()


class Register(StatesGroup):
    name = State()
    city = State()

class Changecity(StatesGroup):
    new_city = State()

'''Commands'''

@router.message(CommandStart())
async def cmd_start(message:Message):
    await message.answer("You are welcome to illya`s bot!\nRegister to get weather(/register)", reply_markup=kb.main)
    
    # await message.reply("How are you?")

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("You pressed help")



@router.message(Command("change_city"))
async def change_city(message: Message, state: FSMContext):
    if await rq.check_user(message.from_user.id):
        await state.set_state(Changecity.new_city)
        await message.answer("Write your new city")
    else:
        await message.answer('You`ve not registered yet\nTo do it write "/register"')
        


@router.message(Command("weather"))
async def register(message: Message):
    await message.answer("Weather")


@router.message(Command("register"))
async def register(message: Message, state: FSMContext):
    if await rq.check_user(message.from_user.id):
        await message.answer("You are alredy registered")
    else:
        await state.set_state(Register.name)
        await message.answer("Write your name")

'''Commands'''

#change_city state
@router.message(Changecity.new_city)
async def changing(message: Message, state: FSMContext):
    await state.update_data(new_city = message.text)
    data = await state.get_data()
    await rq.change_city(message.from_user.id ,data["new_city"])
    
    await state.clear()
    await message.answer("Your city has been successfully changed")



#register state
@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(Register.city)
    await message.answer("Write your city")

#register state
@router.message(Register.city)
async def register_city(message: Message, state: FSMContext):
    await state.update_data(city = message.text)
    data = await state.get_data()
    
    
    await rq.set_user(message.from_user.id, data["name"], data["city"])

    await message.answer(f'Your name: {data["name"]}\nYour city: {data["city"]}')
    await state.clear()

@router.message(F.text == "Today`s")
async def register(message: Message):
    if await rq.check_user(message.from_user.id):
        city = await rq.get_user_city(message.from_user.id)
        temperature = await get_weather("Kyiv")
        
        await message.answer(f"temperature in {city} is {temperature}°C")
    else:
        await message.answer("You`ve not registered yet, to do it /register")

# @router.callback_query(F.data.startswith('category_'))
# async def category(callback: CallbackQuery):
#     await callback.answer('You`ve choosen category')
#     await callback.message.answer('Choose product by category',
#                                   reply_markup=await kb.items(callback.data.split('_')[1]))
    
# @router.callback_query(F.data == "weather")
# async def weather(callback: CallbackQuery):
#     await callback.answer("Weather")#show_alert
#     await callback.message.answer("You`ve choosen weather")
