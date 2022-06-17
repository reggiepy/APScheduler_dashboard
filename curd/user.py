# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/14 下午 3:39 
from sqlalchemy import Column, Integer, String

from core.db.base_class import Base
from curd.base import CRUDBase


class User(CRUDBase[Base]):
    id = Column(Integer, primary_key=True)
    user_name = Column(String(20))
    password = Column(String(30))

    def __repr__(self):
        return "<User(id='%s', user_name='%s')>" % (self.id, self.user_name)

