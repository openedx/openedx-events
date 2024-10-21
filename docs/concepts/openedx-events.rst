Open edX Events
===============

Overview
--------

In the context of Open edX, events provide a mechanism for extending the platform by enabling developers to listen to Open edX-specific Django signals emitted by various services and respond accordingly. This allows for customized reactions to key actions or changes within the platform without modifying the Open edX platform codebase. 

What are Open edX Events?
-------------------------

An Open edX Event is an Open edX-specific Django signal emitted by a service when a specific action or event occurs. These signals notify other services or components of the platform that an event has taken place, allowing them to respond accordingly. Open edX Events are the current standard for communication between components and services within the Open edX ecosystem.

How do Open edX Events work?
----------------------------

Events are defined using the ``OpenEdxPublicSignal`` class, which provides a structured way to define the data and metadata associated with the event and other relevant information. This class is built on top of the ``Signal`` Django class, which provides a way to send and receive notifications when an action takes place within the Open edX ecosystem. Due to this design, Open edX Events follow the Django signal pattern, allowing developers to leverage their existing knowledge of the framework.

The lifecycle of an Open edX Event can be summarized as follows:

1. A service emits an Open edX Event (an Open edX-specific Django signal) triggered by a specific action or event. The event data includes information about the event, such as the event name, timestamp, and other additional metadata.
2. Registered signal handlers listening to the event are called in response to the signal being emitted.
3. The signal handler performs additional processing or triggers other actions based on the event data.
4. The event is considered complete once all registered signal handlers have executed.

Here is an example of how that might look like with an existing event:

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
