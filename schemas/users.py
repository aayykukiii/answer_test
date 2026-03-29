from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str


class UserRead(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = None