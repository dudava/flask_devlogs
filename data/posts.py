from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class Post(Base):
	__tablename__ = 'posts'

	id = Column(Integer, primary_key=True, autoincrement=True)
	topic_id = Column(Integer, ForeignKey('topics.id'))
	content = Column(String, nullable=True)
	comments = relationship('Comment', backref='post')