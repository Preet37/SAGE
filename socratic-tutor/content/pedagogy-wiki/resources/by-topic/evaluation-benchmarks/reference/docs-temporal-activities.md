# Source: https://docs.temporal.io/activities#activity-retries
# Title: Temporal Docs — Activity retries (RetryPolicy fields, defaults, backoff behavior)
# Fetched via: search
# Date: 2026-04-10

A Retry Policy is a collection of settings that tells Temporal how and when to try again after something fails in a Workflow Execution or Activity Task Execution.

## Overview​

Temporal's default behavior is to automatically retry an Activity that fails, so transient or intermittent failures require no action on your part. This behavior is defined by the Retry Policy.

A Retry Policy is declarative. You do not need to implement your own logic for handling the retries; you only need to specify the desired behavior and Temporal will provide it.
In contrast to the Activities it contains, a Workflow Execution itself is not associated with a Retry Policy by default. This may seem counterintuitive, but Workflows and Activities perform different roles. Activities are intended for operations that may fail, so having a default Retry Policy increases the likelihood that they will ultimately complete successfully, even if the initial attempt failed. On the other hand, Workflows must be deterministic and are not intended to perform failure-prone operations. While it is possible to assign a Retry Policy to a Workflow Execution, this is not the default and it is uncommon to do so.
Retry Policies do not apply to Workflow Task Executions, which retry until the Workflow Execution Timeout (which is unlimited by default) with an exponential backoff and a max interval of 10 minutes. A Retry Policy instructs the Temporal Service how to retry a failure of either a Workflow Execution or an Activity Task Execution.

Try out the Activity retry simulator to visualize how a Retry Policy works.

## Default behavior​

Activities in Temporal are associated with a Retry Policy by default, while Workflows are not. The Temporal SDK provides a Retry Policy instance with default behavior. While this object is not specific to either a Workflow or Activity, you'll use different methods to apply it to the execution of each.

This section details the default retry behavior for both Activities and Workflows to provide context for any further customization.

### Activity Execution​

Temporal's default behavior is to automatically retry an Activity, with a short delay between each attempt that increases exponentially, until it either succeeds or is canceled. When a subsequent request succeeds, your Workflow code will resume as if the failure never occurred.

When an Activity Task Execution is retried, the Temporal Service places a new Activity Task into its respective Activity Task Queue, which results in a new Activity Task Execution.
The default Retry Policy uses exponential backoff with a 2.0 backoff coefficient, starting with a 1-second initial interval and capping at a maximum interval of 100 seconds. By default, the maximum attempt of retries are set to zero which is evaluated as unlimited and non-retryable errors default to none. For detailed information about all Retry Policy attributes and their default values, see the Properties section.

### Workflow Execution​

Unlike Activities, Workflow Executions do not retry by default. When a Workflow Execution is spawned, it is not associated with a default Retry Policy and thus does not retry by default.

Temporal provides guidance around idempotence of Activity code with the expectation that Activities will need to re-execute upon failure; this is not typically true of Workflows. In most use cases, a Workflow failure would indicate an issue with the design or deployment of your application; for example, a permanent failure that may require different input data.
Retrying an entire Workflow Execution is not recommended due to Temporal's deterministic design. Since Workflows replay the same sequence of events to reach the same state, retrying the whole workflow would repeat the same logic without resolving the underlying issue that caused the failure. This repetition does not address problems related to external dependencies or unchanged conditions and can lead to unnecessary resource consumption and higher costs.
Instead, it's more efficient to retry only the failed Activities. This approach targets specific points of failure, allowing the workflow to progress without redundant operations, thereby saving on resources and ensuring a more focused and effective error recovery process. If you need to retry parts of your Workflow Definition, we recommend you implement this in your Workflow code.

## Custom Retry Policy​

To use a custom Retry Policy, provide it as an options parameter when starting a Workflow Execution or Activity Execution. Only certain scenarios merit starting a Workflow Execution with a custom Retry Policy, such as the following:

- A Temporal Cron Job or some other stateless, always-running Workflow Execution that can benefit from retries.
- A file-processing or media-encoding Workflow Execution that downloads files to a host.

## Properties​

### Default values for Retry Policy​

```
Initial Interval = 1 second
Backoff Coefficient = 2.0
Maximum Interval = 100 × Initial Interval
Maximum Attempts = ∞
Non-Retryable Errors = []

```

### Initial Interval​
- **Description:** Amount of time that must elapse before the first retry occurs. - **The default value is 1 second.**

- **Use case:** This is used as the base interval time for the Backoff Coefficient to multiply against.

