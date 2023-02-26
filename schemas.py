from typing import List, Union, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None

class ItemIn(ItemBase):
    pass

class ItemOut(ItemBase):
    id: int
    date_posted: datetime
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    name: str
    
class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    # id: int
    is_active: bool

    class Config:
        orm_mode = True

class ItemUserOut(UserBase):
    id: int
    is_active: bool
    items: List[ItemOut] = []

    class Config:
        orm_mode = True