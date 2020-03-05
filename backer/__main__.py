from . import config, stoppable_thread, tasks
from .execute import Execute
import time
import yaml


class MainThread(stoppable_thread.StoppableThread):
    def __init__(self, args=None):
        super().__init__()
        cfg = config.config(args)
        self.dry_run = cfg.pop('dry_run')
        self.cfg = cfg
        self.execute = Execute()

    def run(self):
        if self.dry_run:
            return

        target = self.cfg.pop('target')
        source = self.cfg.pop('source')

        for task_name, section in self.cfg.items():
            if self.is_stopped:
                return

            task = tasks.TASKS[task_name]
            for name, desc in section.items():
                desc['target'] = desc['target'] or target
                if 'source' in desc:
                    desc['source'] = desc['source'] or source

                task(self.execute, name, **desc).start()
        self.execute.start()

    def stop(self):
        super().stop()
        self.execute.stop()

    def join(self):
        if self.is_started:
            super().join()
        if False and self.execute.is_started:
            self.execute.join()


def main(args=None, print=print):
    main = MainThread(args)
    if main.dry_run:
        print(yaml.safe_dump(main.cfg))
        return

    with main:
        return main.execute


def backer():
    with MainThread() as mt:
        if mt.dry_run:
            print(yaml.safe_dump(mt.cfg))
            return

        try:
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            print('KeyboardInterrupt detected')

        except Exception as e:
            print('Unexpected exception detected', e)
            raise e

        print('Finishing off tasks - please wait')

    print('backer has shut down')


if __name__ == '__main__':
    backer()
