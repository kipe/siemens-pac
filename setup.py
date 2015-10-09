#!/usr/bin/env python
from distutils.core import setup

setup(
    name='siemens-pac',
    version='0.20',
    description='A Python library for reading Siemens SENTRON PAC -series measurement devices.',
    author='Kimmo Huoman',
    author_email='kipenroskaposti@gmail.com',
    url='https://github.com/kipe/siemens-pac',
    packages=['siemens'],
    install_requires=[
        'modbus-tk>=0.4.3',
        'pyserial>=2.7',
    ])
