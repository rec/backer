from . import patch


@patch.execute
class TestMySql(patch.MainTester):
    def test_mysql_all(self):
        config = {'mysql': {'0': DATABASE}}
        self.run_test(config, MYSQL, '--all-databases')

    def test_mysql_databases(self):
        config = {'mysql': {'0': dict(DATABASE, databases='foo bar')}}
        self.run_test(config, MYSQL, '--databases', 'foo', 'bar')

    def test_mysql_database_and_tables(self):
        sub = dict(DATABASE, databases='foo', tables=('bing', 'bang'))
        config = {'mysql': {'0': sub}}
        self.run_test(config, MYSQL, 'foo', 'bing', 'bang')


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
