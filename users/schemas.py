from fastapi import HTTPException
from pydantic import BaseModel, validator
from datetime import datetime
from users.constants import (
    PATTERN_PASSWORD,
    PATTERN_USERNAME,
    INVALID_USERNAME_ERROR,
    INVALID_PASSWORD_ERROR
)


class ExtendedModel(BaseModel):

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    password: str

    @validator('username')
    def validate_username(cls, value):
        if not PATTERN_USERNAME.match(value):
            raise HTTPException(
                status_code=422,
                detail=INVALID_USERNAME_ERROR
            )
        return value

    @validator('password')
    def validate_password(cls, value):
        if not PATTERN_PASSWORD.match(value):
            raise HTTPException(
                status_code=422,
                detail=INVALID_PASSWORD_ERROR
            )
        return value


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserRead(ExtendedModel):
    id: int
    username: str
    created_at: datetime


class UserInDB(UserRead):
    password: str


class UserName(ExtendedModel):
    username: str
