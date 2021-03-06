#!/usr/bin/env python

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README')) as f:
    README = f.read()

requires = []

setup(name='python-dogecoinlib',
      version='0.4.1-SNAPSHOT',
      description='The Swiss Army Knife of the Dogecoin protocol.',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
      ],
      url='https://github.com/petertodd/python-dogecoinlib',
      keywords='dogecoin',
      packages=find_packages(),
      zip_safe=False,
      install_requires=requires,
      test_suite="dogecoin.tests"
     )
