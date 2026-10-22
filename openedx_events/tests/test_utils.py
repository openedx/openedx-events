"""
Tests for openedx_events/testing.py.
"""
import ddt
from django.test import TestCase
from packaging.version import InvalidVersion

from openedx_events.testing import FreezeSignalCacheMixin, OpenEdxEventsTestMixin
from openedx_events.tooling import OpenEdxPublicSignal, load_all_signals
from openedx_events.utils import parse_sourcelib_release


class OpenEdxEventsTestMixinIsolationTest(FreezeSignalCacheMixin, TestCase):
    """
    Tests that OpenEdxEventsTestMixin does not leak disabled event state.

    The key regression: setUpClass disables all events, but before the fix
    there was no tearDownClass to re-enable them.  Any test class that ran
    *after* a mixin class with ENABLED_OPENEDX_EVENTS=[] would find every
    event still disabled.
    """

    def setUp(self):
        super().setUp()
        load_all_signals()

    def _all_events_enabled(self):
        return all(e._allow_events for e in OpenEdxPublicSignal.all_events())  # pylint: disable=protected-access

    def _all_events_disabled(self):
        return all(not e._allow_events for e in OpenEdxPublicSignal.all_events())  # pylint: disable=protected-access

    def test_teardown_re_enables_all_events(self):
        """
        After tearDownClass runs, every event should be enabled.

        Simulate the lifecycle of a mixin class with no enabled events:
        setUpClass disables everything, tearDownClass must restore it.
        """
        class EmptyEnabledEvents(OpenEdxEventsTestMixin, TestCase):
            ENABLED_OPENEDX_EVENTS = []

        # Before the class runs all events should be enabled.
        self.assertTrue(self._all_events_enabled())

        EmptyEnabledEvents.setUpClass()
        # After setUpClass, all events are disabled.
        self.assertTrue(self._all_events_disabled())

        EmptyEnabledEvents.tearDownClass()
        # After tearDownClass, all events must be re-enabled.
        self.assertTrue(
            self._all_events_enabled(),
            "tearDownClass should re-enable all events so subsequent test "
            "classes are not affected by this class's event isolation.",
        )

    def test_teardown_re_enables_events_after_subset_enabled(self):
        """
        The tearDownClass re-enables all events even when only a subset was enabled.
        """
        all_event_types = [e.event_type for e in OpenEdxPublicSignal.all_events()]
        one_event_type = all_event_types[0]

        class OneEnabledEvent(OpenEdxEventsTestMixin, TestCase):
            ENABLED_OPENEDX_EVENTS = [one_event_type]

        OneEnabledEvent.setUpClass()
        # Only one event should be enabled at this point.
        enabled = [e for e in OpenEdxPublicSignal.all_events() if e._allow_events]  # pylint: disable=protected-access
        self.assertEqual(len(enabled), 1)
        self.assertEqual(enabled[0].event_type, one_event_type)

        OneEnabledEvent.tearDownClass()
        self.assertTrue(
            self._all_events_enabled(),
            "tearDownClass should re-enable all events regardless of how many were enabled.",
        )


@ddt.ddt
class TestParseSourcelibRelease(TestCase):
    """Tests for parse_sourcelib_release utility."""

    @ddt.data(
        ("11.2.0", (11, 2, 0)),
        ("9.10.post1", (9, 10)),
        ("1.2.3rc1", (1, 2, 3)),
        ("2.0.dev4", (2, 0)),
    )
    @ddt.unpack
    def test_valid_pep440_versions(self, raw_version, expected):
        """It returns the release tuple for valid PEP 440 versions."""
        assert parse_sourcelib_release(raw_version) == expected

    def test_invalid_version_raises(self):
        """It raises InvalidVersion for malformed versions."""
        with self.assertRaises(InvalidVersion):
            parse_sourcelib_release("not-a-version")
