import subprocess
import threading
import time
from watchdog.observers import Observer
from pathlib import Path
from queue import Queue, Empty
import os


def run_git(execute):
    queue = Queue()
    source = Path(os.path.expandvars('.')).expanduser().resolve()

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
                time.sleep(0.05)
                items_in_queue()

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

    def start(self, sleep=1):
        """Start scheduling and observing, if necessary"""
        if self._observer:
            self._observer.start()


def main(args=None):
    execute = Execute()
    run_git(execute)
    execute.start()


if __name__ == '__main__':
    main()
