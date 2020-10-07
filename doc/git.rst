git: `git commit` automatically on any change within a directory.
-----------------------------------------------------------------

``create_at_startup: bool = True``

``target: str = None``

``source: str = None``
    source directory to be backed up (default is current directory)

``git_init: bool = True``
    If `source` is not a Git repository, then if `git_init` is True, then `git
    init` will be called, otherwise ValueError is raised

``remotes: dict = None``
    A dictionary mapping remote names to remote URLs

``add_unknown_files: bool = True``
    If True, unknown files are automatically `git add`'ed

``file_event_window: float = 0.05``
    If `file_event_window` is non-zero, then all file events during that time
    window (in seconds) are consolidated into a single git commit

``commit_message: str = '%Y-%m-%dT%H:%M%SZ'``
    A strftime-style format string for commit messages
