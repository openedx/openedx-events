Open edX Events
===============

Overview
--------

Open edX Events provide a mechanism for extending the platform by enabling developers to listen to Open edX-specific Django signals emitted by various services and respond accordingly. This allows for customized reactions to actions or changes within the platform without modifying the Open edX platform codebase, with the main goal of minimizing maintenance efforts for the Open edX project and plugin maintainers.

What are Open edX Events?
-------------------------

Open edX Events are signals emitted by a service (e.g., LMS, CMS, or others) within the Open edX ecosystem to notify that an action has occurred. For example, a user may have registered, logged in, or created a course.

These events are built on top of Django signals, inheriting their behavior while also incorporating metadata and actions specific to the Open edX ecosystem, making them uniquely suited for Open edX. Since they are essentially Django signals tailored to Open edX's specific needs, we can refer to `Django Signals Documentation`_ for a more detailed understanding of Open edX Events:

Django includes a "signal dispatcher" which helps decoupled applications get notified when actions occur elsewhere in the framework. In a nutshell, signals allow certain senders to notify a set of receivers that some action has taken place. They’re especially useful when many pieces of code may be interested in the same events.

Events are primarily used as a communication method between components within the same application process or with external services using the `Event Bus technology`_, making them the standard communication mechanism within the Open edX ecosystem.

How do Open edX Events work?
----------------------------

Open edX Events are implemented by a class called `OpenEdxPublicSignal`_, which inherits from `Django's Signals class` and adds behaviors specific to the Open edX ecosystem. Thanks to this design, ``OpenEdxPublicSignal`` leverages the functionality of Django signals, allowing developers to apply their existing knowledge of the Django framework.

The event execution process follows these steps:

#. An application component emits an event by calling the `send_event` method implemented by `OpenEdxPublicSignal`_.

#. The class generates Open edX-specific metadata for the event on the fly, like the event version or the timestamp when the event was sent. The event receivers use this metadata during their processing.

#. The tooling uses the `send or send_robust`_ method from Django signals under the hood. The `send`` method is used for development and testing, while the `send_robust` method is used in production to ensure receivers don't raise exceptions halting the application process.

#. Building on Django signals allows us to use the same `Django signals registry mechanism`_ for receiver management. This means that developers can register `signal receivers in their plugins`_ for Open edX Events in the same way they would for Django signals.

#. The event is sent to all registered receivers, which are executed in the order they were registered. Each receiver processes the event data and performs the necessary actions.

#. After all receivers for the event have been executed, the process continues with the application logic.

Here is an example of an event that saves a user's notification preferences when they enroll in a course:

#. A user enrolls in a course, `triggering the COURSE_ENROLLMENT_CREATED event`_. This event includes information about the user, course, and enrollment details.

#. A signal receiver listening for the ``COURSE_ENROLLMENT_CREATED`` event is called and processes the event data.  In this case, it would be the `course_enrollment_post_save receiver`_.

#. The signal receiver creates a notification preference for the user, enabling them to receive notifications about the course.

#. The application continues with the course enrollment process.

The `Django Signals Documentation`_ provides a more detailed explanation of how Django signals work.

How are Open edX Events used?
-----------------------------

Developers can listen to Open edX Events by registering signal receivers from their Open edX Django plugins that respond to the emitted events. This is done using Django's signal mechanism, which allows developers to listen for events and execute custom logic in response.

For more information on using Open edX Events, refer to the `Using Open edX Events`_ how-to guide.

.. _Using Open edX Events: ../how-tos/using-events.html
.. _Django Signals Documentation: https://docs.djangoproject.com/en/4.2/topics/signals/
.. _triggering the COURSE_ENROLLMENT_CREATED event: https://github.com/openedx/edx-platform/blob/master/common/djangoapps/student/models/course_enrollment.py#L777-L795
.. _course_enrollment_post_save receiver: https://github.com/openedx/edx-platform/blob/master/openedx/core/djangoapps/notifications/handlers.py#L38-L53
.. _Event Bus technology: https://openedx.atlassian.net/wiki/spaces/AC/pages/3508699151/How+to+start+using+the+Event+Bus
.. _Django signals registry mechanism: https://docs.djangoproject.com/en/4.2/topics/signals/#listening-to-signals
.. _signal receivers in their plugins: https://edx.readthedocs.io/projects/edx-django-utils/en/latest/edx_django_utils.plugins.html#edx_django_utils.plugins.constants.PluginSignals
.. _Open edX Django plugins: https://edx.readthedocs.io/projects/edx-django-utils/en/latest/plugins/readme.html
.. _OpenEdxPublicSignal: https://github.com/openedx/openedx-events/blob/main/openedx_events/tooling.py#L37
.. _Django's Signals class: https://docs.djangoproject.com/en/4.2/topics/signals/#defining-and-sending-signals
.. _send_event: https://github.com/openedx/openedx-events/blob/main/openedx_events/tooling.py#L185
.. _send: https://docs.djangoproject.com/en/4.2/topics/signals/#sending-signals
