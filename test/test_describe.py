from backer_doc import __main__
import functools
import io
import unittest


class TestDescribe(unittest.TestCase):
    def DONT_test_all(self):
        sio = io.StringIO()
        _print = functools.partial(print, file=sio)
        __main__.write_docs(print=_print)
        value = sio.getvalue()
        print(value)
        assert len(value) > 20
