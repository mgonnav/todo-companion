import firebase_admin
from firebase_admin import credentials, firestore

credential = credentials.ApplicationDefault()
project_id = 'mgonnav-flask-todo'

try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(credential, {'projectId': project_id})

db = firestore.client()


def get_users():
    return db.collection('users').get()


def get_user(user_id):
    return db.collection('users').document(user_id).get()


def get_todos(user_id):
    return db.collection('users').document(user_id).collection('todos').get()
