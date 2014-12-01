"""
This module contains all job-related classes and helpers

"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, SmallInteger, String, DateTime

from .base import Model


class JobStatus:
    """
    A simple class to validate Job status

    """
    UNKNOWN = 0
    IN_PROGRESS = 1
    DONE = 2
    VERIFIED = 3
    FAILED = 4

    @classmethod
    def is_valid(klass, status=0):
        """
        Returns True if status corresponds to valid status

        """
        if status >= klass.UNKNOWN and status <= klass.FAILED:
            return True
        return False



class Job(Model):
    """
    This is the ORM mapping for a single backup job
    An attribute 'host' is created by a relationship in the Host class

    """
    SHORT = 0
    LONG = 1

    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    type = Column(SmallInteger, default=SHORT)
    host_id = Column(Integer, ForeignKey('hosts.id'))
    file_path = Column(String(255))
    status = Column(Integer, default=JobStatus.UNKNOWN)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    expires = Column(DateTime)
