#!/usr/bin/env python3

##
## @package macgrind
## @author Dimitri Kokkonis ([\@kokkonisd](https://github.com/kokkonisd))
##
## This file contains useful tools/functions for the `macgrind` tool.
##


import subprocess

from .definitions import COLORS


def cleanup(files):
    """
    Cleans up.
    """
    # Remove garbage
    for file in files:
        subprocess.run(["rm", "-rf", file])


def print_color_message(message, color, end='\n'):
    """
    Prints a colored message.
    
    :param      message:  The message to print.
    :type       message:  string
    :param      color:    The color to print in.
    :type       color:    string (COLORS dictionary in definitions.py)
    :param      end:      The end character/string ('\n' by default)
    :type       end:      string
    """
    if color not in COLORS.keys():
        return

    print(COLORS[color].format(message), end=end)


def info(message, end='\n'):
    """
    Prints an info message.
    
    :param      message:  The message to print.
    :type       message:  string
    :param      end:      The end character/string ('\n' by default)
    :type       end:      string
    """
    print_color_message(message=message, color='yellow', end=end)


def warn(message, end='\n'):
    """
    Prints a warning message.
    
    :param      message:  The message to print.
    :type       message:  string
    :param      end:      The end character/string ('\n' by default)
    :type       end:      string
    """
    print_color_message(message=f'/!\\ {message}', color='orange', end=end)


def fail(message, cleanup_files, end='\n'):
    """
    Prints a fail message, cleans up and exits.
    
    :param      message:  The message to print.
    :type       message:  string
    :param      message:  A list of files to clean up.
    :type       message:  list
    :param      end:      The end character/string ('\n' by default)
    :type       end:      string
    """
    print_color_message(message=message, color='red', end=end)
    cleanup(cleanup_files)
    exit(1)
