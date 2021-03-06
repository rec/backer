from ._task import dataclass, Task
from pathlib import Path


@dataclass
class ScheduledCommandTask(Task):
    target: str = None
    every: str = ''
    flags: str = ''

    COMMAND = '(none)'

    def __post_init__(self):
        self.target = Path(self.target)
        self.task_dir = self.target / self.name

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

    __dataclass_docs__ = """
target: >-
    The target directory to write the backup to

every: >-
    How often to perform this backup

flags: >-
    Command line flags to the command, either as a single string that will be
    split by shlex, or as a list of string arguments
"""
