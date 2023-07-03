from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, func
from fastapi import HTTPException, Response
from posts.models import Post, Like, Dislike
from posts.func import annotate


async def get_all_posts(session: AsyncSession):
    query = select(
        Post,
        func.count(Like.id).filter(Post.id == Like.post_id).label('likes'),
        func.count(Dislike.id).filter(
            Post.id == Dislike.post_id).label('dislike'),
    ).join(
        Like, isouter=True
    ).join(
        Dislike, isouter=True
    ).group_by(Post.id).options(selectinload(Post.created_by))
    result = await session.execute(query)
    return [la for la in annotate(result)]


async def get_post(session: AsyncSession, post_id: int):
    query = select(Post).where(Post.id == post_id)
    result = await session.execute(query)
    post = result.scalars().first()
    if not post:
        raise HTTPException(
            status_code=404, detail=f'The post with id {post_id} does not exist'
    )
    return post


async def update_post(
        session: AsyncSession, post_id: int, creator_id: int, text: str
):
    post_for_update = await get_post(session=session, post_id=post_id)
    if post_for_update.user_id != creator_id:
        raise HTTPException(
            status_code=401,
            detail='You cannot update posts that are not your own'
    )
    post_for_update.text = text
    await session.commit()
    await session.refresh(post_for_update, ["created_by"])
    return post_for_update


async def remove_post(session: AsyncSession, post_id: int, creator_id: int):
    post_for_delete = await get_post(session=session, post_id=post_id)
    if post_for_delete.user_id != creator_id:
        raise HTTPException(
            status_code=401,
            detail='You cannot delete posts that are not your own'
    )
    await session.delete(post_for_delete)
    await session.commit()
    return Response(status_code=204)


async def get_like_if_exists(session: AsyncSession, user_id: int, post_id: int):
    query = select(Like).where(
        Like.post_id == post_id
    ).where(Like.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().first()


async def get_dislike_if_exists(
        session: AsyncSession, user_id: int, post_id: int
):
    query = select(Dislike).where(
        Dislike.post_id == post_id
    ).where(Dislike.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().first()


async def is_liked_post(session: AsyncSession, user_id: int, post_id: int):
    liked = await get_like_if_exists(
        session=session,
        user_id=user_id,
        post_id=post_id
    )
    if liked:
        raise HTTPException(
            status_code=403, detail='You have already liked this post'
        )


async def set_like_or_change_dislike_on_like(
        session: AsyncSession, user_id: int, post_id: int
):
    dislike = await get_dislike_if_exists(
        session=session, user_id=user_id, post_id=post_id
    )
    if dislike:
        await session.delete(dislike)
        await session.commit()
    set_like = Like(post_id=post_id, user_id=user_id)
    session.add(set_like)
    await session.commit()


async def set_dislike_or_change_like_on_dislike(
        session: AsyncSession, user_id: int, post_id: int
):
    like = await get_like_if_exists(
        session=session, user_id=user_id, post_id=post_id
    )
    if like:
        await session.delete(like)
        await session.commit()
    set_dislike = Dislike(post_id=post_id, user_id=user_id)
    session.add(set_dislike)
    await session.commit()


async def is_disliked_post(session: AsyncSession, user_id: int, post_id: int):
    disliked = await get_dislike_if_exists(
        session=session,
        user_id=user_id,
        post_id=post_id
    )
    if disliked:
        raise HTTPException(
            status_code=403, detail='You have already disliked this post'
        )


async def set_like_for_post(session: AsyncSession, post_id: int, user_id: int):
    post_for_like = await get_post(session=session, post_id=post_id)
    if post_for_like.user_id == user_id:
        raise HTTPException(
            status_code=403, detail='You cannot like your own posts'
        )
    await is_liked_post(session=session, user_id=user_id, post_id=post_id)
    await set_like_or_change_dislike_on_like(
        session=session, user_id=user_id, post_id=post_id
    )
    return Response(status_code=204)


async def set_dislike_for_post(
        session: AsyncSession, post_id: int, user_id: int
):
    post_for_dislike = await get_post(session=session, post_id=post_id)
    if post_for_dislike.user_id == user_id:
        raise HTTPException(
            status_code=403,
            detail='You cannot dislike your own posts'
        )
    await is_disliked_post(session=session, user_id=user_id, post_id=post_id)
    await set_dislike_or_change_like_on_dislike(
        session=session, user_id=user_id, post_id=post_id
    )
    return Response(status_code=204)
