from . import execute


def run(name, target=None, source=None,
        every='day',
        at='4:32',
        type='mysql',
        tables=None,
        user='user',
        password='password'):
    execute.run('something')
