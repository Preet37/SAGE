# Source: https://docs.temporal.io/encyclopedia/event-history/event-history-go
# Title: Event History walkthrough with the Go SDK - Temporal Docs
# Fetched via: trafilatura
# Date: 2026-04-09

Event History walkthrough with the Go SDK
In order to understand how Workflow Replay works, this page will go through the following walkthroughs:
[How Workflow Code Maps to Commands](#How-Workflow-Code-Maps-To-Commands)[How Workflow Commands Map to Events](#How-Workflow-Commands-Map-To-Events)[How History Replay Provides Durable Execution](#How-History-Replay-Provides-Durable-Execution)[Example of a Non-Deterministic Workflow](#Example-of-Non-Deterministic-Workflow)
How Workflow Code Maps to Commands[](#How-Workflow-Code-Maps-To-Commands)
This walkthrough will cover how the Workflow code maps to Commands that get sent to the Temporal Service, letting the Temporal Service know what to do.
How Workflow Commands Map to Events[](#How-Workflow-Commands-Map-To-Events)
The Commands that are sent to the Temporal Service are then turned into Events, which build up the Event History. The Event History is a detailed log of Events that occur during the lifecycle of a Workflow Execution, such as the execution of Workflow Tasks or Activity Tasks. Event Histories are persisted to the database used by the Temporal Service, so they're durable, and will even survive a crash of the Temporal Service itself.
These Events are what are used to recreate a Workflow Execution's state in the case of failure.
How History Replay Provides Durable Execution[](#How-History-Replay-Provides-Durable-Execution)
Now that you have seen how code maps to Commands, and how Commands map to Events, this next walkthrough will take a look at how Temporal uses Replay with the Events to provide Durable Execution and restore a Workflow Execution in the case of a failure.
This code walkthrough will begin by walking through a Workflow Execution, describing how the code maps to Commands and Events. There will then be a Worker crash halfway through, explaining how Temporal uses Replay to recover the state of the Workflow Execution, ultimately resulting in a completed execution that's identical to one that had not crashed.
Example of a Non-Deterministic Workflow[](#Example-of-Non-Deterministic-Workflow)
Now that Replay has been covered, this section will explain why Workflows need to be
[deterministic](https://docs.temporal.io/workflow-definition#deterministic-constraints) in order for Replay to work.
A Workflow is deterministic if every execution of its Workflow Definition produces the same Commands in the same sequence given the same input.
As mentioned in the [ How History Replay Provides Durable Execution](#How-History-Replay-Provides-Durable-Execution)
walkthrough, in the case of a failure, a Worker requests the Event History to replay it. During Replay, the Worker runs
the Workflow code again to produce a set of Commands which is compared against the sequence of Commands in the Event
History. When there’s a mismatch between the expected sequence of Commands the Worker expects based on the Event History
and the actual sequence produced during Replay (due to non-determinism), Replay will be unable to continue.
To better understand why Workflows need to be deterministic, it's helpful to look at a Workflow Definition that violates it. In this case, this code will walk through a Workflow Definition that breaks the determinism constraint with a random number generator.
Note that non-deterministic failures do not fail the Workflow Execution by default. A non-deterministic failure is
considered a [Workflow Task Failure](https://docs.temporal.io/references/failures#workflow-task-failures) which is
considered a transient failure, meaning it retries over and over. Users can also fix the source of non-determinism,
perhaps by removing the Activity, and then restart the Workers. This means that this type of failure can recover by
itself. You can also use a strategy called versioning to address this non-determinism error. See
[versioning](/develop/go/workflows/versioning) to learn more.
For more information on how Temporal handles Durable Execution or to see these slides in a video format with more
explanation, check out our free, self-paced courses: [Temporal 102](https://learn.temporal.io/courses/temporal_102/) and
[Versioning Workflows](https://learn.temporal.io/courses/versioning/).
Temporal Applications Support Non-Deterministic Operations[](#temporal-applications-support-non-deterministic-operations)
We want to emphasize that although your Workflows themselves need to be deterministic, your application itself does not!
Remember that pretty much anything that interacts with the external world is inherently non-deterministic:
- Calling LLM APIs
- Querying databases
- Reading or writing files
- Making HTTP requests to external services
Good news: Your Temporal application can absolutely handle all of these operations. While your Workflow must be deterministic, your application absolutely can handle any type of non-deterministic operation, including those listed above. This gives you the best of both worlds—the crash-proof reliability of a Workflow and the resiliency of Activities which have built-in support for retries.