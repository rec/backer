import backer
from setuptools import setup

with open('requirements.txt') as f:
    _install_requires = f.read().splitlines()

_classifiers = [
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: Software Development :: Libraries',
    'Topic :: Utilities',
]

if __name__ == '__main__':
    setup(
        name='backer',
        version=backer.__version__,
        author='Tom Ritchford',
        author_email='tom@swirly.com',
        url='https://github.com/rec/backer',
        tests_require=['pytest'],
        py_modules=['backer'],
        description='Continuously back up files',
        long_description=open('README.rst').read(),
        license='MIT',
        classifiers=_classifiers,
        keywords=['backups'],
        install_requires=_install_requires,
        scripts=['scripts/backer'],
    )
