Open edX Events
===============

|pypi-badge| |ci-badge| |codecov-badge| |doc-badge| |pyversions-badge|
|license-badge|

Open edX Events from Hooks Extensions Framework (`OEP-50`_).

Overview
--------

This repository implements the necessary tooling and definitions used by the
Hooks Extension Framework to manage the events execution and extra tools.

Getting started
---------------

Dependencies
~~~~~~~~~~~~

Dependencies of the current version of the library:

- attrs
- Django
- edx-opaque-keys
- fastavro

Installation
~~~~~~~~~~~~

.. code-block:: bash

    # Install from PyPi
    pip install openedx-events==<RELEASE>

    # Install from GitHub Repository
    pip install git+https://github.com/openedx/openedx-events.git@<TAG or BRANCH>

Development Workflow
~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

  # Clone the repository
  git clone git@github.com:openedx/openedx-events.git
  cd openedx-events

  # Set up a virtualenv using virtualenvwrapper with the same name as the repo and activate it
  mkvirtualenv -p python3.8 openedx-events

  # Activate the virtualenv
  workon openedx-events

  # Grab the latest code
  git checkout master
  git pull

  # Install/update the dev requirements
  make requirements

  # Run the tests and quality checks (to verify the status before you make any changes)
  make validate

  # Make a new branch for your changes
  git checkout -b <your_github_username>/<short_description>

  # Using your favorite editor, edit the code to make your change.
  vim …

  # Commit all your changes
  git commit …
  git push

  # Open a PR and ask for review.

Running the tests
~~~~~~~~~~~~~~~~~

.. code-block:: bash

  # Run your new tests
  pytest ./path/to/new/tests

  # Run all the tests and quality checks
  make validate


Getting help
------------

Documentation
~~~~~~~~~~~~~

See `documentation on Read the Docs <https://openedx-events.readthedocs.io/en/latest/>`_.

License
-------

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.

How To Contribute
-----------------

Contributions are very welcome.
Please read `How To Contribute <https://github.com/openedx/edx-platform/blob/master/CONTRIBUTING.rst>`_ for details.
Even though they were written with ``edx-platform`` in mind, the guidelines
should be followed for all Open edX projects.

The pull request description template should be automatically applied if you are creating a pull request from GitHub. Otherwise you
can find it at `PULL_REQUEST_TEMPLATE.md <.github/PULL_REQUEST_TEMPLATE.md>`_.

The issue report template should be automatically applied if you are creating an issue on GitHub as well. Otherwise you
can find it at `ISSUE_TEMPLATE.md <.github/ISSUE_TEMPLATE.md>`_.

Reporting Security Issues
-------------------------

Please do not report security issues in public. Please email security@edx.org.

Getting Help
------------

If you're having trouble, we have discussion forums at https://discuss.openedx.org where you can connect with others in the community.

Our real-time conversations are on Slack. You can request a `Slack invitation`_, then join our `community Slack workspace`_.

For more information about these options, see the `Getting Help`_ page.

Additional Resources
--------------------

- For a detailed description of the project, refer to the `OEP-50`_.
- For usage samples, please refer to `openedx-events-2-zapier`_.
- For general guidance, refer to the `Hooks Extension Framework guide`.
- For implementation details, refer to the `BD-32 pull requests`_ on the Open edX platform and this library.
- For architectural design details, refer the current `ADRs`_.

.. _Slack invitation: https://openedx.org/slack
.. _community Slack workspace: https://openedx.slack.com/
.. _Getting Help: https://openedx.org/getting-help
.. _OEP-50: https://open-edx-proposals.readthedocs.io/en/latest/oep-0050-hooks-extension-framework.html
.. _openedx-events-2-zapier: https://github.com/eduNEXT/openedx-events-2-zapier
.. _ Hooks Extension Framework: https://github.com/openedx/edx-platform/tree/master/docs/guides/hooks
.. _ BD-32 pull requests: https://github.com/openedx/edx-platform/pulls?q=is%3Apr+%22BD-32%22
.. _ ADRs: https://github.com/openedx/openedx-events/tree/main/docs/decisions

.. |pypi-badge| image:: https://img.shields.io/pypi/v/openedx-events.svg
    :target: https://pypi.python.org/pypi/openedx-events/
    :alt: PyPI

.. |ci-badge| image:: https://github.com/openedx/openedx-events/workflows/Python%20CI/badge.svg?branch=main
    :target: https://github.com/openedx/openedx-events/actions
    :alt: CI

.. |codecov-badge| image:: https://codecov.io/github/openedx/openedx-events/coverage.svg?branch=main
    :target: https://codecov.io/github/openedx/openedx-events?branch=main
    :alt: Codecov

.. |doc-badge| image:: https://readthedocs.org/projects/openedx-events/badge/?version=latest
    :target: https://openedx-events.readthedocs.io/en/latest/
    :alt: Documentation

.. |pyversions-badge| image:: https://img.shields.io/pypi/pyversions/openedx-events.svg
    :target: https://pypi.python.org/pypi/openedx-events/
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/openedx/openedx-events.svg
    :target: https://github.com/openedx/openedx-events/blob/main/LICENSE.txt
    :alt: License
