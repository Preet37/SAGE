# Source: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
# Title: Structured outputs — Claude API Docs
# Fetched via: trafilatura
# Date: 2026-04-09

Model capabilities
Get validated JSON results from agent workflows
Structured outputs constrain Claude's responses to follow a specific schema, ensuring valid, parseable output for downstream processing. Two complementary features are available:
- JSON outputs (
output_config.format
): Get Claude's response in a specific JSON format - Strict tool use (
strict: true
): Guarantee schema validation on tool names and inputs
These features can be used independently or together in the same request.
Structured outputs are generally available on the Claude API and Amazon Bedrock for [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.6, Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Opus 4.5, and Claude Haiku 4.5. Structured outputs are in beta on Microsoft Foundry. Structured outputs are not supported on Google Cloud's Vertex AI for Claude Mythos Preview.
This feature qualifies for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention) with limited technical retention. See the [Data retention](#data-retention) section for details on what is retained and why.
Migrating from beta? The output_format
parameter has moved to output_config.format
, and beta headers are no longer required. The old beta header (structured-outputs-2025-11-13
) and output_format
parameter will continue working for a transition period. See code examples below for the updated API shape.
Was this page helpful?
Why use structured outputs
Without structured outputs, Claude can generate malformed JSON responses or invalid tool inputs that break your applications. Even with careful prompting, you may encounter:
- Parsing errors from invalid JSON syntax
- Missing required fields
- Inconsistent data types
- Schema violations requiring error handling and retries
Structured outputs guarantee schema-compliant responses through constrained decoding:
- Always valid: No more
JSON.parse()
errors - Type safe: Guaranteed field types and required fields
- Reliable: No retries needed for schema violations
JSON outputs
JSON outputs control Claude's response format, ensuring Claude returns valid JSON matching your schema. Use JSON outputs when you need to:
- Control Claude's response format
- Extract data from images or text
- Generate structured reports
- Format API responses
Quick start
curl https://api.anthropic.com/v1/messages \
-H "content-type: application/json" \
-H "x-api-key: $ANTHROPIC_API_KEY" \
-H "anthropic-version: 2023-06-01" \
-d '{
"model": "claude-opus-4-6",
"max_tokens": 1024,
"messages": [
{
"role": "user",
"content": "Extract the key information from this email: John Smith ([[email protected]](/cdn-cgi/l/email-protection)) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
}
],
"output_config": {
"format": {
"type": "json_schema",
"schema": {
"type": "object",
"properties": {
"name": {"type": "string"},
"email": {"type": "string"},
"plan_interest": {"type": "string"},
"demo_requested": {"type": "boolean"}
},
"required": ["name", "email", "plan_interest", "demo_requested"],
"additionalProperties": false
}
}
}
}'
Response format: Valid JSON matching your schema in response.content[0].text
Output
{
"name": "John Smith",
"email": "[[email protected]](/cdn-cgi/l/email-protection)",
"plan_interest": "Enterprise",
"demo_requested": true
}
How it works
Define your JSON schema
Create a JSON schema that describes the structure you want Claude to follow. The schema uses standard JSON Schema format with some limitations (see
[JSON Schema limitations](#json-schema-limitations)).Add the output_config.format parameter
Include the
output_config.format
parameter in your API request withtype: "json_schema"
and your schema definition.Parse the response
Claude's response is valid JSON matching your schema, returned in
response.content[0].text
.
Working with JSON outputs in SDKs
The SDKs provide helpers that make it easier to work with JSON outputs, including schema transformation, automatic validation, and integration with popular schema libraries.
SDK helper methods (like .parse()
and Pydantic/Zod integration) still accept output_format
as a convenience parameter. The SDK handles the translation to output_config.format
internally. The examples below show the SDK helper syntax.
Using native schema definitions
Instead of writing raw JSON schemas, you can use familiar schema definition tools in your language:
- Python:
[Pydantic](https://docs.pydantic.dev/)models withclient.messages.parse()
- TypeScript:
[Zod](https://zod.dev/)schemas withzodOutputFormat()
- Java: Plain Java classes with automatic schema derivation via
outputConfig(Class<T>)
- Ruby:
Anthropic::BaseModel
classes withoutput_config: {format: Model}
- CLI, C#, Go, PHP: Raw JSON schemas passed via
output_config
{ read -r _ NAME; read -r _ EMAIL; } < <(
ant messages create \
--transform 'content.0.text|@fromstr|{name,email}' --format yaml <<'YAML'
model: claude-opus-4-6
max_tokens: 1024
messages:
- role: user
content: >-
Extract the key information from this email: John Smith
([[email protected]](/cdn-cgi/l/email-protection)) is interested in our Enterprise plan and wants
to schedule a demo for next Tuesday at 2pm.
output_config:
format:
type: json_schema
schema:
type: object
properties:
name: {type: string}
email: {type: string}
plan_interest: {type: string}
demo_requested: {type: boolean}
required: [name, email, plan_interest, demo_requested]
additionalProperties: false
YAML
)
printf '%s (%s)\n' "$NAME" "$EMAIL"
SDK-specific methods
Each SDK provides helpers that make working with structured outputs easier. See individual SDK pages for full details.
How SDK transformation works
The Python and TypeScript SDKs automatically transform schemas with unsupported features:
- Remove unsupported constraints (e.g.,
minimum
,maximum
,minLength
,maxLength
) - Update descriptions with constraint info (e.g., "Must be at least 100"), when the constraint is not directly supported with structured outputs
- Add
additionalProperties: false
to all objects - Filter string formats to supported list only
- Validate responses against your original schema (with all constraints)
This means Claude receives a simplified schema, but your code still enforces all constraints through validation.
Example: A Pydantic field with minimum: 100
becomes a plain integer in the sent schema, but the description is updated to "Must be at least 100", and the SDK validates the response against the original constraint.
Common use cases
Strict tool use
For enforcing JSON Schema compliance on tool inputs with grammar-constrained sampling, see [Strict tool use](/docs/en/agents-and-tools/tool-use/strict-tool-use).
Using both features together
JSON outputs and strict tool use solve different problems and can be used together:
- JSON outputs control Claude's response format (what Claude says)
- Strict tool use validates tool parameters (how Claude calls your functions)
When combined, Claude can call tools with guaranteed-valid parameters AND return structured JSON responses. This is useful for agentic workflows where you need both reliable tool calls and structured final outputs.
ant messages create <<'YAML'
model: claude-opus-4-6
max_tokens: 1024
messages:
- role: user
content: Help me plan a trip to Paris departing May 15, 2026
# JSON outputs: structured response format
output_config:
format:
type: json_schema
schema:
type: object
properties:
summary:
type: string
next_steps:
type: array
items:
type: string
required: [summary, next_steps]
additionalProperties: false
# Strict tool use: guaranteed tool parameters
tools:
- name: search_flights
strict: true
input_schema:
type: object
properties:
destination:
type: string
date:
type: string
format: date
required: [destination, date]
additionalProperties: false
YAML
Important considerations
Grammar compilation and caching
Structured outputs use constrained sampling with compiled grammar artifacts. This introduces some performance characteristics to be aware of:
- First request latency: The first time you use a specific schema, there is additional latency while the grammar compiles
- Automatic caching: Compiled grammars are cached for 24 hours from last use, making subsequent requests much faster
- Cache invalidation: The cache is invalidated if you change:
- The JSON schema structure
- The set of tools in your request (when using both structured outputs and tool use)
- Changing only
name
ordescription
fields does not invalidate the cache
Prompt modification and token costs
When using structured outputs, Claude automatically receives an additional system prompt explaining the expected output format. This means:
- Your input token count is slightly higher
- The injected prompt costs you tokens like any other system prompt
- Changing the
output_config.format
parameter will invalidate any[prompt cache](/docs/en/build-with-claude/prompt-caching)for that conversation thread
JSON Schema limitations
Structured outputs support standard JSON Schema with some limitations. Both JSON outputs and strict tool use share these limitations.
The Python and TypeScript SDKs can automatically transform schemas with unsupported features by removing them and adding constraints to field descriptions. See [SDK-specific methods](#sdk-specific-methods) for details.
Property ordering
When using structured outputs, properties in objects maintain their defined ordering from your schema, with one important caveat: required properties appear first, followed by optional properties.
For example, given this schema:
{
"type": "object",
"properties": {
"notes": { "type": "string" },
"name": { "type": "string" },
"email": { "type": "string" },
"age": { "type": "integer" }
},
"required": ["name", "email"],
"additionalProperties": false
}
The output will order properties as:
name
(required, in schema order)email
(required, in schema order)notes
(optional, in schema order)age
(optional, in schema order)
This means the output might look like:
{
"name": "John Smith",
"email": "[[email protected]](/cdn-cgi/l/email-protection)",
"notes": "Interested in enterprise plan",
"age": 35
}
If property order in the output is important to your application, ensure all properties are marked as required, or account for this reordering in your parsing logic.
Invalid outputs
While structured outputs guarantee schema compliance in most cases, there are scenarios where the output may not match your schema:
Refusals (stop_reason: "refusal"
)
Claude maintains its safety and helpfulness properties even when using structured outputs. If Claude refuses a request for safety reasons:
- The response has
stop_reason: "refusal"
- You'll receive a 200 status code
- You'll be billed for the tokens generated
- The output may not match your schema because the refusal message takes precedence over schema constraints
Token limit reached (stop_reason: "max_tokens"
)
If the response is cut off due to reaching the max_tokens
limit:
- The response has
stop_reason: "max_tokens"
- The output may be incomplete and not match your schema
- Retry with a higher
max_tokens
value to get the complete structured output
Schema complexity limits
Structured outputs work by compiling your JSON schemas into a grammar that constrains Claude's output. More complex schemas produce larger grammars that take longer to compile. To protect against excessive compilation times, the API enforces several complexity limits.
Explicit limits
The following limits apply to all requests with output_config.format
or strict: true
:
| Limit | Value | Description |
|---|---|---|
| Strict tools per request | 20 | Maximum number of tools with strict: true . Non-strict tools don't count toward this limit. |
| Optional parameters | 24 | Total optional parameters across all strict tool schemas and JSON output schemas. Each parameter not listed in required counts toward this limit. |
| Parameters with union types | 16 | Total parameters that use anyOf or type arrays (e.g., "type": ["string", "null"] ) across all strict schemas. These are especially expensive because they create exponential compilation cost. |
These limits apply to the combined total across all strict schemas in a single request. For example, if you have 4 strict tools with 6 optional parameters each, you'll reach the 24-parameter limit even though no single tool seems complex.
Additional internal limits
Beyond the explicit limits above, there are additional internal limits on the compiled grammar size. These limits exist because schema complexity doesn't reduce to a single dimension: features like optional parameters, union types, nested objects, and number of tools interact with each other in ways that can make the compiled grammar disproportionately large.
When these limits are exceeded, you'll receive a 400 error with the message "Schema is too complex for compilation." These errors mean the combined complexity of your schemas exceeds what can be efficiently compiled, even if each individual limit above is satisfied. As a final stop-gap, the API also enforces a compilation timeout of 180 seconds. Schemas that pass all explicit checks but produce very large compiled grammars may hit this timeout.
Tips for reducing schema complexity
If you're hitting complexity limits, try these strategies in order:
-
Mark only critical tools as strict. If you have many tools, reserve it for tools where schema violations cause real problems, and rely on Claude's natural adherence for simpler tools.
-
Reduce optional parameters. Make parameters
required
where possible. Each optional parameter roughly doubles a portion of the grammar's state space. If a parameter always has a reasonable default, consider making it required and having Claude provide that default explicitly. -
Simplify nested structures. Deeply nested objects with optional fields compound the complexity. Flatten structures where possible.
-
Split into multiple requests. If you have many strict tools, consider splitting them across separate requests or sub-agents.
For persistent issues with valid schemas, [contact support](https://support.claude.com/en/articles/9015913-how-to-get-support) with your schema definition.
Data retention
Prompts and responses are processed with ZDR when using structured outputs. However, the JSON schema itself is temporarily cached for up to 24 hours since last use for optimization purposes. No prompt or response data is retained beyond the API response.
Structured outputs are HIPAA eligible, but PHI must not be included in JSON schema definitions. The API compiles JSON schemas into grammars that are cached separately from message content, and these cached schemas do not receive the same PHI protections as prompts and responses. Do not include PHI in schema property names, enum
values, const
values, or pattern
regular expressions. PHI should only appear in message content (prompts and responses), where it is protected under HIPAA safeguards.
For ZDR and HIPAA eligibility across all features, see [API and data retention](/docs/en/build-with-claude/api-and-data-retention).
Feature compatibility
Works with:
[Batch processing](/docs/en/build-with-claude/batch-processing): Process structured outputs at scale with 50% discount[Token counting](/docs/en/build-with-claude/token-counting): Count tokens without compilation[Streaming](/docs/en/build-with-claude/streaming): Stream structured outputs like normal responses- Combined usage: Use JSON outputs (
output_config.format
) and strict tool use (strict: true
) together in the same request
Incompatible with:
[Citations](/docs/en/build-with-claude/citations): Citations require interleaving citation blocks with text, which conflicts with strict JSON schema constraints. Returns 400 error if citations enabled withoutput_config.format
.- Message Prefilling: Incompatible with JSON outputs
Grammar scope: Grammars apply only to Claude's direct output, not to tool use calls, tool results, or thinking tags (when using [Extended Thinking](/docs/en/build-with-claude/extended-thinking)). Grammar state resets between sections, allowing Claude to think freely while still producing structured output in the final response.