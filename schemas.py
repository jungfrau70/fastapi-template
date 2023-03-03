from typing import List, Union, Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class TokenData(BaseModel):
    access_token: Optional[str] = None

class Status(BaseModel):
    message: str

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

# class UserBase(BaseModel):
#     email: EmailStr
#     name: str
    
# class UserIn(UserBase):
#     password: str

# class UserOut(UserBase):
#     id: int
#     is_active: bool

#     class Config:
#         orm_mode = True

# class ItemUserOut(UserBase):
#     id: int
#     is_active: bool
#     items: List[ItemOut] = []

#     class Config:
#         orm_mode = True


class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(...)
    content: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "title": "Securing FastAPI applications with JWT.",
                "content": "In this tutorial, you'll learn how to secure your application by enabling authentication using JWT. We'll be using PyJWT to sign, encode and decode JWT tokens...."
            }
        }


class UserBase(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)

class UserSchema(UserBase):
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Joe Doe",
                "email": "joe@xyz.com",
                "password": "any"
            }
        }

class UserOutSchema(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "joe@xyz.com",
                "password": "any"
            }
        }