### Backoff Coefficient​
- **Description:** The value dictates how much the*retry interval* increases. - **The default value is 2.0.**
 - A backoff coefficient of 1.0 means that the retry interval always equals the Initial Interval.

- **Use case:** Use this attribute to increase the interval between retries. By having a backoff coefficient greater than 1.0, the first few retries happen relatively quickly to overcome intermittent failures, but subsequent retries happen farther and farther apart to account for longer outages. Use the Maximum Interval attribute to prevent the coefficient from increasing the retry interval too much.

### Maximum Interval​
- **Description:** Specifies the maximum interval between retries. - **The default value is 100 times the Initial Interval.**

- **Use case:** This attribute is useful for Backoff Coefficients that are greater than 1.0 because it prevents the retry interval from growing infinitely.

### Maximum Attempts​
- **Description:** Specifies the maximum number of execution attempts that can be made in the presence of failures. - **The default is unlimited.**
 - If this limit is exceeded, the execution fails without retrying again. When this happens an error is returned.
 - Setting the value to 0 also means unlimited.
 - Setting the value to 1 means a single execution attempt and no retries.
- Setting the value to a negative integer results in an error when the execution is invoked.

- **Use case:** Use this attribute to ensure that retries do not continue indefinitely. In most cases, we recommend using the Workflow Execution Timeout for Workflows or the Schedule-To-Close Timeout for Activities to limit the total duration of retries, rather than using this attribute.

### Non-Retryable Errors​

Non-Retryable Errors specify errors that shouldn't be retried. By default, none are specified. Errors are matched
against the

…

field of the Application Failure. If one of those errors
occurs, a retry does not occur. If you know of errors that should not trigger a retry, you can specify that and if they
occur, the execution is not retried.

#### Non-Retryable Errors for Activities​

When writing software applications, you will encounter three types of failures: transient, intermittent, and permanent. While transient and intermittent failures may resolve themselves upon retrying without further intervention, permanent failures will not. Permanent failures, by definition, require you to make some change to your logic or your input. Therefore, it is better to surface them than to retry them.
Non-Retryable Errors are errors that will not be retried, regardless of a Retry Policy.

- Ruby
- Python
- TypeScript
- Java
- Go
- .NET

To raise a non-retryable error, specify the
```
non_retryable
```

…

This will designate the

…

as non-retryable.
To raise a non-retryable error, specify the
```
non_retryable
```

…

as non-retryable.
To throw a non-retryable error, add

…

This will designate the Error as non-retryable.

To throw a non-retryable error, use the

…

as non-retryable.
To return a non-retryable error, replace your call to

…

This will designate the Error as non-retryable.

To throw a non-retryable error, specify the

…

```
var attempt = ActivityExecutionContext.Current.Info.Attempt;

throw new ApplicationFailureException(
 $"Something bad happened on attempt {attempt}",
 errorType: "my_failure_type",
 nonRetryable: true
);

```

…

as non-retryable.
Use non-retryable errors in your code sparingly.

- Ruby
- Python
- TypeScript
- Java
- Go
- .NET

If you do not specify the failure as non-retryable within the definition, you can always mark that error type as
non-retryable in your Activity's Retry Policy, but an

…

will always be non-retryable.
If you do not specify the failure as non-retryable within the definition, you can always mark that error type as
non-retryable in your Activity's Retry Policy, but an

…

will always be non-retryable.
If you do not specify the failure as non-retryable within the definition, you can always mark that error type as
non-retryable in your Activity's Retry Policy, but an error with

…

set will always be non-retryable.
If you throw a regular

…

, you can always mark that error *type* as non-retryable in your Activity's Retry Policy, but a

…

will always be non-retryable.
If you return a regular

…

, you can always mark that error *type* as non-retryable in your Activity's Retry Policy, but a

…

will always be non-retryable.
If you do not specify the failure as non-retryable within the definition, you can always mark that error type as
non-retryable in your Activity's Retry Policy, but an

…

will always be non-retryable.
For example, checking for bad input data is a reasonable time to use a non-retryable error. If the Activity cannot proceed with the input it has, that error should be surfaced immediately so that the input can be corrected on the next attempt.
If responsibility for your application is distributed across multiple maintainers, or if you are developing a library to integrate into somebody else's application, you can think of the decision to hardcode non-retryable errors as following a "caller vs. implementer" dichotomy. Anyone who is calling your Activity would be able to make decisions about their Retry Policy, but only the implementer can decide whether an error should never be retryable out of the box.

## Retry interval​

The wait time before a retry is the *retry interval*. A retry interval is the smaller of two values:

