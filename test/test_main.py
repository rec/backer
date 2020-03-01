from backer import execute
from backer.__main__ import main
from gitz.git import GIT, repo
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock
import time
import unittest
import yaml


class FakeExecute(execute.Execute):
    def __init__(self):
        super().__init__()
        self.scheduled = []
        self.observed = []

    def observe(self, observer, path):
        self.observed.append(observer)

    def schedule(self, callback, every, at=None):
        self.scheduled.append(callback)


def wait():
    # Wait for a queue in another thread to pick up events
    time.sleep(0.1)


class TestMockMain(unittest.TestCase):
    def setUp(self):
        self.result = []

    def main(self, *args, **kwds):
        return main(args, self.result.append, **kwds)

    def test_dry_run(self):
        self.main('-d', '-cgit:')
        assert yaml.safe_load(self.result[0]) == DRY_RUN

    @mock.patch('backer.__main__.Execute', FakeExecute)
    @repo.test
    def test_git(self):
        with self.main('-c', 'git:') as execute:
            repo.write_files('a', 'b', 'c')

            observer, = execute.observed
            observer(None)
            wait()
            files = GIT.diff_tree(
                '--no-commit-id', '--name-only', '-r', 'HEAD')
            assert set(files) == set('abc')

    @mock.patch('backer.__main__.Execute', FakeExecute)
    def test_rsync(self):
        with TemporaryDirectory() as source, TemporaryDirectory() as target:
            ps = Path(source)
            pt = Path(target) / '0' / ps.name
            (ps / 'one').write_text('one')

            with self.main(target, source, '-crsync:') as ex:
                assert pt.exists()
                assert (pt / 'one').exists()
                assert (pt / 'one').read_text() == 'one'

                (ps / 'two').write_text('two')
                callback, = ex.scheduled

                callback()
                wait()
                assert (pt / 'two').exists()
                assert (pt / 'two').read_text() == 'two'


DRY_RUN = yaml.safe_load("""
git:
  '0':
    add_unknown_files: true
    create: true
    commit_message: '%Y-%m-%dT%H:%M%SZ'
    remotes: null
    source: null
    target: null
    file_event_window: 0.05
source: null
target: null""")
