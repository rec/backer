from .task import DatabaseTask

# See https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html


class Mysql(DatabaseTask):
    COMMAND = 'mysqldump'

    def build_command_line(self):
        super().build_command_line()

        self.add(result_file=str(self.filename))

        if not self.databases:
            self.add(all_databases=True)

        elif not self.tables:
            self.add(databases=True)
            self.add_arg(*self.databases)

        else:
            (database,) = self.databases
            self.add(database, *self.tables)