- The Initial Interval multiplied by the Backoff Coefficient raised to the power of the number of retries.
- The Maximum Interval.

Diagram that shows the retry interval and its formula

### Per-error next Retry delay​

Sometimes, your Activity or Workflow raises a special exception that needs a different retry interval from the Retry Policy. To accomplish this, you may throw an Application Failure with the next Retry delay field set. This value will replace and override whatever the retry interval would be on the Retry Policy. Note that your retries will still cap out under the Retry Policy's Maximum Attempts, as well as overall timeouts. For an Activity, its Schedule-to-Close Timeout applies. For a Workflow, the Execution Timeout applies.

## Event History​

There are some subtle nuances to how Events are recorded to an Event History when a Retry Policy comes into play.

- For an Activity Execution, the ActivityTaskStarted Event will not show up in the Workflow Execution Event History until the Activity Execution has completed or failed (having exhausted all retries). This is to avoid filling the Event History with noise. Use the Describe API to get a pending Activity Execution's attempt count.
- When a Workflow fails and has a Retry Policy, the failed run ends with

…

set, and the Temporal Service starts a new Workflow Execution. The new Workflow Execution is created immediately, but the first Workflow Task won’t be scheduled until the backoff duration is exhausted. That duration is recorded as the

div
Hi!
...
For a single wf, you can lookg at the web-ui summary page for a particular workflow.
Information under “Pending Activities” includes the activity type, retry attempt count, as well as the last failure info.
same with tctl “desctribe” command, for example:
`tctl wf desc -w <my_workflow_id>`
Note that you can get the retry attempt inside your activity code as well, for example using Java SDK:
`Activity.getExecutionContext().getInfo().getAttempt();`
For all workflows in a namespace, you can use the sdk client api to get all workflows who have pending activities with retries > X, for example:
```
private static void getActivitiesWithRetriesOver(int retryCount) {
ListOpenWorkflowExecutionsRequest listOpenWorkflowExecutionsRequest =
ListOpenWorkflowExecutionsRequest.newBuilder()
.setNamespace(client.getOptions().getNamespace())
.build();
ListOpenWorkflowExecutionsResponse listOpenWorkflowExecutionsResponse =
service.blockingStub().listOpenWorkflowExecutions(listOpenWorkflowExecutionsRequest);
for(WorkflowExecutionInfo info : listOpenWorkflowExecutionsResponse.getExecutionsList()) {
DescribeWorkflowExecutionRequest describeWorkflowExecutionRequest =
DescribeWorkflowExecutionRequest.newBuilder()
.setNamespace(client.getOptions().getNamespace())
.setExecution(info.getExecution()).build();
DescribeWorkflowExecutionResponse describeWorkflowExecutionResponse =
service.blockingStub().describeWorkflowExecution(describeWorkflowExecutionRequest);
for(PendingActivityInfo activityInfo : describeWorkflowExecutionResponse.getPendingActivitiesList()) {
if(activityInfo.getAttempt() > retryCount) {
System.out.println("Activity Type: " + activityInfo.getActivityType());
System.out.println("Activity attempt: " + activityInfo.getAttempt());
System.out.println("Last failure message : " + activityInfo.getLastFailure().getMessage());
// ...
}
}
}
}
```
Yes you should rely on timeouts rather than RetryOptions->maximumAttempts.
By default your retries will happen up to the activity ScheduleToCloseTimeout, if defined, if it’s not defined, they can retry up to the workflow run/execution timeout.
If that is also not defined, then the retries are “unlimited”.
You can control what types of failures cause retries or not as well.
You specify which failures should not cause retries by adding them in `ActivityOptions->RetryOptions->DoNotRetry`.
For example if you do not want your activity to retry on IllegalArgumentException:
```
ActivityOptions.newBuilder()
.setRetryOptions(RetryOptions.newBuilder()
.setDoNotRetry(IllegalArgumentException.class.getName())
.build())
.build());
```
Another option is to throw a non retryable application failure inside your activity, created via ApplicationFailure.newNonRetryableFailure.
With that, along with ability to get the retry attempt inside activity code, you could, depending on your business logic control at what point retries should stop, and can perform compensation logic inside your workflow or whatever you need to do.
Having automatic retries in the end is super helpful, as you can change your activity method code, and its activity options (and restart worker) to fix errors without breaking workflow determinism.
...
openWorkflows, err := client.ListOpenWorkflow(context.Background(), &workflowservice.ListOpenWorkflowExecutionsRequest{
Namespace: "default",
})
if err != nil {
log.Fatalln("fail to list open workflows", err)
}
for _, openWorkflow := range openWorkflows.GetExecutions() {
describe, err := client.DescribeWorkflowExecution(context.Background(), openWorkflow.Execution.WorkflowId, openWorkflow.Execution.RunId)
if err != nil {
log.Fatalln("fail to descibe workflow", err)
}
for _, pendingActivity := range describe.GetPendingActivities() {
log.Println(pendingActivity.GetAttempt(), pendingActivity.GetActivityType().Name, pendingActivity.GetLastFailure().Message)
}
}
```
Nice!
Much less verbose indeed
...
in typescript you have `client.workflowService.describeWorkflowExecution` that return a `DescribeWorkflowExecutionResponse` that contains pendingActivities.
For each pending activity you can get `attempt`
Antonio
This seems to make a separate request for each workflow - at what point does this become a problem/hit rate limits?

## CodeTime
...
retry logic is a critical aspect of building resilient and fault-tolerant applications, especially in distributed systems like those built with temporal.
when an activity fails, retrying it automatically can significantly improve the application's reliability and reduce the need for manual intervention.
this tutorial will delve into retry logic within temporal activities, covering various aspects, strategies, and code examples to guide you in implementing effective retry mechanisms.
**why retry logic matters for activities**
activities in temporal represent units of work that are executed outside the workflow.
these activities might involve interacting with external systems, databases, apis, or any other resource that can be prone to temporary failures.
potential causes of activity failures include:
*   **network issues:** intermittent network connectivity problems.
*   **resource unavailability:** database or api services being temporarily overloaded or down.
*   **transient errors:** temporary glitches in external systems, like rate limiting or concurrency issues.
*   **temporary service outages:** scheduled maintenance or unplanned downtime of external services.
without proper retry logic, a single activity failure can bring down your entire workflow execution, requiring manual restarts and causing delays.
retry policies address these problems by automatically attempting to re-execute the activity a defined number of times with specific intervals until it succeeds or the maximum retry attempts are exhausted.
**key concepts and terminology**
*   **retry policy:** defines the rules for retrying an activity, including the number of attempts, the delay between retries, and conditions for giving up.
*   **initial interval:** the duration of the first retry attempt delay.
*   **backoff coefficient:** a multiplier applied to the initial interval to increase the delay with each retry attempt (e.g., expo ...
…
### Transcript
{ts:0} download this code from codeg.com link in the description below Retry logic in temporal activities A comprehensive tutorial Retry logic is a critical aspect of building resilient and fault tolerant applications especially in distributed systems like those built with temporal When an activity fails retrying it automatically can significantly improve the application's reliability and reduce the need for manual intervention This tutorial will delve into retry logic within temporal activities covering various aspects strategies and code examples to guide you in implementing effective retry mechanisms Why retry logic matters for activities
{ts:48} activities in temporal represent units of work that are executed outside the workflow These activities might involve interacting with external systems databases APIs or any other resource that can be prone to temporary failures Potential causes of activity failures include asterisk network issues asterisk intermittent network connectivity problems asterisk resource unavailability asterisk database or API services being temporarily overloaded or down asterisk transient errors asterisk temporary glitches in external systems like rate limiting or concurrency issues asterisk temporary service outages asterisk scheduled maintenance or unplanned downtime of external services Without proper retry logic a single activity failure can bring down
your entire workflow execution requiring {ts:107} manual restarts and causing delays Retry policies address these problems by automatically attempting to reexecute the activity a defined number of times with specific intervals until it succeeds or the maximum retry attempts are exhausted Key concepts and terminology Asterisk retry policy Asterisk defines the rules for retrying an activity including the number of attempts the delay between retries and conditions for giving up Asterisk initial interval Asterisk the duration of the first retry attempt Delay Asterisk back off coefficient Asterisk a multiplier applied to the initial interval to increase the delay with each retry attempt Example exponential back
off asterisk maximum interval asterisk the upper limit for the retry interval {ts:160} The delay won't exceed this value Asterisk maximum attempts asterisk the total number of times the activity will be retried Asterisk non-retable errors Asterisk specific error types that are considered unreoverable and should cause the activity to fail immediately without retries Example invalid input parameters business logic errors Implementing retry logic in temporal activities Go Example Let's explore how to implement retry logic in temporal activities using the Go SDK one Defining a retry policy asterisk asterisk The activity Retry options structure in the temporal Go SDK allows
you to configure the retry behavior for your activities Two configuring the retry {ts:213} policy in the workflow asterisk asterisk Now within your workflow definition you specify the retry options when invoking the activity using workflow.execute Execute activity explanation asterisk asterisk retry options asterisk we create a activity retry options strct to define our retry policy asterisk initial interval set to 1 second the first retry will occur after this delay asterisk backoff coefficient set to 2.0 zero The retry interval will double with each subsequent attempt So the delays will be 1 second 2 seconds 4 seconds Asterisk maximum interval set to
5 seconds The retry interval won't exceed this value So in the example above after three retries the delay will be capped at 5 {ts:273} seconds Asterisk maximum attempts set to five The activity will be retrieded a maximum of five times Asterisk activity options asterisk the retry options are embedded inside activity options The activity options are associated with the workflow context using workflow dot with activity options This ensures that the defined retry policy is applied to the specific activity call Start to close timeout is also defined in activity options asterisk workflow.execute execute activity asterisk the activity
…
signal to temporal that the activity should not be retrieded and the workflow should proceed with error handling To create a non-retriable error use the activity new non-retriable error function In the example activity above when the input is invalid non-retable activity returns a non-retable error the workflow will immediately fail and the activity will not be
retried Four important considerations and best practices Asterisk item potency Asterisk ensure your activities are item potent meaning that executing them multiple times with the same input produces the {ts:382} same result as executing them once This is crucial because retries can potentially lead to an activity being executed more than once Design your activities to handle this scenario gracefully This often involves checking the state of external systems before performing an action Asterisk logging asterisk log important information about activity executions and retries including the retry attempts error messages and timestamps This aids in debugging and monitoring Use activity.get logger ctx
to get a logger instance preconfigured for the current activity execution Asterisk deadlines and timeouts asterisk define appropriate timeouts for your activities Even with retry logic it's essential to have a limit on how long an {ts:437} activity can take Start to close timeout in the activity options is crucial for this Consider using schedule to start timeout as well if you want to limit the time an activity spends in the queue before starting Also be aware of the total workflow execution timeout If the combined execution time of all activities including retries exceeds the workflow timeout the workflow will fail Asterisk context propagation asterisk Make sure to pass the context.context
context properly to your activities The context contains important information about the workflow execution including deadlines and cancellation signals Use activity.get logger ctx to get the activity logger from the context Asterisk selective retries asterisk {ts:494} avoid retrying activities that perform irreversible actions unless you have a robust mechanism to handle potential side effects Carefully consider whether a retry makes sense for each type of activity and error Asterisk monitoring and alerting asterisk implement monitoring to track activity failures and retry attempts Set up alerts to notify you when activities are failing frequently or
when retries are exceeding certain thresholds This enables proactive identification and resolution of potential problems Complete example workflow plus activity plus test Here's a complete example demonstrating retry logic including a workflow an activity and a simple test {ts:543} One activities/activities.gois asterisk same as the activity code defined earlier Two workflows/workflows.go asterisk asterisk same as the workflow code defined earlier Three main.gois asterisk worker and client setup Four workflow_est.go Go asterisk asterisk How to run the example asterisk one Install temporal CLI
asterisk follow instructions at https/docs.temporal.io/i/install https/docs.temporal.io/i/install io/ CLI/install Two start temporal server asterisk temporal server start Three run the worker asterisk go run main.go Four start the workflow asterisk in a separate terminal Set the environment variable start_workflow {ts:608}
equals true and rerun the main.go file Start underscoreworkflow equals true Go run main.go Key takeaways from this complete example Asterisk asterisk a clear separation of activity and workflow logic Asterisk using the temporal go SDK activity Retry options to configure retry behavior Asterisk a practical main.go to run both the worker and trigger a
workflow execution Asterisk a testing example that demonstrates how to mock activities and verify retry behavior or the absence of it in the case of non-retriable error Asterisk demonstration of non-retriable error Conclusion Implementing effective retry logic is crucial for building resilient temporal applications by using the activity retry {ts:663} options understanding non-retriable errors and considering the important considerations outlined above you can improve the reliability and robustness of your workflows and handle transient failures gracefully This comprehensive guide provides you with the knowledge and tools to confidently implement retry

## Documentation ¶

### Overview ¶

Package activity contains functions and types used to implement Temporal Activities.

An Activity is an implementation of a task to be performed as part of a larger Workflow. There is no limitation of
what an Activity can do. In the context of a Workflow, it is in the Activities where all operations that affect the
desired results must be implemented.

#### Overview ¶

Temporal Go SDK does all the heavy lifting of handling the async communication between the Temporal
managed service and the Worker running the Activity. As such, the implementation of the Activity can, for the most
part, focus on the business logic. The sample code below shows the implementation of a simple Activity that accepts a
string parameter, appends a word to it and then returns the result.
```
import (
	"context"

	"go.temporal.io/sdk/activity"
)

