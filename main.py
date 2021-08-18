import unittest

from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from app import create_app
from app.firestore_service import delete_todo, get_todos, put_todo, update_todo
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

    return redirect(url_for('home'))


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = TodoForm()
    if form.validate_on_submit():
        put_todo(user_id=current_user.id, description=form.description.data)
        flash('To-do added successfully', category='success')
        return redirect(url_for('home'))

    user_ip = session.get('user_ip')
    username = current_user.id

    context = {
        'user_ip': user_ip,
        'username': username,
        'todos': get_todos(user_id=username),
        'todo_form': form
    }

    return render_template('home.html', **context)


@app.route('/todos/delete/<todo_id>', methods=['POST'])
@login_required
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id, todo_id)
    return redirect(url_for('home'))


@app.route('/todos/update/<todo_id>', methods=['POST'])
@login_required
def update(todo_id):
    user_id = current_user.id
    update_todo(user_id, todo_id)
    return redirect(url_for('home'))
