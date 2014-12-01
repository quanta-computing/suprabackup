#!/usr/bin/python
"""
Usage: suprabackup_receive.py
Author: Matthieu 'Korrigan' Rosinski <mro@quanta-computing.com>

This script is a wrapper to handle xtrabackup uploads for Percona server backups

"""
import os
import sys
import datetime

from suprabackup import db
from suprabackup.logging import setup_logging
from suprabackup.config import load_config
from suprabackup.models import *

logger = None

opts = None
config = {}


def main():
    """
    Main function for receive_xtrabackup

    """
    import argparse
    global opts
    global logger
    global config

    parser = argparse.ArgumentParser(
        description='This program is a wraper for receiving Xtrabackup uploads and storing them',
        epilog='Copyright Quanta 2014')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Switch to loglevel DEBUG')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose mode')
    parser.add_argument('-f', '--config',
                        help='Location of the configuration file')
    parser.add_argument('-p', '--path',
                        help='Where to store the backups')
    parser.add_argument('-t', '--test',
                        help='Test mode: Connect to db and prints out configuration')

    opts = parser.parse_args()
    overrides = {}
    logger = setup_logging('suprabackup-receive', verbose=opts.verbose, debug=opts.debug)
    if opts.path:
        overrides['base_path'] = opts.path
    if opts.config:
        config = load_config(role='receive', overrides=overrides, path=opts.config)
    else:
        config = load_config(role='receive', overrides=overrides)
    logger.debug("Loaded configuration file {}".format(config.file))

    session = connect_db()
    host = get_host(session)
    start_time = datetime.datetime.now()
    path = build_backup_path(create_host_backup_dir(host.name), start_time)
    job = host.new_job(start_time)
    session.add(job)
    pipe_upload(path)
    job.end()


def test():
    """
    Prints out configuration

    """
    import pprint

    print(pprint.pprint(config))


def connect_db():
    """
    Connects to the database specified in configuration file and returns a cursor

    """
    try:
        session = db.connect(engine=config['database']['engine'],
                             host=config['database']['host'],
                             db=config['database']['db'],
                             user=config['database']['user'],
                             password=config['database'].get('password', ''),
                             )
        logger.debug("Successfully connected to databse {}"
                        .format(config['database']['db']))
        return session
    except KeyError as e:
        logger.error("Cannot connect to database: {0} not defined"
                     .format(e))
    except Exception as e:
        logger.error("Cannot connect to database {0} on {1}: {2}"
                     .format(config['database']['name'],
                             config['database']['host'],
                             e))
    return None


def get_host(session):
    """
    Returns an Host object from SSH_CLIENT environ variable

    """
    ssh_client = os.getenv('SSH_CLIENT')
    if not ssh_client:
        logger.critical("The client does not appear to be a SSH client")
        sys.exit(1)
    ip = ssh_client.split()[0]
    try:
        return session.query(Host).filter(Host.ip==ip).one()
    except Exception as e:
        logger.critical("Cannot find client hostname for IP {}: {}"
                        .format(ip, e))
        sys.exit(1)


def create_host_backup_dir(hostname):
    """
    Creates the host backup dir and return it

    """
    path = os.path.join(config['base_path'], hostname)
    try:
        if not os.path.isdir(path):
            logger.info("Creating directory {0}".format(path))
            os.mkdir(path, 0755)
        else:
            logger.debug("Directory {0} already exists, skipping".format(path))
        return path
    except OSError as e:
        logger.critical("Cannot make directory {0}: [{1}] {2}"
                        .format(path, e.errno, e.strerror))
        sys.exit(1)


def build_path(host_path, start_time):
    """
    Returns the full path of the backup

    """
    filename = '{}-{}.tar.gz'.format(config['file_prefix'],
                                     start_time.strftime("%Y-%m-%d_%H-%M"))
    return os.path.join(host_path, filename)


def pipe_upload(filename):
    """
    Pipe the uploaded xtrabackup to a file

    """
    import subprocess

    with open(filename, 'wb') as f:
        logger.info("Uploading backup into {0}".format(filename))
        bs = config['read_size']
        while 42:
            data = sys.stdin.read(bs)
            f.write(data)
            if len(data) < bs:
                break


if __name__ == "__main__":
    main()
