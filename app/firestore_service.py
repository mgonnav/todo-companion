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
    todos_ref = db.collection('users').document(user_id).collection('todos')
    query = todos_ref.order_by('done')
    return query.get()


def put_user(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({'password': user_data.password})


def put_todo(user_id, description):
    todo_collection_ref = db.collection(f'users/{user_id}/todos')
    todo_collection_ref.add({'description': description, 'done': False})


def delete_todo(user_id, todo_id):
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.delete()


def update_todo(user_id, todo_id):
    todo_ref = _get_todo_ref(user_id, todo_id)
    done = todo_ref.get().to_dict()['done']
    todo_ref.update({'done': not done})


def _get_todo_ref(user_id, todo_id):
    return db.document(f'users/{user_id}/todos/{todo_id}')
