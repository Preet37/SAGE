# Source: https://platform.openai.com/docs/api-reference/streaming
# Author: OpenAI
# Author Slug: openai
# Title: Streaming support | OpenAI API Reference
# Fetched via: search
# Date: 2026-04-10

# Streaming API responses
By default, when you make a request to the OpenAI API, we generate the model's entire output before sending it back in a single HTTP response.
When generating long outputs, waiting for a response can take time.
Streaming responses lets you start printing or processing the beginning of the model's output while it continues generating the full response.
## Enable streaming
To start streaming responses, set
`stream=True` in your request to the Responses endpoint:
```
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
17
```import { OpenAI } from "openai";
const client = new OpenAI();
const stream = await client.responses.create({
model: "gpt-5",
input: [
role: "user",
content: "Say 'double bubble bath' ten times fast.",
},
],
stream: true,
});
for await (const event of stream) {
console.log(event);
```
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
```from openai import OpenAI
client = OpenAI()
stream = client.responses.create(
model="gpt-5",
input=[
"role": "user",
"content": "Say 'double bubble bath' ten times fast.",
},
],
stream=True,
for event in stream:
print(event)
The Responses API uses semantic events for streaming.
Each event is typed with a predefined schema, so you can listen for events you care about.
For a full list of event types, see the API reference for streaming.
Here are a few examples:
```
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
17
18
19
20
21
22
23
24
25
```type StreamingEvent =
| ResponseCreatedEvent
| ResponseInProgressEvent
| ResponseFailedEvent
| ResponseCompletedEvent
| ResponseOutputItemAdded
| ResponseOutputItemDone
| ResponseContentPartAdded
| ResponseContentPartDone
| ResponseOutputTextDelta
| ResponseOutputTextAnnotationAdded
| ResponseTextDone
| ResponseRefusalDelta
| ResponseRefusalDone
| ResponseFunctionCallArgumentsDelta
| ResponseFunctionCallArgumentsDone
| ResponseFileSearchCallInProgress
| ResponseFileSearchCallSearching
| ResponseFileSearchCallCompleted
| ResponseCodeInterpreterInProgress
| ResponseCodeInterpreterCallCodeDelta
| ResponseCodeInterpreterCallCodeDone
| ResponseCodeInterpreterCallInterpreting
| ResponseCodeInterpreterCallCompleted
| Error
## Read the responses
If you're using our SDK, every event is a typed instance.
You can also identity individual events using the
`type` property of the event.
Some key lifecycle events are emitted only once, while others are emitted multiple times as the response is generated.
Common events to listen for when streaming text are:
```
1
2
3
4
```- `response.created`
- `response.output_text.delta`
- `response.completed`
- `error`
For a full list of events you can listen for, see the API reference for streaming.
## Advanced use cases
For more advanced use cases, like streaming tool calls, check out the following dedicated guides:
## Moderation risk
Note that streaming the model's output in a production application makes it more difficult to moderate the content of the completions, as partial completions may be more difficult to evaluate.
This may have implications for approved usage.

By default, when you make a request to the OpenAI API, we generate the model’s entire output before sending it back in a single HTTP response.
When generating long outputs, waiting for a response can take time.
Streaming responses lets you start printing or processing the beginning of the model’s output while it continues generating the full response.
This guide focuses on HTTP streaming (`stream=true`) over server-sent events (SSE).
For persistent WebSocket transport with incremental inputs via `previous_response_id`, see the Responses API WebSocket mode.
## Enable streaming
To start streaming responses, set `stream=True` in your request to the Responses endpoint:
python
```
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
from openai import OpenAI
client = OpenAI()
stream = client.responses.create(
model="gpt-5",
input=[
{
"role": "user",
"content": "Say 'double bubble bath' ten times fast.",
},
],
stream=True,
)
for event in stream:
print(event)
```
The Responses API uses semantic events for streaming.
Each event is typed with a predefined schema, so you can listen for events you care about.
For a full list of event types, see the API reference for streaming.
Here are a few examples:
```
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
17
18
19
20
21
22
23
24
25
type StreamingEvent =
| ResponseCreatedEvent
| ResponseInProgressEvent
| ResponseFailedEvent
| ResponseCompletedEvent
| ResponseOutputItemAdded
| ResponseOutputItemDone
| ResponseContentPartAdded
| ResponseContentPartDone
| ResponseOutputTextDelta
| ResponseOutputTextAnnotationAdded
| ResponseTextDone
| ResponseRefusalDelta
| ResponseRefusalDone
| ResponseFunctionCallArgumentsDelta
| ResponseFunctionCallArgumentsDone
| ResponseFileSearchCallInProgress
| ResponseFileSearchCallSearching
| ResponseFileSearchCallCompleted
| ResponseCodeInterpreterInProgress
| ResponseCodeInterpreterCallCodeDelta
| ResponseCodeInterpreterCallCodeDone
| ResponseCodeInterpreterCallInterpreting
| ResponseCodeInterpreterCallCompleted
| Error
```
Streaming Chat Completions is fairly straightforward.
However, we recommend using the Responses API for streaming, as we designed it with streaming in mind.
The Responses API uses semantic events for streaming and is type-safe.
### Stream a chat completion
To stream completions, set `stream=True` when calling the Chat Completions or legacy Completions endpoints.
This returns an object that streams back the response as data-only server-sent events.
The response is sent back incrementally in chunks with an event stream.
You can iterate over the event stream with a `for` loop, like this:
python
```
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
17
18
from openai import OpenAI
client = OpenAI()
stream = client.chat.completions.create(
model="gpt-5",
messages=[
{
"role": "user",
"content": "Say 'double bubble bath' ten times fast.",
},
],
stream=True,
)
for chunk in stream:
print(chunk)
print(chunk.choices[0].delta)
print("****************")
```
## Read the responses
If you’re using our SDK, every event is a typed instance.
You can also identity individual events using the `type` property of the event.
Some key lifecycle events are emitted only once, while others are emitted multiple times as the response is generated.
Common events to listen for when streaming text are:
```
1
2
3
4
- `response.created`
- `response.output_text.delta`
- `response.completed`
- `error`
```
…
## Advanced use cases
For more advanced use cases, like streaming tool calls, check out the following dedicated guides:
...
Note that streaming the model’s output in a production application makes it more difficult to moderate the content of the completions, as partial completions may be more difficult to evaluate.
This may have implications for approved usage.

# Streaming
Streaming lets you subscribe to updates of the agent run as it proceeds.
This can be useful for showing the end-user progress updates and partial responses.
To stream, you can call
```
Runner.run_streamed()
```
…
```
result.stream_events()
```
gives you an async stream of
…
until the async iterator finishes.
A streaming run is not complete until the iterator ends, and post-processing such as session persistence, approval bookkeeping, or history compaction can finish after the last visible token arrives.
When the loop exits,
…
, etc) and data.
These events are useful if you want to stream response messages to the user as soon as they are generated.
Computer-tool raw events keep the same preview-vs-GA distinction as stored results.
Preview flows stream
…
, and the screenshot result comes back as
…
item.
For example, this will output the text generated by the LLM token-by-token.
```
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner
async def main():
agent = Agent(
name="Joker",
instructions="You are a helpful assistant.",
)
result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")
 async for event in result.stream_events():
if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
print(event.data.delta, end="", flush=True)
if __name__ == "__main__":
asyncio.run(main())
```
…
```
result = Runner.run_streamed(agent, "Delete temporary files if they are no longer needed.")
async for _event in result.stream_events():
pass
if result.interruptions:
state = result.to_state()
for interruption in result.interruptions:
state.approve(interruption)
result = Runner.run_streamed(agent, state)
async for _event in result.stream_events():
pass
```
…
. By default this stops the run immediately. To let the current turn finish cleanly before stopping, call
…
with that normalized input instead of appending a fresh user turn right away.
- If a streamed run stopped for tool approval, do not treat that as a new turn. Finish draining the stream, inspect
…
to customize how retrieved session history and the new user input are merged before the next model call. If you rewrite new-turn items there, the rewritten version is what gets persisted for that turn.
…
s are higher level events. They inform you when an item has been fully generated. This allows you to push progress updates at the level of "message generated", "tool ran", etc, instead of each token. Similarly,
…
```
is emitted when the Responses API returns the loaded subset.
For example, this will ignore raw events and stream updates to the user.
```
…
result = Runner.run_streamed(
 agent,
 input="Hello",
 )
 print("=== Run starting ===")
 async for event in result.stream_events():
