Create a New Open edX Event with Long-Term Support
==================================================

Open edX Events are supported and maintained by the Open edX community. This mechanism is designed to be extensible and flexible to allow developers to create new events that can be consumed by other services. This guide describes how to create a new Open edX event with long-term support by following the practices outlined in the :doc:`../decisions/0016-event-design-practices` ADR.

Events design with long-support follow closely the practices described in the ADR to minimize breaking changes, maximize compatibility and support for future versions of Open edX.

.. note:: Before starting, ensure you've reviewed the documentation on :doc:`docs.openedx.org:developers/concepts/hooks_extension_framework`, this documentation helps you decide if creating a new event is necessary. You should also review the documentation on :doc:`../decisions/0016-event-design-practices` to understand the practices that should be followed when creating a new event.

Throughout this guide, we will use an example of creating a new event that will be triggered when a user enrolls in a course from the course about page to better illustrate the steps involved in creating a new event.

Key Outlines from Event Design Practices
----------------------------------------

The :doc:`../decisions/0016-event-design-practices` outlines the following key practices to follow when creating a new event:

- Clearly describe what happened and why.
- Self-descriptive and self-contained as much as possible.
- Avoid runtime dependencies with other services.
- Avoid ambiguous data fields or fields with multiple meaning.
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
-----------

- You have a development environment set up using `Tutor`_.
- You have a basic understanding of Python and Django.
- You have a basic understanding of Django signals. If not, you can review the `Django Signals Documentation`_.
- You understand the concept of events or have reviewed the relevant :doc:`/concepts/index` docs.
- You are familiar with the terminology used in the project, such as the terms :term:`Event Type` or :term:`Event Payload`. If not, you can review the :doc:`../reference/glossary` docs.
- You have reviewed the :doc:`../decisions/0016-event-design-practices` ADR.
- You have identified that you need to create a new event and have a use case for the event.

Steps
-----

To create a new Open edX Event with long-term support, follow these steps:

Step 1: Propose the Use Case to the Community
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before contributing a new event, it is important to propose the event to the community to get feedback on the event's design and use case. For instance, you could create a post in Open edX Discuss Forum or create a new issue in the repository's issue tracker describing your use case for the new event. Here are some examples of community members that have taken this step:

- `Add Extensibility Mechanism to IDV to Enable Integration of New IDV Vendor Persona`_
- `Add Program Certificate events`_

.. note:: If your use case is too specific to your organization, you can implement them in your own library and use it within your services by adopting an organization-scoped approach leveraging the Apache 2.0 license. However, if you think that your use case could be beneficial to the community, you should propose it to the community for feedback and collaboration.

In our example our use case proposal could be:

   I want to add an event that will be triggered when a user enrolls in a course from the course about page. This event will be useful for services that need to send notifications to the user when they enroll in a course.

If you are confident that the event is beneficial to the community, you can proceed to the next steps and implement the event.

Step 2: Place Your Event In an Architecture Subdomain
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To implement the new event in the library, you should understand the purpose of the event and where it fits in the Open edX main architecture subdomains. This will help you place the event in the right architecture subdomain and ensure that the event is consistent with the framework's definitions. Fore more details on the Open edX Architectural Subdomains, refer to the :doc:`../reference/architecture-subdomains`.

In our example, the event is related to the enrollment process, which is part of the ``learning`` subdomain. Therefore, the event should be placed in the ``/learning`` module in the library. The subdomain is also used as part of the :term:`event type <Event Type>`, which is used to identify the event. The event type should be unique and follow the naming convention for event types specified in the :doc:`../decisions/0002-events-naming-and-versioning` ADR.

For the enrollment event, the event type could be ``org.openedx.learning.course.enrollment.v1``, where ``learning`` is the subdomain.

.. note:: If you don't find a suitable subdomain for your event, you can propose a new subdomain to the community. However, new subdomains may require some discussion with the community. So we encourage you to start the conversation as soon as possible through any of the communication channels available.

