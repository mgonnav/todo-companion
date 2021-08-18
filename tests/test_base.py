from flask import current_app, url_for
from flask_testing import TestCase
from flask_login import login_user, logout_user, current_user

from main import app
from app.firestore_service import db
from app.models import UserData, UserModel


class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['USERNAME'] = 'test_user'
        app.config['PASSWORD'] = 'test_password'
        return app

    def setUp(self):
        test_user = {
            'username': app.config['USERNAME'], 
            'password': app.config['PASSWORD']
        }
        self.client.post(url_for('auth.login'), data=test_user, follow_redirects=True)

    def tearDown(self):
        self.client.get(url_for('auth.logout'), follow_redirects=True)

    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_app_csrf_disabled(self):
        self.assertFalse(current_app.config['WTF_CSRF_ENABLED'])

    def test_index_redirects(self):
        response = self.client.get(url_for('index'))
        self.assertRedirects(response, url_for('home'))

    def test_home_template(self):
        response = self.client.get(url_for('home'))
        self.assertTemplateUsed('home.html')

    def test_add_update_remove_todo(self):
        new_todo = {
            'description': 'Test code for flask app'
        }
        response = self.client.post(url_for('home'), data=new_todo, follow_redirects=True)
        self.assertMessageFlashed('To-do added successfully', category='success')
        self.assertIn(b'Test code for flask app', response.data)
        self.assertIn(b'class="badge badge-warning clickable">To-do</label>', response.data)
        self.assertNotIn(b'class="badge badge-info clickable">Done</label>', response.data)

        test_user_todos = db.collection(f"users/{app.config['USERNAME']}/todos")
        new_todo_id = test_user_todos.get()[0].id

        response = self.client.post(url_for('update', todo_id=new_todo_id), follow_redirects=True)
        self.assertIn(b'class="badge badge-info clickable">Done</label>', response.data)
        self.assertNotIn(b'class="badge badge-warning clickable">To-do</label>', response.data)

        response = self.client.post(url_for('delete', todo_id=new_todo_id), follow_redirects=True)
        self.assertNotIn(b'class="badge badge-warning clickable">To-do</label>', response.data)
        self.assertNotIn(b'class="badge badge-info clickable">Done</label>', response.data)
