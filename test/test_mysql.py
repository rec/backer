from . import patch


@patch.execute
class TestMySql(patch.MainTester):
    def test_mysql(self):
        config = {'mysql': {'0': DATABASE}}
        self.run_test(config, MYSQL, '--all-databases')


DATABASE = {
    'user': 'test_user',
    'password': 'test_password',
    'host': 'test_host',
    'port': 7777,
}

MYSQL = """\
mysqldump\
 --user=test_user\
 --password=test_password\
 --port=7777\
 --host=test_host\
 --result-file={tmpdir}/0/mysql.sql\
"""
