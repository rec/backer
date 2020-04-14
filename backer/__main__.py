from . import config, signal_handler, stoppable_thread
from .execute import Execute
from .task import task_class
import time
import yaml


class MainThread(stoppable_thread.StoppableThread):
    def __init__(self, target=None, source=None, **cfg):
        super().__init__()
        self.cfg = cfg
        self.execute = Execute()
        self.target = target
        self.source = source

    def run(self):
        for task_name, section in self.cfg.items():
            if self.is_stopped:
                return

            task = task_class(task_name)
            for name, desc in section.items():
                desc['target'] = desc['target'] or self.target
                if 'source' in desc:
                    desc['source'] = desc['source'] or self.source

                task(execute=self.execute, name=name, **desc).start()
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
        if self.cfg:
            self.dry_run = self.cfg.pop('dry_run')
            self.thread = None

    def run(self):
        if not self.cfg:
            print('Nothing to backup')
        elif self.dry_run:
            print(yaml.safe_dump(self.cfg))
        else:
            signal_handler.run(self.backer, self.stop)

    def new_thread(self):
        return MainThread(**self.cfg)

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


if __name__ == '__main__':
    Main().run()
