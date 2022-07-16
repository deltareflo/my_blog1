from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, BooleanField, TextAreaField,\
    DateTimeField, SelectField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    edad = IntegerField('Edad')
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrar')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], render_kw={"placeholder": "email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Contraseña"})
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')


class BlogForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(max=50)])
    subtitulo = StringField('Subtítulo', validators=[Length(max=50)])
    usuario = SelectField('Autor', coerce=int, validators=[DataRequired()])
    autor = StringField('Autor', validators=[DataRequired(), Length(max=20)])
    date = DateTimeField('Fecha')
    contenido = TextAreaField('Contenido')
