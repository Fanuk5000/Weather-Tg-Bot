from .common_imports import *
from asyncio import sleep
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from datetime import datetime

from ..weather import get_current_weather, get_weather_to_end, get_tomorrow_weather, get_weather_for_3_days
class Timers:
    class PlanTimer(StatesGroup):
        time = State()
        days = State()
        format_time = State()
        
    
    def __init__(self):
        self.bot = None
        self.plan_timer_working = False
        self.router = Router()
        self.TIME_TO_DELETE = 5
        self.scheduler = AsyncIOScheduler()

        self.router.message.register(self.plan_timer_menu, Command("timermenu"))
        # self.router.message.register(self.stop_plan_timer, Command("stopplantimer"))
        self.router.message.register(self.stop_plan_timer, Command("repeatplantimer"))
        self.router.message.register(self.handle_plan_timer, Timers.PlanTimer.time)
        self.router.message.register(self.handle_interval_days, Timers.PlanTimer.days)
        self.router.message.register(self.handle_weather_format, Timers.PlanTimer.format_time)
        
        self.router.callback_query.register(self.stop_plan_timer, F.data =="stop_plan_timer")
        self.router.callback_query.register(self.callback_plan_timer, F.data == "plan_timer")
        self.router.callback_query.register(self.enable_plan_timer, F.data == "enable_plan_timer")
        
        self.router.callback_query.register(self.weather_format, F.data == "weather_format")
        self.router.callback_query.register(self.timer_info, F.data == "timer_info")
        self.router.callback_query.register(self.interval_plan_timer, F.data == "interval_plan_timer")
        
    async def plan_timer_menu(self, message: Message):
        if await rq.check_user(message.from_user.id) is False:
            await message.answer("Щоб користуватись таймером, вкажіть город(/setcity)")
            return
        
        await message.answer("Меню для користування таймером.\nЩоб подивитись функціонал, дивиться \"Інфо\".",
                             parse_mode="HTML", reply_markup=kb.plan_time_keys)
    
    # Callback for the plan timer
    async def callback_plan_timer(self, callback: CallbackQuery, state: FSMContext):
        if await rq.check_user(callback.from_user.id) is False:
            await callback.message.answer("Щоб користуватись таймером, вкажіть город(/setcity)")
            return
        
        if self.plan_timer_working:
            await callback.answer("Таймер вже запущено, зупиніть його перед встановленням нового часу")
            return
        
        await state.set_state(Timers.PlanTimer.time)
        temp_message = await callback.message.answer("Введіть час у форматі 00:00")
        
        await sleep(self.TIME_TO_DELETE)
        await temp_message.delete()
        await callback.answer("")

    # Handle the time input for the plan timer
    async def handle_plan_timer(self, message: Message, state: FSMContext):
        await state.update_data(time = message.text)
        data = await state.get_data()
        
        try:
            hour, minute = map(int, data["time"].strip().split(":"))
            if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                raise ValueError("Invalid time format")
        except ValueError:
            temp_message = await message.answer("Невірний формат часу. Спробуйте ще раз")
        except Exception as e:
            temp_message = await message.answer("Щось пішло не так. Спробуйте ще раз")
            print(e)
        else:
            await rq.set_plan_time(message.from_user.id, data["time"])
            
            temp_message = await message.answer(f"Таймер заплановано на {data['time']}, тепер можна його запустити")\
        
        await state.clear()
        await sleep(self.TIME_TO_DELETE)
        await temp_message.delete()
        await message.delete()
    
    async def timer_info(self, callback: CallbackQuery):
        if await rq.check_user(callback.from_user.id) is False:
            await callback.message.answer("Щоб користуватись таймером, вкажіть город(/setcity)")
            return
        
        time = await rq.get_plan_time(callback.from_user.id)
        planned_time = f"встановлено на {time}" if time  else "не встановлено"
        on_off = "включений" if self.plan_timer_working else "вимкнений"
        interval = await rq.get_days_interval(callback.from_user.id)
        formats = ["Поточна погода", "Погода на завтра", "Погода на 3 дні", "Погода до кінця дня"]
        weather_format = await rq.get_weather_format(callback.from_user.id)
        
        temp_message = await callback.message.answer(f"Зараз таймер <b>{on_off}</b>, час якого <b>{planned_time}</b>.\n"
                                      f"З інтервалом кожні <b>{interval}</b> днів(якщо 0 таймер одноразовий) та форматом <b>{formats[weather_format-1]}</b>", parse_mode="HTML")
        await sleep(10)
        await temp_message.delete()
        await callback.answer("")
        
    
    # Stop the plan timer
    async def stop_plan_timer(self, callback: CallbackQuery):
        if await rq.check_user(callback.from_user.id) is False:
            await callback.message.answer("Щоб користуватись таймером, вкажіть город(/setcity)")
            return
        
        if self.plan_timer_working:
            self.plan_timer_working = False
            self.scheduler.remove_job(f"weather_timer_{callback.from_user.id}")
            await callback.answer("Таймер зупинено")
        else:
            await callback.answer("Таймер не запущено")
    
    async def interval_plan_timer(self, callback: CallbackQuery, state: FSMContext):
        if await rq.check_user(callback.from_user.id) is False:
            await callback.answer("Щоб користуватись таймером, вкажіть город(/setcity)")
            return
        
        if await rq.check_plan_time(callback.from_user.id) is False:
            await callback.answer("Час не встановлено, встановіть його.")
            return
        
        await state.set_state(Timers.PlanTimer.days)
        temp_message = await callback.message.answer("Введіть переодичність таймера в днях")
        
        await sleep(self.TIME_TO_DELETE)
        await temp_message.delete()
        await callback.answer("")
    
    async def handle_interval_days(self, message:Message, state: FSMContext):
        await state.update_data(days =  message.text)
        data = await state.get_data()
        
        try:
            reapeat_in_days = int(data["days"].strip())
            if reapeat_in_days < 0:
                raise ValueError("Days must be greater than 0")
            await rq.set_days_interval(message.from_user.id, reapeat_in_days)
            interval = f"буде повторюватись кожні {reapeat_in_days} днів" if reapeat_in_days > 0 else "одноразовий"
            
            temp_message = await message.answer(f"Таймер {interval}")
        except ValueError:
            temp_message = await message.answer("Невірний формат."
                                                "Введіть невід'ємні цілі числа")
        await state.clear()
        await sleep(self.TIME_TO_DELETE)
        await temp_message.delete()
        await message.delete()

    
    # Enable the plan timer and start checking the time
    async def enable_plan_timer(self, callback: CallbackQuery):
        if self.plan_timer_working:
            await callback.answer("Таймер вже запущено")
            return
        
        plan_time = await rq.get_plan_time(callback.from_user.id)
        if not plan_time:
            await callback.answer("Час не встановлено, встановіть його.")
            return
        
        self.plan_timer_working = True
        
        city = await rq.get_user_city(callback.from_user.id)
        reapeat_in_days = await rq.get_days_interval(callback.from_user.id)
        weather_format = await rq.get_weather_format(callback.from_user.id)
        
        plan_hour, plan_minute = map(int, plan_time.split(":"))
        chat_id = callback.from_user.id
        
        await callback.answer(
            f"Таймер запущено, він буде працювати {'кожні ' + str(reapeat_in_days) + ' днів' if reapeat_in_days else 'один раз'}"
        )
        if reapeat_in_days == 0:
            self.scheduler.add_job(self.send_weather_update, "cron", hour=plan_hour,
                                   minute = plan_minute, args=[chat_id, city, weather_format, reapeat_in_days],
                                   id=f"weather_timer_{chat_id}", replace_existing=True)
        else:
            self.scheduler.add_job(self.send_weather_update, "interval", days=reapeat_in_days,
                                   start_date=datetime.now().replace(hour=plan_hour, minute=plan_minute, second=0, microsecond=0),
                                   replace_existing=True,
                                   args=[chat_id, city, weather_format, reapeat_in_days],
                                   id=f"weather_timer_{chat_id}")
        self.scheduler.start()
    
    async def send_weather_update(self, chat_id: int, city:str,
                                  weather_format:int, reapeat_in_days:int):
        weather_functions = {
            1: get_current_weather,
            2: get_weather_to_end,
            3: get_tomorrow_weather,
            4: get_weather_for_3_days
        }
        
        weather = await weather_functions.get(weather_format, lambda _:
            "Яким чином ти це зробив? Такого формату не існує")(city)

        repeat_or_not = "Одноразовий таймер" if reapeat_in_days == 0 else f"Таймер повториться через {reapeat_in_days} {"день" if reapeat_in_days == 1 else "днів"}"
        
        await self.bot.send_message(chat_id, text=f"Погода в місті {city}:\n\n{weather}\n\n{repeat_or_not}.\n")
        
        if reapeat_in_days == 0:
            self.plan_timer_working = False
            self.scheduler.remove_job(f"weather_timer_{chat_id}")
            await self.bot.send_message(chat_id, text="Таймер зупинено після одноразового сповіщення")
        else:
            await self.bot.send_message(chat_id, text=f"Таймер спрацював, наступне сповіщення буде через {reapeat_in_days} днів")
        
    async def weather_format(self, callback: CallbackQuery, state: FSMContext):
        if await rq.check_user(callback.from_user.id) is False:
            temp_message1 = await callback.message.answer("Щоб користуватись таймером, вкажіть город(/setcity)")
            return
        
        await state.set_state(Timers.PlanTimer.format_time)
        temp_message1 = await callback.message.answer("Оберіть формат погоди(по дефолту стоїть 1): \n"
                             "1. Поточна погода\n"
                             "2. Погода до кінця дня\n"
                             "3. Погода на завтра\n"
                             "4. Погода на 3 дні")
        
        await callback.answer("")
        await sleep(self.TIME_TO_DELETE)
        await temp_message1.delete()
     
    async def handle_weather_format(self, message: Message, state: FSMContext):
        await state.update_data(format_time = message.text)
        data = await state.get_data()
        
        try:
            format_time = int(data["format_time"].strip())
            if format_time < 1 or format_time > 4:
                raise ValueError("Invalid format")
            await rq.set_weather_format(message.from_user.id, format_time)
            temp_message = await message.answer(f"Обрано {format_time} формат погоди")
        except ValueError:
            temp_message = await message.answer("Невірний формат. Введіть число від 1 до 4.")
        except Exception as e:
            temp_message = await message.answer("Щось пішло не так. Спробуйте ще раз.")
        
        await state.clear()
        await sleep(self.TIME_TO_DELETE)
        await temp_message.delete()
        await message.delete()
    
    def set_bot(self, bot):
        self.bot = bot