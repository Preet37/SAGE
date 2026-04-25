# Source: https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-external-events
# Author: PatrickFarley
# Author Slug: patrickfarley
# Title: Azure Durable Functions — External events (raise/wait) for human-in-the-loop signaling
# Fetched via: trafilatura
# Date: 2026-04-10

Note
Access to this page requires authorization. You can try [signing in](#) or [changing directories].
Access to this page requires authorization. You can try [changing directories].
Orchestrator functions can wait and listen for external events. This feature of [Durable Functions](what-is-durable-task) is often useful for handling human interaction or other external triggers.
Note
External events are one-way asynchronous operations. They aren't suitable for situations where the client sending the event needs a synchronous response from the orchestrator function.
Orchestrations can wait and listen for external events. This feature is often useful for handling human interaction or other external triggers.
Note
External events are one-way asynchronous operations. They aren't suitable for situations where the client sending the event needs a synchronous response from the orchestration.
Important
Currently, the PowerShell Durable Task SDK isn't available.
Wait for events
The "wait-for-external-event" API of the [orchestration trigger binding](../../azure-functions/durable-functions/durable-functions-bindings#orchestration-trigger) allows an orchestrator function to asynchronously wait and listen for an event delivered by an external client. The listening orchestrator function declares the name of the event and the shape of the data it expects to receive.
The "wait-for-external-event" API allows an orchestration to asynchronously wait and listen for an event delivered by an external client. The listening orchestration declares the name of the event and the shape of the data it expects to receive.
Isolated worker model
using Microsoft.Azure.Functions.Worker;
using Microsoft.DurableTask;
using Microsoft.Extensions.Logging;
public class BudgetApproval
{
private readonly ILogger _logger;
public BudgetApproval(ILoggerFactory loggerFactory)
{
_logger = loggerFactory.CreateLogger<BudgetApproval>();
}
[Function("BudgetApproval")]
public async Task Run(
[OrchestrationTrigger] TaskOrchestrationContext context)
{
bool approved = await context.WaitForExternalEventAsync<bool>("Approval");
if (approved)
{
// approval granted - do the approved action
}
else
{
// approval denied - send a notification
}
}
}
In-process model
[FunctionName("BudgetApproval")]
public static async Task Run(
[OrchestrationTrigger] IDurableOrchestrationContext context)
{
bool approved = await context.WaitForExternalEvent<bool>("Approval");
if (approved)
{
// approval granted - do the approved action
}
else
{
// approval denied - send a notification
}
}
Note
If you're using Durable Functions 1.x, use DurableOrchestrationContext
instead of IDurableOrchestrationContext
. Check out the [Durable Functions versions](../../azure-functions/durable-functions/durable-functions-versions) article for more version-specific details.
public class BudgetApproval : TaskOrchestrator<object?, bool>
{
public override async Task<bool> RunAsync(TaskOrchestrationContext context, object? input)
{
bool approved = await context.WaitForExternalEvent<bool>("Approval");
if (approved)
{
// approval granted - do the approved action
}
else
{
// approval denied - send a notification
}
return approved;
}
}
The preceding example listens for a specific single event and takes action when the event is received.
You can listen for multiple events concurrently, like in the following example, which waits for one of three possible event notifications.
Isolated worker model
[Function("Select")]
public async Task Run(
[OrchestrationTrigger] TaskOrchestrationContext context)
{
Task<float> event1 = context.WaitForExternalEventAsync<float>("Event1");
Task<bool> event2 = context.WaitForExternalEventAsync<bool>("Event2");
Task<int> event3 = context.WaitForExternalEventAsync<int>("Event3");
Task winner = await Task.WhenAny(event1, event2, event3);
if (winner == event1)
{
// ...
}
else if (winner == event2)
{
// ...
}
else if (winner == event3)
{
// ...
}
}
In-process model
[FunctionName("Select")]
public static async Task Run(
[OrchestrationTrigger] IDurableOrchestrationContext context)
{
var event1 = context.WaitForExternalEvent<float>("Event1");
var event2 = context.WaitForExternalEvent<bool>("Event2");
var event3 = context.WaitForExternalEvent<int>("Event3");
var winner = await Task.WhenAny(event1, event2, event3);
if (winner == event1)
{
// ...
}
else if (winner == event2)
{
// ...
}
else if (winner == event3)
{
// ...
}
}
Note
Using Durable Functions 1.x? Swap in DurableOrchestrationContext
instead of IDurableOrchestrationContext
. See the [Durable Functions versions](../../azure-functions/durable-functions/durable-functions-versions) article to learn about other version differences.
public class SelectOrchestrator : TaskOrchestrator<object?, object?>
{
public override async Task<object?> RunAsync(TaskOrchestrationContext context, object? input)
{
Task<float> event1 = context.WaitForExternalEvent<float>("Event1");
Task<bool> event2 = context.WaitForExternalEvent<bool>("Event2");
Task<int> event3 = context.WaitForExternalEvent<int>("Event3");
Task winner = await Task.WhenAny(event1, event2, event3);
if (winner == event1)
{
// ...
}
else if (winner == event2)
{
// ...
}
else if (winner == event3)
{
// ...
}
return null;
}
}
The previous example listens for any of multiple events. You can also wait for all events.
Isolated worker model
[Function("NewBuildingPermit")]
public async Task Run(
[OrchestrationTrigger] TaskOrchestrationContext context)
{
string applicationId = context.GetInput<string>();
Task gate1 = context.WaitForExternalEventAsync<object>("CityPlanningApproval");
Task gate2 = context.WaitForExternalEventAsync<object>("FireDeptApproval");
Task gate3 = context.WaitForExternalEventAsync<object>("BuildingDeptApproval");
// all three departments must grant approval before a permit can be issued
await Task.WhenAll(gate1, gate2, gate3);
await context.CallActivityAsync("IssueBuildingPermit", applicationId);
}
In-process model
[FunctionName("NewBuildingPermit")]
public static async Task Run(
[OrchestrationTrigger] IDurableOrchestrationContext context)
{
string applicationId = context.GetInput<string>();
var gate1 = context.WaitForExternalEvent("CityPlanningApproval");
var gate2 = context.WaitForExternalEvent("FireDeptApproval");
var gate3 = context.WaitForExternalEvent("BuildingDeptApproval");
// all three departments must grant approval before a permit can be issued
await Task.WhenAll(gate1, gate2, gate3);
await context.CallActivityAsync("IssueBuildingPermit", applicationId);
}
Note
If you're running Durable Functions 1.x, use DurableOrchestrationContext
instead of IDurableOrchestrationContext
. Head over to [Durable Functions versions](../../azure-functions/durable-functions/durable-functions-versions) for a full breakdown of version differences.
In .NET, if the event payload cannot be converted into the expected type T
, an exception is thrown.
public class NewBuildingPermit : TaskOrchestrator<string, object?>
{
public override async Task<object?> RunAsync(TaskOrchestrationContext context, string applicationId)
{
Task<object?> gate1 = context.WaitForExternalEvent<object?>("CityPlanningApproval");
Task<object?> gate2 = context.WaitForExternalEvent<object?>("FireDeptApproval");
Task<object?> gate3 = context.WaitForExternalEvent<object?>("BuildingDeptApproval");
// all three departments must grant approval before a permit can be issued
await Task.WhenAll(gate1, gate2, gate3);
await context.CallActivityAsync("IssueBuildingPermit", applicationId);
return null;
}
}
In .NET, if the event payload cannot be converted into the expected type T
, an exception is thrown.
The "wait-for-external-event" API waits indefinitely for some input. You can safely unload the function app while waiting. If and when an event arrives for this orchestration instance, the instance is awakened automatically and immediately processes the event.
Note
If your function app uses the Consumption Plan, no billing charges are incurred while an orchestrator function is awaiting an external event task, no matter how long it waits.
As with Activity Functions, external events have an at-least-once delivery guarantee. This means that, under certain conditions (like restarts, scaling, crashes, etc.), your application may receive duplicates of the same external event. Therefore, we recommend that external events contain some kind of ID that allows them to be manually de-duplicated in orchestrators.
The "wait-for-external-event" API waits indefinitely for some input. You can safely stop the worker while waiting. If and when an event arrives for this orchestration instance, it is awakened automatically and immediately processes the event.
External events have an at-least-once delivery guarantee. This means that, under certain conditions (like restarts, scaling, crashes, etc.), your application may receive duplicates of the same external event. Therefore, we recommend that external events contain some kind of ID that allows them to be manually de-duplicated in orchestrations.
Send events
You can use the "raise-event" API defined by the [orchestration client](../../azure-functions/durable-functions/durable-functions-bindings#orchestration-client) binding to send an external event to an orchestration. You can also use the built-in [raise event HTTP API](../../azure-functions/durable-functions/durable-functions-http-api#raise-event) to send an external event to an orchestration.
A raised event includes an instanceID
, an eventName
, and eventData
as parameters. Orchestrator functions handle these events using the [ wait-for-external-event](#wait-for-events) APIs. The
eventName
must match on both the sending and receiving ends in order for the event to be processed. The event data must also be JSON-serializable.Internally, the "raise-event" mechanisms enqueue a message that gets picked up by the waiting orchestrator function. If the instance isn't waiting on the specified event name, the event message is added to an in-memory queue. If the orchestration instance later begins listening for that event name, it checks the queue for event messages.
Note
If there's no orchestration instance with the specified instance ID, the event message is discarded.
Below is an example queue-triggered function that sends an "Approval" event to an orchestrator function instance. The orchestration instance ID comes from the body of the queue message.
You can use the "raise-event" API on the Durable Task client to send an external event to an orchestration.
A raised event includes an instance ID, an eventName, and eventData as parameters. Orchestrations handle these events using the ["wait-for-external-event"](#wait-for-events) APIs. The eventName must match on both the sending and receiving ends in order for the event to be processed. The event data must also be JSON-serializable.
Internally, the "raise-event" mechanisms enqueue a message that gets picked up by the waiting orchestration. If the instance is not waiting on the specified event name, the event message is added to an in-memory queue. If the orchestration instance later begins listening for that event name, it will check the queue for event messages.
Note
If there is no orchestration instance with the specified instanceID
, the event message is discarded.
Below is an example that sends an "Approval" event to an orchestration instance.
Isolated worker model
using Microsoft.Azure.Functions.Worker;
using Microsoft.DurableTask.Client;
public class ApprovalQueueProcessor
{
[Function("ApprovalQueueProcessor")]
public async Task Run(
[QueueTrigger("approval-queue")] string instanceId,
[DurableClient] DurableTaskClient client)
{
await client.RaiseEventAsync(instanceId, "Approval", true);
}
}
In-process model
[FunctionName("ApprovalQueueProcessor")]
public static async Task Run(
[QueueTrigger("approval-queue")] string instanceId,
[DurableClient] IDurableOrchestrationClient client)
{
await client.RaiseEventAsync(instanceId, "Approval", true);
}
Note
For Durable Functions 1.x, use the OrchestrationClient
attribute and DurableOrchestrationClient
parameter type instead. Check the [Durable Functions versions](../../azure-functions/durable-functions/durable-functions-versions) article for all version-specific changes.
Internally, the "raise-event" API enqueues a message that gets picked up by the waiting orchestrator function. If the instance isn't waiting on the specified event name, the event message is added to an in-memory buffer. If the orchestration instance later begins listening for that event name, it checks the buffer for event messages and triggers the task that was waiting for it.
Note
If there is no orchestration instance with the specified instance ID, the event message is discarded.
await client.RaiseEventAsync(instanceId, "Approval", true);
Internally, the "raise-event" API enqueues a message that gets picked up by the waiting orchestration. If the instance is not waiting on the specified event name, the event message is added to an in-memory buffer. If the orchestration instance later begins listening for that event name, it will check the buffer for event messages and trigger the task that was waiting for it.
Note
If there is no orchestration instance with the specified instance ID, the event message is discarded.
HTTP
The following is an example of an HTTP request that raises an Approval
event to an orchestration instance.
POST /runtime/webhooks/durabletask/instances/MyInstanceId/raiseEvent/Approval&code=XXX
Content-Type: application/json
"true"
In this case, the instance ID is hardcoded as MyInstanceId.
Best practices for external events
Keep the following best practices in mind when working with external events:
Use unique event names for deduplication
External events have an at-least-once delivery guarantee. Under certain rare conditions (which can occur during restarts, scaling, or crashes), your application might receive duplicates of the same external event. We recommend that external events contain a unique ID that allows them to be manually deduplicated in orchestrators.
Note
The [MSSQL storage provider](durable-task-storage-providers#mssql) consumes external events and updates orchestrator state transactionally, so there's no risk of duplicate events with that backend, unlike the [Azure Storage provider](durable-task-storage-providers#azure-storage). However, it's still recommended that external events have unique names so that code is portable across backends.