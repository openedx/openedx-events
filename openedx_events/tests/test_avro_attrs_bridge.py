#!/usr/bin/env python3

import attr
from opaque_keys.edx.keys import CourseKey, UsageKey
from opaque_keys import InvalidKeyError

from datetime import datetime

from openedx_events.avro_attrs_bridge import AvroAttrsBridge, CourseKeyAvroAttrsBridgeExtension
from openedx_events.learning.data import (
    CourseEnrollmentData,
    UserData,
    CourseData,
    CourseKey,
    UserPersonalData,
)


# def test_non_base_types():
#     user_personal_data = UserPersonalData(
#         username="username", email="email", name="name"
#     )
#     user_data = UserData(id=1, is_active=True, pii=user_personal_data)
#     # define Coursedata, which needs Coursekey, which needs opaque key
#     course_id = "course-v1:edX+DemoX.1+2014"
#     course_key = CourseKey.from_string(course_id)
#     course_data = CourseData(
#         course_key=course_key,
#         display_name="display_name",
#     )
#     course_enrollment_data = CourseEnrollmentData(
#         user=user_data,
#         course=course_data,
#         mode="mode",
#         is_active=False,
#         creation_date=datetime.now(),
#         created_by=user_data,
#     )

#     breakpoint()

#     serialized_course_enrollment_data = attr.asdict(course_enrollment_data)
#     deserialized_course_enrollment_data = CourseEnrollmentData(
#         **serialized_course_enrollment_data
#     )
#     assert course_enrollment_data == deserialized_course_enrollment_data


def test_non_base_types_in_bridge():
    user_personal_data = UserPersonalData(
        username="username", email="email", name="name"
    )
    user_data = UserData(id=1, is_active=True, pii=user_personal_data)
    # define Coursedata, which needs Coursekey, which needs opaque key
    course_id = "course-v1:edX+DemoX.1+2014"
    course_key = CourseKey.from_string(course_id)
    course_data = CourseData(
        course_key=course_key,
        display_name="display_name",
    )
    course_enrollment_data = CourseEnrollmentData(
        user=user_data,
        course=course_data,
        mode="mode",
        is_active=False,
        creation_date=datetime.now(),
        created_by=user_data,
    )

    bridge = AvroAttrsBridge(CourseEnrollmentData, extensions=[CourseKeyAvroAttrsBridgeExtension()])
    serialized_course_enrollment_data = bridge.serialize(course_enrollment_data)

    object_from_wire = bridge.deserialize(serialized_course_enrollment_data)
    assert course_enrollment_data == object_from_wire


def test_base_types():
    @attr.s(auto_attribs=True)
    class SubTest:
        sub_name: str
        course_id: str

    @attr.s(auto_attribs=True)
    class UberSubTest:
        sub_name: str
        course_id: str

    @attr.s(auto_attribs=True)
    class Test:
        name: str
        course_id: str
        user_id: int
        sub_test: SubTest
        uber_sub_test: UberSubTest

    bridge = AvroAttrsBridge(Test)

    # A test record that we can try to serialize to avro.
    record = Test("foo", "bar.course", 1, SubTest("a.sub.name", "a.nother.course"), UberSubTest('b.uber.sub.name', 'b.uber.another.course'))
    serialized_record = bridge.serialize(record)

    # Try to de-serialize back to an attrs class.
    object_from_wire = bridge.deserialize(serialized_record)
    assert record == object_from_wire
