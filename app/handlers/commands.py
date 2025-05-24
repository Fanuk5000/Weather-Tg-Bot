from .common_imports import *

from app.weather import get_city_coordinates, get_current_weather

commands_router = Router()

class SetCity(StatesGroup):
    city = State()

class ChangeCity(StatesGroup):
    new_city = State()

class WeatherNow(StatesGroup):
    city = State()

#-------------start command-----------------
@commands_router.message(CommandStart())
async def cmd_start(message:Message):
    await message.answer("""Ласкаво просимо до погодного боту \"FaneraWeather\"!
Ви можете обрати город(/setcity) для постійного моніторингу погоди у вашому місті або просто дізнатись температуру у вашому місті (/weathernow).
                         """, reply_markup=kb.main)

#-------------answer not registered-----------------
@commands_router.message(lambda message: message.from_user.id == 1094008377 and message.text == "admin")
async def answer_not_registered(message:Message):
    await message.answer("Щоб користуватись кнопками, вкажіть город город(/setcity)", reply_markup=kb.main)

#-------------set city-----------------
@commands_router.message(Command("setcity"))
async def register(message: Message, state: FSMContext):
    if await rq.check_user(message.from_user.id):
        await message.answer("Ви вже вказали город\nЯкщо хочете його змінити \"/change_city\"")
    else:
        await state.set_state(SetCity.city)
        await message.answer("Напишіть назву міста")

@commands_router.message(SetCity.city)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(city = message.text)
    data = await state.get_data()
    await rq.set_user(message.from_user.id, data["city"])
    await message.answer(f"Ви успішно вказали город!", reply_markup=kb.main)
    await state.clear()


#---------test command-----------------
@commands_router.message(Command("test"))
async def cmd_start(message:Message):
    # await message.answer(str(await get_city_coordinates("Kyiv")))
    await get_city_coordinates("Kyiv")

#---------help command-----------------
@commands_router.message(Command("help"))
async def cmd_help(message: Message):
    await answer_not_registered(message)
    
#----------change city command-----------------
@commands_router.message(Command("changecity"))
async def change_city(message: Message, state: FSMContext):
    if await rq.check_user(message.from_user.id):
        await state.set_state(ChangeCity.new_city)
        await message.answer("Напишіть нове місто")
    else:
        await answer_not_registered(message)
        
@commands_router.message(ChangeCity.new_city)
async def changing(message: Message, state: FSMContext):
    await state.update_data(new_city = message.text)
    data = await state.get_data()
    await rq.change_city(message.from_user.id ,data["new_city"])
    
    await state.clear()
    await message.answer("Місто було успішно змінено")
        
        
#------weather now command----------------
@commands_router.message(Command("weathernow"))
async def get_curreant_weather(message: Message, state: FSMContext):
    await state.set_state(WeatherNow.city)
    await message.answer("Напишіть місто, в якому хочете дізнатись погоду")
    
@commands_router.message(WeatherNow.city)
async def register(message: Message, state: FSMContext):
    await state.update_data(city = message.text)
    
    state_data = await state.get_data()
    dict = await get_current_weather(state_data["city"])
    await state.clear()
    
    await message.answer(f"Зараз у городі {state_data["city"]} {dict["temp"]} °C й {dict["description"]}")
    