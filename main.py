import os

from dotenv import load_dotenv
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

from flask import (Flask, make_response, redirect, render_template, request,
                   session, url_for)

app = Flask(__name__)
bootstrap = Bootstrap(app)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

todos = ['Buy coffee', 'Read', 'Study online']


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


@app.route('/hello', methods=['GET', 'POST'])
def hello_world():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username

        return redirect(url_for('index'))

    user_ip = session.get('user_ip')
    username = session.get('username')
    context = {
        'user_ip': user_ip,
        'username': username,
        'todos': todos,
        'login_form': login_form
    }

    return render_template('hello.html', **context)
