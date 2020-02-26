from backer.__main__ import main
import unittest


class TestMockMain(unittest.TestCase):
    def test_git(self):
        main(('-c', 'git:'))
