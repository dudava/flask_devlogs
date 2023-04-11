from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from .db import Base


class Topic(Base, SerializerMixin):
	__tablename__ = 'topics'

	id = Column(Integer, primary_key=True, autoincrement=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	title = Column(String, nullable=True)
	description = Column(String, nullable=True)
	posts = relationship('Post', backref='topic')