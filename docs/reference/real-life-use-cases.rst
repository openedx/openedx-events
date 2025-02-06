Real-Life Use Cases for Open edX Events
########################################

Overview
**********

As mentioned in the :doc:`docs.openedx.org:developers/concepts/hooks_extension_framework` docs, Open edX Events can be used to integrate application components with each other or with external services, allowing them to communicate, synchronize, and perform additional actions when specific triggers occur.

To illustrate the different solutions that can be implemented with this approach, we have compiled a list of use cases built using Open edX Events to address various challenges. The goal of this list is to serve as a reference for extension developers to implement their own solutions in their own plugins or IDAs based on the community's experience.

Use Cases
**********

The following list of real-life use cases showcases the different ways Open edX Events can be used to facilitate communication between IDAs and application components, allowing them to interact, synchronize, and perform additional actions when specific triggers occur.

Cross-services communication
=============================

As mentioned in :doc:`../concepts/event-bus`, the suggested strategy for cross-service communication in the Open edX ecosystem is through an event-based architecture implemented via the :doc:`../concepts/event-bus`. This functionality used for asynchronous communication between services is built on top of sending Open edX Events (Open edX-specific Django signals) within a service. For more details on the Event Bus,  please see :doc:`../how-tos/use-the-event-bus-to-broadcast-and-consume-events`.

Here are some examples of how the Event Bus can be used to facilitate communication between IDAs:

Exam Downstream Effects
------------------------

The `edx-exams`_ service adopts an event-driven architecture, using the event bus to allow communication with edx-platform to downstream effects. Unlike the legacy exams system (`edx-proctoring`_), which relied on direct function calls to edx-platform services, the event bus sends exam-specific events received by the LMS, triggering responses like grade overrides without creating dependencies between the two.

This approach implements a modular and scalable system by enabling `edx-exams`_ to function independently from edx-platform while still interacting through asynchronous communication.

More details on: `ADR Implementation of Event Driven Architecture for Exam Downstream Effects`_.

Course Metadata Synchronization
--------------------------------

An event is emitted each time a course is published by the CMS, which is sent to the event bus and received by the `Course Discovery`_ service. This process allows `Course Discovery`_ to automatically update course metadata, ensuring that any changes in the CMS are reflected. By communicating through the event bus, this setup decreases the need for manual data syncs, keeping course metadata consistently up-to-date across services.

More details on: `Use Event Bus to Replace Refresh Course Metadata`_.

Credentials Management
-------------------------

When the LMS emits certificate-related events, they are sent to the event bus and received by the `Credentials`_ service. `Credentials`_ can automatically award or revoke learner credentials based on the event type. This integration simplifies credential management by enabling real-time updates from the LMS, ensuring the appropriate generation of learner credentials without requiring manual synchronization.

More details on: `Credentials - Event Bus`_.

Credly Integration
--------------------

The LMS sends events about learner progress, like course and section completions, through the event bus. The `Credentials`_ service then receives these events, adds extra information, and forwards them to external credential providers such as `Credly`_. These providers create and display digital credentials for learners based on the completion data.

More details on: `Credly Integration`_.

Real-Time Event Tracking
--------------------------

To make event tracking faster and more efficient, tracking logs are optionally sent through the event bus instead of the traditional method, which relied on asynchronous tasks to process logs. A receiver listens for each tracking event and sends it to the event bus, allowing real-time updates. This new approach improves performance by reducing delays, as logs now reach the `Aspects`_ stack in a near real-time manner.

More details on: `Real-Time Event Tracking`_.

Communication between Application Components
********************************************

Open edX Events can also be used to facilitate communication between different application components running in the same process, allowing them to interact and synchronize their actions. Here are some examples of how Open edX Events can be used to coordinate between application components:

Automatic Content Tagging
---------------------------

When new content is created or existing content is edited, these events trigger updates to automatically apply relevant tags based on system-defined categories. This ensures that content is consistently tagged, reducing the need for manual tagging and keeping content classification up-to-date.

More details on: `Automatic Content Tagging`_.

Keep Search Indexes Up-To-Date
---------------------------------

Each time content is updated or created, an event is emitted that triggers the indexing of the new content, automatically updating the search index with the latest content metadata. This ensure that all content changes are accurately reflected in search results.

More details on: `Update Search Indexes`_

External Certificate Generation
--------------------------------

Events are sent after the certificate generation for a user when they complete a course, these events trigger the generation of corresponding certificates in an external system if the proper conditions are met, allowing for seamless integrations with external certification services.

More details on: `External Certificate Generation`_.

Automatic Group Association
----------------------------

Enrollment events trigger the association of the user into a pre-defined cohort based on the user's preference language. This way, instructors don't need to add a student into a cohort manually, but it's automatically done, reducing logistic efforts and creating more seamless integrations with language-based restricted content.

More details on: `Automatic Group Association`_.

Forum Emails Notifier
-----------------------

