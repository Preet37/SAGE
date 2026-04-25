# Source: https://modelcontextprotocol.io/specification/2025-06-18/server/tools
# Title: Tools — Model Context Protocol Specification (2025-06-18)
# Fetched via: trafilatura
# Date: 2026-04-09

User Interaction Model
Tools in MCP are designed to be model-controlled, meaning that the language model can discover and invoke tools automatically based on its contextual understanding and the user’s prompts. However, implementations are free to expose tools through any interface pattern that suits their needs—the protocol itself does not mandate any specific user interaction model.Capabilities
Servers that support tools MUST declare thetools
capability:
listChanged
indicates whether the server will emit notifications when the list of
available tools changes.
Protocol Messages
Listing Tools
To discover available tools, clients send atools/list
request. This operation supports
[pagination](/specification/2025-06-18/server/utilities/pagination). Request:
Calling Tools
To invoke a tool, clients send atools/call
request:
Request:
List Changed Notification
When the list of available tools changes, servers that declared thelistChanged
capability SHOULD send a notification:
Message Flow
Data Types
Tool
A tool definition includes:name
: Unique identifier for the tooltitle
: Optional human-readable name of the tool for display purposes.description
: Human-readable description of functionalityinputSchema
: JSON Schema defining expected parametersoutputSchema
: Optional JSON Schema defining expected output structureannotations
: optional properties describing tool behavior
Tool Result
Tool results may contain[structured](#structured-content)or unstructured content. Unstructured content is returned in the
content
field of a result, and can contain multiple content items of different types:
All content types (text, image, audio, resource links, and embedded resources)
support optional
[annotations](/specification/2025-06-18/server/resources#annotations)that provide metadata about audience, priority, and modification times. This is the same annotation format used by resources and prompts.Text Content
Image Content
Audio Content
Resource Links
A tool MAY return links to[Resources](/specification/2025-06-18/server/resources), to provide additional context or data. In this case, the tool will return a URI that can be subscribed to or fetched by the client:
[Resource annotations](/specification/2025-06-18/server/resources#annotations)as regular resources to help clients understand how to use them.
Resource links returned by tools are not guaranteed to appear in the results
of a
resources/list
request.Embedded Resources
[Resources](/specification/2025-06-18/server/resources)MAY be embedded to provide additional context or data using a suitable
[URI scheme](./resources#common-uri-schemes). Servers that use embedded resources SHOULD implement the
resources
capability:
[Resource annotations](/specification/2025-06-18/server/resources#annotations)as regular resources to help clients understand how to use them.
Structured Content
Structured content is returned as a JSON object in thestructuredContent
field of a result.
For backwards compatibility, a tool that returns structured content SHOULD also return the serialized JSON in a TextContent block.
Output Schema
Tools may also provide an output schema for validation of structured results. If an output schema is provided:- Servers MUST provide structured results that conform to this schema.
- Clients SHOULD validate structured results against this schema.
- Enabling strict schema validation of responses
- Providing type information for better integration with programming languages
- Guiding clients and LLMs to properly parse and utilize the returned data
- Supporting better documentation and developer experience
Error Handling
Tools use two error reporting mechanisms:-
Protocol Errors: Standard JSON-RPC errors for issues like:
- Unknown tools
- Invalid arguments
- Server errors
-
Tool Execution Errors: Reported in tool results with
isError: true
:- API failures
- Invalid input data
- Business logic errors
Security Considerations
-
Servers MUST:
- Validate all tool inputs
- Implement proper access controls
- Rate limit tool invocations
- Sanitize tool outputs
-
Clients SHOULD:
- Prompt for user confirmation on sensitive operations
- Show tool inputs to the user before calling the server, to avoid malicious or accidental data exfiltration
- Validate tool results before passing to LLM
- Implement timeouts for tool calls
- Log tool usage for audit purposes