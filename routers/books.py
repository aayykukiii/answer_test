from fastapi import HTTPException, APIRouter, Depends
from database.db import get_db
from repositories.books import (create_book, get_all_book, get_book_by_id, update_book, 
                  delete_book_by_id, search_books, create_books_batch
                  )
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.books import BookCreate, BookRead, BookUpdate


router = APIRouter()


@router.post('/books', response_model=BookRead)
async def post_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    return await create_book(db, book)


@router.post('/books/batch', response_model=list[BookRead])
async def post_books_batch(books: list[BookCreate], db: AsyncSession = Depends(get_db)):
    return await create_books_batch(db, books)


@router.get('/books/search', response_model=list[BookRead])
async def search_books_search(title: str, authoor: str, db: AsyncSession = Depends(get_db)):
    return await search_books(db, title, authoor)


@router.get('/books', response_model=list[BookRead])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await get_all_book(db)


@router.get('/books/{book_id}', response_model=BookRead)
async def get_by_id(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail='book not found')
    return book


@router.put('/books/{book_id}', response_model=BookUpdate)
async def update_book_by_id(book_id: int, book: BookUpdate, db: AsyncSession = Depends(get_db)):
    return await update_book(db, book_id, book)


@router.delete('/books/{book_id}')
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_book_by_id(db, book_id)