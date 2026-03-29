from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User
from schemas.users import UserCreate, UserUpdate
                     

async def create_user(db: AsyncSession, user: UserCreate):
    new_user = User(
        username=user.username
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user



async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()



async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def update_user(db: AsyncSession, user_id: int, user_data: UserUpdate):
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail='user not found')
    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail='user not found')
    await db.delete(db_user)
    await db.commit()
    return {'detail': 'user delted'}