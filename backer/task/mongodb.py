from ._database import DatabaseTask

# See https://docs.mongodb.com/manual/reference/program/mongodump/


class Mongodb(DatabaseTask):
    COMMAND = "mongodump"
    SUFFIX = ".sql.gz"

    def build_command_line(self):
        if len(self.databases) > 1:
            raise ValueError("mongodb can back one database up, or all")

        if len(self.tables) > 1:
            raise ValueError("mongodb can back one collection up, or all")

        super().build_command_line()
        self.add(archive=str(self.out_filename))

        if self.filename.suffix.endswith(".gz"):
            self.add(gzip=True)

        if self.databases:
            self.add(db=self.databases[0])
            if self.tables:
                self.add(collection=self.tables[0])

        print(*self.command_line)
        print(self.command_line)
