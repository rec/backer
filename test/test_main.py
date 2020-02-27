from backer.__main__ import main
from backer import execute
from gitz.git import GIT, repo
from unittest import mock
import time
import unittest
import yaml

CLASSES = '__main__', 'git', 'rsync', 'database'
PATCHES = ['backer.%s.execute' % c for c in CLASSES]


class FakeExecute(execute.Execute):
    def __init__(self):
        super().__init__()
        FakeExecute.schedule = []

    def observe(self, observer, path):
        FakeExecute.observer = observer

    def schedule(self, callback, every, at=None):
        FakeExecute.schedule.append((callback, every, at))


def pause():
    time.sleep(0.1)


class TestMockMain(unittest.TestCase):
    def setUp(self):
        self.result = []

    def main(self, *args, **kwds):
        return main(args, self.result.append, **kwds)

    def test_dry_run(self):
        self.main('-d', '-c', 'git:')
        assert yaml.safe_load(self.result[0]) == DRY_RUN

    @mock.patch('backer.__main__.Execute', FakeExecute)
    @repo.test
    def test_git(self):
        with self.main('-c', 'git:'):
            repo.write_files('a', 'b', 'c')
            FakeExecute.observer(None)
            pause()
            files = GIT.diff_tree(
                '--no-commit-id', '--name-only', '-r', 'HEAD')
            assert set(files) == set('abc')


DRY_RUN = yaml.safe_load("""
git:
  '0':
    add_unknown_files: true
    git_init: true
    commit_message: '%Y-%m-%dT%H:%M%SZ'
    remotes: null
    source: null
    target: null
    file_event_window: 0.05
source: null
target: null""")
