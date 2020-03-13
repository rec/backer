from . import git, mongodb, mysql, postgresql, rsync

OMIT_FROM_CONFIG = 'execute', 'name'


def _make():
    tasks, defaults = {}, {}
    for module in git, mongodb, mysql, postgresql, rsync:
        name = module.__name__.split('.')[-1]
        cls = getattr(module, name.capitalize())
        tasks[name] = cls
        defaults[name] = cls.defaults()

    return tasks, defaults


TASKS, DEFAULTS = _make()
