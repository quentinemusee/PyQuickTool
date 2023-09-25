#!/usr/bin/env python
# -*- coding: utf-8 *-*


""" ~*~ Docstring ~*~
    PyQuickCLI file define the PyQuickCLI class, that allow
    easy-to-deploy CLI tools for creating command line tools.
         ~*~ Docstring ~*~

    ~*~ CHANGELOG ~*~
     _________________________________________
    | VERSION |    DATE    |     CONTENT      |
    |=========================================|
    |  0.0.1  | 2023-09-08 | Initial release. |
     ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
                              ~*~ CHANGELOG ~*~ """


#=--------------=#
# Import section #
#=--------------=#

from   __future__ import annotations
import os
import sys
import typing
import json
import re

# =------------------------------= #


#=------------------=#
# Authorship section #
#=------------------=#

__author__       = "Quentin Raimbaud"
__contact__      = "quentin.raimbaud.contact@gmail.com"
__copyright__    = None
__credits__      = None
__date__         = "2023-09-08"
__license__      = "MIT"
__maintainer__   = "Quentin Raimbaud"
__organization__ = None
__status__       = "Development"
__version__      = "0.0.1"

# =-------------------------------------------------= #


#=------------------------------------=#
# Constants & Global variables section #
#=------------------------------------=#

# ...

# =----------------------------------= #


#=--------------------------------=#
# ParsingAborted Exception section #
#=--------------------------------=#

class ParsingAborted(Exception):
    """Parsing aborted exception, useful for stopping parsing process."""

# =-------------------------------------------------------------------= #


#=------------------------=#
# PyQuickCLI class section #
#=------------------------=#

# Specifications:
#                   Optional arguments start with a '-'
#     -:...         specify that the input is an argument
#     -<...>        specify the type into what convert the parsed argument                | DEFAULT: str
#     -[...]        specify the default value of the argument                             | DEFAULT: None
#     -(...)        specify the expected quantity of arguments (0, 1, 2, 3, ..., ?, +, *) | DEFAULT: 1
#     -{.., .., ..} specify the expected possible argument values                         | DEFAULT: {any}
#

