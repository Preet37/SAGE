# Source: https://docs.langchain.com/oss/python/langchain/mcp
# Title: Model Context Protocol (MCP) - Docs by LangChain
# Fetched via: trafilatura
# Date: 2026-04-09

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction)is an open protocol that standardizes how applications provide tools and context to LLMs. LangChain agents can use tools defined on MCP servers using the
[library.](https://github.com/langchain-ai/langchain-mcp-adapters)
langchain-mcp-adapters
Quickstart
Install thelangchain-mcp-adapters
library:
langchain-mcp-adapters
enables agents to use tools defined across one or more MCP servers.
MultiServerMCPClient
is stateless by default. Each tool invocation creates a fresh MCP ClientSession
, executes the tool, and then cleans up. See the [stateful sessions](#stateful-sessions)section for more details.
Accessing multiple MCP servers
Custom servers
To create a custom MCP server, use the[FastMCP](https://gofastmcp.com/getting-started/welcome)library:
Transports
MCP supports different transport mechanisms for client-server communication.HTTP
Thehttp
transport (also referred to as streamable-http
) uses HTTP requests for client-server communication. See the [MCP HTTP transport specification](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http)for more details.
Passing headers
When connecting to MCP servers over HTTP, you can include custom headers (e.g., for authentication or tracing) using theheaders
field in the connection configuration. This is supported for sse
(deprecated by MCP spec) and streamable_http
transports.
Passing headers with MultiServerMCPClient
Authentication
Thelangchain-mcp-adapters
library uses the official [MCP SDK](https://github.com/modelcontextprotocol/python-sdk)under the hood, which allows you to provide a custom authentication mechanism by implementing the
httpx.Auth
interface.
stdio
Client launches server as a subprocess and communicates via standard input/output. Best for local tools and simple setups.Unlike HTTP transports,
stdio
connections are inherently stateful: the subprocess persists for the lifetime of the client connection. However, when using MultiServerMCPClient
without explicit session management, each tool call still creates a new session. See [stateful sessions](#stateful-sessions)for managing persistent connections.Stateful sessions
By default,MultiServerMCPClient
is stateless: each tool invocation creates a fresh MCP session, executes the tool, and then cleans up.
If you need to control the [lifecycle](https://modelcontextprotocol.io/specification/2025-03-26/basic/lifecycle)of an MCP session (for example, when working with a stateful server that maintains context across tool calls), you can create a persistent
ClientSession
using client.session()
.
Using MCP ClientSession for stateful tool usage
Core features
Tools
[Tools](https://modelcontextprotocol.io/docs/concepts/tools)allow MCP servers to expose executable functions that LLMs can invoke to perform actions—such as querying databases, calling APIs, or interacting with external systems. LangChain converts MCP tools into LangChain
[tools](/oss/python/langchain/tools), making them directly usable in any LangChain agent or workflow.
Loading tools
Useclient.get_tools()
to retrieve tools from MCP servers and pass them to your agent:
Structured content
MCP tools can return[structured content](https://modelcontextprotocol.io/specification/2025-03-26/server/tools#structured-content)alongside the human-readable text response. This is useful when a tool needs to return machine-parseable data (like JSON) in addition to text that gets shown to the model. When an MCP tool returns
structuredContent
, the adapter wraps it in an [and returns it as the tool’s artifact. You can access this using the](https://reference.langchain.com/python/langchain_mcp_adapters/#langchain_mcp_adapters.tools.MCPToolArtifact)
MCPToolArtifact
artifact
field on the ToolMessage
. You can also use [interceptors](#tool-interceptors)to process or transform structured content automatically. Extracting structured content from artifact After invoking your agent, you can access the structured content from tool messages in the response:
[interceptor](#tool-interceptors)to automatically append structured content to the tool result:
Multimodal tool content
MCP tools can return[multimodal content](https://modelcontextprotocol.io/specification/2025-03-26/server/tools#tool-result)(images, text, etc.) in their responses. When an MCP server returns content with multiple parts (e.g., text and images), the adapter converts them to LangChain’s
[standard content blocks](/oss/python/langchain/messages#standard-content-blocks). You can access the standardized representation via the
content_blocks
property on the ToolMessage
:
Resources
[Resources](https://modelcontextprotocol.io/docs/concepts/resources)allow MCP servers to expose data—such as files, database records, or API responses—that can be read by clients. LangChain converts MCP resources into
[Blob](https://reference.langchain.com/python/langchain_core/documents/#langchain_core.documents.base.Blob)objects, which provide a unified interface for handling both text and binary content.
Loading resources
Useclient.get_resources()
to load resources from an MCP server:
[directly with a session for more control:](https://reference.langchain.com/python/langchain_mcp_adapters/#langchain_mcp_adapters.resources.load_mcp_resources)
load_mcp_resources
Prompts
[Prompts](https://modelcontextprotocol.io/docs/concepts/prompts)allow MCP servers to expose reusable prompt templates that can be retrieved and used by clients. LangChain converts MCP prompts into
[messages](/oss/python/langchain/messages), making them easy to integrate into chat-based workflows.
Loading prompts
Useclient.get_prompt()
to load a prompt from an MCP server:
[directly with a session for more control:](https://reference.langchain.com/python/langchain_mcp_adapters/#langchain_mcp_adapters.prompts.load_mcp_prompt)
load_mcp_prompt
Advanced features
Tool interceptors
MCP servers run as separate processes—they can’t access LangGraph runtime information like the[store](/oss/python/langgraph/persistence#memory-store),
[context](/oss/python/langchain/context-engineering), or agent state. Interceptors bridge this gap by giving you access to this runtime context during MCP tool execution. Interceptors also provide middleware-like control over tool calls: you can modify requests, implement retries, add headers dynamically, or short-circuit execution entirely.
| Section | Description |
|---|---|
|
[State updates and commands](#state-updates-and-commands)Command
[Writing interceptors](#custom-interceptors)Accessing runtime context
When MCP tools are used within a LangChain agent (viacreate_agent
), interceptors receive access to the ToolRuntime
context. This provides access to the tool call ID, state, config, and store—enabling powerful patterns for accessing user data, persisting information, and controlling agent behavior.
- Runtime context
- Store
- State
- Tool call ID
Access user-specific configuration like user IDs, API keys, or permissions that are passed at invocation time:
Inject user context into MCP tool calls
[Context engineering](/oss/python/langchain/context-engineering)and
[Tools](/oss/python/langchain/tools).
State updates and commands
Interceptors can returnCommand
objects to update agent state or control graph execution flow. This is useful for tracking task progress, switching between agents, or ending execution early.
Mark task complete and switch agents
Command
with goto="__end__"
to end execution early:
End agent run on completion
Custom interceptors
Interceptors are async functions that wrap tool execution, enabling request/response modification, retry logic, and other cross-cutting concerns. They follow an “onion” pattern where the first interceptor in the list is the outermost layer. Basic pattern An interceptor is an async function that receives a request and a handler. You can modify the request before calling the handler, modify the response after, or skip the handler entirely.Basic interceptor pattern
request.override()
to create a modified request. This follows an immutable pattern, leaving the original request unchanged.
Modifying tool arguments
Dynamic header modification
Composing multiple interceptors
Retry on error
Error handling with fallback
Progress notifications
Subscribe to progress updates for long-running tool executions:Progress callback
CallbackContext
provides:
server_name
: Name of the MCP servertool_name
: Name of the tool being executed (available during tool calls)
Logging
The MCP protocol supports[logging](https://modelcontextprotocol.io/specification/2025-03-26/server/utilities/logging#log-levels)notifications from servers. Use the
Callbacks
class to subscribe to these events.
Logging callback
Elicitation
[Elicitation](https://modelcontextprotocol.io/specification/2025-11-25/client/elicitation#elicitation)allows MCP servers to request additional input from users during tool execution. Instead of requiring all inputs upfront, servers can interactively ask for information as needed.
Server setup
Define a tool that usesctx.elicit()
to request user input with a schema:
MCP server with elicitation
Client setup
Handle elicitation requests by providing a callback toMultiServerMCPClient
:
Handling elicitation requests
Response actions
The elicitation callback can return one of three actions:| Action | Description |
|---|---|
accept | User provided valid input. Include the data in the content field. |
decline | User chose not to provide the requested information. |
cancel | User cancelled the operation entirely. |
Response action examples
Additional resources
[Connect these docs](/use-these-docs)to Claude, VSCode, and more via MCP for real-time answers.