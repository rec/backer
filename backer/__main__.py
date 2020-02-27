from . import config, tasks
from . execute import Execute
import time
import yaml


def block():
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass


def main(args=None, print=print, execute=None):
    cfg = config.config(args)
    execute = execute or Execute()

    if cfg.pop('dry_run'):
        print(yaml.safe_dump(cfg))
        return

    target = cfg.pop('target')
    source = cfg.pop('source')

    for task_name, section in cfg.items():
        task = tasks.TASKS[task_name]
        for name, desc in section.items():
            desc['target'] = desc['target'] or target
            desc['source'] = desc['source'] or source
            task.run(execute, name, **desc)

    return execute.start()


if __name__ == '__main__':
    main()
    block()
