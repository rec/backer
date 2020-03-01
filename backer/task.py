from pathlib import Path
import shlex


class Task:
    def __init__(self, execute, name, create):
        self.execute = execute
        self.name = name
        self.create = create

    def start(self):
        raise NotImplementedError


class ScheduledCommandTask(Task):
    COMMAND = '(none)'

    def __init__(self, execute, name, target, create, every, flags):
        """
        target:
            The root directory to back up to

        every:
            When to schedule this

        flags:
            Command line flags

        create:
            If True, immediately create an backup if there is none,
            otherwise wait until the scheduled time for the first backup
        """
        super().__init__(execute, name, create)
        self.target = Path(target)
        self.task_dir = self.target / name
        self.every = every
        self.flags = shlex.split(flags) if isinstance(flags, str) else flags
        self.command_line = [self.COMMAND]

    def start(self):
        self.command_line.extend(self.flags)
        if not self.task_dir.exists():
            self.task_dir.mkdir(parents=True)
            if self.create:
                if not self.run():
                    raise ValueError('Creation failed')

        self.execute.schedule(self.run, self.every)

    def run(self):
        ec = self.execute.run(*self.command_line)
        if ec:
            print('ERROR: code:', ec)

        return ec


class DatabaseTask(ScheduledCommandTask):
    FLAG_VARIABLES = {'user', 'password', 'port', 'host'}

    def __init__(self, execute, name, target, create, every, flags,
                 user, password, port, host, database, table):
        super().__init__(execute, name, target, create, every, flags)
        for key in self.FLAG_VARIABLES:
            value = locals()[key]
            if value is not None:
                self.command_line.append('--%s=%s' % (key, value))

        self.database = database
        self.table = table
