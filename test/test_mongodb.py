from . import patch


@patch.execute
class TestMongodb(patch.MainTester):
    def test_all(self):
        config = {'mongodb': {'0': DATABASE}}
        actual, expected = self._test(config, MONGODB)
        assert actual == expected

    def test_database_and_tables(self):
        sub = dict(DATABASE, databases='foo', tables='bing')
        config = {'mongodb': {'0': sub}}
        actual, expected = self._test(
            config, MONGODB, '--db=foo', '--collection=bing')
        assert actual == expected


DATABASE = {
    'user': 'test_user',
    'password': 'test_password',
    'host': 'test_host',
    'port': 7777,
}

MONGODB = """\
mongodump\
 --user=test_user\
 --password=test_password\
 --port=7777\
 --host=test_host\
 --archive={tmpdir}/0/mongodb.sql.gz\
 --gzip\
"""
