from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Today`s",),],
                                     [KeyboardButton(text="Yesterday")],
                                     [KeyboardButton(text="Tommorow")],
                                     [KeyboardButton(text="Previous 7 days"), KeyboardButton(text="Next 7 days")]],
                           resize_keyboard=True,
                           input_field_placeholder="For when a weather")

get_city = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Send city",
                                                         request_location=True)]],
                               resize_keyboard=True)
