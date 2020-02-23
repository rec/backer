"""
The backer configuration combines .yml and .json files together
to return a dictionary.

If file names are provided on the command line, then these are used to configure
the program, otherwise stdin is read
"""

from pathlib import Path
import sys
import yaml


def get_configuration():
    config = {}
    args = sys.argv[1:]

    if args:
        files = [Path(a) for a in args]
        missing = [f for f in files if not f.exists()]
        if missing:
            raise ValueError(' '.join(str(c) for f in missing) + "don't exist")
        streams = [f.open() for f in files]
    else:
        streams = [sys.stdin]

    for fp in streams:
        for section_name, tasks in yaml.safe_load(fp).items():
            default = DEFAULTS.get(section_name)
            if not default:
                raise KeyError(section_name)
            section_config = config.setdefault(section_name, {})
            for task_name, task in tasks.items():
                task_config = section_config.setdefault(task_name, {})
                if not task_config:
                    task_config.update(default)

                for k, v in task.items():
                    if k not in task_config:
                        raise KeyError(k)
                    task_config[k] = v

    return config


DEFAULTS = {
    'git': {
      'init': True,
      'all': True,
      'window': 0.05,
      'message': '%Y-%m-%dT%H:%M%SZ',
      'sleep': 1,
    },

    'database': {
      'every': 'day',
      'at': '4:23',
      'type': 'mysql',
      'tables': None,
      'user': 'user',
      'password': 'password',
    },

    'rsync': {
      'create': True,
      'every': 'day',
      'exclude': ('.git',),
      'at': '3:32',
      'flags': '--archive -v',
    },
}
