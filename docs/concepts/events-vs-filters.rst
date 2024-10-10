Events vs Filters
=================

Open edX Events and Filters are two types of hooks that allow developers to
extend the functionality of the Open edX platform. They are defined in the
`openedx-events`_ and `openedx-filters`_ libraries respectively.

.. _openedx-events: https://github.com/openedx/openedx-events
.. _openedx-filters: https://github.com/openedx/openedx-filters

Events
------

Events are Open edX specific Django signals sent in specific places in the Open edX
platform. They allow external functions, known as signal handlers in the Django world,
to be executed when the event is triggered. These functions can extend the functionality of the platform or perform additional
processing based on the event data.

For a more detailed explanation of Open edX Events, see the `Open edX Events`_ document.

Filters
-------

Filters are functions that can modify the behavior of the application by
altering input data or halting execution based on specific conditions. They
allow developers to implement application flow control based on their business
login or requirements without directly modifying the application code.

For a more detailed explanation of Open edX Filters, see the `Open edX Filters`_ documentation.

Differences between Events and Filters
--------------------------------------

Here are some key differences between Open edX Events and Filters:

+-----------------+------------------------------------------------------------------------+-------------------------------------------------------------+-----+
|                 | Events                                                                 | Filters                                                     |     |
+=================+========================================================================+=============================================================+=====+
|| Purpose        || Trigger custom actions or processing in response to                   || Modify the behavior of the application by intercepting and ||    |
||                || specific events or actions within the platform,                       || altering the data or parameters passed to a specific       ||    |
||                || without affecting the application's flow.                             || function or method.                                        ||    |
+-----------------+------------------------------------------------------------------------+-------------------------------------------------------------+-----+
|| Usage          || Used to **extend** functionality via signal handlers when an event is || Used to intercept and **modify** the input or output of a  ||    |
||                || triggered.                                                            || component without directly modifying the component itself. ||    |
+-----------------+------------------------------------------------------------------------+-------------------------------------------------------------+-----+
|| Definition     || Defined using the `OpenEdxPublicSignal` class, which                  || Defined using the `OpenEdxFilter` class, which provides a  ||    |
||                || provides a structured way to define the data and                      || way to define the filter function and the parameters it    ||    |
||                || metadata associated with the event.                                   || should receive.                                            ||    |
+-----------------+------------------------------------------------------------------------+-------------------------------------------------------------+-----+
|| Implementation || Implemented using Django signals, which allow                         || Implemented using an accumulative pipeline mechanism which ||    |
||                || developers to send and receive notifications within                   || takes a set of arguments and returns a modified set of     ||    |
||                || a Django application.                                                 || arguments to the caller or raises exceptions during        ||    |
||                ||                                                                       || processing.                                                ||    |
+-----------------+------------------------------------------------------------------------+-------------------------------------------------------------+-----+
|| Example        || A custom event that triggers an email notification                    || A filter that modifies the data returned by a specific     ||    |
||                || when a user enrolls in a course.                                      || API endpoint to include additional information.            ||    |
+-----------------+------------------------------------------------------------------------+-------------------------------------------------------------+-----+

When to use an Open edX Event?
------------------------------

Use an Open edX Event when you need to:

- Trigger custom actions or processing in response to specific events or actions within the platform.
- Communicate or coordinate with other components or services based on specific events or actions.
- Synchronize data between different services or systems in response to specific events or actions.
- Notify users or external systems about specific events or actions within the platform.
- Integrate with external systems or services based on specific events or actions within the platform.

When to use an Open edX Filter?
-------------------------------

Use an Open edX Filter when:

- Modify the input or output of a specific function or method without directly modifying the function itself.
- Intercept and modify the data or parameters passed to a specific component or service.
- Apply a series of transformations or validations to the input or output of a specific function or method.
- Enforce specific constraints or business rules on the input or output of a specific function or method.
- Handle exceptions or errors that occur during the processing of a specific function or method.
- Apply a set of filters to the input or output of a specific function or method based on specific conditions or criteria.
