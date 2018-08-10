#!/usr/bin/env python

"""
Run with:

sudo python ./setup.py install
"""
from subprocess import call
from git import *
from time import gmtime, strftime

import sys
import os

if sys.version_info[:2] < (2, 6):
    raise Exception('This version of tagger needs Python 2.6 or later. ')

from setuptools import setup, find_packages

def generateHumansTxt():
	repo = Repo(os.getcwd())
	f = open(os.getcwd()+"/humans.txt","w")
	f.write("{\"buildNumber\": \"" + os.getenv('BUILD_NUMBER','') + "\",\n")
	f.write(" \"gitCommitId\": \"" + repo.head.commit.hexsha + "\",\n")
	f.write(" \"builtOn\"    : \"" + strftime("%d-%m-%Y %H:%M:%S %z", gmtime()) + "\"}")
	f.close()

generateHumansTxt()

setup(
    name = 'tagger',
    version = '0.1.0',
    description = 'Cisco-B2B-Tagger',

    packages = find_packages(exclude=["tests"]),
    zip_safe = False,
    include_package_data = True,
)
