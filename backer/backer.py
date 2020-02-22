# from . import scheduler, observer



from pathlib import Path
import datetime
import os
import sys
import time

__version__ = '0.1.0'

def main(source, target, sleep_time=1):
    schedule_rsync(source, target, 'wednesday@5:32', 'day@4:32')
    schedule.every().second.do(commit_all)

    while True:
        schedule.run_pending()
        time.sleep(sleep_time)


if __name__ == '__main__':
    main(*sys.argv[1:])
