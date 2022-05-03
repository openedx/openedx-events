6. Optional fields in events
===========================================

Status
------

Provisional

Context
-------
The ``attrs`` documentation specifically defines the notion of optionality as, "An optional attribute is one which
can be set to None in addition to satisfying the requirements of the sub-validator." Importantly, under this definition,
the user must still provide a value for this optional field when instantiating the ``attrs``-decorated class,
but this value can be ``None``. Separately, attrs fields can have a ``default`` value, which will provide a value for
the field if the user does not supply one at instantiation.

The Avro documentation describes somewhat similar mechanics for its fields. If a field's ``type`` list includes
"null," the user can set the value of the field to null/None. Separately, if a field is defined with a ``default``
parameter, then the user does not have to set the value at all. However, it seems the ``default`` parameter may not be
fully-supported with Kafka (see https://github.com/confluentinc/kafka-rest/issues/427 ). The Avro documentation,
in contrast to that of ``attrs``, uses the default parameter to define optionality.

Decision
--------

- The bridge will convert ``attrs`` fields with a default value of None to Avro fields with type = ["null",<type>]
and default = "null".
- Top-level fields in event data definitions will not be optional. This is contrary to and overrides the decision made in
 ":doc:`0006-event-schema-serialization-and-evolution.rst`"


Consequences
------------

- The notions of "optionality" and "nullability" will be effectively conflated. This means no distinctions will be made
between fields for which ``None`` is a valid value and fields that simply do not need to be supplied.
- Attr fields with defaults that are not ``None`` will be treated as required
- At the point of writing this ADR, it is unclear exactly how Kafka will treat the addition and removal of optional
fields for the purposes of schema evolution (because of the issue linked above). This will require a little more testing.

Deferred/Rejected Decisions
---------------------------

-
