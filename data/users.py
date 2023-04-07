from sqlalchemy import Column, Integer, String
from sqlalchemy_serializer import SerializerMixin
from .db import Base


class User(Base, SerializerMixin):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True, autoincrement=True)
	username = Column(String, nullable=True)
	email = Column(String, nullable=True)
	password = Column(String, nullable=True)