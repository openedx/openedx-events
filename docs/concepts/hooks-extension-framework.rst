Hooks Extension Framework
=========================

Overview
--------

Based on the `open-closed principle`_, this framework aims to extend the platform in a maintainable way without modifying its core. The main goal is to leverage the existing extension capabilities provided by the plugin architecture, allowing developers to implement new features to fit customer needs while reducing the need for core modifications and minimizing maintenance efforts.

Hooks: Open edX Events and Filters
----------------------------------

Hooks are a list of places in the Open edX platform where externally defined functions can take place. These functions may alter what the user sees or experiences on the platform, while in other cases, they are purely informative. All hooks are designed to be extended through Open edX plugins and configurations.

Hooks can be of two types: events and filters. Events are signals sent in specific places whose listeners can extend functionality, while filters are functions that can modify the application's behavior.

To allow extension developers to use the framework's definitions in their implementations, both kinds of hooks are defined in lightweight external libraries:

* `openedx-filters`_
* `openedx-events`_

The main goal of the framework is that developers can use it to change the platform's functionality as needed and still migrate to newer Open edX releases with little to no development effort. So, the framework is designed with stability in mind, meaning it is versioned and backward compatible as much as possible.

A longer description of the framework and its history can be found in `OEP 50`_.

.. _OEP 50: https://open-edx-proposals.readthedocs.io/en/latest/oep-0050-hooks-extension-framework.html
.. _openedx-filters: https://github.com/eduNEXT/openedx-filters
.. _openedx-events: https://github.com/eduNEXT/openedx-events
.. _open-closed principle: https://docs.openedx.org/projects/edx-platform/en/open-release-quince.master/concepts/extension_points.html
