from . import git
import schedule as _schedule
import subprocess
import threading
import time
from watchdog.observers import Observer


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
    git.run(execute, 'one', **cfg)
    execute.start()


if __name__ == '__main__':
    main()
