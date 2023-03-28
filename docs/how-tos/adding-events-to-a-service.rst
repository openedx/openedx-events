How to add an Open edX Event to a service
=========================================

The next step after creating your first event in the Open edX Events library, it's to trigger the event in the service
you implemented it for. Here is a checklist of what we've done so far when including a new event to a service:

- Add the openedx-events library to the service project.
- Import the events' data and definition into the place where the event be triggered. Remember the event's purpose when
  choosing a place to send the new event.
- Add inline documentation with the ``event_implemented_name``. This matches the ``event_name`` in line documentation from the library.
- Refer to the service project's contribution guidelines and follow the instructions. Then, open a new pull request!

Consider the addition of the event ``STUDENT_REGISTRATION_COMPLETED`` to edx-platform as an example:

.. code-block:: python

    # Location openedx/core/djangoapps/user_authn/views/register.py
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

If you want to know more about how the integration of the first events' batch went, check out the `PR 28266`_.

.. _PR 28266: https://github.com/openedx/edx-platform/pull/28266
