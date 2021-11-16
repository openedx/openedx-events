#!/usr/bin/env python3

import attrs
from opaque_keys.edx.keys import CourseKey, UsageKey
from opaque_keys import InvalidKeyError

from openedx_events.avro_attrs_bridge import AvroAttrsBridge
from openedx_events.learning.data import CourseEnrollmentData, UserData, CourseData, CourseKey, UserPersonalData

def test_non_base_types():
    user_personal_data = UserPersonalData(username = 'username', email = 'email', name = 'name')
    user_data = UserData(id=1, is_active = True, pii = user_personal_data)
    # define Coursedata, which needs Coursekey, which needs opaque key
    course_id = "course-v1:edX+DemoX.1+2014"
    course_key = CourseKey.from_string(course_id)
    course_data = CourseData(course_key=course_key, display_name="display_name", )
    assert True


def test_base_types():
    @attr.s(auto_attribs=True)
    class SubTest:
        sub_name: str
        course_id: str

    @attr.s(auto_attribs=True)
    class Test:
        name: str
        course_id: str
        user_id: int
        more: SubTest

    bridge = AvroAttrsBridge(Test)

    # A test record that we can try to serialize to avro.
    record = Test("foo", "bar.course", 1, SubTest("a.sub.name", "a.nother.course"))
    serialized_record = bridge.serialize(record)

    # Try to de-serialize back to an attrs class.
    object_from_wire = bridge.deserialize(serialized_record)
    assert record == object_from_wire
