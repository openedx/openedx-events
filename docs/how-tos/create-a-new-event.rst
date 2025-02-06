Create a New Open edX Event with Long-Term Support
####################################################

Open edX Events are supported and maintained by the Open edX community. This mechanism is designed to be extensible and flexible, allowing developers to create new events that other services can consume. This guide describes how to create a new Open edX event with long-term support by following the practices outlined in the :doc:`../decisions/0016-event-design-practices` ADR.

Events designed with long support closely follow the practices described in the ADR to minimize breaking changes and maximize compatibility and support for future versions of Open edX.

.. note:: Before starting, ensure you have reviewed the documentation on :doc:`docs.openedx.org:developers/concepts/hooks_extension_framework`, this documentation helps you decide if creating a new event is necessary. You should also review the documentation on :doc:`../decisions/0016-event-design-practices` to understand the practices that should be followed when creating a new event.

Throughout this guide, we will use an example of creating a new event that will be triggered when a user enrolls in a course from the course about page to illustrate better the steps involved in creating a new event.

Key Outlines from Event Design Practices
******************************************

The :doc:`../decisions/0016-event-design-practices` outlines the following key practices to follow when creating a new event:

- Clearly describe what happened and why.
- Self-descriptive and self-contained as much as possible.
- Avoid runtime dependencies with other services.
- Avoid ambiguous data fields or fields with multiple meanings.
- Appropriate types and formats.
- Events should have a single responsibility.
- Avoid combining multiple events into one.
- Maintain the right granularity: not too fine-grained or too coarse.
- Ensure the triggering logic is consistent and narrow.
- Keep the event size small.
- Avoid flow control information or business logic in the event.
- Consider the consumers' needs when designing the event.
- Avoid breaking changes.

Assumptions
************

- You have a development environment set up using `Tutor`_.
- You have a basic understanding of Python and Django.
- You have a basic understanding of Django signals. If not, you can review the `Django Signals Documentation`_.
- You understand the concept of events or have reviewed the relevant :doc:`/concepts/index` docs.
- You are familiar with the terminology used in the project, such as the terms :term:`Event Type` or :term:`Event Payload`. If not, you can review the :doc:`../reference/glossary` docs.
- You have reviewed the :doc:`../decisions/0016-event-design-practices` ADR.
- You have identified that you need to create a new event and have a use case for the event.

Steps
*******

To create a new Open edX Event with long-term support, follow these steps:

Step 1: Propose the Use Case to the Community
=================================================

Before contributing to a new event, it is important to propose the event to the community to get feedback on the event's design and use case. For instance, you could create a post in the Open edX Discuss Forum or create a new issue in the repository's issue tracker describing your use case for the new event. Here are some examples of community members who have taken this step:

- `Add Extensibility Mechanism to IDV to Enable Integration of New IDV Vendor Persona`_
- `Add Program Certificate events`_

.. note:: If your use case is too specific to your organization, you can implement them in your own library and use them within your services by adopting an organization-scoped approach leveraging the Apache 2.0 license. However, if you think that your use case could be beneficial to the community, you should propose it to the community for feedback and collaboration.

In our example, our use case proposal could be:

   *I want to add an event that will be triggered when a user enrolls in a course from the course about page. This event will be useful for services that need to send the enrollment data to external services for further processing.*

If you are confident that the event benefits the community, you can proceed to the next steps and implement the event.

Step 2: Place Your Event In an Architecture Subdomain
=======================================================

To implement the new event in the library, you should understand the purpose of the event and where it fits in the Open edX main architecture subdomains. This will help you place the event in the right architecture subdomain and ensure that the event is consistent with the framework's definitions. For more details on the Open edX Architectural Subdomains, refer to the :doc:`../reference/architecture-subdomains`.

In our example, the event is related to the enrollment process, which is part of the ``learning`` subdomain. Therefore, the event should be placed in the ``/learning`` module in the library. The subdomain is also used as part of the :term:`event type <Event Type>`, which is used to identify the event. The event type should be unique and follow the naming convention for event types specified in the :doc:`../decisions/0002-events-naming-and-versioning` ADR.

For the enrollment event, the event type could be ``org.openedx.learning.course.enrollment.v1``, where ``learning`` is the subdomain.

.. note:: If you don't find a suitable subdomain for your event, you can propose a new subdomain to the community. However, new subdomains may require some discussion with the community. So, we encourage you to start the conversation as soon as possible through any communication channels available.

Step 3: Identify the Event Triggering Logic
=============================================

The triggering logic for the event should be identified to ensure that the event is triggered consistently in the right places. We should ensure that maximum coverage is achieved with minimal modifications when placing the event in the service we're modifying. The goal is to focus on core, critical areas where the logic we want to modify executes.

