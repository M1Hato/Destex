from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    username: str
    email: EmailStr

class UserCreate(User):
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)