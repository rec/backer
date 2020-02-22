from .execute import execute
from .observer import observe_path
from pathlib import Path
import datetime
import os


def git(source, name, user, remote, init, all, window, message, sleep):
    def commit_all():
        lines = execute('git', 'status', '--porcelain')

        if not all:
            lines = [i for i in lines if not i.startwith('??')]

        if lines:
            files = [i.split(maxsplit=1)[1] for i in lines]
            execute('git', 'add', *files)

            if '%' in message:
                message = datetime.datetime.now().strftime(message)
            execute('git', 'commit', '-am', message)
            for remote in remotes:
                execute('git', 'push', remote)

    def callback():
        os.chdir(source)
        if not Path('.git').is_dir():
            execute('git', 'init')
            for name, remote in remotes.items():
                execute('git', 'remote', 'add', name, remote)
        commit_all()

    observe_path(callback, source, sleep)
