#!/usr/bin/env python
import json
import argparse
import sys
import functools

from IPython import embed

from gettext import gettext as _, ngettext

class OptionshHelpAction(argparse._HelpAction):
    optionsh_help_code = 101
    
    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        sys.exit(self.optionsh_help_code)

def make_short_name(sn):
    if sn:
        return "-{}".format(sn)
    else:
        return None

def make_long_name(ln):
    if ln:
        return "--{}".format(ln)
    else:
        return None

def spec_to_arg(option):
    arg_type = option.get("has_arg", "POSITIONAL")
    pargs = []
    kwargs = {}
    if arg_type == "POSITIONAL":
        pargs = pargs + [
            option.get(
                "long_name",
                option.get("short_name")
            )
        ]
    else:
        try:
            pargs.append(make_long_name(option["long_name"]))
        except KeyError:
            pass
        try:
            pargs.append(make_short_name(option["short_name"]))
        except KeyError:
            pass
        if arg_type == "OPTIONAL_ARGUMENT":
            kwargs["nargs"] = "?"
            kwargs["const"] = "true"
        kwargs["required"] = not bool(option.get("optional"))
    kwargs["help"] = option.get("help")
    return (pargs, kwargs)

def specs_to_args(specs):
    parser = argparse.ArgumentParser(add_help=False)
    # This idea for grouping required named arguments is taken from poke on
    # StackOverflow.
    # https://stackoverflow.com/a/24181138 
    required_named = parser.add_argument_group("required named arguments")
    for spec in specs["options"]:
        args, kwargs = spec_to_arg(spec)
        if not bool(spec.get("optional")) and \
           spec.get("has_arg", "POSITIONAL") != "POSITIONAL": 
            required_named.add_argument(*args, **kwargs)
        else:
            parser.add_argument(*args, **kwargs)
    if specs["help"]:
        parser.add_argument(
            "-h",
            "--help",
            action=OptionshHelpAction,
            default=argparse.SUPPRESS,
            help=_('show this help message and exit')
        )
    return parser

def main():
    sys.argv = sys.argv[1:]
    parser = specs_to_args(json.load(sys.stdin))
    args = parser.parse_args()
    for arg, value in args.__dict__.items():
        print(f"{arg}:{value}")
        
if __name__ == "__main__":
    main()