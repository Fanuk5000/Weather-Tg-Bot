from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_categories, get_category_item

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Catalog")],
                                     [KeyboardButton(text="Trashcan")],
                                     [KeyboardButton(text="Abous us"), KeyboardButton(text="Contats")]],
                           resize_keyboard=True,
                           input_field_placeholder="Choose a menu item")

catalog = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Weather", callback_data="weather")],
    [InlineKeyboardButton(text="AI", callback_data="ai")]])

get_city = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Send city",
                                                         request_location=True)]],
                               resize_keyboard=True)

async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
    keyboard.add(InlineKeyboardButton(text='To main', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()


async def items(category_id):
    all_items = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f"item_{item.id}"))
    keyboard.add(InlineKeyboardButton(text='To main', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()