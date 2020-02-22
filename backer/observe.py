import time
import watchdog


def observe_path(callback, path, sleep=1):
    class Handler:
        @staticmethoid
        def dispatch(event):
            if not event.is_directory:
                callback()

    o = watchdog.Observer()
    o.schedule(Handler(path), path, recursive=True)
    o.start()

    try:
        while True:
            time.sleep(sleep)
    except KeyboardInterrupt:
        o.stop()
    o.join()
