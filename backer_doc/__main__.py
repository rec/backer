from backer import describe
from pathlib import Path
from backer.task import task_class


def describe_all(print=print):
    for i, (task, desc) in enumerate(_descriptions().items()):
        i and print()
        print(task + ':')
        for j, (name, field) in enumerate(desc.items()):
            j and print()
            print('  {name}: {type} = {default!r}'.format(**field))
            doc = field['doc']
            if doc:
                for line in _split(doc, 76):
                    print('   ', line)


def _descriptions():
    files = Path(__file__).parent.parent / 'backer' / 'task'
    stems = (f.stem for f in files.iterdir() if f.suffix == '.py')
    names = sorted(s for s in stems if not s.startswith('_'))
    return {n: describe.describe(task_class(n)) for n in names}


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


if __name__ == '__main__':
    describe_all()
