from pathlib import Path
from queue import Queue, Empty
import datetime
import functools
import os
import threading
import time


def run(execute, name, target=None, source=None,
        remotes=None,
        git_init=True,
        add_unknown_files=True,
        file_event_window=0.05,
        commit_message='%Y-%m-%dT%H:%M%SZ'):
    """"
    `git commit` automatically on any change within a directory.

    Whenever any file changes within the `source` directory recursively,
    attempt to make a git commit, and if this succeeds, push it to all remotes.

    name:
      name of git backup

    source:
      source directory to be backed up (default is current working directory)

    target:
      (not used)

    remotes:
      A dictionary mapping remote names to remote URLs

    git_init:
      If `source` is not a Git repository, then if `git_init` is true, then
      `git init` will be called, otherwise an ValueError is raised

    add_unknown_files:
      If True, unknown files are automatically `git add`'ed

    file_event_window:
      If `file_event_window` is non-zero, then all file events during that
      time window (in seconds) are consolidated into a single git commit

    commit_message:
      A strftime-style format string for commit messages
    """
    queue = Queue()
    git = functools.partial(execute.run, 'git', cwd=source)
    remotes = remotes or {}
    source = Path(os.path.expandvars(source or '.')).expanduser().resolve()

    def items_in_queue():
        items = []
        while True:
            try:
                items.append(queue.get(block=False))
            except Empty:
                return items

    def service_queue():
        while True:
            if items_in_queue():
                if file_event_window:
                    time.sleep(file_event_window)
                    items_in_queue()
                commit()

    def commit():
        lines = git('status', '--porcelain')
        if not add_unknown_files:
            lines = [i for i in lines if not i.startwith('??')]

        if lines:
            files = [i.split(maxsplit=1)[1] for i in lines]
            git('add', *files)

            if '%' in commit_message:
                msg = datetime.datetime.now().strftime(commit_message)
            else:
                msg = commit_message
            git('commit', '-am', msg)
            for remote in remotes:
                git('push', remote)

    def initialize():
        if not (source / '.git').is_dir():
            if not git_init:
                raise ValueError('%s is not a git directory' % source)
            git('init')
            for name, remote in remotes.items():
                git('remote', 'add', name, remote)

    threading.Thread(target=service_queue, daemon=True).start()
    initialize()

    execute.observe(queue.put, source.absolute())
