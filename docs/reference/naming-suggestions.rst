Naming Suggestions for Open edX Events
########################################

When naming a new event and contributing it back to this repository, consider the following suggestions:

- Use a name that is descriptive to the event's purpose. For example, the event associated with a user's enrollment in a course is named ``COURSE_ENROLLMENT_CREATED``, which clearly indicates the event's purpose.
- Use a name that is unique within the framework.
- Match the name to the ``event_type`` identifier. For example, the ``COURSE_ENROLLMENT_CREATED`` event has an ``event_type`` of ``org.openedx.learning.course.enrollment.created.v1``. You can use the ``event_type`` as a reference when naming the event. See :ref:`ADR-2` for more information on naming and versioning events.
- Avoid using ``event`` in the name. It is implied that the variable is an event, so there is no need to include it in the name.
- Try reviewing the :ref:`existing events <Existing Events>` in the repository to ensure that the name you choose is unique and follows the naming conventions.
