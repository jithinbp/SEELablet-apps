#!/usr/bin/env python

from __future__ import print_function
#from distutils.core import setup
from setuptools import setup, find_packages
from setuptools.command.install import install
import os,shutil
from distutils.util import execute
from distutils.cmd import Command
from subprocess import call



class CustomInstall(install):
    def run(self):
        install.run(self)

setup(name='SEEL_Apps',
    version='0.1',
    description='Experiment GUIs for the SEELablet. Requires SEEL',
    author='Jithin B.P.',
    author_email='jithinbp@gmail.com',
    url='https://seelablet.jithinbp.in',
    install_requires = ['numpy>=1.8.1','pyqtgraph>=0.9.10'], #SEEL>=
    packages=find_packages(),#['Labtools', 'Labtools.widgets'],
    scripts=["SEEL_Apps/bin/"+a for a in os.listdir("SEEL_Apps/bin/")],
    package_data={'': ['*.css','*.png','*.gif','*.html','*.css','*.js','*.png','*.jpg','*.jpeg','*.htm']},
    cmdclass={'install': CustomInstall},
)

