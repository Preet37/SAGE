# Card: MCP Transport Norms (stdio + Streamable HTTP)
**Source:** https://modelcontextprotocol.io/specification/2025-06-18/basic/transports  
**Role:** reference_doc | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Normative MCP transport definitions: stdio subprocess lifecycle + Streamable HTTP (POST/GET, SSE), JSON-RPC framing, sessions, resumability, security, version header.

## Key Content
- **stdio transport**
  - Client **launches server as subprocess**.
  - Server reads JSON-RPC from **stdin**, writes JSON-RPC to **stdout**.
  - **Framing:** each message is a single JSON-RPC request/notification/response **delimited by newline**; messages **MUST NOT contain embedded newlines**.
  - Server **MAY** log UTF‑8 to **stderr**.
  - Server **MUST NOT** write anything to **stdout** that isn’t a valid MCP message; client **MUST NOT** write anything to **stdin** that isn’t a valid MCP message.

- **Streamable HTTP transport (replaces HTTP+SSE from 2024‑11‑05)**
  - Server **MUST** expose a **single MCP endpoint path** supporting **POST and GET** (e.g., `https://example.com/mcp`).
  - **Security:** validate **Origin** header (DNS rebinding); local servers **SHOULD** bind to **127.0.0.1** not `0.0.0.0`; **SHOULD** authenticate.
  - **Client → server:** each JSON-RPC message = **new HTTP POST**.
    - Client **MUST** send `Accept: application/json, text/event-stream`.
    - POST body **MUST** be a **single** JSON-RPC msg.
    - If input is **response/notification** and accepted: **202 Accepted** (no body); else HTTP error (e.g., **400**), body **MAY** be JSON-RPC error **without id**.
    - If input is a **request**: server returns either `Content-Type: text/event-stream` (SSE) or `application/json` (single JSON); client **MUST** support both.
    - SSE behavior: stream **SHOULD** include the response; server **MAY** send related requests/notifications before responding; **SHOULD NOT** close before response unless session expires; **SHOULD** close after response.
    - Disconnects **SHOULD NOT** imply cancellation; cancel via **CancelledNotification**.
  - **Server → client listening:** client **MAY** `GET` with `Accept: text/event-stream`; server returns SSE or **405**.
    - On GET SSE: server **MAY** send requests/notifications; **MUST NOT** send responses unless **resuming** a prior stream.
  - **Multiple SSE streams:** client **MAY** keep multiple; server **MUST NOT** broadcast same JSON-RPC message on multiple streams.
  - **Resumability:** server **MAY** set SSE `id`; if present, **MUST** be globally unique within session (or client). Client **SHOULD** resume with `Last-Event-ID`; server **MAY** replay only messages from that same stream; **MUST NOT** replay messages from other streams.
  - **Sessions:** server **MAY** issue `Mcp-Session-Id` on InitializeResult response; ID **SHOULD** be globally unique + cryptographically secure; **MUST** be visible ASCII **0x21–0x7E**. If issued, client **MUST** include `Mcp-Session-Id` on subsequent requests. Missing required session ID → **400**. Terminated session → **404**; on 404 client **MUST** start new session (new InitializeRequest w/o session ID). Client **SHOULD** `DELETE` with `Mcp-Session-Id` to end session; server **MAY** return **405**.
  - **Protocol version header (HTTP):** client **MUST** send `MCP-Protocol-Version: <version>` (e.g., `2025-06-18`). If missing and server can’t infer, server **SHOULD** assume **2025-03-26**. Invalid/unsupported version → **400**.

## When to surface
Use when students ask how MCP messages are framed/delimited, how stdio vs HTTP transports work, how SSE streaming/resume/session/versioning is handled, or what MUST/SHOULD requirements apply for robust tool-use loops and error recovery.