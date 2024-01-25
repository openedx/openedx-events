"""
Data attributes for events within the architecture subdomain `learning`.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.
"""
import json
import socket
from datetime import datetime, timezone
from uuid import UUID, uuid1

import attr
import attrs
from django.conf import settings

import openedx_events


def _ensure_utc_time(_, attribute, value):
    """
    Ensure the value is a UTC datetime.

    Note: Meant to be used along-side an instance_of attr validator.
    """
    if value.tzinfo and value.tzinfo == timezone.utc:
        return
    raise ValueError(f"'{attribute.name}' must have timezone.utc")


def get_service_name():
    """
    Get the service name that should be used in the source of an event.
    """
    # .. setting_name: EVENTS_SERVICE_NAME
    # .. setting_default: None
    # .. setting_description: Identifier for the producing/consuming service of an event. Used in setting the source in
    #   the EventsMetadata. If not set, the EventsMetadata object will look for a SERVICE_VARIANT setting (usually only
    #   set for lms and cms). The full source will be set to openedx/<EVENTS_SERVICE_NAME or SERVICE_VARIANT>/web.
    #   If neither variable is set, the source will be "SERVICE_NAME_UNSET"
    return getattr(settings, "EVENTS_SERVICE_NAME", None) or getattr(settings, "SERVICE_VARIANT", None)


def _get_source():
    """
    Get the source for an event.
    """
    service_name = get_service_name()
    if service_name:
        return "openedx/{service}/web".format(service=service_name)
    else:
        return "SERVICE_NAME_UNSET"


@attr.s(frozen=True)
class EventsMetadata:
    """
    Attributes defined for Open edX Events metadata object.

    The attributes defined in this class are a subset of the
    OEP-41: Asynchronous Server Event Message Format.

    Arguments:
        id (UUID): event identifier.
        event_type (str): name of the event.
        minorversion (int): (optional) version of the event type. Defaults to 0.
        source (str): logical source of an event.
        sourcehost (str): physical source of the event.
        time (datetime): (optional) timestamp when the event was sent with
            UTC timezone. Defaults to current time in UTC. See OEP-41 for
            details.
        sourcelib (tuple of ints): Open edX Events library version. A tuple was
            selected so that version comparisons don't have to worry about
            lexical ordering of strings (e.g. '0.9.0' vs. '0.10.0').
    """

    event_type = attr.ib(type=str, validator=attr.validators.instance_of(str))
    id = attr.ib(
        type=UUID, default=None,
        converter=attr.converters.default_if_none(attr.Factory(lambda: uuid1())),  # pylint: disable=unnecessary-lambda
        validator=attr.validators.instance_of(UUID),
    )
    minorversion = attr.ib(
        type=int, default=None,
        converter=attr.converters.default_if_none(0), validator=attr.validators.instance_of(int)
    )
    source = attr.ib(
        type=str, default=None,
        converter=attr.converters.default_if_none(attr.Factory(_get_source)),
        validator=attr.validators.instance_of(str),
    )
    sourcehost = attr.ib(
        type=str, default=None,
        converter=attr.converters.default_if_none(
            attr.Factory(lambda: socket.gethostname())  # pylint: disable=unnecessary-lambda
        ),
        validator=attr.validators.instance_of(str),
    )
    time = attr.ib(
        type=datetime, default=None,
        converter=attr.converters.default_if_none(attr.Factory(lambda: datetime.now(timezone.utc))),
        validator=[attr.validators.instance_of(datetime), _ensure_utc_time],
    )
    sourcelib = attr.ib(
        type=tuple, default=None,
        converter=attr.converters.default_if_none(
            attr.Factory(lambda: tuple(map(int, openedx_events.__version__.split("."))))
        ),
        validator=attr.validators.instance_of(tuple),
    )

    def to_json_data(self):
        """
        Create a json-compatible dictionary of the instance.
        """
        def value_serializer(inst, field, value):  # pylint: disable="unused-argument"
            if isinstance(value, UUID):
                return str(value)
            elif isinstance(value, datetime):
                return value.isoformat()
            else:
                return value
        return attrs.asdict(self, value_serializer=value_serializer)

    def to_json(self):
        """
        Serialize instance to json string.
        """
        return json.dumps(self.to_json_data())

    @classmethod
    def from_json(cls, json_string):
        """
        Create an instance from a json string.

        Arguments:
            json_string (str): A json representation of an EventsMetadata object, created with as_json_string
        Returns:
            An EventsMetadata object
        """
        as_json = json.loads(json_string)
        time = datetime.fromisoformat(as_json['time'])
        sourcelib = tuple(as_json['sourcelib'])
        return cls(event_type=as_json['event_type'], id=UUID(as_json['id']), source=as_json['source'],
                   sourcehost=as_json['sourcehost'], time=time, sourcelib=sourcelib)
