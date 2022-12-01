"""
Classes and utility functions for the event bus.

This module includes the entry point for the producer.

API:

- ``get_producer`` returns an ``EventBusProducer`` singleton that should be used for sending all events
  to the Event Bus. The backing implementation is chosen via the Django setting ``EVENT_BUS_PRODUCER``.
  See for example the Kafka implementation's ``KafkaEventProducer``, with the ``create_producer`` function
  serving as the loader: https://github.com/openedx/event-bus-kafka/blob/main/edx_event_bus_kafka/internal/producer.py
"""

import warnings
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import NoReturn, Optional

from django.conf import settings
from django.dispatch import receiver
from django.test.signals import setting_changed
from django.utils.module_loading import import_string

from openedx_events.tooling import OpenEdxPublicSignal
from openedx_events.data import EventsMetadata


def _try_load(*, setting_name: str, expected_class: type, default):
    """
    Load an instance of ``expected_class`` as indicated by ``setting_name``.

    The setting points to a callable (function or class) that will fetch or create an
    instance of the expected class. If the configuration is missing or invalid,
    or the callable throws an exception or returns the wrong type, the default is
    returned instead.

    Arguments:
        setting_name: Name of a Django setting containing a dotted module path, indicating a callable
        expected_class: The callable must produce an instance of this class object (or a subclass)
        default: Object to return if any part of the lookup or loading fails
    """
    constructor_path = getattr(settings, setting_name, None)
    if constructor_path is None:
        warnings.warn(f"Event Bus setting {setting_name} is missing; component will be inactive")
        return default

    try:
        constructor = import_string(constructor_path)
        instance = constructor()
        if isinstance(instance, expected_class):
            return instance
        else:
            warnings.warn(
                f"{constructor_path} from {setting_name} returned unexpected type {type(instance)}; "
                "component will be inactive"
            )
            return default
    except BaseException as e:
        warnings.warn(
            f"Failed to load {expected_class} from setting {setting_name}: {e!r}; "
            "component will be inactive"
        )
        return default


class EventBusProducer(ABC):
    """
    Parent class for event bus producer implementations.
    """

    # TODO: Make event_metadata required (https://github.com/openedx/openedx-events/issues/153)
    @abstractmethod
    def send(
            self, *, signal: OpenEdxPublicSignal, topic: str, event_key_field: str, event_data: dict,
            event_metadata: EventsMetadata = None
    ) -> None:
        """
        Send a signal event to the event bus under the specified topic.

        Arguments:
            signal: The original OpenEdxPublicSignal the event was sent to
            topic: The event bus topic for the event (without any environmental prefix)
            event_key_field: Path to the event data field to use as the event key (period-delimited
              string naming the dictionary keys to descend)
            event_data: The event data (kwargs) sent to the signal
            event_metadata: (optional) The CloudEvent metadata
        """


class NoEventBusProducer(EventBusProducer):
    """
    Stub implementation to "load" when no implementation is properly configured.
    """

    def send(
            self, *, signal: OpenEdxPublicSignal, topic: str, event_key_field: str, event_data: dict,
            event_metadata: EventsMetadata = None,
    ) -> None:
        """Do nothing."""


# .. setting_name: EVENT_BUS_PRODUCER
# .. setting_default: None
# .. setting_description: String naming a callable (function or class) that can be called to create
#   or retrieve an instance of EventBusProducer when ``openedx_events.event_bus.get_producer`` is
#   called. The format of the string is a dotted path to an attribute in a module, e.g.
#   ``edx_event_bus_kafka.create_producer``. This producer will be managed as a singleton
#   by openedx_events. If setting is not supplied or the callable raises an exception or does not return
#   an instance of EventBusProducer, calls to the producer will be ignored with a warning at startup.

@lru_cache  # will just be one cache entry, in practice
def get_producer() -> EventBusProducer:
    """
    Create or retrieve the producer implementation, as configured.

    If misconfigured, returns a fake implementation that can be called but does nothing.
    """
    return _try_load(
        setting_name='EVENT_BUS_PRODUCER',
        expected_class=EventBusProducer, default=NoEventBusProducer(),
    )


@receiver(setting_changed)
def _reset_state(sender, **kwargs):  # pylint: disable=unused-argument
    """Reset caches when settings change during unit tests."""
    get_producer.cache_clear()
