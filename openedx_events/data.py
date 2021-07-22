"""
Data attributes for events within the architecture subdomain `learning`.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.
"""
import socket
from datetime import datetime
from uuid import UUID, uuid1

import attr
from django.conf import settings

import openedx_events


@attr.s(frozen=True)
class EventsMetadata:
    """
    Attributes defined for Open edX Events metadata object.

    The attributes defined in this class are a subset of the
    OEP-41: Asynchronous Server Event Message Format.

    Arguments:
        id (UUID): event identifier.
        event_type (str): name of the event.
        minorversion (int): version of the event type.
        source (str): logical source of an event.
        sourcehost (str): physical source of the event.
        time (datetime): timestamp when the event was sent.
        sourcelib (str): Open edX Events library version.
    """

    id = attr.ib(
        type=UUID,
        init=False,
    )
    event_type = attr.ib(type=str)
    minorversion = attr.ib(
        type=int,
        converter=attr.converters.default_if_none(0),
    )
    source = attr.ib(
        type=str,
        init=False,
    )
    sourcehost = attr.ib(
        type=str,
        init=False,
    )
    time = attr.ib(
        type=datetime,
        init=False,
    )
    sourcelib = attr.ib(
        type=tuple,
        init=False,
    )

    def __attrs_post_init__(self):
        """
        Post-init hook that generates metadata for the Open edX Event.
        """
        # Have to use this to get around the fact that the class is frozen
        # (which we almost always want, but not while we're initializing it).
        # Taken from edX Learning Sequences data file.
        object.__setattr__(self, "id", uuid1())
        object.__setattr__(
            self,
            "source",
            "openedx/{service}/web".format(
                service=getattr(settings, "SERVICE_VARIANT", "")
            ),
        )
        object.__setattr__(self, "sourcehost", socket.gethostname())
        object.__setattr__(self, "time", datetime.utcnow())
        object.__setattr__(
            self, "sourcelib", tuple(map(int, openedx_events.__version__.split(".")))
        )
