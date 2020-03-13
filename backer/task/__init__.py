from . import git, mongodb, mysql, postgresql, rsync


def _make():
    tasks = {}
    for module in git, mongodb, mysql, postgresql, rsync:
        name = module.__name__.split('.')[-1]
        tasks[name] = getattr(module, name.capitalize())

    return tasks


TASKS = _make()
