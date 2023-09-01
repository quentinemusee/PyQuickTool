#!/usr/bin/env python
# -*- coding: utf-8 *-*


""" ~*~ Docstring ~*~
     An all in one file utility function,  
    providing what modern python is missing.                   
                           ~*~ Docstring ~*~

    ~*~ CHANGELOG ~*~
     ____________________________________________________________________________________
    | VERSION |    DATE    |                           CONTENT                           |
    |====================================================================================|
    | 0.0.1   | 2023/07/25 | ..........................................................  |
    |------------------------------------------------------------------------------------|
     ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
                                                                         ~*~ CHANGELOG ~*~ """


#=--------------=#
# Import section #
#=--------------=#

from   __future__ import annotations
import typing
import os
import sys
import threading
import queue
import inspect

# =------------------------------= #


#=-----------------=#
# Autorship section #
#=-----------------=#

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


# =--------------------------------------------------------= #


#=------------------------------------=#
# Constants & Global variables section #
#=------------------------------------=#

# ...

# =----------------------------------= #


# ================================== #
# General purpose exceptions section #
# ================================== #

class RequireException(Exception):
    "Raised when a require isn't satisfied and no exception is provided."
    pass

# =----------------------------------= #


# ===================================================== #
# General purpose decorators required functions section #
# ===================================================== #

def copy_function_attributes(src_func: typing.Callable[[object], object], dest_func: typing.Callable[[object], object]) -> typing.Callable[[object], object]:
    """Copy every safe-copy attributes from one function to another, and return the destination function."""
    setattr(dest_func, "__annotations__", {"return": getattr(src_func, "__annotations__").get("return", object)})
    for attr in dir(src_func):
        if attr not in [
            "__annotations__", "__builtins__", "__call__", "__class__", "__closure__", "__code__", "__defaults__", "__delattr__", "__dir__", "__eq__",
            "__format__", "__ge__", "__get__", "__getattribute__", "__globals__", "__gt__", "__hash__", "__init__", "__init_subclass__", "__kwdefaults__",
            "__le__", "__lt__", "__ne__", "__new__", "__reduce__", "__reduce_ex__", "__repr__", "__setattr__", "__sizeof__", "__str__", "__subclasshook__"
        ]:
            setattr(dest_func, attr, getattr(src_func, attr))
    return dest_func

def return_or_raise(value: object) -> object:
    """Return or raise the given value <value> if it is an Exception."""
    if type(value) == Exception:
        raise value
    return value

# =----------------------------------------------------------------------------------------------------------------------------------------------------= #


# ================================== #
# General purpose decorators section #
# ================================== #

def add_flag(flag: str) -> typing.Callable[[object], object]:
    """Add a given attribute name with a <None> value to the decorated function."""
    def decorator(func: typing.Callable[[object], object]) -> typing.Callable[[object], object]:
        setattr(func, flag, None)
        return func
    return decorator
# Marking the decorator itself as tested.
add_flag.tested = None

def add_attribute(attribute: str, value: object = None) -> typing.Callable[[object], object]:
    """Add a given attribute name and value [default: None] to the decorated function."""
    def decorator(func: typing.Callable[[object], object]) -> typing.Callable[[object], object]:
        setattr(func, attribute, value)
        return func
    return decorator

def add_flags(*flags: str) -> typing.Callable[[object], object]:
    """Add a given attribute name with a <None> value to the decorated function."""
    def decorator(func: typing.Callable[[object], object]) -> typing.Callable[[object], object]:
        for flag in flags:
            setattr(func, flag, None)
        return func
    return decorator

def add_attributes(*attributes_and_values: typing.Union[str, typing.Tuple[str, object]]) -> typing.Callable[[object], object]:
    """Add a given list of attribute name and value to the decorated function."""
    def decorator(func: typing.Callable[[object], object]) -> typing.Callable[[object], object]:
        try:
            if type(attributes_and_values[0]) == tuple:
                for attribute_and_value in attributes_and_values:
                    (attribute, value) = attribute_and_value
                    setattr(func, attribute, value)
            else:
                for i in range(0, int(len(attributes_and_values)+1/2), 2):
                    (attribute, value) = attributes_and_values[i], attributes_and_values[i+1]
                    setattr(func, attribute, value)
        except IndexError:
            pass
        return func
    return decorator

def alias(*aliases: str) -> typing.Callable[[object], object]:
    """Create aliases for the decorated object.
       This might cause your IDE to generate warning on undefined functons because decoratord are applied when interprated,
       that's why this utils file use explicit aliasing instead of elegant use of this decorator."""
    def decorator(func: typing.Callable[[object], object]) -> typing.Callable[[object], object]:
        map1(lambda x: globals().update({x: func}), aliases)
        return func
    return decorator

