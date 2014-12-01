"""
This module contains all host-related classes and helpers

"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, backref

from .base import Model


class Host(Model):
    """
    This is the ORM mapping for the hosts table

    """
    IP_MAX_LENGTH = 45

    __tablename__ = 'hosts'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    ip = Column(String(IP_MAX_LENGTH))
    schedule_id = Column(Integer, ForeignKey('schedules.id'))
    schedule = relationship('Schedule', backref='hosts')
    jobs = relationship('Job', backref='host')
