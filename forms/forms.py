from flask_wtf import FlaskForm
#from wtforms import Form
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from flask_ckeditor import CKEditorField

class LoginForm(FlaskForm):
    loginedt = StringField('Логин', validators=[DataRequired()])
    passwdedt = PasswordField('Пароль', validators=[DataRequired()])

class RegForm(FlaskForm):
    loginedt = StringField('Логин', validators=[DataRequired(), Length(min=4)], default='igor1')
    emailedt = EmailField('Электронная почта', validators=[DataRequired(), Email()], default='igor@mail.ru')
    usernameedt = StringField('Ваше имя', validators=[DataRequired(), Length(min=3, max=25)], default='Игорь')
    passwdedt = PasswordField('Пароль', validators=[DataRequired(), Length(min=4)])
    passwd2edt = PasswordField('Подтверждение пароля', validators=[DataRequired(), Length(min=4)])

class EditPost(FlaskForm):
    titleedt = StringField('Название', validators=[DataRequired(), Length(min=4)])
    contentedt = CKEditorField('Текст', validators=[DataRequired()])
    tagsedt = StringField('Теги (через запятую)', validators=[])


