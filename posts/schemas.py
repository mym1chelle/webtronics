from pydantic import BaseModel
from datetime import datetime
from typing import List
from users.schemas import UserRead


class ExtendedModel(BaseModel):

    class Config:
        orm_mode = True


class AddPost(BaseModel):
    text: str


class ShowPost(ExtendedModel):
    id: int
    text: str
    created_by: UserRead
    created_at: datetime


class ShowPostWithLikesAndDislikes(ShowPost):
    likes: int
    dislikes: int


class ShowPosts(ExtendedModel):
    posts: List[ShowPostWithLikesAndDislikes] | List
