from pydantic import BaseModel
from typing import Optional


class BookCreate(BaseModel):
    title: str
    authoor: str
    year: int
    owner_id: int

class BookRead(BaseModel):
    id: int
    title: str
    authoor: str
    year: int
    owner_id: int       

    class Config:
        from_attributes=True


class BookUpdate(BaseModel):
    title: Optional[str] = None
    authoor: Optional[str] = None
    year: Optional[int] = None
    owner_id: Optional[int] = None