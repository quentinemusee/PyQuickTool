#!/usr/bin/env python
# -*- coding: utf-8 *-*


""" ~*~ Docstring ~*~
      PyQuickTemplate is a tool designed for allowing
     easy and quick python project template management.
     The "single_file.py" file contains functions for
    generating and updating python single file projects
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
from   pyquicktools.pyquicktemplate.utils import guard_credits, guard_date, guard_filename, guard_docstring, guard_indent, guard_is_main,  guard_status, guard_version, guard_template_file, parse_template
from   pyquicktools.uutils.uutils         import write_file

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

def new_module(**kwargs : typing.List[str] | str | int | None) -> None:
    """Create a new Python module.
    : param authors       : The authors      of                           the new Python module.
    : param contact       : The contact      of                           the new Python module.
    : param copyright     : The copyright    of                           the new Python module.
    : param credits       : The credits      of                           the new Python module.
    : param date          : The date         of                           the new Python module.
    : param docstring     : The docstring    of                           the new Python module.
    : param filename      : The filename     of                           the new Python module.
    : param indent        : The indentation string or number of spaces of the new Python module.
    : param is_main       : True for adding a main section to             the new Python module.
    : param license       : The license      of                           the new Python module.
    : param maintainer    : The maintainer   of                           the new Python module.
    : param organization  : The organization of                           the new Python module.
    : param status        : The status       of                           the new Python module.
    : param template_file : The template file from which to generate      the new Python module.
    : param version       : The version      of                           the new Python module."""

    # If examples are requested, print examples.
    if kwargs.get("examples", False):
        print("EXAMPLE USEEEE")

    # Parsing the template.
    filename, template = parse_template(
        authors       = kwargs.get("authors", None),
        contact       = kwargs.get("contact", None),
        copyright     = kwargs.get("copyright", None),
        credits       = guard_credits(kwargs.get("credits", None)),
        date          = guard_date(kwargs.get("date", None)),
        docstring     = guard_docstring(kwargs.get("docstring", None)),
        filename      = guard_filename(kwargs.get("filename", None)),
        indent        = guard_indent(kwargs.get("indent", None)),
        is_main       = guard_is_main(kwargs.get("is_main", None)),
        license       = kwargs.get("license", None),
        maintainer    = kwargs.get("maintainer", None),
        organization  = kwargs.get("organization", None),
        status        = guard_status(kwargs.get("status", None)),
        template_file = guard_template_file(kwargs.get("template_file", None)),
        version       = guard_version(kwargs.get("version", None)),
    )

    # Generating the new Python module.
    write_file(filename, template, encoding="utf-8")
    

# =-------------------------= #
