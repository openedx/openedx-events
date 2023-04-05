Using Open edX Events
=====================

How to use
----------

Using openedx-events in your code is very straight forward. We can consider the
two possible cases, sending or receiving an event.

Receiving events
^^^^^^^^^^^^^^^^

This is one of the most common use cases for plugins. The Open edX platform will send
an event and you want to react to it in your plugin.

For this you need to:

1. Include openedx-events in your dependencies.
2. Connect your receiver functions to the signals being sent.

Connecting signals can be done using regular django syntax:

.. code-block:: python

    from openedx_events.learning.signals import STUDENT_REGISTRATION_COMPLETED

    @receiver(STUDENT_REGISTRATION_COMPLETED)
    def your_receiver_function(**kwargs):
        # your implementation here


Or at the apps.py

.. code-block:: python

    {
        "signals_config": {
            "lms.djangoapp": {
                "relative_path": "your_module_name",
                "receivers": [
                    {
                        "receiver_func_name": "your_receiver_function",
                        "signal_path": "openedx_events.learning.signals.STUDENT_REGISTRATION_COMPLETED",
                    },
                ],
            }
        }
    }


In case you are listening to an event in an Open edX platform repo, you can directly
use the django syntax since the apps.py method will not be available without the
plugin system.

.. warning::
    For non-trivial work, we encourage using asynchronous tasks in your receiver functions in order
    to avoid affecting the performance of the service.

Sending events
^^^^^^^^^^^^^^

Sending events requires you to import both the event definition as well as the
attr data classes that encapsulate the event data.

.. code-block:: python

    from openedx_events.learning.data import UserData, UserPersonalData
    from openedx_events.learning.signals import STUDENT_REGISTRATION_COMPLETED

    STUDENT_REGISTRATION_COMPLETED.send_event(
        user=UserData(
            pii=UserPersonalData(
                username=user.username,
                email=user.email,
                name=user.profile.name,
            ),
            id=user.id,
            is_active=user.is_active,
        ),
    )

You can do this both from the Open edX platform code as well as from an openedx
plugin.

Testing events
^^^^^^^^^^^^^^

Testing your code in CI, specially for plugins is now possible without having to
import the complete Open edX platform as a dependency.

To test your functions you need to include the openedx-events library in your
testing dependencies and make the signal connection in your test case.

.. code-block:: python

    from openedx_events.learning.signals import STUDENT_REGISTRATION_COMPLETED

    def test_your_receiver(self):
        STUDENT_REGISTRATION_COMPLETED.connect(your_function)
        STUDENT_REGISTRATION_COMPLETED.send_event(
            user=UserData(
                pii=UserPersonalData(
                    username='test_username',
                    email='test_email@example.com',
                    name='test_name',
                ),
                id=1,
                is_active=True,
            ),
        )

        # run your assertions

Changes in the openedx-events library that are not compatible with your code
should break this kind of test in CI and let you know you need to upgrade your
code.
