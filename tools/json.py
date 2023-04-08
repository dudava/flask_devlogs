from flask import make_response, jsonify
from flask_jwt_simple import create_jwt


def make_JSON_response(message, status):
	resp = make_response(message, status)
	resp.headers['Content-type'] = 'application/json; charset=UTF8'
	return resp


def check_keys(request, keys):
	return all(request_key in keys for request_key in request)


def create_jwt_response(user):
	user_data = user.to_dict(only=('id', 'username'))
	print(user_data)
	j_token = {'token': create_jwt(user_data)}
	return make_JSON_response(jsonify(j_token), 200)