…
print("=== Run complete ===")
if __name__ == "__main__":
 asyncio.run(main())

# Mastering the OpenAI Stream API: Real-Time AI for Developers
A comprehensive guide to the OpenAI Stream API.
Learn how to stream AI responses in real time with code samples, performance insights, and best practices for production use.
## Introduction to the OpenAI Stream API
The OpenAI API empowers developers to tap into state-of-the-art language models for a variety of applications, from chatbots to content generation.
As these models become more prevalent in real-time and interactive systems, the need for faster, more responsive outputs has grown.
The OpenAI Stream API addresses this demand by enabling streaming responses, allowing data to flow token-by-token instead of waiting for the entire completion.
This approach is crucial for developers and enterprises building real-time apps, conversational agents, or any system where latency and user experience matter.
With the OpenAI Stream API, applications can handle user queries more fluidly and deliver a seamless, interactive experience.
## How the OpenAI Stream API Works
Traditionally, APIs like the OpenAI completions API return a full response only after processing the entire request.
While this is straightforward, it can introduce latency—especially with large responses or complex prompts.
The OpenAI stream API changes this paradigm by introducing streaming: as soon as the model generates tokens, they're sent to the client incrementally, dramatically reducing perceived wait times.
When you use the
`stream=True` parameter, the OpenAI API streams response chunks over an HTTP connection via server-sent events (SSE).
Each chunk typically contains a small part of the model's output (for example, a few words or tokens), along with metadata like choices and finish_reason.
This allows applications to display responses as they're generated, vital for chatbots, real-time editors, live data processing, and more.
**Use Cases:** **Chatbots:**Users see AI-generated responses in real time, improving engagement.
...
## Setting Up and Authenticating with OpenAI Stream API
Before streaming with the OpenAI API, ensure you have:
- An OpenAI API key
- Appropriate SDKs installed (Python, Node.js, etc.)
- Environment variables set securely to protect credentials
**Installing the SDKs:** **Python:**
`bash pip install openai`
**Node.js:**
`bash npm install openai`
**Authentication Example:**
*Python*
```
python
import openai
import os
openai.api_key = os.environ[\"OPENAI_API_KEY\"]
```
*Node.js*
```
javascript
const { OpenAIApi, Configuration } = require(\"openai\");
const configuration = new Configuration({
apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);
```
This setup ensures secure, authenticated access to the OpenAI stream API for your applications.
## Making Streamed Requests with OpenAI API
### Basic Streaming Request Structure
A streamed request to the OpenAI stream API typically requires:
`model`: The specific model to use (e.g.,
`gpt-4`)
`messages`: Conversation history (for chat completions)
`stream`: Set to
`True`to enable streaming
- Optional:
`functions`or
`tool_calls`for advanced workflows
**Python Example: Streaming Chat Completion**
```
python
import openai
response = openai.ChatCompletion.create(
model=\"gpt-4\",
messages=[{"role": "user", "content": "Tell me a joke."}],
stream=True
for chunk in response:
print(chunk['choices'][0]['delta'].get('content', ''), end='', flush=True)
```
### Handling Streaming Responses
Streaming responses from the OpenAI API are sent as discrete JSON chunks.
Each chunk contains:
`delta`: The partial content or function call
`choices`: Array of completion choices
`finish_reason`: Indicates why the stream ended (
`stop`,
`length`, etc.)
To process a streamed response, loop through each chunk, extract the new content, and render or process it incrementally.
**Processing Streamed Chunks in Python**
```
python
full_reply = ""
for chunk in response:
delta = chunk['choices'][0]['delta']
if 'content' in delta:
full_reply += delta['content']
if chunk['choices'][0]['finish_reason']:
break
print(full_reply)
```
**Mermaid Diagram: Streaming Response Lifecycle**
## Advanced Streaming Techniques and Patterns
### Streaming to the Frontend (React/JS Example)
Often, you want to display streamed responses to users as they arrive.
This requires pushing data from your backend (where the OpenAI stream API response is handled) to the frontend in real time—commonly done with WebSockets or server-sent events.
**Node.js/Express Backend Streaming Example:**```javascript const express = require("express"); const { OpenAIApi, Configuration } = require("openai"); const app = express(); const configuration = new Configuration({ apiKey: process.env.OPENAI_API_KEY }); const openai = new OpenAIApi(configuration);
app.get('/stream', async (req, res) => { res.set({ 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', }); const completion = await openai.createChatCompletion({ model: "gpt-4", messages: [{ role: "user", content: "Stream a fun fact." }], stream: true, }, { responseType: 'stream' });
completion.data.on('data', data => { res.write(
`data: ${data}\n\n`);
});
completion.data.on('end', () => { res.end(); }); }); ```
**Frontend (React) Example:**
```
javascript
const [reply, setReply] = useState(\"\");
useEffect(() => {
const eventSource = new EventSource('/stream');
eventSource.onmessage = e => {
setReply(prev => prev + e.data);
};
return () => eventSource.close();
}, []);
```
This approach ensures users see content as soon as it's generated by the OpenAI stream API.
### Error Handling and Edge Cases
...
**Incomplete Streams:**Network interruptions can break streams; check for missing finish_reason.
**Indicates a natural end; handle other reasons (e.g.,**
`finish_reason: stop`:
`length`limits) gracefully.
**Function/Tool Calls:**When using OpenAI function calls, streamed chunks may contain partial function arguments—collect and assemble them correctly before execution.
**Moderation:**Streaming exposes partial completions; ensure robust moderation at both the chunk and full-response levels to avoid unsafe content leaks.
...
This is especially important in real-time apps, where even small delays can degrade user experience.
**Latency:**Streaming reduces perceived latency since users see a response unfold instantly, instead of waiting for a full reply.
**Cost:**Token usage is reported incrementally, allowing for precise cost monitoring, but total token consumption is similar to non-streaming modes.
**Best Practices:**
- Use streaming for chatbots and interactive UIs
- Monitor for dropped or incomplete streams in production
- Log token usage per session for cost tracking
## Real-World Examples and Use Cases
...
**Token Privacy:**Never log or expose sensitive prompts or completions; use encrypted storage for logs if needed **Moderation:**Always apply content moderation, even for partial (streamed) responses, to prevent unsafe content leaks **Compliance:**Ensure your use of the OpenAI stream API adheres to regulatory requirements (e.g., GDPR); avoid sending PII in prompts or completions
## Conclusion
The OpenAI stream API unlocks high-performance, real-time AI applications for developers and enterprises.
By streaming responses token by token, it enhances interactivity, reduces latency, and enables entirely new user experiences.
With robust error handling, security, and best practices, you can confidently bring the power of streaming AI to your next project.
Start experimenting today and transform your applications with the OpenAI stream API.

