from dataclasses import dataclass
import shlex


@dataclass
class Task:
    """
    create_at_startup:
        If True, immediately create a backup if there is none,
        otherwise wait until the scheduled time for the first backup
    """

    execute: object = None
    name: str = ''
    create_at_startup: bool = True

    def start(self):
        raise NotImplementedError

    @staticmethod
    def split(s):
        return shlex.split(s) if isinstance(s, str) else s or []
