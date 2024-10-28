Hooks Extension Framework
=========================

Overview
--------

Based on the `open-closed principle`_, this framework aims to extend the platform in a maintainable way without modifying its core. The main goal is to leverage the existing extension capabilities provided by the plugin architecture, allowing developers to implement new features to fit customer needs while reducing the need for core modifications and minimizing maintenance efforts.

Hooks: Open edX Events and Filters
----------------------------------

Hooks are a list of places in the Open edX platform where externally defined functions can take place. These functions may alter what the user sees or experiences on the platform, while in other cases, they are purely informative. All hooks are designed to be extended through Open edX plugins and configurations.

Hooks can be of two types: events and filters. Events are signals sent in specific places whose receivers can extend functionality, while filters are functions that can modify the application's behavior.

To allow extension developers to use the framework's definitions in their implementations, both kinds of hooks are defined in lightweight external libraries:

* `openedx-filters`_
* `openedx-events`_

The main goal of the framework is that developers can use it to change the platform's functionality as needed and still migrate to newer Open edX releases with little to no development effort. So, the framework is designed with stability in mind, meaning it is versioned and backward compatible as much as possible.

A longer description of the framework and its history can be found in `OEP 50`_.

Why use Open edX Hooks?
-------------------------------------- 

#. Stable and Maintainable Extensions

The Hooks Extension Framework allows developers to extend the platform's functionality in a stable, maintainable, and decoupled way ensuring easier upgrades and long-term stability by removing the need to modify the core in an significant way. 

#. Contained Solution Implementation

By avoiding core modifications, the framework promotes self-contained solutions, eliminating the need  for custom code to coexist with core logic which lowers maintenance costs for extension developers.

#. Leveraging the Open edX Plugin Extension Mechanism

The framework allows developers to implement custom business logic and integrations directly in plugins. This keeps core modifications minimal, focusing maintenance and development efforts on plugins, where solutions can be built and maintained independently of the core platform.

#. Standardization

Both filters and events implementations implement an approach for adding additional features, such as communication between components or services, or backend flow control. With these standards in place, it’s easy to identify when and how to use the framework as a solution, ensuring a consistent and predictable approach to extending the platform.

#. Reduce Fork Modifications

The need to modify logic in forks is minimized, as most extensions can now be implementing using the framework, keeping forks closer to the core and easier to manage.

#. Community Compatibility

The framework allows for shorter and more agile contribution cycles. By adding standardized extension points, contributors avoid creating customer-specific logic, making development more community-friendly.

#. Backward Compatibility

Hooks are designed to be backward compatible, guaranteeing stability across releases and making it easier to upgrade without breaking existing functionality.

.. _OEP 50: https://open-edx-proposals.readthedocs.io/en/latest/oep-0050-hooks-extension-framework.html
.. _openedx-filters: https://github.com/eduNEXT/openedx-filters
.. _openedx-events: https://github.com/eduNEXT/openedx-events
.. _open-closed principle: https://docs.openedx.org/projects/edx-platform/en/open-release-quince.master/concepts/extension_points.html
