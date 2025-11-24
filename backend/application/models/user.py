from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^[^\s@]+@[^\s@]+\.[^\s@]+$')

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=20)
    confirm_password: str = Field(..., min_length=8, max_length=20)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    current_password: Optional[str] = Field(None, min_length=8, max_length=20)
    new_password: Optional[str] = Field(None, min_length=8, max_length=20)
    confirm_new_password: Optional[str] = Field(None, min_length=8, max_length=20)

class UserInDB(UserBase):
    hashed_password: str

    class Config:
        orm_mode = True

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=20)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
