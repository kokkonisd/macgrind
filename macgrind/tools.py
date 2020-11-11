#!/usr/bin/env python3

##
## @package macgrind
## @author Dimitri Kokkonis ([\@kokkonisd](https://github.com/kokkonisd))
##
## This file contains useful tools/functions for the `macgrind` tool.
##


from .definitions import COLORS


def print_color_message(message, color, end='\n'):
    if color not in COLORS.keys():
        return

    print(COLORS[color].format(message), end=end)


def info(message, end='\n'):
    """Prints a colored info message."""
    print_color_message(message=message, color='yellow', end=end)


def warn(message, end='\n'):
    """Prints a colored warning message."""
    print_color_message(message=f'/!\\ {message}', color='orange', end=end)


def fail(message, end='\n'):
    """Prints a colored error message and exits."""
    print_color_message(message=message, color='red', end=end)
    exit(1)
