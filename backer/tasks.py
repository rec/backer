from . import git, mongodb, mysql, postgresql, rsync
import inspect

OMIT_FROM_CONFIG = 'execute', 'name'


def _make():
    tasks, defaults = {}, {}
    for module in git, mongodb, mysql, postgresql, rsync:
        name = module.__name__.split('.')[-1]
        cls = getattr(module, name.capitalize())
        tasks[name] = cls

        sig = inspect.signature(cls)
        p = sig.parameters
        p = {k: v.default for k, v in p.items() if k not in OMIT_FROM_CONFIG}
        p = {k: v for k, v in p.items() if v is not sig.empty}
        defaults[name] = p

    return tasks, defaults


TASKS, DEFAULTS = _make()
