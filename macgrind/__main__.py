#!/usr/bin/env python3

##
## @package macgrind
## @author Dimitri Kokkonis ([\@kokkonisd](https://github.com/kokkonisd))
##
## This is the entry point for the `macgrind` tool.
##


import click
import docker
import os
import subprocess

from .definitions import VERSION, DEFAULT_DOCKERFILE
from .tools import info, warn, fail


@click.command()
@click.argument('project_dir', nargs=1)
@click.argument('target', nargs=1)
def main(project_dir, target):
    # Check if Docker is installed
    try:
        client = docker.from_env()
    except docker.errors.DockerException:
        fail('Docker failed to launch. You have either not yet installed Docker or it is currently not running.')

    # Create Dockerfile
    info('Creating temporary Dockerfile...')
    with open('Dockerfile', 'w') as dockerfile:
        dockerfile.write(DEFAULT_DOCKERFILE.format(project_dir, target))

    # Build image
    info('Building Docker image...')
    try:
        client.images.build(path='.', tag='macgrind-ubuntu-18_04')
    except docker.errors.BuildError:
        fail('Could not build container. Check for any compilation errors in your program.')

    # Remove Dockerfile
    subprocess.run(["rm", "-rf", "Dockerfile"])

    # Run container
    info('Running Docker container...')
    container = client.containers.run(image='macgrind-ubuntu-18_04', detach=True, auto_remove=True)

    # Print container output
    info('=' * 10)
    info("Here's the output of the container:")
    for log in container.logs(stream=True):
        print(log.decode('utf-8', errors='replace'), end='')

    # Get error code
    container_exit_code = container.wait()['StatusCode']

    # Fail if error code is non-zero
    if container_exit_code == 0:
        info('Container exited without errors (exit code: 0)')
    else:
        fail(f'Container exited with errors (exit code: {container_exit_code})')

    info("Done bitch!")


if __name__ == '__main__':
    main()
