from . task import Task


class Database(Task):
    def __init__(
            self, execute, name, target=None, source=None,
            every='day@4:32',
            database=None,
            table=None,
            user=None,
            password=None,
            port=None,
            host=None,
            flags=None):
        command_line = [self.COMMAND]

        if isinstance(flags, str):
            flags = flags.split()
        elif flags is None:
            flags = self.DEFAULT_FLAGS

        for key, value in locals().items():
            if key in self.FLAG_VARIABLES:
                if value is not None:
                    command_line.append('--%s=%s' % (key, value))
            elif key != 'self':
                setattr(self, key, value)

        if flags:
            command_line.extend(flags)

        execute.schedule(self._backup, every)

    COMMAND = 'fail'
    FLAG_VARIABLES = {'user', 'password', 'port', 'host'}
    DEFAULT_FLAGS = ''
    OUTPUT_FLAG = ''

    def _backup(self):
        pass
