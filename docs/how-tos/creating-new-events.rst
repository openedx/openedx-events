How to create a new Open edX Event
==================================

The mechanisms implemented by the Open edX Events library are supported and maintained by the Open edX community.
Therefore, we've put together a guide on how to add a new event the library so future contributions are effective.


1. Propose the new event to the community
-----------------------------------------

When creating a new event, you must justify its implementation. For example, you could create a post in Discuss,
send a message through slack or open a new issue in the library repository listing your use cases for it. Or even,
if you have time, you could accompany your proposal with the implementation of the event to illustrate its behavior.

2. Place your event in an architecture subdomain
-------------------------------------------------

As specified in the Architectural Decisions Record (ADR) events naming and versioning, the event definition needs an Open edX Architecture
Subdomain for:

- The name of the event: ``{Reverse DNS}.{Architecture Subdomain}.{Subject}.{Action}.{Major Version}``
- The package name where the definition will live, eg. ``learning/`` or ``content_authoring/``.

For those reasons, after studying your new event purpose, you must place it in one of the subdomains already in use, or introduce a new subdomain:

+------------------+----------------------------------------------------------------------------------------------------+
| Subdomain name   | Description                                                                                        |
+==================+====================================================================================================+
| Course Authoring | Allows educators to create, modify, package, annotate (tag), and share learning content.           |
+----------------- +----------------------------------------------------------------------------------------------------+
| Learning         | Allows learners to consume content and perform actions in a learning activity on the platform.     |
+------------------+----------------------------------------------------------------------------------------------------+

New subdomains may require some discussion, because there does not yet exist and agreed upon set on subdomains. So we encourage you to start the conversation
as soon as possible through any of the communication channels available.

Refer to `edX DDD Bounded Contexts <https://openedx.atlassian.net/l/cp/vf8XjRiX>`_ confluence page for more documentation on domain-driven design in the Open edX project.

3. Create the data attributes for the event (OEP-49)
----------------------------------------------------

Events send `data attributes <https://open-edx-proposals.readthedocs.io/en/latest/architectural-decisions/oep-0049-django-app-patterns.html#data-py>`_ when triggered. Therefore, when designing your new event definition you must
decide if an existent data class works for your use case or you must create a new one. If the answer is the latter, then try to answer:

- Which attributes of the object are the most relevant?
- Which type are they?
- Is any of them optional/required?

And with that information, create the new class justifying each decision. The class created in this step must comply
with:

- It should be created in the `data.py` file, as described in the OEP-49, in the corresponding architectural subdomain. Refer to Naming Conventions ADR for more
  on events subdomains.
- It should follow the naming conventions used across the other events definitions.

Consider the user data representation as an example:

.. code-block:: python

    @attr.s(frozen=True)
    class CourseData:
        """
        Attributes defined for Open edX Course Overview object.

        Arguments:
            course_key (str): identifier of the Course object.
            display_name (str): display name associated with the course.
            start (datetime): start date for the course.
            end (datetime): end date for the course.
        """

        course_key = attr.ib(type=CourseKey)
        display_name = attr.ib(type=str, factory=str)
        start = attr.ib(type=datetime, default=None)
        end = attr.ib(type=datetime, default=None)


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

4. Create the event definition
------------------------------

Open edX Events are instances of the class OpenEdxPublicSignal, this instance represents the event definition that
specifies:

- The event type which should follow the conventions in the Naming Conventions ADR.
- The events' payload, here you must use the class you decided on before.

The definition created in this step must comply with:

- It should be created in the `signals.py` file in the corresponding subdomain. Refer to Naming Conventions ADR for more
  on events subdomains.
- It should follow the naming conventions specified in Naming Conventions ADR.
- It must be documented using in-line documentation with at least: `event_type`, `event_name`, `event_description` and
  `event_data`:

+-------------------+----------------------------------------------------------------------------------------------------+
| Annotation        | Description                                                                                        |
+===================+====================================================================================================+
| event_type        | Allows educators to create, modify, discover, package, annotate (tag), and share learning content. |
+-------------------+----------------------------------------------------------------------------------------------------+
| event_name        | Allows learners to consume content and perform actions in a learning activity on the platform.     |
+-------------------+----------------------------------------------------------------------------------------------------+
| event_description | Allows learners to find the right content at the right time to help achieve their learning goals.  |
+-------------------+----------------------------------------------------------------------------------------------------+
| event_data        | Allows educators and learners to manage and engage in bundled packages (programs) of learning.     |
+-------------------+----------------------------------------------------------------------------------------------------+

Consider the following example:

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
