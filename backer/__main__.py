from . import config, execute, tasks

COMMON_CONFIGS = 'target', 'source'


def main():
    cfg = config.config()
    common = {k: cfg.pop(k) for k in COMMON_CONFIGS}

    if not cfg:
        raise ValueError('No configuration')

    for task_name, section in cfg.items():
        task = tasks.TASKS[task_name]
        for name, desc in section.items():
            for k, v in common.items():
                if k not in section:
                    section[k] = v

            task(name, **desc)

    execute.start()


if __name__ == '__main__':
    main()
