# Source: https://blog.langchain.dev/why-langgraph-platform/
# Author: LangChain
# Author Slug: langchain
# Title: Why do I need LangGraph Platform for agent deployment?
# Fetched via: browser
# Date: 2026-04-10

Note: As of October 2025, LangGraph Platform has been re-named to "LangSmith Deployment".

Last we week, we announced the GA of LangGraph Platform, our deployment platform for long running, stateful, or bursty agents. This blog is a technical explanation of why a deployment platform for agents is needed and how we built it.

Intro

Over the past year we’ve seen companies like LinkedIn, Uber, Klarna, and Elastic successfully build agents with LangGraph. We increasingly have confidence that LangGraph’s high degree of control, built-in persistence layer, and human-in-the-loop features are the right abstractions for building reliable agents.

After an agent is built, it then time to deploy.

For some agents - deployment is easy. Specifically, if you have stateless agents that run quickly and at low volumes - then deployment isn’t that hard! You can run them as a lambda and all will be fine.

For other types of agents, however, deployment becomes trickier. Specifically, the longer running, more stateful, or more bursty your agent is, the more complicated you deployment will be.

Long Running Agents

Problem

For agents that take longer to process (e.g., hours), maintaining an open connection can be impractical.

How we solve it:

The LangGraph Server supports launching agent runs in the background and provides polling endpoints, streaming endpoints and webhooks to monitor run status effectively.

Problem

Regular server setups often encounter timeouts or disruptions when handling requests that take a long time to complete.

How we solve it

LangGraph Server’s API provides robust support for these tasks by sending regular heartbeat signals, preventing unexpected connection closures during prolonged processes. Additionally, stream endpoints can be rejoined if the connection drops, and will very soon buffer events emitted while you were disconnected.

Problem

The longer an agent runs for, the more likely it is to suffer an exception while running.

How we solve it

LangGraph Server implements strategies to both minimize the number of exceptions agents face (eg. by running them in workers which can use isolated event loops and background threads) as well as the amount of time needed to recover from an exception (eg. when an agent fails it is retried a configurable number of times, and each retry starts off from the most recent successful checkpoint).

Problem

The longer an agent runs for, the more you need intermediate output to be emitted while the agent is running, to show the end user that something is happening.

How we solve it

LangGraph Server implements multiple streaming modes, including intermediate results, token-by-token LLM messages, all the way to streaming of custom payloads emitted by your nodes. Streaming events are emitted in realtime from the background workers that run the agents, with minimal latency, giving you a unique combo of durable execution with realtime output. Multiple consumers can connect to the output stream of the same agent, and these connections can be re-established if dropped by the client or intermediate networking layers.

Bursty Agents

Problem

Certain applications, especially those with real-time user interaction, may experience "bursty" request loads where numerous requests hit the server simultaneously.

How we solve it

LangGraph Server includes a task queue, ensuring requests are handled consistently without loss, even under heavy loads. LangGraph Server is designed to scale horizontally on both the server and queue components. This scaling is transparent to you, and doesn’t require complicated load balancing, as all server instances are stateless, and all server instances can communicate with all worker instances to support real-time streaming and cancellation. You can add as many queue instances as needed to handle your desired throughput, and they will all share the queued runs fairly, without ever executing the same run more than once.

Problem

Some of types of bursty applications that are also stateful (see below) may let the user send multiple messages rapidly, without the agent having finished responding to the first one. This “double texting” can disrupt agent flows if not handled properly.

How we solve it

LangGraph Server offers four built-in strategies to address and manage such interactions.

Stateful Agents

Problem

There are several levels of statefulness. There is both short-term and long-term memory. Then there is human-in-the-loop (pausing at an arbitrary point in your graph until you get back human input). On top of that, there is human-on-the-loop (time travel) - letting users go back to a previous state of the graph, modify it, and resume from there.

There are also different shapes of state. The most simple one is just a list of messages. Most agents, however, have more complicated state than that.

The more of these stateful operations you want to support, and the more complex your state, then the more complicated it is to properly set up infrastructure to enable this.

How we solve it

LangGraph Platform includes optimized checkpointers and a memory store, managing state across sessions without the need for custom solutions.

LangGraph Server provides specialized endpoints for human-in-the-loop scenarios, simplifying the integration of manual oversight into agent workflows.

Problem

The more your agent is used, the more memory is used to store conversations and memories that may no longer be relevant.

How we solve it

LangGraph Server supports attaching TTLs (time-to-live) to both conversation threads as well as long-term memory entries, which will be cleared from memory by the platform when they expire.

Conclusion

By using LangGraph Platform, you gain access to a robust, scalable deployment solution that mitigates these challenges, saving you the effort of implementing and maintaining them manually. This allows you to focus more on building effective agent behavior and less on solving deployment infrastructure issues.

To get started, read about our deployment options here. You can also check out our announcement LangGraph Platform's general availability to learn more.

JOIN OUR NEWSLETTER

Updates from the LangChain team and community

Enter your email
Subscribe