#!/usr/bin/python
"""
Usage: suprashell.py [config]
Author: Matthieu 'Korrigan' Rosinski <mro@quanta-computing.com>

This script gives a shell to Suprabackup database using the ORM

"""
import os
import sys

from suprabackup import db
from suprabackup.config import load_config
from suprabackup.models import *

if __name__ == "__main__":
    os.environ['PYTHONINSPECT'] = 'True'
    if len(sys.argv) > 1:
        print("Loading config from {}".format(sys.argv[1]))
        config = load_config(path=sys.argv[1])
    else:
        config = load_config()
    session = db.connect(engine=config['database']['engine'],
                            host=config['database']['host'],
                            db=config['database']['db'],
                            user=config['database']['user'],
                            password=config['database'].get('password', ''),
                        )
