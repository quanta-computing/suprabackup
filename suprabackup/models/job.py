"""
This module contains all job-related classes and helpers

"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, SmallInteger, String, DateTime

from .base import Model


class Job(Model):
    """
    This is the ORM mapping for a single backup job
    An attribute 'host' is created by a relationship in the Host class

    """
    SHORT = 0
    LONG = 1

    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    type = Column(SmallInteger)
    host_id = Column(Integer, ForeignKey('hosts.id'))
    file_path = Column(String(255))
    status = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    expires = Column(DateTime)
