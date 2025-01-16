"""
Tooling necessary to use Open edX events.
"""
import pkgutil
import warnings
from importlib import import_module
from logging import getLogger

from django.conf import settings
from django.db import connection
from django.dispatch import Signal
from edx_django_utils.cache import RequestCache

from openedx_events.data import EventsMetadata
from openedx_events.exceptions import SenderValidationError
from openedx_events.utils import format_responses

log = getLogger(__name__)

# If a signal is explicitly not for use with the event bus, add it to this list
#  and document why in the event's annotations
KNOWN_UNSERIALIZABLE_SIGNALS = [
    "org.openedx.learning.discussions.configuration.changed.v1",
    "org.openedx.content_authoring.course.certificate_config.changed.v1",
    "org.openedx.content_authoring.course.certificate_config.deleted.v1",
    "org.openedx.learning.user.notification.requested.v1",
    "org.openedx.learning.forum.thread.created.v1",
    "org.openedx.learning.forum.thread.response.created.v1",
    "org.openedx.learning.forum.thread.response.comment.created.v1",
    "org.openedx.learning.course.notification.requested.v1",
    "org.openedx.learning.ora.submission.created.v1",
]

SIGNAL_PROCESSED_FROM_EVENT_BUS = "from_event_bus"


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

        Raises:
            Raises KeyError if the event is not found.
        """
        return cls._mapping[event_type]

    def generate_signal_metadata(self, time=None):
        """
        Generate signal metadata when an event is sent.

        These fields are generated on the fly and are a subset of the Event
        Message defined in the OEP-41.

        Arguments:
            time (datetime): (Optional) Timestamp when the event was sent with
              UTC timezone. Defaults to current time in UTC. See OEP-41 for more details.

        Example usage:
            >>> metadata = \
                STUDENT_REGISTRATION_COMPLETED.generate_signal_metadata()
                attr.asdict(metadata)
            >>> {
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

    def _send_event_with_metadata(self, metadata, send_robust=True, from_event_bus=False, **kwargs):
        """
        Send events to all connected receivers with the provided metadata.

        This method is for internal use only.

        Arguments:
            metadata (EventsMetadata): The metadata to be sent with the signal.
            send_robust (bool): Defaults to True. See Django signal docs.
            from_event_bus (bool): Defaults to False. If True, the signal is
              being sent from the event bus. This is used to prevent infinite
              loops when the event bus is consuming events. It should not be
              used when sending events from the application.

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
        kwargs[SIGNAL_PROCESSED_FROM_EVENT_BUS] = from_event_bus

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
            >>> [(<function callback at 0x7f2ce638ef70>, 'callback response')]

        Arguments:
            send_robust (bool): Defaults to True. See Django signal docs.
            time (datetime): (Optional - see note) Timestamp when the event was sent with UTC
               timezone. For events requiring a DB create or update, use the timestamp from the DB
               record. Defaults to current time in UTC. This argument is optional for backward
               compatibility, but ideally would be explicitly set. See OEP-41 for details.

        Keyword Arguments:
           kwargs: Data to be sent to the signal's receivers. The keys must match the attributes defined in
              the event's data.

        Returns:
            list: response of each receiver following the format [(receiver, response), ... ].
               The list is empty if the event is disabled.

        Raises:
            SenderValidationError: raised when there's a mismatch between arguments passed
               to this method and arguments used to initialize the event.
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
        return self._send_event_with_metadata(
            metadata=metadata, send_robust=send_robust, from_event_bus=True, **kwargs
        )

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
    """
    Walk the package tree and apply func on all signals.py files.

    Arguments:
        func: A method that takes a module name as its parameter
    """
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
    _process_all_signals_modules(import_module)


def _reconnect_to_db_if_needed():  # pragma: no cover
    """
    Reconnects the db connection if needed.

    This is important because Django only does connection validity/age checks as part of
    its request/response cycle, which isn't in effect for the consume-loop. If we don't
    force these checks, a broken connection will remain broken indefinitely. For most
    consumers, this will cause event processing to fail.
    """
    has_connection = bool(connection.connection)
    requires_reconnect = has_connection and not connection.is_usable()
    if requires_reconnect:
        connection.connect()


def _clear_request_cache():  # pragma: no cover
    """
    Clear the RequestCache so that each event consumption starts fresh.

    Signal handlers may be written with the assumption that they are called in the context
    of a web request, so we clear the request cache just in case.
    """
    RequestCache.clear_all_namespaces()


def prepare_for_new_work_cycle():  # pragma: no cover
    """
    Ensure that the application state is appropriate for performing a new unit of work.

    This mimics some setup/teardown that is normally performed by Django in its
    request/response based architecture and that is needed for ensuring a clean and
    usable state in this worker-based application.

    See https://github.com/openedx/openedx-events/issues/236 for details.
    """
    # Ensure that the database connection is active and usable.
    _reconnect_to_db_if_needed()

    # Clear the request cache, in case anything in the signal handlers rely on it.
    _clear_request_cache()
