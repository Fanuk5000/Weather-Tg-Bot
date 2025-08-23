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
async def comand_start(message:Message):
    await message.answer("""Ласкаво просимо до погодного боту «FaneraWeather»!
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
async def register_name_state(message: Message, state: FSMContext):
    await state.update_data(city = message.text)
    data = await state.get_data()
    await rq.set_user(message.from_user.id, data["city"], await get_city_coordinates(data["city"]))
    await message.answer(f"Ви успішно вказали город!", reply_markup=kb.main)
    await state.clear()


#---------test command-----------------
@commands_router.message(Command("test"))
async def command_test(message:Message):
    await message.answer("Error occurred!", show_alert=True)
    # await rq.set_plan_time(message.from_user.id, None)

#---------help command-----------------
@commands_router.message(Command("help"))
async def cmd_help(message: Message):
    avaible_commands = [
        {"command": "/start", "description": "Ласкаво просимо до погодного боту «FaneraWeather»!"},
        {"command": "/setcity", "description": "Вказати місто для постійного моніторингу погоди"},
        {"command": "/changecity", "description": "Змінити місто для моніторингу погоди"},
        {"command": "/weathernow", "description": "Дізнатись поточну погоду у вказаному місті"},
        {"command": "/test", "description": "Тестова команда для скидання часу планування"},
        {"command": "/help", "description": "Показати список доступних команд"},
        {"command": "/timermenu", "description": "Виводить меню таймера"},
        {"command": "/enableplantimer", "description": "Вмикає таймер планування"},
        {"command": "/donate", "description": "Підтримати проєкт"},
        
    ]
    help_text = "Доступні команди:\n\n" + "\n".join([f"{cmd['command']} - {cmd['description']}" for cmd in avaible_commands])
    await message.answer(help_text)


#----------change city command-----------------
@commands_router.message(Command("changecity"))
async def change_city(message: Message, state: FSMContext):
    if await rq.check_user(message.from_user.id):
        await state.set_state(ChangeCity.new_city)
        await message.answer("Напишіть нове місто")
    else:
        await answer_not_registered(message)
        
@commands_router.message(ChangeCity.new_city)
async def change_city_state(message: Message, state: FSMContext):
    await state.update_data(new_city = message.text)
    data = await state.get_data()
    await rq.change_city(message.from_user.id, data["new_city"], await get_city_coordinates(data["new_city"]))
    
    await state.clear()
    await message.answer("Місто було успішно змінено")
        
        
#------weather now command----------------
@commands_router.message(Command("weathernow"))
async def getting_current_weather(message: Message, state: FSMContext):
    await state.set_state(WeatherNow.city)
    await message.answer("Напишіть місто, в якому хочете дізнатись погоду")
    
@commands_router.message(WeatherNow.city)
async def getting_current_weather_state(message: Message, state: FSMContext):
    await state.update_data(city = message.text)
    
    state_data = await state.get_data()
    weather = await get_current_weather(state_data["city"])
    await state.clear()
    
    await message.answer(weather)

@commands_router.message(Command("donate"))
async def donate(message: Message):
    help_text = dedent("""
    🔗Посилання на банку(mono)
    https://send.monobank.ua/jar/2hyPuvj2ds

    💳Номер картки банки
    ```4441 1111 2239 4046```

    Дякую за підтримку!
    """)
    await message.answer(help_text, parse_mode="Markdown")