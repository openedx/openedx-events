"""
This file contains all test for the tooling.py file.

Classes:
    EventsToolingTest: Test events tooling.
"""
import datetime
import sys
from contextlib import contextmanager
from unittest.mock import Mock, patch
from uuid import UUID, uuid1

import attr
import ddt
import pytest
from django.test import TestCase, override_settings

from openedx_events.data import EventsMetadata
from openedx_events.exceptions import SenderValidationError
from openedx_events.tests.utils import FreezeSignalCacheMixin
from openedx_events.tooling import OpenEdxPublicSignal, _process_all_signals_modules, load_all_signals


@contextmanager
def receivers_attached(signal, receivers):
    """
    Attach the receivers to the signal for the duration of the context.
    """
    try:
        for receiver in receivers:
            signal.connect(receiver)

        yield
    finally:
        for receiver in receivers:
            signal.disconnect(receiver)


@ddt.ddt
class OpenEdxPublicSignalTestCache(FreezeSignalCacheMixin, TestCase):
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

        self.receiver_error = Exception("fake error")

        def error_receiver(*args, **kwargs):
            raise self.receiver_error

        self.ok_receiver = Mock(return_value="success")
        self.error_receiver = error_receiver

    def test_string_representation(self):
        """
        This methods checks the string representation for events base class.

        Expected behavior:
            The representation contains the event_type.
        """
        self.assertIn(self.event_type, str(self.public_signal))

    def test_get_signal_by_type(self):
        """
        Test found and not-found behavior.
        """
        assert isinstance(
            OpenEdxPublicSignal.get_signal_by_type('org.openedx.learning.session.login.completed.v1'),
            OpenEdxPublicSignal
        )

        with pytest.raises(KeyError):
            OpenEdxPublicSignal.get_signal_by_type('xxx')

    @override_settings(SERVICE_VARIANT="lms")
    @patch("openedx_events.data.openedx_events")
    @patch("openedx_events.data.socket")
    @patch("openedx_events.data.datetime")
    def test_generate_signal_metadata(self, datetime_mock, socket_mock, events_package_mock):
        """
        This methods tests getting the generated metadata for an event.

        Expected behavior:
            Returns the metadata containing information about the event.
        """
        events_package_mock.__version__ = "0.1.0"
        socket_mock.gethostname.return_value = "edx.devstack.lms"
        expected_time = datetime.datetime.now(datetime.timezone.utc)
        datetime_mock.now.return_value = expected_time
        expected_metadata = {
            "event_type": self.event_type,
            "minorversion": 0,
            "source": "openedx/lms/web",
            "sourcehost": "edx.devstack.lms",
            "sourcelib": [0, 1, 0],
            "time": expected_time,
        }

        metadata = self.public_signal.generate_signal_metadata()
        metadata_as_dict = attr.asdict(metadata)

        self.assertEqual(metadata_as_dict, expected_metadata | metadata_as_dict)
        self.assertIsInstance(metadata.id, UUID)

    @override_settings(SERVICE_VARIANT="lms")
    @patch("openedx_events.data.openedx_events")
    @patch("openedx_events.data.socket")
    def test_generate_signal_metadata_with_valid_time(self, socket_mock, events_package_mock):
        """
        Tests getting the generated metadata for an event, providing a valid time in UTC.

        Expected behavior:
            Returns the metadata containing information about the event.
        """
        events_package_mock.__version__ = "0.1.0"
        socket_mock.gethostname.return_value = "edx.devstack.lms"
        expected_time = datetime.datetime.now(datetime.timezone.utc)
        expected_metadata = {
            "event_type": self.event_type,
            "minorversion": 0,
            "source": "openedx/lms/web",
            "sourcehost": "edx.devstack.lms",
            "sourcelib": [0, 1, 0],
            "time": expected_time,
        }

        metadata = self.public_signal.generate_signal_metadata(time=expected_time)
        metadata_as_dict = attr.asdict(metadata)

        self.assertEqual(metadata_as_dict, expected_metadata | metadata_as_dict)
        self.assertIsInstance(metadata.id, UUID)

    @ddt.data(
        (1, TypeError, "'time' must be <class 'datetime.datetime'",),
        # WARNING: utcnow() has no timezone, and could be misinterpreted in local time
        (datetime.datetime.utcnow(), ValueError, "'time' must have timezone.utc",),
    )
    @ddt.unpack
    def test_generate_signal_metadata_fails_with_invalid_time(
        self, invalid_time, error_class, error_message
    ):
        """
        Tests getting generated metadata for an event fails with a non-UTC time.

        Expected behavior:
            Raises an exception
        """
        with self.assertRaisesMessage(error_class, error_message):
            self.public_signal.generate_signal_metadata(time=invalid_time)

    @patch("openedx_events.tooling.OpenEdxPublicSignal.generate_signal_metadata")
    @patch("openedx_events.tooling.Signal.send")
    def test_send_event_allow_failure_successfully(self, send_mock, fake_metadata):
        """
        This method tests the process of sending an event that's allowed to fail.

        Expected behavior:
            The event is sent as a django signal with send method.
        """
        expected_metadata = Mock(some_data="some_data")
        fake_metadata.return_value = expected_metadata
        self.public_signal.allow_send_event_failure()

        self.public_signal.send_event(user=self.user_mock)

        send_mock.assert_called_once_with(
            sender=None,
            user=self.user_mock,
            metadata=expected_metadata,
            from_event_bus=False,
        )

    @patch("openedx_events.tooling.OpenEdxPublicSignal.generate_signal_metadata")
    @patch("openedx_events.tooling.log", autospec=True)
    @patch("openedx_events.tooling.format_responses", autospec=True, return_value="fake-output")
    def test_send_robust_event_successfully(self, format_responses_mock, log_mock, fake_metadata):
        """
        This method tests the process of sending an event that won't crash.

        Expected behavior:
            The event is sent as a django signal with send_robust method.
        """
        expected_metadata = Mock(some_data="some_data")
        fake_metadata.return_value = expected_metadata

        with receivers_attached(self.public_signal, [self.ok_receiver, self.error_receiver]):
            self.public_signal.send_event(user=self.user_mock)

        self.ok_receiver.assert_called_once_with(
            signal=self.public_signal, sender=None, user=self.user_mock, metadata=expected_metadata,
            from_event_bus=False
        )
        # format_responses is mocked out because its output is
        # complicated enough to warrant its own set of tests.
        format_responses_mock.assert_called_once_with(
            [(self.ok_receiver, "success"), (self.error_receiver, self.receiver_error)], depth=2
        )
        log_mock.info.assert_called_once_with(
            "Responses of the Open edX Event <org.openedx.learning.session.login.completed.v1>: \nfake-output"
        )

    @patch("openedx_events.tooling.OpenEdxPublicSignal.generate_signal_metadata")
    def test_send_event_with_time(self, fake_metadata):
        """
        This method tests the process of sending an event with a time argument.

        Expected behavior:
            The generate_signal_metadata is called using the passed time.
        """
        expected_metadata = Mock(some_data="some_data")
        expected_time = datetime.datetime.now(datetime.timezone.utc)
        fake_metadata.return_value = expected_metadata

        self.public_signal.send_event(user=self.user_mock, time=expected_time)

        # generate_signal_metadata is fully tested elsewhere
        fake_metadata.assert_called_once_with(time=expected_time)

    @patch("openedx_events.tooling.OpenEdxPublicSignal._send_event_with_metadata")
    def test_send_event_with_custom_metadata(self, mock_send_event_with_metadata):
        """
        This method tests the process of sending an event with custom metadata.

        Expected behavior:
            The _send_event_with_metadata call is passed the appropriate metadata.

        Note:
            The _send_event_with_metadata is fully tested with the various send_event tests.
        """
        metadata = EventsMetadata(
            id=uuid1(),
            event_type=self.event_type,
            minorversion=99,
            source="mock-source",
            sourcehost="mock-sourcehost",
            time=datetime.datetime.now(datetime.timezone.utc),
            sourcelib=(6, 1, 7),
        )
        expected_response = "mock-response"
        mock_send_event_with_metadata.return_value = expected_response

        response = self.public_signal.send_event_with_custom_metadata(metadata, foo="bar")

        assert response == expected_response
        mock_send_event_with_metadata.assert_called_once_with(
            metadata=metadata, send_robust=True, foo="bar", from_event_bus=True
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
            A warning is showed advising to use Open edX events custom
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

    @patch("openedx_events.tooling.Signal.send")
    def test_send_event_disabled(self, send_mock):
        """
        This method tests sending an event that has been disabled.

        Expected behavior:
            The Django Signal associated to the event is not sent.
        """
        self.public_signal.disable()

        result = self.public_signal.send_event(sender=Mock())

        send_mock.assert_not_called()
        self.assertListEqual([], result)


class TestLoadAllSignals(FreezeSignalCacheMixin, TestCase):
    """ Tests for the load_all_signals method"""
    def setUp(self):
        # load_all_signals does spooky things with module loading,
        # so save the current state of any loaded signals modules to avoid disrupting other tests
        super().setUp()
        self.old_signal_modules = {}

        def save_module(module_name):
            if module_name in sys.modules:
                self.old_signal_modules[module_name] = sys.modules[module_name]
        _process_all_signals_modules(save_module)

    def tearDown(self):
        for k, v in self.old_signal_modules.items():
            sys.modules[k] = v
        super().tearDown()

    def test_load_all_signals(self):
        """
        Tests load_all_signals loads all the signals in the entire library

        It's not the most robust since it just tests a few arbitrary signals but actually testing all the signals
        would require updating this test every time a new signal is added
        """

        # remove any existing imports of signals modules
        for k in self.old_signal_modules:
            sys.modules.pop(k)

        # this class uses FreezeSignalCacheMixin so we can safely remove everything from the OpenEdxPublicSignal
        # cache and it shouldn't affect any other tests
        OpenEdxPublicSignal._mapping = {}  # pylint: disable=protected-access
        OpenEdxPublicSignal.instances = []
        with pytest.raises(KeyError):
            OpenEdxPublicSignal.get_signal_by_type('org.openedx.content_authoring.course.catalog_info.changed.v1')
        with pytest.raises(KeyError):
            OpenEdxPublicSignal.get_signal_by_type('org.openedx.learning.course.enrollment.created.v1')

        load_all_signals()
        assert isinstance(
            OpenEdxPublicSignal.get_signal_by_type('org.openedx.content_authoring.course.catalog_info.changed.v1'),
            OpenEdxPublicSignal
        )
        assert isinstance(
            OpenEdxPublicSignal.get_signal_by_type('org.openedx.learning.course.enrollment.created.v1'),
            OpenEdxPublicSignal
        )
