#!/usr/bin/env python3
#
# Copyright (C) 2016  Carlos Henrique Silva <carlosqsilva@outlook.com>
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

setup(name='pyspc',
      version='0.4',
      description='Statistical Process Control Charts Library for Humans',
      long_description='Statistical Process Control Charts Library for Humans',
      url='https://github.com/carlosqsilva/pyspc',
      author='Carlos Silva',
      author_email='carlosqsilva@outlook.com',
      license='GPLv3',
      packages=find_packages(),
      package_dir={ "pyspc": "pyspc" },
      package_data={
      "pyspc": ["sampledata/*.csv"]},
      install_requires=['pandas', 'matplotlib', 'numpy', 'scipy'],
      test_suite="tests",
      keywords='SPC QCC CEQ CEP UEPA',
      classifiers=[
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Topic :: Scientific/Engineering',
      'Operating System :: Microsoft :: Windows',
      'Operating System :: POSIX :: Linux',
      'Operating System :: MacOS',
      'Programming Language :: Python :: 3.3',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Topic :: Software Development :: Libraries :: Python Modules'],
      zip_safe=False)