def timeout(duration: float, default: object) -> typing.Callable[[object], object]:
    """Add a timeout to the decorated object."""

    # Creating the decorator function.
    def decorator(func: typing.Callable[[object], object]) -> typing.Callable[[object], object]:
        # Creating a queue object for storing the potentially returned value from the given <func> function.
        queue_ = queue.Queue(maxsize=1)

        # Creating a temporary function that simply put the result of the <func> function
        # to the previously created queue whatever its result is (even Exceptions).
        def target():
            try:
                queue_.put(func())
            except Exception as e:
                queue_.put(e)
        
        # Creating the modified function that use a Thread to run in background the <func> function.
        # After a given amount of time, the function result is ignored, and the default value is returned.
        def timeout_func():
            action = threading.Thread(target=target, daemon=True)
            action.start()
            action.join(timeout=duration)
            if action.is_alive():
                return_or_raise(default)
            return_or_raise(queue_.get())

        # Copy the <func> function attributes to the newly created <timeout_func> function.
        return copy_function_attributes(func, timeout_func)
    return decorator

# =----------------------------------------------------------------------------------------------= #


# ================================= #
# General purpose functions section #
# ================================= #

def require(boolean: bool, err: typing.Union[str, Exception] = None, raise_exception: bool = True, file: typing.TextIO = sys.stderr):
    """Rust-style function, evaluate the given boolean <boolean> and raise or print to <file> a given error <err> depending on the given <raise_exception>."""
    if not boolean:
        if raise_exception:
            raise err if type(err) == Exception else RequireException(err)
        print(err, file=file)

def map1(func: typing.Callable[[object], object], x: typing.Iterable[object]) -> typing.Iterable[object]:
    """Map the given function over the elements of the given iterable."""
    return type(x)(map(func, x))

def map2(func: typing.Callable[[object], object], x: typing.Iterable[object], y: typing.Iterable[object]) -> typing.Iterable[object]:
    """Map the given function over the elements of the two given iterables."""
    return type(x)(map(lambda arg: func(*arg), zip(x, y)))

def mapn(func: typing.Callable[[object], object], *xs: typing.Iterable[object]) -> typing.Iterable[object]:
    """Map the given function over the elements of the given iterables."""
    return type(Option(lambda: xs[0]).unwrap_or([]))(map(lambda arg: func(*arg), zip(*xs)))

def filter1(func: typing.Callable[[object], object], x: typing.Iterable[object]) -> typing.Iterable[object]:
    """Filter the given iterable with the given boolean function."""
    return type(x)(filter(func, x))

def filter2(func: typing.Callable[[object], object], x: typing.Iterable[object], y: typing.Iterable[object]) -> typing.Iterable[object]:
    """Filter the two given iterables with the given boolean function."""
    return type(x)(filter(lambda arg: func(*arg), zip(x, y)))

def filtern(func: typing.Callable[[object], object], *xs: typing.Iterable[object]) -> typing.Iterable[object]:
    """Filter the given iterabless with the given boolean function."""
    return type(Option(lambda: xs[0]).unwrap_or([]))(filter(lambda arg: func(*arg), zip(*xs)))

def hasattributes(object: object, *attributes: str) -> bool:
    """Check if a given object has every given attributes."""
    return all(map1(lambda x: hasattr(object, x) if not x.startswith("!") else not hasattr(object, x.split('!')[1]), attributes))

def setattributesflags(object: object, *flags: str) -> object:
    """Set every given flags attributes to a provided object."""
    map1(lambda x: setattr(object, x, None), flags)
    return object

def setattributes(object: object, *attributes_and_values: typing.Tuple[str, object]) -> bool:
    """Set every given attributes and values to a provided object."""
    map1(lambda x: setattr(object, x[0], x[1]), attributes_and_values)
    return object

def get_all_functions(*attributes: str, ctx: typing.Optional[typing.Dict[str, object]] = None) -> typing.List[typing.Callable[[object], object]]:
    """Returns every functions containing every provided attributes from the given context.
       If no context is provided, then the globals context will be used."""
    if ctx := ctx if ctx != None else globals():
        return filter1(lambda x: callable(x) and hasattributes(x, *attributes), list(ctx.values()) if type(ctx) == dict else ctx)
    return []

def get_ctx_from_file(file: str) -> typing.Dict[str, typing.Callable[[object], object]]:
    """Get the global context of a given file name."""
    sys.path.append(os.path.dirname(file))
    filename   = file.split('/')[-1].split('\\')[-1].split('.')[0]
    src_module = __import__(filename)
    ctx_raw    = dir(src_module)
    return  {e: getattr(src_module, e) for e in ctx_raw if callable(getattr(src_module, e))}

def get_caller_file() -> str:
    """get the last caller file different from the one calling this function."""
    return next(
        (e.filename for e in inspect.stack() if e.filename.split('/')[-1].split('\\')[-1] != __file__.split('/')[-1].split('\\')[-1])
    )

def merge1(*iterable: typing.List[object]) -> typing.List[object]:
    """Merge a lists of element into one list."""
    return () if not iterable else type(iterable[0])(f for e in iterable for f in e)

def merge2(*iterable: typing.List[object]) -> typing.List[object]:
    """Merge a lists of lists of element into one list."""
    return () if not iterable else type(iterable[0])(g for e in iterable for f in e for g in f)

