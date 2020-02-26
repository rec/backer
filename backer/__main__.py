from . import git
from .execute import Execute


def main(args=None):
    cfg = {
        'target': None,
        'source': None,
        'remotes': None,
        'git_init': True,
        'add_unknown_files': True,
        'file_event_window': 0.05,
        'commit_message': '%Y-%m-%dT%H:%M%SZ',
    }
    execute = Execute()
    git.run(execute, 'one', **cfg)
    execute.start()


if __name__ == '__main__':
    main()
