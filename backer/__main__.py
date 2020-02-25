from . import config, execute, tasks
import yaml


def main(args=None, print=print):
    cfg = config.config(args)

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
            task.run(name, **desc)

    execute.start()


if __name__ == '__main__':
    main()
