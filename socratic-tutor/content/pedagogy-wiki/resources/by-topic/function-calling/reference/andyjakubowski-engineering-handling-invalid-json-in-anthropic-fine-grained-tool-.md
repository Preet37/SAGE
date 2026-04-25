# Source: https://andyjakubowski.com/engineering/handling-invalid-json-in-anthropic-fine-grained-tool-streaming
# Title: Handling invalid JSON in Anthropic's fine-grained tool streaming
# Fetched via: trafilatura
# Date: 2026-04-09

Handling invalid JSON in Anthropic’s fine-grained tool streaming
Practical strategies for repairing streamed tool calls
Here are a couple of things I learned while working with Anthropic’s fine-grained tool streaming.
At [Deepnote](https://deepnote.com/), we use [tools](https://ai-sdk.dev/docs/foundations/tools) to let AI models generate code in our customers’ notebooks. A model can call a tool by specifying its name and providing any necessary parameters you define. For example, a model might call a tool named create_code_block
with a code
parameter.
We care about 3 things when a model decides to call a tool:
- Quality: The generated code should be idiomatic and do what the customer asked for. We achieve this with a combination of evals, prompt engineering, and context building.
- Speed: The code should appear quickly in the UI. We solve this by streaming model tool calls and rendering partially generated code right away.
- Correctness: The tool call should be valid JSON that matches the tool’s schema. We do this by providing a
[Zod schema](https://zod.dev/api)(which gets converted to a JSON schema) for each tool.
Fine-grained tool streaming
Until recently, Anthropic models would always buffer and validate individual tool call parameters against the JSON schema before streaming them. This was a challenge for a parameter like code
because we wouldn’t receive tool call deltas for partially generated code, and couldn’t render them in the customer’s notebook. The customer would have to wait until the entire code block was generated before they could see anything.
Anthropic recently introduced a beta feature in their API called [fine-grained tool streaming](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/fine-grained-tool-streaming) to address this issue. When this feature is enabled, Anthropic won’t wait for the entire parameter to be generated before streaming it, and will instead stream deltas as they are generated. This lets us render partially generated code in the notebook right away, resulting in a snappier UX. You can enable this feature by adding the beta header anthropic-beta: fine-grained-tool-streaming-2025-05-14
to your HTTP request.
The trade-off is that the streamed deltas may not be valid JSON, and may not match the tool’s JSON schema. Unlike OpenAI’s [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs), Anthropic doesn’t guarantee that the partial or final JSON will be valid when using this beta feature. This means we need to handle invalid JSON deltas on our end.
Being able to quickly render partially generated code is a big win for our customers who chose Anthropic as their preferred AI provider at Deepnote, so we decided to adopt this feature despite the challenges. Here are the strategies we used to work with invalid JSON.
Simplify your JSON schema to minimize invalid JSON
We found that more complex JSON schemas made the model more likely to output incorrectly formatted JSON. For example, we let the model specify a insertAfterBlockId
parameter to control where in the notebook to insert the new code block. Our initial schema allowed a null
value to let the model insert a block at the top of a notebook:
"insertAfterBlockId": {
"type": ["string", "null"],
"description": "The ID of an existing block in the notebook that the new block should be inserted after, or `null` to insert the block at the top of the notebook."
}
However, this made the model output invalid JSON, where UUIDs were not wrapped in double quotes, resulting in a JSON parsing error at runtime:
// Invalid
"insertAfterBlockId": 123e4567-e89b-12d3-a456-426614174000
// Valid
"insertAfterBlockId": "123e4567-e89b-12d3-a456-426614174000"
We were able to mitigate this issue by only allowing string
values for this parameter, and letting the model use an empty string to indicate that the block should be inserted at the top of the notebook:
"insertAfterBlockId": {
"type": "string",
"description": "The ID of an existing block in the notebook that the new block should be inserted after, or an empty string to insert the block at the beginning of the notebook."
}
Repair accumulated tool call deltas before parsing
We accumulated tool call deltas into a string, then used [ untruncate-json](https://www.npmjs.com/package/untruncate-json) and
[to repair the JSON before parsing it. We didn’t repair individual deltas, just the accumulated tool call so far.](https://www.npmjs.com/package/jsonrepair)
jsonrepair
Repair the final tool call in middleware
Regardless of how you handle tool call deltas, the final tool call chunk you get from the model may still be invalid JSON. We use the [AI SDK](https://ai-sdk.dev/), and it would throw a [ AI_JSONParseError](https://ai-sdk.dev/docs/reference/ai-sdk-errors/ai-json-parse-error) before yielding the tool call chunk. The solution that worked for us was to add
[language model middleware](https://ai-sdk.dev/docs/ai-sdk-core/middleware)to intercept the final tool call chunk before AI SDK tries to parse it, and repair the JSON ourselves.
This could look something like this:
import { jsonrepair } from 'jsonrepair';
import untruncateJson from 'untruncate-json';
import type { LanguageModelV1Middleware, LanguageModelV1StreamPart } from 'ai';
/**
* Middleware that repairs malformed JSON arguments in Vercel AI SDK tool streams with `untruncate-json` and `jsonrepair`.
*/
export const repairToolArgsMiddleware: LanguageModelV1Middleware = {
wrapStream: async ({ doStream }) => {
const { stream, ...rest } = await doStream();
const transformStream = new TransformStream<
LanguageModelV1StreamPart,
LanguageModelV1StreamPart
>({
transform(chunk, controller) {
if (chunk.type === 'tool-call') {
try {
const argsTextJson = untruncateJson(chunk.args);
const argsTextJsonRepaired = jsonrepair(argsTextJson);
controller.enqueue({
...chunk,
args: argsTextJsonRepaired,
});
} catch (error) {
controller.enqueue(chunk);
}
} else {
// Don't modify other chunk types
controller.enqueue(chunk);
}
},
});
return {
stream: stream.pipeThrough(transformStream),
...rest,
};
},
};
In AI SDK, you can use middleware by wrapping your language model like this:
import { wrapLanguageModel } from 'ai';
// Create anthropic model
// ...
const wrappedLanguageModel = wrapLanguageModel({
model: anthropicModel,
middleware: repairToolArgsMiddleware,
});