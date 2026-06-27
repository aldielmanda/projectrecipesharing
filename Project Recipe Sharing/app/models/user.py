from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), default='user')
    _password_hash = db.Column('password_hash', db.String(256), nullable=False)

    recipes = db.relationship('Recipe', backref='author', lazy='dynamic')
    reviews = db.relationship('Review', backref='reviewer', lazy='dynamic', cascade='all, delete-orphan')
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def password(self): raise AttributeError('Password terenkapsulasi secara privat!')
    @password.setter
    def password(self, pwd): self._password_hash = generate_password_hash(pwd)
    def verify_password(self, pwd): return check_password_hash(self._password_hash, pwd)
    def is_admin(self): return self.role == 'admin'