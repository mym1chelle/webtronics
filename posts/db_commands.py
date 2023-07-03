from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, Response
from posts.models import Post


async def get_post(session: AsyncSession, post_id: int):
    query = select(Post).where(Post.id == post_id)
    result = await session.execute(query)
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail=f'Пост с id {post_id} не найден')
    return post


async def update_post(session: AsyncSession, post_id: int, creator_id: int, text: str):
    post_for_update = await get_post(session=session, post_id=post_id)
    if post_for_update.user_id != creator_id:
        raise HTTPException(status_code=401, detail='Вы не можете редактировать чужие посты')
    post_for_update.text = text
    await session.commit()
    await session.refresh(post_for_update, ["created_by"])
    return post_for_update


async def remove_post(session: AsyncSession, post_id: int, creator_id: int):
    post_for_delete = await get_post(session=session, post_id=post_id)
    if post_for_delete.user_id != creator_id:
        raise HTTPException(status_code=401, detail='Вы не можете удалять чужие посты')
    await session.delete(post_for_delete)
    await session.commit()
    return Response(status_code=204)
