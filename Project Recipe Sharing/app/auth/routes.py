from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models.user import User
from app.auth.forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('recipes.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            flash(f'Selamat datang, {user.username}!', 'success')
            return redirect(request.args.get('next') or url_for('recipes.index'))
        flash('Kombinasi Username dan Password keliru.', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: return redirect(url_for('recipes.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(username=form.username.data, email=form.email.data, role=form.role.data)
        u.password = form.password.data
        db.session.add(u); db.session.commit()
        flash('Pendaftaran sukses! Silakan login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah keluar sistem.', 'info')
    return redirect(url_for('recipes.index'))