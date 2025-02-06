In-line Code Annotations for an Open edX Event
################################################

When creating a new Open edX Event, you must document the event definition using in-line code annotations. These annotations provide a structured way to document the event's metadata, making it easier for developers to understand the event's purpose and how it should be used.

+----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| Annotation                       | Description                                                                                                                      |
+==================================+==================================================================================================================================+
| event_type (Required)            | Identifier across services of the event. Should follow the :doc:`../decisions/0002-events-naming-and-versioning` standard.       |
+----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| event_name (Required)            | Name of the variable storing the event instance.                                                                                 |
+----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| event_description (Required)     | General description which includes when the event should be emitted.                                                             |
+----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| event_data (Required)            | What type of class attribute the event sends.                                                                                    |
+----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| event_warnings (Optional)        | Any warnings or considerations that should be taken into account when using the event.                                           |
+----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+

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

**Maintenance chart**

+--------------+-------------------------------+----------------+--------------------------------+
| Review Date  | Working Group Reviewer        |   Release      |Test situation                  |
+--------------+-------------------------------+----------------+--------------------------------+
|2025-02-05    | BTR WG - Maria Grimaldi       |Redwood         |Pass.                           |
+--------------+-------------------------------+----------------+--------------------------------+