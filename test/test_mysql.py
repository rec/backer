from . import patch


@patch.execute
class TestMySql(patch.MainTester):
    def test_all(self):
        config = {'mysql': {'0': DATABASE}}
        actual, expected = self._test(config, MYSQL, '--all-databases')
        assert actual == expected

    def test_databases(self):
        config = {'mysql': {'0': dict(DATABASE, databases='foo bar')}}
        actual, expected = self._test(
            config, MYSQL, '--databases', 'foo', 'bar')
        assert actual == expected

    def test_database_and_tables(self):
        sub = dict(DATABASE, databases='foo', tables=('bing', 'bang'))
        config = {'mysql': {'0': sub}}
        actual, expected = self._test(config, MYSQL, 'foo', 'bing', 'bang')
        assert actual == expected


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
