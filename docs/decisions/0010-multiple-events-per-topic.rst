9. Combining multiple event types on one topic
==============================================

Status
------

Accepted

Context
-------
As initially implemented, the Kafka-backed event bus assumed that every topic
would only have events of one type.

Alternatives
------------
1. topic-record-name strategy
2. unions
3. enforce same schema

Github discussion
-----------------
