from pydantic import BaseModel, validator, EmailStr, conint
from typing import Optional
from datetime import datetime



class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # This is needed to convert the output to a type that Pydantic can read
    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    # Will inherit other columns from PostBase
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    # This is needed to convert the output to a type that Pydantic can read
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    # This is needed to convert the output to a type that Pydantic can read
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

# class UpdatePost(BaseModel):
#     # User can only update publish field
#     published: Optional[bool]


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)