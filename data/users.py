from sqlalchemy import Column, Integer, String
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db import Base, create_session


class User(Base, SerializerMixin, UserMixin):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True, autoincrement=True)
	username = Column(String, nullable=True)
	email = Column(String, nullable=True)
	hashed_password = Column(String, nullable=True)
	topics = relationship('Topic', backref='user')
	comments = relationship('Comment', backref='user')

	@staticmethod
	def check_uniqueness_email(email):
		session = create_session()
		users = session.query(User).all()
		for user in users:
			if user.email == email:
				return False
		return True

	@staticmethod
	def check_uniqueness_username(username):
		session = create_session()
		users = session.query(User).all()
		for user in users:
			if user.username == username:
				return False
		return True		


	def set_password(self, password):
		self.hashed_password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.hashed_password, password)


