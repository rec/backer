from . import patch
from gitz.git import GIT, repo


@patch.execute_keep_run
class TestMain(patch.MainTester):
    @repo.test
    def test_git(self):
        with self.main('-c', 'git:') as execute:
            repo.write_files('a', 'b', 'c')

            observer, = execute.observed
            observer(None)
            patch.wait()
            files = GIT.diff_tree(
                '--no-commit-id', '--name-only', '-r', 'HEAD'
            )
            assert set(files) == set('abc')
