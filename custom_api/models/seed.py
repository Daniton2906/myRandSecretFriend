from custom_api.models.user import UserBot

def make_default_user():
    user = UserBot(username="admin", password=UserBot.hashed_password("admin"))
    user.save()

def seed():
    make_default_user()
