from unittest import TestCase, mock
from backer.__main__ import main
import yaml

CLASSES = '__main__', 'git', 'rsync', 'database'
PATCHES = ['backer.%s.execute' % c for c in CLASSES]


@mock.patch('backer.execute.run', autospec=True)
@mock.patch('backer.execute.observe', autospec=True)
@mock.patch('backer.execute.schedule', autospec=True)
@mock.patch('backer.execute.start', autospec=True)
class TestMain(TestCase):
    def test_dry_run(self, start, schedule, observe, run):
        result = []
        main(['-d', '-c', 'git:'], print=result.append)
        assert yaml.safe_load(result[0]) == DRY_RUN
        assert start.method_calls == []
        assert schedule.method_calls == []
        assert run.method_calls == []
        assert observe.method_calls == []

    def test_git(self, start, schedule, observe, run):
        result = []
        main(['-c', 'git:'], print=result.append)
        assert result == []

        start.assert_called_once_with()
        schedule.assert_not_called()
        run.assert_not_called()
        observe.assert_called_once()
        # observe.assert_called_once_with('.')


DRY_RUN = yaml.safe_load("""
git:
  '0':
    all: true
    init: true
    message: '%Y-%m-%dT%H:%M%SZ'
    remotes: null
    sleep: 1
    source: null
    target: null
    window: 0.05
source: null
target: null""")
