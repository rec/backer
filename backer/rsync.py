from .task import ScheduledCommandTask


class Rsync(ScheduledCommandTask):
    COMMAND = 'rsync'

    def __init__(
        self,
        execute,
        name,
        target=None,
        source=None,
        create_at_startup=True,
        every='day@3:32',
        flags='--archive -v --exclude=.git',
    ):
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
        super().__init__(
            execute, name, target, create_at_startup, every, flags
        )
        self.source = source

    def build_command_line(self):
        self.add(self.source or '.', self.task_dir)
        super().build_command_line()
