17. Event Signal for External Grader Score Submission
#####################################################

Status
******

**Provisional** *2025-03-18*

Implemented by: https://github.com/openedx/openedx-events/pull/482

Context
*******

The Open edX platform is currently undergoing a migration from the traditional XQueue system to a more modern event-driven architecture for processing external grader submissions. As part of this transition, we need a standardized way to communicate scoring events between services.

Currently, the communication between external graders and the LMS relies on HTTP callbacks, which:

1. Creates tight coupling between services
2. Introduces potential points of failure through network dependencies
3. Makes asynchronous processing difficult
4. Complicates system monitoring and debugging

An event-based approach would resolve these issues by providing a standardized, decoupled communication mechanism between components involved in the external grading workflow.

Decision
********

We will add a new event signal to the openedx-events repository to standardize the communication of external grader score submissions. This event will be triggered in the edx-submissions repository's when a score is received:

1. **Create ExternalGraderScoreData Class**:
   - Define an immutable data structure using ``attr.s(frozen=True)``
   - Include all necessary fields for score processing: points_earned, points_possible, course_id, etc.
   - Ensure proper typing for validation

2. **Implement EXTERNAL_GRADER_SCORE_SUBMITTED Signal**:
   - Define event type following Open edX naming conventions
   - Use the standard OpenEdxPublicSignal implementation
   - Include appropriate metadata and documentation
   - Ensure the signal carries the ExternalGraderScoreData

3. **Event Trigger Points**:
   - This event will be triggered in edx-submissions when a score is received
   - Specifically, it will be emitted in the submissions put_result service after the score has been successfully recorded in the database
   - The primary trigger location will be in the views/xqueue.py module's save_score function

4. **Event Receiver**:
   - The event will be received in the LMS using a signal receiver decorator
   - The receiver function `handle_external_grader_score` will update the corresponding XBlock
   - This receiver will replace the HTTP callback mechanism previously used with Xqueue

Implementation:

.. code-block:: python

   @attr.s(frozen=True)
   class ExternalGraderScoreData:
       """
       Class that encapsulates score data provided by an external grader.

       This class uses attr.s with frozen=True to create an immutable structure
       containing information about the score assigned to a student submission.

       Attributes:
           points_possible (int): Maximum possible score for this assignment
           points_earned (int): Score earned by the student
           course_id (str): Unique identifier for the course
           score_msg (str): Descriptive message about the score (feedback)
           submission_id (int): Unique identifier for the graded submission
           user_id (str): ID of the user who submitted the assignment
           module_id (str): ID of the module/problem being graded
           queue_key (str): Unique key for the submission in the queue
           queue_name (str): Name of the queue that processed the submission
       """

       points_possible = attr.ib(type=int)
       points_earned = attr.ib(type=int)
       course_id = attr.ib(type=str)
       score_msg = attr.ib(type=str)
       submission_id = attr.ib(type=int)
       user_id = attr.ib(type=str)
       module_id = attr.ib(type=str)
       queue_key = attr.ib(type=str)
       queue_name = attr.ib(type=str)

   # .. event_type: org.openedx.content_authoring.external_grader.score.submitted.v1
   # .. event_name: EXTERNAL_GRADER_SCORE_SUBMITTED
   # .. event_description: emitted when an external grader provides a score for a submission
   # .. event_data: ExternalGraderScoreData
   EXTERNAL_GRADER_SCORE_SUBMITTED = OpenEdxPublicSignal(
       event_type="org.openedx.content_authoring.external_grader.score.submitted.v1",
       data={
           "score_data": ExternalGraderScoreData,
       }
   )

Consequences
************

This event signal provides a standardized way for communicating external grader scores across Open edX services. It supports the transition from HTTP-based callbacks to a more robust event-driven architecture.

The primary benefits include decoupled services, standardized communication, and support for asynchronous processing. The main consideration is ensuring coordination between services during implementation.

References
**********

Related Repositories:

* openedx-events: https://github.com/openedx/openedx-events
* edx-submissions: https://github.com/openedx/edx-submissions
* edx-platform: https://github.com/openedx/edx-platform
* edx-submissions event implement in PR: https://github.com/openedx/edx-submissions/pull/292

Documentation:

* Open edX Events Framework Documentation: https://github.com/openedx/openedx-events/blob/master/README.rst
* XQueue Migration Plan: https://github.com/openedx/edx-platform/pull/36258
