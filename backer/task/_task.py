from dataclasses import dataclass
import shlex


@dataclass
class Task:
    execute: object = None
    name: str = ''
    create_at_startup: bool = True

    _HIDDEN_FIELDS = {'execute', 'name'}

    def start(self):
        raise NotImplementedError

    @staticmethod
    def split(s):
        return shlex.split(s) if isinstance(s, str) else s or []

    __dataclass_docs__ = """
create_at_startup: >-
    If True, immediately create a backup if there is none, otherwise wait
    until the scheduled time for the first backup
"""
