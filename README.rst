Open edX Events
###############

|pypi-badge| |ci-badge| |codecov-badge| |doc-badge| |pyversions-badge|
|license-badge| |status-badge|

Open edX Events from Hooks Extensions Framework (`OEP-50`_).

.. _OEP-50: https://open-edx-proposals.readthedocs.io/en/latest/oep-0050-hooks-extension-framework.html

Purpose
*******

This repository implements the necessary tooling and definitions used by the
Hooks Extension Framework to manage the events execution and extra tools.

Getting Started
***************

Developing
==========

One Time Setup
--------------
.. code-block::

  # Clone the repository
  git clone git@github.com:openedx/openedx-events.git
  cd openedx-events

  # Set up a virtualenv using virtualenvwrapper with the same name as the repo and activate it
  mkvirtualenv -p python3.8 openedx-events

Every time you develop something in this repo
---------------------------------------------
.. code-block::

  # Activate the virtualenv
  workon openedx-events

  # Grab the latest code
  git checkout main
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

Deploying
=========

The Open edX Events component is a Python library which doesn't need independent deployment. Therefore,
its setup is reasonably straightforward. First, it needs to be added to your service requirements,
and then it will be installed alongside requirements of the service.

If the service you intend to use is either the LMS or CMS, then the library is installed alongside
their requirements since the Maple release.

Getting Help
************

Documentation
=============

See `documentation on Read the Docs <https://openedx-events.readthedocs.io/en/latest/>`_.

More Help
=========

If you're having trouble, we have discussion forums at
https://discuss.openedx.org where you can connect with others in the
community.

Our real-time conversations are on Slack. You can request a `Slack
invitation`_, then join our `community Slack workspace`_.

For anything non-trivial, the best path is to open an issue in this
repository with as many details about the issue you are facing as you
can provide.

https://github.com/openedx/openedx-events/issues

For more information about these options, see the `Getting Help`_ page.

.. _Slack invitation: https://openedx.org/slack
.. _community Slack workspace: https://openedx.slack.com/
.. _Getting Help: https://openedx.org/getting-help

License
*******

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.

Contributing
************

Contributions are very welcome.
Please read `How To Contribute <https://openedx.org/r/how-to-contribute>`_ for details.

This project is currently accepting all types of contributions, bug fixes,
security fixes, maintenance work, or new features.  However, please make sure
to have a discussion about your new feature idea with the maintainers prior to
beginning development to maximize the chances of your change being accepted.
You can start a conversation by creating a new issue on this repo summarizing
your idea.

The Open edX Code of Conduct
****************************

All community members are expected to follow the `Open edX Code of Conduct`_.

.. _Open edX Code of Conduct: https://openedx.org/code-of-conduct/

People
******

The assigned maintainers for this component and other project details may be
found in `Backstage`_. Backstage pulls this data from the ``catalog-info.yaml``
file in this repo.

.. _Backstage: https://backstage.openedx.org/catalog/default/component/openedx-events

Reporting Security Issues
*************************

Please do not report security issues in public. Please email security@tcril.org.

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

.. |status-badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen
