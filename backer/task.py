from pathlib import Path
import shlex


class Task:
    DEFAULTS = {'create': True}

    def __init__(self, execute, name, create):
        self.execute = execute
        self.name = name
        self.create = create

    def start(self):
        raise NotImplementedError


class ScheduledCommandTask(Task):
    COMMAND = '(none)'
    DEFAULTS = dict(Task.DEFAULTS, target=None, every='day', flags='')

    def __init__(self, execute, name, create, target, every, flags):
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