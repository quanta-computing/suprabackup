"""
This module handles database connections for suprabackup

"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# This is used just for proxying models to db.models.<something>
from .. import models


def connect(engine, host, db, user, password=''):
    """
    Connects to the database using the ORM and returns a db session

    """
    user_string = "{}:{}".format(user, password)
    e = create_engine('{}://{}@{}/{}'.format(engine, user_string, host, db))
    s = sessionmaker(bind=e)
    return s