class PyQuickCLI:
    """An easy-to-use class that helps for making CLI tools."""

    # ======================== #
    # Public functions section #
    # ======================== #

    def __init__(
        self           : PyQuickCLI,
        struct         : str,
        funs           : list[typing.Callable[[object], object]] = []
    ) -> PyQuickCLI:
        """Initializer function."""

        # VERIFY INPUT TYPES

        # VERIFY STRUCT HAS AT LEAST ONE LINE OR SPECIAL CASE

        # REMOVE EVERY SPACES BETWEEN {} <> () []

        #self._top_level_args = [{f : e[1] for f in e[0]} for e in top_level_args] if top_level_args else {"-h": self.print_help, "--h": self.print_help}
        self._top_level_args_funs = {"-h": self.print_help, "--help": self.print_help}
        self._top_level_args      = {"-h": PyQuickCLIFunArg("-h(0)"), "--help": PyQuickCLIFunArg("--help(0)")}

        # Preparing the struct for parsing.
        prep_struct = self._prep_str(struct)

        # Parsing the prepared struct.
        self._cli_parsing = self._parse_struct(prep_struct, funs)

        #print(json.dumps(self._cli_parsing, indent=4))

    # =------------------------------------------------------= #


    # ======================== #
    # Public functions section #
    # ======================== #

    def run(self: PyQuickCLI, argv: list[str] | None = None) -> object:
        """Run the parser on the given argv if provided, otherwise run it on the sys.argv list."""
        try:
            # Getting the python call arguments if no argv provided.
            if argv == None:
                argv = sys.argv[1:]
            
            # Accessing the intern cli dictionary with the argv parameters.
            try:
                fun = self._multiple_dict_access(self._cli_parsing, argv, stop_at_fun=True)
            except (KeyError, TypeError) as keys:
                self.print_parsing_error(*keys.args)
                return
            
            # Printing help if not enough cli group given.
            if not type(fun) is PyQuickCLIFun:
                self.print_help(argv)
                return
            
            # Parsing the provided arguments.
            args = self._parse_args(fun, argv)

            # Parsing top-level arguments
            for top_level_arg in self._top_level_args:
                if top_level_arg in args:
                    self._top_level_args_funs[top_level_arg](fun, args)
                    raise ParsingAborted

            # Verifying that every mandatory argument are provided.
            args_names   = args.keys()
            missing_args = [mandatory_arg for mandatory_arg in fun.mandatory_args if mandatory_arg not in args_names]
            if missing_args:
                self.print_missing_args_error(missing_args)

            # Format the args names
            self._format_args_names(args)
            
            # Running the function.
            fun.unsafe_exec(args)

        except ParsingAborted:
            return

    def print_help(self: PyQuickCLI, fun: PyQuickCLIFun, args: dict[str, list[object]]) -> None:
        """Print the help message."""
        print("WE NEED A CLEANER PRINT HELP!!")
        raise ParsingAborted
        print(f"""Available values are: [{", ".join(self._multiple_dict_access(self._cli_parsing, keys).keys())}]""")

    def print_parsing_error(self: PyQuickCLI, keys: list[str]) -> None:
        """Print the parsing error message."""
        err_key = keys.pop()
        print("ERROR MESSAGE")
        raise ParsingAborted
        print(keys)
        print(f"""{err_key} is an invalid argument to the {' '.join([os.path.basename(__file__)] + keys)} command!""")
        print(f"""Available values are: [{", ".join(self._multiple_dict_access(self._cli_parsing, keys).keys())}]""")
    
    def print_nargs_error(self: PyQuickCLI, arg: PyQuickCLIFunArg, provided_narg: int) -> None:
        """Print the nargs error."""
        print(f"""The "{arg.name}" argument expects {arg.str_nargs_msg()} but {provided_narg} {"was" if provided_narg == 1 else "were"} provided.""")
        raise ParsingAborted
    
    def print_type_error(self: PyQuickCLI, arg: PyQuickCLIFunArg, vals: list[str]) -> None:
        """Print the type error."""
        try:
            wrong_type_arg = vals.pop(0)
            arg._type(wrong_type_arg)
        except Exception:
            pass
        type_name = arg._type.__name__
        print(f"""The "{arg.name}" argument expects arguments of type "{type_name}" but "{wrong_type_arg}" cannot be casted as "{type_name}".""")
        raise ParsingAborted
    
    def print_missing_args_error(self: PyQuickCLI, missing_args: list[str]) -> None:
        """Print the missing args error."""
        print(f"""The following arguments are missing: {missing_args}.""")
        raise ParsingAborted
    
    def print_extra_arguments_warning(self: PyQuickCLI, args_name: list[str]) -> None:
        """Print the extra arguments warning."""
        print(f"""Ignoring provided extra-arguments {args_name}.""")

    # =------------------------------------------------------= #


    # ========================= #
    # Private functions section #
    # ========================= #

    def _multiple_dict_access(
        self        : PyQuickCLI,
        dictonary   : dict[str, str | PyQuickCLIFun],
        keys        : list[str],
        stop_at_fun : bool = False,
    ) -> list[str] | PyQuickCLIFun:
        """Return the value after applying every given keys to the provided dictionary."""
        for i, key in enumerate(keys.copy()):
            if stop_at_fun:
                keys.pop(0)
            try:
                dictonary = dictonary[key]
            except (KeyError, TypeError):
                raise KeyError(keys[:i+1])
            if (stop_at_fun and type(dictonary) is PyQuickCLIFun):
                return dictonary
        return dictonary

    def _prep_str(self: PyQuickCLI, struct: str) -> str:
        """Prepare the given string argument for an easier struct interpretation."""
        return struct.strip()
    
    def _parse_struct(
            self   : PyQuickCLI,
            struct : str,
            funs   : list[typing.Callable[[object], object]]
        ) -> dict[str, str | PyQuickCLIFun]:
        """Parse the given struct and return the corresponding CLI core."""

        get_flag_val        = lambda x: x[-1] if x[-1][0] != ':' else x[-2]
        get_functions       = lambda x: x     if x[-1][0] != ':' else x[:-1]
        get_opt_last_arg    = lambda x: []    if x[-1][0] != ':' else [x[-1][1:]]

        lines        = struct.split('\n')
        tbl_lines    = self._tlb_lines(lines)
        cli_parsing  = {}
        args         = get_opt_last_arg(tbl_lines[0])
        old_tbl_line = tbl_lines[0]

        def insert_to_dict(dictonary: dict[str, str | list[str]], keys: list[str], values: list[str]) -> dict[str, str | list[str]]:
            """Local multiple keys insertion function for dictionaries."""
            for key in keys[:-1]:
                if key not in dictonary:
                    dictonary[key] = {}
                dictonary = dictonary[key]
            dictonary[keys[-1]] = values

        def insert_new_entry(
            old_tbl_line : str,
            funs         : list[typing.Callable[[object], object]],
            cli_parsing  : dict[str, str | PyQuickCLIFun],
        ):
            """Insert a new entry to both the funs and cli_parsing and the cli_func dictionaries."""
            temp = get_functions(old_tbl_line)
            fun  = funs.pop(0)
            insert_to_dict(cli_parsing, temp, PyQuickCLIFun(fun, args))

        for tbl_line in tbl_lines[1:]:
            if get_flag_val(tbl_line) != get_flag_val(old_tbl_line):
                insert_new_entry(old_tbl_line, funs, cli_parsing)
                args = get_opt_last_arg(tbl_line)
            else:
                args.append(tbl_line[-1][1:])
            old_tbl_line = tbl_line
        insert_new_entry(old_tbl_line, funs, cli_parsing)

        return cli_parsing
    
    def _tlb_lines(self: PyQuickCLI, lines: list[str]) -> list[str]:
        """Fill the given struct lines, rendering a list of completed lines."""
        q_lines  = [re.sub(r"'([^']*)'",    lambda match: match.group().replace(' ', "-----SEP-----"), line) for line in lines]
        dq_lines = [re.sub(r"\"([^\"]*)\"", lambda match: match.group().replace(' ', "-----SEP-----"), line) for line in q_lines]
        old_tbl_line = dq_lines[0].split(' ')
        tbl_lines    = [old_tbl_line]
        for line in dq_lines[1:]:
            parse_lstrip = self._parse_lstrip(line)
            tbl_line     = self._prep_str(line).split(' ')
            i = 0
            temp = []
            length = len(parse_lstrip)
            while length > 0:
                val    = old_tbl_line[i]
                length -= len(val) + 1
                i      += 1
                temp.append(val)
            tbl_line     = temp + tbl_line
            old_tbl_line = tbl_line
            tbl_lines.append(tbl_line)

        return tbl_lines
    
    def _parse_lstrip(self, string: str) -> str:
        """Parse the whitespaces characters on the left of a given string."""
        match = re.match(r"\s*", string)
        if match:
            return match.group(0)
        return ""

    def _parse_args(
        self,
        fun  : PyQuickCLIFun,
        args : dict[str, str | list[str] | list[typing.Callable[[object], object]]]
    ) -> dict[str, list[object]]:
        """Parse the given args for a given function."""

        # If no args to parse, return an empty parsed args list.
        if not args:
            return {}
        
        # Creating an insert function.
        def insert(
            parsed_args    : dict[str, list[object]],
            expected_args  : dict[str, PyQuickCLIFunArg],
            current_arg    : str,
            current_vals   : list[str],
            extra_arg_flag : bool
        ) -> None:
            """Insert a new parsed funtion to the parsed arguments list if the number of arguments and types are valid."""
            if extra_arg_flag:
                return
            arg   = expected_args[current_arg]
            nargs = len(current_vals)
            if not arg.valid_nargs(nargs):
                self.print_nargs_error(arg, nargs)
            if not arg.valid_type(current_vals):
                self.print_type_error(arg, current_vals)
            parsed_args[current_arg] = current_vals
        
        # Declaring necessary functions.
        expected_args  = {**self._top_level_args, **fun.args}
        args_name      = list(expected_args.keys())
        parsed_args    = {}
        current_arg    = args[0]
        current_vals   = []
        if current_arg in args_name:
            extra_args     = []
            extra_arg_flag = False
        else:
            extra_args     = [current_arg]
            extra_arg_flag = True

        # Parsing arguments.
        for e in args[1:]:
            if e not in args_name:
                if e[0] == '-':
                    insert(parsed_args, expected_args, current_arg, current_vals, extra_arg_flag)
                    extra_args.append(e)
                    extra_arg_flag = True
                elif not extra_arg_flag:
                    current_vals.append(e)
            else:
                insert(parsed_args, expected_args, current_arg, current_vals, extra_arg_flag)
                current_arg  = e
                current_vals = []
                extra_arg_flag    = False
        insert(parsed_args, expected_args, current_arg, current_vals, extra_arg_flag)

        # Printing the extra arguments warning if some are provided.
        if len(extra_args):
            self.print_extra_arguments_warning(extra_args)
        
        # Returning the parsed arguments.
        return parsed_args
    
    def _format_args_names(self, args : dict[str, list[object]]) -> dict[str, list[object]]:
        """Format the names of the given args dictionary."""
        keys = list(args.keys())
        for arg_name in keys:
            old_arg_name = arg_name
            if arg_name[0] == '-':
                while arg_name[0] == '-':
                    arg_name = arg_name[1:]
            arg_name = arg_name.replace('-', '_')
            if old_arg_name != arg_name:
                temp = args.pop(old_arg_name)
                args[arg_name] = temp



    # =------------------------------------------------------= #

