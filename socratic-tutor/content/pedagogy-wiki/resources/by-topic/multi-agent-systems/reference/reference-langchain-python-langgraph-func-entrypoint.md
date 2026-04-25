# Source: https://reference.langchain.com/python/langgraph/func/entrypoint
# Title: entrypoint | langgraph (Functional API)
# Fetched via: browser
# Date: 2026-04-10

Class
v1.1.6 (latest)
●
Since v0.2
entrypoint

Define a LangGraph workflow using the entrypoint decorator.

Function signature

The decorated function must accept a single parameter, which serves as the input to the function. This input parameter can be of any type. Use a dictionary to pass multiple parameters to the function.

Injectable parameters

The decorated function can request access to additional parameters that will be injected automatically at run time. These parameters include:

Parameter	Description
config	A configuration object (aka RunnableConfig) that holds run-time configuration values.
previous	The previous return value for the given thread (available only when a checkpointer is provided).
runtime	A Runtime object that contains information about the current run, including context, store, writer

The entrypoint decorator can be applied to sync functions or async functions.

State management

The previous parameter can be used to access the return value of the previous invocation of the entrypoint on the same thread id. This value is only available when a checkpointer is provided.

If you want previous to be different from the return value, you can use the entrypoint.final object to return a value while saving a different value to the checkpoint.

Copy
entrypoint(
  self,
  checkpointer: BaseCheckpointSaver | None = None,
  store: BaseStore | None = None,
  cache: BaseCache | None = None,
  context_schema: type[ContextT] | None = None,
  cache_policy: CachePolicy | None = None,
  retry_policy: RetryPolicy | Sequence[RetryPolicy] | None = None,
  **kwargs: Unpack[DeprecatedKwargs] = {}
)
BASES
Generic[ContextT]

The config_schema parameter is deprecated in v0.6.0 and support will be removed in v2.0.0. Please use context_schema instead to specify the schema for run-scoped context.

Using entrypoint and tasks:

import time

from langgraph.func import entrypoint, task
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver

@task
def compose_essay(topic: str) -> str:
    time.sleep(1.0)  # Simulate slow operation
    return f"An essay about {topic}"

@entrypoint(checkpointer=InMemorySaver())
def review_workflow(topic: str) -> dict:
    """Manages the workflow for generating and reviewing an essay.

    The workflow includes:
    1. Generating an essay about the given topic.
    2. Interrupting the workflow for human review of the generated essay.

    Upon resuming the workflow, compose_essay task will not be re-executed
    as its result is cached by the checkpointer.

    Args:
        topic: The subject of the essay.

    Returns:
        dict: A dictionary containing the generated essay and the human review.
    """
    essay_future = compose_essay(topic)
    essay = essay_future.result()
    human_review = interrupt({
        "question": "Please provide a review",
        "essay": essay
    })
    return {
        "essay": essay,
        "review": human_review,
    }

# Example configuration for the workflow
config = {
    "configurable": {
        "thread_id": "some_thread"
    }
}

# Topic for the essay
topic = "cats"

# Stream the workflow to generate the essay and await human review
for result in review_workflow.stream(topic, config):
    print(result)

# Example human review provided after the interrupt
human_review = "This essay is great."

# Resume the workflow with the provided human review
for result in review_workflow.stream(Command(resume=human_review), config):
    print(result)
Copy

Accessing the previous return value:

When a checkpointer is enabled the function can access the previous return value of the previous invocation on the same thread id.

from typing import Optional

from langgraph.checkpoint.memory import MemorySaver

from langgraph.func import entrypoint

@entrypoint(checkpointer=InMemorySaver())
def my_workflow(input_data: str, previous: Optional[str] = None) -> str:
    return "world"

config = {"configurable": {"thread_id": "some_thread"}}
my_workflow.invoke("hello", config)
Copy

Using entrypoint.final to save a value:

The entrypoint.final object allows you to return a value while saving a different value to the checkpoint. This value will be accessible in the next invocation of the entrypoint via the previous parameter, as long as the same thread id is used.

from typing import Any

from langgraph.checkpoint.memory import MemorySaver

from langgraph.func import entrypoint

@entrypoint(checkpointer=InMemorySaver())
def my_workflow(
    number: int,
    *,
    previous: Any = None,
) -> entrypoint.final[int, int]:
    previous = previous or 0
    # This will return the previous value to the caller, saving
    # 2 * number to the checkpoint, which will be used in the next invocation
    # for the `previous` parameter.
    return entrypoint.final(value=previous, save=2 * number)

config = {"configurable": {"thread_id": "some_thread"}}

my_workflow.invoke(3, config)  # 0 (previous was None)
my_workflow.invoke(1, config)  # 6 (previous was 3 * 2 from the previous invocation)
Copy
USED IN DOCS
Choosing between Graph and Functional APIs
Deploy other frameworks
Functional API overview
Quickstart
Use the functional API
+1 more
Parameters
Name	Type	Description
checkpointer	BaseCheckpointSaver | None	
Default:
None

Specify a checkpointer to create a workflow that can persist its state across runs.


store	BaseStore | None	
Default:
None

A generalized key-value store. Some implementations may support semantic search capabilities through an optional index configuration.


cache	BaseCache | None	
Default:
None

A cache to use for caching the results of the workflow.


context_schema	type[ContextT] | None	
Default:
None

Specifies the schema for the context object that will be passed to the workflow.


cache_policy	CachePolicy | None	
Default:
None

A cache policy to use for caching the results of the workflow.


retry_policy	RetryPolicy | Sequence[RetryPolicy] | None	
Default:
None

A retry policy (or list of policies) to use for the workflow in case of a failure.

Constructors
constructor
__init__
Name	Type
checkpointer	BaseCheckpointSaver | None
store	BaseStore | None
cache	BaseCache | None
context_schema	type[ContextT] | None
cache_policy	CachePolicy | None
retry_policy	RetryPolicy | Sequence[RetryPolicy] | None
Attributes
attribute
checkpointer
: checkpointer
attribute
store
: store
attribute
cache
: cache
attribute
cache_policy
: cache_policy
attribute
retry_policy
: retry_policy
attribute
context_schema
: context_schema
Classes
class
final

A primitive that can be returned from an entrypoint.

This primitive allows to save a value to the checkpointer distinct from the return value from the entrypoint.

View source on GitHub
Version History