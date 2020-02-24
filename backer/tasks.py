from . import database, git, rsync
import inspect


def _make():
    tasks, defaults = {}, {}
    for module in database, git, rsync:
        name = module.__name__.split('.')[-1]
        tasks[name] = module

        sig = inspect.signature(module.run)
        params = sig.parameters
        d = {k: v.default for k, v in params.items()}
        defaults[name] = {k: v for k, v in d.items() if v is not sig.empty}

    return tasks, defaults


TASKS, DEFAULTS = _make()
