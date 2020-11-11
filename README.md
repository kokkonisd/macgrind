# macgrind

Containerized Valgrind on OSX for C and C++ projects.


## why

As of the time of writing this, [Valgrind]() is not natively supported on OSX. This tool allows you to run it in a
[Docker]() container without any code changes or extra garbage.


## how to install

You can install `macgrind` via `pip`:

```text
$ pip3 install macgrind
```

You also need to install [Docker Desktop](), and have it running.


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
`my_c_project/`). The assumption here is that the `all` target in the `Makefile` builds `my_c_project/main`.

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
