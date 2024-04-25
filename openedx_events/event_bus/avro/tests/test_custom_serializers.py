from unittest import TestCase

from ccx_keys.locator import CCXLocator

from openedx_events.event_bus.avro.custom_serializers import (
    CcxCourseLocatorAvroSerializer,
)


class TestCCXLocatorSerailizer(TestCase):
    def test_serialize(self):
        obj1 = CCXLocator(org="edx", course="DemoX", run="Demo_course", ccx="1")
        expected1 = "ccx-v1:edx+DemoX+Demo_course+ccx@1"
        result1 = CcxCourseLocatorAvroSerializer.serialize(obj1)
        self.assertEqual(result1, expected1)

    def test_deseialize(self):
        data1 = "ccx-v1:edx+DemoX+Demo_course+ccx@1"
        expected1 = CCXLocator(org="edx", course="DemoX", run="Demo_course", ccx="1")
        result1 = CcxCourseLocatorAvroSerializer.deserialize(data1)
        self.assertEqual(result1, expected1)
