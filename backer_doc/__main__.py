from backer import describe
from backer.task import task_class
from pathlib import Path
import safer

ROOT = Path(__file__).parent.parent
DIVIDER = 'backer task reference'
README = ROOT / 'README.rst'


def write_docs(readme=README):
    files = ROOT / 'backer' / 'task'
    stems = (f.stem for f in files.iterdir() if f.suffix == '.py')
    files = sorted(s for s in stems if not s.startswith('_'))

    lines = []
    for line in readme.open():
        lines.append(line)
        if line.lower().startswith(DIVIDER):
            break

    with safer.printer(readme) as print:
        print(*lines, sep='\n')
        print('-' * len(lines[-1]) + '\n')

        for name in files:
            print(_describe_one(name))


def _describe_one(name, print=print):
    cls = task_class(name)
    desc = describe.describe(cls)
    intro, body = _get_doc(cls)
    filename = (ROOT / 'doc' / name).with_suffix('.rst')
    with safer.printer(filename) as print:
        title = '%s: %s' % (name, intro)
        print(title)
        print('-' * len(title))
        print()

        for j, (name, field) in enumerate(desc.items()):
            j and print()
            print('``{name}: {type} = {default!r}``'.format(**field))
            for line in _split(field['doc'], 76):
                print('   ', line)

    return f'``{name}``:\n  {intro}\n'


def _get_doc(cls):
    doc = getattr(cls, '__doc__', None) or ''
    lines = [i.strip() for i in doc.splitlines()]
    intro = []
    while lines and not lines[0]:
        lines.pop(0)

    while lines and lines[0]:
        intro.append(lines.pop(0))

    while lines and not lines[0]:
        lines.pop(0)

    return ' '.join(intro), ' '.join(lines)


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
    write_docs()
