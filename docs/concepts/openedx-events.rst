Open edX Events
===============

Overview
--------

Open edX Events provide a mechanism for extending the platform by enabling developers to listen to Open edX-specific Django signals emitted by various services and respond accordingly. This allows for customized reactions to actions or changes within the platform without modifying the Open edX platform codebase, with the main goal of minimizing maintenance efforts for the Open edX project and plugin maintainers.

What are Open edX Events?
-------------------------

Open edX Events are signals emitted by a service (e.g., LMS, CMS, or others) within the Open edX ecosystem to notify that an action has occurred. For example, a user may have registered, logged in, or created a course.

These events are built on top of Django signals, inheriting their behavior while also incorporating metadata and actions specific to the Open edX ecosystem, making them uniquely suited for Open edX. Since they are essentially Django signals tailored to Open edX's specific needs, we can refer to `Django Signals Documentation`_ for a more detailed understanding of Open edX Events:

Django includes a “signal dispatcher” which helps decoupled applications get notified when actions occur elsewhere in the framework. In a nutshell, signals allow certain senders to notify a set of receivers that some action has taken place. They’re especially useful when many pieces of code may be interested in the same events.

Events are primarily used as a communication method between components within the same application process or with external services using the Event Bus technology, making them the standard communication mechanism within the Open edX ecosystem.

How do Open edX Events work?
----------------------------

Open edX Events are implemented by a class called ``OpenEdxPublicSignal``, which inherits from Django’s ``Signals`` class and adds behaviors specific to the Open edX ecosystem. Thanks to this design, ``OpenEdxPublicSignal`` leverages the functionality of Django signals, allowing developers to apply their existing knowledge of the Django framework.

The lifecycle of an Open edX Event can be summarized as follows:

1. A service emits an Open edX Event (an Open edX-specific Django signal) triggered by a specific action or event. The event data includes information about the event, such as the event name, timestamp, and other additional metadata.
2. Registered signal handlers listening to the event are called in response to the signal being emitted.
3. The signal handler performs additional processing or triggers other actions based on the event data.
4. The event is considered complete once all registered signal handlers have executed.

Here is an example of how that might look with an existing event:

1. A user enrolls in a course, `triggering the COURSE_ENROLLMENT_CREATED event`_. This event includes information about the user, course, and enrollment details.
2. A `signal handler listening`_ for the ``COURSE_ENROLLMENT_CREATED`` event is called and processes the event data.
3. The signal handler sends a notification to the user's email confirming their enrollment in the course.
4. The event is considered complete once the signal handler has finished processing the event.

The `Django Signals Documentation`_ provides a more detailed explanation of how Django signals work.

How are Open edX Events used?
-----------------------------

Developers can create handlers for Open edX Events by implementing Django signal handlers that respond to these events emitted by the Open edX platform. These signal handlers can be registered using Django's signal mechanism, allowing them to listen for events and execute custom logic in response.

For more information on using Open edX Events, refer to the `Using Open edX Events`_ how-to guide.

.. _Using Open edX Events: ../how-tos/using-events.html
.. _Django Signals Documentation: https://docs.djangoproject.com/en/4.2/topics/signals/
.. _triggering the COURSE_ENROLLMENT_CREATED event: https://github.com/openedx/edx-platform/blob/master/common/djangoapps/student/models/course_enrollment.py#L777-L795
.. _signal handler listening: https://github.com/openedx/edx-platform/blob/master/openedx/core/djangoapps/notifications/handlers.py#L38-L53
