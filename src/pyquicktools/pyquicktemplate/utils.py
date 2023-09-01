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
import os
import re
from   datetime   import datetime
from   pyquicktools.uutils.uutils     import remove_dupicates, read_file

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

def guard_author(kwargs: typing.Dict[str, typing.List[str] | str | int | None], special_variables: typing.List[str], template: str) -> str:
    """Update the given kwargs context for modifying authors to author if no author of only one is given."""
    if type(kwargs["authors"]) == str:
        kwargs["authors"] = [kwargs["authors"]]
    if kwargs["authors"] == None or len(kwargs["authors"]) == 1:
        kwargs["author"] = kwargs["authors"][0]
        kwargs.pop("authors")
        special_variables.remove("authors")
        special_variables.insert(0, "author")
        template = template.replace("__AUTHORS_", "__AUTHOR_")
    else:
        kwargs["authors"] = remove_dupicates(kwargs["authors"])
        
    return template

def guard_credits(credits: typing.List[str] | None) -> str:
    """Return the credits list without any duplicates."""
    if credits != None:
        credits = remove_dupicates(credits)
    return credits

def guard_date(date: str | None) -> str:
    """Return the current date if the provided one is None."""
    if date == None:
        return datetime.today().strftime('%Y-%m-%d')
    return date

def guard_docstring(docstring: str | None) -> str:
    """Return "Python file docstring." if the provided docstring is None."""
    if docstring == None:
        docstring = "Python file docstring."
    return docstring
    
def guard_filename(filename: str | None) -> str:
    """Return "main.py"" if the provided filename is None, or add an extra ".py" extension if missing."""
    if filename == None:
        filename = "main.py"
    elif filename[-3:] != ".py" and filename[-4:] != ".pyw":
        filename += ".py"
    return filename

def guard_indent(indent: str | int | None) -> str:
    """Return "    " if the given indentation is None or a corresponding number of spaces if indent is an integer."""
    if indent == None:
        indent = "    "
    elif type(indent) == int:
        indent = indent*' '
    return indent

def guard_is_main(is_main: str | bool | None) -> str:
    """Return False if the provided str is None or False or "False"."""
    if is_main == None or str(is_main) == "False":
        is_main = False
    else:
        is_main = True
    return is_main
    
def guard_status(status: str | None) -> str:
    """Return "Development" if the provided status is None."""
    if status == None:
        status = "Development"
    return status
    
def guard_version(version: str | None) -> str:
    """Return "0.0.1" if the provided version is None."""
    if version == None:
        version = "0.0.1"
    return version
    
def guard_template_file(template_file: str | None) -> str:
    """Return the config template file if the template_file provided is None. If this config doesn't exist, return the default template file."""
    if template_file == None:
        template_file = f"{os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))}/.quickpytemplate"
        if not os.path.exists(template_file):
            template_file = f"{os.path.dirname(__file__)}/.default-quickpytemplate"
    return template_file

def parse_kwargs(kwargs: typing.Dict[str, typing.List[str] | str | int | None], tenmplate: str) -> None:
    """Parse the variables defined in the provided template file."""
    for var, value in [var_line.strip().split('=') for var_line in tenmplate.split('\n') if var_line.startswith("%%")]:
        var = var[2:].strip()
        if kwargs.get(var, None) == None:
            kwargs[var] = value.strip().split(',') if ',' in value else value.strip()

def format_kwargs(kwargs: typing.Dict[str, typing.List[str] | str | int | None], tenmplate: str) -> None:
    """Format the given kwargs to fit what's expected for the parse_template function."""
    expected_keywords = ["authors", "contact", "copyright", "credits", "date",
                         "docstring", "filename", "license", "maintainer",
                         "organization", "status", "version", "template_file",
                         "is_main", "indent"]
    for k in expected_keywords:
        if k not in kwargs:
            kwargs[k] = None
    kwargs["template_file"] = guard_template_file(kwargs["template_file"])
    parse_kwargs(kwargs, tenmplate)
    kwargs["credits"]       = guard_credits(kwargs["credits"])
    kwargs["date"]          = guard_date(kwargs["date"])
    kwargs["filename"]      = guard_filename(kwargs["filename"])
    kwargs["status"]        = guard_status(kwargs["status"])
    kwargs["version"]       = guard_version(kwargs["version"])
    kwargs["docstring"]     = guard_docstring(kwargs["docstring"])
    kwargs["indent"]        = guard_indent(kwargs["indent"]) 

def repl_star(template: str, special_variables: typing.List[str]) -> str:
    """Replace any occurence of '*' in the given template with the given list of special variables"""
    if "__*__" in template:
        template = template.replace("__*__", str(special_variables))
    return template