func SimpleActivity(ctx context.Context, value string) (string, error) {
	activity.GetLogger(ctx).Info("SimpleActivity called.", "Value", value)
	return "Processed: ” + value, nil
}

```

…

#### Declaration ¶

In the Temporal programing model, an Activity is implemented with a function. The function declaration specifies the
parameters the Activity accepts as well as any values it might return. An Activity function can take zero or many
Activity specific parameters and can return one or two values. It must always at least return an error value. The
Activity function can accept as parameters and return as results any serializable type.
```
func SimpleActivity(ctx context.Context, value string) (string, error)

```
The first parameter to the function is context.Context. This is an optional parameter and can be omitted. This
parameter is the standard Go context.

The second string parameter is a custom Activity-specific parameter that can be used to pass in data into the Activity
on start. An Activity can have one or more such parameters. All parameters to an Activity function must be
serializable, which essentially means that params can’t be channels, functions, variadic, or unsafe pointer.
The Activity declares two return values: (string, error). The string return value is used to return the result of the
Activity. The error return value is used to indicate an error was encountered during execution.

…

#### Context Cancellation ¶

The first parameter to an activity function can be an optional context.Context. The context will be cancelled when:
* The activity function returns.
* The context deadline is exceeded. The deadline is calculated based on the minimum of the ScheduleToClose timeout plus
the activity task scheduled time and the StartToClose timeout plus the activity task start time.
* The activity calls RecordHeartbeat after being cancelled by the Temporal server.

…

#### Activity Heartbeating ¶

For long running Activities, Temporal provides an API for the Activity code to report both liveness and progress back to
the Temporal managed service.
```
progress := 0
for hasWork {
    // send heartbeat message to the server
    activity.RecordHeartbeat(ctx, progress)
    // do some work
    ...
    progress++
}

