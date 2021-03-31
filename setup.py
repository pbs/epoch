#!/usr/bin/env python
import os
from setuptools import setup, find_packages

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        'README.rst')
                        
dependencies = [
    'django==1.11.29',
    'pbs_uua_consumer',
    'python-openid==2.2.5',
    'righteous',
    'boto==2.2.2',
    'south==0.7.3',
    'python-dateutil==1.5',
    'django-grappelli==2.3.7'
]

dependency_links = [
    'http://pbs.sourcerepository.s3.amazonaws.com/pbs_uua_consumer-1.0.tar.gz#egg=pbs_uua_consumer-1.0',
    'http://github.com/Atr3ides/righteous/tarball/master#egg=righteous',
]

setup(
    name='epoch',
    version='0.1',
    description='PBS App Days prototype of managing Rightscale deployments',
    long_description=open(README_PATH, 'r').read(),
    author='App Days Epoch Team',
    author_email='tpg-pbs-interactive@threepillarglobal.com',
    url='https://github.com/pbs/epoch',
    packages=find_packages(),
    include_package_data=True,
    install_requires=dependencies,
    setup_requires=['versiontools','s3sourceuploader'],
    dependency_links=dependency_links,
)
