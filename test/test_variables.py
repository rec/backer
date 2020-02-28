from backer import variables
import unittest


class ApplyTest(unittest.TestCase):
    def test_simple(self):
        assert variables.apply('${foo}', foo='bar') == 'bar'

        assert variables.apply('') == ''
        assert variables.apply('', foo='bar') == ''
        assert variables.apply('{foo}', foo='bar') == 'bar'
        with self.assertRaises(KeyError):
            variables.apply('{foo}')

        assert variables.apply('$foo', foo='bar') == 'bar'
        assert variables.apply('${foo}', foo='bar') == 'bar'
        assert variables.apply('${foo}') == ''

    def test_complex(self):
        assert variables.apply('${foo:-default}') == 'default'
        assert variables.apply('${foo:-default}', foo='') == 'default'
        assert variables.apply('${foo-default}') == 'default'
        assert variables.apply('${foo-default}', foo='') == ''

        with self.assertRaises(KeyError) as e:
            variables.apply('${foo:?error message}')

        assert 'error message' in str(e.exception)
        with self.assertRaises(KeyError):
            variables.apply('${foo:?error message}', foo='')
        with self.assertRaises(KeyError):
            variables.apply('${foo?error message}')
        variables.apply('${foo?error message}', foo='')
