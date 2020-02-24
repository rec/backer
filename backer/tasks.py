import inspect
import importlib


def _task(name):
    mod = importlib.import_module('backer.' + name)
    sig = inspect.signature(mod.run)
    params = sig.parameters
    defaults = {k: v.default for k, v in params.items()}
    mod.DEFAULTS = {k: v for k, v in defaults.items() if v is not sig.empty}
    return mod


TASKS = {k: _task(k) for k in ('database', 'git', 'rsync')}
DEFAULTS = {k: v.DEFAULTS for k, v in TASKS.items()}
