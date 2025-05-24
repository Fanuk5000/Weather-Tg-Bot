from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select

async def set_plan_time(tg_id:int, plan_time:str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.plan_time = plan_time
        
        await session.commit()

async def set_user(tg_id:int, city:str, cords:str) -> None: 
    async with async_session() as session:
        # user = await session.scalar(select(User).where(User.tg_id == tg_id))

        session.add(User(tg_id = tg_id, city = city, cords = cords))
        await session.commit()
        
async def check_user(tg_id:int) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return bool(user)

async def change_city(tg_id:int, new_city:str, cords:str) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        user.city = new_city
        user.cords = cords
        await session.commit()

    
async def get_user_city(tg_id:int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if user:
            return user.city
        else:
            return None

async def get_city_cords(city:str) -> tuple[int, int] | None:
    async with async_session() as session:
        city = await session.scalar(select(User).where(User.city == city))
        
        if city:
            return map(float, str(city.cords).split(" "))
        else:
            return None