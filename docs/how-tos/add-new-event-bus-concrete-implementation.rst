Add a New Concrete Implementation of the Event Bus
==================================================

Context
-------

Here is a list of the existing concrete implementations of the event bus:

- `Kafka <https://github.com/openedx/event-bus-kafka>`_
- `Redis Streams <https://github.com/openedx/event-bus-redis>`_

This how-to is to help you add a new concrete implementation, for example using Pulsar or some other technology.

Producing
---------

There should be a producer class that inherits from `EventBusProducer <https://github.com/openedx/openedx-events/blob/cbb59f124ed84afacb9ec99baa82a86381370dcc/openedx_events/event_bus/__init__.py#L66>`_ in openedx-events.

The defined ``send`` method is meant to be called from within a signal receiver in the producing service.

Consuming
---------

At a high level, the consumer should be a process that takes the signals and events from the broker and emits the signal with the event. There should be a consumer class that inherits from `EventBusConsumer <https://github.com/openedx/openedx-events/blob/06635f3642cee4020d6787df68bba694bd1233fe/openedx_events/event_bus/__init__.py#L127>`_ in openedx-events.

The consumer class then needs to implement ``consume_indefinitely`` loop, which will stay running and listen to events as they come in.

We have included an utility function called `prepare_for_new_work_cycle <../../openedx_events/tooling.py#L323>`_ in openedx-events which needs to be called before processing any signal. Currently, it reconnects the db connection if required as well as clears RequestCache and there may be later, more comprehensive changes. These steps mimic some setup/teardown that is normally performed by Django in its request/response based architecture.

Checkout `consumer.py <https://github.com/openedx/event-bus-redis/blob/main/edx_event_bus_redis/internal/consumer.py>`_ in event bus redis implementation.

Abstraction tickets
-------------------

The known remaining work for a fully abstracted event bus is captured in the `Abstraction tickets <https://github.com/orgs/edx/projects/11/views/4?filterQuery=label%3Aevent-bus+-status%3ADone+abstraction>`_
