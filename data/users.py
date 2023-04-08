from sqlalchemy import Column, Integer, String
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from .db import Base


class User(Base, SerializerMixin, UserMixin):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True, autoincrement=True)
	username = Column(String, nullable=True)
	email = Column(String, nullable=True)
	password = Column(String, nullable=True)

	def check_password(self, password):
		print(self.password, password)
		return self.password == password


