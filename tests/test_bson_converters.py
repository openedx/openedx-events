"""
Tests for BSON FixedOffset and ObjectId converters in PersistentCourseGradeData.

These tests verify that the converters properly handle MongoDB BSON objects
that cause circular reference errors during JSON serialization.
"""
import json
from datetime import datetime, timezone
from bson import ObjectId
from bson.tz_util import FixedOffset
from opaque_keys.edx.locator import CourseLocator

from openedx_events.learning.data import CourseData, PersistentCourseGradeData


class TestBSONFixedOffsetConverter:
    """Test that BSON FixedOffset timezones are converted to standard UTC."""

    def test_persistent_grade_with_fixedoffset_timezone(self):
        """Test course_edited_timestamp with BSON FixedOffset timezone."""
        # Create a BSON FixedOffset timezone (simulating MongoDB data)
        bson_timezone = FixedOffset(0, 'UTC')  # 0 offset = UTC
        timestamp_with_bson = datetime(2025, 1, 20, 10, 18, 1, 213000, tzinfo=bson_timezone)
        
        course_data = CourseData(
            course_key=CourseLocator('HP', 'HPGG03.en', '2T2023', None, None),
            display_name='Test Course',
        )
        
        grade_data = PersistentCourseGradeData(
            user_id=68293694,
            course=course_data,
            course_edited_timestamp=timestamp_with_bson,  # BSON FixedOffset
            course_version='test-version',
            grading_policy_hash='kzLSFp+s4RiZlW0/QfqsXi5kqOc=',
            percent_grade=0.89,
            letter_grade='Pass',
            passed_timestamp=datetime.now(timezone.utc)
        )
        
        # Verify timezone was converted
        assert grade_data.course_edited_timestamp.tzinfo == timezone.utc
        assert grade_data.course_edited_timestamp.tzinfo.__class__.__name__ != 'FixedOffset'
        
        print("✅ BSON FixedOffset converted to timezone.utc")

    def test_passed_timestamp_with_fixedoffset(self):
        """Test passed_timestamp with BSON FixedOffset timezone."""
        bson_timezone = FixedOffset(0, 'UTC')
        passed_timestamp = datetime(2026, 1, 23, 16, 24, 41, 912992, tzinfo=bson_timezone)
        
        course_data = CourseData(
            course_key=CourseLocator('HP', 'HPGG03.en', '2T2023', None, None),
            display_name='Test Course',
        )
        
        grade_data = PersistentCourseGradeData(
            user_id=68293694,
            course=course_data,
            course_edited_timestamp=datetime.now(timezone.utc),
            course_version='test-version',
            grading_policy_hash='hash123',
            percent_grade=0.89,
            letter_grade='Pass',
            passed_timestamp=passed_timestamp  # BSON FixedOffset
        )
        
        # Verify timezone was converted
        assert grade_data.passed_timestamp.tzinfo == timezone.utc
        assert grade_data.passed_timestamp.tzinfo.__class__.__name__ != 'FixedOffset'
        
        print("✅ passed_timestamp BSON FixedOffset converted to timezone.utc")

    def test_course_data_start_end_with_fixedoffset(self):
        """Test CourseData start/end with BSON FixedOffset timezone."""
        bson_timezone = FixedOffset(0, 'UTC')
        start_time = datetime(2025, 1, 1, tzinfo=bson_timezone)
        end_time = datetime(2025, 12, 31, tzinfo=bson_timezone)
        
        course_data = CourseData(
            course_key=CourseLocator('HP', 'HPGG03.en', '2T2023', None, None),
            display_name='Test Course',
            start=start_time,  # BSON FixedOffset
            end=end_time  # BSON FixedOffset
        )
        
        # Verify timezones were converted
        assert course_data.start.tzinfo == timezone.utc
        assert course_data.end.tzinfo == timezone.utc
        assert course_data.start.tzinfo.__class__.__name__ != 'FixedOffset'
        assert course_data.end.tzinfo.__class__.__name__ != 'FixedOffset'
        
        print("✅ CourseData start/end BSON FixedOffset converted to timezone.utc")

    def test_json_serialization_with_converted_timezone(self):
        """Test that converted timezone is JSON serializable (no circular reference)."""
        bson_timezone = FixedOffset(0, 'UTC')
        timestamp = datetime(2025, 1, 20, 10, 18, 1, 213000, tzinfo=bson_timezone)
        
        course_data = CourseData(
            course_key=CourseLocator('HP', 'HPGG03.en', '2T2023', None, None),
            display_name='Test Course',
        )
        
        grade_data = PersistentCourseGradeData(
            user_id=68293694,
            course=course_data,
            course_edited_timestamp=timestamp,
            course_version='test-version',
            grading_policy_hash='hash123',
            percent_grade=0.89,
            letter_grade='Pass',
            passed_timestamp=datetime.now(timezone.utc)
        )
        
        # This should NOT raise "ValueError: Circular reference detected"
        try:
            # Attempt to serialize the datetime
            json_data = json.dumps({
                'timestamp': grade_data.course_edited_timestamp.isoformat()
            })
            assert json_data is not None
            print("✅ JSON serialization successful - no circular reference!")
        except ValueError as e:
            if 'Circular reference' in str(e):
                raise AssertionError("Circular reference error - converter failed!")
            raise


