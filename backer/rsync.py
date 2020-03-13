from .task import ScheduledCommandTask
from dataclasses import dataclass


@dataclass
class Rsync(ScheduledCommandTask):
    """
    target:
        The root directory to back up to

    every:
        When to schedule this

    flags:
        Command line flags

    create_at_startup:
        If True, immediately create an backup if there is none,
        otherwise wait until the scheduled time for the first backup

    source:
       The directory to back up - default is the current working directory
    """

    COMMAND = 'rsync'
    DEFAULT_EVERY = 'day@3:32'
    DEFAULT_FLAGS = '--archive -v --exclude=.git'

    source: str = None

    def build_command_line(self):
        self.add(self.source or '.', self.task_dir)
        super().build_command_line()
