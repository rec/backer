from . import config, tasks
from .execute import Execute
import time
import yaml


def _tasks(cfg, execute):
    target = cfg.pop('target')
    source = cfg.pop('source')

    for task_name, section in cfg.items():
        task = tasks.TASKS[task_name]
        for name, desc in section.items():
            desc['target'] = desc['target'] or target
            if 'source' in desc:
                desc['source'] = desc['source'] or source
            yield task(execute, name, **desc)


def main(args=None, print=print):
    execute = Execute()

    cfg = config.config(args)
    if cfg.pop('dry_run'):
        print(yaml.safe_dump(cfg))
        return

    for task in _tasks(cfg, execute):
        task.start()

    return execute


def backer():
    with main():
        try:
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            print('KeyboardInterrupt detected - finishing off tasks')

        except Exception as e:
            print('Unexpected exception detected - finishing off tasks', e)
            raise e

        print('Please wait')

    print('backer has shut down')


if __name__ == '__main__':
    backer()
