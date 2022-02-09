"""
Tests for AvroAttrsBridge.
"""
from datetime import datetime
from unittest import TestCase

import attr
from opaque_keys.edx.keys import CourseKey

from openedx_events.bridge.avro_attrs_bridge import AvroAttrsBridge
from openedx_events.bridge.avro_attrs_bridge_extensions import CourseKeyAvroAttrsBridgeExtension
from openedx_events.learning.data import CourseData, CourseEnrollmentData, UserData, UserPersonalData


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
            },
        )
        serialized_course_enrollment_data = bridge.serialize(
            self.course_enrollment_data
        )

        object_from_wire = bridge.deserialize(serialized_course_enrollment_data)
        assert self.course_enrollment_data == object_from_wire

    def test_schema_evolution_add_value(self):
        # Create object from old specification
        old_bridge = AvroAttrsBridge(
            CourseEnrollmentData,
            extensions={
                CourseKeyAvroAttrsBridgeExtension.cls: CourseKeyAvroAttrsBridgeExtension(),
            },
        )
        serialized_course_enrollment_data = old_bridge.serialize(
            self.course_enrollment_data
        )

        def inner_scope(self):
            @attr.s(frozen=True)
            class CourseEnrollmentData:  # pylint: disable=redefined-outer-name
                """
                Temp class create to test schema evolution.
                """

                user = attr.ib(type=UserData)
                course = attr.ib(type=CourseData)
                mode = attr.ib(type=str)
                is_active = attr.ib(type=bool)
                creation_date = attr.ib(type=datetime)
                is_active_2 = attr.ib(type=bool, default=False)
                created_by = attr.ib(type=UserData, default=None)

            new_bridge = AvroAttrsBridge(
                CourseEnrollmentData,
                extensions={
                    CourseKeyAvroAttrsBridgeExtension.cls: CourseKeyAvroAttrsBridgeExtension(),
                },
            )
            object_from_wire_as_dict = attr.asdict(
                new_bridge.deserialize(
                    serialized_course_enrollment_data, old_bridge.schema_dict
                )
            )

            original_object_as_dict = attr.asdict(self.course_enrollment_data)
            original_object_as_dict["is_active_2"] = False
            assert object_from_wire_as_dict == original_object_as_dict

        inner_scope(self)

    def test_schema_evolution_remove_value(self):
        # Create object from old specification
        old_bridge = AvroAttrsBridge(
            CourseEnrollmentData,
            extensions={
                CourseKeyAvroAttrsBridgeExtension.cls: CourseKeyAvroAttrsBridgeExtension(),
            },
        )
        serialized_course_enrollment_data = old_bridge.serialize(
            self.course_enrollment_data
        )

        def inner_scope(self):
            @attr.s(frozen=True)
            class CourseEnrollmentData:  # pylint: disable=redefined-outer-name
                """
                Temp class create to test schema evolution.
                """

                user = attr.ib(type=UserData)
                course = attr.ib(type=CourseData)
                mode = attr.ib(type=str)
                creation_date = attr.ib(type=datetime)
                created_by = attr.ib(type=UserData, default=None)

            new_bridge = AvroAttrsBridge(
                CourseEnrollmentData,
                extensions={
                    CourseKeyAvroAttrsBridgeExtension.cls: CourseKeyAvroAttrsBridgeExtension(),
                },
            )
            object_from_wire_as_dict = attr.asdict(
                new_bridge.deserialize(
                    serialized_course_enrollment_data, old_bridge.schema_dict
                )
            )

            original_object_as_dict = attr.asdict(self.course_enrollment_data)
            del original_object_as_dict["is_active"]
            assert object_from_wire_as_dict == original_object_as_dict

        inner_scope(self)

    def test_schema_evolution_add_complex_value(self):
        # Create object from old specification
        old_bridge = AvroAttrsBridge(
            CourseEnrollmentData,
            extensions={
                CourseKeyAvroAttrsBridgeExtension.cls: CourseKeyAvroAttrsBridgeExtension(),
            },
        )
        serialized_course_enrollment_data = old_bridge.serialize(
            self.course_enrollment_data
        )

        def inner_scope(self):

            user_personal_data = UserPersonalData(
                username="username", email="email", name="name"
            )
            user_data = UserData(id=1, is_active=True, pii=user_personal_data)

            @attr.s(frozen=True)
            class CourseEnrollmentData:  # pylint: disable=redefined-outer-name
                """
                Temp class create to test schema evolution.
                """

                user = attr.ib(type=UserData)
                course = attr.ib(type=CourseData)
                mode = attr.ib(type=str)
                is_active = attr.ib(type=bool)
                creation_date = attr.ib(type=datetime)
                created_by = attr.ib(type=UserData, default=None)
                user2 = attr.ib(type=UserData, default=user_data)

            new_bridge = AvroAttrsBridge(
                CourseEnrollmentData,
                extensions={
                    CourseKeyAvroAttrsBridgeExtension.cls: CourseKeyAvroAttrsBridgeExtension(),
                },
            )
            object_from_wire_as_dict = attr.asdict(
                new_bridge.deserialize(
                    serialized_course_enrollment_data, old_bridge.schema_dict
                )
            )

            original_object_as_dict = attr.asdict(self.course_enrollment_data)
            original_object_as_dict["user2"] = attr.asdict(user_data)
            assert object_from_wire_as_dict == original_object_as_dict

        inner_scope(self)

    def test_schema_evolution_add_complex_extension_value(self):
        # Create object from old specification
        old_bridge = AvroAttrsBridge(
            CourseEnrollmentData,
            extensions={
                CourseKeyAvroAttrsBridgeExtension.cls: CourseKeyAvroAttrsBridgeExtension(),
            },
        )
        serialized_course_enrollment_data = old_bridge.serialize(
            self.course_enrollment_data
        )

        def inner_scope(self):

            @attr.s(frozen=True)
            class CourseEnrollmentData:  # pylint: disable=redefined-outer-name
                """
                Temp class create to test schema evolution.
                """

                user = attr.ib(type=UserData)
                course = attr.ib(type=CourseData)
                mode = attr.ib(type=str)
                is_active = attr.ib(type=bool)
                creation_date = attr.ib(type=datetime)
                created_by = attr.ib(type=UserData, default=None)
                added_date = attr.ib(type=datetime, default=None)

            new_bridge = AvroAttrsBridge(
                CourseEnrollmentData,
                extensions={
                    CourseKeyAvroAttrsBridgeExtension.cls: CourseKeyAvroAttrsBridgeExtension(),
                },
            )
            object_from_wire_as_dict = attr.asdict(
                new_bridge.deserialize(
                    serialized_course_enrollment_data, old_bridge.schema_dict
                )
            )
            original_object_as_dict = attr.asdict(self.course_enrollment_data)
            original_object_as_dict["added_date"] = None
            assert object_from_wire_as_dict == original_object_as_dict

        inner_scope(self)

    def test_throw_exception_on_unextended_custom_type(self):
        with self.assertRaises(TypeError):
            # CourseEnrollmentData has CourseKey and datetime as custom types
            # This should raise TypeError cause no extensions are being passed to bridge
            AvroAttrsBridge(CourseEnrollmentData)


