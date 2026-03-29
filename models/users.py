from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from database.db import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    books: Mapped[list[Book]] = relationship('Book', back_populates="owner")