from .buttons import buttons_router
from .commands import commands_router
from .timers import Timers

timers = Timers()
set_bot_timers = timers.set_bot

# Combine all routers into one list
routers = [buttons_router, commands_router, timers.router]

