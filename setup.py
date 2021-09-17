#! /usr/bin/env python3
"""Install script."""

from setuptools import setup


setup(
    name='marketplace',
    use_scm_version={
        'local_scheme': 'node-and-timestamp'
    },
    setup_requires=['setuptools_scm'],
    install_requires=[
        'configlib',
        'emaillib',
        'flask',
        'functoolsplus',
        'his',
        'hwdb',
        'mdb',
        'notificationlib',
        'peewee',
        'peeweeplus',
        'previewlib',
        'wsgilib'
    ],
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info@homeinfo.de>',
    maintainer='Richard Neumann',
    maintainer_email='<r.neumann@homeinfo.de>',
    packages=['marketplace'],
    license='GPLv3',
    description='Library for a simple market place for ComCat.'
)
