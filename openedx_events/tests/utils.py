"""
Utils used by Open edX event tests.
"""
import pkgutil
from importlib import import_module

from openedx_events.tooling import OpenEdxPublicSignal


class FreezeSignalCacheMixin:
    """
    A mixin to be used by TestCases to avoid new signals persisting in the OpenEdxPublicSignal cache of instances.
    """

    @classmethod
    def setUpClass(cls):
        """
        Save current signal instances.
        """
        super().setUpClass()
        cls.pre_run_instances = list(OpenEdxPublicSignal.instances)
        cls.pre_run_mapping = dict(OpenEdxPublicSignal._mapping)  # pylint: disable=protected-access

    @classmethod
    def tearDownClass(cls):
        """
        Restore instance cache to pre-test state.
        """
        super().tearDownClass()
        OpenEdxPublicSignal.instances = cls.pre_run_instances
        OpenEdxPublicSignal._mapping = cls.pre_run_mapping  # pylint: disable=protected-access


class EventsIsolationMixin:
    """
    A mixin to be used by TestCases that want to isolate their use of Open edX Events.
    """

    @classmethod
    def disable_all_events(cls):
        """
        Disable all events Open edX Events from all subdomains.
        """
        for event in OpenEdxPublicSignal.all_events():
            event.disable()

    @classmethod
    def enable_all_events(cls):
        """
        Enable all events Open edX Events from all subdomains.
        """
        for event in OpenEdxPublicSignal.all_events():
            event.enable()

    @classmethod
    def enable_events_by_type(cls, *event_types):
        """
        Enable specific Open edX Events given their type.

        Arguments:
            event_types (list of `str`): types of events to enable.
        """
        for event_type in event_types:
            try:
                event = OpenEdxPublicSignal.get_signal_by_type(event_type)
            except KeyError:
                all_event_types = sorted(s.event_type for s in OpenEdxPublicSignal.all_events())
                err_msg = (
                    "You tried to enable event '{}', but I don't recognize that "
                    "signal type. Did you mean one of these?: {}"
                )
                raise ValueError(err_msg.format(event_type, all_event_types))  # pylint: disable=raise-missing-from
            event.enable()

    @classmethod
    def allow_send_events_failure(cls, *event_types):
        """
        Allow that send_event method fails for the specified event.

        This method determines which `send` method to use, send or send_robust.
        The first, raises receivers exceptions while the latter catches them.

        Arguments:
            event_types (list of `str`): types of events to enable.
        """
        for event_type in event_types:
            try:
                event = OpenEdxPublicSignal.get_signal_by_type(event_type)
            except KeyError:
                all_event_types = sorted(s.event_type for s in OpenEdxPublicSignal.all_events())
                err_msg = (
                    "You tried to enable event '{}', but I don't recognize that "
                    "signal type. Did you mean one of these?: {}"
                )
                raise ValueError(err_msg.format(event_type, all_event_types))  # pylint: disable=raise-missing-from
            event.allow_send_event_failure()


class OpenEdxEventsTestMixin(EventsIsolationMixin):
    """
    A mixin to be used by TestCases that want to isolate their use of Open edX Events.

    Example usage:

        class MyTestCase(TestCase, OpenEdxEventsTestCase):

            ENABLED_OPENEDX_EVENTS = ['org.openedx.learning.student.registration.completed.v1']

    This class assumes that's it's being used in conjunction TestCase or TestCase subclasses.
    """

    ENABLED_OPENEDX_EVENTS = []

    @classmethod
    def setUpClass(cls):
        """
        Start events isolation for class.
        """
        super().setUpClass()
        cls().start_events_isolation()

    @classmethod
    def start_events_isolation(cls):
        """
        Start Open edX Events isolation and then enable events by type.
        """
        cls().disable_all_events()
        cls().enable_events_by_type(*cls.ENABLED_OPENEDX_EVENTS)
        cls().allow_send_events_failure(*cls.ENABLED_OPENEDX_EVENTS)


def load_all_signals():
    """
    Ensure OpenEdxPublicSignal.all_events() cache is fully populated.

    Loads all non-test signals.py modules.
    """
    found = set()

    root = import_module('openedx_events')
    for m in pkgutil.walk_packages(root.__path__, root.__name__ + '.'):
        module_name = m.name
        if 'tests' in module_name.split('.') or '.test_' in module_name:
            continue
        if module_name.endswith('.signals'):
            import_module(module_name)
            found.add(module_name)

    # Check that the auto-discovered list matches the known modules.
    # This is just here to ensure that the auto-discovery is working
    # properly and doesn't start to silently fail.
    #
    # If this assertion fails because a module has been added, renamed,
    # or deleted, please update the hardcoded list.
    assert found == {
        'openedx_events.content_authoring.signals',
        'openedx_events.learning.signals',
    }
