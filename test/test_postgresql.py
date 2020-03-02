from . import patch


@patch.execute
class TestPostgresql(patch.MainTester):
    def test_all(self):
        config = {'postgresql': {'0': DATABASE}}
        line = 'pg_dumpall' + POSTGRESQL
        actual, expected = self._test(config, line)
        assert actual == expected

    def test_database_and_tables(self):
        sub = dict(DATABASE, databases='foo', tables=('bing', 'bang'))
        config = {'postgresql': {'0': sub}}
        line = 'pg_dump foo' + POSTGRESQL
        actual, expected = self._test(
            config, line, '--table=bing', '--table=bang')
        assert actual == expected


DATABASE = {
    'user': 'test_user',
    'password': 'test_password',
    'host': 'test_host',
    'port': 7777,
}

POSTGRESQL = """\
 --file={tmpdir}/0/postgresql.sql\
 --user=test_user\
 --password=test_password\
 --port=7777\
 --host=test_host\
"""
