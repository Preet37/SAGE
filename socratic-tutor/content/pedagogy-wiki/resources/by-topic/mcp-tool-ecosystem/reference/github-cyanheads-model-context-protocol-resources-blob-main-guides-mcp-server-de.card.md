# Card: MCP stdio server end-to-end wiring (TypeScript SDK)
**Source:** https://github.com/cyanheads/model-context-protocol-resources/blob/main/guides/mcp-server-development-guide.md  
**Role:** code | **Need:** WORKING_EXAMPLE  
**Anchor:** End-to-end stdio server setup pattern using MCP SDK (newline-delimited JSON-RPC on stdin/stdout; stderr-only logging) with concrete server + transport wiring.

## Key Content
- **Protocol/transport constraints (stdio):**
  - MCP uses **JSON-RPC 2.0**; messages are **newline-delimited** over stdio.
  - **stdin**: only MCP messages in. **stdout**: only MCP messages out. **stderr**: logging.
- **Initialization lifecycle rule (critical):**
  - Before initialization completes, **only `ping` requests** and **server `logging` notifications** are permitted; **all other requests are forbidden** until client sends `initialized`.
- **JSON-RPC message requirements (table):**
  - **Request:** `jsonrpc:"2.0"`, **id required** (string/number), `method` required, `params` optional.
  - **Response:** `jsonrpc:"2.0"`, **id matches request**, exactly one of `result` or `error`.
  - **Notification:** `jsonrpc:"2.0"`, `method` required, **id forbidden**.
- **Concrete stdio server procedure (TypeScript):**
  1. Create `McpServer({ name, version }, { capabilities: { tools: { listChanged: false }}})`.
  2. Register a tool via `server.tool("greet", z.object({ name: z.string().min(1) }), async (input)=>({ content:[{type:"text", text:`Hello, ${input.name}! Welcome to MCP.`}] }))`.
  3. Create transport: `const transport = new StdioServerTransport();`
  4. Start: `await server.connect(transport);` and **log to stderr**.
- **Manual test command (exact):**
  - `echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"greet","arguments":{"name":"World"}}}' | node build/index.js`
- **Defaults/parameters (project setup):**
  - Node target: **ES2022**, TS module: **NodeNext**, output dir `./build`, root `./src`.
  - Example deps: `@modelcontextprotocol/sdk` **^1.11.0**, `zod` **^3.24.1**.

## When to surface
Use when a student asks how to implement or debug an MCP **stdio** server, especially message formatting, initialization ordering, or correct server/transport wiring in the TypeScript SDK.