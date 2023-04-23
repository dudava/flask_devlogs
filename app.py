from flask import Flask, request, render_template, redirect, flash, jsonify
import flask
from flask_restful import Api
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS, cross_origin
from datetime import timedelta
from loguru import logger
import os
import uuid
from waitress import serve

from data import db
from data.__all_models import User, Topic, Post, Comment
import users_resources
from tools.json import make_JSON_response, check_keys, create_jwt_response
from forms import RegisterForm, LoginForm, TopicForm, PostForm


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
api = Api(app)
login_manager = LoginManager()

login_manager.init_app(app)
api.add_resource(users_resources.UserResource, '/api/v1/users/<int:user_id>')
api.add_resource(users_resources.UsersListResource, '/api/v1/users')
blueprint = flask.Blueprint(
    'upload_image_api',
    __name__,
    template_folder = 'templates'
)


@blueprint.route('/upload_image', methods=['POST', 'OPTIONS'])
@login_required
def upload_image():
    if not os.path.exists(f'static/imgs/{current_user.username}'):
        os.mkdir(f'static/imgs/{current_user.username}')
    image = request.files['file']
    image_name = request.form['image_name'].split('.')[0]
    image_type = request.form['image_name'].split('.')[-1]
    image_path = f"static/imgs/{current_user.username}/{uuid.uuid1(node=uuid.getnode())}.{image_type}" 
    with open(image_path, mode='wb') as file:
        file.write(request.files['file'].read())
    return f"![{image_name}]({'/' + image_path})"

@blueprint.route('/get_preview_md', methods=['POST', 'OPTIONS'])
@login_required
def get_preview_md():
    tempfile_path = f'static/tempfiles/{uuid.uuid1(node=uuid.getnode())}.md'
    with open(tempfile_path, mode='wt', encoding='utf-8') as md_file:
        md_file.write(request.form['text'])
    return '/' + tempfile_path


@app.route('/fill_db')
def fill_db():
    user = User(username='dudavik', email='123@123.ru')
    user.set_password('123')
    topic = Topic(title='Классный проект на flask и еще цыганском табуне очень нужных библиотек фласка', description='Очень большой текст описания для тестирования размеров блока'
                             'для топиков на главной страницы, надеюсь он будет классно выглядеть, а то я повешусь')
    post1 = Post(content_url="/static/posts/01_rest_register.md")

    topic.posts.append(post1)
    user.topics.append(topic)

    comment = Comment(content='Fooo Huina')
    user.comments.append(comment)
    post1.comments.append(comment)

    session = db.create_session()
    
    session.add(user)
    try:
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()
    return redirect('/')


@app.route('/')
def root():
    session = db.create_session()
    user = session.query(User).first()
    topics = session.query(Topic).all()
    session.commit()
    return render_template('index.html', topics=topics)


@app.route('/topic/<int:user_id>/<int:topic_id>')
def topic(user_id, topic_id):
    session = db.create_session()
    user = session.get(User, user_id)
    topic = session.get(Topic, topic_id)
    session.commit()
    return render_template('topic.html', user=user, topic=topic)


@app.route('/create_topic', methods=['GET', 'POST'])
@login_required
def create_topic():
    form = TopicForm()
    if form.validate_on_submit():
        topic = Topic(title=form.title.data, description=form.description.data)
        if not os.path.exists(f'static/posts/{current_user.username}'):
            os.mkdir(f'static/posts/{current_user.username}')
        if not os.path.exists(f'static/posts/{current_user.username}/{topic.title}'):
            logger.debug('нет папки с топиком')
            os.mkdir(f'static/posts/{current_user.username}/{topic.title}')
        session = db.create_session()
        user = session.get(User, current_user.id)
        user.topics.append(topic)
        session.add(user)
        try:
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()
        return redirect('/')
    return render_template('create_topic.html', form=form)


@app.route('/create_post/<int:topic_id>', methods=['GET', 'POST'])
def create_post(topic_id):
    session = db.create_session()
    topic = session.get(Topic, topic_id)
    if current_user == topic.user:
        form = PostForm()
        if form.validate_on_submit():
            post = Post()
            session.add(post)
            session.flush()
            post_path = f'static/posts/{current_user.username}/{topic.title}/{post.id}.md'
            with open(post_path, mode='wt', encoding='utf-8') as md_file:
                md_file.write(form.text.data)
            post.content_url = '/' + post_path
            topic.posts.append(post)
            session.add(topic)
            user_id = topic.user.id
            topic_id = topic.id
            try:
                session.commit()
            except:
                session.rollback()
            finally:
                session.close()
            return redirect(f'/topic/{user_id}/{topic_id}')
        return render_template('create_post.html', form=form)
    return 'пошел отсюда'


@login_manager.user_loader
def load_user(user_id):
    session = db.create_session()
    user = session.get(User, user_id)
    # session.commit()
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        session.commit()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
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
        if not User.check_uniqueness_username(form.username.data):
            return render_template('registration.html', form=form, error='Аккаунт с таким именем уже зарегистрирован')
        session = db.create_session()
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        session.add(user)
        try:
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()
        flash('Аккаунт успешно создан')     
        return redirect('/login')
    return render_template('registration.html', form=form)


def main():
    db.init('databases/database.sqlite')
    app.register_blueprint(blueprint)
    # serve(app, host='0.0.0.0', port=5000)
    app.run()


if __name__ == '__main__':
    main()