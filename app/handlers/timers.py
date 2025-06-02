from .common_imports import *
from asyncio import sleep

from datetime import datetime
class Timers:
    class PlanTimer(StatesGroup):
        time = State()
        days = State()
        format_time = State()
        
    
    def __init__(self):
        self.plan_timer_working = False
        self.router = Router()
        self.TIME_TO_DELETE = 5

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
        
        # self.router.callback_query.register(self.handle_days_input, F.data == "interval_plan_timer", Timers.IntervalTimer.days)
        
    async def plan_timer_menu(self, message: Message):
        if await rq.check_user(message.from_user.id) is False:
            await message.answer("Щоб користуватись таймером, вкажіть город(/setcity)")
            return
        
        await message.answer("Меню для користування таймером.\nЩоб подивитись функціонал, дивиться \"Інфо\".",
                             parse_mode="HTML", reply_markup=kb.plan_time_keys)

    # Start the plan timer
    async def plan_timer(self, message: Message, state: FSMContext):
        if await rq.check_user(message.from_user.id) is False:
            await message.answer("Щоб користуватись таймером, вкажіть город(/setcity)")
            return
        
        await state.set_state(Timers.PlanTimer.time)
        temp_message = await message.answer("Введіть час у форматі 00:00")
        await sleep(self.TIME_TO_DELETE)
        await temp_message.delete()
        
    
    # Callback for the plan timer
    async def callback_plan_timer(self, callback: CallbackQuery, state: FSMContext):
        
        if await rq.check_user(callback.from_user.id) is False:
            await callback.message.answer("Щоб користуватись таймером, вкажіть город(/setcity)")
            return
        
        await state.set_state(Timers.PlanTimer.time)
        temp_message = await callback.message.answer("Введіть час у форматі 00:00")
        
        await sleep(self.TIME_TO_DELETE)
        await temp_message.delete()
        await callback.answer("")
    
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
        await sleep(15)
        await temp_message.delete()
        
    
    # Stop the plan timer
    async def stop_plan_timer(self, callback: CallbackQuery):
        if await rq.check_user(callback.from_user.id) is False:
            await callback.message.answer("Щоб користуватись таймером, вкажіть город(/setcity)")
            return
        
        if self.plan_timer_working:
            self.plan_timer_working = False
            await callback.answer("Таймер зупинено")
        else:
            await callback.answer("Таймер не запущено")
    
    # Repeat the plan timer every 24 hours
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
        print(data)
        try:
            reapeat_in_days = int(data["days"].strip())
            if reapeat_in_days < 1:
                raise ValueError("Days must be greater than 0")
            await rq.set_days_interval(message.from_user.id, reapeat_in_days)
            await state.clear()
            temp_message = await message.answer(f"Таймер буде повторюватись кожні {self.reapeat_in_days} днів")
        except ValueError:
            temp_message = await message.answer("Невірний формат. Введіть число днів більше 0 або ціле число.")
        
        await sleep(self.TIME_TO_DELETE)
        await temp_message.delete()

    
    
    # Handle the time input for the plan timer
    async def handle_plan_timer(self, message: Message, state: FSMContext):
        await state.update_data(time = message.text)
        data = await state.get_data()
        
        try:
            hour, minute = map(int, data["time"].strip().split(":"))
            if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                raise ValueError("Invalid time format")
        except ValueError:
            temp_message = await message.answer("Невірний формат часу. Спробуйте ще раз(/plantimer)")
        except Exception as e:
            temp_message = await message.answer("Щось пішло не так. Спробуйте ще раз(/plantimer)")
            print(e)
        else:
            self.plan_timer_working = True
            await rq.set_plan_time(message.from_user.id, data["time"])
            await state.clear()
            
            temp_message = await message.answer(f"Таймер заплановано на {data['time']}, тепер можна його запустити")
        await sleep(self.TIME_TO_DELETE)
        await temp_message.delete()
    
    # Enable the plan timer and start checking the time
    async def enable_plan_timer(self, callback: CallbackQuery):
        plan_time = await rq.get_plan_time(callback.from_user.id)
        if not plan_time:
            await callback.answer("Час не встановлено, встановіть його.")
            return
        day_counter = 0
        
        self.plan_timer_working = True
        reapeat_in_days = await rq.get_days_interval(callback.from_user.id)
        if reapeat_in_days == 0:
            await callback.answer("Таймер запущено, він спрацює один раз")
        else:
            await callback.answer(f"Таймер запущено, він буде працювати кожні {reapeat_in_days} днів")
        
        while self.plan_timer_working:
                print(f"Timer working: {self.plan_timer_working}")
                current_time = datetime.now().strftime("%H:%M")
                if current_time == plan_time:
                    await callback.message.answer("Час вийшов! Пора перевірити погоду!")
                    
                    if reapeat_in_days == 0:
                        self.plan_timer_working = False
                    else:
                        if day_counter == reapeat_in_days:
                            day_counter = 0
                        else:
                            day_counter += 1
                    
                    await rq.set_plan_time(callback.from_user.id, None)
                await sleep(59)
        
    async def weather_format(self, callback: CallbackQuery, state: FSMContext):
        if await rq.check_user(callback.from_user.id) is False:
            await callback.message.answer("Щоб користуватись таймером, вкажіть город(/setcity)")
            return
        
        await state.set_state(Timers.PlanTimer.format_time)
        temp_message1 = await callback.message.answer("Оберіть формат погоди(по дефолту стоїть 1): \n"
                             "1. Поточна погода\n"
                             "2. Погода на завтра\n"
                             "3. Погода на 3 дні\n"
                             "4. Погода до кінця дня")
        
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

        
        