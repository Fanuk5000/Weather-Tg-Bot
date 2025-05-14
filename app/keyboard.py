from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Поточна",),],
                                     [KeyboardButton(text="Завтрашня")],
                                     [KeyboardButton(text="3 дні")],
                                     ],
                           resize_keyboard=True,
                           input_field_placeholder="For when a weather")

get_city = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Send city",
                                                         request_location=True)]],
                               resize_keyboard=True)
