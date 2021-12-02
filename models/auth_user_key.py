from orm_engine import *
from mongoengine import *


class AuthUsersKeys(models):
    __tablename__ = 'auth_users_keys'

    token = StringField()
    user_id = StringField()
    expire_date = DateTimeField()
    iat_date = DateTimeField()

