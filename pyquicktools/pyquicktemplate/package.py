#!/usr/bin/env python
# -*- coding: utf-8 *-*


""" ~*~ Docstring ~*~
       PyQuickTemplate is a tool designed for allowing
      easy and quick python project template management.
     The "multiple_files.py" file contains functions for
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

def new_package(**kwargs : typing.List[str] | str | int | None) -> None:
    """Create a new python multiple-files project from the given parameters.
    : param authors       : The authors        of the new python multiple-files project.
    : param contact       : The contact        of the new python multiple-files project.
    : param copyright     : The copyright      of the new python multiple-files project.
    : param credits       : The credits        of the new python multiple-files project.
    : param date          : The date           of the new python multiple-files project.
    : param license       : The license        of the new python multiple-files project.
    : param maintainer    : The maintainer     of the new python multiple-files project.
    : param organization  : The organization   of the new python multiple-files project.
    : param status        : The status         of the new python multiple-files project.
    : param version       : The version        of the new python multiple-files project.
    : param docstring     : The docstring      of the new python multiple-files project.
    : param filenames     : The filenames list of the new python multiple-files project.
    : param main_file     : The main file name of the new python multiple-files project. If not provided, "main.py" will be designed.
    : param template_file : The path of the template file used for the new python multiple-files project. If not provided, the default one is used instead.
    : param indent        : The indentation string. If an indentation is given, it will be a number of spaces."""

    # If examples are requested, print examples.
    if kwargs.get("examples", False):
        print("EXAMPLE USEEEE")
        exit()

    # If no filenames list is provided, an empty list is used.
    filenames = kwargs.get("filenames", None)
    if filenames == None:
        filenames = []
    # Otherwise, removing duplicates filenames
    else:
        filenames = filter1(
            lambda x: x+".py" not in filenames and x+".pyw" not in filenames,
            filenames
        )

    # If no "main_file" is provided, "main.py" is used.
    main_file = kwargs.get("main_file", None)
    if main_file == None:
        main_file = "main.py"

    # Adding the main file to the filenames list if not already included.
    if main_file not in filenames:
        filenames.append(main_file)

    # If no project name is provided, use "Python_project" by default.
    project_name = kwargs.get("project_name", None)
    if project_name == None:
        project_name = "Python_project"

    # Creating the new project directory
    if not os.path.isdir(project_name):
        os.mkdir(project_name)

    for filename in filenames:
        # Parsing the template.
        filename, template = parse_template(
            authors       = kwargs.get("authors", None),
            contact       = kwargs.get("contact", None),
            copyright     = kwargs.get("copyright", None),
            credits       = guard_credits(kwargs.get("credits", None)),
            date          = guard_date(kwargs.get("date", None)),
            docstring     = guard_docstring(kwargs.get("docstring", None)),
            filename      = guard_filename(f"{project_name}/{filename}"),
            indent        = guard_indent(kwargs.get("indent", None)),
            is_main       = filename == main_file,
            license       = kwargs.get("license", None),
            maintainer    = kwargs.get("maintainer", None),
            organization  = kwargs.get("organization", None),
            status        = guard_status(kwargs.get("status", None)),
            template_file = guard_template_file(kwargs.get("template_file", None)),
            version       = guard_version(kwargs.get("version", None)),
        )

        # Generating the new Python single-file project.
        write_file(filename, template, encoding="utf-8")

# =-------------------------= #
