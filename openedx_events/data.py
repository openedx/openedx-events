"""
Data attributes for events within the architecture subdomain `learning`.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.
"""
from datetime import datetime
from uuid import UUID

import attr


@attr.s(frozen=True)
class EventsMetadata:
    """
    Attributes defined for events metadata object.
    """

    id = attr.ib(type=UUID)
    event_type = attr.ib(type=str)
    minorversion = attr.ib(type=int)
    time = attr.ib(type=datetime)
    source = attr.ib(type=str)
    sourcehost = attr.ib(type=str)
    specversion = attr.ib(type=str)
    sourcelib = attr.ib(type=str)
