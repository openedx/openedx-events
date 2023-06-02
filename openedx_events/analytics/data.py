"""
Data attributes for events within the architecture subdomain ``analytics``.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.
"""

from datetime import datetime

import attr


@attr.s(frozen=True)
class TrackingLogData:
    """
    Data describing tracking log data.

    Arguments:
        name (str): course name
        timestamp (datetime): course start date
        data (str): json string representation of a dictionary with extra data (optional),
                    e.g. {"course_id": "course-v1:edX+DemoX+Demo_Course"}
        context (dict): json string representation of a dictionary of context data
            defined in https://edx.readthedocs.io/projects/devdata/en/latest/internal_data_formats/tracking_logs/
    """

    name = attr.ib(type=str)
    timestamp = attr.ib(type=datetime)
    data = attr.ib(type=str)
    context = attr.ib(type=str)
