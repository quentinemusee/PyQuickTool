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
     ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
                                                                         ~*~ CHANGELOG ~*~ """


#=--------------=#
# Import section #
#=--------------=#

from   __future__                                  import annotations
import argparse
from   pyquicktools.pyquicktemplate.module         import new_module
from   pyquicktools.pyquicktemplate.package        import new_package
from   pyquicktools.utils                          import add_group_subparser, build_group_epilog

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
# CLI subparser setup function section #
#=------------------------------------=#

def setup_parser(subparsers: argparse.Action) -> argparse.ArgumentParser:
    """Setup the parser """

    # Defining the software version string.
    version = f"PyQuickTemplate v{__version__} status: {__status__}"

    # Adding the template subparser group.
    template_parser     = add_group_subparser(subparsers, "template", "create, update and manage templates Python projects", version)
    template_subparsers = template_parser.add_subparsers()

    # Adding the new template command parser.
    new_template_subparser = add_group_subparser(template_subparsers, "new", "create a template Python project", version, prefix="template")
    new_template_subparsers = new_template_subparser.add_subparsers()

    # Adding the new module template command parser.
    new_module_template_subparser = add_group_subparser(new_template_subparsers, "module", "create, update and manage a module template Python projects", version, prefix="template new")

    # Adding the new module template arguments
    new_module_template_subparser.add_argument("-a",   "--authors",       type = str, nargs = '+', default = None, help = "setting the Python module authors list")
    new_module_template_subparser.add_argument("-con", "--contact",       type = str,              default = None, help = "setting the Python module contact")
    new_module_template_subparser.add_argument("-cop", "--copyright",     type = str,              default = None, help = "setting the Python module copyright")
    new_module_template_subparser.add_argument("-cr",  "--credits",       type = str, nargs = '+', default = None, help = "setting the Python module credits")
    new_module_template_subparser.add_argument("-da",  "--date",          type = str,              default = None, help = "setting the Python module date")
    new_module_template_subparser.add_argument("-do",  "--docstring",     type = str,              default = None, help = "setting the Python module docstring")
    new_module_template_subparser.add_argument("-f", "-fn",
                                             "--filename", "--file-name", type = str,              default = None, help = "setting the Python module filename to generate")
    new_module_template_subparser.add_argument("-i",   "--indent",        type = str,              default = None, help = "setting the Python module indentation string or number of spaces")
    new_module_template_subparser.add_argument("-im",  "--is-main",     action = "store_true",     default = None, help = "add a main section to the generated Python module")
    new_module_template_subparser.add_argument("-l",   "--license",       type = str,              default = None, help = "setting the Python module licence")
    new_module_template_subparser.add_argument("-m",   "--maintainer",    type = str,              default = None, help = "setting the Python module maintainer")
    new_module_template_subparser.add_argument("-o",   "--organization",  type = str,              default = None, help = "setting the Python module organization")
    new_module_template_subparser.add_argument("-s",   "--status",        type = str,              default = None, help = "setting the Python module status")
    new_module_template_subparser.add_argument("-tf",  "--template-file", type = str,              default = None, help = "setting the Python module custom template file")
    new_module_template_subparser.add_argument("-e",   "--examples",    action = "store_true",     default = None, help = "show examples and exit")
    
    # Setting the new module template function to call
    new_module_template_subparser.set_defaults(func=new_module)

    # Adding the new package template command parser.
    new_package_template_subparser = add_group_subparser(new_template_subparsers, "package", "create, update and manage a package template Python projects", version, prefix="template new")

    # Adding the new package template arguments
    new_package_template_subparser.add_argument("-a",   "--authors",       type = str, nargs = '+', default = None, help = "setting the Python package authors list")
    new_package_template_subparser.add_argument("-con", "--contact",       type = str,              default = None, help = "setting the Python package contact")
    new_package_template_subparser.add_argument("-cop", "--copyright",     type = str,              default = None, help = "setting the Python package copyright")
    new_package_template_subparser.add_argument("-cr",  "--credits",       type = str, nargs = '+', default = None, help = "setting the Python package credits")
    new_package_template_subparser.add_argument("-da",  "--date",          type = str,              default = None, help = "setting the Python package date")
    new_package_template_subparser.add_argument("-do",  "--docstring",     type = str,              default = None, help = "setting the Python package docstring")
    new_package_template_subparser.add_argument("-f", "-fn",
                                            "--filenames", "--file-names", type = str, nargs = '+', default = None, help = "setting the Python package different filenames to generate")
    new_package_template_subparser.add_argument("-i",   "--indent",        type = str,              default = None, help = "setting the Python package indentation string or number of spaces")
    new_package_template_subparser.add_argument("-l",   "--license",       type = str,              default = None, help = "setting the Python package licence")
    new_package_template_subparser.add_argument("-m",   "--maintainer",    type = str,              default = None, help = "setting the Python package maintainer")
    new_package_template_subparser.add_argument("-mf", "--main-file",      type = str,              default = None, help = "setting the Python package main file name")
    new_package_template_subparser.add_argument("-o",   "--organization",  type = str,              default = None, help = "setting the Python package organization")
    new_package_template_subparser.add_argument("-pn", "--project-name",   type = str,              default = None, help = "setting the Python package name")
    new_package_template_subparser.add_argument("-s",   "--status",        type = str,              default = None, help = "setting the Python package status")
    new_package_template_subparser.add_argument("-tf",  "--template-file", type = str,              default = None, help = "setting the Python package custom template file")
    new_package_template_subparser.add_argument("-e",   "--examples",    action = "store_true",     default = None, help = "show examples and exit")

    # Setting the new package template function to call
    new_package_template_subparser.set_defaults(func=new_package)

    # Adding the new library template command parser.
    # new_library_template_subparser = add_group_subparser(new_template_subparsers, "library", "create, update and manage a library template Python projects", version, prefix="template new")

    # Adding the new library template arguments
    # new_library_template_subparser.add_argument("-a",   "--authors",       type = str, nargs = '+', default = None, help = "setting the Python library authors list")
    # new_library_template_subparser.add_argument("-con", "--contact",       type = str,              default = None, help = "setting the Python library contact")
    # new_library_template_subparser.add_argument("-cop", "--copyright",     type = str,              default = None, help = "setting the Python library copyright")
    # new_library_template_subparser.add_argument("-cr",  "--credits",       type = str, nargs = '+', default = None, help = "setting the Python library credits")
    # new_library_template_subparser.add_argument("-da",  "--date",          type = str,              default = None, help = "setting the Python library date")
    # new_library_template_subparser.add_argument("-do",  "--docstring",     type = str,              default = None, help = "setting the Python library docstring")
    # new_library_template_subparser.add_argument("-l",   "--license",       type = str,              default = None, help = "setting the Python library licence")
    # new_library_template_subparser.add_argument("-m",   "--maintainer",    type = str,              default = None, help = "setting the Python library maintainer")
    # new_library_template_subparser.add_argument("-o",   "--organization",  type = str,              default = None, help = "setting the Python library organization")
    # new_library_template_subparser.add_argument("-s",   "--status",        type = str,              default = None, help = "setting the Python library status")
    # new_library_template_subparser.add_argument("-tf",  "--template-file", type = str,              default = None, help = "setting the Python library custom template file")
    # new_library_template_subparser.add_argument("-i",   "--indent",        type = str,              default = None, help = "setting the Python library indentation string or number of spaces")
    # new_library_template_subparser.add_argument("-e",   "--examples",    action = "store_true",     default = None, help = "show examples and exit")

    # Setting the new library template function to call
    #new_library_template_subparser.set_defaults(func=new_library)

    # Adding the new template subparser epilog.
    new_template_subparser.epilog = build_group_epilog(new_template_subparsers)

    # Adding the update template command parser.
    #update_template_subparser = add_group_subparser(template_subparsers, "update", "update a template Python project", version)
    #update_template_subparsers = update_template_subparser.add_subparsers()

    # Adding the template subparser epilog.
    template_parser.epilog        = build_group_epilog(template_subparsers)

    return template_subparsers

# =-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------= #
