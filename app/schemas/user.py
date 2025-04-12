from uuid import UUID
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    username: str
    password: str

class UserResponse(UserBase):
    id: UUID
    username: str
    is_active: bool

    class Config:
        from_attributes = True