from .execute import execute
from .scheduler import schedule
from pathlib import Path


def rsync(source, target, tasks):
    def schedule_once(name, every, at, exclude, flags, create):
        if isinstance(flags, str):
            flags = flags.split()
        elif not isinstance(flags, list):
            flags = list(flags)

        if isinstance(exclude, str):
            exclude = [exclude]
        flags.extend('--exclude=' + e for e in exclude or [])

        rsync_dir = Path(target) / name

        def rsync():
            return execute('rsync', *flags, source, rsync_dir)

        if create and not rsync_dir.exists():
            rsync()

       schedule(every, at, rsync)

    for name, desc in tasks.items():
        schedule_once(name, **desc)
