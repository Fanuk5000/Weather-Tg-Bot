from .common_imports import *
from asyncio import sleep

from datetime import datetime
class Timers:
    class PlanTimer(StatesGroup):
        time = State()
        days = State()
        
    def __init__(self):
        self.plan_timer_working = False
        self.reapeat_in_days = 0
        self.router = Router() 

        self.router.message.register(self.plan_timer_menu, Command("timermenu"))
        # self.router.message.register(self.stop_plan_timer, Command("stopplantimer"))
        self.router.message.register(self.stop_plan_timer, Command("repeatplantimer"))
        self.router.message.register(self.handle_plan_timer, Timers.PlanTimer.time)
        
        self.router.callback_query.register(self.stop_plan_timer, F.data =="stop_plan_timer")
        self.router.callback_query.register(self.callback_plan_timer, F.data == "plan_timer")
        self.router.callback_query.register(self.enable_plan_timer, F.data == "enable_plan_timer")
        self.router.callback_query.register(self.timer_info, F.data == "timer_info")
        self.router.callback_query.register(self.interval_plan_timer, F.data == "interval_plan_timer")
        
        self.router.callback_query.register(self.handle_days_input, F.data == "interval_plan_timer", Timers.PlanTimer.days)
        
    async def plan_timer_menu(self, message: Message):
        if await rq.check_user(message.from_user.id) is False:
            await message.answer("Щоб користуватись таймером, вкажіть город(/setcity)")
            return
        
        await message.answer("Меню для користування таймером.\nВ ньому можна: запустити таймер, виключити його,"
                             "повторити(якщо таймер ще не спрацював, то єфекту не буде) та поставити на якийсь інтервал у днях",
                             parse_mode="HTML", reply_markup=kb.plan_time_keys)

    # Start the plan timer
    async def plan_timer(self, message: Message, state: FSMContext):
        if await rq.check_user(message.from_user.id) is False:
            await message.answer("Щоб користуватись таймером, вкажіть город(/setcity)")
            return
        
        await state.set_state(Timers.PlanTimer.time)
        await message.answer("Введіть час у форматі <b>години</b>:<b>хвилини</b>(00:00)", parse_mode="HTML")
    
    # Callback for the plan timer
    async def callback_plan_timer(self, callback: CallbackQuery, state: FSMContext):
        
        if await rq.check_user(callback.from_user.id) is False:
            await callback.message.answer("Щоб користуватись таймером, вкажіть город(/setcity)")
            return
        
        await state.set_state(Timers.PlanTimer.time)
        await callback.message.answer("Введіть час у форматі 00:00")
        await callback.answer("")
    
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
        await callback.message.answer("Введіть переодичність таймера в днях")
    
    async def handle_days_input(self, callback: CallbackQuery, state: FSMContext):
        await state.update_data(days = callback.text)
        data = await state.get_data()
        print(data)
        try:
            self.reapeat_in_days = int(data["days"].strip())
            if self.reapeat_in_days < 1:
                raise ValueError("Days must be greater than 0")
            await state.clear()
            await callback.answer(f"Таймер буде повторюватись кожні {self.reapeat_in_days} днів")
        except ValueError:
            self.reapeat_in_days = 0
            await callback.answer("Невірний формат. Введіть число днів більше 0.")

    
    
    # Handle the time input for the plan timer
    async def handle_plan_timer(self, message: Message, state: FSMContext):
        await state.update_data(time = message.text)
        data = await state.get_data()
        
        try:
            hour, minute = map(int, data["time"].strip().split(":"))
            if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                raise ValueError("Invalid time format")
        except ValueError:
            await message.answer("Невірний формат часу. Спробуйте ще раз(/plantimer)")
        except Exception as e:
            await message.answer("Щось пішло не так. Спробуйте ще раз(/plantimer)")
            print(e)
        else:
            self.plan_timer_working = True
            await rq.set_plan_time(message.from_user.id, data["time"])
            await state.clear()
            await message.answer(f"Таймер заплановано на {data['time']}, тепер можна його запустити")
    
    # Enable the plan timer and start checking the time
    async def enable_plan_timer(self, callback: CallbackQuery):
        plan_time = await rq.get_plan_time(callback.from_user.id)
        if not plan_time:
            await callback.answer("Час не встановлено, встановіть його.")
            return
        day_counter = 0
        
        self.plan_timer_working = True
        print(self.reapeat_in_days)
        await callback.answer("Таймер запущено, він буде працювати до наступного перезапуску бота")
        while self.plan_timer_working:
                print(f"Timer working: {self.plan_timer_working}")
                current_time = datetime.now().strftime("%H:%M")
                if current_time == plan_time:
                    await callback.message.answer("Час вийшов! Пора перевірити погоду!")
                    
                    if self.reapeat_in_days == 0:
                        self.plan_timer_working = False
                    else:
                        if day_counter == self.reapeat_in_days:
                            day_counter = 0
                        else:
                            day_counter += 1
                    
                    await rq.set_plan_time(callback.message.from_user.id, None)
                    break
                await sleep(59)
    
    
    async def timer_info(self, callback: CallbackQuery):
        if await rq.check_user(callback.from_user.id) is False:
            await callback.message.answer("Щоб користуватись таймером, вкажіть город(/setcity)")
            return
        
        plan_time = await rq.get_plan_time(callback.from_user.id)
        if not plan_time:
            await callback.answer("Таймер не запущено")
            return
        
        await callback.answer(f"Таймер запущено на {plan_time}")