import unittest
from backer.task import _describe


class TestDescribe(unittest.TestCase):
    def test_all(self):
        actual = []
        _describe.describe_all(print=lambda *a: actual.append(a))
        joined = [' '.join(a) for a in actual]
        assert len(joined) > 20  # Lame but the full file is too complex