Step 3: Identify the Event Triggering Logic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The triggering logic for the event should be identified to ensure that the event is triggered in the right places and that the event is triggered consistently. We should identify the triggering logic to ensure that maximum coverage is achieved with minimal modifications. The goal is to focus on core, critical areas where the logic we want to modify executes, ensuring the event is triggered consistently.

In our example, the triggering logic could be a place where all enrollment logic goes through. This could be the ``enroll`` method in the enrollment model in the LMS, which is called when a user enrolls in a course in all cases.

.. note:: When designing an event take into account the support over time of the service and triggering logic. If the service is likely to change or be deprecated, consider the implications of implementing the event in that service.

.. note:: It is helpful to inspect the triggering logic to review the data that is available at the time the event is triggered. This will help you determine the content of the event and the data that should be included in the event payload.

Step 4: Determine the Content of the Event
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The content of the event should comply with the practices outlined in the :doc:`../decisions/0016-event-design-practices`. The event should be self-descriptive and self-contained as much as possible. The event should contain all the necessary information for consumers to react to the event without having to make additional calls to other services when possible.

When determining the content of the event, consider the following:

- What happened and why?
- What data is needed to describe the event?
- What data is needed to react to the event?

In our specific example of the enrollment event this could be:

- What happened: A user enrolled in a course.
- Why: The user enrolled in the course from the course about page.
- Data needed to describe the event: User information (who), course information (where), enrollment date and mode (output details).
- Data needed to react to the event: User information, course information, enrollment Date, enrollment Mode. For instance, a notification could send a welcome email to the user.

As a rule of thumb, the event should contain the minimum amount of data required to describe the event and react to it. Try including data about each entity involved such that:

- Consumers can identify the entities involved in the event.
- Key data about the entities is included in the event.
- The outcome of the event is clear.

This will help ensure that the event is self-descriptive and self-contained as much as possible.

.. note:: There has been cases where events also carry other contextual data not directly related to the event but useful for consumers. Although this is not recommended, if you need to include such data, ensure that the reasoning behind it is documented and does not introduce ambiguity.

.. note:: Also consider how relevant is the data to where the event is triggered. Consider whether it could be removed or deprecated in the future so that the event remains consistent and maintainable over time.

Step 5: Implement the Event Definition and Payload
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implement the :term:`Event Definition` and :term:`Event Payload` for your event in the corresponding subdomain module. The event definition would be a signal that is triggered when the event takes place, and the event payload would be the data that is included in the event.

.. note:: Ideally, the data that is included in the event payload should be available at the time the event is triggered, and it should be directly related to the event that took place. So before defining the payload, inspect the triggering logic to review the data that is available at the time the event is triggered.

The event definition and payload must comply with the practices outlined in the :doc:`../decisions/0002-events-naming-and-versioning` and :doc:`../decisions/0003-events-payload` ADRs. Also, with the practices outlined in the :doc:`../decisions/0016-event-design-practices` ADR. Mainly:

- The event should be self-descriptive and self-contained as much as possible.
- The event should contain all the necessary information directly related to the event that took place.
- Maintain the right granularity: not too fine-grained or too coarse to ensure that the event is useful for consumers.

Event Payload
*************

The event payload is a data `attrs`_ class which defines the data that is included in the event that is defined in the corresponding subdomain module in the ``data.py`` file. The payload should contain all the necessary information directly related to the event that took place to ensure that consumers can react to the event without introducing new dependencies to understand the event.

In our example, the event definition and payload for the enrollment event could be ``CourseEnrollmentData``. This class should contain all the necessary information about the enrollment event, such as user information, course information, enrollment mode, and other relevant data.

