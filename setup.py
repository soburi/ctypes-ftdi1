#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.rst', 'r') as fh:
    long_desc = fh.read()

setup(name='ctypes-ftdi1',
      version='0.0.4',
      description='libftdi1 python bindings based on ctypes',
      long_description=long_desc,
      license='MIT',
      author='Tokita Hiroshi',
      author_email='tokita.hiroshi@gmail.com',
      url='https://github.com/soburi/ctypes-ftdi1',
      platforms=['any'],
      packages=find_packages(),
      classifiers=[
          'Programming Language :: Python',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Topic :: System :: Hardware :: Hardware Drivers']
     )
