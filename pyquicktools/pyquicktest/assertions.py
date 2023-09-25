#!/usr/bin/env python
# -*- coding: utf-8 *-*


""" ~*~ Docstring ~*~
      PyQuickTest is an experimental python testing
             framework designed to deliver an
    easy-and-quick-to-start python testing mechanism.
        assertion.py is the file containing every
        assertions functions, useful for the tests.
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
import inspect

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
__version__      = "0.1.1"

# =----------------------------= #


#=------------------------------------=#
# Constants & Global variables section #
#=------------------------------------=#

NL     = '\n'
DQUOTE = '"'

# =----------------------------------= #


#=-------------------------------=#
# ValiAssertion functions section #
#=-------------------------------=#

class TestPassedException(Exception):
    "Raised when a test passed."
    pass

class TestFailedException(Exception):
    "Raised when a test failed."
    pass

class TestInvalidException(Exception):
    "Raised when a test is raise an unexpected exception."
    pass

class TestTimeoutException(Exception):
    "Raised when a test is timeout."
    pass

def ok() -> TestPassedException:
    """Validate a test."""
    raise TestPassedException

def ko(error_msg: str = "") -> TestFailedException:
    """Unvalidate a test."""
    stack = inspect.stack()[1]
    raise TestFailedException(f"""{stack.filename}:{stack.function[10:]}:{stack.lineno}: {"".join([error_msg] + list(args))}""")

def check(boolean: bool, error_msg: str = "", *args: str, ensure: bool = False) -> typing.Optional[TestFailedException]:
    """Unvalidate a test if the given <boolean> value is False, but otherwise does nothing."""
    if not boolean:
        stack = next(
            (e for e in inspect.stack()[1:] if e.function not in ["ensure"])
        )
        raise TestFailedException(f"""{stack.filename}:{stack.function[10:]}:{stack.lineno}: {"".join([error_msg] + list(args))}""")
    if ensure:
        ok()

def ensure(boolean: bool, error_msg: str = "", *args: str) -> typing.Union[TestPassedException, TestFailedException]:
    """Validate a test depending on the given <boolean> value."""
    check(boolean, error_msg, *args, ensure=True)

def check_eq(x: typing.Any, y: typing.Any, error_msg: str = "", ensure: bool = False) -> typing.Optional[TestFailedException]:
    """Unvalidate a test depending on the following boolean expression: <x> == <y>."""
    try:
        if not x == y:
            stack = next(
                (e for e in inspect.stack() if e.filename.split('/')[-1].split('\\')[-1] != __file__.split('/')[-1].split('\\')[-1])
            )
            raise TestFailedException(stack.filename.split('/')[-1].split('\\')[-1] + f":{stack.lineno}: {error_msg}\n|    where {x} == {y}")
    except Exception as e:
        raise TestInvalidException(e)
    if ensure:
        ok()

def ensure_eq(x: typing.Any, y: typing.Any,  error_msg: str = "") -> typing.Union[TestPassedException, TestFailedException]:
    """Validate or unvalidate a test depending on the following boolean expression: <x> == <y>."""
    check_eq(x, y, error_msg, ensure=True)
# Explicit aliasing for avoiding possibly warning generate by some IDEs.
eq = ensure_eq
    
def check_neq(x: typing.Any, y: typing.Any, error_msg: str = "", ensure: bool = False) -> typing.Optional[TestFailedException]:
    """Unvalidate a test depending on the following boolean expression: <x> != <y>."""
    try:
        if not x != y:
            stack = next(
                (e for e in inspect.stack() if e.filename.split('/')[-1].split('\\')[-1] != __file__.split('/')[-1].split('\\')[-1])
            )
            raise TestFailedException(stack.filename.split('/')[-1].split('\\')[-1] + f":{stack.lineno}: {error_msg}\n|    where {x} != {y}")
    except Exception as e:
        raise TestInvalidException(e)
    if ensure:
        ok()

def ensure_neq(x: typing.Any, y: typing.Any,  error_msg: str = "") -> typing.Union[TestPassedException, TestFailedException]:
    """Validate or unvalidate a test depending on the following boolean expression: <x> != <y>."""
    check_neq(x, y, error_msg, ensure=True)
# Explicit aliasing for avoiding possibly warning generate by some IDEs.
neq = ensure_neq

def check_lt(x: typing.Any, y: typing.Any, error_msg: str = "", ensure: bool = False) -> typing.Optional[TestFailedException]:
    """Unvalidate a test depending on the following boolean expression: <x> < <y>."""
    try:
        if not x < y:
            stack = next(
                (e for e in inspect.stack() if e.filename.split('/')[-1].split('\\')[-1] != __file__.split('/')[-1].split('\\')[-1])
            )
            raise TestFailedException(stack.filename.split('/')[-1].split('\\')[-1] + f":{stack.lineno}: {error_msg}\n|    where {x} < {y}")
    except Exception as e:
        raise TestInvalidException(e)
    if ensure:
        ok()

def ensure_lt(x: typing.Any, y: typing.Any,  error_msg: str = "") -> typing.Union[TestPassedException, TestFailedException]:
    """Validate or unvalidate a test depending on the following boolean expression: <x> < <y>."""
    check_lt(x, y, error_msg, ensure=True)
# Explicit aliasing for avoiding possibly warning generate by some IDEs.
lt = ensure_lt

def check_le(x: typing.Any, y: typing.Any, error_msg: str = "", ensure: bool = False) -> typing.Optional[TestFailedException]:
    """Unvalidate a test depending on the following boolean expression: <x> <= <y>."""
    try:
        if not x <= y:
            stack = next(
                (e for e in inspect.stack() if e.filename.split('/')[-1].split('\\')[-1] != __file__.split('/')[-1].split('\\')[-1])
            )
            raise TestFailedException(stack.filename.split('/')[-1].split('\\')[-1] + f":{stack.lineno}: {error_msg}\n|    where {x} <= {y}")
    except Exception as e:
        raise TestInvalidException(e)
    if ensure:
        ok()

def ensure_le(x: typing.Any, y: typing.Any,  error_msg: str = "") -> typing.Union[TestPassedException, TestFailedException]:
    """Validate or unvalidate a test depending on the following boolean expression: <x> <= <y>."""
    check_le(x, y, error_msg, ensure=True)
# Explicit aliasing for avoiding possibly warning generate by some IDEs.
le = ensure_le

def check_gt(x: typing.Any, y: typing.Any, error_msg: str = "", ensure: bool = False) -> typing.Optional[TestFailedException]:
    """Unvalidate a test depending on the following boolean expression: <x> > <y>."""
    try:
        if not x > y:
            stack = next(
                (e for e in inspect.stack() if e.filename.split('/')[-1].split('\\')[-1] != __file__.split('/')[-1].split('\\')[-1])
            )
            raise TestFailedException(stack.filename.split('/')[-1].split('\\')[-1] + f":{stack.lineno}: {error_msg}\n|    where {x} > {y}")
    except Exception as e:
        raise TestInvalidException(e)
    if ensure:
        ok()

def ensure_gt(x: typing.Any, y: typing.Any,  error_msg: str = "") -> typing.Union[TestPassedException, TestFailedException]:
    """Validate or unvalidate a test depending on the following boolean expression: <x> > <y>."""
    check_gt(x, y, error_msg, ensure=True)
# Explicit aliasing for avoiding possibly warning generate by some IDEs.
gt = ensure_gt

def check_ge(x: typing.Any, y: typing.Any, error_msg: str = "", ensure: bool = False) -> typing.Optional[TestFailedException]:
    """Unvalidate a test depending on the following boolean expression: <x> >= <y>."""
    try:
        if not x >= y:
            stack = next(
                (e for e in inspect.stack() if e.filename.split('/')[-1].split('\\')[-1] != __file__.split('/')[-1].split('\\')[-1])
            )
            raise TestFailedException(stack.filename.split('/')[-1].split('\\')[-1] + f":{stack.lineno}: {error_msg}\n|    where {x} >= {y}")
    except Exception as e:
        raise TestInvalidException(e)
    if ensure:
        ok()

def ensure_ge(x: typing.Any, y: typing.Any,  error_msg: str = "") -> typing.Union[TestPassedException, TestFailedException]:
    """Validate or unvalidate a test depending on the following boolean expression: <x> >= <y>."""
    check_ge(x, y, error_msg, ensure=True)
# Explicit aliasing for avoiding possibly warning generate by some IDEs.
ge = ensure_ge

def check_and(x: typing.Any, y: typing.Any, error_msg: str = "", ensure: bool = False) -> typing.Optional[TestFailedException]:
    """Unvalidate a test depending on the following boolean expression: <x> and <y>."""
    try:
        if not x and y:
            stack = next(
                (e for e in inspect.stack() if e.filename.split('/')[-1].split('\\')[-1] != __file__.split('/')[-1].split('\\')[-1])
            )
            raise TestFailedException(stack.filename.split('/')[-1].split('\\')[-1] + f":{stack.lineno}: {error_msg}\n|    where {x} and {y}")
    except Exception as e:
        raise TestInvalidException(e)
    if ensure:
        ok()

def ensure_and(x: typing.Any, y: typing.Any,  error_msg: str = "") -> typing.Union[TestPassedException, TestFailedException]:
    """Validate or unvalidate a test depending on the following boolean expression: <x> and <y>."""
    check_and(x, y, error_msg, ensure=True)
# Explicit aliasing for avoiding possibly warning generate by some IDEs.
and_ = ensure_and

def check_or(x: typing.Any, y: typing.Any, error_msg: str = "", ensure: bool = False) -> typing.Optional[TestFailedException]:
    """Unvalidate a test depending on the following boolean expression: <x> or <y>."""
    try:
        if not x or y:
            stack = next(
                (e for e in inspect.stack() if e.filename.split('/')[-1].split('\\')[-1] != __file__.split('/')[-1].split('\\')[-1])
            )
            raise TestFailedException(stack.filename.split('/')[-1].split('\\')[-1] + f":{stack.lineno}: {error_msg}\n|    where {x} or {y}")
    except Exception as e:
        raise TestInvalidException(e)
    if ensure:
        ok()

def ensure_or(x: typing.Any, y: typing.Any,  error_msg: str = "") -> typing.Union[TestPassedException, TestFailedException]:
    """Validate or unvalidate a test depending on the following boolean expression: <x> or <y>."""
    check_or(x, y, error_msg, ensure=True)
# Explicit aliasing for avoiding possibly warning generate by some IDEs.
or_ = ensure_or

def check_band(x: typing.Any, y: typing.Any, error_msg: str = "", ensure: bool = False) -> typing.Optional[TestFailedException]:
    """Unvalidate a test depending on the following boolean expression: <x> & <y>."""
    try:
        if not x & y:
            stack = next(
                (e for e in inspect.stack() if e.filename.split('/')[-1].split('\\')[-1] != __file__.split('/')[-1].split('\\')[-1])
            )
            raise TestFailedException(stack.filename.split('/')[-1].split('\\')[-1] + f":{stack.lineno}: {error_msg}\n|    where {x} & {y}")
    except Exception as e:
        raise TestInvalidException(e)
    if ensure:
        ok()

def ensure_band(x: typing.Any, y: typing.Any,  error_msg: str = "") -> typing.Union[TestPassedException, TestFailedException]:
    """Validate or unvalidate a test depending on the following boolean expression: <x> & <y>."""
    check_band(x, y, error_msg, ensure=True)
# Explicit aliasing for avoiding possibly warning generate by some IDEs.
band = ensure_band

def check_bor(x: typing.Any, y: typing.Any, error_msg: str = "", ensure: bool = False) -> typing.Optional[TestFailedException]:
    """Unvalidate a test depending on the following boolean expression: <x> | <y>."""
    try:
        if not x | y:
            stack = next(
                (e for e in inspect.stack() if e.filename.split('/')[-1].split('\\')[-1] != __file__.split('/')[-1].split('\\')[-1])
            )
            raise TestFailedException(stack.filename.split('/')[-1].split('\\')[-1] + f":{stack.lineno}: {error_msg}\n|    where {x} | {y}")
    except Exception as e:
        raise TestInvalidException(e)
    if ensure:
        ok()

def ensure_bor(x: typing.Any, y: typing.Any,  error_msg: str = "") -> typing.Union[TestPassedException, TestFailedException]:
    """Validate or unvalidate a test depending on the following boolean expression: <x> | <y>."""
    check_bor(x, y, error_msg, ensure=True)
# Explicit aliasing for avoiding possibly warning generate by some IDEs.
bor = ensure_bor

# =---------------------------------------------------------------------------------------------------= #