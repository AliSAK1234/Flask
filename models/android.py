from orm_engine import *
from mongoengine import *


class Android(models):
    __tablename__ = 'android'

    rev_pld_var = FloatField()
    src_port = IntField()
    pld_distinct = IntField()
    rev_hdr_ccnt = ListField()
    bytes_out = IntField()
    hdr_mean = StringField()