def remove_dupicates(list_: typing.List[object]) -> typing.List[object]:
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

# =-----------------------------------------------------------= #


# ======================= #
# Files functions section #
# ======================= #

def read_file(file: str, encoding: str | None = None) -> str:
    """Read and return the content of a given filepath.
    : param file     : The file to open and read the content.
    : param encoding : The encoding format to apply for reading."""
    with open(file, 'r', encoding=encoding) as read_file:
        return read_file.read()
    
def write_file(file: str, content: str, encoding: str | None = None) -> str:
    """Write a given content to the given filepath.
    : param file     : The file to open and write the content.
    : param content  : The content to write to the file.
    : param encoding : The encoding format to apply for writing."""
    with open(file, 'w', encoding=encoding) as write_file:
        write_file.write(content)

# =-----------------------------------------------------------= #


# ==================== #
# Option class section #
# ==================== #

class Option(object):
    """A Rust-style Option class containing a single object that can be of any type (error included).
       Allows single instruction object manipulation without the need of a heavy try-catch statement."""

    # =================== #
    # Initializer section #
    # =================== #

    @add_flag("tested")
    def __init__(self: Option, optional: object, type_: typing.Optional[typing.Type[object]] = None) -> Option:
        """Option class initializer function."""

        # If the given optional data isn't callable, simply wrap its value.
        if not callable(optional):
            self._optional    = optional
            self._type        = type_ if type_ else type(self._optional)
            self._unwrappable = True
            return

        # Otherwise, call it to retrieve its result.
        try:
            # Optional call success
            self._optional    = optional()
            self._type        = type_ if type_ else type(self._optional)
            self._unwrappable = True
        except Exception as e:
            # Optional call failed
            self._optional    = e
            self._type        = type_
            self._unwrappable = False

    # =------------------------------------------------------= #

    # ===================================================== #
    # Optional data manipulation instance functions section #
    # ===================================================== #

    @add_flag("tested")
    def apply(self: Option, fun: typing.Callable[[object], object]) -> Option:
        """Apply a given callable <fun> to the optional value if it is unwrappable."""
        if self._unwrappable:
            try:
                self._optional = fun(self._optional)
            except Exception as e:
                self._optional    = e
                self._unwrappable = False
        return self

    @add_flag("tested")
    def apply_to(self: Option, fun: typing.Callable[[object], object]) -> object:
        """Apply the optional value to the given function <fun>.
           Return the result without modifying the Option itself.
           If the optonal isn't unwrappable, returns False."""
        return fun(self._optional) if self._unwrappable else False
    
    @add_flag("tested")
    def unwrap(self: Option) -> object:
        """Return the optional value, whatever it is.
           If the optional value is not wrappable (i.e.: is an exception), then this exception is raised."""
        if self._unwrappable:
            return self._optional
        else:
            raise  self._optional

    @add_flag("tested")
    def unwrap_or(self: Option, or_: object) -> object:
        """Return the optional value or a given <or_> value if the optional value is not unwrappable."""
        return self._optional if self._unwrappable else or_

    @add_flag("tested")
    def unwrap_or_default(self: Option) -> object:
        """Return the optional value or its type default value if the optional value is not unwrappable."""
        return self._optional if self._unwrappable else self._type() if self._type != None else None

    @add_flag("tested")
    def unwrap_or_else(self: Option, else_: typing.Callable[[object], object]) -> object:
        """Return the optional value or compute the given callable <else_> if the optional value is not unwrappable."""
        return self._optional if self._unwrappable else else_()

    # =-------------------------------------------------------------------------------------------------------------= #

    # ================== #
    # Properties section #
    # ================== #

    # ------- #
    # Getters #
    #-------- #

    @property
    def optional(self: Option) -> ValueError:
        """It is not possible to get the optional value via this property method."""
        raise ValueError("It is not possible to get the optional value via this property method.")

    @property
    def type(self: Option) -> bool:
        """Option type property getter."""
        return self._type

    @property
    def unwrappable(self: Option) -> bool:
        """Unwrappable property getter."""
        return self._unwrappable

    # =--------------------------------------------------------------------------------------------= #

    # ------- #
    # Setters #
    #-------- #

    @optional.setter
    def optional(self: Option, value: object) -> ValueError:
        """It is not possible to set the optional value via this property method."""
        raise ValueError("It is not possible to set the optional value via this property method.")
    
    @type.setter
    def type(self: Option, value: typing.Optional[typing.Type[object]]) -> ValueError:
        """It is not possible to set the optional type via this property method."""
        raise ValueError("It is not possible to set the optional type via this property method.")

    @unwrappable.setter
    def unwrappable(self: Option, value: bool) -> ValueError:
        """It is not possible to set the unwrappable value via this property method."""
        raise ValueError("It is not possible to set the unwrappable value via this property method.")

    # =-------------------------------------------------------------------------------------------= #

# =-----------------------------------------------------------------------------------------------------= #
