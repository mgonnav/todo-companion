import os

from dotenv import load_dotenv
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
import unittest
from wtforms.fields import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

from flask import (Flask, make_response, redirect, render_template, request,
                   session, url_for, flash)

app = Flask(__name__)
bootstrap = Bootstrap(app)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

todos = ['Buy coffee', 'Read', 'Study online']
names = []


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


@app.errorhandler(404)
def not_found_404(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def internal_server_error_505(error):
    return render_template('500.html', error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr
    session['user_ip'] = user_ip

    response = make_response(redirect('/hello'))

    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        if form.validate():
            username = form.username.data
            if username in names:
                flash('Username is already registered', category='danger')
                return make_response(redirect('/login'))
            else:
                session['username'] = username
                names.append(username)

                flash('Username registered successfully', category='success')
                return make_response(redirect('/'))
        else:
            flash('Invalid form data', category='danger')
            return make_response(redirect('/login'))

    return render_template('login.html', form=form)


@app.route('/hello')
def hello():
    user_ip = session.get('user_ip')
    username = session.get('username')

    if not user_ip or not username:
        return make_response(redirect('/login'))

    context = {
        'user_ip': user_ip,
        'username': username,
        'todos': todos,
    }

    return render_template('hello.html', **context)
