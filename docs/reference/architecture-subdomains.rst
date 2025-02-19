Architecture Subdomains
##########################

Currently, these are the `architecture subdomains`_ used by the Open edX Events library:

+-------------------+----------------------------------------------------------------------------------------------------+
| Subdomain name    | Description                                                                                        |
+===================+====================================================================================================+
| Content Authoring | Allows educators to create, modify, package, annotate (tag), and share learning content.           |
+-------------------+----------------------------------------------------------------------------------------------------+
| Learning          | Allows learners to consume content and perform actions in a learning activity on the platform.     |
+-------------------+----------------------------------------------------------------------------------------------------+
| Analytics         | Provides visibility into learner behavior and course performance.                                  |
+-------------------+----------------------------------------------------------------------------------------------------+
| Enterprise        | Provides tools for organizations to manage their learners and courses.                             |
+-------------------+----------------------------------------------------------------------------------------------------+

Here we list useful information about Open edX architecture subdomains and their use in the Hooks Extension framework:

- `Events Naming and Versioning`_
- `Notes on events design and subdomains`_
- `edX Domain Driven Design documentation`_
- `Subdomains from OEP-41`_
- `Message Content Data Guidelines`_


.. _Events Naming and Versioning: https://github.com/openedx/openedx-events/blob/main/docs/decisions/0002-events-naming-and-versioning.rst#L1
.. _edX Domain Driven Design documentation: https://openedx.atlassian.net/wiki/spaces/AC/pages/213910332/Domain-Driven+Design
.. _Subdomains from OEP-41: https://docs.openedx.org/projects/openedx-proposals/en/latest/architectural-decisions/oep-0041-arch-async-server-event-messaging.html#subdomain-from-domain-driven-design
.. _Message Content Data Guidelines: https://docs.openedx.org/projects/openedx-proposals/en/latest/architectural-decisions/oep-0041-arch-async-server-event-messaging.html?highlight=subdomain#message-content-data-guidelines
.. _Notes on events design and subdomains: https://github.com/openedx/openedx-events/issues/72#issuecomment-1179291340
.. _architecture subdomains: https://microservices.io/patterns/decomposition/decompose-by-subdomain.html

**Maintenance chart**

+--------------+-------------------------------+----------------+--------------------------------+
| Review Date  | Reviewer                      |   Release      |Test situation                  |
+--------------+-------------------------------+----------------+--------------------------------+
|2025-02-05    | Maria Grimaldi                |  Sumac         |Pass.                           |
+--------------+-------------------------------+----------------+--------------------------------+