def test_object_evolution_add_value():
    @attr.s(auto_attribs=True)
    class TestData:
        sub_name: str
        course_id: str

    original_bridge = AvroAttrsBridge(TestData)

    record = TestData("sub_name", "course_id")
    serialized_record = original_bridge.serialize(record)

    @attr.s(auto_attribs=True)
    class TestData:  # pylint: disable=function-redefined
        sub_name: str
        course_id: str
        added_key: str = "default_value"

    new_bridge = AvroAttrsBridge(TestData)
    deserialized_obj = new_bridge.deserialize(
        serialized_record, original_bridge.schema_dict
    )
    assert deserialized_obj == TestData(
        sub_name="sub_name", course_id="course_id", added_key="default_value"
    )


def test_object_evolution_remove_value():
    @attr.s(auto_attribs=True)
    class TestData:
        sub_name: str
        course_id: str
        removed_key: str

    original_bridge = AvroAttrsBridge(TestData)

    record = TestData("sub_name", "course_id", "removed_value")
    serialized_record = original_bridge.serialize(record)

    @attr.s(auto_attribs=True)
    class TestData:  # pylint: disable=function-redefined
        sub_name: str
        course_id: str

    new_bridge = AvroAttrsBridge(TestData)
    deserialized_obj = new_bridge.deserialize(
        serialized_record, original_bridge.schema_dict
    )
    assert deserialized_obj == TestData(sub_name="sub_name", course_id="course_id")


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
    class TestData:  # pylint: disable=missing-class-docstring
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
