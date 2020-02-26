from backer.__main__ import main
from backer import execute
import unittest

CLASSES = '__main__', 'git', 'rsync', 'database'
PATCHES = ['backer.%s.execute' % c for c in CLASSES]


class TestMockMain(unittest.TestCase):
    def setUp(self):
        self.execute = execute.Execute()
        self.result = []

    def test_git(self):
        main(('-c', 'git:'))
