#!/usr/bin/env python
# -*- coding: utf-8 *-*


""" ~*~ Docstring ~*~
      PyQuickTest is an experimental python testing
             framework designed to deliver an
    easy-and-quick-to-start python testing mechanism.
    rewrite.py is the file containing the functions
    that allow smart check/ensure rewriting for adding
       explicit and error message when a test fail.               
                                     ~*~ Docstring ~*~

    ~*~ CHANGELOG ~*~
     ____________________________________________________________________________________
    | VERSION |    DATE    |                           CONTENT                           |
    |====================================================================================|
    |         |            | Initial release, including the following features:          |
    |         |            |     -Decorators for test functions.                         |
    |         |            |     -Assertions functions for test functions.               |
    |         |            |     -Testing routine functions for:                         |
    |  0.0.1  | 2023/08/06 |         *A single function.                                 |
    |         |            |         *A given group/subgroup of functions.               |
    |         |            |         *All functions from a given file.                   |
    |         |            |     -Generators functions for random inputs.                |
    |         |            |     -a CLI tool for running tests.                          |
    |------------------------------------------------------------------------------------|
    |         |            | Adding a smart assertion error printing to avoid useless    |
    |  0.1.0  | 2023/08/06 | lines, and a more detailed test session start message that  |
    |         |            | includes informations about the OS & the software versions. |
     ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
                                                                         ~*~ CHANGELOG ~*~ """


#=--------------=#
# Import section #
#=--------------=#

from   __future__      import annotations
import typing
import io
import re
from   pyquicktools.pyquicktest.utils import *

# =-----------------------------------= #


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
__version__      = "0.1.1"

# =--------------------------------------------------------= #


#=------------------------------------=#
# Constants & Global variables section #
#=------------------------------------=#

BS     = '\\'
DQUOTE = '"'
LBRCKT = '{'
RBRCKT = '}'

# =----------------------------------= #


#=-------------------------------------=#
# Parsing & Rewriting functions section #
#=-------------------------------------=#

def smart_assertion_print(
    *values : typing.Any,
    sep     : typing.Optional[str]           = " ",
    end     : typing.Optional[str]           = "\n",
    file    : typing.Optional[typing.TextIO] = None,
    flush   : typing.Literal[False]          = False):
    """Smart print assertions statements without obvious lines."""

    # Printing to a local StringIO object
    output = io.StringIO()
    print(*values, sep=sep, end=end, file=output, flush=flush)
    content = output.getvalue()
    output.close()

    # Making this string smart.
    for line in content.split('\n'):
        # removing A = A in the where statement.
        if '=' in line:
            (A, B) = map1(lambda x: x.replace(' ', "").strip(), line.split('='))
            if A == B:
                content = content.replace('\n' + line, "")

    print(content, file=file)

def parse_function_call(string: str) -> typing.Optional[str]:
    """Parse a single lowest function call from a given string expression."""
    try:
        res = re.findall(r"([\w.]+\(.*?\))", string)[0]
        while True:
            temp = re.findall(r"([\w.]+\(.*?\))", '('.join(e for e in res.split('(')[1:]))
            if temp:
                res = temp[0]
            else:
                break
        return res
    except IndexError:
        return None

def parse_function_calls(string: str) -> typing.Tuple[typing.Dict[str, str], str]:
    """Parse every function call from a given string expression and returns them, their variable name and the resulting string."""
    counter = 1
    out = {}
    res = parse_function_call(string)
    while res:
        arg = f"__GENERATED_ARG_{counter}__"
        out[arg] = res
        counter +=1
        string = string.replace(res, arg)
        res = parse_function_call(string)
    return (out, string)

def rewrite_check(check: str) -> typing.Tuple[typing.Dict[str, str], str]:
    """rewrite a single check instruction, returning it as well as the core rewritten variables."""
    check = check.replace('\n', "")
    tab = get_str_tab(check)
    func = check.split('(')[0].strip()
    (core, res) = parse_function_calls(check.split(func)[-1])
    out = ""
    for key in core:
        out += f"{tab}{key} = {core[key]}\n"
    return (core, out + f"{tab}{func}{res}")

def rewrite_test(test: typing.Callable[[object], object], caller_file : typing.Optional[str] = None) -> typing.Callable[[object], object]:
    """Rewrite a test function."""
    caller_lib = __import__(caller_file.split('/')[-1].split('\\')[-1].split('.')[0])
    for name in dir(caller_lib):
        globals()[name] = getattr(caller_lib, name)
    new_func_name = f"rewritten_{test.__name__}"
    src = test.__rewritten_source__
    src:list[str] = src.replace(test.__name__, new_func_name).split('\n')
    while not src[0].lstrip().startswith("def"):
        src.pop(0)
    src: str = "\n".join(src)
    res: list[str] = re.findall(r"(\s*(ensure|check)\s?\(.*\))", src)
    for check in res:
        temp = check[0].replace('\n', "")
        tab = get_str_tab(temp)
        (core, rewritten) = rewrite_check(temp)
        multi_replaced_values = [multiple_replace(core[key], *[(k, v) for k, v in core.items()], (DQUOTE, BS + DQUOTE)) for key in core]
        maxlength = max([len(e) for e in multi_replaced_values]) if multi_replaced_values else 0
        rewritten = rewritten[:-1].rstrip() + f""", "\\nwhere\\n{(BS + 'n').join(
            f"{tab}{replaced_values_and_key[0]}{(maxlength-len(replaced_values_and_key[0]))*' '} = " 
          + f"{LBRCKT}{replaced_values_and_key[1]}{RBRCKT}" for replaced_values_and_key in zip(multi_replaced_values, core)
        )}")"""
        src = src.replace(temp, rewritten)
    exec(compile(src, test.__code__.co_filename, "exec"))
    return locals()[new_func_name]

# =----------------------------------------------------------------------------------------------------------------------------------------------= #