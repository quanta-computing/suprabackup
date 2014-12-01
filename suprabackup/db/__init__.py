"""
This module handles database connections for suprabackup

"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# This is used just for proxying models to db.models.<something>
from .. import models
from ..models.base import Model


def get_engine(engine, host, db, user, password=''):
    """
    Get the engine corresponding to the given parameters

    """
    user_string = "{}:{}".format(user, password)
    return create_engine('{}://{}@{}/{}'.format(engine, user_string, host, db))


def connect_engine(engine):
    """
    Get a session from an engine

    """
    return sessionmaker(bind=engine)


def connect(engine, host, db, user, password=''):
    """
    Connects to the database using the ORM and returns a db session

    """
    return connect_engine(get_engine(engine, host, db, user, password))
