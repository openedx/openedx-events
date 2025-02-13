Add Event Bus Support to an Open edX Event
############################################

Before sending an event across services, you need to ensure that the event is compatible with the Open edX Event Bus. This involves ensuring that the event, with its corresponding payload, can be emitted by a service through the event bus and that other services can consume it. This guide will walk you through the process of adding event bus support to an Open edX event.

For more details on how the :term:`Event Payload` is structured, refer to the :doc:`../decisions/0003-events-payload` decision record.

.. note::
    This guide assumes that you have already created an Open edX event. If you have not, refer to the :doc:`../how-tos/create-a-new-event` how-to guide.

Step 1: Does my Event Need Event Bus Support?
===============================================

By default, Open edX Events should be compatible with the Open edX Event Bus. However, there are cases when support might not be available or needed for a particular event. Here are some scenarios where you might not need to add event bus support:

- The event is only used within the same application process and cannot be scoped to other services.
- The :term:`Event Payload` contains data types that are not supported by the event bus, e.g., lists of dictionaries or data attrs classes with unsupported data types when it is not possible to refactor the :term:`Event Payload` to use supported data types.

When adding support is not possible, do the following:

- Add it to the ``KNOWN_UNSERIALIZABLE_SIGNALS`` list in the ``openedx_events/tooling.py`` file so the event bus ignores it.
- Add a ``warning`` in the event’s docstring to inform developers why the event is incompatible with the event bus.

If you don't add the event to the ``KNOWN_UNSERIALIZABLE_SIGNALS`` list, the CI/CD pipeline will fail because the missing Avro schema could not be generated for the :term:`Event Payload`. If you don't add a warning in the event's docstring, developers might try to send the event across services and encounter issues.

.. warning:: Maintainers will check event bus compatibility for new events. To avoid issues, make sure to consider compatibility during the design phase. Contact maintainers if you are unsure about the compatibility of an event.

Step 2: Define the Event Payload
==================================

An Open edX Event is compatible with the event bus when its payload can be serialized, sent, and deserialized by other services. The payload, structured as `attrs data classes`_, must align with the event bus schema format, which in this case is the :term:`Avro Schema`. This schema is used to serialize and deserialize the :term:`Event Payload` when sending it across services.

This ensures the event can be sent by the producer and then re-emitted by the same instance of `OpenEdxPublicSignal`_ on the consumer side, guaranteeing that the data sent and received is identical. Serializing this way should prevent data inconsistencies between services, e.g., timezone issues and precision loss. For more information on the event bus schema format, refer to the :doc:`../decisions/0004-external-event-bus-and-django-signal-events` and :doc:`../decisions/0005-external-event-schema-format` decision records.

The data types used in the attrs classes that the current Open edX Event Bus with the chosen schema are:

Primitive Data Types
-----------------------

- Boolean
- Integer
- Float
- String
- Bytes

Complex Data Types
--------------------

- Type-annotated Lists (e.g., ``List[int]``, ``List[str]``)
- Attrs Classes (e.g., ``UserNonPersonalData``, ``UserPersonalData``, ``UserData``, ``CourseData``)
- Types with Custom Serializers (e.g., ``CourseKey``, ``datetime``)

Ensure that the :term:`Event Payload` is structured as `attrs data classes`_ and that the data types used in those classes align with the event bus schema format.

In the ``data.py`` files within each architectural subdomain, you can find examples of the :term:`Event Payload` structured as `attrs data classes`_ that align with the event bus schema format.

Step 3: Ensure Serialization and Deserialization
==================================================

Before sending the event across services, you need to ensure that the :term:`Event Payload` can be serialized and deserialized correctly. The event bus concrete implementations use the :term:`Avro Schema` to serialize and deserialize the :term:`Event Payload` as mentioned in the :doc:`../decisions/0005-external-event-schema-format` decision record. The concrete implementation of the event bus handles serialization and deserialization with the help of methods implemented by this library.

If you are interested in how the serialization and deserialization of the :term:`Event Payload` are handled by the event bus, you can refer to the concrete event bus implementation in the Open edX Event Bus repository. For example, here's how the Redis event bus handles `serialization`_ and `deserialization`_ when sending and receiving events.

If the :term:`Event Payload` contains types that are not supported by the event bus, you could implement custom serializers for these types. This ensures that the :term:`Event Payload` can be serialized and deserialized correctly when sent across services.

