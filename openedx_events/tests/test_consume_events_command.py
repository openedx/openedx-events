"""
Tests for consume_events command.
"""
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from openedx_events.management.commands.consume_events import Command


class TestCommand(TestCase):
    """
    Tests for the consume_events management command
    """

    @patch('openedx_events.tooling.OpenEdxPublicSignal.get_signal_by_type', return_value="test-signal")
    @patch('openedx_events.management.commands.consume_events.make_single_consumer', autospec=True)
    def test_consumer_call_with_only_required_args(self, mock_make_consumer, _):
        call_command(Command(), topic=['test'], group_id=['test'], signal=['test-signal'])
        mock_make_consumer.assert_called_once_with(topic='test', group_id='test', signal='test-signal')

    @patch('openedx_events.tooling.OpenEdxPublicSignal.get_signal_by_type', return_value="test-signal")
    @patch('openedx_events.management.commands.consume_events.make_single_consumer', autospec=True)
    def test_consumer_call_with_extra_args(self, mock_make_consumer, _):
        call_command(
            Command(),
            topic=['test'],
            group_id=['test'],
            signal=['test-signal'],
            extra='{"check_backlog":true}'
        )
        mock_make_consumer.assert_called_once_with(
            topic='test',
            group_id='test',
            signal='test-signal',
            check_backlog=True
        )

    @patch('openedx_events.management.commands.consume_events.logger', autospec=True)
    @patch('openedx_events.management.commands.consume_events.make_single_consumer', autospec=True)
    def test_consumer_call_with_incorrect_json_string(self, mock_make_consumer, mock_logger):
        call_command(
            Command(),
            topic=['test'],
            group_id=['test'],
            signal=['test-signal'],
            extra="{'check_backlog':true}"
        )
        mock_logger.exception.assert_called_once_with("Error consuming events")
        mock_make_consumer.assert_not_called()
