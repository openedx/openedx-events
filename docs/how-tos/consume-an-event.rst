.. include:: ../common_refs.rst

.. _Consume an Event:

Consume an Open edX Event
##########################

You have two ways of consuming an Open edX event: within the same service or in a different service. In this guide, we will show you how to consume an event within the same service. For consuming events across services, see :ref:`Use the Open edX Event Bus to Broadcast and Consume Events`.

.. note:: We encourage you to also consider the practices outlined in the :ref:`ADR-16` ADR for event consumption.

Throughout this guide, we will implement the use case to send the enrollment data to a webhook when a user enrolls in a course to better illustrate the steps involved in creating a consumer for an event.

Assumptions
************

- You have a development environment set up using `Tutor`_.
- You have a basic understanding of Python and Django.
- You have a basic understanding of Django signals. If not, you can review the `Django Signals Documentation`_.
- You are familiar with the terminology used in the project, such as the terms :term:`Event Type` or :term:`Event Receiver`. If not, you can review the :ref:`Glossary` documentation.

Steps
*******

To consume an event within the same service, follow these steps:

Step 1: Understand your Use Case and Identify the Event to Consume
===================================================================

Before you start consuming an event, you should understand the use case and the event you want to consume, for this review the `list of events`_ available in the Open edX platform. In this case, we want to send the enrollment data to a webhook when a user enrolls in a course. You should review the event definition and payload to understand the data that is being passed to the event receiver and how you can use it to implement the custom logic.

In our example, we want to send the enrollment data to a webhook when a user enrolls in a course. We will consume the ``COURSE_ENROLLMENT_CREATED`` event, which is triggered every time a user enrolls in a course. You can review the event definition and payload to understand the data that is being passed to the event receiver and how you can use it to implement the request to the webhook.

Step 2: Install Open edX Events
================================

First, add the ``openedx-events`` plugin into your dependencies so the library's environment recognizes the event you want to consume. You can install ``openedx-events`` by running:

.. code-block:: bash

   pip install openedx-events

This will mainly make the events available for your CI/CD pipeline and local development environment. If you are using the Open edX platform, the library should already be installed in the environment, so there is no need to install it.

Step 3: Create an Event Receiver and Connect it to the Event
=============================================================

An :term:`Event Receiver` is simply a function that listens for a specific event and executes custom logic in response to the event being triggered. You can create an event receiver by using the Django signals `receiver`_ decorator. Here's an example of an event receiver that listens for the ``COURSE_ENROLLMENT_CREATED`` event and creates a notification preference for the user:

.. code-block:: python

    from openedx_events import COURSE_ENROLLMENT_CREATED
    from django.dispatch import receiver

    @receiver(COURSE_ENROLLMENT_CREATED)
    def send_enrollment_data_to_webhook(signal, sender, enrollment, metadata, **kwargs):
        # Custom logic to send enrollment data to a webhook
        pass

- The Django dispatcher will call the ``send_enrollment_data_to_webhook`` function when the ``COURSE_ENROLLMENT_CREATED`` event is triggered by using the ``receiver`` decorator. In this case, that would be every time a user enrolls in a course.
- Consider using asynchronous tasks to handle the event processing to avoid blocking the main thread and improve performance. Also, make sure to handle exceptions and errors gracefully to avoid silent failures and improve debugging. It is recommended to not create a tight coupling between receivers and other services. If doing so is necessary, consider using the event bus to broadcast the event.
- When implementing the receiver, inspect the event payload to understand the data that is being passed to the event receiver by reviewing the ``data.py`` file of the event you are consuming. For example, the ``COURSE_ENROLLMENT_CREATED`` event has the following payload:

.. code-block:: python

    # Location openedx_events/learning/data.py
    COURSE_ENROLLMENT_CREATED = OpenEdxPublicSignal(
        event_type="org.openedx.learning.course.enrollment.created.v1",
        data={
            "enrollment": CourseEnrollmentData,
        }
    )

