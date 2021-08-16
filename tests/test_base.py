from flask_testing import TestCase
from flask import current_app, url_for

from main import app


class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['USERNAME'] = 'mateo'
        app.config['PASSWORD'] = 'password'
        return app

    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_app_csrf_disabled(self):
        self.assertFalse(current_app.config['WTF_CSRF_ENABLED'])

    def test_index_redirects(self):
        test_user = {
            'username': current_app.config['USERNAME'],
            'password': current_app.config['PASSWORD']
        }
        self.client.post(url_for('auth.login'), data=test_user)

        response = self.client.get(url_for('index'))

        self.assertRedirects(response, url_for('hello'))

    def test_auth_blueprint_exists(self):
        self.assertIn('auth', self.app.blueprints)

    def test_login_get(self):
        response = self.client.get(url_for('auth.login'))
        self.assert200(response)

    def test_login_template(self):
        self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('login.html')

    def test_login_logout(self):
        user = {
            'username': current_app.config['USERNAME'],
            'password': current_app.config['PASSWORD']
        }

        response = self.client.post(url_for('auth.login'), data=user)
        self.assertRedirects(response, url_for('index'))

        response = self.client.get(url_for('auth.logout'))
        self.assertRedirects(response, url_for('auth.login'))
        self.assertMessageFlashed('Come back soon!', category='success')

    def test_login_post_unregistered_user(self):
        unregistered_user = {
            'username': 'unregistered',
            'password': 'unregistered_pass'
        }
        response = self.client.post(url_for('auth.login'),
                                    data=unregistered_user)

        self.assertRedirects(response, url_for('auth.login'))
        self.assertMessageFlashed('Invalid credentials.', category='danger')
