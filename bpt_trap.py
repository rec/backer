import threading
import time
from watchdog.observers import Observer
from pathlib import Path
from queue import Queue, Empty
import os


def main():
    observer = Observer()
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

    class Handler:
        @staticmethod
        def dispatch(event):
            if not event.is_directory:
                queue.event(event)

    observer.schedule(Handler(), source, recursive=True)
    observer.start()


if __name__ == '__main__':
    main()
