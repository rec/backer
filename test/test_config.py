from backer import config
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from backer import task
from backer.task._describe import defaults

SECTIONS = ('git', 'mongodb', 'mysql', 'postgresql', 'rsync')
TASKS = {s: task.task_class(s) for s in SECTIONS}
LINE = ':\n'.join(TASKS) + ':'


class TestConfig(TestCase):
    def test_simple(self):
        actual = config._combine(['git:'])
        expected = {
            'git': {
                '0': {
                    'source': None,
                    'target': None,
                    'remotes': None,
                    'add_unknown_files': True,
                    'create_at_startup': True,
                    'git_init': True,
                    'commit_message': '%Y-%m-%dT%H:%M%SZ',
                    'file_event_window': 0.05,
                }
            }
        }
        assert expected == actual

    def test_all(self):
        actual = config._combine([LINE])
        expected = {k: {'0': defaults(v)} for k, v in TASKS.items()}
        assert expected == actual

    def test_parts(self):
        actual = config._combine([LINE])
        expected = {k: {'0': defaults(v)} for k, v in TASKS.items()}
        assert expected == actual

    def test_config(self):
        cfg = 'rsync: {hourly: {every: hour@3:32}}'
        cfg = config.config(['foo', '-c', cfg])
        assert cfg == EXPECTED

    def test_variable_substitution(self):
        with TemporaryDirectory() as source:
            fname = Path(source) / '.env'
            fname.write_text('name = hourly\n# comment\nevery=hour@3:32')
            fname.write_text('# comment\nevery=hour@3:32')
            cfg = 'rsync: {"${name}": {every: "{every}"}}'
            env = ' name = hourly '
            cmd = ['foo', '-c', cfg, '-e', env, '--env-file', str(fname)]
            cfg = config.config(cmd)
            assert cfg == EXPECTED


EXPECTED = {
    'target': 'foo',
    'source': None,
    'dry_run': False,
    'full_help': False,
    'rsync': {
        'hourly': {
            'create_at_startup': True,
            'every': 'hour@3:32',
            'flags': '--archive -v --exclude=.git',
            'source': None,
            'target': None,
        }
    },
}