# =----------------------------------------------------------------------------------------------------= #


#=---------------------------=#
# PyQuickCLIFun class section #
#=---------------------------=#

class PyQuickCLIFun:
    """An easy-to-use class that represent functions used by the PyQuickCLI class."""

    # ======================== #
    # Public functions section #
    # ======================== #

    def __init__(self: PyQuickCLIFun, fun: typing.Callable[[object], object], expected_args: list[str]) -> PyQuickCLIFun:
        """Initializer function."""

        self._fun  = fun
        temp       = [PyQuickCLIFunArg(expected_arg) for expected_arg in expected_args]
        self._args = {arg._name : arg for arg in temp}

    # =-----------------------------------------------------------------------------= #


    # ======================== #
    # Public functions section #
    # ======================== #

    def unsafe_exec(self: PyQuickCLIFun, args: dict[str, list[object]]) -> None:
        """Execute the function with the provided args, without verifying the validity of the provided args."""
        print(self.fun(**args))

    def __str__(self: PyQuickCLIFun) -> str:
        """String casting method."""
        return f"""{self._fun.__name__}({", ".join(self._args[key]._name for key in self._args)})"""

    # =-----------------------------------------------------------------------------= #


    # ================== #
    # Properties section #
    # ================== #

    @property
    def fun(self: PyQuickCLIFun) -> typing.Callable[[object], object]:
        """Getter function for the fun attribute."""
        return self._fun
    
    @property
    def args(self: PyQuickCLIFun) -> object:
        """Getter function for the args attribute."""
        return self._args
    
    @property
    def mandatory_args(self: PyQuickCLIFun) -> object:
        """Getter function for the args attribute, only keeping those that are mandatory."""
        return [arg for arg in self._args if not self._args[arg]._optional]

    @fun.setter
    def fun(self: PyQuickCLIFun, fun: typing.Callable[[object], object]) -> None:
        """Setter function for the fun attribute. fun is immutable"""
        pass
    
    @args.setter
    def args(self: PyQuickCLIFun, args: object) -> None:
        """Setter function for the args attribute. args is immutable"""
        pass
    
    # =-----------------------------------------------------------------------------= #

