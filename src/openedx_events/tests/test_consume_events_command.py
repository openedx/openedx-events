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
        """
        This methods checks the required args are correctly passed to consumer.

        Expected behavior:
            The required args are passed to consumer.
        """
        call_command(Command(), topic=['test'], group_id=['test'])
        mock_make_consumer.assert_called_once_with(topic='test', group_id='test')

    @patch('openedx_events.management.commands.consume_events.make_single_consumer', autospec=True)
    def test_consumer_call_with_extra_args(self, mock_make_consumer):
        """
        This methods checks the extra args are correctly parsed and passed to consumer.

        Expected behavior:
            The extra args are parsed and passed to consumer.
        """
        call_command(
            Command(),
            topic=['test'],
            group_id=['test'],
            extra='{"check_backlog":true}'
        )
        mock_make_consumer.assert_called_once_with(
            topic='test',
            group_id='test',
            check_backlog=True
        )

    @patch('openedx_events.management.commands.consume_events.logger', autospec=True)
    @patch('openedx_events.management.commands.consume_events.make_single_consumer', autospec=True)
    def test_consumer_call_with_incorrect_json_string(self, mock_make_consumer, mock_logger):
        """
        This methods checks that consumer is not called with incorrect args if extra args json is incorrectly formed.

        Expected behavior:
            The command logs and skips execution if extra args json is incorrectly formed.
        """
        call_command(
            Command(),
            topic=['test'],
            group_id=['test'],
            extra="{'check_backlog':true}"
        )
        mock_logger.exception.assert_called_once_with("Error consuming events")
        mock_make_consumer.assert_not_called()
