from fastapi import HTTPException, APIRouter, Depends
from database.db import get_db
from repositories.users import (
    create_user, get_all_users, get_user_by_id, update_user, delete_user_by_id
)
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import UserCreate, UserRead, UserUpdate


router = APIRouter()


@router.post('/users', response_model=UserRead)
async def post_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)


@router.get('/users', response_model=list[UserRead])
async def get_all_user(db: AsyncSession = Depends(get_db)):
    return await get_all_users(db)


@router.get('/users/{user_id}', response_model=UserRead)
async def get_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='user not found')
    return user


@router.put('/users/{user_id}', response_model=UserUpdate)
async def update_user_by_id(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    return await update_user(db, user_id, user)


@router.delete('/users/{user_id}')
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_user_by_id(db, user_id)
