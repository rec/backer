"""
Perform variable substituition like Python's format strings or Docker
compose format

See
https://docs.docker.com/compose/compose-file/
#volume-configuration-reference#variable-substitution

{x} - Python format

$VAR
${VAR}
${VAR:-default} evaluates to default if VAR is unset or empty
${VAR-default} evaluates to default only if VAR is unset.
${VAR:?err} errors with a message containing err if VAR is unset or empty
${VAR?err} errors with a message containing err if VAR is unset

"""

import re

DOCKER_RE = re.compile(r"""
\$ ( \w+ \b ) |
#    name1

\$ \{ ( \w* \b ) (?: ( \:? ) ( [-?] ) ([^}]+ ) )? \}
#       name2        colon    sep     arg

""", re.X)


def _apply(s, env):
    split = DOCKER_RE.split(s)
    assert len(split) % 6 == 1

    for before, name1, name2, colon, sep, arg in zip(*[iter(split)] * 6):
        yield before.format(**env)

        if name1 == '' or name2 == '':
            raise KeyError('Empty variable name')

        value = env.get(name1 or name2)
        if sep == '?':
            if value is None or (colon and not value):
                raise KeyError(
                    arg or 'Variable "%s" does not exist' % name2)
        elif sep == '-':
            if value is None or (colon and not value):
                value = arg

        yield value or ''

    yield split[-1].format(**env)


def apply(s, **env):
    return ''.join(_apply(s, env))
