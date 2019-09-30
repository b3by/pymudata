#!/usr/bin/env python

from setuptools import setup


with open('README.md', 'r') as f:
    long_description = f.read()

setup(name='pymudata',
      version='0.0.1',
      description='Wrapepr for inertial signal datasets',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Antonio Bevilacqua',
      author_email='b3by.in.th3.sky@gmail.com',
      maintainer='Antonio Bevilacqua',
      maintainer_email='b3by.in.th3.sky@gmail.com',
      url='https://github/com/b3by/pymudata',
      packages=['pymudata'],
      classifiers=[
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7',
          'Operating System :: OS Independent'],
      install_requires=[
          'numpy',
          'pandas'
      ],
      python_requires='>=3.6')
