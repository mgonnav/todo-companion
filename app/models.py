from flask_login import UserMixin
from .firestore_service import get_user


class UserData:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class UserModel(UserMixin):
    def __init__(self, user_data):
        """
        :param user_data: UserData
        """
        self.id = user_data.username
        self.password = user_data.password

    @staticmethod
    def query(user_id):
        user_document = get_user(user_id)
        user_data = UserData(user_document.id,
                             password=user_document.to_dict()['password'])

        return UserModel(user_data)
