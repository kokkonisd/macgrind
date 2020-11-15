#!/usr/bin/env python3

##
## @package macgrind
## @author Dimitri Kokkonis ([\@kokkonisd](https://github.com/kokkonisd))
##
## This file contains useful definitions for the `macgrind` tool.
##


VERSION = "1.0.4"


COLORS = {
    'yellow': '\033[33m{}\033[0m',
    'orange': '\033[91m{}\033[0m',
    'red'   : '\033[31m{}\033[0m'
}


# Different name, such as to not accidentally erase any user Dockerfiles
DOCKERFILE_NAME = 'temp_Macgrind_Dockerfile'


DEFAULT_DOCKERFILE = '''\
FROM       {}
RUN        apt-get update -y
RUN        apt-get install -y build-essential valgrind {}
ADD        . /valgrind_project_tmp/
WORKDIR    /valgrind_project_tmp/
RUN        {}
RUN        {}
ENTRYPOINT valgrind --leak-check=full --error-exitcode=1 ./{} && {}
'''
