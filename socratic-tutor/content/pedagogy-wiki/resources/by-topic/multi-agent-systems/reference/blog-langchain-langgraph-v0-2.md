# Source: https://blog.langchain.com/langgraph-v0-2/
# Author: LangChain
# Author Slug: langchain
# Title: LangGraph v0.2: Increased customization with new checkpointer ...
# Fetched via: trafilatura
# Date: 2026-04-10

Today, we’re excited to announce the stable release of LangGraph v0.2, which introduces a new ecosystem of LangGraph checkpointer libraries. These simplify the creation and customization of checkpointers, which allows users to build more resilient LLM applications with smooth session memory, robust error recovery, and human-in-the-loop features.
Why we built LangGraph v0.2
One of the key pillars of LangGraph is its built-in persistence layer, implemented through checkpointers. When you use a checkpointer with a graph, you can interact with and manage the graph's state. The checkpointer saves a checkpoint of the graph state at each step, enabling several powerful capabilities, including:
- Session memory: Store history (checkpoints) of user interactions and resume from a saved checkpoint in follow up interactions
- Error recovery: Recover from failures at any given step in the graph execution by continuing from the last successful step checkpoint
- Human-in-the-loop: Implement tool approval, wait for human input, edit agent actions and more
- Time travel: Edit graph state at any point in the history of execution and create an alternative execution from that point in time (i.e. fork the thread)
Since the early days of LangGraph, we’ve designed checkpointing to be database-agnostic, allowing users to implement their own checkpointer adapters for their database of choice.
Since the [LangGraph v0.1 release,](https://blog.langchain.com/langgraph-cloud/) we've seen a lot of interest from the community in creating checkpointers for many popular databases like Postgres, Redis, and MongoDB. However, there was no clear blueprint for the users to implement their own, custom checkpointers.
New checkpointer libraries in LangGraph
With LangGraph v0.2, we’re making it easier to create new checkpointers. We’ve also laid the foundation to foster a community-maintained ecosystem of checkpointer implementations.
We now have a suite of new, dedicated checkpointer libraries:
langgraph_checkpoint
: The base interface for checkpointer savers (BaseCheckpointSaver
) and serialization/deserialization interface (SerializationProtocol
). Includes in-memory checkpointer implementation (MemorySaver
) for experimentation.langgraph_checkpoint_sqlite
: An implementation of LangGraph checkpointer that uses SQLite database. Ideal for experimentation and local workflows.langgraph_checkpoint_postgres
: Our advanced checkpointer that we wrote and optimized for Postgres in LangGraph Cloud is now open-sourced and available to the community to build upon. Ideal for using in production.
Checkpointer implementations can be used interchangeably, which lets users tailor their stateful LangGraph applications to their custom needs.
LangGraph Postgres Checkpointer for production-ready apps
langgraph_checkpoint_postgres
implementation can serve as a blueprint for community members to implement their own optimized, production-ready checkpointers for their favorite database. Postgres checkpointer implements a number of optimizations both on the write-, as well as read-side.
Write-side optimizations:
- We're making use of Postgres pipeline mode to reduce database roundtrips
- We're storing each channel value separately and versioned so that each new checkpoint only stores the values that changed.
Read-side optimizations:
- We're making use of a cursor for the list endpoint in order to efficiently fetch long thread histories when needed.
Getting started on LangGraph v0.2
Since LangGraph checkpointer libraries are implemented as namespace packages, you can import checkpointer interfaces and implementations the same way as before, using:
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver
Since SQLite and Postgres checkpointers are provided via separate libraries, you will need to install them using pip install langgraph-checkpoint-sqlite
or pip install langgraph-checkpoint-postgres
.
LangGraph checkpoint libraries will follow semantic versioning (starting with current release of 1.0), and any breaking changes in the main library will result in a major version bump for those libraries. For example, the next breaking change in langgraph_checkpoint
will result in 2.0 version, and you can expect the checkpointer implementations (e.g.,langgraph_checkpoint_sqlite
) to also be updated to 2.0 to follow that change.
To get started, follow this guide on [how to use checkpointers in LangGraph](https://langchain-ai.github.io/langgraph/how-tos/persistence/?ref=blog.langchain.com). You can also check out our documentation, including a [reference](https://langchain-ai.github.io/langgraph/reference/checkpoints/?ref=blog.langchain.com) and [overview](https://langchain-ai.github.io/langgraph/concepts/low_level/?ref=blog.langchain.com#send) of checkpointers.
Run agents at scale with LangGraph Cloud
To complement the LangGraph framework, we also have a new runtime, [LangGraph Cloud](https://langchain-ai.github.io/langgraph/cloud/?ref=blog.langchain.com), which provides infrastructure purpose-built for deploying agents at scale.
LangGraph Cloud does the heavy lifting for your agentic application, removing the maintenance work for custom checkpointers while adding fault-tolerant scalability. It gracefully manages horizontally-scaling task queues, servers, and includes our robust Postgres checkpointer out-of-the-box to help you handle many concurrent users and efficiently store large states and threads.
In addition, LangGraph Cloud supports real-world interaction patterns beyond streaming and human-in-the-loop. These include double-texting to handle new user inputs on currently-running threads of the graph, async background jobs for long-running tasks, and cron jobs.
Lastly, you can easily deploy your agentic app and collaborate in LangGraph Studio, a playground-like space for visualizing and debugging agent trajectories, with LangGraph Cloud. The [LangGraph Studio desktop app](https://blog.langchain.com/langgraph-studio-the-first-agent-ide/) is now also available for all LangSmith users to try for free.
LangGraph Cloud is now available in beta for all LangSmith users on Plus or Enterprise plans. Try it out today for free [by signing up for LangSmith](https://smith.langchain.com/?ref=blog.langchain.com).
Additional changes in LangGraph v0.2
LangGraph v0.2 contains many improvements, and we've designed it to be largely backwards compatible. Below is a list of breaking changes and deprecations in this latest version.
Breaking changes
LangGraph v0.2 introduces several breaking changes:
thread_ts
andparent_ts
have been renamed tocheckpoint_id
andparent_checkpoint_id
, respectively (vialanggraph_checkpoint==1.0.0
).- Note: LangGraph checkpointers still recognize
thread_ts
if passed via config and treat it ascheckpoint_id
- Note: LangGraph checkpointers still recognize
- Re-exported imports like
from langgraph.checkpoint import BaseCheckpointSaver
are no longer possible due to the use of namespace packages. Instead, usefrom langgraph.checkpoint.base import BaseCheckpointSaver
- SQLite checkpointers have been moved to a separate library, so you’ll need to install them separately using
pip install langgraph-checkpoint-sqlite
Deprecations
In LangGraph v0.2, we've removed:
langgraph.prebuilt.chat_agent_executor.create_function_calling_executor
. We recommend you uselanggraph.prebuilt.chat_agent_executor.create_react_agent
instead.langgraph.prebuilt.agent_executor
. We recommend you uselanggraph.prebuilt.chat_agent_executor.create_react_agent
instead.
Conclusion
We are incredibly grateful to our community and users for pushing us and building with LangGraph to improve agent reliability. We hope that with LangGraph v0.2, you’ll find it easier to build and maintain your own checkpointer implementations– and we’re excited to see all the apps that you create.
As you try out LangGraph v0.2, we'd love to hear your feedback at hello@langchain.dev. You can also learn more from these additional resources: