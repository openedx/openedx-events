In-line Code Annotations for an Open edX Event
################################################

When creating a new Open edX Event, you must document the event definition using in-line code annotations. These annotations provide a structured way to document the event's metadata, making it easier for developers to understand the event's purpose and how it should be used.

+-------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| Annotation                          | Description                                                                                                                |
+=====================================+============================================================================================================================+
| event_type (Required)               | Identifier across services of the event. Should follow the :doc:`../decisions/0002-events-naming-and-versioning` standard. |
+-------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| event_name (Required)               | Name of the variable storing the event instance.                                                                           |
+-------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| event_key_field (Optional)          | The field in the event data that uniquely identifies the event.                                                            |
+-------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| event_description (Required)        | General description which includes when the event should be emitted.                                                       |
+-------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| event_data (Required)               | What type of class attribute the event sends.                                                                              |
+-------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| event_trigger_repository (Required) | The repository that triggers the event. This is useful to find the source of the event.                                    |
+-------------------------------------+----------------------------------------------------------------------------------------------------------------------------+
| event_warnings (Optional)           | Any warnings or considerations that should be taken into account when using the event.                                     |
+-------------------------------------+----------------------------------------------------------------------------------------------------------------------------+

Consider the following example:

.. code-block:: python

    # .. event_type: org.openedx.learning.course.enrollment.created.v1
    # .. event_name: COURSE_ENROLLMENT_CREATED
    # .. event_key_field: enrollment.course.course_key
    # .. event_description: Emitted when the user enrolls in a course.
    # .. event_data: CourseEnrollmentData
    # .. event_trigger_repository: openedx/edx-platform
    COURSE_ENROLLMENT_CREATED = OpenEdxPublicSignal(
        event_type="org.openedx.learning.course.enrollment.created.v1",
        data={
            "enrollment": CourseEnrollmentData,
        }
    )

In-line code annotations are also used when integrating the event into the service.

+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Annotation                        | Description                                                                                                                                                |
+===================================+============================================================================================================================================================+
| event_implemented_name (Required) | Variable name storing the event instance used to trigger the event. The name of the variable usually matches the ``{Subject}_{Action}`` of the event type. |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------+

Consider the following example:

.. code-block:: python

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

Developers can refer to the in-line code annotations to understand the event's purpose and how it should be used. This makes it easier to work with the event and ensures that it is used correctly across services.

**Maintenance chart**

+--------------+-------------------------------+----------------+--------------------------------+
| Review Date  | Reviewer                      |   Release      |Test situation                  |
+--------------+-------------------------------+----------------+--------------------------------+
|2025-02-05    | Maria Grimaldi                |  Sumac         |Pass.                           |
+--------------+-------------------------------+----------------+--------------------------------+