```
When the Activity times out due to a missed heartbeat, the last value of the details (progress in the above sample) is
returned from the go.temporal.io/sdk/workflow.ExecuteActivity function as the details field of go.temporal.io/sdk/temporal.TimeoutError with TimeoutType_HEARTBEAT.

It is also possible to heartbeat an Activity from an external source:
```
// instantiate a Temporal service Client
client.Client client = client.Dial(...)

// record heartbeat
err := client.RecordActivityHeartbeat(ctx, taskToken, details)

```
It expects an additional parameter, "taskToken", which is the value of the binary "TaskToken" field of the
activity.Info retrieved inside the Activity (GetActivityInfo(ctx).TaskToken). "details" is the serializable payload containing progress information.

#### Activity Cancellation ¶

When an Activity is canceled (or its Workflow execution is completed or failed) the context passed into its function
is canceled which sets its Done channel’s closed state. So an Activity can use that to perform any necessary cleanup
and abort its execution. Currently cancellation is delivered only to Activities that call RecordHeartbeat.

#### Async/Manual Activity Completion ¶

In certain scenarios completing an Activity upon completion of its function is not possible or desirable.

One example would be the UberEATS order processing Workflow that gets kicked off once an eater pushes the “Place Order”
button. Here is how that Workflow could be implemented using Temporal and the “async Activity completion”:

- Activity 1: send order to restaurant
- Activity 2: wait for restaurant to accept order
- Activity 3: schedule pickup of order
- Activity 4: wait for courier to pick up order
- Activity 5: send driver location updates to eater
- Activity 6: complete order
Activities 2 & 4 in the above flow require someone in the restaurant to push a button in the Uber app to complete the
Activity. The Activities could be implemented with some sort of polling mechanism. However, they can be implemented
much simpler and much less resource intensive as a Temporal Activity that is completed asynchronously.
There are 2 parts to implementing an asynchronously completed Activity. The first part is for the Activity to provide
the information necessary to be able to be completed from an external system and notify the Temporal service that it is
waiting for that outside callback:
```
// retrieve Activity information needed to complete Activity asynchronously
activityInfo := activity.GetInfo(ctx)
taskToken := activityInfo.TaskToken

