11. Depending on multiple event bus implementations
###################################################

Status
******

**Accepted** *2023-05-25*

(This decision was actually made in November 2022, and retroactively documented in May 2023 but with additional, newer context such as the existence of event-bus-redis.)

Context
*******

The Event Bus is an abstraction allowing events to be passed from one IDA to another in near-real-time. The transport mechanism has to be something based on queues, but there are many possible options and none of them are likely to be suitable for all deployers. (For example, Kafka is a mature event store that would meet the needs of larger deployers, but Redis is already part of Open edX deployments and therefore better suited for smaller installations.) This has led us to create an abstraction layer: openedx-events provides IDAs an interface to the event bus, but relies on other packages to implement that interface. Currently we have event-bus-kafka and event-bus-redis, using Kafka and Redis as their respective transport mechanisms.

Any given deployer will likely only be using one of these implementations at most, and will need to install it one way or another. This can either be by explicit inclusion in the base requirements of each IDA ("in-tree") or by a separate installation process of one sort or another ("out-of-tree"). Each implementation package also has its own dependencies and dependency version constraints which may conflict with the other dependencies pulled in by any given IDA. Each package will need to be kept compatible with a significant number of IDAs.

Currently, use of the event bus is optional, so choice of implementation is moot for most deployers. However, we expect that the event bus will later become a core part of the architecture, such that all deployments will need to use one implementation or another.

Decision
********

We will depend on *all* known and supported event bus implementations in every IDA that needs to produce to or consume from the event bus.

All deployers will have all implementations installed and available for use. Dependency conflicts will need to be addressed as they arise during development and maintenance.

Consequences
************

By keeping all implementations in the base requirements, we have the following benefits:

- Version management is overall simplified. By including package versions in source control, we can more easily maintain stable development and production environments. Deployers can collaborate more easily because they are using shared version specifications.
- Developers will not have to repeatedly adjust their devstack containers to include the desired event bus implementation.
- Dependency conflicts will be discovered relatively quickly. If an IDA and an event bus implementation have incompatible constraints on a transitive dependency, there is no risk that we will upgrade the dependency in the IDA and then write code that relies on new features; we will instead have to solve the conflict up front.
- As a corollary, we can readily switch from explicit requirements to out-of-tree requirements, since dependencies will be kept consistent. This would not be true the other way around, since we might have to contend with various conflicts.
- This approach does not preclude the use of other implementations that are not part of the Open edX project. If a community member creates their own implementation and it is not offered to or accepted into the Open edX project, it can still be installed out-of-tree by that deployer.

There are also some downsides:

- The dependency tree is larger, and is more or less guaranteed to include at least one top-level dependency that each deployer is not using. Not only does each dependency take up bandwidth to download, space on disk, and time spent in upgrading packages, but it can also bring licensing and architecture incompatibilities.
- More concretely, event-bus-kafka depends on confluent-kafka, but that package does not provide binaries compatible with Linux on Apple Silicon. This means that developers on Apple M1 laptops cannot install this package in devstack at all. So as a knock-on effect, event-bus-kafka has had to keep confluent-kafka out of its own in-tree dependencies; deployers wishing to use it have to install and version that package out-of-tree anyhow. While this may eventually be resolved, this does obviate a number of the stated benefits for development and version management for the Kafka users.

We are not necessarily *satisfied* with this approach, but regard it as suitable for at least one release.

Rejected or deferred alternatives
*********************************

There are several alternative approaches we have considered:

- Have the implementation be part of the openedx-events package
- Just have one implementation
- Require all implementations to be installed out-of-tree
- Depend on one default implementation in-tree, and require that others be installed

Implement inside openedx-events
===============================

We briefly discussed the idea of including all of the implementations *in* the openedx-events package, possibly as extras (e.g. ``openedx-events[kafka]``). However, this would have complicated the development of openedx-events; it would have become impossible to e.g. pin the version of the Redis implementation in a dependent IDA while continuing to receive updates to the Kafka implementation. (The use of extras also would not have helped our dependencies issue; we'd then need to decide which extras to depend upon from IDAs' base requirements files.)

Single implementation
=====================

It's very unlikely that one implementation would satisfy everyone. Any event store, queue, or message bus technology that is used is additional software that deployers must learn to install, manage, configure, and operate. The exceptions would be MySQL and Redis, which are already used in Open edX. However, neither of these was used for the first implementation. Therefore, even if Redis turns out to work very well, we'll still need the extension point.

All out-of-tree
===============

As discussed, this results in more development friction (although possibly lower maintenance burden). The package also would not participate in our usual ``make upgrade`` process. This leads to either A) more operational risk if deployers leave the implementation package version unpinned in their deployment pipeline, or B) more toil if the version is pinned but has to be manually bumped in every IDA every time a new package version is released.

Not having *any* implementation provided in a standard devstack installation also makes Event Bus work unnecessarily difficult.

This decision is taking place against a backdrop of trying to use plugins and other extension mechanisms in more places, which would frequently require external dependencies. In the event bus work we have deferred figuring out how to reconcile out-of-tree dependency lists against our upgrade and pinning processes, but we'll need to figure it out sooner or later. Once we do, this option becomes more palatable (although likely not as appealing as the option in the next section, "one default").

One default
===========

Another option would be to select one implementation to always keep in the dependencies, and require that others be installed out-of-tree. If we went this route, we would likely choose event-bus-redis as the default, as it does not require the deployer to run additional services. (Redis is already used in Open edX deployments.)

Given that event-bus-kafka already requires out-of-tree installation, this may be a path we take in the future. However, 2U is using event-bus-kafka and developed the initial version of the event bus, and the direct inclusion of the dependency made that work easier. As the event bus and its main implementations stabilize, this factor may no longer have much weight.

As of May 2023, we are moving towards including event-bus-redis in *development* settings so that the event bus can be used in a standard devstack. It is possible that we will later choose to extend this to other environments, such that Redis will be the default for deployment as well. If so, we will likely reconsider our decision to include the Kafka implementation in our dependencies by default.

References
**********

(None.)
