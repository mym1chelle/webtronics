import datetime
from jose import JWTError, jwt
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from sqlalchemy import select
from fastapi import Depends, status
from fastapi import HTTPException
from data.database import Base, async_session_maker
from users.schemas import TokenData, UserInDB, UserRead
from users.auth import (
    SECRET_KEY,
    ALGORITHM,
    oauth2_scheme,
    verify_password,
    get_password_hash
)
from posts.models import Post


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    posts = relationship('Post', back_populates='created_by')


class UserManager:
    def __init__(self, session: AsyncSession = None):
        self.session = session

    async def get_user(self, username: str):
        query = select(User).where(User.username == username)
        if not self.session:
            async with async_session_maker() as session:
                async with session.begin():
                    result = await session.execute(query)
                    user = result.scalars().first()
        else:
            result = await self.session.execute(query)
            user = result.scalars().first()
        if user:
            return UserInDB(
                id=user.id,
                username=user.username,
                created_at=user.created_at,
                password=user.password,
                )
        return None

    async def create_user(self, username: str, password: str):
        user = await self.get_user(username)
        if user:
            raise HTTPException(
                status_code=403,
                detail=f'The user with username {username} alredy exist'
            )
        else:
            new_user = User(
                username=username,
                password=get_password_hash(password)
            )
            self.session.add(new_user)
            await self.session.flush()
            return new_user

    async def authenticate_user(self, username: str, password: str):
        user = await self.get_user(username)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user

    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = await self.get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user


async def get_current_active_user(
        current_user: UserRead = Depends(UserManager().get_current_user)
):
    return current_user
