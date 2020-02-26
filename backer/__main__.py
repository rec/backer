from . import config, tasks
from . execute import Execute


def main(args=None):
    cfg = config.config(args)
    execute = Execute()

    target = cfg.pop('target')
    source = cfg.pop('source')

    for task_name, section in cfg.items():
        task = tasks.TASKS[task_name]
        for name, desc in section.items():
            desc['target'] = desc['target'] or target
            desc['source'] = desc['source'] or source
            task.run(execute, name, **desc)

    execute.start()


if __name__ == '__main__':
    main()
