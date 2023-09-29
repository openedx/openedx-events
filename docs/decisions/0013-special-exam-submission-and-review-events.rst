12. Event definitions for special exam post-submission and review
#################################################################

Status
******

**Draft** 2023-09-29

Context
*******

* A new backend for exams called `edx-exams` is being developed (See the `exams IDA ADR <https://github.com/openedx/edx-proctoring/blob/master/docs/decisions/0004-exam-ida.rst>`_ for more info).
* We are currently working to implement the downstream effects triggered whenever an exam attempt is submitted or reviewed. (For example, when an exam attempt is submitted, we will want to make sure `edx-platform` knows to mark the exam subsection as completed.)


Decision
********

* We have defined the events that we plan to define in `this ADR <https://github.com/edx/edx-exams/blob/main/docs/decisions/0004-downstream-effect-events.rst>`_ in `edx-exams` to use the event bus, as the new exams backend is independent in this ADR
* We plan for these events to be produced in `edx-exams`, and consumed in various `edx-platform` services (e.g. certificates, credit, instructor, grades).

* Note that events that use the newly defined data type:
    A. Pretain to "Special Exams", e.g. Timed or Proctored exams, and not non-timed course subsections that are labelled as an exam.

    B. Are only ever emitted from the newer exams backend, `edx-exams`, and never from the legacy exams backend, edx-proctoring.

* For the event data and signal names, we are using the prefix "Exam" as opposed to the prefix `Special_Exam` because "special exams" will likely be the only type of exam that will be of concern to developers in the context of events/the event bus.


Consequences
************

* `Edx-exams` will emit events via the event bus to send information without needing a response.
* Since, `edx-exams` already recieves and responds to REST requests, we will avoid creating circular dependencies because `edx-exams` will not need to send REST requests itself.
* These events are dynamic, in that they can also be consumed in other places as needed.

