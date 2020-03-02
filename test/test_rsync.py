from . import patch
from pathlib import Path
from tempfile import TemporaryDirectory


@patch.execute_keep_run
class TestRsync(patch.MainTester):
    def test_rsync(self):
        with TemporaryDirectory() as source, TemporaryDirectory() as target:
            ps = Path(source)
            pt = Path(target) / '0' / ps.name

            (ps / 'one').write_text('test_one')

            with self.main(target, source, '-c', 'rsync:') as ex:
                assert (pt / 'one').read_text() == 'test_one'

                (ps / 'two').write_text('test_two')

                (callback, ) = ex.scheduled
                callback()
                patch.wait()

                assert (pt / 'two').read_text() == 'test_two'
