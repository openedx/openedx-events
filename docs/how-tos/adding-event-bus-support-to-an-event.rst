Adding Event Bus Support to an Open edX Event
=============================================

Before sending an event across services, you need to ensure that the event is compatible with the Open edX Event Bus. This involves ensuring that the event, with its corresponding payload, can be emitted by a service through the event bus and that it can be consumed by other services. This guide will walk you through the process of adding event bus support to an Open edX event.

For more details on how the :term:`Event Payload` is structured refer to the :doc:`../decisions/0003-events-payload` decision record.

.. note::
    This guide assumes that you have already created an Open edX event. If you haven't, refer to the :doc:`../how-tos/creating-new-events` how-to guide.

Step 1: Does my Event Need Event Bus Support?
----------------------------------------------

By default, Open edX Events should be compatible with the Open edX Event Bus. However, there are cases when the support might not be possible or needed for a particular event. Here are some scenarios where you might not need to add event bus support:

- The event is only used within the same application process and cannot be scoped to other services.
- The :term:`Event Payload` contains data types that are not supported by the event bus, and it is not possible to refactor the :term:`Event Payload` to use supported data types.

When adding support is not possible do the following:

- Add it to the ``KNOWN_UNSERIALIZABLE_SIGNALS`` list in the ``openedx_events/tooling.py`` file so the event bus ignores it.
- Add a ``warning`` in the event's docstring to inform developers that the event is not compatible with the event bus and why.

If you don't add the event to the ``KNOWN_UNSERIALIZABLE_SIGNALS`` list, the CI/CD pipeline will fail for the missing Avro schema that could not be generated for the :term:`Event Payload`. If you don't add a warning in the event's docstring, developers might try to send the event across services and encounter issues.

Step 2: Define the Event Payload
--------------------------------

An Open edX Event is compatible with the event bus when its payload can be serialized, sent, and deserialized by other services. The payload, structured as `attrs data classes`_, must align with the event bus schema format which in this case is the :term:`Avro Schema`. This schema is used to serialize and deserialize the :term:`Event Payload` when sending it across services.

This ensures the event can be sent by the producer and be then re-emitted by the same instance of `OpenEdxPublicSignal`_ on the consumer side. For more information on the event bus schema format, refer to the :doc:`../decisions/0004-external-event-bus-and-django-signal-events` and :doc:`../decisions/0005-external-event-schema-format` decision records.

Here is an example of an :term:`Event Payload` structured as `attrs data classes`_ that align with the event bus schema format:

.. code-block:: python

    @attr.s(frozen=True)
    class UserNonPersonalData:
        """
        Attributes defined for Open edX user object based on non-PII data.

        Arguments:
            id (int): unique identifier for the Django User object.
            is_active (bool): indicates whether the user is active.
        """

        id = attr.ib(type=int)
        is_active = attr.ib(type=bool)

    @attr.s(frozen=True)
    class UserPersonalData:
        """
        Attributes defined for Open edX user object based on PII data.

        Arguments:
            username (str): username associated with the Open edX user.
            email (str): email associated with the Open edX user.
            name (str): name associated with the Open edX user's profile.
        """

        username = attr.ib(type=str)
        email = attr.ib(type=str)
        name = attr.ib(type=str, factory=str)

    @attr.s(frozen=True)
    class UserData(UserNonPersonalData):
        """
        Attributes defined for Open edX user object.

        This class extends UserNonPersonalData to include PII data completing the
        user object.

        Arguments:
            pii (UserPersonalData): user's Personal Identifiable Information.
        """

        pii = attr.ib(type=UserPersonalData)

    @attr.s(frozen=True)
    class CourseData:
        """
        Attributes defined for Open edX Course Overview object.

        Arguments:
            course_key (str): identifier of the Course object.
            display_name (str): display name associated with the course.
            start (datetime): start date for the course.
            end (datetime): end date for the course.
        """

        course_key = attr.ib(type=CourseKey)
        display_name = attr.ib(type=str, factory=str)
        start = attr.ib(type=datetime, default=None)
        end = attr.ib(type=datetime, default=None)

The data types used in the attrs classes that the current Open edX Event Bus with the chosen schema are:

Primitive Data Types
~~~~~~~~~~~~~~~~~~~~

- Boolean
- Integer
- Float
- String
- Bytes

Complex Data Types
~~~~~~~~~~~~~~~~~~

