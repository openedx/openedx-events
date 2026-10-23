"""
This file contains all test for the tooling.py file.

Classes:
    EventsToolingTest: Test events tooling.
"""
import base64
import datetime
import sys
from contextlib import contextmanager
from unittest.mock import ANY, Mock, patch
from uuid import UUID, uuid1

import attr
import ddt
import pytest
from django.db import transaction
from django.test import TestCase, TransactionTestCase, override_settings

from openedx_events.data import EventsMetadata
from openedx_events.exceptions import SenderValidationError
from openedx_events.learning.data import UserData, UserPersonalData
from openedx_events.learning.signals import SESSION_LOGIN_COMPLETED
from openedx_events.testing import FreezeSignalCacheMixin
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
        self.public_signal = OpenEdxPublicSignal(  # pylint: disable=missing-or-incorrect-annotation
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

        self.assertEqual(metadata_as_dict, {**expected_metadata, **metadata_as_dict})
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

        self.assertEqual(metadata_as_dict, {**expected_metadata, **metadata_as_dict})
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
            metadata=metadata, send_robust=True, foo="bar", from_event_bus=True,
            send_on_commit=False, send_async=False,
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


def _make_user_data():
    """Build a UserData payload for the real SESSION_LOGIN_COMPLETED signal."""
    return UserData(
        pii=UserPersonalData(username="alice", email="alice@example.com", name="Alice"),
        id=1,
        is_active=True,
    )


class SendEventOnCommitTests(TestCase):
    """
    Tests for the ``send_on_commit`` parameter of ``send_event``.

    Uses ``TestCase.captureOnCommitCallbacks`` to observe callbacks that
    ``transaction.on_commit`` registers inside the outer test-level
    transaction.
    """

    def setUp(self):
        super().setUp()
        self.receiver = Mock(return_value="ok")
        SESSION_LOGIN_COMPLETED.connect(self.receiver)
        self.addCleanup(SESSION_LOGIN_COMPLETED.disconnect, self.receiver)

    def test_send_on_commit_defers_until_commit(self):
        """
        With ``send_on_commit=True`` inside a transaction, the receiver is
        only called once the enclosing transaction commits.
        """
        with self.captureOnCommitCallbacks(execute=False) as callbacks:
            result = SESSION_LOGIN_COMPLETED.send_event(
                send_on_commit=True, user=_make_user_data(),
            )

        self.receiver.assert_not_called()
        self.assertEqual(result, [])
        self.assertEqual(len(callbacks), 1)

        # Now "commit" and verify receiver runs.
        for cb in callbacks:
            cb()
        self.receiver.assert_called_once()

    def test_send_on_commit_callback_runs_receiver(self):
        """
        Executing the captured ``on_commit`` callback (simulating a commit)
        triggers the receiver, verifying that the work registered under the
        callback is the actual signal send.
        """
        with self.captureOnCommitCallbacks(execute=True):
            SESSION_LOGIN_COMPLETED.send_event(
                send_on_commit=True, user=_make_user_data(),
            )
        self.receiver.assert_called_once()


class SendEventOnCommitRollbackTests(TransactionTestCase):
    """
    Tests that ``send_on_commit`` suppresses sending when the transaction
    rolls back. Uses ``TransactionTestCase`` so transactions actually commit
    and roll back.
    """

    def setUp(self):
        super().setUp()
        self.receiver = Mock(return_value="ok")
        SESSION_LOGIN_COMPLETED.connect(self.receiver)
        self.addCleanup(SESSION_LOGIN_COMPLETED.disconnect, self.receiver)

    def test_send_on_commit_immediate_when_no_transaction(self):
        """
        Outside any transaction, ``send_on_commit=True`` sends immediately
        (per Django's ``transaction.on_commit`` contract).
        """
        SESSION_LOGIN_COMPLETED.send_event(
            send_on_commit=True, user=_make_user_data(),
        )
        self.receiver.assert_called_once()

    def test_send_on_commit_not_sent_on_rollback(self):
        """
        If the transaction rolls back, the on_commit callback is never run,
        so the event is not sent.
        """
        class _Rollback(Exception):
            pass

        with self.assertRaises(_Rollback):
            with transaction.atomic():
                SESSION_LOGIN_COMPLETED.send_event(
                    send_on_commit=True, user=_make_user_data(),
                )
                raise _Rollback()

        self.receiver.assert_not_called()


class SendEventAsyncTests(TestCase):
    """
    Tests for the ``send_async`` parameter of ``send_event``.
    """

    def setUp(self):
        super().setUp()
        self.receiver = Mock(return_value="ok")
        SESSION_LOGIN_COMPLETED.connect(self.receiver)
        self.addCleanup(SESSION_LOGIN_COMPLETED.disconnect, self.receiver)

    @patch("openedx_events.tasks.send_async_event.delay")
    def test_send_async_dispatches_celery_task(self, mock_delay):
        """
        With ``send_async=True``, the receiver is not called synchronously.
        Instead a Celery task is dispatched with the serialized event data.
        """
        result = SESSION_LOGIN_COMPLETED.send_event(
            send_async=True, user=_make_user_data(),
        )

        self.assertEqual(result, [])
        self.receiver.assert_not_called()
        mock_delay.assert_called_once_with(
            SESSION_LOGIN_COMPLETED.event_type, ANY, ANY,
        )
        _, metadata_json, event_data_b64 = mock_delay.call_args.args
        # The metadata round-trips through JSON.
        self.assertEqual(
            EventsMetadata.from_json(metadata_json).event_type,
            SESSION_LOGIN_COMPLETED.event_type,
        )
        # The event data is valid base64.
        base64.b64decode(event_data_b64)

    def test_send_async_task_sends_event(self):
        """
        End-to-end: when ``send_async=True``, running the dispatched Celery
        task synchronously delivers the event to the receiver with the same
        metadata and a payload that round-trips through Avro.
        """
        captured = {}

        def _capture_delay(event_type, metadata_json, event_data_b64):
            captured["args"] = (event_type, metadata_json, event_data_b64)

        with patch("openedx_events.tasks.send_async_event.delay", side_effect=_capture_delay):
            SESSION_LOGIN_COMPLETED.send_event(
                send_async=True, user=_make_user_data(),
            )

        self.receiver.assert_not_called()

        # Now run the task body directly, simulating a Celery worker.
        from openedx_events.tasks import send_async_event  # pylint: disable=import-outside-toplevel
        send_async_event(*captured["args"])

        self.receiver.assert_called_once()
        call_kwargs = self.receiver.call_args.kwargs
        self.assertEqual(call_kwargs["signal"], SESSION_LOGIN_COMPLETED)
        self.assertEqual(call_kwargs["user"], _make_user_data())
        self.assertEqual(call_kwargs["metadata"].event_type, SESSION_LOGIN_COMPLETED.event_type)
        self.assertEqual(call_kwargs["from_event_bus"], False)


class SendEventAsyncOnCommitTests(TestCase):
    """
    Tests combining ``send_on_commit=True`` with ``send_async=True``: the
    Celery task dispatch should be deferred until the transaction commits.
    """

    def setUp(self):
        super().setUp()
        self.receiver = Mock(return_value="ok")
        SESSION_LOGIN_COMPLETED.connect(self.receiver)
        self.addCleanup(SESSION_LOGIN_COMPLETED.disconnect, self.receiver)

    @patch("openedx_events.tasks.send_async_event.delay")
    def test_async_on_commit_defers_dispatch(self, mock_delay):
        """
        ``send_async=True`` + ``send_on_commit=True`` in a transaction: the
        Celery dispatch is registered as an on_commit callback, not invoked
        immediately.
        """
        with self.captureOnCommitCallbacks(execute=False) as callbacks:
            SESSION_LOGIN_COMPLETED.send_event(
                send_async=True, send_on_commit=True, user=_make_user_data(),
            )

        mock_delay.assert_not_called()
        self.assertEqual(len(callbacks), 1)

        for cb in callbacks:
            cb()
        mock_delay.assert_called_once()


class SendEventAsyncOnCommitRollbackTests(TransactionTestCase):
    """Rollback behavior for ``send_async`` + ``send_on_commit``."""

    def setUp(self):
        super().setUp()
        self.receiver = Mock(return_value="ok")
        SESSION_LOGIN_COMPLETED.connect(self.receiver)
        self.addCleanup(SESSION_LOGIN_COMPLETED.disconnect, self.receiver)

    @patch("openedx_events.tasks.send_async_event.delay")
    def test_async_on_commit_not_dispatched_on_rollback(self, mock_delay):
        class _Rollback(Exception):
            pass

        with self.assertRaises(_Rollback):
            with transaction.atomic():
                SESSION_LOGIN_COMPLETED.send_event(
                    send_async=True, send_on_commit=True, user=_make_user_data(),
                )
                raise _Rollback()

        mock_delay.assert_not_called()
        self.receiver.assert_not_called()


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
