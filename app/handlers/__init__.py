from .buttons import buttons_router
from .commands import commands_router
from .timers import Timers

timers = Timers()

# Combine all routers into one listb
routers = [buttons_router, commands_router, timers.router]