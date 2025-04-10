from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select

async def set_user(tg_id:int, name:str, city:str) -> None: 
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        session.add(User(tg_id = tg_id, name = name, city = city))
        await session.commit()
        
async def check_user(tg_id:int) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return bool(user)

async def change_city(tg_id:int, new_city:str) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        user.city = new_city
        await session.commit()

    
async def get_user_city(tg_id:int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        
        if user:
            return user.city
        else:
            return None

