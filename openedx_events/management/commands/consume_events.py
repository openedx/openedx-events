"""
Makes ``consume_events`` management command available.
"""
import json
import logging
from django.core.management.base import BaseCommand
from openedx_events.event_bus import make_single_consumer

from openedx_events.tooling import OpenEdxPublicSignal, load_all_signals

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Management command for consumer workers in the event bus.
    """
    help = """
    Consume messages of specified signal type from a topic and send their data to that signal.

    Example::

        python3 manage.py consume_events -t user-login -g user-activity-service \
            -s org.openedx.learning.auth.session.login.completed.v1
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '-t', '--topic',
            nargs=1,
            required=True,
            help='Topic to consume (without environment prefix)'
        )

        parser.add_argument(
            '-g', '--group_id',
            nargs=1,
            required=True,
            help='Consumer group id'
        )
        parser.add_argument(
            '-s', '--signal',
            nargs=1,
            required=True,
            help='Type of signal to emit from consumed messages.'
        )
        parser.add_argument(
            '--extra',
            nargs='?',
            type=str,
            required=False,
            help='JSON string to pass additional arguments to the consumer.'
        )

    def handle(self, *args, **options):
        try:
            extra = json.loads(options.get('extra') or '{}')
            load_all_signals()
            signal = OpenEdxPublicSignal.get_signal_by_type(options['signal'][0])
            event_consumer = make_single_consumer(
                topic=options['topic'][0],
                group_id=options['group_id'][0],
                signal=signal,
                **extra,
            )
            event_consumer.consume_indefinitely()
        except Exception:  # pylint: disable=broad-except
            logger.exception("Error consuming events")