// send the taskToken to external service that will complete the Activity
...

// return from Activity function indicating the Temporal should wait for an async completion message
return "", activity.ErrResultPending

```

…

```
// instantiate a Temporal service Client
// the same client can be used complete or fail any number of Activities
client.Client client = client.NewClient(...)

// complete the Activity
client.CompleteActivity(taskToken, result, nil)

```

…

```
// fail the Activity
client.CompleteActivity(taskToken, nil, err)

```
The parameters of the CompleteActivity function are:

- taskToken: This is the value of the binary “TaskToken” field of the
  “ActivityInfo” struct retrieved inside the Activity.
- result: This is the return value that should be recorded for the Activity.
  The type of this value needs to match the type of the return value
  declared by the Activity function.
- err: The error code to return if the Activity should terminate with an
  error.
If error is not null the value of the result field is ignored.

For a full example of implementing this pattern see the Expense sample.

…

```
c, err := client.Dial(client.Options{})
if err != nil {
  log.Fatalln("unable to create Temporal client", err)
}
defer c.Close()
w := worker.New(c, "SomeTaskQueue", worker.Options{})
w.RegisterActivity(SomeActivityFunction)

```

…

### Index ¶
- Variables
- func GetClient(ctx context.Context) internal.Client
- func GetHeartbeatDetails(ctx context.Context, d ...interface{}) error
- func GetLogger(ctx context.Context) log.Logger
- func GetMetricsHandler(ctx context.Context) metrics.Handler
- func GetWorkerStopChannel(ctx context.Context) <-chan struct{}
- func HasHeartbeatDetails(ctx context.Context) bool
- func IsActivity(ctx context.Context) bool
- func RecordHeartbeat(ctx context.Context, details ...interface{})
- type DynamicRegisterOptions
- type Info
  - func GetInfo(ctx context.Context) Info
- type RegisterOptions
- type Type

…

ErrActivityPaused is returned from an activity heartbeat or the cause of an activity's context to indicate that the activity is paused.

WARNING: Activity pause is currently experimental

View Source
```
var ErrActivityReset = internal.ErrActivityReset
```
ErrActivityReset is returned from an activity heartbeat or the cause of an activity's context to indicate that the activity has been reset.

WARNING: Activity reset is currently experimental

View Source

…

GetHeartbeatDetails extracts heartbeat details from the last failed attempt. This is used in combination with the retry policy.
An activity could be scheduled with an optional retry policy on ActivityOptions. If the activity failed, then server
would attempt to dispatch another activity task to retry according to the retry policy. If there were heartbeat
details reported by activity from the failed attempt, the details would be delivered along with the activity task for
the retry attempt. An activity can extract the details from GetHeartbeatDetails() and resume progress from there.
See TestActivityEnvironment.SetHeartbeatDetails() for unit test support.

…

GetWorkerStopChannel returns a read-only channel. The closure of this channel indicates the activity worker is stopping.
When the worker is stopping, it will close this channel and wait until the worker stop timeout finishes. After the timeout
hits, the worker will cancel the activity context and then exit. The timeout can be defined by worker option: WorkerStopTimeout.
Use this channel to handle a graceful activity exit when the activity worker stops.

…

RecordHeartbeat sends a heartbeat for the currently executing activity.
If the activity is either canceled or the workflow/activity doesn't exist, then we would cancel
the context with error context.Canceled. The context.Cause will be set based on the reason for the cancellation.

For example, if the activity is requested to be paused by the Server:
```
	func MyActivity(ctx context.Context) error {
		activity.RecordHeartbeat(ctx, "")
		// assume the activity is paused by the server
		activity.RecordHeartbeat(ctx, "some details")
		context.Cause(ctx) // Will return activity.ErrActivityPaused
     	return ctx.Err() // Will return context.Canceled
	}

