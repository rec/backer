from . import config, stoppable_thread, tasks
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
            if not self.is_running:
                return

            task = tasks.TASKS[task_name]
            for name, desc in section.items():
                desc['target'] = desc['target'] or target
                if 'source' in desc:
                    desc['source'] = desc['source'] or source

                task(self.execute, name, **desc).start()


def main(args=None, print=print):
    cfg = config.config(args)
    if cfg.pop('dry_run'):
        print(yaml.safe_dump(cfg))
        return

    with MainThread(cfg) as mt:
        return mt.execute


def backer():
    with main():
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
