"""
Tooling necessary to use Open edX events.
"""
import warnings

from django.dispatch import Signal

from openedx_events.data import EventsMetadata
from openedx_events.exceptions import InstantiationError, SenderValidationError


class OpenEdxPublicSignal(Signal):
    """
    Custom class used to create Open edX events.
    """

    def __init__(self, event_type, data, minor_version=0):
        """
        Init method for OpenEdxPublicSignal definition class.

        Arguments:
            event_type (str): name of the event.
            data (dict): attributes passed to the event.
            minor_version (int): version of the event type.
        """
        if not event_type:
            raise InstantiationError(
                message="Missing required argument 'event_type'"
            )
        if not data:
            raise InstantiationError(
                event_type=event_type, message="Missing required argument 'data'"
            )
        self.init_data = data
        self.event_type = event_type
        self.minor_version = minor_version
        super().__init__()

    def __repr__(self):
        """
        Represent OpenEdxPublicSignal as a string.
        """
        return "<OpenEdxPublicSignal: {event_type}>".format(event_type=self.event_type)

    def generate_signal_metadata(self):
        """
        Generate signal metadata when an event is sent.

        These fields are generated on the fly and are a subset of the Event
        Message defined in the OEP-41.

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
        )

    def send_event(self, send_robust=False, **kwargs):
        """
        Send events to all connected receivers.

        Used to send events just like Django signals are sent. In addition,
        some validations are run on the arguments, and then relevant metadata
        that can be used for logging or debugging purposes is generated.
        Besides this behavior, send_event behaves just like the send method.

        Example usage:
            >>> STUDENT_REGISTRATION_COMPLETED.send_event(
                user=user_data, registration=registration_data,
            )
            [(<function callback at 0x7f2ce638ef70>, 'callback response')]

        Keyword arguments:
            send_robust (bool): determines whether the Django signal will be
            sent using the method `send` or `send_robust`.

        Returns:
            list: response of each receiver following the format
            [(receiver, response), ... ]

        Exceptions raised:
            SenderValidationError: raised when there's a mismatch between
            arguments passed to this method and arguments used to initialize
            the event.
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

        validate_sender()

        kwargs["metadata"] = self.generate_signal_metadata()

        if send_robust:
            return super().send_robust(sender=None, **kwargs)
        return super().send(sender=None, **kwargs)

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
