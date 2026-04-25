# Card: LangChain MCP client behavior & adapter patterns
**Source:** https://docs.langchain.com/oss/python/langchain/mcp  
**Role:** reference_doc | **Need:** COMPARISON_DATA  
**Anchor:** Concrete client integration behavior/defaults (stateless MultiServerMCPClient; per-invocation session lifecycle) + adapter-based tool/resource/prompt consumption.

## Key Content
- **Definition:** MCP is an open protocol standardizing how apps provide **tools + context** to LLMs; LangChain uses **langchain-mcp-adapters** (built on the official **MCP Python SDK**) to consume MCP servers.
- **Default client lifecycle (stateless):** `MultiServerMCPClient` is **stateless by default**: **each tool invocation** creates a **fresh `ClientSession`**, executes the tool, then **cleans up** (per-invocation session lifecycle).
- **Stateful sessions (procedure):** If you need persistent context across calls (stateful server), explicitly manage lifecycle by creating a persistent `ClientSession` via **`client.session()`** (controls MCP session lifecycle per MCP spec).
- **Transports (comparison + rationale):**
  - **HTTP / streamable-http:** Uses HTTP requests; supports **custom headers** via connection config `headers` (also supported for **SSE**, but SSE is **deprecated by MCP spec**).
  - **stdio:** Client launches server as a **subprocess** and communicates over stdin/stdout; **inherently stateful** because subprocess persists for lifetime of the connection. **However**, with `MultiServerMCPClient` **without explicit session management**, each tool call still creates a **new session**.
- **Auth mechanism:** Provide custom auth by implementing **`httpx.Auth`** (supported via MCP SDK).
- **Adapter conversions (how LangChain consumes MCP primitives):**
  - **Tools:** MCP tools → LangChain **tools**; load via **`client.get_tools()`**.
  - **Structured tool output:** If tool returns `structuredContent`, adapter wraps it as **`MCPToolArtifact`** accessible via `ToolMessage.artifact`; interceptors can transform/append it.
  - **Multimodal tool output:** Multi-part content (text/images) → LangChain **standard content blocks**; access via `ToolMessage.content_blocks`.
  - **Resources:** MCP resources → LangChain **`Blob`**; load via **`client.get_resources()`** (or `load_mcp_resources` with a session).
  - **Prompts:** MCP prompts → LangChain **messages**; load via **`client.get_prompt()`** (or `load_mcp_prompt` with a session).
- **Interceptors (design rationale):** MCP servers are separate processes and can’t access LangGraph runtime (store/context/state); **interceptors** provide middleware-like control (modify requests, retries, dynamic headers, short-circuit) and can return **`Command`** to update state/control flow (e.g., `goto="__end__"`).

## When to surface
Use when students ask how LangChain integrates with MCP servers (sessions, transports, headers/auth), or how MCP tools/resources/prompts map into LangChain objects (artifacts, content blocks, Blobs, interceptors).