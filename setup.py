import setuptools

from macgrind.definitions import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "macgrind",
    version = VERSION,
    author = "Dimitri Kokkonis",
    author_email = "kokkonisd@gmail.com",
    description = "A containerized version of Valgrind for OSX.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/kokkonisd/macgrind",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires = [ "click", "docker" ],
    package_data = {'macgrind': []},
    include_package_data = True,
    entry_points = {'console_scripts': [
        'macgrind = macgrind.__main__:main',
    ], },
)
