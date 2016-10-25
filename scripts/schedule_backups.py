#!/usr/bin/env python
from __future__ import print_function
import schedule
import os
import time
import datetime
import subprocess

def _update_env_vars():
    env = {}
    os.environ['PGPASSFILE'] = '/tmp/.pgpass'
    env['POSTGRES_HOST'] = os.environ.get('POSTGRES_HOST', 'localhost')
    env['POSTGRES_PORT'] = os.environ.get('POSTGRES_PORT', '5432')
    env['POSTGRES_DB'] = os.environ.get('POSTGRES_DB', '')
    env['POSTGRES_USER'] = os.environ.get('POSTGRES_USER', 'postgres')
    env['POSTGRES_PASSWORD'] = os.environ.get('POSTGRES_PASSWORD', '')
    env['PGPASSWORD'] = os.environ.get('POSTGRES_PASSWORD', '')
    os.environ.update(env)

def _write_pgpass_file():
    env = os.environ
    with os.fdopen(os.open(os.environ['PGPASSFILE'], os.O_WRONLY | os.O_CREAT, 0o600), 'w') as f:
        print("{hostname}:{port}:{database}:{username}:{password}".format(
            hostname=env['POSTGRES_HOST'],
            port=env['POSTGRES_PORT'],
            database=env['POSTGRES_DB'],
            username=env['POSTGRES_USER'],
            password=env['POSTGRES_PASSWORD'],
            ),
            file=f
        )

def job():
    print("###################################")
    print("Time on Server: ", datetime.datetime.now())
    _update_env_vars()
    _write_pgpass_file()
    print("backing up")
    print(subprocess.check_output(['bash', '/usr/local/bin/pg_backup_rotated.sh'], env=os.environ))
    print("###################################")

def job_once():
    print("\nCreating first backup immediately:\n")
    job()
    print("\nDone creating initial backup\n")

def set_up_schedule():
    # backup whenever the container is booted, only runs once.
    job_once()

    every_day_at = os.environ.get('EVERY_DAY_AT', '03:02')
    schedule.every(1).days.at(every_day_at).do(job)
    print("Scheduled to run every day at: ", every_day_at, "(now: {})".format(datetime.datetime.now()))
    # Other examples would be:
    # schedule.every(10).minutes.do(job)
    # schedule.every(10).seconds.do(job)
    # schedule.every().hour.do(job)
    # schedule.every().day.at("10:30").do(job)
    # schedule.every().monday.do(job)
    # schedule.every().wednesday.at("13:15").do(job)

def run():
    set_up_schedule()
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    run()
