# Source: https://microsoft.github.io/autogen/0.2/docs/reference/
# Author: Microsoft
# Author Slug: microsoft
# Title: AutoGen 0.2 API Reference (index)
# Fetched via: search
# Date: 2026-04-09

# Introduction to AutoGen
Welcome!
AutoGen is an open-source framework that leverages multiple
*agents* to enable complex workflows.
This tutorial introduces basic concepts and building blocks of AutoGen.
## Why AutoGen?
​
...
While there are many definitions of agents, in AutoGen, an agent is an
entity that can send messages, receive messages and generate a reply
using models, tools, human inputs or a mixture of them.
This abstraction
not only allows agents to model real-world and abstract entities, such
as people and algorithms, but it also simplifies implementation of
complex workflows as collaboration among agents.
Further, AutoGen is extensible and composable: you can extend a simple
agent with customizable components and create workflows that can combine
these agents and power a more sophisticated agent, resulting in
implementations that are modular and easy to maintain.
Most importantly, AutoGen is developed by a vibrant community of
researchers and engineers.
It incorporates the latest research in
multi-agent systems and has been used in many real-world applications,
including agent platform, advertising, AI employees, blog/article
writing, blockchain, calculate burned areas by wildfires, customer
support, cybersecurity, data analytics, debate, education, finance,
gaming, legal consultation, research, robotics, sales/marketing, social
simulation, software engineering, software security, supply chain,
t-shirt design, training data generation, Youtube service…
## Installation ​
The simplest way to install AutoGen is from pip:
`pip install autogen-agentchat~=0.2`.
Find more options in
Installation.
## Agents ​
In AutoGen, an agent is an entity that can send and receive messages to
and from other agents in its environment.
An agent can be powered by
models (such as a large language model like GPT-4), code executors (such
as an IPython kernel), human, or a combination of these and other
pluggable and customizable components.
An example of such agents is the built-in `ConversableAgent` which
supports the following components:
1. A list of LLMs
...
3. A function and tool executor
4. A component for keeping human-in-the-loop
You can switch each component on or off and customize it to suit the
need of your application.
For advanced users, you can add additional
components to the agent by using
`registered_reply`.
LLMs, for example, enable agents to converse in natural languages and
transform between structured and unstructured text.
The following
...
from autogen import ConversableAgent
agent = ConversableAgent(
"chatbot",
llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ.get("OPENAI_API_KEY")}]},
code_execution_config=False, # Turn off code execution, by default it is off.
...
human_input_mode="NEVER", # Never ask for human input.
...
The `llm_config` argument contains a list of configurations for the
...
You can ask this agent to generate a response to a question using the
`generate_reply` method:
```
reply = agent.generate_reply(messages=[{"content": "Tell me a joke.", "role": "user"}])
print(reply)
```
```
...
In AutoGen, you can assign roles to agents and have them participate in
conversations or chat with each other.
A conversation is a sequence of
messages exchanged between agents.
You can then use these conversations
to make progress on a task.
For example, in the example below, we assign
different roles to two agents by setting their `system_message`.
```
cathy = ConversableAgent(
...
Now that we have two comedian agents, we can ask them to start a comedy
show.
This can be done using the `initiate_chat` method.
We set the
`max_turns` to 2 to keep the conversation short.
```
result = joe.initiate_chat(cathy, message="Cathy, tell me a joke.", max_turns=2)
```
```
joe (to cathy):
...
In this chapter, we introduced the concept of agents, roles and
conversations in AutoGen.
For simplicity, we only used LLMs and created
fully autonomous agents (`human_input_mode` was set to `NEVER`).
In the

# Getting Started
AutoGen is an open-source programming framework for building AI agents and facilitating cooperation among multiple agents to solve tasks.
AutoGen aims to provide an easy-to-use and flexible framework for accelerating development and research on agentic AI, like PyTorch for Deep Learning.
It offers features such as agents that can converse with other agents, LLM and tool use support, autonomous and human-in-the-loop workflows, and multi-agent conversation patterns.
### Main Features​
- AutoGen enables building next-gen LLM applications based on multi-agent conversations with minimal effort.
It simplifies the orchestration, automation, and optimization of a complex LLM workflow.
It maximizes the performance of LLM models and overcomes their weaknesses.
- It supports diverse conversation patterns for complex workflows.
With customizable and conversable agents, developers can use AutoGen to build a wide range of conversation patterns concerning conversation autonomy, the number of agents, and agent conversation topology.
- It provides a collection of working systems with different complexities.
These systems span a wide range of applications from various domains and complexities.
This demonstrates how AutoGen can easily support diverse conversation patterns.
AutoGen is powered by collaborative research studies from Microsoft, Penn State University, and University of Washington.
### Quickstart​
```
pip install autogen-agentchat~=0.2
```
- No code execution
- Local execution
- Docker execution
```
import os
from autogen import AssistantAgent, UserProxyAgent
llm_config = { "config_list": [{ "model": "gpt-4", "api_key": os.environ.get("OPENAI_API_KEY") }] }
assistant = AssistantAgent("assistant", llm_config=llm_config)
user_proxy = UserProxyAgent("user_proxy", code_execution_config=False)
# Start the chat
user_proxy.initiate_chat(
assistant,
message="Tell me a joke about NVDA and TESLA stock prices.",
```
When asked, be sure to check the generated code before continuing to ensure it is safe to run.
...
import autogen
from autogen import AssistantAgent, UserProxyAgent
llm_config = {"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}
assistant = AssistantAgent("assistant", llm_config=llm_config)
user_proxy = UserProxyAgent(
"user_proxy", code_execution_config={"executor": autogen.coding.LocalCommandLineCodeExecutor(work_dir="coding")}
# Start the chat
user_proxy.initiate_chat(
assistant,
message="Plot a chart of NVDA and TESLA stock price change YTD.",
```
```
import os
import autogen
from autogen import AssistantAgent, UserProxyAgent
llm_config = {"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}
with autogen.coding.DockerCommandLineCodeExecutor(work_dir="coding") as code_executor:
assistant = AssistantAgent("assistant", llm_config=llm_config)
user_proxy = UserProxyAgent(
"user_proxy", code_execution_config={"executor": code_executor}
...
# Start the chat
user_proxy.initiate_chat(
assistant,
message="Plot a chart of NVDA and TESLA stock price change YTD.
Save the plot to a file called plot.png",
)
```
…
```
coding/plot.png
```
…
#### Multi-Agent Conversation Framework​
Autogen enables the next-gen LLM applications with a generic multi-agent conversation framework.
It offers customizable and conversable agents which integrate LLMs, tools, and humans.
By automating chat among multiple capable agents, one can easily make them collectively perform tasks autonomously or with human feedback, including tasks that require using tools via code.
For example,
The figure below shows an example conversation flow with AutoGen.
### Where to Go Next?​
- Go through the tutorial to learn more about the core concepts in AutoGen
- Read the examples and guides in the notebooks section
- Understand the use cases for multi-agent conversation and enhanced LLM inference
- Read the API docs
- Learn about research around AutoGen
- Follow on Twitter
- See our roadmaps

AutoGen is an open-source programming framework for building AI agents and facilitating cooperation among multiple agents to solve tasks.
AutoGen aims to provide an easy-to-use and flexible framework for accelerating development and research on agentic AI.
Over the past year, our work on AutoGen has highlighted the transformative potential of agentic AI in addressing real-world challenges through agents and multi-agent applications.
Building on this progress, we are excited to announce AutoGen v0.4—a significant milestone shaped by learning and valuable feedback from our community of users and developers.
This update represents a complete redesign of the AutoGen library, aimed at improving code quality, robustness, generality, and the scalability of agentic workflows.
The initial release of AutoGen generated widespread interest in agentic technologies.
At the same time, users faced challenges scaling applications due to limited support for dynamic workflows and debugging tools.
Feedback highlighted the need for stronger observability, more flexible collaboration patterns, and for reusable components.
AutoGen v0.4 addresses these issues with its asynchronous, event-driven architecture.
AutoGen v0.4 adopts a more robust, asynchronous, and event-driven architecture, enabling a broader range of agentic scenarios with stronger observability, more flexible collaboration patterns, and for reusable components.
## Key Features
- **Asynchronous messaging**: Agents communicate through asynchronous messages, supporting both event-driven and request/response interaction patterns.
- **Modular and extensible**: Users can easily customize systems with pluggable components, including custom agents, tools, memory, and models.
They can also build proactive and long-running agents.
- **Observability and debugging**: Built-in tools provide tracking, tracing, and debugging agent interactions and workflows, with support for OpenTelemetry for industry-standard observability.
- **Scalable and distributed**: Users can design complex, distributed agent networks that operate seamlessly across organizational boundaries.
- **Built-in and community extensions**: The extensions module enhances the framework’s functionality with advanced model clients, agents, multi-agent teams, and tools for agentic workflows.
Support for community extensions allows open-source developers to manage their own extensions.
- **Cross-language support**: This update enables interoperability between agents built in different programming languages, with current support for Python and .NET and additional languages in development.
- **Full type support**: Interfaces now enforce type checks at build time, ensuring robust and cohesive code quality.

# AutoGen
AutoGen is an open-source framework that was released initially by Microsoft.
AutoGen focuses on enabling conversational and collaborative autonomous AI agents.
It provides a flexible architecture for building multi-agent systems with an emphasis on asynchronous, event-driven interactions between agents for complex autonomous workflows.
## Key features of AutoGen
AutoGen provides the following key features:
- **Conversational agents** – Built around natural language conversations between autonomous agents, enabling sophisticated reasoning through dialogue.
For more information, see Multi-agent Conversation Framework in the AutoGen documentation.
- **Asynchronous architecture** – Event-driven design for non-blocking autonomous agent interactions, supporting complex parallel workflows.
For more information, see Solving Multiple Tasks in a Sequence of Async Chats in the AutoGen documentation.
- **Human-in-the-loop** – Strong support for optional human participation in otherwise autonomous agent workflows when needed.
For more information, see Allowing Human Feedback in Agents in the AutoGen documentation.
- **Code generation and execution** – Specialized capabilities for code-focused autonomous agents that can write and run code.
For more information, see Code Execution in the AutoGen documentation.
- **Customizable behaviors** – Flexible autonomous agent configuration and conversation control for diverse use cases.
For more information, see agentchat.conversable_agent in the AutoGen documentation.
- **Foundation model selection** – Support for various foundation models including Anthropic Claude, Amazon Nova models (Premier, Pro, Lite, and Micro) on Amazon Bedrock, and others for different autonomous reasoning capabilities.
For more information, see LLM Configuration in the AutoGen documentation.
- **LLM API integration** – Standardized configuration for multiple LLM service interfaces including Amazon Bedrock, OpenAI, and Azure OpenAI.
For more information, see oai.openai_utils in the AutoGen API Reference.
- **Multimodal processing** – Support for text and image processing to enable rich multimodal autonomous agent interactions.
For more information, see Engaging with Multimodal Models: GPT-4V in AutoGen in the AutoGen documentation.
## When to use AutoGen
AutoGen is particularly well-suited for autonomous agent scenarios
including:
- Applications that require natural conversational flows between autonomous
agents for complex reasoning
- Projects that need both fully autonomous operation and optional human
oversight capabilities
- Use cases that involve autonomous code generation, execution, and
debugging without human intervention
- Scenarios that require flexible, asynchronous autonomous agent
communication patterns
## Implementation approach for AutoGen
AutoGen provides a conversational implementation approach for
business stakeholders, as detailed in Getting Started in the AutoGen documentation.
The framework enables organizations to:
- Create autonomous agents that communicate through natural language
conversations.
- Implement asynchronous, event-driven interactions between multiple
agents.
- Combine fully autonomous operation with optional human oversight when
needed.
- Develop specialized agents for different business functions that
collaborate through dialogue.
This conversational approach makes the autonomous system's reasoning transparent
and accessible to business users.
Decision-makers can observe the dialogue between
agents to understand how conclusions are reached and optionally participate in the
conversation when human judgment is required.
## Real-world example of AutoGen
Magentic-One is an open‑source, generalist multi‑agent system
designed to autonomously solve complex, multi‑step tasks across diverse
environments, as described in the Microsoft AI Frontiers blog.
At its core is the Orchestrator agent, which decomposes high‑level goals and tracks progress by using structured ledgers.
This agent delegates subtasks to specialized agents (such as WebSurfer, FileSurfer, Coder, and ComputerTerminal) and adapts dynamically by re‑planning when necessary.
The system is built on the AutoGen framework and is model‑agnostic,
defaulting to GPT‑4o.
It achieves state‑of‑the‑art performance across benchmarks
like GAIA, AssistantBench, and
WebArena—all without task‑specific tuning.
Additionally, it
supports modular extensibility and rigorous evaluation through
AutoGenBench suggestions.

microsoft / **