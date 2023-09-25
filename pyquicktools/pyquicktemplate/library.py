#!/usr/bin/env python
# -*- coding: utf-8 *-*


""" ~*~ Docstring ~*~
       PyQuickTemplate is a tool designed for allowing
      easy and quick python project template management.
        The "librarys.py" file contains functions for
    generating and updating python multiple files projects
                        from templates.
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
import os
from   pyquicktools.pyquicktemplate.utils import guard_credits, guard_date, guard_filename, guard_status, guard_version, guard_docstring, guard_template_file, guard_indent, parse_template
from   pyquicktools.uutils.uutils         import filter1, write_file

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

#=---------------------------=#
# Top-level functions section #
#=---------------------------=#

def new_library(**kwargs : typing.List[str] | str | int | None) -> None:
    """Create a new python library project from the given parameters.
    : param authors       : The authors        of the new python library project.
    : param contact       : The contact        of the new python library project.
    : param copyright     : The copyright      of the new python library project.
    : param credits       : The credits        of the new python library project.
    : param date          : The date           of the new python library project.
    : param license       : The license        of the new python library project.
    : param maintainer    : The maintainer     of the new python library project.
    : param organization  : The organization   of the new python library project.
    : param status        : The status         of the new python library project.
    : param version       : The version        of the new python library project.
    : param docstring     : The docstring      of the new python library project.
    : param filenames     : The filenames list of the new python library project.
    : param main_file     : The main file name of the new python library project. If not provided, "main.py" will be designed.
    : param template_file : The path of the template file used for the new python library project. If not provided, the default one is used instead.
    : param indent        : The indentation string. If an indentation is given, it will be a number of spaces."""

    # If no project name is provided, use "Python_library" by default.
    if project_name == None:
        project_name = "Python_library"

    # Creating the new project directory
    if not os.path.isdir(project_name):
        os.mkdir(project_name)

# =-------------------------= #
