#!/usr/bin/env python3

from setuptools import setup

setup_classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
]

setup(name='py_cmd_exec',
      version='0.5b',
      description='Execute external command',
      author='Filip M. Nowak',
      author_email='github@temp.oneiroi.net',
      url='https://github.com/filipmnowak/py_cmd_exec',
      packages=['py_cmd_exec'],
      classifiers=setup_classifiers
     )
