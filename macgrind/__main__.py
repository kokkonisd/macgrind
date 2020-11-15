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
from io import BytesIO

from .definitions import VERSION, DEFAULT_DOCKERFILE, DOCKERFILE_NAME
from .tools import cleanup, info, warn, fail


@click.command()
@click.argument('project_dir', nargs=1)
@click.argument('target', nargs=1)
@click.option('-i',
              '--image',
              default='ubuntu:18.04',
              show_default=True,
              help='Docker image to run Valgrind in.')
@click.option('-d',
              '--dependencies',
              default='',
              help='Additional dependencies (to be installed with apt-get).')
@click.option('-c',
              '--custom-command',
              default='make all',
              show_default=True,
              help='Command to run in order to build the project.')
@click.option('--run-before',
              default=':', # : is the Bash no-op, if nothing is provided
              help='Command to run before building the project.')
@click.option('--run-after',
              default=':', # : is the Bash no-op, if nothing is provided
              help='Command to run after building the project & running Valgrind (Note: will only run if Valgrind '\
                   'returns 0).')
@click.option('-s',
              '--silent',
              is_flag=True,
              default=False,
              help='Silence all output.')
@click.version_option(version = VERSION,
                      prog_name = "macgrind")
def main(project_dir, target, image, dependencies, custom_command, run_before, run_after, silent):
    # Setup list of files to be cleaned up
    cleanup_files = [os.path.join(project_dir, DOCKERFILE_NAME)]

    # Check that project directory exists
    if not (os.path.exists(project_dir) and os.path.isdir(project_dir)):
        fail(f'Project directory `{project_dir}` either does not exist or is not a directory.',
             cleanup_files=cleanup_files)

    # Check if Docker is installed
    try:
        client = docker.from_env()
    except docker.errors.DockerException:
        if silent:
            fail('', cleanup_files=cleanup_files, end='')
        else:
            fail('Docker failed to launch. You have either not yet installed Docker or it is currently not running.',
                 cleanup_files=cleanup_files)

    # Create Dockerfile
    if not silent:
        info('Creating temporary Dockerfile...')
    # The Dockerfile must be created in the project's directory, because the `dockerfile` parameter on the build
    # command below is relative to the build path, and the build path must be equal to the path to the project's
    # diectory.
    with open(os.path.join(project_dir, DOCKERFILE_NAME), 'w') as dockerfile:
            # Create a Dockerfile
            dockerfile.write(DEFAULT_DOCKERFILE.format(image,
                                                       dependencies,
                                                       run_before,
                                                       custom_command,
                                                       target,
                                                       run_after))

    # Build image
    if not silent:
        info('Building Docker image...')
    try:
        # The path must be the project path, or else the files cannot be copied
        client.images.build(path=project_dir,
                            dockerfile=DOCKERFILE_NAME,
                            tag=f"macgrind-{image.replace(':', '_').replace('.', '-')}")
    except docker.errors.BuildError as err:
        # Remove Dockerfile if failed
        if silent:
            fail('', cleanup_files=cleanup_files, end='')
        else:
            fail(f'Could not build image. Possible reasons:\n'\
                 f'- Image `{image}` does not exist.\n'\
                 f'- You need to specify additional dependencies (use the `--dependencies` option).\n'\
                 f'- Your project has build errors.\n\n'\
                 f'Here is the error message returned by Docker:\n'\
                 f'{err}',
                 cleanup_files=cleanup_files)

    # Run container
    if not silent:
        info('Running Docker container...')
    container = client.containers.run(image=f"macgrind-{image.replace(':', '_').replace('.', '-')}",
                                      detach=True,
                                      auto_remove=True)

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
            fail('', cleanup_files=cleanup_files, end='')
        else:
            fail(f'Container exited with errors (exit code: {container_exit_code})',
                 cleanup_files=cleanup_files)

    # Clean up before exiting
    cleanup(cleanup_files)

    if not silent:
        info("Done!")


if __name__ == '__main__':
    main()