For this, choose a specific point in the service where the event should be triggered. This could be a method in a service, a view, or a model where the logic that you interested in is executed. The triggering logic should be consistent and narrow to ensure that the event is triggered only when the conditions are met. For instance, the triggering logic should be a place where all enrollment logic goes through, ensuring that the event is triggered consistently when a user enrolls in a course. This could be the ``enroll`` method in the enrollment model in the LMS, which is called when a user enrolls in a course in all cases.

.. note:: When designing an event, consider the support over time of the service and triggering logic. If the service is likely to change or be deprecated, consider the implications of implementing the event in that service.

.. note:: It is helpful to inspect the triggering logic to review the data that is available at the time the event is triggered. This will help you determine the content of the event and the data that should be included in the event payload.

Step 4: Determine the Content of the Event
=============================================

The event's content should comply with the practices outlined in the :doc:`../decisions/0016-event-design-practices`. The event should be self-descriptive and self-contained as much as possible. The event should contain all the necessary information for consumers to react to the event without having to make additional calls to other services when possible.

When determining the content of the event, consider the following:

- What happened and why?
- What data is needed to describe the event?
- What data is needed to react to the event?

In our specific example of the enrollment event, this could be:

- What happened: A user enrolled in a course.
- Why: The user enrolled in the course from the course about page.
- Data needed to describe the event: User information (who), course information (where), enrollment date, and mode (output details).
- Data needed to react to the event: User information, course information, enrollment Date, enrollment Mode. For instance, a notification could send a welcome email to the user.

As a rule of thumb, the event should contain the minimum amount of data required to describe the event and react to it. Try including data about each entity involved such that:

- Consumers can identify the entities involved in the event.
- Key data about the entities is included in the event.
- The outcome of the event is clear.

This will help ensure that the event is self-descriptive and self-contained as much as possible.

.. note:: There have been cases where events also carry other contextual data that is not directly related to the event but useful for consumers Although this is not recommended, if you need to include such data, ensure that the reasoning behind it is documented and does not introduce ambiguity.

.. note:: Also, consider how relevant the data is to where the event is triggered. Consider whether it could be removed or deprecated in the future so that the event remains consistent and maintainable over time.

Step 5: Implement the Event Definition and Payload
=====================================================

Implement the :term:`Event Definition` and :term:`Event Payload` for your event in the corresponding subdomain module. The event definition would be a signal that is triggered when the event takes place, and the event payload would be the data that is included in the event.

.. note:: Ideally, the data that is included in the event payload should be available at the time the event is triggered, and it should be directly related to the event that took place. So before defining the payload, inspect the triggering logic to review the data that is available at the time the event is triggered.

The event definition and payload must comply with the practices outlined in the :doc:`../decisions/0002-events-naming-and-versioning` and :doc:`../decisions/0003-events-payload` ADRs. Also, with the practices outlined in the :doc:`../decisions/0016-event-design-practices` ADR. Mainly:

- The event should be self-descriptive and self-contained as much as possible.
- The event should contain all the necessary information directly related to the event that took place.
- Maintain the right granularity: not too fine-grained or too coarse to ensure that the event is useful for consumers.

Event Payload
----------------

The event payload is a data `attrs`_ class that defines the data included in the event defined in the corresponding subdomain module in the ``data.py`` file. The payload should contain all the necessary information directly related to the event that took place to ensure that consumers can react to the event without introducing new dependencies to understand the event.

In our example, the event definition and payload for the enrollment event could be ``CourseEnrollmentData``. This class should contain all the necessary information about the enrollment event, such as user information, course information, enrollment mode, and other relevant data.

.. code-block:: python

    # Location openedx_events/learning/data.py
    @attr.s(frozen=True)
    class CourseEnrollmentData:
        """
        Attributes defined for Open edX Course Enrollment Object.

        Arguments:
            user (UserData): user associated with the Course Enrollment.
            course (CourseData): course where the user is enrolled in.
            mode (str): course mode associated with the course.
            is_active (bool): whether the enrollment is active.
            creation_date (datetime): creation date of the enrollment.
            created_by (UserData): if available, who created the enrollment.
        """

        user = attr.ib(type=UserData)
        course = attr.ib(type=CourseData)
        mode = attr.ib(type=str)
        is_active = attr.ib(type=bool)
        creation_date = attr.ib(type=datetime)
        created_by = attr.ib(type=UserData, default=None)

