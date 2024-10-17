13. Event definitions for special exam post-submission and review
#################################################################

Status
******

**Accepted** 2023-10-02

Context
*******

About Special Exams:
====================
* Course subsections that have an `exam_type` have additional logic that governs completion, grading, credit requirements, and more based on the `exam_type` value (e.g. timed, proctored, etc).
* These subsections are also known as **Special Exams**.
    * NOTE: The events described in this document will only be produced/consumed in the context of **Special Exams**.
* Course subsections that do not have an `exam_type` configured may still have a grading policy named 'Exam'. This type of content does not have the exam user experience and is not governed by any exam specific logic.

The New Exams IDA:
==================
* A new backend for exams called `edx-exams` is being developed (See the `exams IDA ADR <https://github.com/openedx/edx-proctoring/blob/master/docs/decisions/0004-exam-ida.rst>`_ for more info).
* We are currently working to use the event bus to trigger the downstream effects whenever an exam attempt is submitted or reviewed.
    * For example, when an exam attempt is submitted, we will want to make sure `edx-platform` knows to mark the exam subsection as completed.


Decision
********

Where these events will be produced/consumed:
=============================================

* `edx-exams` will produce these events.
    * NOTE: There is no plan to have the legacy exams backend, `edx-proctoring`, produce these events.
* `edx-platform` will consume these events in order to handle all behavior as it pertains to the state of an exam subsection.

Event Definitions:
==================
* We will define the events that as planned in `the ADR for events in edx-exams <https://github.com/edx/edx-exams/blob/main/docs/decisions/0004-downstream-effect-events.rst>`_.

Note on the Event Data/Signal Names:
====================================
We are using the prefix "Exam" as opposed to the prefix "Special_Exam" for these events because **Special Exams** will likely be the only type of exam that will be of concern to developers in the context of events for the forseeable future.


Consequences
************

* `edx-exams` will emit events via the event bus to send information without needing a response.
* Since, `edx-exams` already recieves and responds to REST requests, we will avoid creating circular dependencies because `edx-exams` will not need to send REST requests itself.
* These events are dynamic, in that they can also be consumed by other services/applications as needed in the future.

