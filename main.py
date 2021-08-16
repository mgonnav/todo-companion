import unittest

from flask import (flash, make_response, redirect, render_template, request,
                   session)
from flask_login import login_required, current_user

from app import create_app
from app.forms import LoginForm
from app.firestore_service import get_users, get_todos

app = create_app()


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found_404(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def internal_server_error_505(error):
    return render_template('500.html', error=error)


@app.route('/')
@login_required
def index():
    user_ip = request.remote_addr
    session['user_ip'] = user_ip

    response = make_response(redirect('/hello'))

    return response


@app.route('/hello')
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id

    if not user_ip or not username:
        return make_response(redirect('/auth/login'))

    context = {
        'user_ip': user_ip,
        'username': username,
        'todos': get_todos(user_id=username),
    }

    return render_template('hello.html', **context)
