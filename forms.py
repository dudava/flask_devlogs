from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Optional, Length, Email


class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class TopicForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Краткое описание', validators=[Optional(strip_whitespace=True),
                                                                Length(min=0, max=200)])
    github_link = StringField('Ссылка на github')
    submit = SubmitField('Создать')


class PostForm(FlaskForm):
    text = TextAreaField('Текст')
    submit = SubmitField('Добавить')
