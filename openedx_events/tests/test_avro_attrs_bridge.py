"""
Tests for AvroAttrsBridge.
"""
from unittest import TestCase
from datetime import datetime

import attr

from opaque_keys.edx.keys import CourseKey

from openedx_events.avro_attrs_bridge import AvroAttrsBridge
from openedx_events.avro_attrs_bridge_extensions import (
    CourseKeyAvroAttrsBridgeExtension,
    DatetimeAvroAttrsBridgeExtension,
)
from openedx_events.learning.data import (
    CourseEnrollmentData,
    UserData,
    CourseData,
    UserPersonalData,
)


class TestNoneBaseTypesInBridge(TestCase):
    """
    Tests to make sure AttrsAvroBridge handles custom types correctly.
    """
    def setUp(self):
        super().setUp()
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
            start=datetime.now(),
            end=datetime.now(),
        )
        self.course_enrollment_data = CourseEnrollmentData(
            user=user_data,
            course=course_data,
            mode="mode",
            is_active=False,
            creation_date=datetime.now(),
            created_by=user_data,
        )

    def test_non_base_types_in_bridge(self):
        """
        Test to makes ure AvroattrsBridge works correctly with non-attr classes.

        Specifically, testing to make sure the extension classes work as intended.
        """
        bridge = AvroAttrsBridge(
            CourseEnrollmentData,
            extensions={
                CourseKeyAvroAttrsBridgeExtension.cls: CourseKeyAvroAttrsBridgeExtension(),
                DatetimeAvroAttrsBridgeExtension.cls: DatetimeAvroAttrsBridgeExtension(),
            },
        )
        serialized_course_enrollment_data = bridge.serialize(
            self.course_enrollment_data
        )

        object_from_wire = bridge.deserialize(serialized_course_enrollment_data)
        assert self.course_enrollment_data == object_from_wire

    def test_throw_exception_on_unextended_custom_type(self):
        with self.assertRaises(TypeError):
            # CourseEnrollmentData has CourseKey and datetime as custom types
            # This should raise TypeError cause no extensions are being passed to bridge
            AvroAttrsBridge(CourseEnrollmentData)

def test_base_types():
    @attr.s(auto_attribs=True)
    class SubTestData:
        sub_name: str
        course_id: str

    @attr.s(auto_attribs=True)
    class SubTestData2:
        sub_name: str
        course_id: str

    @attr.s(auto_attribs=True)
    class TestData:                   # pylint: disable=missing-class-docstring
        name: str
        course_id: str
        user_id: int
        sub_test: SubTestData
        uber_sub_test: SubTestData2

    bridge = AvroAttrsBridge(TestData)

    # A test record that we can try to serialize to avro.
    record = TestData(
        "foo",
        "bar.course",
        1,
        SubTestData("a.sub.name", "a.nother.course"),
        SubTestData2("b.uber.sub.name", "b.uber.another.course"),
    )
    serialized_record = bridge.serialize(record)

    # Try to de-serialize back to an attrs class.
    object_from_wire = bridge.deserialize(serialized_record)
    assert record == object_from_wire
