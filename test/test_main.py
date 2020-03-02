from . import patch
import yaml


@patch.execute
class TestMain(patch.MainTester):
    def test_dry_run(self):
        self.main('-d', '-cgit:')
        assert yaml.safe_load(self.result[0]) == DRY_RUN


DRY_RUN = {
    'git': {
        '0': {
            'add_unknown_files': True,
            'create': True,
            'commit_message': '%Y-%m-%dT%H:%M%SZ',
            'remotes': None,
            'source': None,
            'target': None,
            'file_event_window': 0.05,
        },
    },
    'source': None,
    'target': None,
}