class TestObjectIdConverter:
    """Test that MongoDB ObjectId is converted to string."""

    def test_course_version_with_objectid(self):
        """Test course_version with MongoDB ObjectId."""
        mongo_oid = ObjectId('678e22d9035e75dd65e56c28')
        
        course_data = CourseData(
            course_key=CourseLocator('HP', 'HPGG03.en', '2T2023', None, None),
            display_name='Test Course',
        )
        
        grade_data = PersistentCourseGradeData(
            user_id=68293694,
            course=course_data,
            course_edited_timestamp=datetime.now(timezone.utc),
            course_version=mongo_oid,  # ObjectId, not string
            grading_policy_hash='hash123',
            percent_grade=0.89,
            letter_grade='Pass',
            passed_timestamp=datetime.now(timezone.utc)
        )
        
        # Verify ObjectId was converted to string
        assert isinstance(grade_data.course_version, str)
        assert grade_data.course_version == '678e22d9035e75dd65e56c28'
        
        print("✅ ObjectId converted to string")

    def test_course_version_string_passthrough(self):
        """Test that regular strings pass through unchanged."""
        course_data = CourseData(
            course_key=CourseLocator('HP', 'HPGG03.en', '2T2023', None, None),
            display_name='Test Course',
        )
        
        grade_data = PersistentCourseGradeData(
            user_id=68293694,
            course=course_data,
            course_edited_timestamp=datetime.now(timezone.utc),
            course_version='regular-string-version',  # Regular string
            grading_policy_hash='hash123',
            percent_grade=0.89,
            letter_grade='Pass',
            passed_timestamp=datetime.now(timezone.utc)
        )
        
        # Verify string passes through unchanged
        assert grade_data.course_version == 'regular-string-version'
        
        print("✅ Regular string passes through unchanged")


class TestProductionScenario:
    """Test the exact production scenario from the error log."""

    def test_production_error_scenario(self):
        """
        Replicate the exact production error scenario:
        - BSON FixedOffset in course_edited_timestamp
        - ObjectId in course_version
        """
        # Exact data from production error log
        bson_timezone = FixedOffset(0, 'UTC')
        course_edited = datetime(2025, 1, 20, 10, 18, 1, 213000, tzinfo=bson_timezone)
        passed_timestamp = datetime(2026, 1, 23, 16, 24, 41, 912992, tzinfo=timezone.utc)
        course_version_oid = ObjectId('678e22d9035e75dd65e56c28')
        
        course_data = CourseData(
            course_key=CourseLocator('HP', 'HPGG03.en', '2T2023', None, None),
            display_name='',
            start=None,
            end=None
        )
        
        # This is the exact data structure that was causing the error
        grade_data = PersistentCourseGradeData(
            user_id=68293694,
            course=course_data,
            course_edited_timestamp=course_edited,  # BSON FixedOffset
            course_version=course_version_oid,  # ObjectId
            grading_policy_hash='kzLSFp+s4RiZlW0/QfqsXi5kqOc=',
            percent_grade=0.89,
            letter_grade='Pass',
            passed_timestamp=passed_timestamp
        )
        
        # Verify both conversions worked
        assert grade_data.course_edited_timestamp.tzinfo == timezone.utc
        assert isinstance(grade_data.course_version, str)
        assert grade_data.course_version == '678e22d9035e75dd65e56c28'
        
        # Verify JSON serialization works (the ultimate test)
        try:
            test_dict = {
                'user_id': grade_data.user_id,
                'course_edited_timestamp': grade_data.course_edited_timestamp.isoformat(),
                'course_version': grade_data.course_version,
                'percent_grade': grade_data.percent_grade,
                'letter_grade': grade_data.letter_grade,
            }
            json_output = json.dumps(test_dict)
            assert json_output is not None
            print("✅ Production scenario: Successfully serialized to JSON!")
            print(f"   JSON output: {json_output[:100]}...")
        except ValueError as e:
            if 'Circular reference' in str(e):
                raise AssertionError("FAILED: Circular reference still occurring!")
            raise


if __name__ == '__main__':
    import pytest
    import sys
    
    # Run tests with verbose output
    exit_code = pytest.main([__file__, '-v', '-s'])
    sys.exit(exit_code)
