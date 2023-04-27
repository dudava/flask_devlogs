from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base


class Post(Base):
	__tablename__ = 'posts'

	id = Column(Integer, primary_key=True, autoincrement=True)
	topic_id = Column(Integer, ForeignKey('topics.id'))
	content_url = Column(String, nullable=True)
	likes = Column(Integer, default=0)
	comments = relationship('Comment', backref='post')
