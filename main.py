import uvicorn
from fastapi import HTTPException, FastAPI, Depends
from database.db import get_db, init_db
from crud import (create_book, get_all_book, get_book_by_id, update_book, delete_book_by_id,
                  create_user, get_all_users, get_user_by_id, update_user, delete_user_by_id,
                  search_books, create_books_batch
                  )
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import (BookCreate, BookRead, BookUpdate,
                     UserCreate, UserRead, UserUpdate)


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.post('/books', response_model=BookRead)
async def post_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    return await create_book(db, book)


@app.post('/books/batch', response_model=list[BookRead])
async def post_books_batch(books: list[BookCreate], db: AsyncSession = Depends(get_db)):
    return await create_books_batch(db, books)


@app.get('/books/search', response_model=list[BookRead])
async def search_books_search(title: str, authoor: str, db: AsyncSession = Depends(get_db)):
    return await search_books(db, title, authoor)


@app.get('/books', response_model=list[BookRead])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await get_all_book(db)


@app.get('/books/{book_id}', response_model=BookRead)
async def get_by_id(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail='book not found')
    return book


@app.put('/books/{book_id}', response_model=BookUpdate)
async def update_book_by_id(book_id: int, book: BookUpdate, db: AsyncSession = Depends(get_db)):
    return await update_book(db, book_id, book)


@app.delete('/books/{book_id}')
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_book_by_id(db, book_id)


#user

@app.post('/users', response_model=UserRead)
async def post_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)


@app.get('/users', response_model=list[UserRead])
async def get_all_user(db: AsyncSession = Depends(get_db)):
    return await get_all_users(db)


@app.get('/users/{user_id}', response_model=UserRead)
async def get_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='user not found')
    return user


@app.put('/users/{user_id}', response_model=UserUpdate)
async def update_user_by_id(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    return await update_user(db, user_id, user)


@app.delete('/users/{user_id}')
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_user_by_id(db, user_id)


if __name__ == '__main__':
    uvicorn.run(app=app)