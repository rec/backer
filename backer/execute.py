from .stoppable_thread import StoppableThreadList
from watchdog.observers import Observer
import run_subprocess as rs
import schedule as _schedule
import time


class Execute:
    def __init__(self, sleep=1):
        self._observer = self._scheduler = None
        self.sleep = sleep
        self.threads = StoppableThreadList()

    def run(self, *cmd, out=None, err=None, **kwds):
        print('$', *cmd)
        result = []

        def output(line):
            result.append(line)
            print(line)

        ec = rs.run(cmd, out or output, err or print, **kwds)
        if ec:
            raise ValueError('Command failed with error ', ec)

        return result

    def observe(self, callback, path):
        """Call `callback` if any file recursively within `path` changes"""
        if not self._observer:
            self._observer = Observer()
            self.threads.add_thread(self._observer)

        class Handler:
            @staticmethod
            def dispatch(event):
                if not event.is_directory:
                    callback(event)

        self._observer.schedule(Handler(), path, recursive=True)

    def schedule(self, callback, every):
        """Schedule a function"""
        if not self._scheduler:
            self._scheduler = _schedule.Scheduler()
            self.threads.new_thread(self._scheduler_loop)

        every, *at = every.split('@', maxsplit=1)
        sched = getattr(self._scheduler.every(), every)

        if at:
            # Rewrite 4:32 to 04:32
            at = at[0]
            if len(at.split(':')[0]) < 2:
                at = '0' + at
            sched = sched.at(at)

        sched.do(callback)

    def __enter__(self):
        self.threads.__enter__()
        return self

    def __exit__(self, type, value, traceback):
        self.threads.__exit__(type, value, traceback)

    def _scheduler_loop(self):
        while True:
            self._scheduler.run_pending()
            time.sleep(self.sleep)
