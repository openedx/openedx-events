1. Events status
================

Status
------

Draft

Context
-------

Each Open edX Event will evolve according to the needs of the community.
For that reason, with this ADR, we attempt to define a lifecycle that each
event will follow individually.

Decision
--------

Each Open edX Event will follow the following lifecycle:

State 1. Provisional
~~~~~~~~~~~~~~~~~~~~

Events just created and accepted in the repository `openedx-events`,
these events haven't been accepted in Open edX platform or by the community.

State 2. Active
~~~~~~~~~~~~~~~

Events being used by Open edX platform and by the community.

State 3. Deprecated
~~~~~~~~~~~~~~~~~~~

Events that members of the community decide to deprecate in Open edX platform.

State 4. Removed
~~~~~~~~~~~~~~~~~

Events that members of the community removed from Open edX platform after
documentation and discussion of the removal.

State 5. Replaced
~~~~~~~~~~~~~~~~~

Events that members of the community replaced for another event after
documentation and discussion of the change.


Consequences
------------

1. Each event must carry its state in its code-annotation documentation.

2. Each event must go through each state in order. First, must be created
in this repository with the state `provisional`, when Open edX accepts it
must change to `active` and when the community decides to deprecate it, it
must be updated to `deprecated`, then `removed` and `unused`.

3. Each state must be up-to-date.
