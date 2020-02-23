from . import backer
from pathlib import Path


def rsync(source, target, tasks):
    """Schedule rsync tasks.

    source:
        The directory to be backed up

    target:
        The root directory for rsync backups:

    tasks:
        A dictionary that maps the name of the backup directory
        to the *task* - the description of how often and how rsync is called.

        Tasks may have the following fields:
           every, at (optional):
             when to schedule this rsync

           exclude (default '.git'):
             a list of files or directories to exclude.

           flags:
             command line flags to rsync (default '--archive', '-v')

    """

    def schedule_one(name, every, at, exclude, flags, create):
        if isinstance(flags, str):
            flags = flags.split()
        elif not isinstance(flags, list):
            flags = list(flags)

        if isinstance(exclude, str):
            exclude = [exclude]
        flags.extend('--exclude=' + e for e in exclude or [])

        rsync_dir = Path(target) / name

        def rsync():
            return backer.execute('rsync', *flags, source, rsync_dir)

        if create and not rsync_dir.exists():
            rsync()

       backer.schedule(rsync, every, at)

    for name, desc in tasks.items():
        schedule_one(name, **desc)
