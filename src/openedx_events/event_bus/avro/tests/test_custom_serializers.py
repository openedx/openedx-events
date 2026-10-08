"""Test custom servializers"""
from unittest import TestCase
from uuid import UUID, uuid4

from ccx_keys.locator import CCXLocator

from openedx_events.event_bus.avro.custom_serializers import CcxCourseLocatorAvroSerializer, UuidAvroSerializer


class TestCCXLocatorSerailizer(TestCase):
    """Test case for CCXLocator serializer."""

    def test_serialize(self):
        """
        Test case for serializing CCXLocator object.
        """

        obj1 = CCXLocator(org="edx", course="DemoX", run="Demo_course", ccx="1")
        expected1 = "ccx-v1:edx+DemoX+Demo_course+ccx@1"
        result1 = CcxCourseLocatorAvroSerializer.serialize(obj1)
        self.assertEqual(result1, expected1)

    def test_deserialize(self):
        """
        Test case for deserializing CCXLocator object.
        """

        data1 = "ccx-v1:edx+DemoX+Demo_course+ccx@1"
        expected1 = CCXLocator(org="edx", course="DemoX", run="Demo_course", ccx="1")
        result1 = CcxCourseLocatorAvroSerializer.deserialize(data1)
        self.assertEqual(result1, expected1)


class TestUuidAvroSerializer(TestCase):
    """
    Tests case for Avro UUID de-/serialization.
    """
    def test_serialize(self):
        """
        Test UUID Avro serialization.
        """
        some_uuid = uuid4()
        expected_result = str(some_uuid)
        actual_result = UuidAvroSerializer.serialize(some_uuid)
        self.assertEqual(actual_result, expected_result)

    def test_deserialize(self):
        """
        Test UUID Avro de-serialization.
        """
        uuid_str = str(uuid4())
        expected_result = UUID(uuid_str)
        actual_result = UuidAvroSerializer.deserialize(uuid_str)
        self.assertEqual(actual_result, expected_result)
