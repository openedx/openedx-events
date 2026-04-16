"""
Data attributes for events within the architecture subdomain `learning`.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.
"""

import json
import socket
from datetime import datetime, timezone
from typing import Any, Self
from uuid import UUID, uuid1

import attrs
from django.conf import settings

import openedx_events


def _default_id(value: UUID | None) -> UUID:
    """
    Return value if set, otherwise generate a new UUID1.
    """
    return value if value is not None else uuid1()


def _default_minorversion(value: int | None) -> int:
    """
    Return value if set, otherwise default to 0.
    """
    return value if value is not None else 0


def _default_source(value: str | None) -> str:
    """
    Return value if set, otherwise derive source from service name.
    """
    return value if value is not None else _get_source()


def _default_sourcehost(value: str | None) -> str:
    """
    Return value if set, otherwise use the current hostname.
    """
    return value if value is not None else socket.gethostname()


def _default_time(value: datetime | None) -> datetime:
    """
    Return value if set, otherwise use the current UTC time.
    """
    return value if value is not None else datetime.now(timezone.utc)


def _default_sourcelib(value: tuple[int, ...] | None) -> tuple[int, ...]:
    """
    Return value if set, otherwise derive from the openedx_events version string.
    """
    return (
        value
        if value is not None
        else tuple(map(int, openedx_events.__version__.split(".")))
    )


def _ensure_utc_time(
    _: Any, attribute: "attrs.Attribute[Any]", value: datetime
) -> None:
    """
    Ensure the value is a UTC datetime.

    Note: Meant to be used along-side an instance_of attr validator.
    """
    if value.tzinfo and value.tzinfo == timezone.utc:
        return
    raise ValueError(f"'{attribute.name}' must have timezone.utc")


def get_service_name() -> str | None:
    """
    Get the service name of the producing/consuming service of an event (or None if not set).

    Uses EVENTS_SERVICE_NAME setting if present, otherwise looks for SERVICE_VARIANT.
    """
    # .. setting_name: EVENTS_SERVICE_NAME
    # .. setting_default: None
    # .. setting_description: Identifier for the producing/consuming service of an event. For example, "cms" or
    #   "course-discovery." Used, among other places, to determine the source header of the event.
    return getattr(settings, "EVENTS_SERVICE_NAME", None) or getattr(
        settings, "SERVICE_VARIANT", None
    )


def _get_source() -> str:
    """
    Get the source for an event using the service name.

    If the service name is set, the full source will be set to openedx/<service_name>/web or
    openedx/SERVICE_NAME_UNSET/web if service name is None.
    """
    return "openedx/{service}/web".format(
        service=(get_service_name() or "SERVICE_NAME_UNSET")
    )


@attrs.define(frozen=True)
class EventsMetadata:
    """
    Attributes defined for Open edX Events metadata object.

    The attributes defined in this class are a subset of the
    OEP-41: Asynchronous Server Event Message Format.

    Attributes:
        - id (UUID): event identifier.
        - event_type (str): name of the event.
        - minorversion (int): (optional) version of the event type. Defaults to 0.
        - source (str): logical source of an event.
        - sourcehost (str): physical source of the event.
        - time (datetime): (optional) timestamp when the event was sent with UTC timezone.
          Defaults to current time in UTC. See OEP-41 fordetails.
        - sourcelib (tuple of ints): Open edX Events library version. A tuple was
          selected so that version comparisons don't have to worry about lexical ordering of
          strings (e.g. '0.9.0' vs. '0.10.0').
    """

    event_type: str = attrs.field(validator=attrs.validators.instance_of(str))
    id: UUID = attrs.field(
        default=None,
        converter=_default_id,
        validator=attrs.validators.instance_of(UUID),
    )
    minorversion: int = attrs.field(
        default=None,
        converter=_default_minorversion,
        validator=attrs.validators.instance_of(int),
    )
    source: str = attrs.field(
        default=None,
        converter=_default_source,
        validator=attrs.validators.instance_of(str),
    )
    sourcehost: str = attrs.field(
        default=None,
        converter=_default_sourcehost,
        validator=attrs.validators.instance_of(str),
    )
    time: datetime = attrs.field(
        default=None,
        converter=_default_time,
        validator=[attrs.validators.instance_of(datetime), _ensure_utc_time],
    )
    sourcelib: tuple[int, ...] = attrs.field(
        default=None,
        converter=_default_sourcelib,
        validator=attrs.validators.instance_of(tuple),
    )

    def to_json_data(self) -> dict[str, Any]:
        """
        Create a json-compatible dictionary of the instance.
        """

        def value_serializer(  # pylint: disable=unused-argument
            inst: type, field: "attrs.Attribute[Any]", value: Any
        ) -> Any:
            if isinstance(value, UUID):
                return str(value)
            elif isinstance(value, datetime):
                return value.isoformat()
            else:
                return value

        return attrs.asdict(self, value_serializer=value_serializer)

    def to_json(self) -> str:
        """
        Serialize instance to json string.
        """
        return json.dumps(self.to_json_data())

    @classmethod
    def from_json(cls, json_string: str) -> Self:
        """
        Create an instance from a json string.

        Arguments:
            json_string (str): A json representation of an EventsMetadata object, created with as_json_string
        Returns:
            An EventsMetadata object
        """
        as_json = json.loads(json_string)
        time = datetime.fromisoformat(as_json["time"])
        sourcelib = tuple(as_json["sourcelib"])
        return cls(
            event_type=as_json["event_type"],
            id=UUID(as_json["id"]),
            source=as_json["source"],
            sourcehost=as_json["sourcehost"],
            time=time,
            sourcelib=sourcelib,
        )
