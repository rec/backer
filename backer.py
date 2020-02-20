from pathlib import Path
import datetime
import os
import schedule
import subprocess
import sys
import time
import watchdog

__version__ = '0.1.0'

RSYNC = 'rsync', '--archive', '-v', '--exclude=.git'


def observe_files(callback, *paths, sleep_time=1):
    class Handler:
        def __init__(self, path):
            self.path = path

        def dispatch(self, event):
            if not event.is_directory:
                callback(self.path, event)

    o = watchdog.Observer()
    for path in paths:
        o.schedule(Handler(path), path, recursive=True)
        o.start()

    try:
        while True:
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        o.stop()
    o.join()


def commit_all(add_unknown=True, message='%Y-%m-%dT%H:%M%SZ', push=True):
    lines = execute('git', 'status', '--porcelain')

    if not add_unknown:
        lines = [i for i in lines if not i.startwith('??')]

    if not lines:
        return

    files = [i.split(maxsplit=1)[1] for i in lines]
    execute('git', 'add', *files)

    if '%' in message:
        message = datetime.datetime.now().strftime(message)
    execute('git', 'commit', '-am', message)

    if push:
        execute('git', 'push')


def execute(*args):
    print('$', *args)
    result = subprocess.check_output(args, encoding='utf-8')
    print(result)
    return [i.rstrip() for i in result.splitlines()]


def add_remotes(*remotes, push=True):
    existing = set()
    urls = set()
    for line in execute('git', 'remote', '-v'):
        name, url, _ = line.split()
        existing.add(name)
        urls.add(url)

    remotes = [r for r in remotes if r not in urls]

    for remote in remotes:
        i = 0
        while True:
            name = 'remote_%d' % i
            if name not in existing:
                break
            i += 1

        execute('git', 'remote', 'add', name, remotes)
        if push:
            execute('git', 'push')


def git_init():
    if not Path('.git').is_dir():
        execute('git', 'init')
        return True


def schedule_rsync(source, target, *slots, schedule=schedule, create=True):
    def schedule_one(period, at=None):
        sched = getattr(schedule.every(), period)
        if at:
            if len(at.split(':')[0]) < 2:
                # Rewrite 4:32 to 04:32
                at = '0' + a
            sched = sched.at(at)
        rsync_dir = Path(target) / period

        def func():
            return execute(*RSYNC, source, rsync_dir)

        if create and not rsync_dir.exists():
            func()

        sched.do(func)

   for slot in slots:
       schedule_one(*slot.split('@', maxsplit=1))


def main(source, target, sleep_time=1):
    schedule_rsync(source, target, 'wednesday@5:32', 'day@4:32')
    schedule.every().second.do(commit_all)

    while True:
        schedule.run_pending()
        time.sleep(sleep_time)


if __name__ == '__main__':
    main(*sys.argv[1:])
