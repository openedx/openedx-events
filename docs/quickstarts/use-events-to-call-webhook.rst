Using Open edX Events in the LMS service
========================================

Live example
------------

For a complete and detailed example you can see the `openedx-events-2-zapier`_
plugin. This is a fully functional plugin that connects to
``STUDENT_REGISTRATION_COMPLETED`` and ``COURSE_ENROLLMENT_CREATED`` and sends
the relevant information to zapier.com using a webhook.

Let's see it working!

Setup your environment
----------------------

This tutorial assumes you're using `Tutor`_ > 13.x and its default services are
already provisioned.

Installation
------------

For this tutorial to work, you'll need a openedx image with the following package
installed:

- `openedx-events-2-zapier`_

You can use your preferred method for installing new packages in Tutor.

Configuration
-------------

The package we just installed is a `Django plugin`_, which adds additional
configurations to our working environment thanks to the extension mechanisms put in place. Now,
signal receivers are listening to the registration and enrollment events sent within the LMS service.

The following is the implementation for the signal receiver listening for the event ``STUDENT_REGISTRATION_COMPLETED``:

.. code-block:: python

    # File openedx_events_2_zapier/receivers.py
    class OpenedxEventsSamplesConfig(AppConfig):
    """
    Configuration for the openedx_events_2_zapier Django application.
    """

    name = "openedx_events_2_zapier"

    plugin_app = {
        "settings_config": {},
        "signals_config": {
            "lms.djangoapp": {
                "relative_path": "receivers",
                "receivers": [
                    {
                        "receiver_func_name": "send_user_data_to_webhook",
                        "signal_path": "openedx_events.learning.signals.STUDENT_REGISTRATION_COMPLETED",
                    },
                ],
            }
        },
    }

    # File openedx_events_2_zapier/receivers.py
    def send_user_data_to_webhook(user, **kwargs):
        """
        POST user's data after STUDENT_REGISTRATION_COMPLETED event is sent.

        The data sent to the webhook is, for example:

        'user_id': 39,
        'user_is_active': True,
        'user_pii_username': 'test',
        'user_pii_email': 'test@example.com',
        'user_pii_name': 'test',
        'event_metadata_id': UUID('b1be2fac-1af1-11ec-bdf4-0242ac12000b'),
        'event_metadata_event_type': 'org.openedx.learning.student.registration.completed.v1',
        'event_metadata_minorversion': 0,
        'event_metadata_source': 'openedx/lms/web',
        'event_metadata_sourcehost': 'lms.devstack.edx',
        'event_metadata_time': datetime.datetime(2021, 9, 21, 15, 36, 31, 311506),
        'event_metadata_sourcelib': [0, 6, 0]

        This format is convenient for Zapier to read.
        """
        user_info = asdict(user)
        event_metadata = asdict(kwargs.get("metadata"))
        zapier_payload = {
            "user": user_info,
            "event_metadata": event_metadata,
        }
        requests.post(
            settings.ZAPIER_REGISTRATION_WEBHOOK,
            flatten_dict(zapier_payload),
        )

Those receivers work out of the box after the plugin installation. Now, we must
set the plugin settings which indicate where to send the events data. For this,
go to ``env/apps/openedx/settings/development.py`` and add your Zapier configuration:

.. code-block:: python

    ZAPIER_REGISTRATION_WEBHOOK = "https://hooks.zapier.com/hooks/catch/<account>/<webhook>/"
    ZAPIER_ENROLLMENT_WEBHOOK = "https://hooks.zapier.com/hooks/catch/<account>/<webhook>/"

Getting data from Zapier
------------------------

Now that you have configured both receivers, you'll need to trigger the events
so you receive the events data in Zapier. Try it out!

.. _openedx-events-2-zapier: https://github.com/eduNEXT/openedx-events-2-zapier
.. _Tutor: https://github.com/overhangio/tutor
.. _Django plugin: https://github.com/openedx/edx-django-utils/blob/master/edx_django_utils/plugins/README.rst

.. warning::
    The receiver function implemented in this tutorial was intended to be lightweight, just to serve as an example for events' receivers. However, in production
    settings, we encourage the use of asynchronous tasks to avoid creating bottlenecks.
