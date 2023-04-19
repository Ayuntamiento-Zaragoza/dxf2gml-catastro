# -*- coding: UTF-8 -*-

# Copyright (c) 2016-2023 Jose Antonio Chavarría <jachavar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Jose Antonio Chavarría'
__license__ = 'GPLv3'

import sys

if not hasattr(sys, 'version_info') or sys.version_info < (3, 6, 0, 'final'):
    raise SystemExit('This project requires Python 3.6 or later.')

import os
PATH = os.path.dirname(__file__)
README = open(os.path.join(PATH, 'README.md')).read()
VERSION = open(os.path.join(PATH, 'VERSION')).read().splitlines()[0]

from setuptools import setup, find_packages


setup(
    name='dxf2gml-catastro',
    version=VERSION,
    description='dxf2gml_catastro is a web service to generate GML files from DXF',
    long_description=README,
    license='GPLv3',
    author='Jose Antonio Chavarría',
    author_email='jachavar@gmail.com',
    platforms=['Linux'],
    packages = find_packages(),
    data_files=[
        ('/usr/share/doc/dxf2gml-catastro', [
            'AUTHORS',
            'INSTALL',
            'LICENSE',
            'README.md',
            'VERSION',
        ]),
    ],
    entry_points = {
        'console_scripts': [
            'dxf2gml=catastro.dxf2gml:main'
        ],
    },
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
