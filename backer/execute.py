from .stoppable_thread import Stoppable, StoppableThreadList
from watchdog import observers
import run_subprocess as rs
import schedule as _schedule
import time


class Execute(StoppableThreadList):
    def __init__(self, sleep=1):
        super().__init__()
        self._observer = self._scheduler = None
        self.sleep = sleep

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
            self.add_thread(self._observer)

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
            self.new_thread(self._scheduler_loop, name='scheduler_loop')

        every, *at = every.split('@', maxsplit=1)
        sched = getattr(self._scheduler.every(), every)

        if at:
            # Rewrite 4:32 to 04:32
            at = at[0]
            if len(at.split(':')[0]) < 2:
                at = '0' + at
            sched = sched.at(at)

        sched.do(callback)

    def _scheduler_loop(self):
        while True:
            self._scheduler.run_pending()
            time.sleep(self.sleep)


class Observer(observers.Observer, Stoppable):
    def __init__(self, *args, name='observer', **kwds):
        Observer.__init__(self, *args, **kwds)
        Stoppable.__init__(self, name)

    def start(self):
        if not self.is_started:
            Stoppable.start(self)
            Observer.start(self)

    def stop(self):
        Stoppable.stop(self)
        Observer.stop(self)
