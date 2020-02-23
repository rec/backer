from .backer import execute, observe
from pathlib import Path
import datetime
import os


def git(source, remotes, init, all, window, message, sleep):
    """"`git commit` automatically on any change within a directory.

    Whenever any file changes within the `source` directory recursively,
    attempt to make a git commit, and if this succeeds, push it to all remotes.

    source:
      source directory to be backed up

    remotes:

    """
    def commit_all():
        lines = execute('git', 'status', '--porcelain')

        if not all:
            lines = [i for i in lines if not i.startwith('??')]

        if lines:
            files = [i.split(maxsplit=1)[1] for i in lines]
            execute('git', 'add', *files)

            if '%' in message:
                msg = datetime.datetime.now().strftime(message)
            else:
                msg = message
            execute('git', 'commit', '-am', msg)
            for remote in remotes:
                execute('git', 'push', remote)

    def callback():
        os.chdir(source)
        if not Path('.git').is_dir():
            execute('git', 'init')
            for name, remote in remotes.items():
                execute('git', 'remote', 'add', name, remote)
        commit_all()

    observe(source, callback, sleep)