- The payload should be an `attrs`_ class to ensure that the data is immutable by using the ``frozen=True`` argument and to ensure that the data is self-descriptive.
- Use the ``attr.ib`` decorator to define the fields in the payload with the data type that the field should contain. Try to use the appropriate data type for each field to ensure that the data is consistent and maintainable, you can inspect the triggering logic to review the data that is available at the time the event is triggered.
- Try using nested data classes to group related data together. This will help maintain consistency and make the event more readable. For instance, in the above example, we have grouped the data into User, Course, and Enrollment data.
- Try reusing existing data classes if possible to avoid duplicating data classes. This will help maintain consistency and reduce the chances of introducing errors. You can review the existing data classes in :doc:`../reference/events-data` to see if there is a data class that fits your use case.
- Each field in the payload should be documented with a description of what the field represents and the data type it should contain. This will help consumers understand the payload and react to the event. You should be able to justify why each field is included in the payload and how it relates to the event.
- Use defaults for optional fields in the payload to ensure its consistency in all cases.

.. note:: When defining the payload, enforce :doc:`../concepts/event-bus` compatibility by ensuring that the data types used in the payload align with the event bus schema format. This will help ensure that the event can be sent by the producer and then be re-emitted by the same instance of `OpenEdxPublicSignal`_ on the consumer side, guaranteeing that the data sent and received is identical. For more information about adding event bus support to an event, refer to :doc:`../how-tos/add-event-bus-support-to-an-event`.

Event Definition
------------------

The :term:`Event Definition` should be implemented in the corresponding subdomain module in the ``signals.py`` file. In our example, the event definition for the enrollment event could be:

.. code-block:: python

    # Location openedx_events/learning/signals.py
    # .. event_type: org.openedx.learning.course.enrollment.created.v1
    # .. event_name: COURSE_ENROLLMENT_CREATED
    # .. event_description: emitted when the user's enrollment process is completed.
    # .. event_data: CourseEnrollmentData
    COURSE_ENROLLMENT_CREATED = OpenEdxPublicSignal(
        event_type="org.openedx.learning.course.enrollment.created.v1",
        data={
            "enrollment": CourseEnrollmentData,
        }
    )

- The event definition should be documented using in-line documentation with at least ``event_type``, ``event_name``, ``event_description``, and ``event_data``. This will help consumers understand the event and react to it. See :doc:`../reference/in-line-code-annotations-for-an-event` for more information.
- The :term:`Event Type` should be unique and follow the naming convention for event types specified in the :doc:`../decisions/0002-events-naming-and-versioning` ADR. This is used by consumers to identify the event.
- The ``event_name`` should be a constant that is used to identify the event in the code.
- The ``event_description`` should describe what the event is about and why it is triggered.
- The ``event_data`` should be the payload class that is used to define the data that is included in the event.
- The ``data`` dictionary should contain the payload class that is used to define the data that is included in the event. This will help consumers understand the event and react to it. Try using a descriptive name for the data field, but keep consistency with the payload class name. Avoid using suffixes like ``_data`` or ``_payload`` in the data field name.
- The event should be an instance of the ``OpenEdxPublicSignal`` class to ensure that the event is consistent with the Open edX event framework.
- Receivers should be able to access the event payload in their receivers to react to the event.

Step 6: Send the Event
=========================

After defining the event, you should trigger the event in the places we identified in the triggering logic. In our example, we identified that the event should be triggered when a user enrolls in a course, so it should be triggered when the enrollment process completes, successfully independent of the method of enrollment used. Therefore, we should trigger the event in the ``enroll`` method in the enrollment model in the LMS service when the enrollment process is complete successfully, i.e., at the end of the method.

Here is how the integration could look like:

.. code-block:: python

    # Location common/djangoapps/student/models.py
    from openedx_events.learning.signals import COURSE_ENROLLMENT_CREATED

    def enroll(cls, user, course_key, mode=None, **kwargs):
        """
        Enroll a user in this course.
        """
        # Enrollment logic here
        ...
        # .. event_implemented_name: COURSE_ENROLLMENT_CREATED
        COURSE_ENROLLMENT_CREATED.send_event(
            enrollment=CourseEnrollmentData(
                user=UserData(
                    pii=UserPersonalData(
                        username=user.username,
                        email=user.email,
                        name=user.profile.name,
                    ),
                    id=user.id,
                    is_active=user.is_active,
                ),
                course=course_data,
                mode=enrollment.mode,
                is_active=enrollment.is_active,
                creation_date=enrollment.created,
            )
        )

- Ensure that the event is triggered consistently and only when the event should be triggered. Avoid triggering the event multiple times for the same event unless necessary, e.g., when there is no other way to ensure that the event is triggered consistently.
- Try placing the event after the triggering logic completes successfully to ensure that it is triggered only when needed.  This will help ensure that the event is triggered only for factual events. If the triggering logic fails, the event should not be triggered.

