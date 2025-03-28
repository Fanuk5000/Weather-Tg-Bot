from app.database.models import async_session
from app.database.models import User, Category, Item
from sqlalchemy import select

async def set_user(tg_id:int, name:str, city:str) -> None: 
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        session.add(User(tg_id = tg_id, name = name, city = city))
        await session.commit()
        
async def check_user(tg_id:int) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user

async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))

async def get_category_item(category_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.category == category_id))