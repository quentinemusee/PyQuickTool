#!/usr/bin/env python
# -*- coding: utf-8 *-*


""" ~*~ Docstring ~*~
        PyQuickTest is an experimental python testing
               framework designed to deliver an
      easy-and-quick-to-start python testing mechanism.
       pqt.py is the main file to import when writing a
    test file, but also to use as a CLI tool for testing. 
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

from   __future__           import annotations
import typing
import platform
import os
import time
from pyquicktools.pyquicktest.utils      import *
from pyquicktools.pyquicktest.decorators import *
from pyquicktools.pyquicktest.gen        import *
from pyquicktools.pyquicktest.assertions import *
from pyquicktools.pyquicktest.rewrite    import *

# =----------------------------------------= #


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
NL     = '\n'
SQUOTE = '\''
DQUOTE = '"'
LBRCKT = '{'
RBRCKT = '}'

# =----------------------------------= #


#=----------------------------=#
# Main testing routine section #
#=----------------------------=#

def test_one(
        test_func   : typing.Callable[[object], object],
        prefix      : str = "",
        indent      : typing.Union[str, int] = 0,
        caller_file : typing.Optional[str] = None,
        from_all    : bool = False,
        from_group  : bool = False
    ) -> typing.List[str]:
    """Run a single test."""

    # Declaring and updating required variables.
    res = []
    indent = indent*' ' if type(indent) == int else indent

    # Retrieving the caller file if required
    caller_file = caller_file if caller_file else get_caller_file(5 if from_all else 4 if from_group else 2)

    # Forcing the execution number property.
    if not hasattr(test_func, "test_execnbr"):
        test_func.test_execnbr = 1
    
    # Rewriting the function for pertinent check testing messages
    rewritten_func = rewrite_test(test_func, caller_file=caller_file)

    # Pretty printing.
    print(prefix, end="")
    print(f"Running the test \"{test_func.__name__}\"...")
    print(f"""{indent}\033[90m{((len(prefix)-len(indent)-11)*'>' + ' ') if len(prefix)-len(indent)-11 > 0 else ""}{test_func.__doc__}\033[00m""")

    # Creating a function timer variable
    func_time = time.perf_counter_ns()

    # Creating a success counter variable.
    success_counter = 0

    # Compute the clear str
    clear_str = 100*' '

    # Executing the test functions <test_execnbr> times.
    for i in range(test_func.test_execnbr):
        # Trying to execute the function.
        try:
            # Executing the functions. An exception should be raised through the different validator functions.
            rewritten_func()

            # If the code continue, then no exception has been raised. This isn't normal, it means that any validator functions has been used.
            raise TestFailedException(f"Test function <{test_func.__name__}> didn't use a validator function.")
        
        # If the test passed.
        except TestPassedException:
            # Incrmementing the success counter and pretty printing if no tests failed so far.
            success_counter += 1
            if not res:
                print(clear_str, end="\r", flush=True)
                print(f"{indent}\033[92m[{i+1}{(len(str(test_func.test_execnbr))-len(str(i+1)))*' '}/{test_func.test_execnbr}]",
                      f"passed! ({100*success_counter/test_func.test_execnbr}%)", 
                      f"""[{format_time_unit((time.perf_counter_ns() - func_time), unit="ns")}]\033[00m""", end="\r", flush=True)
        
        # If the test failed.
        except (TestFailedException, TestInvalidException, TestTimeoutException) as e:
            # Pretty printing.
            print(f"{indent}\033[91m[{i+1}{(len(str(test_func.test_execnbr))-len(str(i+1)))*' '}/{test_func.test_execnbr}] failed!\033[00m")
            print(f"""\033[93m{NL.join(e for e in test_func.__source__.split(NL) if not e.lstrip().startswith('@'))}\033[00m""")
            smart_assertion_print(f"\033[91m{e}\033[00m")
            print(os.get_terminal_size()[0]*"~")
            
            # Updating the result.
            res = [test_func.__name__]

    # If all tests passed.
    if not res:
        # Printing the function time without flushing to save the last line printed.
        print(f"{indent}\033[92m[{test_func.test_execnbr}{(len(str(test_func.test_execnbr))-len(str(i+1)))*' '}/{test_func.test_execnbr}]",
              f"passed!    (100%)",
              f"""[{format_time_unit((time.perf_counter_ns() - func_time), unit="ns")}]\033[00m""")
    
    # If some tests failed.
    else:
        # Printing the function time in a new line.
        print(f"{indent}\033[91m({100*success_counter/test_func.test_execnbr}%)",
              f"""[{format_time_unit((time.perf_counter_ns() - func_time), unit="ns")}]\033[00m""")
    
    # Returning the result.
    return res

def test_groups_core(
        core        : CORE,
        last_group  : str = "",
        indent      : typing.Union[str, int] = 0,
        caller_file : typing.Optional[str] = None,
        from_all    : bool = False
    ) -> typing.List[str]:
    """Run grouped tests."""

    # Normalizing the indent.
    indent = indent*' ' if type(indent) == int else indent

    # Retrieving the caller file if required
    caller_file = caller_file if caller_file else get_caller_file(4 if from_all else 2)

    # Creating the result variable
    res = []

    # Creating a group timer variable
    group_time = time.perf_counter_ns()

    # For every group.
    for group in core:
        # Functions aren't groups.
        if group == "***funcs***":
            continue

        # Computing the group length.
        length = compute_group_length(core[group])

        # Pretty printing.
        if border_length := 21 + len(group) + len(str(length)):
            print(f"\033[95m{indent}·{border_length*'_'}·\n{indent}| Running all {length} {group} tests |\n{indent}·{border_length*'‾'}·\033[00m")

        # Incrementing the res by calling recursively the test_groups_core function.
        res += test_groups_core(core[group], group, indent=indent+4*' ', caller_file=caller_file)

    # If this group contains functions.
    if "***funcs***" in core:
        # Retrieving the number of functions in the current group.
        group_length = len(core["***funcs***"])

        # Calling the ungrouped testing function.
        temp = merge2(
            map2(
                lambda x, y: test_one(x, prefix=f"""{indent}[{y}/{group_length}] """, indent=indent, caller_file=caller_file, from_all=from_all, from_group=True),
                core["***funcs***"],
                list(range(1, group_length+1))
            )
        )

        # Updating the group timer value.
        group_time_str = format_time_unit((time.perf_counter_ns() - group_time), unit="ns")

        # If all grouped tests passed.
        if not temp:
            # Pretty printing.
            if border_length := 31 + len(str(group_length)) + len(last_group) + len(group_time_str):
                print(f"\033[95m{indent[:-4]}·{border_length*'_'}·\n{indent[:-4]}| All {group_length} {last_group} tests",
                      f"passed! (100%)",
                      f"[{group_time_str}] |\n{indent[:-4]}·{border_length*'‾'}·\033[00m")
        
        # If some tests failed.
        else:
            # Pretty printing.
            group_success_rate = round(100*(group_length-len(temp))/group_length, 3)
            if border_length := 29 + len(group_time_str) + len(str(group_success_rate)):
                print(f"\033[91m{indent[:-4]}·{border_length*'='}·\n{indent[:-4]}|| Some tests",
                      f"failed! ({group_success_rate}%)",
                      f"[{group_time_str}] ||\n{indent[:-4]}·{border_length*'='}·\033[00m")
                print(f"""\033[91m{indent[:-4]}{", ".join(temp)}\033[00m\n""")

        # Incrementing the res by the just called ungrouped testing function.
        res += [temp]

    # Returning the result.
    return res

def test_group(
        *group   : str,
        ctx      : typing.Optional[typing.Dict[str, typing.Any]] = None,
        filename : typing.Optional[str] = None,
        from_all : bool = False,
        run_dir  : typing.Optional[str] = None,
    ) -> typing.List[str]:
    """Run a group of tests."""

    # Retrieve the ctx value if required.
    caller_file = filename if filename else get_caller_file(3 if from_all else 2)
    ctx = ctx if ctx != None else get_callable_ctx_from_file(caller_file) if caller_file != None else globals()
    # If the global context contains some test functions to execute.
    if test_funcs := get_all_functions("test", ctx=ctx if ctx != None else globals()):
        # Retrieving the grouped test functions.
        group_test_funcs = sorted(get_all_functions("test", "test_group", ctx=ctx if ctx != None else globals()), key=lambda x: x.__getattribute__("test_group"))

        # Retrieving the different grouped test values.
        groups = map1(lambda x: x.__getattribute__("test_group"), filter1(lambda x: hasattr(x, "test_group"), group_test_funcs))
    
        # Constructing the core dictionary for grouped test functions hierarchy.
        core   = {}
        for i, e in enumerate(groups):
            if e[0] not in core:
                core[e[0]] = {}
            temp = core[e[0]]
            for f in e[1:]:
                if f not in temp:
                    temp[f] = {}
                temp = temp[f]
            ref = eval(f"""core{"".join(f"[e[{k}]]" for k in range(len(e)-1))}""")
            if "***funcs***" not in ref[e[-1]]:
                ref[e[-1]]["***funcs***"]  = [group_test_funcs[i]]
            else:
                ref[e[-1]]["***funcs***"] += [group_test_funcs[i]]

        # Diving into the core dictionary
        core = eval("core" + "".join(f"[\"{e}\"]" for e in group))

        # Get the group length.
        length = len(test_funcs)

        # Retrieving the ungrouped test functions list.
        no_groups = filter1(lambda x: not hasattr(x, "test_group"), test_funcs)

        # Pretty printing.
        stdout_width = (os.get_terminal_size()[0] -22)/2
        if border_length := 22 + len(str(length)):
            print(f"\033[01m\033[47m\033[90m{int(stdout_width+0.5)*'='} test sessions starts {int(stdout_width)*'='}\033[00m")
            print(f"platform {platform.platform()}, Python v{platform.python_version()}, PyQuickTest v{__version__} [{__status__}]")
            print(f"Working file: {caller_file}" if not run_dir else f"Working dir: {run_dir}")
            print(f"""Collected {length} test{'s' if length > 1 else ""} to run\n""")
            print(f"\033[96m{border_length*'*'}\n* Running all {length} tests *\n{border_length*'*'}\033[00m\n")

        # Creating a global timer variable
        total_time = time.perf_counter_ns()

    # If the global context contains no  test functions to execute.
    else:
        print("\033[91mNo tests functions to execute.\033[00m")
        return

    try:            
        # Calling the grouped and ungrouped testing functions.
        res = merge2(test_groups_core(core, indent=4, caller_file=caller_file)
                     + map1(lambda x: test_one(x, prefix=4*" ", indent=4, caller_file=caller_file, from_all=from_all, from_group=True), no_groups))

        # Updating the global timer value and the terminal width to use.
        total_time = format_time_unit((time.perf_counter_ns() - total_time), unit="ns")
        stdout_width = (os.get_terminal_size()[0] -26 -len(str(total_time)))/2

        # If all tests passed.
        if not res:
            # Pretty printing.
            if border_length := 32 + len(str(length)) + len(total_time):
                print(f"\n\033[96m{border_length*'*'}\n* All {length} tests",
                    f"passed! (100%)",
                    f"[{total_time}] *\n{border_length*'*'}\033[00m\n")
        
        # If some tests failed.
        else:
            # Pretty printing.
            group_success_rate = round(100*(length-len(res))/length, 3)
            if border_length := 29 + len(str(group_success_rate)) + len(total_time):
                print(f"\n\033[91m{border_length*'*'}\n* Some tests",
                    f"failed! ({group_success_rate}%)",
                    f"[{total_time}] *\n{border_length*'*'}\033[00m\n")
                print(f"""\033[91m{", ".join(res)}\033[00m\n""")

        # Pretty printing.
        print(f"\033[01m\033[47m\033[90m{int(stdout_width+0.5)*'='} test sessions ended in {total_time}s {int(stdout_width)*'='}\033[00m")
    
    except KeyboardInterrupt:
        # Updating the global timer value and the terminal width to use.
        total_time = format_time_unit((time.perf_counter_ns() - total_time), unit="ns")
        stdout_width = (os.get_terminal_size()[0] -26 -len(str(total_time)))/2

        # Pretty printing.
        print("\n\n\033[01mTests interrupted!\033[00m")
        print(f"\033[01m\033[47m\033[90m{int(stdout_width+0.5)*'='} test sessions ended in {total_time}s {int(stdout_width)*'='}\033[00m")

def test_file(ctx: typing.Optional[typing.Dict[str, typing.Any]] = None, filename: typing.Optional[str] = None) -> None:
    """Run all tests from a given file."""
    test_group(ctx=ctx, filename=filename, from_all=True)

def test_directory(ctx: typing.Optional[typing.Dict[str, typing.Any]] = None, path: typing.Optional[str] = None) -> None:
    """Run all tests from a given directory."""
    for filename in os.listdir(path):
        if filename.endswith(".py") or filename.endswith(".pyw"):
            test_file(ctx=ctx, filename=f"{os.path.abspath(path)}/{filename}")

# =---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------= #

