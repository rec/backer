from ._scheduled import dataclass, ScheduledCommandTask


@dataclass
class DatabaseTask(ScheduledCommandTask):
    every: str = 'day'  # override
    user: str = None
    password: str = None
    port: str = None
    host: str = None
    databases: str = None
    tables: str = None
    filename: str = None

    SUFFIX = '.sql'
    TEMP_SUFFIX = '.tmp'

    def __post_init__(self):
        super().__post_init__()
        self.db_flags = {
            'user': self.user,
            'password': self.password,
            'port': self.port,
            'host': self.host,
        }
        self.databases = self.split(self.databases)
        self.tables = self.split(self.tables)

        if self.tables and len(self.databases) != 1:
            raise ValueError('Exactly one database if there are tables')

        if not self.filename:
            self.filename = self.__class__.__name__.lower() + self.SUFFIX

        self.out_filename = self.task_dir / (self.filename + self.TEMP_SUFFIX)
        self.filename = self.task_dir / self.filename

    def build_command_line(self):
        self.add(**self.db_flags)
        super().build_command_line()

    def run(self):
        super().run()
        if self.out_filename.exists():
            self.out_filename.rename(self.filename)
