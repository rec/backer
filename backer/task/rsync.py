from ._scheduled import ScheduledCommandTask
from dataclasses import dataclass


@dataclass
class Rsync(ScheduledCommandTask):
    every: str = 'day@3:32'
    flags: str = '--archive -v --exclude=.git'
    source: str = None

    COMMAND = 'rsync'

    def build_command_line(self):
        self.add(self.source or '.', self.task_dir)
        super().build_command_line()
