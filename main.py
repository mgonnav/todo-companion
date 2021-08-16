import unittest

from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from app import create_app
from app.firestore_service import get_todos, get_users, put_todo
from app.forms import LoginForm, TodoForm

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

    return redirect(url_for('hello'))


@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    form = TodoForm()
    if form.validate_on_submit():
        put_todo(user_id=current_user.id, description=form.description.data)
        flash('To-do added successfully', category='success')
        return redirect(url_for('hello'))

    user_ip = session.get('user_ip')
    username = current_user.id

    context = {
        'user_ip': user_ip,
        'username': username,
        'todos': get_todos(user_id=username),
        'todo_form': form
    }

    return render_template('hello.html', **context)