- This event has a single field called ``enrollment``, which is an instance of the ``CourseEnrollmentData`` class. You can review the ``CourseEnrollmentData`` class to understand the data that is available to you and how you can use it to implement the custom logic.
- The ``metadata`` parameter contains the Open edX-specific metadata for the event, such as the event version and timestamp when the event was sent. You can use this metadata to understand more about the event and its context.

These event receivers are usually implemented independently of the service in an `Open edX Django plugin`_ and are registered in the ``handlers.py`` (according to `OEP-49`_) file of the plugin. You can review the ``handlers.py`` file of the `openedx-events-2-zapier`_ plugin to understand how the event receivers are implemented and connected to the events.

Consider the following when implementing the event receiver:

- Limit each receiver to a single responsibility to make the code easier to maintain and test.
- Keep the receiver logic simple and focused on the specific task it needs to perform.
- Consider the performance implications of the receiver and avoid adding unnecessary complexity or overhead, considering that receivers will be executed each time the event is triggered. Consider using asynchronous tasks to handle the event processing to avoid blocking the main thread and improve performance.
- Implement error handling and logging in the pipeline step to handle exceptions and provide useful information for debugging, considering both development and production environments.

Step 4: Test the Event Receiver
================================

Given the design of Open edX Events, you can include the events' definitions in your test suite to ensure that the event receiver is working as expected. You can use the ``send_event`` method to trigger the event and test the event receiver. Here's an example of how you can test the event receiver:

.. code-block:: python

    from openedx_events.learning.signals import COURSE_ENROLLMENT_CREATED
    from openedx_events.learning.data import CourseData, CourseEnrollmentData, UserData, UserPersonalData

    def test_send_enrollment_data_to_webhook(self):
        # Trigger the event
        enrollment_data = CourseEnrollmentData(
            user=UserData(
                pii=UserPersonalData(
                    username=self.user.username,
                    email=self.user.email,
                    name=self.user.profile.name,
                ),
                id=self.user.id,
                is_active=self.user.is_active,
            ),
            course=CourseData(
                course_key=self.course.id,
                display_name=self.course.display_name,
            ),
            mode=self.course_enrollment.mode,
            is_active=self.course_enrollment.is_active,
            creation_date=self.course_enrollment.created,
        )

        COURSE_ENROLLMENT_CREATED.send_event(
            enrollment=enrollment_data
        )

        # Assert that the request was sent to the webhook with the correct data

- In the test suite, you can use the ``send_event`` method to trigger the event and pass the necessary data to the event receiver. In this case, we pass the user, course, and enrollment data to the event receiver as the triggering logic would.
- After triggering the event, you can assert that the event receiver executed the custom logic as expected. In this case, we check that the request was sent to the webhook with the correct data.

You can review this example to understand how you can test the event receiver and ensure that the custom logic is executed when the event is triggered in the `openedx-events-2-zapier`_ plugin.

This way you can ensure that the event receiver is working as expected and that the custom logic is executed when the event is triggered. If the event definition or payload changes in any way, you can catch the error in the test suite instead of in production.

.. _Open edX Django plugin: https://docs.openedx.org/en/latest/developers/concepts/platform_overview.html#new-plugin
.. _OEP-49: https://docs.openedx.org/projects/openedx-proposals/en/latest/best-practices/oep-0049-django-app-patterns.html#signals
.. _list of events: https://docs.openedx.org/projects/openedx-events/en/latest/reference/events.html
.. _receiver: https://docs.djangoproject.com/en/4.2/topics/signals/#django.dispatch.receiver

**Maintenance chart**

+--------------+-------------------------------+----------------+--------------------------------+
| Review Date  | Reviewer                      |   Release      |Test situation                  |
+--------------+-------------------------------+----------------+--------------------------------+
|2025-02-10    | Maria Grimaldi                |   Sumac        |Pass.                           |
+--------------+-------------------------------+----------------+--------------------------------+
