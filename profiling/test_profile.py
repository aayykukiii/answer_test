import cProfile
import pstats
import asyncio
from database.db import async_session
from repositories.books import create_book
from schemas.books import BookCreate
from models.users import User
from models.books import Book


async def main():
    async with async_session() as db:
        book_data = BookCreate(title='Test', authoor='eeef', year=3444, owner_id=6)

        profiler = cProfile.Profile()
        profiler.enable()

        await create_book(db, book_data)

        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.strip_dirs()
        stats.sort_stats('cumulative')
        stats.print_stats(10)


asyncio.run(main())