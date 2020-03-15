from . import task_class
from pathlib import Path
import yaml


def describe(cls, desc=None):
    desc = desc or {}

    try:
        fields = cls.__dataclass_fields__
    except AttributeError:
        return desc

    hidden = getattr(cls, '_HIDDEN_FIELDS', ())
    fields = {k: v for k, v in fields.items() if k not in hidden}

    docs = getattr(cls, '__dataclass_docs__', {})
    if isinstance(docs, str):
        docs = yaml.safe_load(docs)

    for base in cls.__bases__:
        describe(base, desc)

    for name, field in fields.items():
        desc[name] = {
            'name': name,
            'type': field.type.__name__,
            'default': field.default,
            'doc': docs.get(name, ''),
        }

    return desc


def _reduce(desc):
    result = {}
    for name, field in desc.items():
        key = '{name}: {type} = {default}'.format(**field)
        result[key] = field['doc']
    return result


def defaults(cls):
    desc = describe(cls)
    return {k: v['default'] for k, v in desc.items()}


def descriptions():
    files = Path(__file__).parent.iterdir()
    stems = (f.stem for f in files if f.suffix == '.py')
    names = sorted(s for s in stems if not s.startswith('_'))
    return {n: describe(task_class(n)) for n in names}


def describe_all(print=print):
    for i, (task, desc) in enumerate(descriptions().items()):
        i and print()
        print(task + ':')
        for j, (name, field) in enumerate(desc.items()):
            j and print()
            print('  {name}: {type} = {default!r}'.format(**field))
            doc = field['doc']
            if doc:
                for line in _split(doc, 76):
                    print('   ', line)


def _split(line, width):
    parts, total = [], 0
    for word in line.split():
        lw = len(word) + 1
        if total + lw > width:
            yield ' '.join(parts)
            parts, total = [], 0
        parts.append(word)
        total += lw

    if parts:
        yield ' '.join(parts)
