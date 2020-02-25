import schedule as _schedule
import subprocess
import threading
import time
import watchdog

_OBSERVER = None
_SCHEDULE = None


def run(*args, **kwds):
    print('$', *args)
    result = subprocess.check_output(args, encoding='utf-8', **kwds)
    print(result)
    return [i.rstrip() for i in result.splitlines()]


def observe(path, callback):
    """Call `callback` if any file recursively within `path` changes"""
    global _OBSERVER
    _OBSERVER = _OBSERVER or watchdog.Observer()

    class Handler:
        @staticmethod
        def dispatch(event):
            if not event.is_directory:
                callback(event)

    _OBSERVER.schedule(Handler(path), path, recursive=True)


def schedule(func, every, at=None):
    """Schedule a function"""
    global _SCHEDULE
    _SCHEDULE = _SCHEDULE or _schedule.Schedule()

    if '@' in every:
        if at:
            raise ValueError('Cannot use @ and at: at the same time')
        every, at = every.split('@')

    scheduler = getattr(_SCHEDULE.every(), every)
    if at:
        # Rewrite 4:32 to 04:32
        if len(at.split(':')[0]) < 2:
            scheduler = scheduler.at('0' + at)

    scheduler.at(at).do(func)


def start(sleep=1):
    """Start scheduling and observing, if necessary"""
    if _OBSERVER:
        _OBSERVER.start()

    if _SCHEDULE:
        def loop():
            while True:
                _SCHEDULE.run_pending()
                time.sleep(sleep)

        threading.Thread(target=loop, daemon=True).start()
