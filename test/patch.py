from backer.__main__ import main
from backer import execute
from unittest import mock
import time
import unittest


class FakeExecuteKeepRun(execute.Execute):
    def __init__(self):
        super().__init__()
        self.scheduled = []
        self.observed = []

    def observe(self, observer, path):
        self.observed.append(observer)

    def schedule(self, callback, every, at=None):
        self.scheduled.append(callback)


class FakeExecute(FakeExecuteKeepRun):
    def __init__(self):
        super().__init__()
        self.runs = []

    def run(self, *cmd, out=None, err=None, **kwds):
        self.runs.append((cmd, out, err, kwds))
        return []


class MainTester(unittest.TestCase):
    def setUp(self):
        self.result = []

    def main(self, *args):
        return main(args, self.result.append)


def wait():
    # Wait for a queue in another thread to pick up events
    time.sleep(0.1)


_EXECUTE = 'backer.__main__.Execute'
execute_keep_run = mock.patch(_EXECUTE, FakeExecuteKeepRun)
execute = mock.patch(_EXECUTE, FakeExecute)
