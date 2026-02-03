import importlib


def task_class(name):
    if "." not in name:
        name = f"{__package__}.{name}"

    mod = importlib.import_module(name)
    r = name.split(".")[-1].lower()
    items = [v for k, v in vars(mod).items() if callable(v) and k.lower() == r]
    if len(items) < 1:
        raise ValueError("No task in " + name)
    if len(items) > 1:
        raise ValueError("Ambiguous task in " + name)
    return items[0]
