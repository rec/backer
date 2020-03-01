from . task import ScheduledCommandTask


class Mysql(ScheduledCommandTask):
    def __init__(self, execute, name,
                 target=None,
                 create=True,
                 every='day@4:32',
                 flags='',
                 type='mysql',
                 tables=None,
                 databases=None,
                 user='user',
                 password='password'):
        super().__init__(execute, name, target, create, every, flags)

        self.type = type
        self.tables = tables
        self.databases = databases
        self.user = user
        self.password = password
