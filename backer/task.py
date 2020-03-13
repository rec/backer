from dataclasses import dataclass
from pathlib import Path
import shlex


@dataclass
class Task:
    """
    create_at_startup:
        If True, immediately create a backup if there is none,
        otherwise wait until the scheduled time for the first backup
    """
    execute: object = None
    name: str = ''
    create_at_startup: bool = True

    def start(self):
        raise NotImplementedError

    @staticmethod
    def split(s):
        return shlex.split(s) if isinstance(s, str) else s or []


@dataclass
class ScheduledCommandTask(Task):
    COMMAND = '(none)'
    DEFAULT_EVERY = ''

    target: Path = None
    every: str = ''
    flags: str = ''

    def __post_init__(self):
        self.target = Path(self.target)
        self.task_dir = self.target / self.name
        self.every = self.every or self.DEFAULT_EVERY

    def build_command_line(self):
        self.add(*self.split(self.flags))

    def start(self):
        self.command_line = [self.COMMAND]
        self.build_command_line()
        if not self.task_dir.exists():
            self.task_dir.mkdir(parents=True)
            if self.create_at_startup:
                self.run()

        self.execute.schedule(self.run, self.every)

    def run(self):
        return self.execute.run(*self.command_line)

    def add(self, *args, **kwds):
        self.command_line.extend(args)

        for flag, value in kwds.items():
            if value is not None:
                flag = flag.replace('_', '-')
                flag = ('-' if len(flag) == 1 else '--') + flag
                if value is not True:
                    flag = '%s=%s' % (flag, value)
                self.add(flag)


class DatabaseTask(ScheduledCommandTask):
    SUFFIX = '.sql'
    TEMP_SUFFIX = '.tmp'

    def __init__(
        self,
        execute,
        name,
        target=None,
        create_at_startup=True,
        every='day',
        flags='',
        user=None,
        password=None,
        port=None,
        host=None,
        databases=None,
        tables=None,
        filename=None,
    ):
        super().__init__(
            execute, name, create_at_startup, target, every, flags
        )
        self.db_flags = {
            'user': user,
            'password': password,
            'port': port,
            'host': host,
        }
        self.databases = self.split(databases)
        self.tables = self.split(tables)

        if self.tables and len(self.databases) != 1:
            raise ValueError('Exactly one database if there are tables')

        filename = filename or (self.__class__.__name__.lower() + self.SUFFIX)
        self.filename = self.task_dir / filename
        self.out_filename = self.task_dir / (filename + self.TEMP_SUFFIX)

    def build_command_line(self):
        self.add(**self.db_flags)
        super().build_command_line()

    def run(self):
        super().run()
        if self.out_filename.exists():
            self.out_filename.rename(self.filename)
