"""
Tooling necessary to use Open edX events.
"""
import pkgutil
import warnings
from importlib import import_module
from logging import getLogger

from django.conf import settings
from django.dispatch import Signal

from openedx_events.data import EventsMetadata
from openedx_events.exceptions import SenderValidationError
from openedx_events.utils import format_responses

log = getLogger(__name__)


class OpenEdxPublicSignal(Signal):
    """
    Standardized Django Signals used to create Open edX events.
    """

    _mapping = {}
    instances = []

    def __init__(self, event_type, data, minor_version=0):
        """
        Init method for OpenEdxPublicSignal definition class.

        Arguments:
            event_type (str): name of the event.
            data (dict): attributes passed to the event.
            minor_version (int): version of the event type.
        """
        self.init_data = data
        self.event_type = event_type
        self.minor_version = minor_version
        self._allow_events = True
        self._allow_send_event_failure = False
        self.__class__.instances.append(self)
        self.__class__._mapping[self.event_type] = self
        super().__init__()

    def __repr__(self):
        """
        Represent OpenEdxPublicSignal as a string.
        """
        return "<OpenEdxPublicSignal: {event_type}>".format(event_type=self.event_type)

    @classmethod
    def all_events(cls):
        """
        Get all current events.
        """
        return cls.instances

    @classmethod
    def get_signal_by_type(cls, event_type):
        """
        Get event identified by type.

        Arguments:
            event_type (str): name of the event.

        Exceptions raised:
            Raises KeyError if not found.
        """
        return cls._mapping[event_type]

    def generate_signal_metadata(self, time=None):
        """
        Generate signal metadata when an event is sent.

        These fields are generated on the fly and are a subset of the Event
        Message defined in the OEP-41.

        Arguments:
            time (datetime): (Optional) Timestamp when the event was sent with
                UTC timezone. Defaults to current time in UTC. See OEP-41 for
                details.

        Example usage:
            >>> metadata = \
                STUDENT_REGISTRATION_COMPLETED.generate_signal_metadata()
                attr.asdict(metadata)
            {
                'event_type': '...learning.student.registration.completed.v1',
                'minorversion': 0,
                'time': '2021-06-09T14:12:45.320819Z',
                'source': 'openedx/lms/web',
                'sourcehost': 'edx.devstack.lms',
                'specversion': '1.0',
                'sourcelib: (0,1,0,),
            }
        """
        return EventsMetadata(
            event_type=self.event_type,
            minorversion=self.minor_version,
            time=time,
        )

    def _send_event_with_metadata(self, metadata, send_robust=True, **kwargs):
        """
        Send events to all connected receivers with the provided metadata.

        This method is for internal use only.

        Arguments:
            metadata (EventsMetadata): The metadata to be sent with the signal.
            send_robust (bool): Defaults to True. See Django signal docs.

        See ``send_event`` docstring for more details on its usage and behavior.
        """

        def validate_sender():
            """
            Run validations over the send arguments.

            The validation checks whether the send arguments match the
            arguments used when instantiating the event. If they don't a
            validation error is raised.
            """
            if len(kwargs) != len(self.init_data):
                raise SenderValidationError(
                    event_type=self.event_type,
                    message="There's a mismatch between initialization data and send_event arguments",
                )

            for key, value in self.init_data.items():
                argument = kwargs.get(key)
                if not argument:
                    raise SenderValidationError(
                        event_type=self.event_type,
                        message="Missing required argument '{key}'".format(key=key),
                    )
                if not isinstance(argument, value):
                    raise SenderValidationError(
                        event_type=self.event_type,
                        message="The argument '{key}' is not instance of the Class Attribute '{attr}'".format(
                            key=key, attr=value.__class__.__name__
                        ),
                    )

        if not self._allow_events:
            return []

        validate_sender()

        kwargs["metadata"] = metadata

        if self._allow_send_event_failure or settings.DEBUG or not send_robust:
            return super().send(sender=None, **kwargs)

        responses = super().send_robust(sender=None, **kwargs)
        log.info(
            f"Responses of the Open edX Event <{self.event_type}>: \n{format_responses(responses, depth=2)}",
        )

        return responses

    def send_event(self, send_robust=True, time=None, **kwargs):
        """
        Send events to all connected receivers.

        Arguments:
            send_robust (bool): Defaults to True. See Django signal docs.
            time (datetime): (Optional - see note) Timestamp when the event was
                sent with UTC timezone. For events requiring a DB create or
                update, use the timestamp from the DB record. Defaults to
                current time in UTC. This argument is optional for backward
                compatability, but ideally would be explicitly set. See OEP-41
                for details.
            kwargs: Data to be sent to the signal's receivers.

        Used to send events just like Django signals are sent. In addition,
        some validations are executed on the arguments, and then generates relevant
        metadata that can be used for logging or debugging purposes. Besides this behavior,
        send_event behaves just like the send method.

        If the event is disabled (i.e _allow_events is False), then this method
        won't have any effect. Meaning, the Django Signal won't be sent.

        Example usage:
            >>> STUDENT_REGISTRATION_COMPLETED.send_event(
                user=user_data, registration=registration_data,
            )
            [(<function callback at 0x7f2ce638ef70>, 'callback response')]

        Returns:
            list: response of each receiver following the format
            [(receiver, response), ... ]. Empty list if the event is disabled.

        Exceptions raised:
            SenderValidationError: raised when there's a mismatch between
            arguments passed to this method and arguments used to initialize
            the event.
        """
        metadata = self.generate_signal_metadata(time=time)
        return self._send_event_with_metadata(metadata=metadata, send_robust=send_robust, **kwargs)

    def send_event_with_custom_metadata(
            self, metadata, /, *, send_robust=True, **kwargs
    ):
        """
        Send events to all connected receivers using the provided metadata.

        This method works exactly like ``send_event``, except it uses the given
            event metadata rather than generating it. This is used by the
            event bus consumer, where we want to recreate the metadata used
            in the producer when resending the same signal on the consuming
            side.

        Arguments:
            metadata (EventsMetadata): The metadata to be sent with the signal.
            send_robust (bool): Defaults to True. See Django signal docs.
            kwargs: Data to be sent to the signal's receivers.

        See ``send_event`` docstring for more details.

        """
        return self._send_event_with_metadata(metadata=metadata, send_robust=send_robust, **kwargs)

    def send(self, sender, **kwargs):  # pylint: disable=unused-argument
        """
        Override method used to recommend the sender to adopt our custom send.
        """
        warnings.warn("Please, use 'send_event' when triggering an Open edX event.")

    def send_robust(self, sender, **kwargs):  # pylint: disable=unused-argument
        """
        Override method used to recommend the sender to adopt our custom send.
        """
        warnings.warn(
            "Please, use 'send_event' with send_robust equals to True when triggering an Open edX event."
        )

    def enable(self):
        """
        Enable all events. Meaning, send_event will send a Django signal.
        """
        self._allow_events = True

    def disable(self):
        """
        Disable all events. Meaning, send_event will have no effect.
        """
        self._allow_events = False

    def allow_send_event_failure(self):
        """
        Allow Django signal to fail. Meaning, uses send_robust instead of send.

        More information on send_robust in the Django official documentation.
        """
        self._allow_send_event_failure = True

def _process_all_signals_modules(func):
    root = import_module('openedx_events')
    for m in pkgutil.walk_packages(root.__path__, root.__name__ + '.'):
        module_name = m.name
        if 'tests' in module_name.split('.') or '.test_' in module_name:
            continue
        if module_name.endswith('.signals'):
            func(module_name)

def load_all_signals():
    """
    Ensure OpenEdxPublicSignal.all_events() cache is fully populated.
    Loads all non-test signals.py modules.
    """
    _process_all_signals_modules(lambda module_name: import_module(module_name))

