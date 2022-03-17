#!/usr/bin/env python

from setuptools import setup

with open('VERSION') as f:
      version = str(f.read())

setup(name='difft',
      version=version,
      description='Python Distribution Utilities',
      author='difft.org',
      author_email='teams@difft.org',
      url='',
      packages=['difft'],
      python_requires=">=3.6",
     )
     