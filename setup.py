#!/usr/bin/env python
"""
Package metadata for openedx_events.
"""
import os
import re
import sys

from setuptools import setup


def get_version(*file_paths):
    """
    Extract the version string from the file.

    Input:
     - file_paths: relative path fragments to file with
                   version string
    """
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    with open(filename) as file:
        version_file = file.read()
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.

    Returns:
        list: Requirements file relative path strings
    """
    requirements = set()
    for path in requirements_paths:
        with open(path) as file:
            requirements.update(
                line.split('#')[0].strip() for line in file.readlines()
                if is_requirement(line.strip())
            )
    return list(requirements)


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement.

    Returns:
        bool: True if the line is not blank, a comment, a URL, or
              an included file
    """
    return line and not line.startswith(('-r', '#', '-e', 'git+', '-c'))


VERSION = get_version('openedx_events', '__init__.py')

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (VERSION, VERSION))
    os.system("git push --tags")
    sys.exit()

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()
with open(os.path.join(os.path.dirname(__file__), 'CHANGELOG.rst')) as changelog:
    CHANGELOG = changelog.read()

setup(
    name='openedx-events',
    version=VERSION,
    description="""Open edX events from the Hooks Extensions Framework""",
    long_description=README + '\n\n' + CHANGELOG,
    long_description_content_type='text/x-rst',
    author='edX',
    author_email='oscm@edx.org',
    url='https://github.com/openedx/openedx-events',
    packages=[
        'openedx_events',
    ],
    include_package_data=True,
    install_requires=load_requirements('requirements/base.in'),
    python_requires=">=3.8",
    license="Apache 2.0",
    zip_safe=False,
    keywords='Python edx',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)
