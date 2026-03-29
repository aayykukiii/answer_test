from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.books import Book
from schemas.books import BookCreate, BookUpdate
from typing import List


async def create_book(db: AsyncSession, book: BookCreate):
    new_book = Book(
        title=book.title,
        authoor=book.authoor,
        year=book.year,
        owner_id=book.owner_id
    )
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book


async def get_all_book(db: AsyncSession):
    result = await db.execute(select(Book))
    return result.scalars().all()


async def create_books_batch(db: AsyncSession, books: List[BookCreate]):
    new_books = []
    for book in books:
        new_book = Book(
            title=book.title, 
            authoor=book.authoor,
            year=book.year,
            owner_id=book.owner_id
        )
        db.add(new_book)
        new_books.append(new_book)
    await db.commit()
    for book in new_books:
        await db.refresh(book)
    return new_books


async def search_books(db: AsyncSession, title: str, authoor: str):
    query = select(Book)
    if title:
        query = query.where(Book.title.ilike(f'%{title}%'))
    if authoor:
        query = query.where(Book.authoor.ilike(f'%{authoor}%'))
    result = await db.execute(query)
    books = result.scalars().all()
    return books


async def get_book_by_id(db: AsyncSession, book_id: int):
    result = await db.execute(select(Book).where(Book.id == book_id))
    return result.scalar_one_or_none()


async def update_book(db: AsyncSession, book_id: int, book_data: BookUpdate):
    result = await db.execute(select(Book).where(Book.id == book_id))
    db_book = result.scalar_one_or_none()
    if not db_book:
        raise HTTPException(status_code=404, detail='book not found')
    update_data = book_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)
    await db.commit()
    await db.refresh(db_book)
    return db_book


async def delete_book_by_id(db: AsyncSession, book_id: int):
    result = await db.execute(select(Book).where(Book.id == book_id))
    db_book = result.scalar_one_or_none()
    if not db_book:
        raise HTTPException(status_code=404, detail='book not found')
    await db.delete(db_book)
    await db.commit()
    return {'detail': 'book delted'}
