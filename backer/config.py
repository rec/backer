"""
The backer configuration combines .yml and .json files together
to return a dictionary.

If file names are provided on the command line, then these are used to
configure the program, otherwise stdin is read.
"""

from . import variables
from .tasks import DEFAULTS
from pathlib import Path
import argparse
import os
import yaml

STEM = Path('backer')
SUFFIXES = '.yml', '.yaml', '.json'


def config(args=None, env=os.environ):
    p = argparse.ArgumentParser(description=_DESCRIPTION)

    p.add_argument('target', default=None, nargs='?', help=_TARGET_HELP)
    p.add_argument('source', default=None, nargs='?', help=_SOURCE_HELP)

    p.add_argument('--config', '-c', nargs='+', help=_CONFIG_HELP)
    p.add_argument('--dry-run', '-d', action='store_true', help=_DRY_RUN_HELP)
    p.add_argument('--env-file', default=None, help=_ENV_FILE_HELP)

    results = vars(p.parse_args(args))
    variables.read_env(results.pop('env_file'))

    configs = results.pop('config') or [_get_default_config()]
    cfg = _combine_sections(configs)
    cfg.update(results)

    return variables.replace(cfg, env)


def _combine_sections(sections):
    config = {}

    for section in sections:
        section = _read_config(section)
        for section_name, tasks in section.items():
            tasks = tasks or {'0': None}
            default = DEFAULTS.get(section_name)
            if not default:
                raise KeyError(section_name)

            section_config = config.setdefault(section_name, {})
            for task_name, task in (tasks or {}).items():
                task_config = section_config.setdefault(task_name, {})
                if not task_config:
                    task_config.update(default)

                for k, v in (task or {}).items():
                    if k not in task_config:
                        raise KeyError(k)
                    task_config[k] = v

    return config


def _read_config(file_or_config):
    if isinstance(file_or_config, dict):
        return file_or_config

    p = Path(file_or_config)
    if p.exists():
        return yaml.safe_load(p.open())

    try:
        return yaml.safe_load(file_or_config)
    except Exception:
        pass

    raise ValueError('Cannot understand config ' + file_or_config)


def _get_default_config():
    for s in SUFFIXES:
        path = STEM.with_suffix(s)
        if path.exists():
            return path

    raise ValueError('No configuration file found')


_DESCRIPTION = 'Periodically back up a directory or database'
_CONFIG_HELP = 'One or more JSON or Yaml configuration files'
_DRY_RUN_HELP = """
If set, print the final configuration and stop without backing up"""
_ENV_FILE_HELP = """
The file to read environment variables from - it is an error if this
file does not exist.  If this variable is not set, environment variables
are read from the file .env, if it exists.  If this variable is set to '',
do not read any environment variables.
"""
_SOURCE_HELP = """
The source directory to back up from.  Default is the current directory."""
_TARGET_HELP = 'The target directory to back up to.'
