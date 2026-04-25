# Source: https://docs.aws.amazon.com/step-functions/latest/dg/limits.html
# Title: AWS Step Functions Developer Guide — Quotas and limits
# Fetched via: trafilatura
# Date: 2026-04-10

Step Functions service quotas
AWS Step Functions provide default service quotas for state machine parameters, such as the number of API actions during a time period or the number of state machines that you can define. Quotas are designed to prevent misconfigured state machine from consuming all of the resources of the system, although many do not have hard limits.
To request a service quota increase, you can do one of the following:
-
Use the Service Quotas console at
[https://console.aws.amazon.com/servicequotas/home](https://console.aws.amazon.com/servicequotas/home). For information about requesting a quota increase using the Service Quotas console, see[Requesting a quota increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html)in the Service Quotas User Guide. -
Use the Support Center page in the AWS Management Console to request a quota increase for resources provided by AWS Step Functions on a per-Region basis. For more information, see
[AWS service quotas](https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html)in the AWS General Reference.
Important
New AWS accounts have reduced state transition quotas. AWS raises these quotas automatically based on your usage.
Note
If a particular stage of your state machine execution or activity execution takes too long, you can configure a state machine timeout to cause a timeout event.
Topics
General quotas
Names of state machines, executions, and activity tasks must not exceed 80 characters in length. These names must be unique for your account and AWS Region, and must not contain any of the following:
-
Whitespace
-
Wildcard characters (
? *
) -
Bracket characters (
< > { } [ ]
) -
Special characters (
" # % \ ^ | ~ ` $ & , ; : /
) -
Control characters (
\\u0000
-\\u001f
or\\u007f
-\\u009f
).
Step Functions accepts names for state machines, executions, activities, and labels that contain non-ASCII characters. Because such characters will prevent Amazon CloudWatch from logging data, we recommend using only ASCII characters so you can track Step Functions metrics.
Quotas related to accounts
| Resource | Default quota | Can be increased to |
|---|---|---|
| Maximum number of registered state machines | 100,000 | 150,000 |
|
Maximum number of registered activities |
100,000 | 150,000 |
|
Maximum size of state machine definition |
1 MB | Hard quota |
| Maximum request size | 1 MB per request. This is the total data size per Step Functions API request, including the request header and all other associated request data. | Hard quota |
|
Maximum open executions per account |
1,000,000 executions for each AWS account
in each AWS Region. Exceeding this limit will cause an
ExecutionLimitExceeded error. This doesn't apply to Express
Workflows. |
Millions |
Maximum number of open Map Runs |
1000 This quota applies to An open |
Hard quota |
Maximum |
1000 This quota applies to Distributed Map state. |
Hard quota |
| Maximum number of parallel Map Run child executions | 10,000 |
Hard quota |
Quotas related to HTTP Task
HTTP Tasks are throttled using a token bucket scheme to maintain the Step Functions service bandwidth.
| Resource | Bucket size | Refill rate per second |
|---|---|---|
|
| Resource | Default quota |
|---|---|
| HTTP Task duration — time to send an HTTP request and receive a response | 60 seconds (Hard quota) |
Quotas related to state throttling
Step Functions state transitions are throttled using a token bucket scheme to maintain service bandwidth. Standard Workflows and Express Workflows have different state transition throttling. Standard Workflows quotas are soft quotas and can be increased.
Note
Throttling on the StateTransition
service metric is reported as
ExecutionThrottled
in Amazon CloudWatch. For more information, see the [ExecutionThrottled CloudWatch metric](./procedure-cw-metrics.html#cloudwatch-step-functions-execution-metrics).
| Standard | Express | |||
| Service metric | Bucket size | Refill rate per second | Bucket size | Refill rate per second |
|
|
5,000 | 5,000 |
Unlimited |
Unlimited |
|
|
800 | 800 |
Unlimited |
Unlimited |
Quotas related to API action throttling
Some Step Functions API actions are throttled using a token bucket scheme to maintain service bandwidth. The following are soft quotas and can be increased.
Note
Throttling quotas are per account, per AWS Region.
AWS Step Functions may increase both the bucket size and refill rate at any time.
| Standard | Express | |||
| API name | Bucket size | Refill rate per second | Bucket size | Refill rate per second |
StartExecution — US East (N. Virginia),
US West (Oregon), and Europe (Ireland) |
1,300 | 300 | 6,000 | 6,000 |
StartExecution — All other
regions |
800 | 150 | 6,000 | 6,000 |
Other quotas
The following are soft quotas and can be increased.
| US East (N. Virginia), US West (Oregon), and Europe (Ireland) | All other regions | |||
| API name | Bucket size | Refill rate per second | Bucket size | Refill rate per second |
CreateActivity |
100 | 1 | 100 | 1 |
CreateStateMachine |
100 | 1 | 100 | 1 |
CreateStateMachineAlias |
100 | 1 | 100 | 1 |
DeleteActivity |
100 | 1 | 100 | 1 |
DeleteStateMachine |
100 | 1 | 100 | 1 |
DeleteStateMachineAlias |
100 | 1 | 100 | 1 |
DeleteStateMachineVersion |
100 | 1 | 100 | 1 |
DescribeActivity |
200 | 1 | 200 | 1 |
DescribeExecution |
300 | 15 | 250 | 10 |
DescribeMapRun |
200 | 1 | 200 | 1 |
DescribeStateMachine |
200 | 20 | 200 | 20 |
DescribeStateMachineAlias |
200 | 1 | 200 | 1 |
DescribeStateMachineForExecution |
200 | 1 | 200 | 1 |
GetActivityTask |
3,000 | 500 | 1,500 | 300 |
GetExecutionHistory |
400 | 20 | 400 | 20 |
ListActivities |
100 | 10 | 100 | 5 |
ListExecutions |
200 | 5 | 100 | 2 |
ListMapRuns |
100 | 1 | 100 | 1 |
ListStateMachineAliases |
100 | 1 | 100 | 1 |
ListStateMachines |
100 | 5 | 100 | 5 |
ListStateMachineVersions |
100 | 1 | 100 | 1 |
ListTagsForResource |
100 | 1 | 100 | 1 |
PublishStateMachineVersion |
100 | 1 | 100 | 1 |
RedriveExecution |
1,300 | 300 | 800 | 150 |
SendTaskFailure |
3,000 | 500 | 1,500 | 300 |
SendTaskHeartbeat |
3,000 | 500 | 1,500 | 300 |
SendTaskSuccess |
3,000 | 500 | 1,500 | 300 |
| StartSyncExecution |
Synchronous Express execution API calls don't contribute to existing account capacity limits. Step Functions provides capacity on demand and automatically scales with sustained workload. Surges in workload may be throttled until capacity is available. If you experience throttling, try again after some time. For information about Synchronous Express workflows, see |
|||
StopExecution |
1,000 | 200 | 500 | 25 |
TagResource |
200 | 1 | 200 | 1 |
TestState |
10 | 50 | 10 | 50 |
UntagResource |
200 | 1 | 200 | 1 |
UpdateMapRun |
100 | 1 | 100 | 1 |
UpdateStateMachine |
100 | 1 | 100 | 1 |
UpdateStateMachineAlias |
100 | 1 | 100 | 1 |
ValidateStateMachineDefinition |
100 | 1 | 100 | 1 |
Quotas related to state machine executions
The following table describes quotas related to state machine executions. State machine execution quotas are hard quotas that can't be changed, except for the Execution history retention time quota.
| Quota | Standard | Express |
|---|---|---|
|
Maximum execution time |
1 year. If an execution runs for more than the 1-year maximum, it
will fail with a |
5 minutes. If an execution runs for more than the 5-minute
maximum, it will fail with a |
|
Maximum execution history size |
25,000 events in a single state machine execution history. If the execution history reaches this quota, the execution will fail. To avoid this, see
|
Maximum execution idle time
1 year
Constrained by maximum execution time.
5 minutes
Constrained by maximum execution time.
90 days after an execution is closed. After this time, you can no longer retrieve or view the execution history. There is no further quota for the number of closed executions that Step Functions retains.
To meet compliance, organizational, or regulatory requirements, you can reduce the execution history retention period to 30 days by sending a quota request. To do this, use the AWS Support Center Console and create a new case.
The change to reduce the retention period to 30 days is applicable for each account in a Region.
To see execution history, Amazon CloudWatch Logs logging must be configured.
For more information, see [Using CloudWatch Logs to log execution history in Step Functions](./cw-logs.html).
14 days
Hard quota applies to [Distributed Map state](./state-map-distributed.html).
Redrivable period refers to the time during which you can [redrive](./redrive-executions.html) a given [Standard Workflow](./choosing-workflow-type.html) execution. This period starts from the day a state machine completes its execution.
Quotas related to task executions
The following table describes quotas related to task executions. These are all hard quotas that cannot be changed.
| Quota | Standard | Express |
|---|---|---|
| Maximum task execution time | 1 year — Constrained by maximum execution time. | 5 minutes — Constrained by maximum execution time. |
| Maximum time Step Functions keeps a task in the queue | 1 year — Constrained by maximum execution time. | 5 minutes — Constrained by maximum execution time. |
| Maximum input or output size for a task, state, or execution | 256 KiB of data as a UTF-8 encoded string. This quota affects tasks (activity, Lambda function, or integrated service), state or execution output, and input data when scheduling a task, entering a state, or starting an execution. | 256 KiB of data as a UTF-8 encoded string. This quota affects tasks (activity, Lambda function, or integrated service), state or execution output, and input data when scheduling a task, entering a state, or starting an execution. |
Quotas related to versions and aliases
| Resource | Default quota |
|---|---|
| Maximum number of published state machine versions | 1000 per state machine |
| Maximum number of state machine aliases | 100 per state machine |
To request an increase to soft limits for published state machine versions and aliases,
use the Support Center page in the
[AWS Management Console](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html).
Restrictions related to tagging
The following tagging restrictions can not be modified or increased.
Prefix restriction — Do not use the
aws:
prefix in your tag names or values because it is reserved for AWS use only. You cannot edit or delete tag names or values with anaws:
prefix. Tags with theaws:
prefix do not count against your tags per resource quota.Character restrictions — Tags may only contain Unicode letters, digits, whitespace, or the following symbols:
_ . : / = + - @
| Restriction | Description |
|---|---|
| Maximum number of tags per resource | 50 |
| Maximum key length | 128 Unicode characters in UTF-8 |
| Maximum value length | 256 Unicode characters in UTF-8 |