from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

#states imports 
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

#keyboard import
import app.keyboard as kb
#db import
import app.database.requests as rq