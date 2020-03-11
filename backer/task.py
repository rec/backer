from pathlib import Path
import shlex


class Task:
    def __init__(self, execute, name, create_at_startup):
        self.execute = execute
        self.name = name
        self.create_at_startup = create_at_startup

    def start(self):
        raise NotImplementedError

    @staticmethod
    def split(s):
        return shlex.split(s) if isinstance(s, str) else s or []


class ScheduledCommandTask(Task):
    COMMAND = '(none)'

    def __init__(self, execute, name, target, create_at_startup, every, flags):
        """
        target:
            The root directory to back up to

        every:
            When to schedule this

        flags:
            Command line flags

        create_at_startup:
            If True, immediately create a backup if there is none,
            otherwise wait until the scheduled time for the first backup
        """
        super().__init__(execute, name, create_at_startup)
        self.target = Path(target)
        self.task_dir = self.target / name
        self.every = every
        self.flags = self.split(flags)
        self.command_line = [self.COMMAND]

    def build_command_line(self):
        self.add(*self.flags)

    def start(self):
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
            execute, name, target, create_at_startup, every, flags
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
