from ._task import Task
from dataclasses import dataclass
from pathlib import Path
from queue import Queue, Empty
import datetime
import functools
import os
import sys
import time

# How long before timing out the service queue?
QUEUE_TIMEOUT = 1


@dataclass
class Git(Task):
    """
    `git commit` automatically on any change within a directory.

    Whenever any file changes within the `source` directory recursively,
    attempt to make a git commit, and if this succeeds, push it to all
    remotes.
    """

    target: str = None
    source: str = None
    git_init: bool = True
    remotes: dict = None
    add_unknown_files: bool = True
    file_event_window: float = 0.05
    commit_message: str = "%Y-%m-%dT%H:%M%SZ"

    def __post_init__(self):
        self.queue = Queue()
        self.source = os.path.expandvars(self.source or ".")
        self.source = Path(self.source).expanduser()
        self.git = self.execute and functools.partial(
            self.execute.run, "git", cwd=str(self.source)
        )

        if not (self.git_init or (self.source / ".git").is_dir()):
            raise ValueError(_ERROR_NO_GIT_DIR % self.source)

    def start(self):
        if self.create_at_startup:
            self._commit()

        self.execute.new_thread(self._service_queue, "service_queue")
        self.execute.observe(self.queue.put, self.source)

    def _service_queue(self):
        try:
            self.queue.get(timeout=QUEUE_TIMEOUT)
        except Empty:
            return
        if self.file_event_window:
            time.sleep(self.file_event_window)
        with self.queue.mutex:
            self.queue.queue.clear()
        self._commit()

    def _initialize(self):
        if isinstance(self.remotes, dict):
            requested = self.remotes
        else:
            requested = {k: None for k in self.remotes or ()}
        remotes = list(requested)

        if not (self.source / ".git").is_dir():
            self.git("init")
            self.git("add", ".")
            for remote, url in requested.items():
                if url:
                    self.git("remote", "add", remote, url)
                else:
                    _warn("Unable to create remote", remote)
                    remotes.remove(remote)
            return remotes

        if self.remotes is None:
            return self.git("remote")

        existing = [i.split()[:2] for i in self.git("remote", "-v")]
        existing = {k: v for k, v in existing}

        for remote, url in requested.items():
            existing_url = existing.get(remote)
            if url is None:
                if existing_url is None:
                    _warn("No remote named", remote)
                    remotes.remove(remote)

            elif existing_url != url:
                _warn("Changing remote from", existing_url, "to", url)
                self.git("remote", "set-url", remote, url)

        return remotes

    def _commit(self):
        remotes = self._initialize()
        lines = self.git("status", "--porcelain")
        if not self.add_unknown_files:
            lines = [i for i in lines if not i.startwith("??")]

        if lines:
            files = [i.split(maxsplit=1)[1] for i in lines]
            self.git("add", *files)

            if "%" in self.commit_message:
                msg = datetime.datetime.now().strftime(self.commit_message)
            else:
                msg = self.commit_message
            self.git("commit", "-am", msg)
            for remote in remotes:
                self.git("push", remote)

    __dataclass_docs__ = """
source: >-
    source directory to be backed up (default is current directory)

remotes: >-
  A dictionary mapping remote names to remote URLs

git_init: >-
  If `source` is not a Git repository, then if `git_init` is
  True, then `git init` will be called, otherwise ValueError is raised

add_unknown_files: >-
  If True, unknown files are automatically `git add`'ed

file_event_window: >-
  If `file_event_window` is non-zero, then all file events during that
  time window (in seconds) are consolidated into a single git commit

commit_message: >-
  A strftime-style format string for commit messages
"""


def _warn(*args, **kwds):
    print("WARNING:", *args, **kwds, file=sys.stderr)


_ERROR_NO_GIT_DIR = "Not a git directory and `git_init` is not set: %s"
