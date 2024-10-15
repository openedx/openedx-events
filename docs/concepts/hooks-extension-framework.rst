Hooks Extension Framework
=========================

Overview
--------

To sustain the growth of the Open edX ecosystem, the business rules of the
platform must be open for extension following the open-closed principle. This
framework allows developers to do just that without needing to fork and modify
Open edX platform.

Hooks: Open edX Events and Filters
----------------------------------

Hooks are predefined places in the Open edX platform where externally defined
functions can take place. These functions may alter what the user
sees or experiences on the platform, while in other cases, they are purely informative. All
hooks are designed to be extended through Open edX plugins and configurations.

Hooks can be of two types, events and filters. Events are, in essence, signals
sent in specific places whose listeners can extend functionality. While filters
are functions that can modify the behavior of the application.

To allow extension developers to use the framework's definitions in their
implementations, both kinds of hooks are defined in lightweight external
libraries:

* `openedx-filters`_
* `openedx-events`_

The main goal of the framework is that developers can use them to change the
functionality of the platform as needed and still be able to migrate to newer
open releases with very little to no development effort, so they're designed
with stability in mind, meaning that they are versioned and backward compatible
as much as possible.

A longer description of the framework and its history can be found in `OEP 50`_.

.. _OEP 50: https://open-edx-proposals.readthedocs.io/en/latest/oep-0050-hooks-extension-framework.html
.. _openedx-filters: https://github.com/eduNEXT/openedx-filters
.. _openedx-events: https://github.com/eduNEXT/openedx-events
