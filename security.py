from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):		# A safer way to compare strings
        print('authenticated!')
        return user


def identity(payload):
    print('identity check passed!')
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
