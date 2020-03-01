from .task import ScheduledCommandTask


class Rsync(ScheduledCommandTask):
    COMMAND = 'rsync'
    DEFAULTS = dict(
        ScheduledCommandTask.DEFAULTS,
        every='day@3:32',
        flags='--archive -v --exclude=.git',
        source='.')

    def __init__(self, *args, source, **kwds):
        """
        Parameters from ScheduledCommandTask, plus:

        source:
           The directory to back up - default is the current working directory
        """
        super().__init__(*args, **kwds)
        self.source = source

    def start(self):
        self.command_line.extend((self.source, self.task_dir))
        super().start()


def run(execute, name, target=None, source=None,
        every='day@3:32',
        flags='--archive -v --exclude=.git',
        create=True):
    rs = Rsync(execute, name, create, target, every, flags, source=source)
    rs.start()
