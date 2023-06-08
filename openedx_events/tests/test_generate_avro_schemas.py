"""Tests for generate_avro_schemas."""
import os
from importlib import import_module
from unittest.mock import call, mock_open, patch

from django.core.management import call_command
from django.test import TestCase

from openedx_events.event_bus.avro.tests.test_utilities import create_simple_signal
from openedx_events.management.commands.generate_avro_schemas import Command
from openedx_events.tests.utils import FreezeSignalCacheMixin
from openedx_events.tooling import KNOWN_UNSERIALIZABLE_SIGNALS, OpenEdxPublicSignal, load_all_signals


class TestGenerateAvroCommand(FreezeSignalCacheMixin, TestCase):
    """
    Tests for generate_avro_schemas management command.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.root_path = import_module('openedx_events').__path__[0]
        cls.folder_path = f"{cls.root_path}/event_bus/avro/tests/schemas"

    # assume the schema folder already exists but has no files so we're not overwriting anything
    @patch('os.path.exists', lambda path: path == TestGenerateAvroCommand.folder_path)
    def test_generate_multiple_specified_schemas(self):
        signal_a = create_simple_signal({'key': str})
        signal_b = create_simple_signal({'key': str}, event_type='simple.signal.B')
        with patch("builtins.open", mock_open()) as mock_file:
            call_command(Command(), signal_a.event_type, signal_b.event_type)
            # make sure we created files with the correct name
            mock_file.assert_has_calls([
                    call(f"{TestGenerateAvroCommand.folder_path}/simple+signal_schema.avsc", "w"),
                    call(f"{TestGenerateAvroCommand.folder_path}/simple+signal+B_schema.avsc", "w"),
                ],
                # need any_order=True because opening a file involves a bunch of other secret calls
                any_order=True)
            handle = mock_file()
            # make sure we wrote the schemas. Exact JSON determined from testing
            assert handle.write.mock_calls == [
                call('{\n  "name": "CloudEvent",\n  "type": "record",\n'
                     '  "doc": "Avro Event Format for CloudEvents created with openedx_events/schema",'
                     '\n  "fields": [\n    {\n      "name": "key",\n      "type": "string"\n    }\n  ],\n  "namespace":'
                     ' "simple.signal"\n}'),
                call('{\n  "name": "CloudEvent",\n  "type": "record",\n'
                     '  "doc": "Avro Event Format for CloudEvents created with openedx_events/schema",'
                     '\n  "fields": [\n    {\n      "name": "key",\n      "type": "string"\n    }\n  ],\n  "namespace":'
                     ' "simple.signal.B"\n}')
            ]

    # pretend that all files in the schema folder have already been created
    @patch('os.path.exists', lambda path: TestGenerateAvroCommand.folder_path in path)
    def test_command_warns_if_schema_exists(self):
        signal_a = create_simple_signal({'key': str})
        with patch("builtins.open", mock_open()) as mock_file:
            # test we skip if the user doesn't want to continue
            with patch("builtins.input", return_value='n'):
                call_command(Command(), signal_a.event_type)
                mock_file.assert_not_called()
            # check we continue if the user wants to continue
            with patch("builtins.input", return_value='Y'):
                call_command(Command(), signal_a.event_type)
                mock_file.assert_has_calls([
                    call(f"{TestGenerateAvroCommand.folder_path}/simple+signal_schema.avsc", "w"),
                ])

    @patch('os.path.exists', lambda path: path == TestGenerateAvroCommand.folder_path)
    def test_generate_all(self):
        load_all_signals()
        expected_files = [f"{TestGenerateAvroCommand.folder_path}/{signal.event_type.replace('.','+')}_schema.avsc"
                          for signal in OpenEdxPublicSignal.all_events() if signal.event_type
                          not in KNOWN_UNSERIALIZABLE_SIGNALS]
        with patch("builtins.open", mock_open()) as mock_file:
            call_command(Command(), all=True)
            mock_file.assert_has_calls([call(file, 'w') for file in expected_files], any_order=True)

    # mostly added to appease the coverage gods
    @patch('os.makedirs')
    def test_create_schema_dir_if_not_exists(self, mock_makedirs):
        signal = create_simple_signal({"key": str})
        old_exists = os.path.exists
        with patch('os.path.exists',
                   lambda path: False if path == TestGenerateAvroCommand.folder_path else old_exists(path)):
            with patch("builtins.open", mock_open()):
                call_command(Command(), signal.event_type)
        mock_makedirs.assert_called_once_with(TestGenerateAvroCommand.folder_path)
