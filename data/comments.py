from sqlalchemy import Column, Integer, String, ForeignKey
from .db import Base


class Comment(Base):
	__tablename__ = 'comments'

	id = Column(Integer, primary_key=True, autoincrement=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	post_id = Column(Integer, ForeignKey('posts.id'))
	content = Column(String, nullable=True)
	likes = Column(Integer, nullable=True)
