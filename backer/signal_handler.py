import signal

SIGNAL_NUMBERS = {
    k: v for k, v in signal.__dict__.items() if k.startswith("SIG") and "_" not in k
}

SIGNAL_NAMES = {v: k for k, v in SIGNAL_NUMBERS.items()}

STOPS = "SIGINT", "SIGTERM"
RESTARTS = ("SIGHUP",)


def run(runner, stopper, stops=STOPS, restarts=RESTARTS, print=print):
    handlers = {s: stopper for s in stops + restarts}
    signals = {}

    def handler(signum, frame):
        signame = SIGNAL_NAMES[signum]
        signals[signame] = True
        handler = handlers[signame]
        handler()

    def set_all(handler):
        for signame in handlers:
            if signame in SIGNAL_NUMBERS:  # Windows doesn't have all signals
                signal.signal(SIGNAL_NUMBERS[signame], handler)

    set_all(handler)

    try:
        while True:
            runner()
            if not signals:
                return

            running = all(s in restarts for s in signals)
            msg = "restarting" if running else "stopping"
            print("Received signal {}: {}".format(" ".join(signals), msg))
            signals.clear()
            if not running:
                return

    finally:
        set_all(signal.SIG_DFL)


if __name__ == "__main__":
    import itertools
    import time

    running = [0]

    def runner():
        running[:] = [0]
        for i in itertools.count():
            if not running:
                return
            print(i)
            time.sleep(2)

    run(runner, running.clear)
