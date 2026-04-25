# Source: https://platform.openai.com/docs/guides/tools
# Author: OpenAI
# Author Slug: openai
# Title: OpenAI API Docs — Tools (tool calling, tool_choice, parallel tool calls, structured outputs)
# Fetched via: browser
# Date: 2026-04-10

Starter app

Experiment with built-in tools in the Responses API.

Copy Page
More page actions

When generating model responses or building agents, you can extend capabilities using built‑in tools, function calling, tool search, and remote MCP servers. These enable the model to search the web, retrieve from your files, load deferred tool definitions at runtime, call your own functions, or access third‑party services. Only gpt-5.4 and later models support tool_search.

Web search
File search
Tool search
Function calling
Remote MCP
Include web search results for the model response
javascript
1
2
3
4
5
6
7
8
9
10
11
12

import OpenAI from "openai";
const client = new OpenAI();

const response = await client.responses.create({
    model: "gpt-5",
    tools: [
        { type: "web_search" },
    ],
    input: "What was a positive news story from today?",
});

console.log(response.output_text);
Available tools

Here’s an overview of the tools available in the OpenAI platform—select one of them for further guidance on usage.

Function calling

Call custom code to give the model access to additional data and capabilities.

Web search

Include data from the Internet in model response generation.

Remote MCP servers

Give the model access to new capabilities via Model Context Protocol (MCP) servers.

Skills

Upload and reuse versioned skill bundles in hosted shell environments.

Shell

Run shell commands in hosted containers or in your own local runtime.

Computer use

Create agentic workflows that enable a model to control a computer interface.

Image generation

Generate or edit images using GPT Image.

File search

Search the contents of uploaded files for context when generating a response.

Tool search

Dynamically load relevant tools into the model’s context to optimize token usage.

Usage in the API

When making a request to generate a model response, you usually enable tool access by specifying configurations in the tools parameter. Each tool has its own unique configuration requirements—see the Available tools section for detailed instructions.

Based on the provided prompt, the model automatically decides whether to use a configured tool. For instance, if your prompt requests information beyond the model’s training cutoff date and web search is enabled, the model will typically invoke the web search tool to retrieve relevant, up-to-date information.

Some advanced workflows can also load more tool definitions during the interaction. For example, tool search can defer function definitions until the model decides they’re needed.

You can explicitly control or guide this behavior by setting the tool_choice parameter in the API request.

Usage in the Agents SDK

In the Agents SDK, the tool semantics stay the same, but the wiring moves into the agent definition and workflow design rather than a single Responses API request.

Attach hosted tools, function tools, or hosted MCP tools directly on the agent when one specialist should call them itself.
Expose a specialist as a tool when a manager should stay in control of the user-facing reply.
Keep shell, apply patch, and computer-use harnesses in your runtime even when the SDK models the tool decision.
Wrap local logic as a function tool
typescript
1
2
3
4
5
6
7
8
9
10
11

import { tool } from "@openai/agents";
import { z } from "zod";

const getWeatherTool = tool({
  name: "get_weather",
  description: "Get the weather for a given city.",
  parameters: z.object({ city: z.string() }),
  async execute({ city }) {
    return `The weather in ${city} is sunny.`;
  },
});
Expose a specialist as a tool
typescript
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16

import { Agent } from "@openai/agents";

const summarizer = new Agent({
  name: "Summarizer",
  instructions: "Generate a concise summary of the supplied text.",
});

const mainAgent = new Agent({
  name: "Research assistant",
  tools: [
    summarizer.asTool({
      toolName: "summarize_text",
      toolDescription: "Generate a concise summary of the supplied text.",
    }),
  ],
});

Use Agent definitions when you are shaping a single specialist, Orchestration and handoffs when tools affect ownership, Guardrails and human review when tools affect approvals, and Integrations and observability when the capability comes from MCP.