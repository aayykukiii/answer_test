from pydantic import BaseModel

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


class BookUpdate(BookCreate):
    pass
