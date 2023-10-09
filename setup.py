#!/usr/bin/env python

from setuptools import setup

with open('VERSION') as f:
      version = str(f.read())

setup(name='difftcc',
      version=version,
      description='Difft Openapi For CC',
      author='difft.org',
      author_email='teams@difft.org',
      url='',
      entry_points={
            'console_scripts': ['difft-cli=difft.command:main']
      },
      packages=['difft'],
      python_requires=">=3.6",
      install_requires=[
            "requests",
            "pycryptodome",
            "websocket-client",
            "rel"
      ],
      )
