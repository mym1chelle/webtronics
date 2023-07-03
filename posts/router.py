from fastapi import Depends, APIRouter
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from users.models import get_current_active_user
from posts.models import Post, Like, Dislike
from posts.schemas import AddPost, ShowPost, ShowPosts
from posts.func import annotate
from posts.db_commands import update_post, remove_post
from data.database import get_async_session


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=ShowPosts)
async def get_posts(session: AsyncSession = Depends(get_async_session), user=Depends(get_current_active_user)):
    query = select(
        Post,
        func.count(Like.id).filter(Post.id == Like.post_id).label('likes'),
        func.count(Dislike.id).filter(
            Post.id == Dislike.post_id).label('dislike'),
    ).join(Like, isouter=True).join(Dislike, isouter=True).group_by(Post.id).options(selectinload(Post.created_by))
    result = await session.execute(query)
    return {'posts': [la for la in annotate(result)]}


@router.post('/')
async def add_post(post: AddPost, session: AsyncSession = Depends(get_async_session), user=Depends(get_current_active_user)) -> ShowPost:
    """Добавление нового поста"""
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


@router.put('/{post_id}/')
async def edit_post(post_id: int, post: AddPost, session: AsyncSession = Depends(get_async_session), user=Depends(get_current_active_user)) -> ShowPost:
    """Редактирование поста"""
    updated_post = await update_post(
        session=session,
        post_id=post_id,
        creator_id=user.id,
        text=post.text
    )
    return ShowPost(
        id=updated_post.id,
        text=updated_post.text,
        created_by=updated_post.created_by,
        created_at=updated_post.created_at
    )


@router.delete('/{post_id}/')
async def delete_post(post_id: int, session: AsyncSession = Depends(get_async_session), user=Depends(get_current_active_user)) -> ShowPost:
    """Удаление поста"""
    return await remove_post(
        session=session,
        post_id=post_id,
        creator_id=user.id
    )