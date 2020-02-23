from unittest import TestCase
from backer import configure
from io import StringIO


def get_configuration(*strings):
    return configure.get_configuration([StringIO(s) for s in strings])


class TestConfigure(TestCase):
    def test_simple(self):
        actual = get_configuration('git:')
        expected = {
            'git': {
                '0': {
                    'all': True,
                    'init': True,
                    'message': '%Y-%m-%dT%H:%M%SZ',
                    'sleep': 1,
                    'window': 0.05}}}
        assert expected == actual

    def test_all(self):
        actual = get_configuration('git:\nrsync:\ndatabase:')
        expected = {k: {'0': v} for k, v in configure.DEFAULTS.items()}
        assert expected == actual

        # Make sure they aren't the same
        actual['git'] = {}
        assert configure.DEFAULTS != actual
