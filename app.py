from flask import Flask, request, render_template, redirect, flash
from flask_restful import Api
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from datetime import timedelta

from data import db
from data.__all_models import User, Topic, Post, Comment
import users_resources
from tools.json import make_JSON_response, check_keys, create_jwt_response
from forms import RegisterForm, LoginForm


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

login_manager = LoginManager()
login_manager.init_app(app)


api = Api(app)

api.add_resource(users_resources.UserResource, '/api/v1/users/<int:user_id>')
api.add_resource(users_resources.UsersListResource, '/api/v1/users')


@app.route('/fill_db')
def fill_db():
	user = User(email='123@123.ru')
	user.set_password('123')
	topic = Topic(title='Охуеннейший проект на flask и еще цыганском табуне очень нужных библиотек фласка', description='Очень большой текст описания для тестирования размеров блока'
							 'для топиков на главной страницы, надеюсь он будет классно выглядеть, а то я повешусь')
	post1 = Post(content="Simple content")
	post2 = Post(content="Simple content twice")

	topic.posts.append(post1)
	topic.posts.append(post2)
	user.topics.append(topic)

	comment = Comment(content='Fooo Huina')
	user.comments.append(comment)
	post1.comments.append(comment)

	session = db.create_session()
	
	# session.delete(session.query(User).get(3))
	session.add(user)
	session.commit()
	return redirect('/')


@app.route('/')
def root():
	session = db.create_session()
	user = session.query(User).first()
	topics = session.query(Topic).all()
	return render_template('index.html', topics=topics)


@app.route('/topic')
def topic():
	return render_template('topic.html')


@app.route('/test')
@login_required
def test():
	return render_template('test.html')


@login_manager.user_loader
def load_user(user_id):
	session = db.create_session()
	return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            print(current_user.get_id())
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def user_register():
	form = RegisterForm()
	if form.validate_on_submit():
		if not User.check_uniqueness_email(form.email.data):
			return render_template('registration.html', form=form, error='Аккаунт с такой почтой уже зарегистрирован')
		session = db.create_session()
		user = User(email=form.email.data)
		user.set_password(form.password.data)
		session.add(user)
		session.commit()
		flash('Аккаунт успешно создан')		
		return redirect('/login')
	return render_template('registration.html', form=form)


def main():
	db.init('databases/database.sqlite')
	app.run()


if __name__ == '__main__':
	main()