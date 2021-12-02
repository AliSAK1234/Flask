from orm_engine import *
from mongoengine import *


class ResUsers(models):
    __tablename__ = 'res_users'

    name = StringField()
    email = StringField()
    password = StringField()
    phone = StringField()
