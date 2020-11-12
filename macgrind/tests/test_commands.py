#!/env/bin/python3

import unittest
import subprocess
import sys

from macgrind.definitions import VERSION


class TestProjects(unittest.TestCase):

    def test_version(self):
        res = subprocess.run([sys.executable,
                              '-m',
                              'macgrind',
                              '--version'],
                              stdout=subprocess.PIPE)

        self.assertEqual(res.stdout.decode('utf-8')[:-1], f'macgrind, version {VERSION}')


    def test_ubuntu_1604_container(self):
        res = subprocess.run([sys.executable,
                              '-m',
                              'macgrind',
                              './macgrind/tests/dummy_projects/cproj_ok_simple/',
                              'main',
                              '-s',
                              '-i',
                              'ubuntu:16.04'])

        self.assertEqual(res.returncode, 0)


    def test_nonexistant_container(self):
        res = subprocess.run([sys.executable,
                              '-m',
                              'macgrind',
                              './macgrind/tests/dummy_projects/cproj_ok_simple/',
                              'main',
                              '-s',
                              '-i',
                              'notarealcontainer__macgrind__'])

        self.assertEqual(res.returncode, 1)


    def test_c_project_with_dependency(self):
        res = subprocess.run([sys.executable,
                              '-m',
                              'macgrind',
                              './macgrind/tests/dummy_projects/cproj_ok_curl_dep/',
                              'main',
                              '-s',
                              '-d',
                              'libcurl4-openssl-dev'])

        self.assertEqual(res.returncode, 0)

        # It should fail if the curl dependency is not specified
        res = subprocess.run([sys.executable,
                              '-m',
                              'macgrind',
                              './macgrind/tests/dummy_projects/cproj_ok_curl_dep/',
                              'main',
                              '-s'])

        self.assertEqual(res.returncode, 1)


    def test_c_project_custom_build_command(self):
        res = subprocess.run([sys.executable,
                              '-m',
                              'macgrind',
                              './macgrind/tests/dummy_projects/cproj_ok_simple/',
                              './main',
                              '-s',
                              '-c',
                              'gcc -c src/main.c -o main.o && gcc main.o -o main'])

        self.assertEqual(res.returncode, 0)


    def test_c_project_custom_run_commands(self):
        res = subprocess.run([sys.executable,
                              '-m',
                              'macgrind',
                              './macgrind/tests/dummy_projects/cproj_ok_simple/',
                              'build/main',
                              '-s',
                              '--run-before',
                              'mkdir -p build/',
                              '-c',
                              'gcc -c src/main.c -o build/main.o && gcc build/main.o -o build/main',
                              '--run-after',
                              'ls; rm -rf build/; ls'])

        self.assertEqual(res.returncode, 0)
