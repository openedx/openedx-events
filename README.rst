Open edX Events
===============

|pypi-badge| |ci-badge| |codecov-badge| |doc-badge| |pyversions-badge|
|license-badge|

Open edX Events from Hooks Extensions Framework (`OEP-50`_).

What is this project?

Overview
--------

This repository implements the necessary tooling and definitions used by the
Hooks Extension Framework to manage the events execution and extra tools.

Documentation
-------------

(TODO: `Set up documentation <https://openedx.atlassian.net/wiki/spaces/DOC/pages/21627535/Publish+Documentation+on+Read+the+Docs>`_)

Development Workflow
--------------------

One Time Setup
~~~~~~~~~~~~~~
.. code-block::

  # Clone the repository
  git clone git@github.com:edxuNEXT/openedx-events.git
  cd openedx-events

  # Set up a virtualenv using virtualenvwrapper with the same name as the repo and activate it
  mkvirtualenv -p python3.8 openedx-events


Every time you develop something in this repo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block::

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

  # Run your new tests
  pytest ./path/to/new/tests

  # Run all the tests and quality checks
  make validate

  # Commit all your changes
  git commit …
  git push

  # Open a PR and ask for review.

License
-------

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.

How To Contribute
-----------------

Contributions are very welcome.
Please read `How To Contribute <https://github.com/edx/edx-platform/blob/master/CONTRIBUTING.rst>`_ for details.
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

.. _Slack invitation: https://openedx-slack-invite.herokuapp.com/
.. _community Slack workspace: https://openedx.slack.com/
.. _Getting Help: https://openedx.org/getting-help
.. _OEP-50: https://open-edx-proposals.readthedocs.io/en/latest/oep-0050-hooks-extension-framework.html

.. |pypi-badge| image:: https://img.shields.io/pypi/v/openedx-events.svg
    :target: https://pypi.python.org/pypi/openedx-events/
    :alt: PyPI

.. |ci-badge| image:: https://github.com/eduNEXT/openedx-events/workflows/Python%20CI/badge.svg?branch=main
    :target: https://github.com/eduNEXT/openedx-events/actions
    :alt: CI

.. |codecov-badge| image:: https://codecov.io/github/eduNEXT/openedx-events/coverage.svg?branch=main
    :target: https://codecov.io/github/eduNEXT/openedx-events?branch=main
    :alt: Codecov

.. |doc-badge| image:: https://readthedocs.org/projects/openedx-events/badge/?version=latest
    :target: https://openedx-events.readthedocs.io/en/latest/
    :alt: Documentation

.. |pyversions-badge| image:: https://img.shields.io/pypi/pyversions/openedx-events.svg
    :target: https://pypi.python.org/pypi/openedx-events/
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/eduNEXT/openedx-events.svg
    :target: https://github.com/eduNEXT/openedx-events/blob/main/LICENSE.txt
    :alt: License
