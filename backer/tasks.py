from . import git, mongodb, mysql, postgresql, rsync
import inspect


def _make():
    tasks, defaults = {}, {}
    for module in git, mongodb, mysql, postgresql, rsync:
        name = module.__name__.split('.')[-1]
        cls = getattr(module, name.capitalize())
        tasks[name] = cls

        sig = inspect.signature(cls)
        params = sig.parameters
        d = {k: v.default for k, v in params.items()}
        defaults[name] = {k: v for k, v in d.items() if v is not sig.empty}

    return tasks, defaults


TASKS, DEFAULTS = _make()
