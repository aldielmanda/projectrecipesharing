from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models.user import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Masuk ke Hub')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField('Email Kampus', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Ulangi Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Peran Akun', choices=[('user', 'User Standar'), ('admin', 'Administrator Penguji')])
    submit = SubmitField('Daftar Sekarang')

    def validate_username(self, u):
        if User.query.filter_by(username=u.data).first(): raise ValidationError('Username telah terpakai!')
    def validate_email(self, e):
        if User.query.filter_by(email=e.data).first(): raise ValidationError('Email sudah terdaftar!')