Here is an example of a custom serializer for the ``CourseKey`` type:

.. code-block:: python

    # event_bus/avro/custom_serializers.py
    class CourseKeyAvroSerializer(BaseCustomTypeAvroSerializer):
        """
        CustomTypeAvroSerializer for CourseKey class.
        """

        cls = CourseKey
        field_type = PYTHON_TYPE_TO_AVRO_MAPPING[str]

        @staticmethod
        def serialize(obj) -> str:
            """Serialize obj into string."""
            return str(obj)

        @staticmethod
        def deserialize(data: str):
            """Deserialize string into obj."""
            return CourseKey.from_string(data)


After implementing the serializer, add it to ``DEFAULT_CUSTOM_SERIALIZERS`` at the end of the ``event_bus/avro/custom_serializers.py`` file:

.. code-block:: python

    DEFAULT_CUSTOM_SERIALIZERS = [
        # Other custom serializers
        CourseKey: CourseKeyAvroSerializer,
    ]

Now, the :term:`Event Payload` can be serialized and deserialized correctly when sent across services.

.. warning::
    One of the known limitations of the current Open edX Event Bus is that it does not support dictionaries as data types. If the :term:`Event Payload` contains dictionaries, you may need to refactor the :term:`Event Payload` to use supported data types. When you know the structure of the dictionary, you can create an attrs class that represents the dictionary structure. If not, you can use a str type to represent the dictionary as a string and deserialize it on the consumer side using JSON deserialization.

Step 4: Generate the Avro Schema
====================================

As mentioned in the previous step, the serialization and deserialization of the :term:`Event Payload` are handled by the concrete event bus implementation with the help of methods implemented in this library. However, although openedx-events does not handle the serialization and deserialization of the :term:`Event Payload` directly, it ensures the payload of new events can be serialized and deserialized correctly by adding checks in the CI/CD pipeline for schema verification. To ensure tests pass, you need to generate an Avro test schema for your new event's :term:`Event Payload`:

1. Run the following command to generate the Avro schema for the :term:`Event Payload`:

.. code-block:: bash

    python manage.py generate_avro_schemas YOUR_EVENT_TYPE

Run ``python manage.py generate_avro_schemas --help`` to see the available options for the command.

2. The Avro schema for the :term:`Event Payload` will be generated in the ``openedx_events/event_bus/avro/tests/schemas`` directory.
3. Push the changes to the branch and create a pull request or run the checks locally to verify that the Avro schema was generated correctly.

.. code-block:: bash

    make test

Step 5: Send the Event Across Services with the Event Bus
==========================================================

To validate that you can consume the event emitted by a service through the event bus, you can send the event across services. Here is an example of how you can send the event across services using the Redis event bus implementation following the `setup instructions in a Tutor environment`_. We recommend also following the :doc:`../how-tos/use-the-event-bus` to understand how to use the event bus in your environment.

.. note:: If you implemented a custom serializer for a type in the :term:`Event Payload`, the custom serializer support must be included in both the producer and consumer sides before it can be used.

.. _Avro: https://avro.apache.org/
.. _OpenEdxPublicSignal: https://github.com/openedx/openedx-events/blob/main/openedx_events/tooling.py#L37
.. _attrs data classes: https://www.attrs.org/en/stable/overview.html
.. _serialize_event_data_to_bytes: https://github.com/openedx/openedx-events/blob/main/openedx_events/event_bus/avro/serializer.py#L82-L98
.. _deserialize_bytes_to_event_data: https://github.com/openedx/openedx-events/blob/main/openedx_events/event_bus/avro/deserializer.py#L86-L98
.. _setup instructions in a Tutor environment: https://github.com/openedx/event-bus-redis/blob/main/docs/tutor_installation.rst
.. _serialization: https://github.com/openedx/event-bus-redis/blob/main/edx_event_bus_redis/internal/producer.py#L128-L137
.. _deserialization: https://github.com/openedx/event-bus-redis/blob/main/edx_event_bus_redis/internal/consumer.py#L276-L289

**Maintenance chart**

+--------------+-------------------------------+----------------+--------------------------------+
| Review Date  | Reviewer                      |   Release      |Test situation                  |
+--------------+-------------------------------+----------------+--------------------------------+
|2025-02-10    | Maria Grimaldi                |   Sumac        |Pass.                           |
+--------------+-------------------------------+----------------+--------------------------------+
