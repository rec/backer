from unittest import TestCase
from backer import config


class TestConfig(TestCase):
    def test_simple(self):
        actual = config._combine_sections(['git:'])
        expected = {
            'git': {
                '0': {
                    'source': None,
                    'target': None,
                    'remotes': None,
                    'all': True,
                    'init': True,
                    'message': '%Y-%m-%dT%H:%M%SZ',
                    'sleep': 1,
                    'window': 0.05}}}
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
        cfg = 'rsync: {hourly: {every: hour}}'
        cfg = config.config(['foo', '-c', cfg])

        expected = {
            'target': 'foo',
            'source': None,
            'dry_run': None,
            'rsync': {
                'hourly': {
                    'at': '3:32',
                    'create': True,
                    'every': 'hour',
                    'exclude': ('.git',),
                    'flags': '--archive -v',
                    'source': None,
                    'target': None}}}

        assert cfg == expected
