from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Поточна",),KeyboardButton(text="До кінця дня")],
                                     [KeyboardButton(text="Завтрашня"), KeyboardButton(text="3 дні")],
                                     [KeyboardButton(text="🎁Підтримка проєкту💵",)]],
                           resize_keyboard=True,
                           input_field_placeholder="Оберіть на коли потрібна погода",)

plan_time_keys = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Запустити", callback_data="enable_plan_timer"),
                      InlineKeyboardButton(text="Зупинити", callback_data="stop_plan_timer"),
                      InlineKeyboardButton(text="Формат погоди", callback_data="weather_format")],
            [InlineKeyboardButton(text="Встановити час", callback_data="plan_timer"),
            InlineKeyboardButton(text="Інтервал", callback_data="interval_plan_timer"),
            InlineKeyboardButton(text="Інфо", callback_data="timer_info")]
                    ])
