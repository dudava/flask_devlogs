from flask_restful import Resource, reqparse, abort
from flask import jsonify

from data import db
from data.users import User


def abort_if_user_not_found(user_id):
	session = db.create_session()
	user = session.query(User).get(user_id)
	if not user:
		abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
	def get(self, user_id):
		abort_if_user_not_found(user_id)
		session = db.create_session()
		user = session.query(User).get(user_id)
		return jsonify({'user': user.to_dict(only=('id', 'username'))})

	def delete(self, user_id):
		abort_if_user_not_found(user_id)
		session = db.create_session()
		user = session.query(User).get(user_id)
		session.delete(user)
		session.commit()
		return jsonify({'success': 'ok'})


user_parser = reqparse.RequestParser()
user_parser.add_argument('username', required=True)


class UsersListResource(Resource):
	def get(self):
		session = db.create_session()
		users = session.query(User).all()
		return jsonify({'users': [user.to_dict(only=('id', 'username')) for user in users]})

	def post(self):
		args = user_parser.parse_args()
		session = db.create_session()
		user = User(username=args['username'])
		session.add(user)
		session.commit()
		return jsonify({'success': 'ok'})
		