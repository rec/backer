from pathlib import Path
from watchdog.observers import Observer

WANT_TO_FAIL = True

if WANT_TO_FAIL:
    PATH = Path('.')
else:
    PATH = '.'


def main():
    class Handler:
        @staticmethod
        def dispatch(event):
            print(event)

    observer = Observer()
    observer.schedule(Handler(), PATH, recursive=True)

    observer.start()
    # If PATH is a path, the line above causes:
    # Compilation trace/BPT trap: 5 at Wed Feb 26 17:38:13
    # on Python 3.6.6, Python 3.7.0, Python 3.8.1
    # Darwin bantam.local 16.7.0 Darwin Kernel Version 16.7.0: (etc)

if __name__ == '__main__':
    main()
