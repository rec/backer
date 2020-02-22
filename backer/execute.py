import subprocess


def execute(*args):
    print('$', *args)
    result = subprocess.check_output(args, encoding='utf-8')
    print(result)
    return [i.rstrip() for i in result.splitlines()]
