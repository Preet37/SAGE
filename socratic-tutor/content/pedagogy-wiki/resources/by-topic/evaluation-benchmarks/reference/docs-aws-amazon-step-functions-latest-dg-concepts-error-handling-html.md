# Source: https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html
# Title: AWS Step Functions Developer Guide — Error handling (Retry/Catch) semantics
# Fetched via: trafilatura
# Date: 2026-04-10

Handling errors in Step Functions workflows
All states, except Pass
and Wait
-
State machine definition issues - such as a Choice state without a matching rule
-
Task failures - such as an exception in a AWS Lambda function
-
Transient issues - such as network partition events
When a state reports an error, Step Functions defaults to failing the entire state machine execution. Step Functions also has more advanced error handling features. You can set up your state machine to catch errors, retry failed states, and gracefully implement error handling protocols.
Step Functions catchers are available for Task, Parallel and Map states, but not for
top-level state machine execution failures. To handle executions you anticipate might fail,
your caller can handle the error, or you might nest those executions inside child workflows
to catch errors inside your parent workflow. Alternatively, you might choose to listen for
TIMED_OUT
events from Standard workflows with an EventBridge bus and invoke an action to
handle the failed execution.
Practical examples for handling errors
To deploy an example of a workflow that includes error handling, see [Handling error conditions in a Step Functions state machine](./tutorial-handling-error-conditions.html) tutorial in this guide, and [Error Handling](https://catalog.workshops.aws/stepfunctions/handling-errors) in The AWS Step Functions Workshop.
Error names
Step Functions identifies errors using case-sensitive strings, known as error
names. The Amazon States Language defines a set of built-in strings that name well-known
errors, all beginning with the States.
prefix.
States can report errors with other names. However, the error names cannot begin with
the States.
prefix.
Ensure your production code can handle AWS Lambda service exceptions
(Lambda.ServiceException
and Lambda.SdkClientException
). For
more information, see how to [Handle transient Lambda service exceptions](./sfn-best-practices.html#bp-lambda-serviceexception) in Best practices.
-
States.ALL
-
A wildcard that matches any known error name.
The
States.ALL
error type must appear alone in aCatcher
and cannot catch theStates.DataLimitExceeded
terminal error orRuntime
error types.For more information, see
[States.DataLimitExceeded](#error-data-limit-exceed)and[States.Runtime](#states-runtime-error). -
States.DataLimitExceeded
-
A terminal error which cannot be caught by the
States.ALL
error type.Reported due to the following conditions:
-
Output of a connector is larger than payload size quota.
-
Output of a state is larger than payload size quota.
-
After
Parameters
processing, the input of a state is larger than the payload size quota.
For more information on quotas, see
[Step Functions service quotas](./service-quotas.html). -
States.ExceedToleratedFailureThreshold
A
Map
States.HeartbeatTimeout
-
A
Task
value.HeartbeatTimeout
is available inside theCatch
andRetry
fields. -
States.Http.Socket
-
Occurs when an HTTP task times out after 60 seconds. See
[Quotas related to HTTP Task](./service-quotas.html#service-limits-http-task). States.ItemReaderFailed
A
Map
field. For more information, see
.[ItemReader (Map)](./input-output-itemreader.html)-
States.Permissions
-
A
Task
A
Map
field. For more information, see
.[ResultWriter (Map)](./input-output-resultwriter.html)States.Runtime
-
An execution failed due to some exception that it couldn't process. Often these are caused by errors at runtime, such as attempting to apply
InputPath
orOutputPath
on a null JSON payload. AStates.Runtime
error isn't retriable, and will always cause the execution to fail. A retry or catch onStates.ALL
won't catchStates.Runtime
errors. -
States.TaskFailed
-
A
Task
acts as a wildcard that matches any known error name except forStates.Timeout
. -
States.Timeout
-
Reported when a
Task
value or failed to send a heartbeat for a period longer than theHeartbeatSeconds
value.If a nested state machine throws a
States.Timeout
, the parent will receive aStates.TaskedFailed
error.A
States.Timeout
error is also reported when an entire state machine execution runs longer than the specifiedTimeoutSeconds
value.
Note
Unhandled errors in Lambda runtimes were historically reported only as Lambda.Unknown
. In newer runtimes, timeouts are reported as Sandbox.Timedout
in the
error output.
When Lambda exceeds the maximum number of invocations, the reported error will be Lambda.TooManyRequestsException
.
Match on Lambda.Unknown
, Sandbox.Timedout
, and States.TaskFailed
to handle possible errors. You can also use States.ALL
, but it must be alone and at the end of the list.
For more information about Lambda Handled
and Unhandled
errors, see FunctionError
in the [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html#API_Invoke_ResponseSyntax).
Retrying after an error
Task
, Parallel
, and Map
, whose value
must be an array of objects known as retriers. An individual retrier represents a certain number of retries, usually at increasing time intervals.
When one of these states reports an error and there's a Retry
field, Step Functions scans through the retriers in the order listed in the array. When the error name appears in the value of a retrier's ErrorEquals
field, the state machine makes retry attempts as defined in the Retry
field.
If your redriven execution reruns a [Task workflow state](./state-task.html), [Parallel workflow state](./state-parallel.html), or [Inline Map state](./state-map-inline.html), for which you have defined retries, the retry attempt count for these states is reset to 0 to allow for the maximum number of attempts on redrive. For a redriven execution, you can track individual retry attempts of these states using the console. For more information, see [Retry behavior of redriven executions](./redrive-executions.html#redrive-retry-behavior) in [Restarting state machine executions with redrive in Step Functions](./redrive-executions.html).
A retrier contains the following fields:
-
ErrorEquals
(Required) -
A non-empty array of strings that match error names. When a state reports an error, Step Functions scans through the retriers. When the error name appears in this array, it implements the retry policy described in this retrier.
-
IntervalSeconds
(Optional) -
A positive integer that represents the number of seconds before the first retry attempt (
1
by default).IntervalSeconds
has a maximum value of 99999999. -
MaxAttempts
(Optional) -
A positive integer that represents the maximum number of retry attempts (
3
by default). If the error recurs more times than specified, retries cease and normal error handling resumes. A value of0
specifies that the error is never retried.MaxAttempts
has a maximum value of 99999999. -
BackoffRate
(Optional) -
The multiplier by which the retry interval denoted by
IntervalSeconds
increases after each retry attempt. By default, theBackoffRate
value increases by2.0
.For example, say your
IntervalSeconds
is 3,MaxAttempts
is 3, andBackoffRate
is 2. The first retry attempt takes place three seconds after the error occurs. The second retry takes place six seconds after the first retry attempt. While the third retry takes place 12 seconds after the second retry attempt. -
MaxDelaySeconds
(Optional) -
A positive integer that sets the maximum value, in seconds, up to which a retry interval can increase. This field is helpful to use with the
BackoffRate
field. The value you specify in this field limits the exponential wait times resulting from the backoff rate multiplier applied to each consecutive retry attempt. You must specify a value greater than 0 and less than 31622401 forMaxDelaySeconds
.If you don't specify this value, Step Functions doesn't limit the wait times between retry attempts.
-
JitterStrategy
(Optional) -
A string that determines whether or not to include jitter in the wait times between consecutive retry attempts. Jitter reduces simultaneous retry attempts by spreading these out over a randomized delay interval. This string accepts
FULL
orNONE
as its values. The default value isNONE
.For example, say you have set
MaxAttempts
as 3,IntervalSeconds
as 2, andBackoffRate
as 2. The first retry attempt takes place two seconds after the error occurs. The second retry takes place four seconds after the first retry attempt and the third retry takes place eight seconds after the second retry attempt. If you setJitterStrategy
asFULL
, the first retry interval is randomized between 0 and 2 seconds, the second retry interval is randomized between 0 and 4 seconds, and the third retry interval is randomized between 0 and 8 seconds.
Note
Retries are treated as state transitions. For information about how state transitions affect billing, see [Step Functions Pricing](https://aws.amazon.com/step-functions/pricing/).
Retry field examples
This section includes the following Retry
field examples.
Example 1 – Retry with BackoffRate
The following example of a Retry
makes two retry attempts with the first retry taking place after waiting for three seconds. Based on the BackoffRate
you specify, Step Functions increases the interval between each retry until the maximum number of retry attempts is reached. In the following example, the second retry attempt starts after waiting for three seconds after the first retry.
"Retry": [ {
"ErrorEquals": [ "States.Timeout" ],
"IntervalSeconds": 3,
"MaxAttempts": 2,
"BackoffRate": 1
} ]
Example 2 – Retry with MaxDelaySeconds
The following example makes three retry attempts and limits the wait time resulting from BackoffRate
at 5 seconds. The first retry takes place after waiting for three seconds. The second and third retry attempts take place after waiting for five seconds after the preceding retry attempt because of the maximum wait time limit set by MaxDelaySeconds
.
"Retry": [ {
"ErrorEquals": [ "States.Timeout" ],
"IntervalSeconds": 3,
"MaxAttempts": 3,
"BackoffRate":2,
"MaxDelaySeconds": 5,
"JitterStrategy": "FULL"
} ]
Without MaxDelaySeconds
, the second retry attempt would take place six seconds after the first retry, and the third retry attempt would take place 12 seconds after the second retry.
Example 3 – Retry all errors except States.Timeout
The reserved name States.ALL
that appears in a retrier's ErrorEquals
field is a wildcard that matches any error name. It must appear alone in the ErrorEquals
array and must appear in the last retrier in the Retry
array. The name States.TaskFailed
also acts a wildcard and matches any error except for States.Timeout
.
The following example of a Retry
field retries any error except States.Timeout
.
"Retry": [ {
"ErrorEquals": [ "States.Timeout" ],
"MaxAttempts": 0
}, {
"ErrorEquals": [ "States.ALL" ]
} ]
Example 4 – Complex retry scenario
A retrier's parameters apply across all visits to the retrier in the context of a single-state execution.
Consider the following Task
"X": {
"Type": "Task",
"Resource": "arn:aws:states:region
:123456789012:task:X",
"Next": "Y",
"Retry": [ {
"ErrorEquals": [ "ErrorA", "ErrorB" ],
"IntervalSeconds": 1,
"BackoffRate": 2.0,
"MaxAttempts": 2
}, {
"ErrorEquals": [ "ErrorC" ],
"IntervalSeconds": 5
} ],
"Catch": [ {
"ErrorEquals": [ "States.ALL" ],
"Next": "Z"
} ]
}
This task fails four times in succession, outputting these error names: ErrorA
, ErrorB
, ErrorC
, and
ErrorB
. The following occurs as a result:
-
The first two errors match the first retrier and cause waits of one and two seconds.
-
The third error matches the second retrier and causes a wait of five seconds.
-
The fourth error also matches the first retrier. However, it already reached its maximum of two retries (
MaxAttempts
) for that particular error. Therefore, that retrier fails and the execution redirects the workflow to theZ
field.
Fallback states
Task
,
Map
and Parallel
each
have a field named Catch
. This field's value must be an
array of objects, known as catchers.
A catcher contains the following fields.
-
ErrorEquals
(Required) -
A non-empty array of strings that match error names, specified exactly as they are with the retrier field of the same name.
-
Next
(Required) -
A string that must exactly match one of the state machine's state names.
-
ResultPath
(JSONPath, Optional) -
A
[path](./concepts-input-output-filtering.html)that determines what input the catcher sends to the state specified in theNext
field.
When a state reports an error and either there is no Retry
field, or if
retries fail to resolve the error, Step Functions scans through the catchers in the order listed
in the array. When the error name appears in the value of a catcher's
ErrorEquals
field, the state machine transitions to the state named in
the Next
field.
The reserved name States.ALL
that appears in a catcher's
ErrorEquals
field is a wildcard that matches any error name. It must
appear alone in the ErrorEquals
array and must appear in the last catcher
in the Catch
array. The name States.TaskFailed
also acts a
wildcard and matches any error except for States.Timeout
.
The following example of a Catch
field transitions to the state named
RecoveryState
when a Lambda function outputs an unhandled Java
exception. Otherwise, the field transitions to the EndState
"Catch": [ {
"ErrorEquals": [ "java.lang.Exception" ],
"ResultPath": "$.error-info",
"Next": "RecoveryState"
}, {
"ErrorEquals": [ "States.ALL" ],
"Next": "EndState"
} ]
How many errors can a catcher catch?
Each catcher can specify multiple errors to handle.
Error output
When Step Functions transitions to the state specified in a catch name, the object usually
contains the field Cause
. This field's value is a human-readable
description of the error. This object is known as the error
output.
In the previous JSONPath example, the first catcher contains a ResultPath
field. This
works similarly to a ResultPath
field in a state's top level, resulting
in two possibilities:
-
Take the results of that state's execution and overwrite either all of, or a portion of, the state's input.
-
Take the results and adds them to the input. In the case of an error handled by a catcher, the result of the state's execution is the error output.
Thus, for the first catcher in the example,
the catcher
adds the error
output
to the input as a field named error-info
if there
isn't already a field with this name in the
input.
Then, the
catcher sends the entire
input
to RecoveryState
. For the second catcher, the error output overwrites
the input and
the catcher
only
sends the
error output
to
EndState
.
For JSONPath workflows, if you don't specify the ResultPath
field, it defaults to
$
, which selects and overwrites the entire input.
When a state has both Retry
and Catch
fields, Step Functions uses
any appropriate retriers first.
If
the retry policy fails to resolve the error, Step Functions applies the
matching catcher
transition.
Cause payloads and service integrations
A catcher returns a string payload as an output. When working with service
integrations such as Amazon Athena or AWS CodeBuild, you may want to convert the
Cause
string to JSON. The following example of a
Pass
Cause
string to JSON.
"Handle escaped JSON with JSONtoString": {
"Type": "Pass",
"Parameters": {
"Cause.$": "States.StringToJson($.Cause)"
},
"Next": "Pass State with Pass Processing"
},
State machine examples using Retry and Catch
The state machines defined in the following examples assume the existence of two Lambda functions: one that always fails and one that waits long enough to allow a timeout defined in the state machine to occur.
This is a definition of a Node.js Lambda function that always fails, returning the
message error
. In the state machine examples that follow, this Lambda
function is named FailFunction
. For information about creating a Lambda
function, see [Step 1: Create a Lambda function](./tutorial-creating-lambda-state-machine.html#create-lambda-function) section.
exports.handler = (event, context, callback) => {
callback("error");
};
This is a definition of a Node.js Lambda function that sleeps for 10 seconds. In the state machine examples that follow, this Lambda function is named sleep10
.
exports.handler = (event, context, callback) => {
setTimeout(function(){
}, 11000);
};
Timeout settings for the function
When you create the Lambda function for the examples, remember to set the Timeout
value in the advanced settings to 11 seconds.
Handling a failure using Retry
This state machine uses a Retry
field to retry a function that fails
and outputs the error name HandledError
.
It retries
this
function
twice
with an exponential backoff between retries.
{
"Comment": "A Hello World example invoking Lambda function",
"StartAt": "HelloWorld",
"States": {
"HelloWorld": {
"Type": "Task",
"Resource": "arn:aws:lambda:region
:123456789012:function:FailFunction",
"Retry": [ {
"ErrorEquals": ["HandledError"],
"IntervalSeconds": 1,
"MaxAttempts": 2,
"BackoffRate": 2.0
} ],
"End": true
}
}
}
This variant uses the predefined error code States.TaskFailed
, which
matches any error that a Lambda function outputs.
{
"Comment": "Hello World example which invokes a AWS Lambda function",
"StartAt": "HelloWorld",
"States": {
"HelloWorld": {
"Type": "Task",
"Resource": "arn:aws:lambda:region
:123456789012:function:FailFunction",
"Retry": [ {
"ErrorEquals": ["States.TaskFailed"],
"IntervalSeconds": 1,
"MaxAttempts": 2,
"BackoffRate": 2.0
} ],
"End": true
}
}
}
Best practices for handling Lambda exceptions
Tasks that reference a Lambda function should handle Lambda
service exceptions. For more information, see [Handle transient Lambda service exceptions](./sfn-best-practices.html#bp-lambda-serviceexception) in Best Practices.
Handling a failure using Catch
This example uses a Catch
field. When a Lambda function outputs an
error, it
catches the error
and
the state machine transitions to the fallback
{
"Comment": "Hello World example which invokes a AWS Lambda function",
"StartAt": "HelloWorld",
"States": {
"HelloWorld": {
"Type": "Task",
"Resource": "arn:aws:lambda:region
:123456789012:function:FailFunction",
"Catch": [ {
"ErrorEquals": ["HandledError"],
"Next": "fallback"
} ],
"End": true
},
"fallback": {
"Type": "Pass",
"Result": "Hello, AWS Step Functions!",
"End": true
}
}
}
This variant uses the predefined error code States.TaskFailed
, which
matches any error that a Lambda function outputs.
{
"Comment": "Hello World example which invokes a AWS Lambda function",
"StartAt": "HelloWorld",
"States": {
"HelloWorld": {
"Type": "Task",
"Resource": "arn:aws:lambda:region
:123456789012:function:FailFunction",
"Catch": [ {
"ErrorEquals": ["States.TaskFailed"],
"Next": "fallback"
} ],
"End": true
},
"fallback": {
"Type": "Pass",
"Result": "Hello, AWS Step Functions!",
"End": true
}
}
}
Handling a timeout using Retry
This state machine uses a Retry
field to retry a Task
out,
based on the timeout value specified in TimeoutSeconds
.
Step Functions retries
the
Lambda function invocation in this Task
twice,
with an exponential backoff between retries.
{
"Comment": "Hello World example which invokes a AWS Lambda function",
"StartAt": "HelloWorld",
"States": {
"HelloWorld": {
"Type": "Task",
"Resource": "arn:aws:lambda:region
:123456789012:function:sleep10",
"TimeoutSeconds": 2,
"Retry": [ {
"ErrorEquals": ["States.Timeout"],
"IntervalSeconds": 1,
"MaxAttempts": 2,
"BackoffRate": 2.0
} ],
"End": true
}
}
}
Handling a timeout using Catch
This example uses a Catch
field. When a timeout occurs, the state
machine transitions to the fallback
{
"Comment": "Hello World example which invokes a AWS Lambda function",
"StartAt": "HelloWorld",
"States": {
"HelloWorld": {
"Type": "Task",
"Resource": "arn:aws:lambda:region
:123456789012:function:sleep10",
"TimeoutSeconds": 2,
"Catch": [ {
"ErrorEquals": ["States.Timeout"],
"Next": "fallback"
} ],
"End": true
},
"fallback": {
"Type": "Pass",
"Result": "Hello, AWS Step Functions!",
"End": true
}
}
}
Preserving state input and error in JSONPath
In JSONPath, you can preserve the state input and the error by using
ResultPath
. See [Use ResultPath to include both error and input in a Catch](./input-output-resultpath.html#input-output-resultpath-catch).