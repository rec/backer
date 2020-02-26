from . import tasks
from .execute import Execute


def main(args=None):
    cfg = {
        'git': {
            '0': {
                'target': None,
                'source': None,
                'remotes': None,
                'git_init': True,
                'add_unknown_files': True,
                'file_event_window': 0.05,
                'commit_message': '%Y-%m-%dT%H:%M%SZ',
            }
        }
    }
    execute = Execute()

    for task_name, section in cfg.items():
        task = tasks.TASKS[task_name]
        for name, desc in section.items():
            task.run(execute, name, **desc)

    execute.start()


if __name__ == '__main__':
    main()