When new threads, responses or comments are created in the discussion forum, events are sent with relevant information about what occurred, triggering email notifications with relevant information about the update based on the user's preferences. This allows users stay up-to-date with discussions threads.

More details on: `Forum Emails Notifier`_.

Webhooks Integration
----------------------

`Webhooks`_ trigger an HTTP POST request to a configurable URL when certain events happen in the Open edX platform, including information relevant to the event. When these events are sent, then the data is sent to services like Zapier or any other configured, allowing the sharing of data between different external services.

More details on:

* `Webhooks`_.
* `Open edX Events Sender`_.
* `Open edX Events To Zapier`_.

Send ORA Submissions to Third-Party Plagiarism Services
---------------------------------------------------------

Each time a student submits an Open Response Assessment (ORA), an event is emitted triggering a request to external services to review the student response for plagiarism. This allows a seamless integration of tools to help instructors while grading.

More details on: `Send ORA Submissions to Third-Party Plagiarism Services`_.

Other Use Cases
================

Here are some additional use cases that can be implemented using Open edX Events:

- `Linking In-Context Discussions to Units`_
- `Send Staff Notification`_
- `Course-wide Notifications`_
- `Program Certificate Sync`_
- `Link User to Invite`_
- `Enterprise Unenrollment Sync`_
- `IDV Integration with new Vendors`_

.. note:: If you have implemented a solution using Open edX Events and would like to share it with the community, please submit a pull request to add it to this list!

.. _edx-exams: https://github.com/edx/edx-exams
.. _edx-proctoring: https://github.com/openedx/edx-proctoring
.. _ADR Implementation of Event Driven Architecture for Exam Downstream Effects: https://github.com/edx/edx-exams/blob/main/docs/decisions/0004-downstream-effect-events.rst
.. _Course Discovery: https://github.com/openedx/course-discovery
.. _Use Event Bus to Replace Refresh Course Metadata: https://github.com/openedx/course-discovery/blob/master/docs/decisions/0015-event-bus-with-rcm.rst
.. _Credentials: https://github.com/openedx/credentials
.. _Credly: https://credly.com/
.. _Credentials - Event Bus: https://github.com/openedx/credentials/blob/master/docs/event_bus.rst
.. _Credly Integration: https://github.com/openedx/platform-roadmap/issues/280
.. _Aspects: https://github.com/openedx/openedx-aspects
.. _Real-Time Event Tracking: https://github.com/openedx/wg-data/issues/28
.. _Automatic Content Tagging: https://github.com/openedx/modular-learning/issues/78
.. _Update Search Indexes: https://github.com/openedx/edx-platform/pull/34391
.. _External Certificate Generation: https://github.com/eduNEXT/eox-nelp/blob/master/eox_nelp/signals/receivers.py#L113-L160
.. _Automatic Group Association: https://github.com/eduNEXT/openedx-unidigital/blob/main/openedx_unidigital/handlers.py#L26-L51
.. _Forum Emails Notifier: https://github.com/eduNEXT/platform-plugin-forum-email-notifier
.. _Webhooks: https://github.com/aulasneo/openedx-webhooks?tab=readme-ov-file#introduction
.. _Open edX Events Sender: https://github.com/open-craft/openedx-events-sender:
.. _Open edX Events To Zapier: https://github.com/eduNEXT/openedx-events-2-zapier:
.. _Send ORA Submissions to Third-Party Plagiarism Services: https://github.com/eduNEXT/platform-plugin-turnitin/blob/main/platform_plugin_turnitin/handlers.py#L9-L26
.. _Linking In-Context Discussions to Units: https://github.com/openedx/edx-platform/blob/master/openedx/core/djangoapps/discussions/docs/decisions/0004-in-context-discussions-linking.rst
.. _Send Staff Notification: https://github.com/openedx/edx-ora2/pull/2201
.. _Course-wide Notifications: https://github.com/openedx/edx-platform/pull/33666
.. _Program Certificate Sync: https://github.com/openedx/credentials/pull/2119
.. _Link User to Invite: https://github.com/academic-innovation/mogc-partnerships/blob/main/mogc_partnerships/receivers.py#L9
.. _Enterprise Unenrollment Sync: https://github.com/openedx/edx-enterprise/pull/1754
.. _IDV Integration with new Vendors: https://openedx.atlassian.net/wiki/spaces/OEPM/pages/4307386369/Proposal+Add+Extensibility+Mechanisms+to+IDV+to+Enable+Integration+of+New+IDV+Vendor+Persona#Event-Hooks

**Maintenance chart**

+--------------+-------------------------------+----------------+--------------------------------+
| Review Date  | Working Group Reviewer        |   Release      |Test situation                  |
+--------------+-------------------------------+----------------+--------------------------------+
|2025-02-05    | BTR WG - Maria Grimaldi       |Redwood         |Pass.                           |
+--------------+-------------------------------+----------------+--------------------------------+