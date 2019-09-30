#!/usr/bin/env python

from distutils.core import setup


setup(name='pymudata',
      version='0.0.1',
      description='Wrapepr for inertial signal datasets',
      author='Antonio Bevilacqua',
      author_email='b3by.in.th3.sky@gmail.com',
      maintainer='Antonio Bevilacqua',
      maintainer_email='b3by.in.th3.sky@gmail.com',
      download_url='https://github.com/b3by/pymudata/archive/v0.0.1.tar.gz',
      packages=['pymu'],
      classifiers=[
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7'],
      install_requires=[
          'numpy',
          'pandas'
      ])
