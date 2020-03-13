from dataclasses import dataclass
import shlex
import yaml


@dataclass
class Task:
    execute: object = None
    name: str = ''
    create_at_startup: bool = True

    OMIT_FROM_DEFAULTS = {'execute', 'name'}

    def start(self):
        raise NotImplementedError

    @classmethod
    def defaults(cls):
        fields, omit = cls.__dataclass_fields__, cls.OMIT_FROM_DEFAULTS
        return {k: v.default for k, v in fields.items() if k not in omit}

    @staticmethod
    def split(s):
        return shlex.split(s) if isinstance(s, str) else s or []

    @classmethod
    def docs(cls):
        try:
            parent = super().docs()
        except Exception:
            parent = {}

        dd = cls.__dataclass_docs__
        dd = yaml.safe_load(dd) if isinstance(dd, str) else dd
        return dict(parent, **dd)

    __dataclass_docs__ = """
create_at_startup: >-
    If True, immediately create a backup if there is none, otherwise wait
    until the scheduled time for the first backup
"""
