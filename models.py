from shared import db
from sqlalchemy import column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import enum


class Usuarios(db.Model, UserMixin):
    __tablename__= 'blog_user'

    id = db.Column(Integer, primary_key=True)
    nombre= db.Column(String(length=50), nullable=False)
    edad = db.Column(Integer)
    email = db.Column(String(length=150), unique= True)
    password= db.Column(String(length=128))
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Usuarios.query.get(id)
    @staticmethod
    def get_by_email(email):
        return Usuarios.query.filter_by(email=email).first()


class Blog(db.Model):
    __tablename__ = 'blog_content'
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(length=50))
    subtitle = db.Column(String(length=50))
    # autor = db.Column(String(length=20))
    date = db.Column(DateTime)
    contenido = db.Column(Text)
    # Foreignkey
    id_user = db.Column(Integer, ForeignKey('blog_user.id'))
    user = db.relationship('Usuarios', backref='blog_user', lazy=True)


class User(UserMixin):
    pass