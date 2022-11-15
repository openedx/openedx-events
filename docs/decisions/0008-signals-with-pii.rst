8. Event signals with PII
=========================

Status
------

Provisional

Context
-------

- Event signals can sometimes contain PII (Personally Identifiable Information), which is sensitive user information. We often store this as a PersonalUserData field inside a UserData field.
- The PII fields are often required fields, which would be serialization when publishing events to the event bus.
- The LMS often couples the PII data to its events. The LMS also serves as the `Identity Provider`_.
- Since we are dealing with user's personal data, there are often legal requirements around data retention and the ability for a user to request deletion of this data.

.. _Identity Provider: https://open-edx-proposals.readthedocs.io/en/latest/best-practices/oep-0042-bp-authentication.html#identity-provider-idp

Decision
--------

Events including PII will be published to the event bus as-is. We will rely on short data retention in the event bus to meet any legal requirements.

If longer data retention is required in the future, see "Deferred Alternatives" section for avoiding publishing PII.

Consequences
------------

- This decision does not cover data duplication of PII from the event bus into a consuming service. PII duplication should be avoided where possible. If duplicating PII is required, you must follow all legal requirements for enabling user data retirement in your service, which is outside the scope of this ADR.
- PII contained in most events should not be used as user data of record. Only user identity events (e.g. user created, user updated, etc.) should be used for this purpose, which do not yet exist as of the writing of this ADR.
- Event bus topics must be configured with short data retention (e.g. 2 weeks) to ensure the sensitive data will be deleted, regardless of requests from the user. You must follow your own legal team's advice for specifics around the maximum retention time.
- Event data that is logged (e.g. when an error is encountered) may also contain PII. Application logs often contain PII already and are usually treated as sensitive as a result, so this may not be a change from status quo, but for some applications it may be a new exposure route.

Deferred/Rejected Decisions
---------------------------

If the need arises to retain an event containing PII for a longer period of time than legally acceptable, the front-running solution is to create a second duplicate event that does not contain the PII (e.g. PersonalUserData) for use with the event bus. Details around naming conventions, etc. would need discovery.

References
----------

Discussion: `<https://github.com/openedx/openedx-events/issues/66>`_.

