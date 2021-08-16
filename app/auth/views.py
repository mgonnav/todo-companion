from flask import flash, redirect, render_template, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.firestore_service import get_user, user_put
from app.forms import LoginForm, SignUpForm
from app.models import UserData, UserModel

from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user_document = get_user(username)

        if user_document.to_dict() is not None:
            password_hash = user_document.to_dict()['password']

            if check_password_hash(password_hash, password):
                user_data = UserData(username, password_hash)
                user = UserModel(user_data)

                login_user(user)

                return redirect(url_for('index'))

        flash('Invalid credentials.', category='danger')
        return redirect(url_for('auth.login'))

    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Come back soon!', category='success')

    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user_document = get_user(username)

        if user_document.to_dict() is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            user_put(user_data)

            flash('Registration successful. You can log in now.',
                  category='success')
            return redirect(url_for('auth.login'))
        else:
            flash('That username is already taken.', category='danger')
            return redirect(url_for('auth.signup'))

    return render_template('signup.html', form=form)
