from backer import describe
from backer.task import task_class
from pathlib import Path
import contextlib
import functools

ROOT = Path(__file__).parent.parent
DIVIDER = 'backer task reference'


def write_docs(print=print):
    assert print is not __builtins__['print']
    files = ROOT / 'backer' / 'task'
    stems = (f.stem for f in files.iterdir() if f.suffix == '.py')
    files = sorted(s for s in stems if not s.startswith('_'))

    readme = ROOT / 'README.rst'

    lines = []
    for line in readme.open():
        lines.append(line)
        if line.lower().startswith(DIVIDER):
            break

    with _open(readme, print) as pr:
        __builtins__['print']('HERE!')
        pr('here')
        pr(*lines, sep='\n')
        pr('-' * len(lines[-1]) + '\n')

        for name in files:
            pr(_describe_one(name))


def _describe_one(name, print=print):
    cls = task_class(name)
    desc = describe.describe(cls)
    intro, body = _get_doc(cls)
    filename = (ROOT / 'doc' / name).with_suffix('.rst')
    with _open(filename, print) as pr:
        title = '%s: %s' % (name, intro)
        pr(title)
        pr('-' * len(title))
        pr()

        for j, (name, field) in enumerate(desc.items()):
            j and pr()
            pr('``{name}: {type} = {default!r}``'.format(**field))
            for line in _split(field['doc'], 76):
                pr('   ', line)

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


@contextlib.contextmanager
def _open(filename, print=print):
    with open(filename, 'w') as fp:
        def pr(*args, **kwds):
            __builtins__['print']('XXX', args, kwds)
            print(*args, **kwds, file=fp)

        if True:
            yield pr
        else:
            yield functools.partial(print, file=fp)


if __name__ == '__main__':
    write_docs()