# Mastering openai-streams: Real-Time AI Output, Streaming API Integrations, and Best Practices
Unlock the full potential of openai-streams: dive into real-time OpenAI streaming API, code examples, advanced integrations, and best practices for developers.
...
As artificial intelligence rapidly evolves, the demand for real-time, responsive AI applications grows.
Enter
**openai-streams**—a powerful feature of the OpenAI API that enables developers to receive AI-generated output incrementally, as it is produced.
This technology is pivotal for applications that require immediate feedback, such as live chatbots, interactive coding tools, or dynamic market analysis agents.
By leveraging openai-streams, developers can craft seamless user experiences, minimize latency, and fully unlock the potential of real-time AI.
## Understanding the Concept of Streaming in openai-streams
### What is Streaming in the Context of OpenAI?
In traditional API calls, you submit a request and wait for the server to process and return the entire response.
With
**openai-streams**, however, the server sends back partial responses (chunks) as soon as they are generated.
This streaming capability means you do not need to wait for the full completion—your application can start processing and displaying results in real time.
### Streaming vs. Standard API Responses
**Standard Responses:**The API processes the entire request and then returns a single, complete response object.
Latency is higher and user feedback is delayed until completion.
**Streaming Responses:**The API sends data incrementally as it is generated, enabling immediate consumption and display.
This drastically reduces perceived latency and is ideal for interactive user experiences.
### Use Cases for Streaming Responses
**Conversational Chatbots:**Users see AI responses as they are typed out, mimicking human conversations.
...
## Setting Up openai-streams
### Prerequisites
To get started with openai-streams, you need:
- An OpenAI API key (sign up at
OpenAI)
- The appropriate OpenAI SDK/library for your language (e.g., Python, Node.js)
### Initializing the OpenAI API for Streaming
In Python, install the OpenAI SDK:
```
1pip install openai
2
```
Set your API key securely in your environment:
```
1export OPENAI_API_KEY=\"sk-...\"
2
```
### Basic Python Example for Enabling Streams
Here’s a minimal Python example to enable streaming with the OpenAI API:
```
1import openai
2
3openai.api_key = \"sk-...\"
4
5response = openai.ChatCompletion.create(
6 model=\"gpt-4\",
7 messages=[{"role": "user", "content": "Tell me a joke."}],
8 stream=True
9)
10
11for chunk in response:
12 print(chunk[\"choices\"][0][\"delta\"][\"content\"], end="", flush=True)
13
```
This code initiates a streaming chat completion, printing each chunk of content as it arrives.
## Deep Dive: How openai-streams Work
### Streaming Parameter and the API Call
The key to enabling streaming in OpenAI’s API is the
`stream` parameter.
When set to
`True`, the API returns a generator yielding data chunks as they are produced, rather than a single response object.
#### Handling Chunked Responses
Here’s how you can process chunked responses efficiently:
```
1def stream_chat_completion(messages):
2 for chunk in openai.ChatCompletion.create(
3 model=\"gpt-4\",
4 messages=messages,
5 stream=True
6 ):
7 if \"content\" in chunk[\"choices\"][0][\"delta\"]:
8 yield chunk[\"choices\"][0][\"delta\"][\"content\"]
9
10# Usage
11for part in stream_chat_completion([{\"role\": \"user\", \"content\": \"Summarize the news today.\"}]):
12 print(part, end="", flush=True)
13
```
This generator processes each streaming chunk, emitting content as soon as it’s available.
### Real-Time Data Processing with openai-streams
To build robust real-time applications, you must handle streaming data efficiently and implement error handling for network issues or API timeouts.
#### Robust Streaming Handler Example
```
1import time
2
3def robust_stream_chat_completion(messages, max_retries=3):
4 attempt = 0
5 while attempt < max_retries:
6 try:
7 for chunk in openai.ChatCompletion.create(
8 model=\"gpt-4\",
9 messages=messages,
10 stream=True
11 ):
12 if \"content\" in chunk[\"choices\"][0][\"delta\"]:
13 yield chunk[\"choices\"][0][\"delta\"][\"content\"]
14 break
15 except Exception as e:
16 print(f"Error: {e}. Retrying...")
17 attempt += 1
18 time.sleep(2 ** attempt)
19
```
This code adds exponential backoff retries for improved resilience.
### Mermaid Diagram: OpenAI Streaming Data Flow
...
2for event in agent_stream:
3 process_event(event) # Analyze streamed data
4 if urgent(event):
5 alert_mcp(event)
6
```
### Real-World Applications
...
Several open-source libraries further enhance the openai-streams developer experience:
**async-stream-openai-st:**Enables async/await syntax, making it easier to consume streaming responses in Python async applications.
**openai-stream-parser:**Aids in parsing and assembling streamed response chunks into coherent outputs.
**Ecosystem Tools:**Libraries like
`openai-node`(Node.js) or community SDKs provide additional integrations and streaming utilities.
These tools are particularly useful for developers building complex or high-throughput systems, where efficient streaming data handling is crucial.
## Best Practices and Security Considerations for openai-streams
### Efficient Resource Management
- Use efficient data buffers and avoid memory leaks when processing large streams.
- Close connections promptly when streaming is no longer needed.
- Limit concurrent streams to match your infrastructure’s capacity.
### Error Handling, Retries, and Timeouts
- Implement retry logic with exponential backoff for network failures.
- Set appropriate timeouts to prevent stalled connections.
- Monitor and log streaming errors for proactive issue resolution.
### Security and Privacy in Streamed Data
- Always use HTTPS for API communications.
- Sanitize and securely handle streamed data, especially if routed through remote servers.
- Avoid logging sensitive streamed content to prevent data leakage.
## Conclusion
openai-streams are revolutionizing real-time AI application development.
By enabling incremental, low-latency responses, they empower developers to create dynamic, interactive experiences.
As agentic applications and AI-driven systems become more prevalent, mastering openai-streams—and their integration with robust, secure infrastructure—will be crucial for future innovation.