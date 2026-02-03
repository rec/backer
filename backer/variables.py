"""
Perform variable substituition like Python's format strings or Docker
compose format.

See
https://docs.docker.com/compose/compose-file/
#volume-configuration-reference#variable-substitution

Python format:
    {VAR} - throws an exception if VAR is unset

Docker format:
    $VAR or ${VAR} - If VAR is unset, the empty string is used
    ${VAR:-default} - evaluates to default if VAR is unset or empty
    ${VAR-default} - evaluates to default only if VAR is unset.
    ${VAR:?err} - throws an exception containing err if VAR is unset or empty
    ${VAR?err} - throws an exception containing err if VAR is unset
"""

import os
import re
from pathlib import Path

import dotenv

DOCKER_RE = re.compile(
    r"""
\$ ( \w+ \b ) |
#    name1

\$ \{ ( \w* \b ) (?: ( \:? ) ( [-?] ) ( [^}]+ ) )? \}
#        name2        colon    sep       arg

""",
    re.X,
)


def read_env(env_file=None):
    """Read environment variables from a .env file"""
    if env_file != "":
        if isinstance(env_file, str) and not Path(env_file).exists():
            raise FileNotFoundError(env_file)

        dotenv.load_dotenv(env_file)


def replace(s, env=None):
    if isinstance(s, str):
        if "$" in s or "{" in s:
            return "".join(_apply(s, env))
        return s

    if isinstance(s, dict):
        return {replace(k, env): replace(v, env) for k, v in s.items()}

    if isinstance(s, list):
        return [replace(i, env) for i in s]

    if isinstance(s, tuple):
        return tuple(replace(i, env) for i in s)

    return s


def _apply(s, env):
    split = DOCKER_RE.split(s)
    assert len(split) % 6 == 1
    env = os.environ if env is None else env or {}

    for before, name1, name2, colon, sep, arg in zip(*[iter(split)] * 6, strict=True):
        yield before.format(**env or {})

        if name1 == "" or name2 == "":
            raise KeyError("Empty variable name")

        value = env.get(name1 or name2)
        if sep == "?":
            if value is None or (colon and not value):
                raise KeyError(arg or 'Variable "%s" does not exist' % name2)

        elif sep == "-":
            if value is None or (colon and not value):
                value = arg

        yield value or ""

    yield split[-1].format(**env)