Step 7: Test the Event
========================

You should test the event to ensure it triggers consistently and that its payload contains the necessary information. Add unit tests to the service that trigger the event. The main goal is to verify that the event triggers as needed, that consumers can react to it, and it carries the expected information.

To ensure that our example is tested thoroughly, we should:

- Add unit tests to the ``enroll`` method to ensure that the event is triggered when a user enrolls in a course. This means testing the event is triggered when the enrollment process is completed successfully.
- Add checks to ensure that the event is triggered consistently and only when the event should be triggered.
- Verify that the payload contains the necessary information for consumers to react to the event, such as user information, course information, enrollment mode, and other relevant data.

There is no need to test the event definition since the tooling already tests the definitions for you. Still, you should test the event triggering logic to ensure that the event complies with the expected behavior.

In our example, we could write a test that enrolls a user in a course and verifies that the event is triggered with the correct payload. Here is an example of how the test could look like:

.. code-block:: python

    # Location common/djangoapps/student/tests/test_events.py
    from openedx_events.learning.signals import COURSE_ENROLLMENT_CREATED

    def _event_receiver_side_effect(self, **kwargs):
        """
        Used show that the Open edX Event was called by the Django signal handler.
        """
        self.receiver_called = True

    def test_enrollment_created_event_emitted(self):
        """
        Test whether the student enrollment event is sent after the user's enrollment process.

        Expected result:
            - COURSE_ENROLLMENT_CREATED is sent and received by the mocked receiver.
            - The arguments that the receiver gets are the arguments sent by the event
            except the metadata generated on the fly.
        """
        event_receiver = mock.Mock(side_effect=self._event_receiver_side_effect)
        COURSE_ENROLLMENT_CREATED.connect(event_receiver)

        enrollment = CourseEnrollment.enroll(self.user, self.course.id)

        self.assertTrue(self.receiver_called)
        self.assertDictContainsSubset(
            {
                "signal": COURSE_ENROLLMENT_CREATED,
                "sender": None,
                "enrollment": CourseEnrollmentData(
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
                    mode=enrollment.mode,
                    is_active=enrollment.is_active,
                    creation_date=enrollment.created,
                ),
            },
            event_receiver.call_args.kwargs
        )

- Ensure that the test verifies that the event is triggered when the enrollment process completes successfully and that the payload contains the necessary information.
- Connect a dummy event receiver to the event to verify that the event is triggered.
- Verify that the event receiver is called with the correct payload when the event is triggered.

Step 8: Consume the Event
===========================

Since the event is now implemented, you should consume it to verify that it is triggered and that the payload contains the necessary information. You can consume the event in a test environment using a Django Signal Receiver. This will help you verify that the event is triggered and that the payload contains the necessary information. You can follow the steps in :doc:`../how-tos/consume-an-event` to consume the event in a test environment with a Django Signal Receiver. You could also use the Open edX Event Bus to consume the event in a test environment. For more information on how to use the Open edX Event Bus, refer to the :doc:`../how-tos/use-the-event-bus-to-broadcast-and-consume-events`.

Step 9: Continue the Contribution Process
============================================

After implementing the event, you should continue the contribution process by creating a pull request in the repository. The pull requests should contain the changes you made to implement the event, including the event definition, payload, and the places where the event is triggered.

For more details on how the contribution flow works, refer to the :doc:`docs.openedx.org:developers/concepts/hooks_extension_framework` documentation.

.. _Add Extensibility Mechanism to IDV to Enable Integration of New IDV Vendor Persona: https://openedx.atlassian.net/wiki/spaces/OEPM/pages/4307386369/Proposal+Add+Extensibility+Mechanisms+to+IDV+to+Enable+Integration+of+New+IDV+Vendor+Persona
.. _Add Program Certificate events: https://github.com/openedx/openedx-events/issues/250
.. _attrs: https://www.attrs.org/en/stable/
.. _Tutor: https://docs.tutor.edly.io/
.. _Django Signals Documentation: https://docs.djangoproject.com/en/4.2/topics/signals/
.. _OpenEdxPublicSignal: https://github.com/openedx/openedx-events/blob/main/openedx_events/tooling.py#L37

**Maintenance chart**

+--------------+-------------------------------+----------------+--------------------------------+
| Review Date  | Working Group Reviewer        |   Release      |Test situation                  |
+--------------+-------------------------------+----------------+--------------------------------+
|2025-02-05    | BTR WG - Maria Grimaldi       |Redwood         |Pass.                           |
+--------------+-------------------------------+----------------+--------------------------------+