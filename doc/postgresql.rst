postgresql: 
------------

``create_at_startup: bool = True``

``target: str = None``

``every: str = 'day'``

``flags: str = ''``

``host: str = None``
    The URL host for this database (blank means localhost)

``port: str = None``
    The numeric port on which to contact the database

``user: str = None``
    The database user

``password: str = None``
    The password for the database user. You can use variables to read passwords
    from the environment or .env file without storing them in config files.

``databases: str = None``
    A list of databases to back up. Blank means "backup all databases".

``tables: str = None``
    A list of tables to back up. Blank means "backup all tables". tables: and
    databases: cannot both be set

``filename: str = None``
    The name of the backup file (defaults to <database>.sql
