.. include:: ../common_refs.rst

Using Open edX Events in the LMS Service
##########################################

Live Example
**************

For a complete and detailed example you can see the `openedx-events-2-zapier`_ plugin and its `documentation`_. This is a fully functional plugin that connects to ``STUDENT_REGISTRATION_COMPLETED`` and ``COURSE_ENROLLMENT_CREATED`` and sends the relevant information to Zapier or any other services.

Let's see it working!

Setup Your Environment
*************************

This tutorial assumes you are using `Tutor`_ > 18.x and its default services are already provisioned.

Installation
==============

For this tutorial to work, you will need a ``openedx`` image with the following package installed:

- `openedx-events-2-zapier`_

You can use your preferred method to `install extra requirements in Tutor`_.

Configuration
==============

The package we just installed is a `Django plugin`_, which adds additional configurations to our working environment thanks to the extension mechanisms that were put in place. Now, :term:`event receivers <Event Receiver>` are listening to the registration and enrollment events sent within the LMS service.

The following is the implementation for the :term:`event receivers <Event Receiver>` listening for the event ``STUDENT_REGISTRATION_COMPLETED``:

.. code-block:: python

    # File openedx_events_2_zapier/receivers.py
    class OpenedxEvents2ZapierConfig(AppConfig):
        """
        Configuration for the openedx_events_2_zapier Django application.
        """

        name = "openedx_events_2_zapier"

        plugin_app = {
            "settings_config": {
                "lms.djangoapp": {
                    "common": {"relative_path": "settings.common"},
                    "test": {"relative_path": "settings.test"},
                    "production": {"relative_path": "settings.production"},
                },
                "cms.djangoapp": {
                    "common": {"relative_path": "settings.common"},
                    "test": {"relative_path": "settings.test"},
                    "production": {"relative_path": "settings.production"},
                },
            },
        }

        def ready(self):
            """Perform initialization tasks required for the plugin."""
            from openedx_events_2_zapier import handlers

    # File openedx_events_2_zapier/receivers.py
    @receiver(STUDENT_REGISTRATION_COMPLETED)
    def send_user_data_to_webhook(
        signal, sender, user, metadata, **kwargs  # pylint: disable=unused-argument
    ):
        zapier_payload = {
            "user": asdict(user),
            "event_metadata": asdict(metadata),
        }
        send_data_to_zapier.delay(settings.ZAPIER_REGISTRATION_WEBHOOK, zapier_payload)

Those `event receivers <Event Receiver>` work out of the box after the plugin installation. Now, we must set the plugin settings which indicate where to send the events data. For this, go to ``env/apps/openedx/settings/development.py`` and add your Zapier configuration:

.. code-block:: python

    ZAPIER_REGISTRATION_WEBHOOK = "https://hooks.zapier.com/hooks/catch/<account>/<webhook>/"
    ZAPIER_ENROLLMENT_WEBHOOK = "https://hooks.zapier.com/hooks/catch/<account>/<webhook>/"

Getting data from Zapier
========================

Now that you have configured both :term:`event receivers <Event Receiver>`, you'll need to trigger the events so you receive the events data in Zapier. Try it out!

.. warning::
    The `event receiver <Event Receiver>` function in this tutorial is designed to be lightweight, serving as a basic example of event receivers. However, it has not been tested in a production environment. When implementing an event receiver for real-world use, consider additional factors such as error handling, logging, and performance.

.. _Django plugin: https://github.com/openedx/edx-django-utils/blob/master/edx_django_utils/plugins/README.rst
.. _documentation: https://edunext.github.io/openedx-events-2-zapier/
.. _install extra requirements in Tutor: https://docs.tutor.edly.io/configuration.html#installing-extra-xblocks-and-requirements

**Maintenance chart**

+--------------+-------------------------------+----------------+--------------------------------+
| Review Date  | Reviewer                      |   Release      |Test situation                  |
+--------------+-------------------------------+----------------+--------------------------------+
|2025-02-13    |  Maria Grimaldi               |   Sumac        |Pass.                           |
+--------------+-------------------------------+----------------+--------------------------------+
