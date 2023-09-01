#!/usr/bin/env python
# -*- coding: utf-8 *-*


""" ~*~ Docstring ~*~
     PyQuickTemplate is a tool designed for allowing
    easy and quick python project template management.
    The "utils.py" file contains utiliyy functions for
         the rest of the PyQuickTemplate project.
                                      ~*~ Docstring ~*~

    ~*~ CHANGELOG ~*~
     ____________________________________________________________________________________
    | VERSION |    DATE    |                           CONTENT                           |
    |====================================================================================|
    |  0.0.1  | 2023/08/14 | Initial release.                                            |
     ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
                                                                         ~*~ CHANGELOG ~*~ """


#=--------------=#
# Import section #
#=--------------=#

from   __future__ import annotations
import typing
import argparse

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
__version__      = "0.0.1"

# =-------------------------------------------------= #


#=------------------------------------=#
# Constants & Global variables section #
#=------------------------------------=#

NL = '\n'

# =----------------------------------= #


#=-------------------------=#
# Utility functions section #
#=-------------------------=#

def wider_help_formatter(prog: str):
    return argparse.RawDescriptionHelpFormatter(prog, max_help_position=75, width=142)

def add_group_subparser(
        subparsers  : argparse._SubParsersAction[argparse.ArgumentParser],
        group       : str,
        description : str,
        version     : str,
        prefix      : str = ""
    ) -> argparse._ActionsContainer[argparse.ArgumentParser]:
    parser = subparsers.add_parser(
        group,
        usage=f"""pqt {prefix + ' ' if prefix else ""}{group} COMMAND [-h] [-v] [-vv] ...""",
        description=description,
        formatter_class=wider_help_formatter
    )
    parser.add_argument("-v",  "--version", action="version",    version=version)
    parser.add_argument("-vv", "--verbose", action="store_true", help="add verbosity printing during the execution of the program", default=False)
    parser._positionals.title = "COMMANDS"
    parser._optionals.title   = "OPTIONS"

    return parser

def build_group_epilog(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> str:
    epilog = """
*=----------------------=*
| COMMAND GROUPS summary |
*=----------------------=*
"""
    for choice, sub in subparsers.choices.items():
        description_first_line = sub.description.splitlines()[0]
        epilog += f"{choice.ljust(30)} {description_first_line}\n"

    return epilog

# =------------------------------------------------------------------------= #