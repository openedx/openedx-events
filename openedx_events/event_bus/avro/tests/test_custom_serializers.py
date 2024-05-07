from unittest import TestCase

from ccx_keys.locator import CCXLocator

from openedx_events.event_bus.avro.custom_serializers import (
    CcxCourseLocatorAvroSerializer,
)


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

    def test_deseialize(self):
        """
        Test case for deserializing CCXLocator object.
        """

        data1 = "ccx-v1:edx+DemoX+Demo_course+ccx@1"
        expected1 = CCXLocator(org="edx", course="DemoX", run="Demo_course", ccx="1")
        result1 = CcxCourseLocatorAvroSerializer.deserialize(data1)
        self.assertEqual(result1, expected1)
