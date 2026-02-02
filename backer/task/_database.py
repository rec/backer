from ._scheduled import dataclass, ScheduledCommandTask


@dataclass
class DatabaseTask(ScheduledCommandTask):
    every: str = "day"  # override
    host: str = None
    port: str = None
    user: str = None
    password: str = None
    databases: str = None
    tables: str = None
    filename: str = None

    SUFFIX = ".sql"
    TEMP_SUFFIX = ".tmp"

    def __post_init__(self):
        super().__post_init__()
        self.db_flags = {
            "user": self.user,
            "password": self.password,
            "port": self.port,
            "host": self.host,
        }
        self.databases = self.split(self.databases)
        self.tables = self.split(self.tables)

        if self.tables and len(self.databases) != 1:
            raise ValueError("Exactly one database if there are tables")

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

    __dataclass_docs__ = """
host: >-
    The URL host for this database (blank means localhost)

port: >-
    The numeric port on which to contact the database

user: >-
    The database user

password: >-
    The password for the database user.  You can use variables to read
    passwords from the environment or .env file without storing them in
    config files.

databases: >-
    A list of databases to back up.  Blank means "backup all databases".

tables: >-
    A list of tables to back up.  Blank means "backup all tables".
    tables: and databases: cannot both be set

filename: >-
    The name of the backup file (defaults to <database>.sql
"""
