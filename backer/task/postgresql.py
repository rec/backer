from ._database import DatabaseTask

# See https://www.postgresql.org/docs/current/app-pgdump.html and
# https://www.postgresql.org/docs/current/app-pg-dumpall.html


class Postgresql(DatabaseTask):
    COMMAND = "pg_dump"
    ALL_COMMAND = "pg_dumpall"

    def build_command_line(self):
        if not self.databases:
            self.command_line[0] = self.ALL_COMMAND
        elif len(self.databases) == 1:
            self.add(self.databases[0])
        else:
            raise ValueError("postgresql can back one database up, or all")

        self.add(file=str(self.out_filename))
        super().build_command_line()
        for table in self.tables:
            self.add(table=table)
