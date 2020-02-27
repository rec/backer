import schedule as _schedule
import subprocess
import time
from watchdog.observers import Observer
from .stoppable_thread import StoppableThreadList


class Execute:
    def __init__(self, sleep=1):
        self._observer = self._scheduler = None
        self.sleep = sleep
        self.threads = StoppableThreadList()

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
        self._scheduler = self._scheduler or _schedule.Scheduler()

        if '@' in every:
            if at:
                raise ValueError('Cannot use @ and at: at the same time')
            every, at = every.split('@')

        sched = getattr(self._scheduler.every(), every)
        if at:
            # Rewrite 4:32 to 04:32
            if len(at.split(':')[0]) < 2:
                at = '0' + at
            sched = sched.at(at)

        sched.do(callback)

    def start_threads(self, sleep=1):
        """Start scheduling and observing, if necessary"""

        if self._observer:
            self.threads.add_thread(self._observer)

        if self._scheduler:
            def loop():
                while True:
                    self._scheduler.run_pending()
                    time.sleep(sleep)

            self.threads.new_thread(loop)
