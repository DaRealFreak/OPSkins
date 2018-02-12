#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

current_directory = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(current_directory, 'kuon', '__version__.py'), 'r') as f:
    exec(f.read(), about)

setup(name=about['__title__'],
      version=about['__version__'],
      description=about['__description__'],
      url=about['__url__'],
      author=about['__author__'],
      author_email=about['__author_email__'],
      license=about['__license__'],
      packages=find_packages(),
      install_requires=[
          'requests>=2.18.4', 'requests',
          'python-dotenv>=0.7.1', 'python-dotenv',
          'selenium>=3.8.1', 'selenium',
          'bs4>=0.0.1', 'bs4',
          'html5lib>=1.0.1', 'html5lib'
      ],
      extras_require={
      },
      zip_safe=True)
