1. Purpose of this Repo
=======================

Status
------

Draft

Context
-------

OEP-50 was created with the intention of create a common pattern to extend some places of the platform in a more suitable way. In this regard, it was defined a set of requirements that requires the creation of a repository to store the Django Signals definitions used in edx-platform that could be used by plugins or in other Djangoapps.

Decision
--------

This repository was created as a home for all the definitions of the Django Signals (events) of the edx-platform.

Consequences
------------

Some Django Signals defined in edx-platform will moved to this library.
