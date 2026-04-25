# Source: https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle
# Title: Lifecycle / stdio — Model Context Protocol Specification (2025-06-18)
# Fetched via: trafilatura
# Date: 2026-04-09

- Initialization: Capability negotiation and protocol version agreement
- Operation: Normal protocol communication
- Shutdown: Graceful termination of the connection
Lifecycle Phases
Initialization
The initialization phase MUST be the first interaction between client and server. During this phase, the client and server:- Establish protocol version compatibility
- Exchange and negotiate capabilities
- Share implementation details
initialize
request containing:
- Protocol version supported
- Client capabilities
- Client implementation information
initialized
notification
to indicate it is ready to begin normal operations:
- The client SHOULD NOT send requests other than
[pings](/specification/2025-06-18/basic/utilities/ping)before the server has responded to theinitialize
request. - The server SHOULD NOT send requests other than
[pings](/specification/2025-06-18/basic/utilities/ping)and[logging](/specification/2025-06-18/server/utilities/logging)before receiving theinitialized
notification.
Version Negotiation
In theinitialize
request, the client MUST send a protocol version it supports.
This SHOULD be the latest version supported by the client.
If the server supports the requested protocol version, it MUST respond with the same
version. Otherwise, the server MUST respond with another protocol version it
supports. This SHOULD be the latest version supported by the server.
If the client does not support the version in the server’s response, it SHOULD
disconnect.
If using HTTP, the client MUST include the
MCP-Protocol-Version: <protocol-version>
HTTP header on all subsequent requests to the MCP
server.
For details, see [the Protocol Version Header section in Transports](/specification/2025-06-18/basic/transports#protocol-version-header).Capability Negotiation
Client and server capabilities establish which optional protocol features will be available during the session. Key capabilities include:| Category | Capability | Description |
|---|---|---|
| Client | roots | Ability to provide filesystem
|
sampling
[sampling](/specification/2025-06-18/client/sampling)requestselicitation
[elicitation](/specification/2025-06-18/client/elicitation)requestsexperimental
prompts
[prompt templates](/specification/2025-06-18/server/prompts)resources
[resources](/specification/2025-06-18/server/resources)tools
[tools](/specification/2025-06-18/server/tools)logging
[log messages](/specification/2025-06-18/server/utilities/logging)completions
[autocompletion](/specification/2025-06-18/server/utilities/completion)experimental
listChanged
: Support for list change notifications (for prompts, resources, and tools)subscribe
: Support for subscribing to individual items’ changes (resources only)
Operation
During the operation phase, the client and server exchange messages according to the negotiated capabilities. Both parties MUST:- Respect the negotiated protocol version
- Only use capabilities that were successfully negotiated
Shutdown
During the shutdown phase, one side (usually the client) cleanly terminates the protocol connection. No specific shutdown messages are defined—instead, the underlying transport mechanism should be used to signal connection termination:stdio
For the stdio[transport](/specification/2025-06-18/basic/transports), the client SHOULD initiate shutdown by:
- First, closing the input stream to the child process (the server)
- Waiting for the server to exit, or sending
SIGTERM
if the server does not exit within a reasonable time - Sending
SIGKILL
if the server does not exit within a reasonable time afterSIGTERM
HTTP
For HTTP[transports](/specification/2025-06-18/basic/transports), shutdown is indicated by closing the associated HTTP connection(s).
Timeouts
Implementations SHOULD establish timeouts for all sent requests, to prevent hung connections and resource exhaustion. When the request has not received a success or error response within the timeout period, the sender SHOULD issue a[cancellation notification](/specification/2025-06-18/basic/utilities/cancellation)for that request and stop waiting for a response. SDKs and other middleware SHOULD allow these timeouts to be configured on a per-request basis. Implementations MAY choose to reset the timeout clock when receiving a
[progress notification](/specification/2025-06-18/basic/utilities/progress)corresponding to the request, as this implies that work is actually happening. However, implementations SHOULD always enforce a maximum timeout, regardless of progress notifications, to limit the impact of a misbehaving client or server.
Error Handling
Implementations SHOULD be prepared to handle these error cases:- Protocol version mismatch
- Failure to negotiate required capabilities
- Request
[timeouts](#timeouts)