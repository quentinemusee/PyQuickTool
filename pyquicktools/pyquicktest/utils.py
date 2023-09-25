#!/usr/bin/env python
# -*- coding: utf-8 *-*


""" ~*~ Docstring ~*~
      PyQuickTest is an experimental python testing
             framework designed to deliver an
    easy-and-quick-to-start python testing mechanism.
       utils.py is the utility file of the project.             
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

from   __future__ import annotations
import typing
import os
import sys
import inspect

# =------------------------------= #


#=------------------------------------=#
# Constants & Global variables section #
#=------------------------------------=#

CORE = typing.Dict[str, typing.Union[str, typing.Callable[[object], object], typing.Dict[str, 'CORE']]]

# =----------------------------------= #


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


#=-------------------------------------=#
# Require functions & Exception section #
#=-------------------------------------=#

class RequireException(Exception):
    "Raised when a require isn't satisfied and no exception is provided."
    pass

def require(boolean: bool, err: typing.Union[str, Exception] = None, raise_exception: bool = True, file: typing.TextIO = sys.stderr):
    """Rust-style function, evaluate the given boolean <boolean> and raise or print to <file> a given error <err> depending on the given <raise_exception>."""
    if not boolean:
        if raise_exception:
            raise err if type(err) == Exception else RequireException(err)
        print(err, file=file)

# =--------------------------------------------------------------------------------------------------------------------------------------------------------= #


#=-------------------------=#
# Utility functions section #
#=-------------------------=#

def read_file(filename: str) -> str:
    """Read the content of a given file."""
    with open(filename, 'r') as file:
        return file.read()

def map1(func: typing.Callable[[object], object], x: typing.Iterable[object]) -> typing.Iterable[object]:
    """Map the given function over the elements of the given iterable."""
    return type(x)(map(func, x))

def map2(func: typing.Callable[[object], object], x: typing.Iterable[object], y: typing.Iterable[object]) -> typing.Iterable[object]:
    """Map the given function over the elements of the two given iterables."""
    return type(x)(map(lambda arg: func(*arg), zip(x, y)))

def filter1(func: typing.Callable[[object], object], x: typing.Iterable[object]) -> typing.Iterable[object]:
    """Filter the given iterable with the given boolean function."""
    return type(x)(filter(func, x))

def filter2(func: typing.Callable[[object], object], x: typing.Iterable[object], y: typing.Iterable[object]) -> typing.Iterable[object]:
    """Filter the two given iterables with the given boolean function."""
    return type(x)(filter(lambda arg: func(*arg), zip(x, y)))

def hasattributes(object: typing.Any, *attributes: str) -> bool:
    """Check if a given object has every given attributes."""
    return all(map1(lambda x: hasattr(object, x) if not x.startswith("!") else not hasattr(object, x.split('!')[1]), attributes))

def setattributesflags(object: typing.Any, *flags: str) -> typing.Any:
    """Set every given flags attributes to a provided object."""
    map1(lambda x: setattr(object, x, None), flags)
    return object

def setattributes(object: typing.Any, *attributes_and_values: typing.Tuple[str, typing.Any]) -> bool:
    """Set every given attributes and values to a provided object."""
    map1(lambda x: setattr(object, x[0], x[1]), attributes_and_values)
    return object

def get_all_functions(*attributes: str, ctx: typing.Optional[typing.Dict[str, typing.Any]] = None) -> typing.List[typing.Callable[[object], object]]:
    """Returns every functions containing every provided attributes from the given context.
       If no context is provided, then the globals context will be used."""
    if ctx := ctx if ctx != None else globals():
        return filter1(lambda x: callable(x) and hasattributes(x, *attributes), list(ctx.values()) if type(ctx) == dict else ctx)
    return []

def get_callable_ctx_from_file(file: str) -> typing.Dict[str, typing.Callable[[object], object]]:
    """Get the global context of a given file name."""
    sys.path.append(os.path.dirname(file))
    filename   = file.split('/')[-1].split('\\')[-1].split('.')[0]
    src_module = __import__(filename)
    ctx_raw    = dir(src_module)
    return  {e: getattr(src_module, e) for e in ctx_raw if callable(getattr(src_module, e))}

def get_caller_file(stack_nbr: int) -> str:
    """get the last caller file different from the one calling this function."""
    return inspect.stack()[stack_nbr].filename

def merge1(*iterable: typing.List[typing.Any]) -> typing.List[typing.Any]:
    """Merge a lists of element into one list."""
    return () if not iterable else type(iterable[0])(f for e in iterable for f in e)

def merge2(*iterable: typing.List[typing.Any]) -> typing.List[typing.Any]:
    """Merge a lists of lists of element into one list."""
    return () if not iterable else type(iterable[0])(g for e in iterable for f in e for g in f)

def remove_dupicates(list_: typing.List[typing.Any]) -> typing.List[typing.Any]:
    """Remove duplicates element from a given list."""
    return list(dict.fromkeys(list_))

def format_time_unit(time: int, unit: str = "ms") -> str:
    """Format the given time and unit in the most appropriated time unit."""

    # Creating the unit corresponding scale dictionary.
    time_units = {"qs" : 0.000000000000000000000000000001, "rs" : 0.000000000000000000000000001, "ys" : 0.000000000000000000000001,
                  "zs" : 0.000000000000000000001, "as" : 0.000000000000000001, "fs" : 0.000000000000001, "sv" : 0.0000000000001,
                  "ps" : 0.000000000001, "ns" : 0.000000001, "sh" : 0.00000001, "us" : 0.000001, "ms" : 0.001, "cs" : 0.01, "ds" : 0.1,
                  's'  : 1, 'm'  : 60, 'h'  : 3600}
    
    out_time_units = {"qs" : 0.000000000000000000000000000001, "rs" : 0.000000000000000000000000001, "ys" : 0.000000000000000000000001,
                      "zs" : 0.000000000000000000001, "as" : 0.000000000000000001, "fs" : 0.000000000000001, "ps" : 0.000000000001,
                      "ns" : 0.000000001, "us" : 0.000001, "ms" : 0.001, 's'  : 1, 'm'  : 60, 'h'  : 3600}

    # Ensuring the validity of the given unit.
    require(unit in time_units, f"Provided unit {unit} doesn't exist or isn't handled by the <format_time_unit> function.")
    

    # Converting the given time to the seconds unit.
    time_s = time*time_units[unit]

    # The results depends on the value scale.
    if time_s < 1:
        return next(f"{round(time_s/out_time_units[key], 3)}{key}" for key in list(out_time_units.keys())[:-2] if 1 <= time_s/out_time_units[key] < 1000)

    return   f"{round(time_s, 3)}s"                     if 1 <= time_s  < 60 \
        else f"{int(time_s/60)}m{round(time_s%60, 3)}s" if 60 <= time_s < 3600 \
        else f"{int(time_s/3600)}h{int((time_s-3600*int(time_s/3600))/60)}m{round(time_s%60, 3)}s"

def get_str_tab(string: str) -> str:
    """Get the prefix tabulation of a given string <string>."""
    tab = ""
    counter = 0
    while string[counter] == ' ' or string[counter] == '\t':
        tab += string[counter]
        counter += 1
    return tab

def multiple_replace(string: str, *pattern_and_replace: typing.Tuple[str, str]) -> str:
    """Get the prefix tabulation of a given string <string>."""
    for pattern, replace in pattern_and_replace:
        string = string.replace(pattern, replace)
    return string

def compute_group_length(core: CORE) -> int:
    """Compute the length of a given grouped test core hierarchy."""
    
    # Create the length variable.
    length = 0

    # If the core contains functions.
    if "***funcs***" in core:
        # Increment the length variable.
        length += len(core["***funcs***"])

    # For every other groups in the core.
    for group in core:
        if group != "***funcs***":
            # Increment the length variable recursively.
            length += compute_group_length(core[group])
    
    # Return the length.
    return length

# =---------------------------------------------------------------------------------------------------------------------------------------------------= #