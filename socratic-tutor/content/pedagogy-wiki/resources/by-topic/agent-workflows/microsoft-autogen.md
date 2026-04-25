# Source: https://microsoft.github.io/autogen/
# Fetched via: headless browser (Playwright)
# Downloaded: 2026-04-09
# Words: 219
# Author: Microsoft
# Author Slug: microsoft
AutoGen
A framework for building AI agents and applications
 Studio 

An web-based UI for prototyping with agents without writing code. Built on AgentChat.

pip install -U autogenstudio
autogenstudio ui --port 8080 --appdir ./myapp


Start here if you are new to AutoGen and want to prototype with agents without writing code.

Get Started

 AgentChat 

A programming framework for building conversational single and multi-agent applications. Built on Core. Requires Python 3.10+.
# pip install -U "autogen-agentchat" "autogen-ext[openai]"
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main() -> None:
    agent = AssistantAgent("assistant", OpenAIChatCompletionClient(model="gpt-4o"))
    print(await agent.run(task="Say 'Hello World!'"))

asyncio.run(main())


Start here if you are prototyping with agents using Python. Migrating from AutoGen 0.2?.

Get Started

 Core 

An event-driven programming framework for building scalable multi-agent AI systems. Example scenarios:

Deterministic and dynamic agentic workflows for business processes.

Research on multi-agent collaboration.

Distributed agents for multi-language applications.

Start here if you are getting serious about building multi-agent systems.

Get Started

 Extensions 

Implementations of Core and AgentChat components that interface with external services or other libraries. You can find and use community extensions or create your own. Examples of built-in extensions:

McpWorkbench for using Model-Context Protocol (MCP) servers.

OpenAIAssistantAgent for using Assistant API.

DockerCommandLineCodeExecutor for running model-generated code in a Docker container.

GrpcWorkerAgentRuntime for distributed agents.

Discover Community Extensions Create New Extension