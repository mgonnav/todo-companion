from flask import flash, make_response, redirect, render_template, url_for
from flask_login import login_user, login_required, logout_user

from app.firestore_service import get_user
from app.forms import LoginForm
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
            password_from_db = user_document.to_dict()['password']

            if password == password_from_db:
                user_data = UserData(username, password)
                user = UserModel(user_data)

                login_user(user)

                return redirect(url_for('index'))

        flash('Invalid credentials.', category='danger')
        return make_response(redirect('/auth/login'))

    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Come back soon!', category='success')

    return redirect(url_for('auth.login'))
