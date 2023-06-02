"""
Data attributes for events within the architecture subdomain ``analytics``.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.

The attributes for the events come from the CourseDetailView in the LMS, with some unused fields removed
(see deprecation proposal at https://github.com/openedx/public-engineering/issues/160)
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
        data (dict): dictionary of extra data (optional), e.g. {"course_id": "course-v1:edX+DemoX+Demo_Course"}
        context (dict): dictionary of context data, defined in https://edx.readthedocs.io/projects/devdata/en/latest/internal_data_formats/tracking_logs/common_fields.html
    """

    name = attr.ib(type=str)
    timestamp = attr.ib(type=datetime)
    data = attr.ib(type=dict, default={})
    context = attr.ib(type=dict, factory=dict)
