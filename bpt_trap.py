from pathlib import Path
from watchdog.observers import Observer


def main():
    class Handler:
        @staticmethod
        def dispatch(event):
            print(event)

    observer = Observer()
    observer.schedule(Handler(), Path('.'), recursive=True)
    observer.start()


if __name__ == '__main__':
    main()
