"""
openedx_events Django application initialization.
"""

from django.apps import AppConfig
from django.conf import settings

from openedx_events.event_bus import get_producer
from openedx_events.exceptions import ProducerConfigurationError
from openedx_events.tooling import OpenEdxPublicSignal, load_all_signals


def general_signal_handler(sender, signal, **kwargs):  # pylint: disable=unused-argument
    """
    Signal handler for publishing events to configured event bus.
    """
    configurations = getattr(settings, "EVENT_BUS_PRODUCER_CONFIG", {}).get(signal.event_type, {})
    event_data = {key: kwargs.get(key) for key in signal.init_data}

    for topic in configurations.keys():
        if configurations[topic]["enabled"]:
            get_producer().send(
                signal=signal,
                topic=topic,
                event_key_field=configurations[topic]["event_key_field"],
                event_data=event_data,
                event_metadata=kwargs["metadata"],
            )


class OpenedxEventsConfig(AppConfig):
    """
    Configuration for the openedx_events Django application.
    """

    name = "openedx_events"

    def _get_validated_signal_config(self, event_type, configuration):
        """
        Validate signal configuration format.

        Example expected signal configuration:
        {
            "topic_a": { "event_key_field": "my.key.field", "enabled": True },
            "topic_b": { "event_key_field": "my.key.field", "enabled": False }
        }

        Raises:
            ProducerConfigurationError: If configuration is not valid.
        """
        if not isinstance(configuration, dict) and not isinstance(configuration, dict):
            raise ProducerConfigurationError(
                event_type=event_type,
                message="Configuration for event_types should be a dict"
            )
        try:
            signal = OpenEdxPublicSignal.get_signal_by_type(event_type)
        except KeyError as exc:
            raise ProducerConfigurationError(message=f"No OpenEdxPublicSignal of type: '{event_type}'.") from exc
        for _, topic_configuration in configuration.items():
            print(f"{topic_configuration=}")
            if not isinstance(topic_configuration, dict):
                raise ProducerConfigurationError(
                    event_type=event_type,
                    message="One of the configuration objects is not a dictionary"
                )
            expected_keys = {"event_key_field": str, "enabled": bool}
            for expected_key, expected_type in expected_keys.items():
                if expected_key not in topic_configuration.keys():
                    raise ProducerConfigurationError(
                        event_type=event_type,
                        message=f"One of the configuration object is missing '{expected_key}' key."
                    )
                if not isinstance(topic_configuration[expected_key], expected_type):
                    raise ProducerConfigurationError(
                        event_type=event_type,
                        message=(f"Expected type: {expected_type} for '{expected_key}', "
                                    f"found: {type(topic_configuration[expected_key])}")
                    )
        return signal

    def ready(self):
        """
        Read `EVENT_BUS_PRODUCER_CONFIG` setting and connects appropriate handlers to the events based on it.

        Example expected configuration:
        {
            "org.openedx.content_authoring.xblock.deleted.v1" : {
                "topic_a": { "event_key_field": "xblock_info.usage_key", "enabled": True },
                "topic_b": { "event_key_field": "xblock_info.usage_key", "enabled": False }
            },
            "org.openedx.content_authoring.course.catalog_info.changed.v1" : {
                "topic_c": {"event_key_field": "course_info.course_key", "enabled": True }
            }
        }

        Raises:
            ProducerConfigurationError: If `EVENT_BUS_PRODUCER_CONFIG` is not valid.
        """
        load_all_signals()
        signals_config = getattr(settings, "EVENT_BUS_PRODUCER_CONFIG", {})
        if not isinstance(signals_config, dict):
            raise ProducerConfigurationError(
                message=("Setting 'EVENT_BUS_PRODUCER_CONFIG' should be a dictionary with event_type as"
                         " key and list or tuple of config dictionaries as values")
            )
        for event_type, configurations in signals_config.items():
            signal = self._get_validated_signal_config(event_type, configurations)
            signal.connect(general_signal_handler)
        return super().ready()
