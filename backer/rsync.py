from . import execute
from pathlib import Path


def run(name, source=None, target=None,
        every='day',
        at='3:32',
        exclude=('.git',),
        flags='--archive -v',
        create=True):
    """Schedule rsync tasks.

    source:
        The directory to be backed up

    target:
        The root directory for rsync backups:

    every, at:
        When to schedule this rsync

    exclude (default '.git'):
        A list of files or directories to exclude.

    flags:
         command line flags to rsync (default '--archive', '-v')

    """
    if isinstance(flags, str):
        flags = flags.split()
    elif not isinstance(flags, list):
        flags = list(flags)

    if isinstance(exclude, str):
        exclude = [exclude]
    flags.extend('--exclude=' + e for e in exclude or [])

    rsync_dir = Path(target) / name

    def rsync():
        return execute.run('rsync', *flags, source, rsync_dir)

    if create and not rsync_dir.exists():
        rsync()

    execute.run(rsync, every, at)


DEFAULT = {
    'create': True,
    'every': 'day',
    'exclude': ('.git',),
    'at': '3:32',
    'flags': '--archive -v',
}
