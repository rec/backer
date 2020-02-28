from backer import variables
import unittest


class VariablesTest(unittest.TestCase):
    def test_simple(self):
        assert variables.replace('${foo}', {'foo': 'bar'}) == 'bar'

        assert variables.replace('') == ''
        assert variables.replace('', {'foo': 'bar'}) == ''
        assert variables.replace('{foo}', {'foo': 'bar'}) == 'bar'
        with self.assertRaises(KeyError):
            variables.replace('{foo}')

        assert variables.replace('$foo', {'foo': 'bar'}) == 'bar'
        assert variables.replace('${foo}', {'foo': 'bar'}) == 'bar'
        assert variables.replace('${foo}') == ''

    def test_complex(self):
        assert variables.replace('${foo:-default}') == 'default'
        assert variables.replace('${foo:-default}', {'foo': ''}) == 'default'
        assert variables.replace('${foo-default}') == 'default'
        assert variables.replace('${foo-default}', {'foo': ''}) == ''

        with self.assertRaises(KeyError) as e:
            variables.replace('${foo:?error message}')

        assert 'error message' in str(e.exception)
        with self.assertRaises(KeyError):
            variables.replace('${foo:?error message}', {'foo': ''})
        with self.assertRaises(KeyError):
            variables.replace('${foo?error message}')
        variables.replace('${foo?error message}', {'foo': ''})
