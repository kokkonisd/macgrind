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

from .definitions import VERSION, DEFAULT_DOCKERFILE, CUSTOM_COMMAND_DOCKERFILE
from .tools import cleanup, info, warn, fail


@click.command()
@click.argument('project_dir', nargs=1)
@click.argument('target', nargs=1)
@click.option('-i',
              '--image',
              default='ubuntu:18.04',
              show_default=True,
              help='Docker image to run Valgrind in.')
@click.option('-c',
              '--custom-command',
              help='Command to run in order to build the project.')
@click.option('-s',
              '--silent',
              is_flag=True,
              default=False,
              help='Silence all output.')
def main(project_dir, target, image, custom_command, silent):
    # Check that project directory exists
    if not (os.path.exists(project_dir) and os.path.isdir(project_dir)):
        fail(f'Project directory `{project_dir}` either does not exist or is not a directory.')

    # Check if Docker is installed
    try:
        client = docker.from_env()
    except docker.errors.DockerException:
        if silent:
            exit(1)
        else:
            fail('Docker failed to launch. You have either not yet installed Docker or it is currently not running.')

    # Create Dockerfile
    if not silent:
        info('Creating temporary Dockerfile...')
    with open('Dockerfile', 'w') as dockerfile:
        if custom_command:
            # Create a Dockerfile with a custom build command
            dockerfile.write(CUSTOM_COMMAND_DOCKERFILE.format(image, project_dir, custom_command, target))
        else:
            # Create a Dockerfile with a `make all` build command
            dockerfile.write(DEFAULT_DOCKERFILE.format(image, project_dir, target))

    # Build image
    if not silent:
        info('Building Docker image...')
    try:
        client.images.build(path='.', tag='macgrind-ubuntu-18_04')
    except docker.errors.BuildError:
        # Remove Dockerfile if failed
        if silent:
            exit(1)
        else:
            fail(f'Could not build image. Either image `{image}` does not exist or your project has build errors.')

    # Run container
    if not silent:
        info('Running Docker container...')
    container = client.containers.run(image='macgrind-ubuntu-18_04', detach=True, auto_remove=True)

    # Print container output
    if not silent:
        info('=' * 10)
        info("Here's the output of the container:")
        for log in container.logs(stream=True):
            print(log.decode('utf-8', errors='replace'), end='')

    # Get error code
    container_exit_code = container.wait()['StatusCode']

    # Fail if error code is non-zero
    if container_exit_code == 0:
        if not silent:
            info('Container exited without errors (exit code: 0)')
    else:
        if silent:
            exit(1)
        else:
            fail(f'Container exited with errors (exit code: {container_exit_code})')

    # Clean up before exiting
    cleanup()

    if not silent:
        info("Done!")


if __name__ == '__main__':
    main()
