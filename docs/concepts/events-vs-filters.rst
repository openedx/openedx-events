Events vs Filters
=================

Open edX Events and Filters are two types of hooks that allow developers to extend the functionality of the Open edX platform. They are defined in the `openedx-events`_ and `openedx-filters`_ libraries respectively.

.. _openedx-events: https://github.com/openedx/openedx-events
.. _openedx-filters: https://github.com/openedx/openedx-filters

Events
------

Events are Open edX-specific Django signals sent in specific places on the Open edX platform. They allow developers to listen to these signals and perform additional processing based on the event data.

For a more detailed explanation of Open edX Events, see the rest of the Open edX Events documentation.

Filters
-------

Filters are functions that can modify the application's behavior by altering input data or halting execution based on specific conditions. They allow developers to implement application flow control based on their business logic or requirements without directly modifying the application code.

For a more detailed explanation of Open edX Filters, see the `Open edX Filters`_ documentation.

.. _Open edX Filters: https://docs.openedx.org/projects/openedx-filters/en/latest/

Differences between Events and Filters
--------------------------------------

Here are some key differences between Open edX Events and Filters:

+--------------------+------------------------------------------------------------------------+-------------------------------------------------------------+
|                    | Events                                                                 | Filters                                                     |
+====================+========================================================================+=============================================================+
| **Purpose**        | Notify when an action occurs in a specific part of the                 | Alter the application flow control.                         |
|                    | application.                                                           |                                                             |
+--------------------+------------------------------------------------------------------------+-------------------------------------------------------------+
|  **Usage**         | Used to **extend** functionality via signal handlers when an event is  |  Used to intercept and **modify** the data used within a    |
|                    | triggered.                                                             |  component without directly modifying the application       |
|                    |                                                                        |  itself.                                                    |
+--------------------+------------------------------------------------------------------------+-------------------------------------------------------------+
|  **Definition**    |  Defined using the `OpenEdxPublicSignal` class, which                  |  Defined using the ``OpenEdxPublicFilter`` class,           |
|                    |  provides a structured way to define the data and                      |  which provides a way to define the filter function         |
|                    |  metadata associated with the event.                                   |  and the parameters it should receive.                      |
+--------------------+------------------------------------------------------------------------+-------------------------------------------------------------+
| **Implementation** |  Implemented using Django signals, which allow                         |  Implemented using an accumulative pipeline mechanism which |
|                    |  developers to send and receive notifications that an action happened  |  takes a set of arguments and returns a modified set        |
|                    |  within a Django application.                                          |  to the caller or raises exceptions during                  |
|                    |                                                                        |  processing.                                                |
+--------------------+------------------------------------------------------------------------+-------------------------------------------------------------+
| **Use cases**      |  Send an email notification when a user enrolls in a course.           |  Include additional information in an API endpoint response.|
|                    |  an email notification.                                                |                                                             |
+--------------------+------------------------------------------------------------------------+-------------------------------------------------------------+

When to use an Open edX Event?
------------------------------

Use an Open edX Event when you need to:

- Trigger custom logic or processing in response to specific actions within the platform, e.g., updating a search index after a course block is modified.
- Communicate, synchronize, or coordinate with other components or services based on specific events or actions, e.g., send certificate data from LMS to credentials service to keep models up to date.
- Integrate with external systems or services based on specific events or actions within the platform, e.g., send user data to third-party services upon registration for marketing purposes.

In summary, events can be used to integrate application components with each other or with external services, allowing them to communicate, synchronize, and perform additional actions when specific triggers occur.

When to use an Open edX Filter?
-------------------------------

Use an Open edX Filter when:

- Enrich the data or parameters passed to a specific component, e.g., fetch reusable LTI configurations from external plugins.
- Intercept and modify the input of a specific component, e.g., include "Edit" link to an HTML block if certain conditions are met.
- Enforce specific constraints or business rules on the input or output of a specific function or method, e.g., prevent enrollment for non-authorized users.

In summary, filters can be used when implementing application flow control that modifies the application's behavior, navigation, or user interaction flow during runtime.
