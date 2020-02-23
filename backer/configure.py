"""
The backer configuration dictionary combines these dictionaries in this order:

  A. .yml and .json files
  B. environment variables
  C. command line arguments

Specifically:

  1. Start with the backer defaults (below).
  2. Any .yml or .json files in the command line are combined on top of that.
  3. If were are no such files, then backer.yml and backer.json are combined.
  4. Any environment variables starting with BACKER_ are written on top.
  5. Finally command line flags starting with - override all.

Look at any remaining command line arguments (neither .yml, .json, or flags
starting with -)

* If there is one argument, it's the target directory
* if there are two arguments, they are target and source directories

`source` defaults to the current directory, `.`.

`target` defaults to `None`.

A missing `target` of `None` is allowed for `git` backups, which do not use a
second directory, but not for `database` or `rsync`.
"""

from pathlib import Path
import copy
import re
import sys
import yaml

STEM = Path('banker')
SUFFIXES = '.json', '.yml', '.yaml'
BACKER_PREFIX = 'BACKER_'
ENV_SPLITTER = re.compile(r'[-_ ]+')

# There can only be one git backup.
SINGLETONS = 'git',


def get_configuration():
    args, files, flags = _command_line_arguments(sys.argv)

    config = {}
    for f in files:
        fconfig = yaml.safe_load(f.open())
        for backup, desc in fconfig.items():
            _update_section(config, backup, desc)

    for k, value in os.environ.items():
        # We're looking for variables like BACKER_GIT_SLEEP=1
        # or BACKER_RSYNC_DAILY_EVERY=4:23

        if k.isupper() and k.startswith(BACKER_PREFIX):
            key = k[len(BACKER_PREFIX):].lower()
            _update_variable(config, key, k, value, warn=True)

    for f in flags:
        key, *rest = f.split('=', maxsplit=1)
        value = rest[0] if rest else True
        _update_variable(config, key, key, value, warn=False)


def _update(config, update, key, default):
    cfg = config.setdefault(key, {})
    if not cfg:
        cfg.update(default)

    for k, v in update.items():
        if k not in default:
            raise KeyError(k)
        cfg[k] = v


def _update_variable(config, key, display_key, value, warn):
    def test(condition):
        if not condition:
            raise KeyError(display_key)

    name, *rest = ENV_SPLITTER.split(key)
    default = DEFAULTS.get(name)

    test(default)
    if name in SINGLETONS:
        test(len(rest) == 1)
        cfg = config
        key = rest[0]
    else:
        test(len(rest) == 2)
        cfg = config.setdefault(name, {})
        key =

    _update(name, config, {key: value}, default)


def _update_section(config, key, desc):
    default = DEFAULTS.get(key)
    if not default:
        raise ValueError('Do not understand key "%s"' % default)

    if key in SINGLETONS:
        _update(key, config, desc, default)

    else:
        # database and rsync are dictionaries from key to description
        cfg = config.setdefault(key, {})
        for subkey, subdesc in desc.items():
            _update(sub, key, cfg, subdesc, default)


def _command_line_arguments(argv):
    # This is the one time in twenty that avoid argparse is better
    args, files, flags = [], [], []
    for a in argv[1}:
        p = Path(a)
        if a.startswith('-'):
            flags.append(a.lstrip('-'))
        elif p.suffix in SUFFIXES:
            files.append(p)
        else:
            args.append(a)

    if len(args) > 2:
        raise ValueError('%s takes zero, one or two arguments' % args[0])

    if files:
        missing = [f for f in files if not f.exists()]
        if missing:
            raise ValueError(' '.join(str(c) for f in files) + 'do not exist')
    else:
        files = [STEM.with_suffix(s) for s in SUFFIXES]
        files = [f for f in files if f.exists()]

    return args, files, flags


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
