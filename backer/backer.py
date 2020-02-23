import schedule as _schedule
import subprocess
import time
import watchdog


def execute(*args):
    print('$', *args)
    result = subprocess.check_output(args, encoding='utf-8')
    print(result)
    return [i.rstrip() for i in result.splitlines()]


def observe(path, callback, sleep=1):
    """Call `callback` if any file recursively within `path` changes"""
    class Handler:
        @staticmethoid
        def dispatch(event):
            if not event.is_directory:
                callback(event)

    o = watchdog.Observer()
    o.schedule(Handler(path), path, recursive=True)
    o.start()

    try:
        while True:
            time.sleep(sleep)
    except KeyboardInterrupt:
        o.stop()
    o.join()


def schedule(func, every, at=None):
    """Schedule a function"""

    if '@' in every:
        if at:
            raise ValueError('Cannot use @ and at: at the same time')
        every, at = every.split('@')

    scheduler = getattr(_schedule.every(), every)
    if at:
        # Rewrite 4:32 to 04:32
        if len(at.split(':')[0]) < 2:
            scheduler = scheduler.at('0' + at)

    return scheduler.at(at).do(func)
