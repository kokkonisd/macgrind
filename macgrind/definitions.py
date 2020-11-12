#!/usr/bin/env python3

##
## @package macgrind
## @author Dimitri Kokkonis ([\@kokkonisd](https://github.com/kokkonisd))
##
## This file contains useful definitions for the `macgrind` tool.
##


VERSION = "1.0.1"


COLORS = {
    'yellow': '\033[33m{}\033[0m',
    'orange': '\033[91m{}\033[0m',
    'red'   : '\033[31m{}\033[0m'
}


DEFAULT_DOCKERFILE = '''\
FROM {}
RUN  apt-get update -y
RUN  apt-get install -y build-essential valgrind {}
ADD  . /valgrind_project_tmp/
RUN  cd /valgrind_project_tmp/ && {}
RUN  make -C /valgrind_project_tmp/ all 
CMD  ["valgrind", "--leak-check=full", "--error-exitcode=1", "/valgrind_project_tmp/{}"]
'''


CUSTOM_COMMAND_DOCKERFILE = '''\
FROM {}
RUN  apt-get update -y
RUN  apt-get install -y build-essential valgrind {}
ADD  . /valgrind_project_tmp/
RUN  cd /valgrind_project_tmp/ && {}
RUN  cd /valgrind_project_tmp/ && {} 
CMD  ["valgrind", "--leak-check=full", "--error-exitcode=1", "/valgrind_project_tmp/{}"]
'''
