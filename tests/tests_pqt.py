#!/usr/bin/env python
# -*- coding: utf-8 *-*


""" ~*~ Docstring ~*~
    Testing file for the pqt library.                  
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
from pyquicktools.pyquicktest.assertions import *
from pyquicktools.pyquicktest.decorators import *
from pyquicktools.pyquicktest.gen        import *
from pyquicktools.pyquicktest.test       import *
from pyquicktools.pyquicktest.utils      import *
import typing


# =------------------------------= #


#=------------------=#
# Authorship section #
#=------------------=#

__filename__     = "test_pqt.py"

# =--------------------------------------------------------= #


#=------------------------------------=#
# Constants & Global variables section #
#=------------------------------------=#

NBR_TESTS_EXEC = 100

# =----------------------------------= #


#=-----------------------=#
# Tests functions section #
#=-----------------------=#


####################################################
### -------------------------------------------- ###
### _*~*_ General purpose decorateurs test _*~*_ ###
### -------------------------------------------- ###
####################################################

@group("General purpose decorators", "Attributes")
@execnbr(NBR_TESTS_EXEC)
def test_add_flag_1() -> typing.Union[TestPassedException, TestFailedException]:
    """Test the add_flag decorator with a random attribute."""
    attribute  = gen_ascii_string()
    @add_flag(attribute)
    def func() -> None: pass
    check(hasattr(func, attribute),                   f"The decorated function doesn't have the just added attribute <{attribute}>.")
    ensure(func.__getattribute__(attribute) == None,  f"The decorated function just added attribute <{attribute}> retrieved value <{func.__getattribute__(attribute)}> doesn't fit the default flag value <None>.")

@group("General purpose decorators", "Attributes")
@execnbr(NBR_TESTS_EXEC)
def test_add_attribute_1() -> typing.Union[TestPassedException, TestFailedException]:
    """Test the add_attribute decorator with random and default values."""
    attribute  = gen_ascii_string()
    value      = gen_random_value()
    if gen_bool():
        @add_attribute(attribute, value)
        def func() -> None: pass
        check(hasattr(func, attribute),                    f"The decorated function doesn't have the just added attribute <{attribute}>.")
        ensure(func.__getattribute__(attribute) == value,  f"The decorated function just added attribute <{attribute}> retrieved value <{func.__getattribute__(attribute)}> doesn't fit the added value <{value}>.")
    @add_attribute(attribute)
    def func() -> None: pass
    check(hasattr(func, attribute),                   f"The decorated function doesn't have the just added attribute <{attribute}>.")
    ensure(func.__getattribute__(attribute) == None,  f"The decorated function just added attribute <{attribute}> retrieved value <{func.__getattribute__(attribute)}> doesn't fit the default value <None>.")

@group("General purpose decorators", "Attributes")
@execnbr(NBR_TESTS_EXEC)
def test_add_flags_1() -> typing.Union[TestPassedException, TestFailedException]:
    """Test the add_flags decorator with random attributes."""
    attributes = gen_generator(length=gen_int(max=10), gen_element=gen_ascii_string)
    @add_flags(*attributes)
    def func() -> None: pass
    for attribute in attributes:
        check(hasattr(func, attribute),                  f"The decorated function doesn't have the just added attribute <{attribute}>.")
        check(func.__getattribute__(attribute) == None,  f"The decorated function just added attribute <{attribute}> retrieved value <{func.__getattribute__(attribute)}> doesn't fit the default flag value <None>.")
    ok()

@group("General purpose decorators", "Attributes", "eheh")
@execnbr(NBR_TESTS_EXEC)
def test_add_attributes_1() -> typing.Union[TestPassedException, TestFailedException]:
    """Test the add_attributes decorator with several attributes and values."""
    attributes_and_values = gen_list(length=gen_int(max=10), gen_element=lambda: (gen_ascii_string(), gen_random()))
    @add_attributes(*attributes_and_values)
    def func() -> None: pass
    for (attribute, value) in attributes_and_values:
        check(hasattr(func, attribute),                   f"The decorated function doesn't have the just added attribute <{attribute}>.")
        check(func.__getattribute__(attribute) == value,  f"The decorated function just added attribute <{attribute}> retrieved value <{func.__getattribute__(attribute)}> doesn't fit the default value <value>.")
    ok()

# =----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------= #


##################################################
### ------------------------------------------ ###
### _*~*_ General purpose functions test _*~*_ ###
### ------------------------------------------ ###
##################################################

@group("General purpose functions", "Map")
@execnbr(NBR_TESTS_EXEC)
def test_map1_1() -> typing.Union[TestPassedException, TestFailedException]:
    """Test the map1 function with a random iterables and a trivial function."""
    list_ = gen_list()
    func = lambda x: False
    ensure(not any(map1(func, list_)), f"The mapped function <to_False> didn't change every value of the given list to False.")

@group("General purpose functions", "Map")
@parametrize(list(range(10)))
@execnbr(NBR_TESTS_EXEC)
def test_map1_2(iterable: typing.Iterable[object]) -> typing.Union[TestPassedException, TestFailedException]:
    """Test the map1 function with a random iterables and a trivial function."""
    func = lambda x: x+1
    ensure(map1(func, iterable) == list(range(1, 11)), f"The mapped function <+1> didn't change every value of the given list as expected.")

@group("General purpose functions", "Map")
@execnbr(NBR_TESTS_EXEC)
def test_map2_1() -> typing.Union[TestPassedException, TestFailedException]:
    """Test the map2 function with two random iterables and a trivial function."""
    list_1 = gen_list()
    list_2 = gen_list()
    func = lambda x, y: (y, x)
    ensure(map2(func, list_1, list_2) == list(zip(list_2, list_1)), f"The mapped function <to_zip> didn't fit the applied zip function to the lists.")

@group("General purpose functions", "Map")
def test_map2_2() -> typing.Union[TestPassedException, TestFailedException]:
    """Test the map1 function with a random iterables and a trivial function."""
    iterable1, iterable2 = list(range(10)), list(range(9, -1, -1))
    func = lambda x, y: x+y
    ensure(map2(func, iterable1, iterable2) == 10*[9], f"The mapped function <+1> didn't change every value of the given list as expected.")

@group("General purpose functions", "Attributes")
@execnbr(NBR_TESTS_EXEC)
def test_hasattributes_setattributesflags_1() -> typing.Union[TestPassedException, TestFailedException]:
    """Test the hasattributes and setattributesflags functions with random functions and attributes. The expected hasattributes result is True."""
    attributes = gen_generator(length=gen_int(max = 10), gen_element=gen_ascii_string)
    def func() -> None: pass
    setattributesflags(func, *attributes)
    ensure(hasattributes(func, *attributes), f"The just added attributes aren't all detected by the <hasattributes> function.")

@group("General purpose functions", "Attributes")
@execnbr(NBR_TESTS_EXEC)
def test_hasattributes_setattributes_2() -> typing.Union[TestPassedException, TestFailedException]:
    """Test the hasattributes and setattributes functions with random functions and attributes. The expected hasattributes result is False."""
    attributes = gen_list(length=gen_int(min=1, max = 10), gen_element=gen_ascii_string)
    sub_attributes = attributes[1:-1]
    def func() -> None: pass
    setattributes(func, *zip(*sub_attributes, len(sub_attributes)*[None]))
    ensure(not hasattributes(func, *attributes), f"The just added attributes aren't all detected by the <hasattributes> function.")

@group("General purpose functions", "Attributes")
@execnbr(NBR_TESTS_EXEC)
def test_get_all_functions_1() -> typing.Union[TestPassedException, TestFailedException]:
    """Test the get_all_functions function with a random context full of functions with no attributes."""
    ctx = gen_dict(length=gen_int(max=10), gen_keys=gen_ascii_string, gen_values=gen_callable)
    ensure(get_all_functions(ctx=ctx) == list(ctx.values()), f"The iterable of functions returned doesn't match the given context.")

@group("General purpose functions", "Attributes")
@execnbr(NBR_TESTS_EXEC)
def test_get_all_functions_2() -> typing.Union[TestPassedException, TestFailedException]:
    """Test the get_all_functions function with a random context full of functions and random attributes."""
    ctx = gen_dict(length=gen_int(max=10), gen_keys=gen_ascii_string, gen_values=gen_callable)
    map1(lambda func: setattr(func, "attr", gen_random_value()), list(ctx.values()))
    ensure(get_all_functions("attr", ctx=ctx) == list(ctx.values()), f"The iterable of functions returned doesn't match the given context for the added attributes.")

# =---------------------------------------------------------------------------------------------------------------------------------------------------------------= #


# Running the tests if the file is directly executed.
if __name__ == '__main__':
    test_file()