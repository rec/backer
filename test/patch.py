from backer import execute
from backer.__main__ import Main
from tempfile import TemporaryDirectory
from unittest import mock
import time
import unittest
import yaml


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
        main = Main(args)
        if main.dry_run:
            self.result.append(yaml.safe_dump(main.cfg))
            return

        main_thread = main.new_thread()
        with main_thread:
            return main_thread.execute

    def _test(self, config, expected, *args):
        cfg = yaml.safe_dump(config)
        with TemporaryDirectory() as td:
            with self.main(td, '-c', cfg) as ex:
                ((cmd, *_),) = ex.runs
                expected = ' '.join((expected.format(tmpdir=td), *args))
                actual = ' '.join(cmd)
                return actual, expected


def wait():
    # Wait for a queue in another thread to pick up events
    time.sleep(0.1)


_EXECUTE = 'backer.__main__.Execute'
execute_keep_run = mock.patch(_EXECUTE, FakeExecuteKeepRun)
execute = mock.patch(_EXECUTE, FakeExecute)
