from pathlib import Path
from queue import Queue, Empty
import datetime
import functools
import os
import threading
import time
from .task import Task


class Git(Task):
    def __init__(
        self,
        execute,
        name,
        target=None,
        source=None,
        create=True,
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

        remotes:
          A dictionary mapping remote names to remote URLs

        create:
          If `source` is not a Git repository, then if `create` is true, then
          `create init` will be called, otherwise an ValueError is raised

        add_unknown_files:
          If True, unknown files are automatically `git add`'ed

        file_event_window:
          If `file_event_window` is non-zero, then all file events during that
          time window (in seconds) are consolidated into a single git commit

        commit_message:
          A strftime-style format string for commit messages
        """
        super().__init__(execute, name, create)
        self.queue = Queue()
        source = source or '.'
        self.source = Path(os.path.expandvars(source)).expanduser().resolve()
        self.git = functools.partial(execute.run, 'git', cwd=str(source))
        self.remotes = remotes or {}
        self.add_unknown_files = add_unknown_files
        self.file_event_window = file_event_window
        self.commit_message = commit_message

    def start(self):
        if self.create:
            self.commit()

        # TODO: this thread doesn't get stopped
        threading.Thread(target=self.service_queue, daemon=True).start()
        self.execute.observe(self.queue.put, self.source)

    def items_in_queue(self):
        items = []
        while True:
            try:
                items.append(self.queue.get(block=False))
            except Empty:
                return items

    def service_queue(self):
        while True:
            if self.items_in_queue():
                if self.file_event_window:
                    time.sleep(self.file_event_window)
                    self.items_in_queue()
                self.commit()

    def commit(self):
        if not (self.source / '.git').is_dir():
            if not self.create:
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
