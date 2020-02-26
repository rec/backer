import schedule as _schedule
import subprocess
import threading
import time
from watchdog.observers import Observer
from pathlib import Path
from queue import Queue, Empty
import os


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
                pass

    threading.Thread(target=service_queue, daemon=True).start()
    execute.observe(queue.put, source.absolute())


class Execute:
    _observer = _schedule = None

    def run(self, *args, **kwds):
        print('$', *args)
        result = subprocess.check_output(args, encoding='utf-8', **kwds)
        print(result)
        return [i.rstrip() for i in result.splitlines()]

    def observe(self, callback, path):
        """Call `callback` if any file recursively within `path` changes"""
        self._observer = self._observer or Observer()

        class Handler:
            @staticmethod
            def dispatch(event):
                if not event.is_directory:
                    callback(event)

        self._observer.schedule(Handler(), path, recursive=True)

    def schedule(self, callback, every, at=None):
        """Schedule a function"""
        self._schedule = self._schedule or _schedule.Schedule()

        if '@' in every:
            if at:
                raise ValueError('Cannot use @ and at: at the same time')
            every, at = every.split('@')

        scheduler = getattr(self._schedule.every(), every)
        if at:
            # Rewrite 4:32 to 04:32
            if len(at.split(':')[0]) < 2:
                scheduler = scheduler.at('0' + at)

        scheduler.at(at).do(callback)

    def start(self, sleep=1):
        """Start scheduling and observing, if necessary"""
        if self._observer:
            self._observer.start()

        if self._schedule:
            def loop():
                while True:
                    self._schedule.run_pending()
                    time.sleep(sleep)

            threading.Thread(target=loop, daemon=True).start()


def main(args=None):
    cfg = {
        'target': None,
        'source': None,
        'remotes': None,
        'git_init': True,
        'add_unknown_files': True,
        'file_event_window': 0.05,
        'commit_message': '%Y-%m-%dT%H:%M%SZ',
    }
    execute = Execute()
    run(execute, 'one', **cfg)
    execute.start()


if __name__ == '__main__':
    main()
