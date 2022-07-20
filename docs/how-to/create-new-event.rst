How to create a new Open edX Event
==================================

The mechanisms implemented by the Open edX Events library are supported and maintained by the Open edX community.
Therefore, we've put together a guide on how to add a new event to have an effective contribution process.


1. Propose the new event to the community
-----------------------------------------

When creating a new event, you must justify its implementation. For example, you could create a post in Discuss,
send a message through slack or open a new issue in the library repository listing your use cases for it. Or even,
if you have time, you could accompany your proposal with the implementation of the event to illustrate its behavior.


2. Create the data attributes for the event (OEP-49)
----------------------------------------------------

Events send data attribute instances when triggered. Therefore, when designing your new event definition you must
decided if an existent data attribute class works for your use case or you must create a new one. If the answer is
the latter, then try to answer:

- Which attributes of the object are the most relevant?
- Which type are they?
- Is any of them optional/required?

And with that information, create the new class justifying each decision. The class created in this step must comply
with:

- It should be created in the `data.py` file in the corresponding subdomain. Refer to Naming Conventions ADR for more
  on events subdomains.
- It should follow the naming conventions specified in...

3. Create the event definition
------------------------------

Open edX Events are instances of the class OpenEdxPublicSignal, this instance represents the event definition that
specifies:

- The event type which should follow the conventions in the Naming Conventions ADR.
- The events' payload, here you must use the class you decided on before.

The definition created in this step must comply with:

- It should be created in the `signals.py` file in the corresponding subdomain. Refer to Naming Conventions ADR for more
  on events subdomains.
- It should follow the naming conventions specified in Naming Conventions ADR.
- It must be documented using in-line documentation with at least: `event_type`, `event_name`, `event_description` and
  `event_data`.

4. Integrate into service
-------------------------

After or during the events definition implementation, you now must trigger the event in the service you intentioned. Meaning:

- Add the openedx-events library to the service project.
- Import the events' data and definition into the place where will be triggered. Remember the Open edX Events purpose when
  choosing a place to send the new event

Before opening a PR in the service project, refer to its contribution guidelines.
