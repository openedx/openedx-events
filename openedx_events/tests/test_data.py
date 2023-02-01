"""
Tests for data.py.
"""
import attr
import pytest
from django.test import TestCase

from openedx_events.data import EventsMetadata
from openedx_events.tests.utils import load_all_signals
from openedx_events.tooling import OpenEdxPublicSignal


class EventsMetadataTestCache(TestCase):
    """
    Tests for EventsMetadata.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load_all_signals()

    def test_key_non_collision(self):
        """
        Check whether any events have a data key that collides with a metadata key.

        This is important because both the data dict and the metadata dict get
        splatted into the signal receiver, so we need to make sure none of the keys
        collide.
        """
        metadata_fields = set(f.name for f in attr.fields(EventsMetadata))
        for signal in OpenEdxPublicSignal.all_events():
            for signal_root_key in signal.init_data.keys():
                if signal_root_key in metadata_fields:
                    pytest.fail(
                        f"Signal {signal} has a root data key called {signal_root_key!r}, "
                        "but this collides with an EventMetadata field. This signal will "
                        "need to use a different key at the root of its data dictionary."
                    )
