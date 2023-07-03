from sqlalchemy import Column, DateTime, Integer, Text, ForeignKey
import datetime
from data.database import Base
from sqlalchemy.orm import relationship


class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(
        Integer, ForeignKey('posts.id', ondelete='cascade'), nullable=False
    )
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)


class Dislike(Base):
    __tablename__ = 'dislikes'
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(
        Integer, ForeignKey('posts.id', ondelete='cascade'), nullable=False
    )
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = relationship('User', back_populates='posts')