# =---------------------------------------------------------------------------------------= #


#=------------------------------=#
# PyQuickCLIFunArg class section #
#=------------------------------=#

class PyQuickCLIFunArg:
    """An easy-to-use class that represent argements used by the PyQuickCLIFun class."""

    # ======================== #
    # Public functions section #
    # ======================== #

    def __init__(self: PyQuickCLIFunArg, expected_arg: str) -> PyQuickCLIFunArg:
        """Initializer function."""

        self._name          = self._parse_name(expected_arg)
        self._optional      = expected_arg[0] == '-'
        self._type          = self._parse_type(expected_arg)
        self._default       = self._parse_default(expected_arg)
        self._nargs         = self._parse_nargs(expected_arg)
        self._possible_vals = self._parse_possible_vals(expected_arg)

    # =----------------------------------------------------------------------= #


    # ======================== #
    # Public functions section #
    # ======================== #

    def valid_nargs(self: PyQuickCLIFunArg, nargs: int) -> bool:
        """Check if the given number of arguments matches the expected one."""
        if   self._nargs.isdigit():
            return int(self._nargs) == nargs
        elif self._nargs == '?':
            return nargs in [0, 1]
        elif self._nargs == '+':
            return nargs > 0
        else:
            return True
        
    def valid_type(self: PyQuickCLIFunArg, vals: list[str]) -> bool:
        """Check if the given values can be convetted into the expected type."""
        try:
            [self._type(val) for val in vals]
        except Exception:
            return False
        return True

    def str_nargs_msg(self: PyQuickCLIFunArg) -> str:
        """Return the expected number of arguments followed by the word "argument"."""
        if   self._nargs.isdigit():
            return f"{self._nargs} argument" + 's' if int(self._nargs) else ""
        elif self._nargs == '?':
            return "0 or 1 argument"
        elif self._nargs == '+':
            return "1 or more arguments"
        else:
            return "any number of arguments"

    def __str__(self: PyQuickCLIFunArg) -> str:
        """String casting method."""
        return f"""\
{self._name}:
    Optional      : {self._optional}
    Type          : {self._type}
    Default       : {self._default}
    Nbr args      : {self._nargs}
    Possible vals : {self._possible_vals}"""

    # =-------------------------------------= #

    # ========================= #
    # Private functions section #
    # ========================= #

    def _parse_name(self, expected_arg: str) -> str:
        """Parse the name of the given expected_arg."""
        return re.findall(r"^[a-zA-Z-][a-zA-Z0-9_-]*", expected_arg)[0]
    
    def _parse_type(self, expected_arg: str) -> str:
        """Parse the potentially provided type to case to the given expected_arg."""
        match = re.findall(r"<(.*?)>", expected_arg)
        if match:
            return eval(match[0])
        return str
    
    def _parse_default(self, expected_arg: str) -> str:
        """Parse the potentially provided default value of the given expected_arg."""
        match = re.findall(r"\[(.*?)\]", expected_arg)
        if match:
            return self._type(match[0])
        return None

    def _parse_nargs(self, expected_arg: str) -> str:
        """Parse the potentially provided number of arguments of the given expected_arg."""
        match = re.findall(r"\((.*?)\)", expected_arg)
        if match:
            return match[0]
        return '1'
    
    def _parse_possible_vals(self, expected_arg: str) -> str:
        """Parse the potentially providedpossible values of the given expected_arg."""
        match = re.findall(r"{(.*?)}", expected_arg)
        if match:
            return [self._type(e) for e in match[0].split(',')]
        return '*'
    
    def _expect_possible_vals(self) -> bool:
        """Utility function for determining if a choice of arguments is expectd."""
        return type(self._expect_possible_vals) is list

    # =----------------------------------------------------------------------= #


    # ================== #
    # Properties section #
    # ================== #

    @property
    def name(self: PyQuickCLIFun) -> str:
        """Getter function for the name attribute."""
        return self._name
    
    @property
    def optional(self: PyQuickCLIFun) -> bool:
        """Getter function for the optional attribute."""
        return self._optional
    
    @property
    def type(self: PyQuickCLIFun) -> type:
        """Getter function for the type attribute."""
        return self._type 
    
    @property
    def default(self: PyQuickCLIFun) -> object:
        """Getter function for the default attribute."""
        return self._default
    
    @property
    def nargs(self: PyQuickCLIFun) -> str:
        """Getter function for the nargs attribute."""
        return self._nargs
    
    @property
    def possible_vals(self: PyQuickCLIFun) -> list[object] | str['*']:
        """Getter function for the possible_vals attribute."""
        return self._possible_vals

    @name.setter
    def name(self: PyQuickCLIFun, name: str) -> None:
        """Setter function for the name attribute. name is immutable"""
        pass

    @optional.setter
    def optional(self: PyQuickCLIFun, optional: bool) -> None:
        """Setter function for the optional attribute. optional is immutable"""
        pass

    @type.setter
    def type(self: PyQuickCLIFun, type: type) -> None:
        """Setter function for the type attribute. type is immutable"""
        pass

    @default.setter
    def default(self: PyQuickCLIFun, default: object) -> None:
        """Setter function for the default attribute. default is immutable"""
        pass

    @nargs.setter
    def nargs(self: PyQuickCLIFun, nargs: str) -> None:
        """Setter function for the nargs attribute. nargs is immutable"""
        pass

    @possible_vals.setter
    def expected_arg(self: PyQuickCLIFun, possible_vals: list[object] | str['*']) -> None:
        """Setter function for the possible_vals attribute. possible_vals is immutable"""
        pass

    # =----------------------------------------------------------------------= #

