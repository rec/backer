from . import patch

from tempfile import TemporaryDirectory
import yaml


@patch.execute
class TestMySql(patch.MainTester):
    def test_mysql(self):
        with TemporaryDirectory() as target:
            cfg = yaml.safe_dump({'mysql': DATABASE})
            with self.main(target, '-c', cfg) as ex:
                assert ex is not None
                ((cmd, *_), ) = ex.runs
                assert list(cmd) == MYSQL.format(tmpdir=target).split()


DATABASE = {
    '0': {
        'user': 'test_user',
        'password': 'test_password',
        'host': 'test_host',
        'port': 7777,
    }
}

MYSQL = """\
mysqldump\
 --user=test_user\
 --password=test_password\
 --port=7777\
 --host=test_host\
 --result-file={tmpdir}/0/mysql.sql\
 --all-databases\
"""
