from pathlib import Path


def run(execute, name, target=None, source=None,
        every='day@3:32',
        exclude_files=('.git',),
        flags='--archive -v',
        create_if_missing=True):
    """Schedule rsync tasks.

    source:
        The directory to back up - default is the current working directory

    target:
        The root directory for rsync backups

    every, at:
        When to schedule this rsync

    exclude_files:
        A list of files or directories to exclude.

    flags:
        Command line flags to rsync

    create_if_missing:
        If True, immediately create an rsync backup if there is none,
        otherwise wait until the scheduled time for the first backup

    """
    if isinstance(flags, str):
        flags = flags.split()
    elif not isinstance(flags, list):
        flags = list(flags)

    ex = [exclude_files] if isinstance(exclude_files, str) else exclude_files
    flags.extend('--exclude=' + e for e in ex or [])

    rsync_dir = Path(target) / name

    def rsync():
        return execute.run('rsync', *flags, source, rsync_dir)

    if create_if_missing and not rsync_dir.exists():
        rsync()

    execute.schedule(rsync, every)
