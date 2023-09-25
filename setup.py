#!/usr/bin/env python
# -*- coding: utf-8 *-*


""" ~*~ Docstring ~*~
     PyQuickTemplate is a tool designed for allowing
    easy and quick python project template management.
      A single CLI line is required to create single
     file project, folder project, library or package.
                                     ~*~ Docstring ~*~

    ~*~ CHANGELOG ~*~
     ____________________________________________________________________________________
    | VERSION |    DATE    |                           CONTENT                           |
    |====================================================================================|
    |  0.0.1  | 2023/08/14 | Initial release.                                            |
    |------------------------------------------------------------------------------------|
    |  0.1.0  | 2023/09/24 | Add a working CLI tool.                                     |
     ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
                                                                         ~*~ CHANGELOG ~*~ """


#=--------------=#
# Import section #
#=--------------=#

from setuptools       import find_packages, setup
from pyquicktools.cli import __version__
import os

# =-------------------------------------= #


#=------------------=#
# Authorship section #
#=------------------=#

__author__       = "Quentin Raimbaud"
__contact__      = "quentin.raimbaud.contact@gmail.com"
__copyright__    = None
__credits__      = []
__date__         = "2023/09/23"
__license__      = "MIT"
__maintainer__   = "Quentin Raimbaud"
__organization__ = None
__status__       = "Development"
__version__      = "0.1.0"

# =--------------------------------------------------------= #


#=-------------------------=#
# Utility functions section #
#=-------------------------=#

def get_required_packages():
    with open("requirements.txt", 'r') as file:
        return file.read().splitlines()


def get_readme():
    with open("README.md", 'r') as file:
        return file.read()
    
# =-----------------------------------------= #


#=---------------------=#
# Package setup section #
#=---------------------=#

if __name__ == "__main__":

    REQUIRED_PACKAGES = get_required_packages()

    setup(
        name="PyQuickTools",
        version=__version__,
        description="PyQuickTools provides quick-to-use tools for Python developers.",
        long_description=get_readme(),
        url="https://github.com/quentinemusee/PyQuickTools",
        author="Quentin Raimbaud",
        author_email="quentin.raimbaud.contact@gmail.com",
        packages=find_packages(),
        # entry_points={
        #     "console_scripts": ["pqt = pyquicktools.cli:main"],
        # },
        #install_requires=REQUIRED_PACKAGES,
        #tests_require=REQUIRED_PACKAGES,
        python_requires=">=3.9",
        classifiers=[
            "Development Status :: 1 - Planning",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3 :: Only",
            "Operating System :: OS Independent",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Utilities",
            "Topic :: Software Development :: Libraries",
        ],
        license="MIT",
        #keywords="pyquicktools python quick tools template test cli",
    )

# =---------------------------------------------------------------------------------------= #