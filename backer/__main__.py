from . import config, tasks
from .execute import Execute
import time
import yaml


def backer(args=None, print=print, block=True):
    cfg = config.config(args)
    if cfg.pop('dry_run'):
        print(yaml.safe_dump(cfg))
        return

    target = cfg.pop('target')
    source = cfg.pop('source')

    execute = Execute()

    for task_name, section in cfg.items():
        task = tasks.TASKS[task_name]
        for name, desc in section.items():
            desc['target'] = desc['target'] or target
            if 'source' in desc:
                desc['source'] = desc['source'] or source
            task(execute, name, **desc).start()

    if block:
        with execute:
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass

    return execute


if __name__ == '__main__':
    backer()
