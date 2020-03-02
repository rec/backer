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
    ENABLE_RUN = True

    def __init__(self):
        super().__init__()
        self.scheduled = []
        self.observed = []
        self.runs = []

    def run(self, *cmd, out=None, err=None, **kwds):
        self.runs.append((cmd, out, err, kwds))
        if self.ENABLE_RUN:
            return super().run(*cmd, out=out, err=err, **kwds)
        return []

    def observe(self, observer, path):
        self.observed.append(observer)

    def schedule(self, callback, every, at=None):
        self.scheduled.append(callback)


def wait():
    # Wait for a queue in another thread to pick up events
    time.sleep(0.1)


@mock.patch('backer.__main__.Execute', FakeExecute)
class TestMain(unittest.TestCase):
    def setUp(self):
        self.result = []

    def main(self, *args):
        return main(args, self.result.append)

    def test_dry_run(self):
        self.main('-d', '-cgit:')
        assert yaml.safe_load(self.result[0]) == DRY_RUN

    @repo.test
    def test_git(self):
        with self.main('-c', 'git:') as execute:
            repo.write_files('a', 'b', 'c')

            observer, = execute.observed
            observer(None)
            wait()
            files = GIT.diff_tree(
                '--no-commit-id', '--name-only', '-r', 'HEAD'
            )
            assert set(files) == set('abc')

    def test_rsync(self):
        with TemporaryDirectory() as source, TemporaryDirectory() as target:
            ps = Path(source)
            pt = Path(target) / '0' / ps.name

            (ps / 'one').write_text('test_one')

            with self.main(target, source, '-c', 'rsync:') as ex:
                assert (pt / 'one').read_text() == 'test_one'

                (ps / 'two').write_text('test_two')

                (callback, ) = ex.scheduled
                callback()
                wait()

                assert (pt / 'two').read_text() == 'test_two'

    def test_mysql(self):
        with TemporaryDirectory() as target:
            cfg = yaml.safe_dump({'mysql': DATABASE})

            enable_run = 'test.test_main.FakeExecute.ENABLE_RUN'
            with mock.patch(enable_run, False):
                with self.main(target, '-c', cfg) as ex:
                    assert ex is not None
                    ((cmd, *_), ) = ex.runs
                    assert list(cmd) == MYSQL.format(tmpdir=target).split()


DATABASE = {
    '0': {
        'user': 'test_user',
        'password': 'test_password',
        'host': 'test_host',
        'port': 7777,
    }
}

DRY_RUN = yaml.safe_load(
    """
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
target: null"""
)

MYSQL = """\
mysqldump\
 --user=test_user\
 --password=test_password\
 --port=7777\
 --host=test_host\
 --result-file={tmpdir}/0/mysql.sql\
 --all-databases\
"""
