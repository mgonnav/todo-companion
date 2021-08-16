from flask import render_template, make_response, redirect, session, flash
from app.forms import LoginForm

from . import auth

names = []


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        if form.validate():
            username = form.username.data
            if username in names:
                flash('Username is already registered', category='danger')
                return make_response(redirect('/auth/login'))
            else:
                session['username'] = username
                names.append(username)

                flash('Username registered successfully', category='success')
                return make_response(redirect('/'))
        else:
            flash('Invalid form data', category='danger')
            return make_response(redirect('/auth/login'))

    return render_template('login.html', form=form)
