"""This file contains all test for the tooling.py file.

Classes:
    EventsToolingTest: Test events tooling.
"""
from unittest.mock import Mock, patch

import attr
import ddt
from django.test import TestCase, override_settings

from openedx_events.exceptions import InstantiationError, SenderValidationError
from openedx_events.tooling import OpenEdxPublicSignal


@ddt.ddt
class OpenEdxPublicSignalTest(TestCase):
    """
    Test cases for Open edX events base class.
    """

    def setUp(self):
        """
        Setup common conditions for every test case.
        """
        super().setUp()
        self.event_type = "org.openedx.learning.session.login.completed.v1"
        self.user_mock = Mock()
        self.data_attr = {
            "user": Mock,
        }
        self.public_signal = OpenEdxPublicSignal(
            event_type=self.event_type,
            data=self.data_attr,
        )

    def test_string_representation(self):
        """
        This methods checks the string representation for events base class.

        Expected behavior:
            The representation contains the event_type.
        """
        self.assertIn(self.event_type, str(self.public_signal))

    @override_settings(SERVICE_VARIANT="lms")
    @patch("openedx_events.data.openedx_events")
    @patch("openedx_events.data.socket")
    def test_get_signal_metadata(self, socket_mock, events_package_mock):
        """
        This methods tests getting the generated metadata for an event.

        Expected behavior:
            Returns the metadata containing information about the event.
        """
        events_package_mock.__version__ = "0.1.0"
        socket_mock.gethostname.return_value = "edx.devstack.lms"
        expected_metadata = {
            "event_type": self.event_type,
            "minorversion": 0,
            "source": "openedx/lms/web",
            "sourcehost": "edx.devstack.lms",
            "sourcelib": [0, 1, 0],
        }

        metadata = self.public_signal.generate_signal_metadata()

        self.assertDictContainsSubset(expected_metadata, attr.asdict(metadata))

    @ddt.data(
        ("", {"user": Mock()}, "event_type"),
        ("org.openedx.learning.session.login.completed.v1", None, "data"),
    )
    @ddt.unpack
    def test_event_instantiation_exception(
        self, event_type, event_data, missing_argument
    ):
        """
        This method tests when an event is instantiated without event_type or
        event data.

        Expected behavior:
            An InstantiationError exception is raised.
        """
        exception_message = "InstantiationError {event_type}: Missing required argument '{missing_argument}'".format(
            event_type=event_type, missing_argument=missing_argument
        )

        with self.assertRaisesMessage(InstantiationError, exception_message):
            OpenEdxPublicSignal(event_type=event_type, data=event_data)

    @patch("openedx_events.tooling.OpenEdxPublicSignal.generate_signal_metadata")
    @patch("openedx_events.tooling.Signal.send")
    def test_send_event_successfully(self, send_mock, fake_metadata):
        """
        This method tests the process of sending an event.

        Expected behavior:
            The event is sent as a django signal.
        """
        expected_metadata = {
            "some_data": "data",
            "raise_exception": True,
        }
        fake_metadata.return_value = expected_metadata

        self.public_signal.send_event(user=self.user_mock)

        send_mock.assert_called_once_with(
            sender=None,
            user=self.user_mock,
            metadata=expected_metadata,
        )

    @patch("openedx_events.tooling.OpenEdxPublicSignal.generate_signal_metadata")
    @patch("openedx_events.tooling.Signal.send_robust")
    def test_send_robust_event_successfully(self, send_robust_mock, fake_metadata):
        """
        This method tests the process of sending an event.

        Expected behavior:
            The event is sent as a django signal.
        """
        expected_metadata = {
            "some_data": "data",
            "raise_exception": True,
        }
        fake_metadata.return_value = expected_metadata

        self.public_signal.send_event(user=self.user_mock, send_robust=True)

        send_robust_mock.assert_called_once_with(
            sender=None,
            user=self.user_mock,
            metadata=expected_metadata,
        )

    @ddt.data(
        (
            {"student": Mock()},
            "SenderValidationError org.openedx.learning.session.login.completed.v1: "
            "Missing required argument 'user'",
        ),
        (
            {"user": {"student": Mock()}},
            "SenderValidationError org.openedx.learning.session.login.completed.v1: "
            "The argument 'user' is not instance of the Class Attribute 'type'",
        ),
        (
            {"student": Mock(), "user": Mock()},
            "SenderValidationError org.openedx.learning.session.login.completed.v1: "
            "There's a mismatch between initialization data and send_event arguments",
        ),
    )
    @ddt.unpack
    def test_invalid_sender(self, send_arguments, exception_message):
        """
        This method tests sending an event with invalid setup on the sender
        side.

        Expected behavior:
            A SenderValidationError exception is raised.
        """
        with self.assertRaisesMessage(SenderValidationError, exception_message):
            self.public_signal.send_event(**send_arguments)

    def test_send_event_with_django(self):
        """
        This method tests sending an event using the `send` built-in Django
        method.

        Expected behavior:
            A warning is showed advicing to use Open edX events custom
            send_signal method.
        """
        message = "Please, use 'send_event' when triggering an Open edX event."

        with self.assertWarns(Warning, msg=message):
            self.public_signal.send(sender=Mock())

    def test_send_robust_event_with_django(self):
        """
        This method tests sending an event using the `send` built-in Django
        method.

        Expected behavior:
            A warning is showed advicing to use Open edX events custom
            send_signal method.
        """
        message = "Please, use 'send_event' with send_robust equals to True when triggering an Open edX event."

        with self.assertWarns(Warning, msg=message):
            self.public_signal.send_robust(sender=Mock())
