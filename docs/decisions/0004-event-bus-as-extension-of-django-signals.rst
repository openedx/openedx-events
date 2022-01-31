1 Event bus as extension of django signals
------------------------------------------

1.1 Context
~~~~~~~~~~~

- Django Signals are widely used in edx-platform and elsewhere. OpenedX developers are familiar with Django Signals.

- Django Signals are much cheaper to send, and offer pretty much no additional work as compared to sending via Kafka.

- Django Signals don’t require extra infrastructure and are simpler for people to test with.

- We want to make it easy to integrate different event bus technologies

1.2 Decision
~~~~~~~~~~~~

Django signals will be used as the event bus for internal service communication and external event bus will be implemented as an app listening for relevant Django signals and passing it on to external event bus.
