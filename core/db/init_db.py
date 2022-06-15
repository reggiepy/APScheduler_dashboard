# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/6/14 下午 5:39 
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly

async def init_db(db: AsyncSession):
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    pass
