from . import execute
from pathlib import Path
from queue import Queue, Empty
import datetime
import functools
import threading
import time


def run(name, source=None, target=None,
        remotes=None,
        init=True,
        all=True,
        window=0.05,
        message='%Y-%m-%dT%H:%M%SZ',
        sleep=1):
    """"
    `git commit` automatically on any change within a directory.

    Whenever any file changes within the `source` directory recursively,
    attempt to make a git commit, and if this succeeds, push it to all remotes.

    source:
      source directory to be backed up

    target:
      (not used)

    name:
      name of git backup

    remotes:
      A dictionary mapping remote names to remote URLs
    """
    queue = Queue()
    git = functools.partial(execute.run, 'git', cwd=source)
    remotes = remotes or {}
    source = source or '.'

    def clear_queue():
        had_items = False
        while True:
            try:
                queue.get(block=False)
                had_items = True
            except Empty:
                return had_items

    def service_queue():
        while True:
            if not clear_queue():
                continue
            if window:
                time.sleep(window)
                clear_queue()
            commit()

    def commit():
        lines = git('status', '--porcelain')
        if not all:
            lines = [i for i in lines if not i.startwith('??')]

        if lines:
            files = [i.split(maxsplit=1)[1] for i in lines]
            git('add', *files)

            if '%' in message:
                msg = datetime.datetime.now().strftime(message)
            else:
                msg = message
            git('commit', '-am', msg)
            for remote in remotes:
                git('push', remote)

    def initialize():
        if not (Path(source) / '.git').is_dir():
            if not init:
                raise ValueError('%s is not a git directory' % source)
            git('init')
            for name, remote in remotes.items():
                git('remote', 'add', name, remote)

    threading.Thread(target=service_queue, daemon=True).start()
    initialize()
    execute.observe(source, queue.put, sleep)
