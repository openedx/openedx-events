2. Open edX events naming
=========================

Status
------

Draft

Context
-------

Besides a suitable location, event-type hooks need a form of
identification when adding them to the Open edX platform. By doing this,
recognizing which event to use, or debugging errors will be easier.

This ADR has the purpose of defining the rules to be followed when
naming an Open edX Event.

Decisions
---------

The following decisions were made after receiving feedback from the Open edX
community on this repository and on other platforms such as discuss.

1. The name will be a ``string`` that follows the `type format`_ defined in
the `OEP-41`_ with a minor change:

``{Reverse DNS}.{Architecture Subdomain}.{Subject}.{Action}``

Examples:

* org.openedx.learning.course.enrollment.created
* org.openedx.learning.student.registration.completed
* org.openedx.learning.session.login.completed

As can be seen, ``{Major Version}`` was removed from the name, meaning,
events won't be versioned. Instead, the data sent by them will be:

.. code-block:: python

  providing_args={
            "user_data": UserData,
            "registration_data": RegistrationData,
            "registration_data_v2": RegistrationDataV2,
        }

2. The name will be sent as metadata for the events to
help with debugging, logging, or any other process related to events.

For example:

.. code-block:: python

  # Event definition
  STUDENT_REGISTRATION_COMPLETED = OpenEdxPublicSignal(
      event_type="org.openedx.learning.student.registration.completed",
      providing_args={
          "user_data": UserData,
          "registration_data": RegistrationData,
          ...
      }
  )

3. The definition of the signal does not have a one-to-one mapping to the name
proposed here. The definition will be done in such a way that it's the most
usable and accessible for the developer.

.. _type format: https://open-edx-proposals.readthedocs.io/en/latest/oep-0041-arch-async-server-event-messaging.html#id5
.. _OEP-41: https://open-edx-proposals.readthedocs.io/en/latest/oep-0041-arch-async-server-event-messaging.html#specification

Consequences
------------

* All events must follow the same format for their associated name.
