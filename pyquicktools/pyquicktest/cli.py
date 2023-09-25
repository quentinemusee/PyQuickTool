#!/usr/bin/env python
# -*- coding: utf-8 *-*


""" ~*~ Docstring ~*~
        PyQuickTest is an experimental python testing
               framework designed to deliver an
      easy-and-quick-to-start python testing mechanism.
       cli.py is the command line interface tool file
       for starting test by wimply calling this script. 
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

from   __future__                    import annotations
from   pyquicktools.utils            import add_group_subparser
from   pyquicktools.pyquicktest.test import test_directory, test_file
import typing
import os
import argparse

# =----------------------------------------------------= #


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

# =-------------------------------------------------= #


#=------------------------------------=#
# CLI subparser setup function section #
#=------------------------------------=#

def setup_parser(subparsers: argparse.Action) -> argparse.ArgumentParser:
    """Setup the parser """

    # Defining the software version string.
    version = f"PyQuickTest v{__version__} status: {__status__}"

    # Adding the test subparser group.
    test_parser     = add_group_subparser(subparsers, "test", "test python project with an easy to deploy testing framework", version)

    # Adding the new module test arguments
    test_parser.add_argument("-e", "--example", action = "store_true", default = None, help = "give examples and instructions to get started.")
    test_parser.add_argument("-p", "--path",    type = str,            default = '.' , help = "path of the file or directory to test")

    # Setting the new module test function to call
    test_parser.set_defaults(func=cli_test)

    return test_parser


def cli_test(**kwargs : typing.Dict[str, typing.List[str] | str | int | None]) -> None:
    """PyQuickTest CLI function.
    : path                : The path of the test file or directory to test."""

    # If the -e or --example argument is provided, print examples and instructions to get started and exit the program.
    if kwargs["example"]:
        print("""\
