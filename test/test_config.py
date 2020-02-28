from backer import config
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase


class TestConfig(TestCase):
    def test_simple(self):
        actual = config._combine_sections(['git:'])
        expected = {
            'git': {
                '0': {
                    'source': None,
                    'target': None,
                    'remotes': None,
                    'add_unknown_files': True,
                    'git_init': True,
                    'commit_message': '%Y-%m-%dT%H:%M%SZ',
                    'file_event_window': 0.05}}}
        assert expected == actual

    def test_all(self):
        actual = config._combine_sections(['git:\nrsync:\ndatabase:'])
        expected = {k: {'0': v} for k, v in config.DEFAULTS.items()}
        assert expected == actual

        # Make sure they aren't the same
        actual['git'] = {}
        assert config.DEFAULTS != actual

    def test_parts(self):
        actual = config._combine_sections(['git:', 'rsync:', 'database:'])
        expected = {k: {'0': v} for k, v in config.DEFAULTS.items()}
        assert expected == actual

    def test_config(self):
        cfg = 'rsync: {hourly: {every: hour@3:32}}'
        cfg = config.config(['foo', '-c', cfg])
        assert cfg == EXPECTED

    def test_variable_substitution(self):
        with TemporaryDirectory() as source:
            fname = Path(source) / '.env'
            fname.write_text('name = hourly\n# comment\nevery=hour@3:32')
            cfg = 'rsync: {"${name}": {every: "{every}"}}'
            cfg = config.config(['foo', '-c', cfg, '--env-file', str(fname)])
            assert cfg == EXPECTED


EXPECTED = {
    'target': 'foo',
    'source': None,
    'dry_run': False,
    'rsync': {
        'hourly': {
            'create_if_missing': True,
            'every': 'hour@3:32',
            'exclude_files': ('.git',),
            'flags': '--archive -v',
            'source': None,
            'target': None}}}
