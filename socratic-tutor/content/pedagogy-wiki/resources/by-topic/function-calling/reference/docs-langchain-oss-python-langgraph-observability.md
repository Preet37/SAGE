# Source: https://docs.langchain.com/oss/python/langgraph/observability
# Title: LangSmith Observability - Docs by LangChain
# Fetched via: jina
# Date: 2026-04-10

Title: LangSmith Observability - Docs by LangChain


# LangSmith Observability - Docs by LangChain


Join us May 13th & May 14th at Interrupt, the Agent Conference by LangChain. [Buy tickets >](https://interrupt.langchain.com/)

[Docs by LangChain home page![Image 1: light logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-dark-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=5babf1a1962208fd7eed942fa2432ecb)![Image 2: dark logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-light-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=0bcd2a1f2599ed228bcedf0f535b45b1)](https://docs.langchain.com/)![Image 3: https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png](https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png)Open source

Search...

⌘K

*   [Ask AI](https://chat.langchain.com/)
*   [GitHub](https://github.com/langchain-ai)
*   [Try LangSmith](https://smith.langchain.com/)
*   [Try LangSmith](https://smith.langchain.com/)

Search...

Navigation

Production

LangSmith Observability

[Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview)[LangChain](https://docs.langchain.com/oss/python/langchain/overview)[LangGraph](https://docs.langchain.com/oss/python/langgraph/overview)[Integrations](https://docs.langchain.com/oss/python/integrations/providers/overview)[Learn](https://docs.langchain.com/oss/python/learn)[Reference](https://docs.langchain.com/oss/python/reference/overview)[Contribute](https://docs.langchain.com/oss/python/contributing/overview)

Python

*   [Overview](https://docs.langchain.com/oss/python/langgraph/overview)

##### Get started

*   [Install](https://docs.langchain.com/oss/python/langgraph/install)
*   [Quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart)
*   [Local server](https://docs.langchain.com/oss/python/langgraph/local-server)
*   [Changelog](https://docs.langchain.com/oss/python/releases/changelog)
*   [Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)
*   [Workflows + agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents)

##### Capabilities

*   [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
*   [Durable execution](https://docs.langchain.com/oss/python/langgraph/durable-execution)
*   [Streaming](https://docs.langchain.com/oss/python/langgraph/streaming)
*   [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
*   [Time travel](https://docs.langchain.com/oss/python/langgraph/use-time-travel)
*   [Memory](https://docs.langchain.com/oss/python/langgraph/add-memory)
*   [Subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs)

##### Production

*   [Application structure](https://docs.langchain.com/oss/python/langgraph/application-structure)
*   [Test](https://docs.langchain.com/oss/python/langgraph/test)
*   [LangSmith Studio](https://docs.langchain.com/oss/python/langgraph/studio)
*   [Agent Chat UI](https://docs.langchain.com/oss/python/langgraph/ui)
*   [LangSmith Deployment](https://docs.langchain.com/oss/python/langgraph/deploy)
*   [LangSmith Observability](https://docs.langchain.com/oss/python/langgraph/observability)

##### Frontend

*   [Overview](https://docs.langchain.com/oss/python/langgraph/frontend/overview)
*   [Graph execution](https://docs.langchain.com/oss/python/langgraph/frontend/graph-execution)

##### LangGraph APIs

*   Graph API  
*   Functional API  
*   [Runtime](https://docs.langchain.com/oss/python/langgraph/pregel)

On this page

*   [Prerequisites](https://docs.langchain.com/oss/python/langgraph/observability#prerequisites)
*   [Enable tracing](https://docs.langchain.com/oss/python/langgraph/observability#enable-tracing)
*   [Trace selectively](https://docs.langchain.com/oss/python/langgraph/observability#trace-selectively)
*   [Log to a project](https://docs.langchain.com/oss/python/langgraph/observability#log-to-a-project)
*   [Add metadata to traces](https://docs.langchain.com/oss/python/langgraph/observability#add-metadata-to-traces)
*   [Use anonymizers to prevent logging of sensitive data in traces](https://docs.langchain.com/oss/python/langgraph/observability#use-anonymizers-to-prevent-logging-of-sensitive-data-in-traces)

[Production](https://docs.langchain.com/oss/python/langgraph/application-structure)

# LangSmith Observability

Copy page

Copy page

Traces are a series of steps that your application takes to go from input to output. Each of these individual steps is represented by a run. You can use [LangSmith](https://smith.langchain.com/) to visualize these execution steps. To use it, [enable tracing for your application](https://docs.langchain.com/langsmith/trace-with-langgraph). This enables you to do the following:
*   [Debug a locally running application](https://docs.langchain.com/langsmith/observability-studio#debug-langsmith-traces).
*   [Evaluate the application performance](https://docs.langchain.com/oss/python/langchain/test/evals).
*   [Monitor the application](https://docs.langchain.com/langsmith/dashboards).

## [​](https://docs.langchain.com/oss/python/langgraph/observability#prerequisites)

Prerequisites

Before you begin, ensure you have the following:
*   **A LangSmith account**: Sign up (for free) or log in at [smith.langchain.com](https://smith.langchain.com/).
*   **A LangSmith API key**: Follow the [Create an API key](https://docs.langchain.com/langsmith/create-account-api-key#create-an-api-key) guide.

## [​](https://docs.langchain.com/oss/python/langgraph/observability#enable-tracing)

Enable tracing

To enable tracing for your application, set the following environment variables:

```
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<your-api-key>
```

By default, the trace will be logged to the project with the name `default`. To configure a custom project name, see [Log to a project](https://docs.langchain.com/oss/python/langgraph/observability#log-to-a-project).For more information, see [Trace with LangGraph](https://docs.langchain.com/langsmith/trace-with-langgraph).
## [​](https://docs.langchain.com/oss/python/langgraph/observability#trace-selectively)

Trace selectively

You may opt to trace specific invocations or parts of your application using LangSmith’s `tracing_context` context manager:

```
import langsmith as ls

# This WILL be traced
with ls.tracing_context(enabled=True):
    agent.invoke({"messages": [{"role": "user", "content": "Send a test email to alice@example.com"}]})

# This will NOT be traced (if LANGSMITH_TRACING is not set)
agent.invoke({"messages": [{"role": "user", "content": "Send another email"}]})
```

## [​](https://docs.langchain.com/oss/python/langgraph/observability#log-to-a-project)

Log to a project

Statically

You can set a custom project name for your entire application by setting the `LANGSMITH_PROJECT` environment variable:

```
export LANGSMITH_PROJECT=my-agent-project
```

Dynamically

You can set the project name programmatically for specific operations:

```
import langsmith as ls

with ls.tracing_context(project_name="email-agent-test", enabled=True):
    response = agent.invoke({
        "messages": [{"role": "user", "content": "Send a welcome email"}]
    })
```

## [​](https://docs.langchain.com/oss/python/langgraph/observability#add-metadata-to-traces)

Add metadata to traces

You can annotate your traces with custom metadata and tags:

```
response = agent.invoke(
    {"messages": [{"role": "user", "content": "Send a welcome email"}]},
    config={
        "tags": ["production", "email-assistant", "v1.0"],
        "metadata": {
            "user_id": "user_123",
            "session_id": "session_456",
            "environment": "production"
        }
    }
)
```

`tracing_context` also accepts tags and metadata for fine-grained control:

```
with ls.tracing_context(
    project_name="email-agent-test",
    enabled=True,
    tags=["production", "email-assistant", "v1.0"],
    metadata={"user_id": "user_123", "session_id": "session_456", "environment": "production"}):
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "Send a welcome email"}]}
    )
```

This custom metadata and tags will be attached to the trace in LangSmith.

To learn more about how to use traces to debug, evaluate, and monitor your agents, see the [LangSmith documentation](https://docs.langchain.com/langsmith/home).

## [​](https://docs.langchain.com/oss/python/langgraph/observability#use-anonymizers-to-prevent-logging-of-sensitive-data-in-traces)

Use anonymizers to prevent logging of sensitive data in traces

You may want to mask sensitive data to prevent it from being logged to LangSmith. You can create [anonymizers](https://docs.langchain.com/langsmith/mask-inputs-outputs#rule-based-masking-of-inputs-and-outputs) and apply them to your graph using configuration. This example will redact anything matching the Social Security Number format XXX-XX-XXXX from traces sent to LangSmith.

Python

```
from langchain_core.tracers.langchain import LangChainTracer
from langgraph.graph import StateGraph, MessagesState
from langsmith import Client
from langsmith.anonymizer import create_anonymizer

anonymizer = create_anonymizer([
    # Matches SSNs
    { "pattern": r"\b\d{3}-?\d{2}-?\d{4}\b", "replace": "<ssn>" }
])

tracer_client = Client(anonymizer=anonymizer)
tracer = LangChainTracer(client=tracer_client)
# Define the graph
graph = (
    StateGraph(MessagesState)
    ...
    .compile()
    .with_config({'callbacks': [tracer]})
)
```

* * *

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langgraph/observability.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](https://docs.langchain.com/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

Yes No

[LangSmith Deployment Previous](https://docs.langchain.com/oss/python/langgraph/deploy)[Overview Next](https://docs.langchain.com/oss/python/langgraph/frontend/overview)

⌘I

[Docs by LangChain home page![Image 4: light logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-dark-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=5babf1a1962208fd7eed942fa2432ecb)![Image 5: dark logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-light-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=0bcd2a1f2599ed228bcedf0f535b45b1)](https://docs.langchain.com/)

[github](https://github.com/langchain-ai)[x](https://x.com/LangChain)[linkedin](https://www.linkedin.com/company/langchain)[youtube](https://www.youtube.com/@LangChain)

Resources

[Forum](https://forum.langchain.com/)[Changelog](https://changelog.langchain.com/)[LangChain Academy](https://academy.langchain.com/)[Contact Sales](https://www.langchain.com/contact-sales)

Company

[Home](https://langchain.com/)[Trust Center](https://trust.langchain.com/)[Careers](https://langchain.com/careers)[Blog](https://blog.langchain.com/)

[github](https://github.com/langchain-ai)[x](https://x.com/LangChain)[linkedin](https://www.linkedin.com/company/langchain)[youtube](https://www.youtube.com/@LangChain)