*========================================================================================*
|                  :PyQuickTest test kit is divided into few categories:                 |
| -------------------------------------------------------------------------------------- |
| Decorators :                                                                           |
|     is_test : Transform the decorated function into a test function for the framework. |
|         example :                                                                      |
|                   def my_function(): | is not                                          |
|                       ok()           | a test                                          |
|                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~                                          |
|                   @is_test()         |  is                                             |
|                   def my_function(): |  a                                              |
|                       ok()           | test                                            |
|     ********************************************************************************** |
|     qpt_group : Categorize the decorated function as belonging to the given groups and |
|                      subgroups. Groups and subgroups should be given as arguments.     |
|         example :                                                                      |
|                   @is_test()         |     has                                         |
|                   def my_function():a|     no                                          |
|                       ok()           | test group                                      |
|                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                                      |
|                   @is_test()          |  belong                                        |
|                   @qpt_group("Group") | to the                                         |
|                   def my_function():  |  group                                         |
|                       ok()            | "Group"                                        |
|                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                                        |
|                   @is_test()                      |   belong to the                    |
|                   @qpt_group("Group", "Subgroup") |   group "Group"                    |
|                   def my_function():              | and the subgroup                   |
|                       ok()                        |    "Subgroup"                      |
|     ********************************************************************************** |
|     qpt_execnbr : Order the decorated test function to be run a given number of times. |
|         example :                                                                      |
|                   @is_test()         |     runs                                        |
|                   def my_function(): |     once                                        |
|                       ok()           | my_function                                     |
|                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                                     |
|                   @is_test()         |    runs                                         |
|                   @qpt_execnbr(100)  |    100                                          |
|                   def my_function(): |    times                                        |
|                       ok()           | my_function                                     |
|     ********************************************************************************** |
|     qpt_parametrize : Use the given parameters to the test function.                   |
|         example :                                                                      |
|                   @is_test()            |   will fail                                  |
|                   def my_function(arg): |   because no                                 |
|                       ok()              | "arg" provided                               |
|                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                               |
|                   @is_test()            | test                                         |
|                   @qpt_parametrize(8)   | with                                         |
|                   def my_function(arg): | arg                                          |
|                       ok()              | = 8                                          |
|                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~                                         |
|                   @is_test()                         | test with                       |
|                   @qpt_parametrize(8, 'a', [45.19])  | arg1 = 8                        |
|                   def my_function(arg1, arg2, arg3): | arg2 = 'a'                      |
|                       ok()                           | arg3 = [45.19]                  |
| -------------------------------------------------------------------------------------- |
| Assertion functions:                                                                   |
|     ok : Validate the current test.                                                    |
|         example :                                                                      |
|                   @is_test()            |  This                                        |
|                   def my_function(arg): |  test                                        |
|                       ok()              | passes                                       |
|     ********************************************************************************** |
|     ko : Unvalidate the current test with an optional error message.                   |
|         example :                                                                      |
|                   @is_test()                  | This                                   |
|                   def my_function(arg):       | test                                   |
|                       ko("This test failed!") | fail                                   |
|     ********************************************************************************** |
|     check :   Unvalidate the current test if the given boolean is False. An optional   |
|              error message can be provided. If the given boolean is True, do nothing.  |
|         example :                                                                      |
|                   @is_test()                                   |      if the           |
|                   def my_function(arg):                        | generated number      |
|                       a = gen_int()                            | a is lower than       |
|                       check(a > 10, "a isn't greater than 10") |   10, the tests       |
|                       ok()                                     |     will fail.        |
|     ********************************************************************************** |
|     ensure :  Validate or unvalidate the current test depending on the given boolean.  |
|                             An optional error message can be provided.                 |
|         example :                                                                      |
|                   @is_test()                                    |   if the generated   |
|                   def my_function(arg):                         | number a is greater  |
|                       a = gen_int()                             | than 10, the tests   |
|                       ensure(a > 10, "a isn't greater than 10") |      will pass       |
|                                                                 | (otherwise it fails) |
| -------------------------------------------------------------------------------------- |
| Generator functions                                                                    |
|     gen_none               : Generate None.                                            |
|     gen_bool               : Generate a random boolean.                                |
|     gen_int                : Generate a random integer. Min and max can be provided.   |
|     gen_signed_int         : Generate a random signed integer. Min / max can be given. |
|     gen_float              : Generate a random float.                                  |
|     gen_signed_float       : Generate a random signed float. Min and max can be given. |
|     gen_ascii_lower_char   : Generate a random ascii lower char.                       |
|     gen_ascii_upper_char   : Generate a random ascii upper char.                       |
|     gen_ascii_char         : Generate a random ascii char.                             |
|     gen_ascii_lower_string : Generate a random ascii lower string.                     |
|     gen_ascii_upper_string : Generate a random ascii upper string.                     |
|     gen_ascii_string       : Generate a random ascii string.                           |
|     gen_callable           : Generate a random callable. The number of arguments can   |
|                              be specified with nbr_args, as well as the generator      |
|                              function for the returned value with gen_return. If       |
|                              raised_exception = True, then the callable will raise an  |
|                              exception.                                                |
|     gen_generator          : Generate a random iterator. The iterator length can be    |
|                              provided, as well as the elements generator function with |
|                              the gen_element argument.                                 |
|     gen_list               : Generate a random list. The list length can be provided,  |
|                              as well as the elements generator function with the       |
|                              the gen_element argument.                                 |
|     gen_dict               : Generate a random dict. The dict length can be provided,  |
|                              as well as the keys generator function with the           |
|                              the gen_keys argument, and the element generator function |
|                              with the gen_element argument.                            |
|     gen_random_value       : Generate a random value from any single value generator   |
|                              decorated with the "is_gen_value" flag attribute.         |
|     gen_random_iterable    : Generate a random iterable from any iterable generator    |
|                              decorated with the "is_gen_iterable" flag attribute.      |
|     gen_random             : Generate a random data from any generator decorated with  |
|                              the "is_gen" flag attribute.                              |
| -------------------------------------------------------------------------------------- |
| Testing functions                                                                      |
|     test_one(                                                                          |
|         test_func   : The test function to run.                                        |
|         prefix      : An optional prefix string to print before the test result.       |
|         indent      : The test result output indentation level. Can be a number of     |
|                                     spaces or a specific string.                       |
|         caller_file : The path to the caller file. Can be None, in this case the file  |
|                        is retrieve using the inspect module. Please leave it as None.  |
|     )                                                                                  |
|      -> Run a single test function <test_func>.                                        |
|         A few optional arguments can be provided, but if this function is directly     |
|         used alone, only passing the test function as a parameter is certainly enough. |
|                                                                                        |
|         example :                                                                      |
|                   test_one(my_function) | This will run the test function my_function. |
|                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ |
|                   test_one(        |     This will run the test                        |
|                       my_function, |  function my_function with a                      |
|                       prefix="==>" |      printed prefix "==>"                         |
|                   )                | before the test result output.                    |
|                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ |
|                   test_one(        |     This will run the test                        |
|                       my_function, |  function my_function with an                     |
|                       prefix="==>" |  indentation of 4 spaces and a                    |
|                       indent=4     |      printed prefix "==>"                         |
|                   )                | before the test result output.                    |
|     ********************************************************************************** |
|     test_group(                                                                        |
|         *group   : The group to test. Can be multiple argument if the desired group to |
|                            test is composed of seveal groups (i.e.: subgroups).        |
|         ctx      : The context containing all the test functions. Can be None, in this |
|                    case the context will be obtained using get_callable_ctx_from_file. |
|                                          Please leave it as None.                      |
|         filename : The filename from wich retrieving every test functions. Can be      |
|                       None, in this case the filename will be the caller one's.        |
|     )                                                                                  |
|      -> Run a group of test functions.                                                 |
|         If you want to run a subgroup, pass every group and subgroup as a parameter.   |
|         If no context <ctx> is provided, it will be obtained by importing the caller   |
|                      file using the get_callable_ctx_from_file function.               |
|         If a filename is provided, the context will be retrieved from this file.       |
|                                                                                        |
|         example :                                                                      |
|                   test_group("G") | This will run very test function from group "G".   |
|                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ |
|                   test_group(    |   This will run every                               |
|                       "G",       |    test function from                               |
|                       "Subgroup" |  the group "G" and the                              |
|                   )              |   subgroup "Subgroup".                              |
|                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ |
|                   test_group(             |  This will run every                       |
|                       "G",                |   test function from                       |
|                       "SG",               |   the group "G", the                       |
|                       "SSG",              | subgroup "SG" and the                      |
|                       filename="tests.py" | subgroup "SSG" from the                    |
|                   )                       |      "test.py" file.                       |
|     ********************************************************************************** |
|     test_all(                                                                          |
|         ctx      : The context containing all the test functions. Can be None, in this |
|                    case the context will be obtained using get_callable_ctx_from_file. |
|                                          Please leave it as None.                      |
|         filename : The filename from wich retrieving every test functions. Can be      |
|                       None, in this case the filename will be the caller one's.        |
|     )                                                                                  |
|      -> Run every test functions.                                                      |
|         If no context <ctx> is provided, it will be obtained by importing the caller   |
|                      file using the get_callable_ctx_from_file function.               |
|         If a filename is provided, the context will be retrieved from this file.       |
|                                                                                        |
|         example :                                                                      |
|                   test_all() | This will every test function from caller file context. |
|                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ |
|                   test_all(               | This will run every                        |
|                       filename="tests.py" | test function from                         |
|                   )                       | the "test.py" file.                        |
| -------------------------------------------------------------------------------------- |
|                  :PyQuickTest test kit is divided into few categories:                 |
*========================================================================================*""")
        exit()

    if os.path.isdir(kwargs["path"]):
        test_directory(path=kwargs["path"])
    else:
        test_file(filename=kwargs["path"])