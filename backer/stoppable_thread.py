from threading import Event, Thread


class Stoppable:
    def __init__(self):
        self.start_requested = Event()
        self.stop_requested = Event()

    def start(self):
        self.start_requested.set()

    def stop(self):
        self.stop_requested.set()

    @property
    def is_started(self):
        return self.start_requested.is_set()

    @property
    def is_stopped(self):
        return self.stop_requested.is_set()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()
        self.join()


class StoppableThread(Thread, Stoppable):
    def __init__(self, target=None, daemon=True, **kwargs):
        Stoppable.__init__(self)
        Thread.__init__(self, target=target, daemon=daemon, **kwargs)

    def start(self):
        if not self.is_started:
            Stoppable.start(self)
            Thread.start(self)

    def run(self):
        try:
            while not self.is_stopped and self._target:
                self._target(*self._args, **self._kwargs)
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs


class StoppableThreadList(Stoppable):
    def __init__(self):
        super().__init__()
        self.threads = []

    def add_thread(self, thread):
        self.threads.append(thread)
        return thread

    def new_thread(self, *args, **kwds):
        return self.add_thread(StoppableThread(*args, **kwds))

    def start(self):
        super().start()
        for i in self.threads:
            if not i.start_requested.is_set():
                i.start()

    def stop(self):
        super().stop()
        for i in self.threads:
            i.stop()

    def join(self):
        for i in self.threads:
            i.join()

    def is_alive(self):
        return any(i.is_alive() for i in self.threads)