#                   Optional arguments start with a '-'
#     -:...         specify that the input is an argument
#     -<...>        specify the type into what convert the parsed argument                | DEFAULT: str
#     -[...]        specify the default value of the argument                             | DEFAULT: None
#     -(...)        specify the expected quantity of arguments (0, 1, 2, 3, ..., ?, +, *) | DEFAULT: 1
#     -{.., .., ..} specify the expected possible argument values                         | DEFAULT: {any}

# =----------------= #

def group1_subgroup1(arg1: object, arg2: object, arg3: object) -> None:
    print("Running the group1_subgroup1 function!")
    print("arg1 =", arg1)
    print("arg2 =", arg2)
    print("arg3 =", arg3)
def group1_subgroup2(arg1: object, arg2: object) -> None:
    print("Running the group1_subgroup2 function!")
    print("arg1 =", arg1)
    print("arg2 =", arg2)
def group2_subgroup1() -> None:
    print("Running the group2_subgroup1 function!")
def group2_subgroup2(arg1: object, arg2: object) -> None:
    print("Running the group2_subgroup2 function!")
    print("arg1 =", arg1)
    print("arg2 =", arg2)
def group3_subgroup1(arg1: object) -> None:
    print("Running the group3_subgroup1 function!")
    print("arg1 =", arg1)

# Specifications:
#                   Optional arguments start with a '-'
#     -:...         specify that the input is an argument
#     -<...>        specify the type into what convert the parsed argument                | DEFAULT: str
#     -[...]        specify the default value of the argument                             | DEFAULT: None
#     -(...)        specify the expected quantity of arguments (0, 1, 2, 3, ..., ?, +, *) | DEFAULT: 1
#     -{.., .., ..} specify the expected possible argument values                         | DEFAULT: {any}
#     -"..."        specify the description of the element it follows                     | DEFAULT: ""
#

PyQuickCLI("""
group1 subgroup1 :arg1<str>"First arg!"
                 :-arg2(+)[True]
                 :-arg3(*)
       subgroup2 :-arg1(1){bleu,rouge,vert}
                 :-arg2(*)
group2 subgroup1
       subgroup2 :-arg1(+)
                 :-arg2(+)
group3 subgroup1 :-arg1(*)<int>[5]
""",
    funs=[group1_subgroup1, group1_subgroup2, group2_subgroup1, group2_subgroup2, group3_subgroup1],
).run()