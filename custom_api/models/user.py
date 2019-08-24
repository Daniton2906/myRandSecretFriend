# -*- coding: utf-8 -*-
from custom_api.models import db
from custom_api.utils import bcrypt

class UserBot(db.Document):

    names = db.StringField()
    first_last_name = db.StringField()
    second_last_name = db.StringField()
    gender = db.StringField()
    phone_number = db.StringField()
    email = db.StringField()
    username = db.StringField()
    password = db.StringField()
    active = db.BooleanField(default=True)

    @staticmethod
    def get_user_with_username_and_password(username, password):
        user = UserBot.objects(username=username).first()
        if user is not None and bcrypt.check_password_hash(user.password, password.encode('utf-8')):
            return user
        else:
            return None
    
    @staticmethod
    def hashed_password(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')
    