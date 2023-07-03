from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from users.models import get_current_active_user
from posts.models import Post
from posts.schemas import (
    AddPost, ShowPost, ShowPostWithLikesAndDislikes, UpdatePost
)
from posts.db_commands import (
    update_post,
    remove_post,
    get_all_posts,
    set_like_for_post,
    set_dislike_for_post
)
from data.database import get_async_session


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=List[ShowPostWithLikesAndDislikes])
async def get_posts(
    limit: int = 15,
    offset: int = 0,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_active_user)
):
    """Viewing posts"""
    return await get_all_posts(
        session=session,
        limit=limit,
        offset=offset
    )


@router.post('/', response_model=ShowPost)
async def add_post(
    post: AddPost,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_active_user)
) -> ShowPost:
    """Adding a new post"""
    new_post = Post(
        user_id=user.id,
        text=post.text
    )
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post, ["created_by"])
    return ShowPost(
        id=new_post.id,
        text=new_post.text,
        created_by=new_post.created_by,
        created_at=new_post.created_at
    )


@router.put('/{post_id}/', response_model=ShowPost)
async def edit_post(
    post_id: int,
    post: UpdatePost,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_active_user)
) -> ShowPost:
    """Editing a post"""
    return await update_post(
        session=session,
        post_id=post_id,
        creator_id=user.id,
        text=post.text
    )


@router.delete('/{post_id}/', response_model=ShowPost)
async def delete_post(
    post_id: int,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_active_user)
) -> ShowPost:
    """Deleting a post"""
    return await remove_post(
        session=session,
        post_id=post_id,
        creator_id=user.id
    )


@router.post('/{post_id}/like/')
async def set_like(
    post_id: int,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_active_user)
):
    """Like a post"""
    return await set_like_for_post(
        session=session,
        post_id=post_id,
        user_id=user.id
    )


@router.post('/{post_id}/dislike/')
async def set_dislike(
    post_id: int,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_active_user)
):
    """Dislike a post"""
    return await set_dislike_for_post(
        session=session,
        post_id=post_id,
        user_id=user.id
    )
