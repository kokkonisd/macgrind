#!/env/bin/python3

import unittest
import subprocess
import sys


class TestProjects(unittest.TestCase):

    def test_c_project_ok_simple(self):
        # Run macgrind
        res = subprocess.run([sys.executable,
                              '-m',
                              'macgrind',
                              './macgrind/tests/dummy_projects/cproj_ok_simple/',
                              'main'])

        self.assertEqual(res.returncode, 0)


    def test_c_project_ko_simple(self):
        # Run macgrind
        res = subprocess.run([sys.executable,
                              '-m',
                              'macgrind',
                              './macgrind/tests/dummy_projects/cproj_ko_simple/',
                              'main',
                              '-s'])

        self.assertEqual(res.returncode, 1)


    def test_c_project_ko_syntax_error(self):
        # Run macgrind
        res = subprocess.run([sys.executable,
                              '-m',
                              'macgrind',
                              './macgrind/tests/dummy_projects/cproj_ko_syntax_error/',
                              'main',
                              '-s'])

        self.assertEqual(res.returncode, 1)
