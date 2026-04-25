# Source: https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-timers
# Author: PatrickFarley
# Author Slug: patrickfarley
# Title: Azure Durable Functions — Timers (durable sleep/wait) and behavior
# Fetched via: trafilatura
# Date: 2026-04-10

Note
Access to this page requires authorization. You can try [signing in](#) or [changing directories].
Access to this page requires authorization. You can try [changing directories].
[Durable Functions](what-is-durable-task) provides durable timers for use in orchestrator functions to implement delays or to set up timeouts on async actions. Use durable timers in orchestrator functions instead of sleep
or delay
APIs that might be built into the language.
Durable Task SDKs provide durable timers for use in orchestrations to implement delays or to set up timeouts on async actions. Use durable timers in orchestrations instead of sleep
or delay
APIs that might be built into the language.
Important
Currently, the PowerShell Durable Task SDK isn't available.
Durable timers are tasks created using the appropriate create timer
API for the provided language, as shown in the following examples, and take either a due time or a duration as an argument.
// Put the orchestrator to sleep for 72 hours
DateTime dueTime = context.CurrentUtcDateTime.AddHours(72);
await context.CreateTimer(dueTime, CancellationToken.None);
// Put the orchestration to sleep for 72 hours
await context.CreateTimer(TimeSpan.FromHours(72), CancellationToken.None);
When you await
the timer task, the orchestrator function sleeps until the specified expiration time.
When you await
the timer task, the orchestration sleeps until the specified expiration time.
Note
Orchestrations continue to process other incoming events while waiting for a timer task to expire.
Timer limitations
When you create a timer that expires at 4:30 pm UTC, the underlying Durable Task Framework enqueues a message that becomes visible only at 4:30 PM UTC. If the function app is scaled down to zero instances in the meantime, the newly visible timer message ensures that the function app activates again on an appropriate VM.
Note
- For JavaScript, Python, and PowerShell apps, durable timers are limited to six days. To work around this limitation, use the timer APIs in a
while
loop to simulate a longer delay. Up-to-date .NET and Java apps support arbitrarily long timers. - Depending on the version of the SDK and
[storage provider](durable-task-storage-providers)being used, long timers of six days or more might be internally implemented using a series of shorter timers (for example, of three-day durations) until the desired expiration time is reached. This behavior is observable in the underlying data store but doesn't affect orchestration behavior. - Don't use built-in date/time APIs to get the current time. When calculating a future date for a timer to expire, always use the orchestrator function's current time API. For more information, see the
[orchestrator function code constraints](durable-task-code-constraints#dates-and-times)article.
When you create a timer that expires at 4:30 pm UTC, the underlying Durable Task Framework enqueues a message that becomes visible only at 4:30 PM UTC. The timer message ensures that the worker activates again when the timer expires.
Note
- Specifying a long delay (for example, a delay of a few days or more) might result in the creation of multiple, internally managed durable timers. The orchestration code doesn't need to be aware of this behavior. However, it might be visible in framework logs and the stored history state.
- Don't use built-in date and time APIs to get the current time. When calculating a future date for a timer to expire, always use the orchestration context's current time property (like
context.CurrentUtcDateTime
in .NET,ctx.current_utc_datetime
in Python, orctx.currentUtcDateTime
in JavaScript).
Usage for delays
The following example shows how to use durable timers to delay execution. The example issues a billing notification every day for 10 days.
[FunctionName("BillingIssuer")]
public static async Task Run(
[OrchestrationTrigger] IDurableOrchestrationContext context)
{
for (int i = 0; i < 10; i++)
{
DateTime deadline = context.CurrentUtcDateTime.Add(TimeSpan.FromDays(1));
await context.CreateTimer(deadline, CancellationToken.None);
await context.CallActivityAsync("SendBillingEvent");
}
}
Note
The preceding C# example targets Durable Functions 2.x. For Durable Functions 1.x, use DurableOrchestrationContext
instead of IDurableOrchestrationContext
. For more information about the differences between versions, see the [Durable Functions versions](../../azure-functions/durable-functions/durable-functions-versions) article.
public class BillingIssuer : TaskOrchestrator<object?, string>
{
public override async Task<string> RunAsync(TaskOrchestrationContext context, object? input)
{
for (int i = 0; i < 10; i++)
{
await context.CreateTimer(TimeSpan.FromDays(1), CancellationToken.None);
await context.CallActivityAsync("SendBillingEvent");
}
return "done";
}
}
Warning
Avoid infinite loops in orchestrator functions. For information about how to safely and efficiently implement infinite loop scenarios, see [Eternal orchestrations](durable-task-eternal-orchestrations).
Warning
Avoid infinite loops in orchestrations. For information about how to safely and efficiently implement infinite loop scenarios, see [Eternal orchestrations](durable-task-eternal-orchestrations).
Usage for timeouts
This example shows how to use durable timers to implement timeouts:
[FunctionName("TryGetQuote")]
public static async Task<bool> Run(
[OrchestrationTrigger] IDurableOrchestrationContext context)
{
TimeSpan timeout = TimeSpan.FromSeconds(30);
DateTime deadline = context.CurrentUtcDateTime.Add(timeout);
using (var cts = new CancellationTokenSource())
{
Task activityTask = context.CallActivityAsync("GetQuote");
Task timeoutTask = context.CreateTimer(deadline, cts.Token);
Task winner = await Task.WhenAny(activityTask, timeoutTask);
if (winner == activityTask)
{
// success case
cts.Cancel();
return true;
}
else
{
// timeout case
return false;
}
}
}
Note
The previous C# example targets Durable Functions 2.x. For Durable Functions 1.x, use DurableOrchestrationContext
instead of IDurableOrchestrationContext
. For more information about the differences between versions, see the [Durable Functions versions](../../azure-functions/durable-functions/durable-functions-versions) article.
public class TryGetQuote : TaskOrchestrator<object?, bool>
{
public override async Task<bool> RunAsync(TaskOrchestrationContext context, object? input)
{
using var cts = new CancellationTokenSource();
Task<double> activityTask = context.CallActivityAsync<double>("GetQuote");
Task timeoutTask = context.CreateTimer(TimeSpan.FromSeconds(30), cts.Token);
Task winner = await Task.WhenAny(activityTask, timeoutTask);
if (winner == activityTask)
{
// success case
cts.Cancel();
return true;
}
else
{
// timeout case
return false;
}
}
}
Warning
In .NET, JavaScript, Python, and PowerShell, cancel any created durable timers if your code doesn't wait for them to complete. See the previous examples for how to cancel pending timers. The Durable Task Framework doesn't change an orchestration's status to "Completed" until all outstanding tasks, including durable timer tasks, are either completed or canceled.
Warning
If your SDK supports timer cancellation (for example, .NET), cancel any created durable timers if your code doesn't wait for them to complete. See the previous examples for how to cancel pending timers. The Durable Task Framework doesn't change an orchestration's status to "Completed" until all outstanding tasks, including durable timer tasks, are either completed or canceled.
This cancellation mechanism using the when-any pattern doesn't terminate in-progress activity function or sub-orchestration executions. Rather, it simply lets the orchestrator function ignore the result and move on. If your function app uses the Consumption plan, you're still billed for any time and memory the abandoned activity function consumes. By default, functions running in the Consumption plan have a timeout of five minutes. If this limit is exceeded, the Azure Functions host recycles to stop all execution and prevent a runaway billing situation. The [function timeout is configurable](../../azure-functions/functions-host-json#functiontimeout).
For a more detailed example of how to implement timeouts in orchestrator functions, see the [Human interaction](durable-task-human-interaction) article.
This cancellation mechanism using the when-any pattern doesn't terminate in-progress activity or sub-orchestration executions. Rather, it simply lets the orchestration ignore the result and move on.