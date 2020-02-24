from unittest import TestCase
from backer import configure


class TestConfigure(TestCase):
    def test_simple(self):
        actual = configure.combine_sections(['git:'])
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
        actual = configure.combine_sections(['git:\nrsync:\ndatabase:'])
        expected = {k: {'0': v} for k, v in configure.DEFAULTS.items()}
        assert expected == actual

        # Make sure they aren't the same
        actual['git'] = {}
        assert configure.DEFAULTS != actual

    def test_parts(self):
        actual = configure.combine_sections(['git:', 'rsync:', 'database:'])
        expected = {k: {'0': v} for k, v in configure.DEFAULTS.items()}
        assert expected == actual

    def test_parse(self):
        cfg = 'rsync: {hourly: {every: hour}}'
        target, source, config = configure.parse(['foo', '-c', cfg])
        assert target == 'foo'
        assert source is None
        expected = {
            'rsync': {
                'hourly': {
                    'at': '3:32',
                    'create': True,
                    'every': 'hour',
                    'exclude': ('.git',),
                    'flags': '--archive -v',
                    'source': None,
                    'target': None}}}

        assert config == expected
