"""
Management command to generate and store Avro schemas for testing.
"""
import json
import logging
import os
from importlib import import_module

from django.core.management.base import BaseCommand

from openedx_events.event_bus.avro.serializer import AvroSignalSerializer
from openedx_events.tooling import KNOWN_UNSERIALIZABLE_SIGNALS, OpenEdxPublicSignal, load_all_signals

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Management command to save current Avro schemas for all signals for schema evolution testing.
    """

    help = """
    Generate and save the current Avro schemas of OpenEdxPublicSignals.

    Schemas will be saved in openedx_events/avro/tests/schemas. The folder will be created if it does not already exist.
    Should only be used for new signals. Even if a schema is changing, it is recommended you leave the original
    in place. Only overwrite the file for an exceptional case, like the schema still being under development.

    Example::

        # one signal
        python manage.py generate_avro_schemas org.openedx.learning.course.enrollment.changed.v1

        # multiple signals
        python manage.py generate_avro_schemas org.openedx.learning.course.enrollment.changed.v1 /
            org.openedx.learning.course.unenrollment.completed.v1

        # all signals
        python manage.py generate_avro_schemas --all

    """

    def add_arguments(self, parser):
        """
        Add arguments for either individual event types or all of them.
        """
        parser.add_argument(
            'types',
            nargs='*',
            type=str,
            help='Event types for which to write and save the schema, separated by a space'
        )

        parser.add_argument(
            '--all',
            action="store_true",
            help='Write schema for all event types'
        )

    def handle(self, *args, **options):
        """
        Create consumer based on django settings and consume events.
        """
        load_all_signals()
        if options['all']:
            signals = OpenEdxPublicSignal.all_events()
        else:
            signals = [OpenEdxPublicSignal.get_signal_by_type(event_type) for event_type in options['types']]

        for signal in signals:
            if signal.event_type in KNOWN_UNSERIALIZABLE_SIGNALS:
                logger.info(f"Known unserializable signal: {signal.event_type}. Skipping.")
                continue
            serializer = AvroSignalSerializer(signal)
            schema_dict = serializer.schema
            filename = f"{signal.event_type.replace('.', '+')}_schema.avsc"
            root_path = import_module('openedx_events').__path__[0]
            folder_path = f"{root_path}/event_bus/avro/tests/schemas"
            full_file_name = f"{folder_path}/{filename}"
            if os.path.exists(full_file_name):
                confirmation = input(f"Warning: overwriting schema for {signal.event_type}. It is recommended to leave"
                                     f" existing schemas unchanged. Are you sure you want to "
                                     f"continue [y/n]? ")
                if confirmation.lower().strip() != 'y':
                    logger.info(f"Skipping generating schema for {signal.event_type}")
                    continue
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            logger.info(f"Writing {full_file_name}")
            with open(full_file_name, 'w') as writes:
                writes.write(json.dumps(schema_dict, indent=2))
