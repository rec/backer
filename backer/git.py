from .task import Task
from pathlib import Path
from queue import Queue, Empty
import datetime
import functools
import os
import time


class Git(Task):
    def __init__(
        self,
        execute,
        name,
        target=None,
        source=None,
        create_at_startup=True,
        git_init=True,
        remotes=None,
        add_unknown_files=True,
        file_event_window=0.05,
        commit_message='%Y-%m-%dT%H:%M%SZ',
    ):
        """"
        `git commit` automatically on any change within a directory.

        Whenever any file changes within the `source` directory recursively,
        attempt to make a git commit, and if this succeeds, push it to all
        remotes.

        name:
          name of git backup

        source:
          source directory to be backed up (default is current directory)

        target:
          (not used)

        create_at_startup:
            If True, immediately create a backup if there is none,
            otherwise wait until the scheduled time for the first backup

        remotes:
          A dictionary mapping remote names to remote URLs

        git_init:
          If `source` is not a Git repository, then if `git_init` is
          true, then `git init` will be called, otherwise ValueError is raised

        add_unknown_files:
          If True, unknown files are automatically `git add`'ed

        file_event_window:
          If `file_event_window` is non-zero, then all file events during that
          time window (in seconds) are consolidated into a single git commit

        commit_message:
          A strftime-style format string for commit messages
        """
        super().__init__(execute, name, create_at_startup)
        self.queue = Queue()
        source = source or '.'
        self.source = Path(os.path.expandvars(source)).expanduser().resolve()
        self.git = functools.partial(execute.run, 'git', cwd=str(source))
        self.git_init = git_init or {}
        self.remotes = remotes or {}
        self.add_unknown_files = add_unknown_files
        self.file_event_window = file_event_window
        self.commit_message = commit_message

    def start(self):
        if self.create_at_startup:
            self._commit()

        self.execute.new_thread(self._service_queue, 'service_queue')
        self.execute.observe(self.queue.put, self.source)

    def _items_in_queue(self):
        items = []
        while True:
            try:
                items.append(self.queue.get(block=False))
            except Empty:
                return items

    def _service_queue(self):
        if self._items_in_queue():
            if self.file_event_window:
                time.sleep(self.file_event_window)
                self._items_in_queue()
            self._commit()

    def _commit(self):
        if not (self.source / '.git').is_dir():
            if not self.git_init:
                raise ValueError('%s is not a git directory' % self.source)
            self.git('init')
            for name, remote in self.remotes.items():
                self.git('remote', 'add', name, remote)

        lines = self.git('status', '--porcelain')
        if not self.add_unknown_files:
            lines = [i for i in lines if not i.startwith('??')]

        if lines:
            files = [i.split(maxsplit=1)[1] for i in lines]
            self.git('add', *files)

            if '%' in self.commit_message:
                msg = datetime.datetime.now().strftime(self.commit_message)
            else:
                msg = self.commit_message
            self.git('commit', '-am', msg)
            for remote in self.remotes:
                self.git('push', self.remote)
