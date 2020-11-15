# macgrind

![CI](https://github.com/kokkonisd/macgrind/workflows/CI/badge.svg)
![Stable version](https://img.shields.io/pypi/v/macgrind?label=stable%20version)
![Latest version](https://img.shields.io/github/v/tag/kokkonisd/macgrind?color=yellow&label=latest%20version)

Containerized Valgrind on macOS for C and C++ projects.


## why

As of the time of writing this, [Valgrind](https://www.valgrind.org/) is not natively supported on several recent
versions of macOS. This tool allows you to run it in a [Docker](https://www.docker.com/) container without any code
changes or extra garbage.


## how to install

You can install `macgrind` via `pip`:

```text
$ pip3 install macgrind
```

You also need to install [Docker Desktop](https://www.docker.com/products/docker-desktop), and have it running.


## how to use

You can use `macgrind` by specifying the project's directory, and a target binary to run `valgrind` on.
Please note that the target binary's path must be the one **relative to the project path** instead of the absolute one.

For example, say I have a C project with the following structure:

```text
my_c_project/
    src/
        main.c
    Makefile
```

I need to supply the full path to `my_c_project/`, but only the relative path to the target executable: `main` (and not
`my_c_project/main`). The assumption here is that the `all` target in the `Makefile` builds `my_c_project/main`.

So, we could run `macgrind` like this:

```text
$ macgrind my_c_project/ main
Creating temporary Dockerfile...
Building Docker image...
Running Docker container...
==========
Here's the output of the container:
==1== Memcheck, a memory error detector
==1== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1== Using Valgrind-3.13.0 and LibVEX; rerun with -h for copyright info
==1== Command: /valgrind_project_tmp/main
==1==
Hello, World!
==1==
==1== HEAP SUMMARY:
==1==     in use at exit: 0 bytes in 0 blocks
==1==   total heap usage: 2 allocs, 2 frees, 4,196 bytes allocated
==1==
==1== All heap blocks were freed -- no leaks are possible
==1==
==1== For counts of detected and suppressed errors, rerun with: -v
==1== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
Container exited without errors (exit code: 0)
Done!
```

By default, `macgrind` will build a Docker image based on `ubuntu:18.04`. It will then build your project by running
`make all` in the project directory, then run the target using `valgrind --leak-check=full --error-exitcode=1
<target>`.

## more options

You can specify the image on which the container will be built by running `macgrind` with the `-i` (or `--image`)
option:

```text
$ macgrind my_c_project/ main --image ubuntu:16.04
```

Very often, projects depend on additional libraries. You can specify dependencies to be installed with `apt-get` using
the `-d` (or `--dependencies`) option:

```text
$ macgrind my_curl_c_project/ main --dependencies libcurl4-openssl-dev
```

If you wish to run a custom command to build your project or just one target, other than `make all`, you can specify
it using the `-c` (or `--custom-command`) option. Be aware, as with the executable, **the custom command must assume
a relative address, as it will be run inside of your project directory**:

```text
$ macgrind my_c_project/ main --custom-command "gcc src/main.c -o main"
```

To get the full option list, run:

```text
$ macgrind --help
```