```

# ​ Activities
Activities are the mechanism in Temporal for executing non-deterministic operations or side effects like API calls, database operations, or file I/O.
Unlike workflow code which must be deterministic, activity code can interact with the outside world.
## ​ Activity Execution Model
Activities are scheduled by workflow code and executed by workers.
The History Service orchestrates the activity lifecycle through events and task queues.
### ​ Activity Scheduling Flow
## ​ Activity State Machine
The History Service tracks activity state in Mutable State:
1
Scheduled
Activity task created but not yet picked up by a worker.
The `ActivityTaskScheduled` event is written to history.
2
Started
Worker has picked up the task and begun execution.
The `ActivityTaskStarted` event records which worker and when.
3
Completed / Failed / Timed Out / Canceled
Activity reaches terminal state.
Result or failure is recorded in corresponding event.
```
// From service/history/workflow/activity.go
func GetActivityState(ai *persistencespb.ActivityInfo) enumspb.PendingActivityState {
if ai.CancelRequested {
return enumspb.PENDING_ACTIVITY_STATE_CANCEL_REQUESTED
}
if ai.StartedEventId != common.EmptyEventID {
return enumspb.PENDING_ACTIVITY_STATE_STARTED
}
return enumspb.PENDING_ACTIVITY_STATE_SCHEDULED
}
```
## ​ Activity Info
The server maintains rich metadata for each activity in `ActivityInfo`:
ActivityInfo Structure
```
type ActivityInfo struct {
ScheduledEventId int64 // Event ID when activity was scheduled
StartedEventId int64 // Event ID when activity started (or empty)
ActivityId string // User-provided activity ID
RequestId string // Unique request ID for deduplication
ScheduledTime *timestamp // When activity was scheduled
StartedTime *timestamp // When worker picked up task
TaskQueue string // Which task queue to dispatch to
ActivityType string // Activity function name
// Retry state
Attempt int32
RetryLastFailure *Failure
RetryLastWorkerIdentity string
// Heartbeat tracking
LastHeartbeatUpdateTime *timestamp
LastHeartbeatDetails *Payloads
// Timeout configuration
ScheduleToStartTimeout time.Duration
ScheduleToCloseTimeout time.Duration
StartToCloseTimeout time.Duration
HeartbeatTimeout time.Duration
CancelRequested bool
Paused bool
}
```
## ​ Activity Timeouts
Temporal enforces four types of activity timeouts to prevent stuck activities:
…
## Start-To-Close
Maximum execution time from when worker starts until completion.
Detects hung activity execution.
## Schedule-To-Close
End-to-end timeout including queue time, execution, and all retries.
Overall deadline for activity.
…
```
// From service/history/tasks/activity_task_timer.go
// Timer tasks are created when activity is scheduled/started:
// - ActivityRetryTimerTask: For retry backoff
// - ActivityTimeoutTask: For timeout enforcement
```
…
## ​ Activity Retry
Activities support automatic retry with exponential backoff:
### ​ Retry Policy
```
{
"initialInterval": "1s",
"backoffCoefficient": 2.0,
"maximumInterval": "100s",
"maximumAttempts": 0, // infinite
"nonRetryableErrorTypes": ["InvalidArgument"]
}
```
### ​ Retry Logic
1
Activity fails
Worker sends `RespondActivityTaskFailed` with failure information
2
History Service evaluates retry policy
Checks attempt count, error type, and calculates next backoff interval
3
Schedule retry or fail workflow
If retryable: Create ActivityRetryTimer task and keep activity in Scheduled state If not retryable: Append ActivityTaskFailed event and schedule workflow task
4
Timer fires
Activity is re-dispatched to Matching Service for another attempt
```
// From service/history/workflow/activity.go
func UpdateActivityInfoForRetries(
ai *persistencespb.ActivityInfo,
version int64,
attempt int32,
failure *failurepb.Failure,
nextScheduledTime *timestamppb.Timestamp,
isActivityRetryStampIncrementEnabled bool,
) {
ai.Attempt = attempt
ai.ScheduledTime = nextScheduledTime
ai.StartedEventId = common.EmptyEventID // Reset started state
ai.RetryLastFailure = failure
ai.RetryLastWorkerIdentity = ai.StartedIdentity
// Mark timers for recreation
ai.TimerTaskStatus &^= TimerTaskStatusCreatedHeartbeat |
TimerTaskStatusCreatedStartToClose
}
```
Activity retry attempts do NOT create new history events.
Only the final success or non-retryable failure creates an event.
This keeps history bounded for activities with many retries.
…
### ​ Heartbeat Mechanism
1. **Activity code calls heartbeat API** with optional progress payload
2. **Worker sends HeartbeatActivityTask RPC** to History Service
3. **History Service updates activity info** with heartbeat time and details
4. **Heartbeat timer is reset** to detect future missed heartbeats
…
```
// Heartbeat details are stored in ActivityInfo
if ai.LastHeartbeatUpdateTime != nil && !ai.LastHeartbeatUpdateTime.AsTime().IsZero() {
p.LastHeartbeatTime = ai.LastHeartbeatUpdateTime
p.HeartbeatDetails = ai.LastHeartbeatDetails
}
```
…
### ​ Cancellation Flow
...
Local activities are a special optimization for very short activities: - Execute in the same worker process as workflow
- Not recorded in history until completion
- Lower latency (no History Service roundtrip)
- Limited to short operations (seconds)
- No cross-worker routing
## ​ Activity Dispatch
Activities are dispatched through the Matching Service: 1.
**Transfer Task** created in History Service
2. **Queue Processor** reads task and calls Matching Service
3. **Matching Service** adds to appropriate task queue partition
4. **Worker** polls and receives activity task
5. **Task includes** activity input, attempt number, heartbeat details