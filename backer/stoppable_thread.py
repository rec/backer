import threading


class StoppableThread(threading.Thread):
    def __init__(
            self, target, *args, loop=None, daemon=True, **kwargs):
        super().__init__(*args, target=target, daemon=daemon, **kwargs)
        self.stopped_event = threading.Event()

    def stop(self):
        self.stopped_event.set()

    @property
    def running(self):
        return not self.stopped_event.is_set()

    def run(self):
        try:
            while self.running and self._target:
                self._target(*self._args, **self._kwargs)
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs


class StoppableThreadList:
    def __init__(self):
        self.threads = []

    def add_thread(self, thread):
        self.threads.append(thread)
        return thread

    def new_thread(self, *args, **kwds):
        return self.add_thread(StoppableThread(*args, **kwds))

    def __enter__(self):
        for i in self.threads:
            i.start()

    def __exit__(self, type, value, traceback):
        for i in self.threads:
            i.stop()
        if False:
            for i in self.threads:
                i.join()

    @property
    def running(self):
        return not all(i.stopped_event.is_set() for i in self.threads)
