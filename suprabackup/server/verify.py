"""
This module contains utils to verify past jobs

"""
from ..models import Job, JobStatus
from .. import db


class SupraVerify:
    """
    This class is used to store logger, config and db connection with utils
    for verifying last backup jobs

    """

    def __init__(self, config, logger):
        """
        Sets up SupraReceive with given config/logger and db connection

        """
        self.config = config
        self.logger = logger


    def verify(self):
        """
        Fetch all backups from database and check each file
        Updates the job status accordingly

        """
        self.logger.debug("Started verify")
        jobs = []
        with db.within_session(self.config, self.logger) as session:
            jobs = session.query(
                Job.id, Job.file_path
                ).filter(Job.status == JobStatus.DONE)
        for job_id, file_path in jobs:
            self.verify_one(job_id, file_path)
        self.logger.debug("Ended verify")

    def verify_job(self, job_id):
        """
        Verify a job from it's ID

        """
        file_path = None
        self.logger.info("Started verify with job_id #{}".format(job_id))
        with db.within_session(self.config, self.logger) as session:
            file_path, = session.query(
                Job.file_path
                ).filter(Job.id == job_id).one()
        return self.verify_one(job_id, file_path)

    def verify_one(self, job_id, file_path):
        """
        Verify a single job

        """
        status = self.check_file(file_path)
        with db.within_session(self.config, self.logger) as session:
            job = session.query(Job).filter(Job.id == job_id).one()
            if status:
                self.logger.info("Job {} for host {} is OK"
                                 .format(job.id, job.host.name))
                job.status = JobStatus.VERIFIED
            else:
                self.logger.warning("Job {} for host {} is NOT OK"
                                    .format(job_id, job.host.name))
                job.status = JobStatus.FAILED

    def check_file(self, path):
        """
        Checks the TAR archive at path and returns True if OK

        """
        import subprocess

        with open('/dev/null', 'w') as null:
            ret = subprocess.call(['tar', '-tzf', path],
                                  stdout=null, stderr=null, stdin=null)
            if ret:
                return False
            else:
                return True


def verify_backups(config, logger):
    """
    A simple wrapper to SupraVerify

    """
    verifier = SupraVerify(config, logger)
    verifier.verify()


def verify_job(config, logger, job_id):
    """
    Wrapper for verifying a single job

    """
    verifier = SupraVerify(config, logger)
    verifier.verify_job(job_id)
