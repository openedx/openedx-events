How to add an Open edX Event to a service
=========================================

5. Integrate into service
-------------------------

After or during the events definition implementation, you now must trigger the event in the service you intentioned. Meaning:

- Add the openedx-events library to the service project.
- Import the events' data and definition into the place where will be triggered. Remember the Open edX Events purpose when
  choosing a place to send the new event.
- Add inline documentation with the event implemented name.

Before opening a PR in the service project, refer to its contribution guidelines.

Consider the integration of the event ``STUDENT_REGISTRATION_COMPLETED`` as an example:

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
