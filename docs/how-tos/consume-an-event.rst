Consume an Open edX Event
=========================

You have two ways of consuming an Open edX event, within the same service or in a different service. In this guide, we will show you how to consume an event within the same service. For consuming events across services, see :doc:`../how-tos/use-the-event-bus-to-broadcast-and-consume-events`.

.. note:: We encourage you to also consider the practices outlined in the :doc:`../decisions/0016-event-design-practices` ADR for event consumption.

Throughout this guide, we will implement the use case to send the enrollment data to a webhook when a user enrolls in a course to better illustrate the steps involved in creating a consumer for an event.

Assumptions
-----------

- You have a development environment set up using `Tutor`_.
- You have a basic understanding of Python and Django.
- You have created a new Open edX event. If not, you can follow the :doc:`../how-tos/create-a-new-event` guide to create a new event.
- You have a basic understanding of Django signals. If not, you can review the `Django Signals Documentation`_.
- You are familiar with the terminology used in the project, such as the terms :term:`Event Type` or :term:`Event Receiver`. If not, you can review the :doc:`../reference/glossary` documentation.

Steps
-----

To consume an event within the same service, follow these steps:

Step 1: Understand your Use Case
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before you start consuming an event, you should understand the use case and the event you want to consume. In this case, we want to send the enrollment data to a webhook when a user enrolls in a course. You should review the event definition and payload to understand the data that is being passed to the event receiver and how you can use it to implement the custom logic.

In our example, we want to send the enrollment data to a webhook when a user enrolls in a course. We will consume the ``COURSE_ENROLLMENT_CREATED`` event, which is triggered every time a user enrolls in a course. You can review the event definition and payload to understand the data that is being passed to the event receiver and how you can use it to implement the request to the webhook.

Step 2: Install Open edX Events
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, add the ``openedx-events`` plugin into your dependencies so the library's environment recognizes the event you want to consume. You can install ``openedx-events`` by running:

.. code-block:: bash

   pip install openedx-events

This will mainly make the events available for your CI/CD pipeline and local development environment. If you are using the Open edX platform, the library should be already be installed in the environment so no need to install it.

Step 3: Create a Event Receiver and Connect it to the Event
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An :term:`Event Receiver` is simply a function that listens for a specific event and executes custom logic in response to the event being triggered. You can create an event receiver by using the Django signal receivers decorator. Here's an example of an event receiver that listens for the ``COURSE_ENROLLMENT_CREATED`` event and creates a notification preference for the user:

.. code-block:: python

    from openedx_events import COURSE_ENROLLMENT_CREATED
    from django.dispatch import receiver

    @receiver(COURSE_ENROLLMENT_CREATED)
    def send_enrollment_data_to_webhook(signal, sender, enrollment, metadata, **kwargs):
        # Custom logic to send enrollment data to a webhook
        pass

- The Django dispatcher will call the ``send_enrollment_data_to_webhook`` function when the ``COURSE_ENROLLMENT_CREATED`` event is triggered by using the ``receiver`` decorator. In this case, that would be every time a user enrolls in a course.
- Consider using asynchronous tasks to handle the event processing to avoid blocking the main thread and improve performance. Also, make sure to handle exceptions and errors gracefully to avoid silent failures and improve debugging. You should also consider not creating a tight coupling between receivers and other services, if doing so is necessary consider using the event bus to broadcast the event.
- When implementing the receiver, inspect the event payload to understand the data that is being passed to the event receiver by reviewing the ``data.py`` file of the event you are consuming. For example, the ``COURSE_ENROLLMENT_CREATED`` event has the following payload:

.. code-block:: python

    # Location openedx_events/learning/data.py
    COURSE_ENROLLMENT_CREATED = OpenEdxPublicSignal(
        event_type="org.openedx.learning.course.enrollment.created.v1",
        data={
            "enrollment": CourseEnrollmentData,
        }
    )

- This event has a single field called ``enrollment`` which is an instance of the ``CourseEnrollmentData`` class. You can review the ``CourseEnrollmentData`` class to understand the data that is available to you and how you can use it to implement the custom logic.
- The ``metadata`` parameter contains the Open edX-specific metadata for the event, such as the event version and timestamp when the event was sent. You can use this metadata to understand more about the event and its context.

These event receivers are usually implemented independently of the service in an `Open edX Django plugins`_ and are registered in the ``handlers.py`` (according to `OEP-49`_) file of the plugin. You can review the ``handlers.py`` file of the openedx-events-2-zapier_ plugin to understand how the event receivers are implemented and connected to the events.

.. TODO: change receivers.py in openedx-events-2-zapier to handlers.py

Step 4: Test the Event Receiver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Given the design of Open edX Events, you can include the events definitions in your test suite to ensure that the event receiver is working as expected. You can use the ``send_event`` method to trigger the event and test the event receiver. Here's an example of how you can test the event receiver:

.. code-block:: python

    from openedx_events import send_event, COURSE_ENROLLMENT_CREATED

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

- In the test suite, you can use the ``send_event`` method to trigger the event and pass the necessary data to the event receiver. In this case, we are passing the user, course and enrollment data to the event receiver as the triggering logic would do.
- After triggering the event, you can assert that the event receiver executed the custom logic as expected. In this case, we are checking that the request was sent to the webhook with the correct data.

You can review this example to understand how you can test the event receiver and ensure that the custom logic is executed when the event is triggered in the openedx-events-2-zapier plugin.

This way you can ensure that the event receiver is working as expected and that the custom logic is executed when the event is triggered. If the event definition or payload changes in any way, you can catch the error in the test suite instead of in production.

.. _Tutor: https://docs.tutor.edly.io/
.. _Django Signals Documentation: https://docs.djangoproject.com/en/4.2/topics/signals/
.. _openedx-events-2-zapier: https://github.com/eduNEXT/openedx-events-2-zapier
.. _Open edX Django plugins: https://docs.openedx.org/en/latest/developers/concepts/platform_overview.html#new-plugin
.. _OEP-49: https://docs.openedx.org/projects/openedx-proposals/en/latest/best-practices/oep-0049-django-app-patterns.html#signals
