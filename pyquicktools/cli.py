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
    |  0.0.2  | 2023/09/24 | Changind decorators names.                                  |
    |------------------------------------------------------------------------------------|
    |  0.1.0  | 2023/09/24 | Add a working CLI tool.                                     |
     ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
                                                                         ~*~ CHANGELOG ~*~ """


#=--------------=#
# Import section #
#=--------------=#

from   __future__     import annotations
import typing
import logging
import sys
import argparse
import os;sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
import pyquicktools.pyquicktemplate.cli
import pyquicktools.pyquicktest.cli
from   pyquicktools.pyquicktemplate.module  import new_module
from   pyquicktools.pyquicktemplate.package import new_package
from   pyquicktools.pyquicktest.cli         import cli_test

# =------------------------------= #


#=------------------=#
# Authorship section #
#=------------------=#

__author__       = "Quentin Raimbaud"
__contact__      = "quentin.raimbaud.contact@gmail.com"
__copyright__    = None
__credits__      = []
__date__         = "2023/08/14"
__license__      = "MIT"
__maintainer__   = "Quentin Raimbaud"
__organization__ = None
__status__       = "Development"
__version__      = "0.1.0"

# =-------------------------------------------------= #


#=------------------------------------=#
# Constants & Global variables section #
#=------------------------------------=#

NL = '\n'

# =----------------------------------= #


#=-------------------------=#
# main CLI function section #
#=-------------------------=#

def main() -> None:
    """PyQuickTools main CLI function."""

    # Setting up the parser.
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog        = "pqt",
        usage       = "pqt [-h] [-v] [--verbose] COMMAND-GROUP [-h] COMMAND ...",
        description = """
*=-----------=*
| DESCRIPTION |
*=-----------=*
pqt (PyQuickTools) is the main CLI tool for interfacing PyQuickTools toolkit.

pqt targets a broad audience of developers.
https://github.com/quentinemusee/PyQuickTools.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Modifing private attributes for customizing the printing.
    parser._positionals.title = "COMMAND GROUPS"
    parser._optionals.title   = "TOP-LEVEL OPTIONS"

    # Adding the version argument.
    parser.add_argument("-v", "--version", action="version", version=f"PyQuickTools Python CLI v{__version__} status: {__status__}")

    # Adding the verbose argument.
    parser.add_argument(
        "-vv",
        "--verbose",
        action="store_true",
        help="add verbosity printing during the execution of the program",
        default=False
    )

    # Adding subparsers to the parser..
    subparsers = parser.add_subparsers()

    # Filling the commands list with every packages subparser.
    commands: typing.List[typing.Any] = []
    commands.append(pyquicktools.pyquicktemplate.cli.setup_parser(subparsers))
    commands.append(pyquicktools.pyquicktest.cli.setup_parser(subparsers))

    # Setting the parser epilog for customizing the printing.
    parser.epilog = """
*=----------------------=*
| COMMAND GROUPS summary |
*=----------------------=*
template                       create, update and manage templates Python projects
test                           test python project with an easy to deploy testing framework
"""

    # Parsing the provided command line.
    args = parser.parse_args()

    # Updating the verbosity.
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, force=True)
    else:
        logging.basicConfig(level=logging.INFO, force=True)

    # If no function selected, print the corresponding help message.
    if not hasattr(args, "func"):
        parser.parse_args(sys.argv[1:] + ["-h"])
    # Otherwise call the corresponding function.
    else:
        kwargs = vars(args)
        func = kwargs.pop("func")
        func(**kwargs)

# =--------------------------------------------------------------------------------------------------------------------------= #

if __name__ == "__main__":
    main()