def repl_inits(template: str, kwargs: typing.Dict[str, typing.List[str] | str | int | None]) -> str:
    """Replace any occurence of "INIT" in the given template."""
    maxsize = 0
    for init in re.findall(r"INIT\(__(.*)__\)", template):
        if len(init) > maxsize:
            maxsize = len(init)
    maxfullsize = 0
    for init, var in re.findall(r"(INIT\(__(.*)__\))", template):
        value       = kwargs[var.lower()]
        replacement = f"""\\__{var.lower()}__{(maxsize-len(var))*' '} = {'"' if value != None and type(value) != list else ""}{value}{'"' if value != None and type(value) != list else ""}"""
        if len(replacement) > maxfullsize:
            maxfullsize = len(replacement)
        template = template.replace(init, replacement)
        template = re.sub(r"{{(" + replacement + r")}}", r"\1", template)
    return template.replace("INITS_WIDTH", str(maxfullsize-1))

def repl_var(template: str, kwargs: typing.Dict[str, typing.List[str] | str | int | None]) -> str:
    """Replace any keywords variable with their contextual value."""
    return template.replace("__IS_MAIN__", str(kwargs["is_main"]))

def repl_eval(template: str, kwargs: typing.Dict[str, typing.List[str] | str | int | None]) -> str:
    """Replace any expression to evaluate with its evaluated value."""

    # Creating the pattern replace function.
    def repl_cst(cst: str) -> str:
        """Constant replacement function."""
        cst = cst.lower()
        for k in kwargs:
            if cst == f"__{k}__":
                return f"\"{kwargs[k]}\""
            if cst == f"__{k}_width__":
                return  str(len(kwargs[k]))
        return "None"
    
    # Iterate over the expressions to evaluate.
    for pattern_to_eval in re.findall(r"{{[^}]*}}", template, flags=re.DOTALL):
        save_pattern_to_eval = pattern_to_eval
        for pattern_to_replace in re.findall(r"(?<!\\)(?<!\")(?<!')__[a-zA-Z_][a-zA-Z0-9_]*__(?<!')(?<!\")", pattern_to_eval):
            pattern_to_eval = pattern_to_eval.replace(pattern_to_replace, str(eval(repl_cst(pattern_to_replace))))
        for pattern_to_replace in re.findall(r"(?<!\\)\\(?<!\")(?<!')__[a-zA-Z_][a-zA-Z0-9_]*__(?<!')(?<!\")", pattern_to_eval):
            pattern_to_eval = pattern_to_eval.replace(pattern_to_replace, pattern_to_replace[1:])
        try:
            template = template.replace(save_pattern_to_eval, eval(pattern_to_eval[2:-2]))
        except SyntaxError:
            template = template.replace(save_pattern_to_eval, pattern_to_eval[2:-2])
    return template

def parse_template(**kwargs : typing.List[str] | str | int | None) -> typing.Tuple[str, str]:
    """Parse a template file an apply modifications from the given parameters.
    : param authors       : The authors      of the new python single-file project.
    : param contact       : The contact      of the new python single-file project.
    : param copyright     : The copyright    of the new python single-file project.
    : param credits       : The credits      of the new python single-file project.
    : param date          : The date         of the new python single-file project.
    : param license       : The license      of the new python single-file project.
    : param maintainer    : The maintainer   of the new python single-file project.
    : param organization  : The organization of the new python single-file project.
    : param status        : The status       of the new python single-file project.
    : param version       : The version      of the new python single-file project.
    : param docstring     : The docstring    of the new python single-file project.
    : param filename      : The filename     of the new python single-file project.
    : param template_file : The path of the template file used for the new python single-file project. If not provided, the default one is used instead.
    : param is_main       : True if the template to parse if for a main file.
    : param indent        : The indentation string. If an indentation is given, it will be a number of spaces."""

    # If examples are requested, print examples.
    if kwargs.get("examples", False):
        print("EXAMPLE USEEEE")

    # Reading the template content.
    template = read_file(kwargs["template_file"], encoding="utf-8")

    # Format the kwargs dictionary.
    format_kwargs(kwargs, template)

    # Special variables list
    special_variables = ["authors", "contact", "copyright", "credits", "date",
                         "docstring", "filename", "license", "maintainer",
                         "organization", "status", "version"]

    # Filter the template content by ignoring every file starting with a '%'
    template = '\n'.join(line[1:] if line.startswith("\\%") else line for line in template.split('\n') if not line.startswith('%'))

    # Replacing "authors" by "author" if one or zero author is provided.
    template = guard_author(kwargs, special_variables, template)

    # If the special variable "__*__" is used, replace it by a list containing evey other special variables.
    template = repl_star(template, special_variables)
    
    # Using regex to replace special variables by their initialization line.
    template = repl_inits(template, kwargs)

    # Replace keywords variable with their litteral contextual value.
    template = repl_var(template, kwargs)

    # Using regex to replace expressions to evaluate.
    template = repl_eval(template, kwargs)
    
    # Returning both the filename to create and its template content.
    return kwargs["filename"], template