.. code-block:: python

    # Location openedx_events/learning/data.py
    @attr.s(frozen=True)
    class CourseEnrollmentData:
        """
        Attributes defined for Open edX Course Enrollment object.

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

.. note:: Try grouping the data into logical groups to make the event more readable and maintainable. For instance, in the above example, we have grouped the data into User, Course, and Enrollment data.

Each field in the payload should be documented with a description of what the field represents and the data type it should contain. This will help consumers understand the payload and react to the event. You should be able to justify why each field is included in the payload and how it relates to the event.

.. note:: Try reusing existing data classes if possible to avoid duplicating data classes. This will help maintain consistency and reduce the chances of introducing errors.

Event Definition
****************

The event definition should be defined in the corresponding subdomain module in the ``signals.py`` file. The :term:`Event Definition` should comply with:

- It must be documented using in-line documentation with at least: ``event_type``, ``event_name``, ``event_description`` and ``event_data``. See :doc:`../reference/in-line-code-annotations-for-an-event` for more information.

In our example, the event definition for the enrollment event could be:

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

Consumers will be able to access the event payload in their receivers to react to the event. The ``event_type`` is mainly used to identify the event.

.. TODO: add reference to how to add event bus support to the event's payload

Step 6: Send the Event
~~~~~~~~~~~~~~~~~~~~~~~

After defining the event, you should trigger the event in the places we identified in the triggering logic. In our example, we identified that the event should be triggered when a user enrolls in a course so it should be triggered when the enrollment process completes successfully independent of the method of enrollment used. Therefore, we should trigger the event in the ``enroll`` method in the enrollment model in the LMS services.

Here is how the integration could look like:

.. code-block:: python

    # Location openedx/core/djangoapps/enrollments/models.py
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

.. note:: Ensure that the event is triggered consistently and only when the event should be triggered. Avoid triggering the event multiple times for the same event unless necessary, e.g., when there is no other way to ensure that the event is triggered consistently.

.. note:: Try placing the event after the triggering logic to ensure that the event is triggered only when the triggering logic completes successfully. This will help ensure that the event is triggered only for factual events if the triggering logic fails, the event should not be triggered.

Step 7: Test the Event
~~~~~~~~~~~~~~~~~~~~~~~

You should test the event to ensure it triggers consistently and that its payload contains the necessary information. Add unit tests in the service that triggers the event. The main goal is to verify that the event triggers as needed, consumers can react to it, and it carries the expected information.

To ensure that our example is tested thoroughly, we should:

- Add unit tests to the ``enroll`` method to ensure that the event is triggered when a user enrolls in a course. This means testing the event is triggered when the enrollment process completes successfully.
- Add checks to ensure that the event is triggered consistently and only when the event should be triggered.
- Verify that the payload contains the necessary information for consumers to react to the event like user information, course information, enrollment mode, and other relevant data.

Step 8: Consume the Event
~~~~~~~~~~~~~~~~~~~~~~~~~

Since the event is now implemented, you should consume the event to verify that it is triggered and that the payload contains the necessary information. You can consume the event in a test environment using a Django Signal Receiver. This will help you verify that the event is triggered and that the payload contains the necessary information. You can use follow the steps in :doc:`../how-tos/consume-an-event` to consume the event in a test environment with a Django Signal Receiver. Or you could also use the Open edX Event Bus to consume the event in a test environment. For more information on how to use the Open edX Event Bus, refer to the :doc:`../how-tos/use-the-event-bus-to-broadcast-and-consume-events`.

Step 9: Continue the Contribution Process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After implementing the event, you should continue the contribution process by creating a pull request in the repository. The pull request should contain the changes you made to implement the event, including the event definition, payload, and the places where the event is triggered.

For more details on how the contribution flow works, refer to the :doc:`docs.openedx.org:developers/concepts/hooks_extension_framework` documentation.

.. _Add Extensibility Mechanism to IDV to Enable Integration of New IDV Vendor Persona: https://openedx.atlassian.net/wiki/spaces/OEPM/pages/4307386369/Proposal+Add+Extensibility+Mechanisms+to+IDV+to+Enable+Integration+of+New+IDV+Vendor+Persona
.. _Add Program Certificate events: https://github.com/openedx/openedx-events/issues/250
.. _attrs: https://www.attrs.org/en/stable/
.. _Tutor: https://docs.tutor.edly.io/
.. _Django Signals Documentation: https://docs.djangoproject.com/en/4.2/topics/signals/
