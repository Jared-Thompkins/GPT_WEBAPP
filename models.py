from flask_login import UserMixin
from extensions import db


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def get_by_username(cls, username):
        user_data = db.users.find_one({"username": username})
        if not user_data:
            return None
        return cls(id=str(user_data["_id"]), username=user_data["username"], password=user_data["password"])

    @classmethod
    def get_by_id(cls, id):
        user_data = db.users.find_one({"_id": id})
        if not user_data:
            return None
        return cls(id=str(user_data["_id"]), username=user_data["username"], password=user_data["password"])

    def save(self):
        user_data = {
            "username": self.username,
            "password": self.password,
        }
        db.users.insert_one(user_data)
