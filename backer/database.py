from . import execute


def run(name, source=None, target=None,
        every='day',
        at='4:32',
        type='mysql',
        tables=None,
        user='user',
        password='password'):
    execute.run('something')