- Type-annotated Lists (e.g., ``List[int]``, ``List[str]``)
- Attrs Classes (e.g., ``UserNonPersonalData``, ``UserPersonalData``, ``UserData``, ``CourseData``)
- Types with Custom Serializers (e.g., ``CourseKey``, ``datetime``)

Ensure that the :term:`Event Payload` is structured as `attrs data classes`_ and that the data types used in those classes align with the event bus schema format.

Step 3: Ensure Serialization and Deserialization
------------------------------------------------

Before sending the event across services, you need to ensure that the :term:`Event Payload` can be serialized and deserialized correctly. The event bus concrete implementations use the :term:`Avro Schema` to serialize and deserialize the :term:`Event Payload` as mentioned in the :doc:`../decisions/0005-external-event-schema-format` decision record. The concrete implementation of the event bus handles the serialization and deserialization with the help of methods implemented by this library.

.. For example, here's how the Redis event bus handles serialization before sending a message:

.. .. code-block:: python
..     :emphasize-lines: 4

..     # edx_event_bus_redis/internal/producer.py
..     full_topic = get_full_topic(topic)
..     context.full_topic = full_topic
..     event_bytes = serialize_event_data_to_bytes(event_data, signal)
..     message = RedisMessage(topic=full_topic, event_data=event_bytes, event_metadata=event_metadata)
..     stream_data = message.to_binary_dict()

.. Where `serialize_event_data_to_bytes`_ is a method that serializes the :term:`Event Payload` to bytes using the Avro schema. While the consumer side deserializes the :term:`Event Payload` using the Avro schema with the help of the `deserialize_bytes_to_event_data`_ method:

.. .. code-block:: python
..     :emphasize-lines: 3

..     # edx_event_bus_redis/internal/consumer.py
..     signal = OpenEdxPublicSignal.get_signal_by_type(msg.event_metadata.event_type)
..     event_data = deserialize_bytes_to_event_data(msg.event_data, signal)
..     send_results = signal.send_event_with_custom_metadata(msg.event_metadata, **event_data)

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

Now the :term:`Event Payload` can be serialized and deserialized correctly when sent across services.

.. warning::
    One of the known limitations of the current Open edX Event Bus is that it does not support dictionaries as data types. If the :term:`Event Payload` contains dictionaries, you may need to refactor the :term:`Event Payload` to use supported data types. When you know the structure of the dictionary, you can create an attrs class that represents the dictionary structure. If not, you can use a str type to represent the dictionary as a string and deserialize it on the consumer side using JSON deserialization.

If your :term:`Event Payload` contains only supported data types, you can skip this step.

Step 4: Generate the Avro Schema
--------------------------------

As mentioned in the previous step, the serialization and deserialization of the :term:`Event Payload` is handled by the concrete event bus implementation with the help of methods implemented in this library. However, although openedx-events does not handles the serialization and deserialization of the :term:`Event Payload` directly, it ensures the payload of new events can be serialized and deserialized correctly by adding checks in the CI/CD pipeline for schema verification. To ensure this, you need to generate the Avro schema for the :term:`Event Payload`:

1. Run the following command to generate the Avro schema for the :term:`Event Payload`:

.. code-block:: bash

    python manage.py generate_avro_schemas org.openedx.learning.course.enrollment.changed.v1

2. The Avro schema for the :term:`Event Payload` will be generated in the ``openedx_events/event_bus/avro/tests/schemas`` directory.
3. Push the changes to the branch and create a pull request or run the checks locally to verify that the Avro schema was generated correctly.

.. code-block:: bash

    make test

Step 5: Send the Event Across Services with the Event Bus
---------------------------------------------------------

To validate that you can consume the event emitted by a service through the event bus, you can send the event across services. Here is an example of how you can send the event across services using the Redis event bus implementation following the `setup instructions in a Tutor environment`_.

.. _Avro: https://avro.apache.org/
.. _OpenEdxPublicSignal: https://github.com/openedx/openedx-events/blob/main/openedx_events/tooling.py#L37
.. _attrs data classes: https://www.attrs.org/en/stable/overview.html
.. _serialize_event_data_to_bytes: https://github.com/openedx/openedx-events/blob/main/openedx_events/event_bus/avro/serializer.py#L82-L98
.. _deserialize_bytes_to_event_data: https://github.com/openedx/openedx-events/blob/main/openedx_events/event_bus/avro/deserializer.py#L86-L98
.. _setup instructions in a Tutor environment: https://github.com/openedx/event-bus-redis/blob/main/docs/tutor_installation.rst
