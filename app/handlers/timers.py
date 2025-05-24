from .common_imports import *

import app.keyboard as kb
import app.database.requests as rq

class Timers:
    plan_timer_working = False
    class PlanTimer(StatesGroup):
        time = State()
        
    def __init__(self):
        self.router = Router()
        #---plan_timer---
        self.router.message.register(self.plan_timer, Command("plantimer"))
        self.router.message.register(self.handle_plan_timer, Timers.PlanTimer.time)
        
        
    
    async def plan_timer(self, message: Message, state: FSMContext):
        if await rq.check_user(message.from_user.id) is False:
            await message.answer("Щоб користуватись таймером, вкажіть город(/setcity)")
            return
        
        await state.set_state(Timers.PlanTimer.time)
        await message.answer("Введіть час у форматі <b>години</b>:<b>хвилини</b>(00:00)", parse_mode="HTML")
        Timers.plan_timer_working = True
        
        
    
    async def handle_plan_timer(self, message: Message, state: FSMContext):
        await state.update_data(time = message.text)
        data = await state.get_data()
        
        try:
            hour, minute = map(int, data["time"].split(":"))
            if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                raise ValueError("Invalid time format")
        except ValueError:
            await message.answer("Невірний формат часу. Спробуйте ще раз(/plantimer)")
        except Exception as e:
            await message.answer("Щось пішло не так. Спробуйте ще раз(/plantimer)")
            print(e)
        else:
            await rq.set_plan_time(message.from_user.id, data["time"])
            await message.answer(f"Таймер заплановано на {data['time']}")
            
        await state.clear()