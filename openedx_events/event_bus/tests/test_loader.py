"""
Tests for event bus implementation loader.
"""

import copy
import warnings
from contextlib import contextmanager
from unittest import TestCase

from django.test import override_settings

from openedx_events.data import EventsMetadata
from openedx_events.event_bus import _try_load, get_producer, make_single_consumer, merge_publisher_configs
from openedx_events.learning.signals import SESSION_LOGIN_COMPLETED


@contextmanager
def assert_warnings(warning_messages: list):
    with warnings.catch_warnings(record=True) as caught_warnings:
        warnings.simplefilter('always')
        yield
    assert [str(w.message) for w in caught_warnings] == warning_messages


class TestLoader(TestCase):

    # No, the "constructors" here don't make much sense, but I didn't
    # want to create a bunch of test classes/factory functions, so I'm
    # using built-in functions instead.

    def test_unconfigured(self):
        with assert_warnings(["Event Bus setting DOES_NOT_EXIST is missing; component will be inactive"]):
            loaded = _try_load(
                setting_name="DOES_NOT_EXIST", args=(1), kwargs={'2': 3},
                expected_class=dict, default={'def': 'ault'},
            )
        assert loaded == {'def': 'ault'}

    @override_settings(EB_LOAD_PATH='builtins.dict')
    def test_success(self):
        with assert_warnings([]):
            loaded = _try_load(
                setting_name="EB_LOAD_PATH", args=(), kwargs={'2': 3},
                expected_class=dict, default={'def': 'ault'},
            )
        assert loaded == {'2': 3}

    @override_settings(EB_LOAD_PATH='builtins.list')
    def test_wrong_type(self):
        with assert_warnings([
                "builtins.list from EB_LOAD_PATH returned unexpected type <class 'list'>; "
                "component will be inactive"
        ]):
            loaded = _try_load(
                setting_name="EB_LOAD_PATH", args=([1, 2, 3],), kwargs={},
                expected_class=dict, default={'def': 'ault'},
            )
        assert loaded == {'def': 'ault'}

    @override_settings(EB_LOAD_PATH='no_module_here.foo.nope')
    def test_missing_module(self):
        with assert_warnings([
                "Failed to load <class 'dict'> from setting EB_LOAD_PATH: "
                "ModuleNotFoundError(\"No module named 'no_module_here'\"); "
                "component will be inactive"
        ]):
            loaded = _try_load(
                setting_name="EB_LOAD_PATH", args=(1), kwargs={'2': 3},
                expected_class=dict, default={'def': 'ault'},
            )
        assert loaded == {'def': 'ault'}

    @override_settings(EB_LOAD_PATH='builtins.does_not_exist')
    def test_missing_attribute(self):
        with assert_warnings([
                "Failed to load <class 'dict'> from setting EB_LOAD_PATH: "
                "ImportError('Module \"builtins\" does not define a \"does_not_exist\" attribute/class'); "
                "component will be inactive"
        ]):
            loaded = _try_load(
                setting_name="EB_LOAD_PATH", args=(1), kwargs={'2': 3},
                expected_class=dict, default={'def': 'ault'},
            )
        assert loaded == {'def': 'ault'}

    @override_settings(EB_LOAD_PATH='builtins.dict')
    def test_bad_args_for_callable(self):
        with assert_warnings([
                "Failed to load <class 'dict'> from setting EB_LOAD_PATH: "
                "TypeError('type object argument after * must be an iterable, not int'); "
                "component will be inactive"
        ]):
            loaded = _try_load(
                setting_name="EB_LOAD_PATH", args=(1), kwargs={'2': 3},
                expected_class=dict, default={'def': 'ault'},
            )
        assert loaded == {'def': 'ault'}


class TestProducer(TestCase):

    @override_settings(EVENT_BUS_PRODUCER=None)
    def test_default_does_nothing(self):
        """
        Test that the default is of the right class but does nothing.
        """
        producer = get_producer()

        with assert_warnings([]):
            # Nothing thrown, no warnings.
            assert producer.send(
                signal=SESSION_LOGIN_COMPLETED, topic='user-logins',
                event_key_field='user.id', event_data={},
                event_metadata=EventsMetadata(event_type='eh')
            ) is None


class TestConsumer(TestCase):

    @override_settings(EVENT_BUS_CONSUMER=None)
    def test_default_does_nothing(self):
        """
        Test that the default is of the right class but does nothing.
        """
        consumer = make_single_consumer(topic="test", group_id="test", signal=SESSION_LOGIN_COMPLETED)

        with assert_warnings([]):
            # Nothing thrown, no warnings.
            assert consumer.consume_indefinitely() is None


class TestSettings(TestCase):
    def test_merge_configs(self):
        dict_a = {
            'event_type_0': {
                'topic_a': {'event_key_field': 'field', 'enabled': True},
                'topic_b': {'event_key_field': 'field', 'enabled': True}
            },
            'event_type_1': {
                'topic_c': {'event_key_field': 'field', 'enabled': True},
            }
        }
        # for ensuring we didn't change the original dict
        dict_a_copy = copy.deepcopy(dict_a)
        dict_b = {
            'event_type_0': {
                # disable an existing event/topic pairing
                'topic_a': {'event_key_field': 'field', 'enabled': False},
                # add a new topic to an existing topic
                'topic_d': {'event_key_field': 'field', 'enabled': True},
            },
            # add a new event_type
            'event_type_2': {
                'topic_e': {'event_key_field': 'field', 'enabled': True},
            }
        }
        dict_b_copy = copy.deepcopy(dict_b)
        result = merge_publisher_configs(dict_a, dict_b)
        self.assertDictEqual(result, {
            'event_type_0': {
                'topic_a': {'event_key_field': 'field', 'enabled': False},
                'topic_b': {'event_key_field': 'field', 'enabled': True},
                'topic_d': {'event_key_field': 'field', 'enabled': True},
            },
            'event_type_1': {
                'topic_c': {'event_key_field': 'field', 'enabled': True},
            },
            'event_type_2': {
                'topic_e': {'event_key_field': 'field', 'enabled': True},
            }
        })
        self.assertDictEqual(dict_a, dict_a_copy)
        self.assertDictEqual(dict_b, dict_b_copy)

    def test_merge_configs_with_empty(self):
        dict_a = {
            'event_type_0': {
                'topic_a': {'event_key_field': 'field', 'enabled': True},
                'topic_b': {'event_key_field': 'field', 'enabled': True}
            },
            'event_type_1': {
                'topic_c': {'event_key_field': 'field', 'enabled': True},
            }
        }
        dict_b = {}
        result = merge_publisher_configs(dict_a, dict_b)
        self.assertDictEqual(result, dict_a)
