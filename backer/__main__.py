from . import config, signal_handler, stoppable_thread, tasks
from .execute import Execute
import time
import yaml


class MainThread(stoppable_thread.StoppableThread):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.execute = Execute()

    def run(self):
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
        if not self.is_stopped:
            self.execute.start()

    def stop(self):
        super().stop()
        self.execute.stop()

    def join(self):
        if self.is_started:
            super().join()
        if self.execute.is_started:
            self.execute.join()


class Main:
    def __init__(self, args=None):
        self.cfg = config.config(args)
        self.dry_run = self.cfg.pop('dry_run')
        self.thread = None

    def new_thread(self):
        return MainThread(dict(self.cfg))

    def stop(self):
        self.thread and self.thread.stop()

    def backer(self):
        with self.new_thread() as self.thread:
            try:
                while not self.thread.is_stopped:
                    time.sleep(1)

            except KeyboardInterrupt:
                print('KeyboardInterrupt detected')

            except Exception as e:
                print('Unexpected exception detected', e)
                raise e

            print('Finishing off tasks - please wait')
        self.thread = None
        print('Tasks finished')


def backer():
    main = Main()
    if main.dry_run:
        print(yaml.safe_dump(main.cfg))
        return

    signal_handler.run(main.backer, main.stop)


if __name__ == '__main__':
    backer()
