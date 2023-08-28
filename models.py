from flask_login import UserMixin
from extensions import db
from bson import ObjectId


class User(UserMixin):
    def __init__(self, id, username, password):
        assert isinstance(id, str), "ID must be a string"
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
        user_data = db.users.find_one({"_id": ObjectId(id)})
        if not user_data:
            return None
        return cls(id=str(user_data["_id"]), username=user_data["username"], password=user_data["password"])

    def save(self):
        user_data = {
            "username": self.username,
            "password": self.password,
        }
        db.users.insert_one(user_data)
    
    def get_id(self):
        return str(self.id)
