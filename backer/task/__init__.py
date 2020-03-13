from . import git, mongodb, mysql, postgresql, rsync
from pathlib import Path

OMIT_FROM_CONFIG = 'execute', 'name'


def _make():
    tasks, defaults = {}, {}
    for module in git, mongodb, mysql, postgresql, rsync:
        name = module.__name__.split('.')[-1]
        cls = getattr(module, name.capitalize())
        tasks[name] = cls

        t = cls()
        keys = (k for k in t.__dataclass_fields__ if k not in OMIT_FROM_CONFIG)
        d = {k: getattr(t, k) for k in keys}
        d = {k: str(v) if isinstance(v, Path) else v for k, v in d.items()}
        defaults[name] = d

    return tasks, defaults


TASKS, DEFAULTS = _make()
