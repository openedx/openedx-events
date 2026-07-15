"""
Data attributes for events within the architecture subdomain ``analytics``.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.
"""

from datetime import datetime

import attrs


@attrs.define(frozen=True)
class TrackingLogData:
    """
    Data related to tracking events.

    Attributes:
        name (str): event name
        timestamp (datetime): timestamp of the event
        data (str): json string representation of a dictionary with extra data (optional), e.g.,
           >>> {"course_id": "course-v1:edX+DemoX+Demo_Course"}
        context (dict): json string representation of a dictionary of context data
           defined in https://docs.openedx.org/en/latest/developers/references/internal_data_formats/index.html
    """

    name: str
    timestamp: datetime
    data: str
    context: str
