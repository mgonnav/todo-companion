from flask_testing import TestCase
from flask import current_app, url_for

from main import app


class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_app_csrf_disabled(self):
        self.assertFalse(current_app.config['WTF_CSRF_ENABLED'])

    def test_index_redirects(self):
        response = self.client.get(url_for('index'))
        self.assertRedirects(response, url_for('hello'))

    def test_hello_get_not_logged(self):
        response = self.client.get(url_for('hello'))
        self.assertRedirects(response, url_for('auth.login'))

    def test_auth_blueprint_exists(self):
        self.assertIn('auth', self.app.blueprints)

    def test_login_get(self):
        response = self.client.get(url_for('auth.login'))
        self.assert200(response)

    def test_login_template(self):
        self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('login.html')

    def test_login_post_new(self):
        import uuid
        fake_form = {
            'username': uuid.uuid4().hex[:8],
            'password': uuid.uuid4().hex[:8]
        }
        response = self.client.post(url_for('auth.login'), data=fake_form)

        self.assertRedirects(response, url_for('index'))
        self.assertMessageFlashed('Username registered successfully',
                                  'success')

    def test_login_post_already_registered(self):
        import uuid
        fake_form = {
            'username': uuid.uuid4().hex[:6],
            'password': uuid.uuid4().hex[:6]
        }
        self.client.post(url_for('auth.login'), data=fake_form)
        response = self.client.post(url_for('auth.login'), data=fake_form)

        self.assertRedirects(response, url_for('auth.login'))
        self.assertMessageFlashed('Username is already registered', 'danger')

    def test_login_post_invalid_form(self):
        invalid_form = {'username': '', 'password': ''}
        response = self.client.post(url_for('auth.login'), data=invalid_form)

        self.assertRedirects(response, url_for('auth.login'))
        self.assertMessageFlashed('Invalid form data', 'danger')
