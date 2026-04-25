# Source: https://platform.openai.com/docs/guides/streaming-responses?api-mode=responses
# Author: OpenAI
# Author Slug: openai
# Title: Streaming API responses - OpenAI API
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
model: "gpt-4.1",
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
…
```from openai import OpenAI
client = OpenAI()
stream = client.responses.create(
model="gpt-4.1",
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
…
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
| ResponseCodeInterpreterCallIntepreting
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
- Streaming function calls
- Streaming structured output
...
Note that streaming the model’s output in a production application makes it more difficult to moderate the content of the completions, as partial completions may be more difficult to evaluate.
This may have implications for approved usage.

# Streaming
Streaming lets you subscribe to updates of the agent run as it proceeds.
This can be useful for showing the end-user progress updates and partial responses.
To stream, you can call
…
until the async iterator finishes.
A streaming run is not complete until the iterator ends, and post-processing such as session persistence, approval bookkeeping, or history compaction can finish after the last visible token arrives.
When the loop exits,
…
are raw events passed directly from the LLM.
They are in OpenAI Responses API format, which means each event has a type (like
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
s are higher level events.
They inform you when an item has been fully generated.
This allows you to push progress updates at the level of "message generated", "tool ran", etc, instead of each token.
Similarly,
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

## What Is OpenAI’s Responses API?

The Responses API is OpenAI’s newest and most advanced API. It combines the strengths of the Chat Completions and Assistants APIs into a single streamlined interface. Released in March 2025, it maintains familiar capabilities while providing a more integrated approach to building AI applications.

The key innovation is how it simplifies development by automatically handling orchestration logic and natively integrating OpenAI’s built-in tools for web search and file search without requiring custom implementation.
In this tutorial, we’ll walk through how to use the Responses API in your projects. You’ll see how it handles text generation, works with images, and delivers streaming responses. We’ll examine the built-in tools that make development faster and more straightforward than before, showing you how these tools work together within the API’s framework.
By the end of this guide, you’ll understand when to use the Responses API instead of other OpenAI options and how this knowledge can help you build more efficient applications with less code and effort. If you’re new to the OpenAI API, check out our introductory course, Working with the OpenAI API, to start your journey developing AI-powered applications.

## Getting Started With the Responses API

The Responses API provides a more streamlined and user-friendly interface for interacting with OpenAI’s models, combining what previously required verbose and complex syntax into an elegant solution.

Before diving into specific use cases, let’s set up our environment and understand the basic syntax.
```
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```
This initialization step creates a client object that will handle all your API requests. The

…

### Generating content with the Responses API

The most straightforward use of the Responses API is generating text content. Let’s explore a real-world scenario: suppose you’re building an e-commerce platform and need to automatically generate compelling product descriptions based on basic product details.

Traditionally, this would require careful prompt engineering and multiple iterations. With the Responses API, you can create a simple function that handles this elegantly:
```
def generate_product_description(product_name, features, target_audience):
 response = client.responses.create(
 model="gpt-4o",
 instructions="You are a professional copywriter specialized in creating concise, compelling product descriptions. Focus on benefits rather than just features.",
 input=f"""
 Create a product description for {product_name}.
 Key features:
 - {features[0]}
 - {features[1]}
 - {features[2]}
 Target audience: {target_audience}
 Keep it under 150 words.
 """,
 temperature=0.7,
 max_output_tokens=200
 )

 return response.output_text

# Example usage
headphones_desc = generate_product_description(
 "NoiseGuard Pro Headphones",
 ["Active noise cancellation", "40-hour battery life", "Memory foam ear cushions"],
 "Business travelers and remote workers"

print(headphones_desc)
```

…

With just a few lines of code, we’ve created marketing-quality copy that would normally require a professional writer. The function is also reusable — just change the parameters, and you can generate descriptions for any product in your catalog.

This example demonstrates key patterns when using the Responses API:

1. The

…

parameter acts as a system prompt, defining the AI's behavior and context.
2. The

…

parameter limits response length, which helps control costs and ensure concise outputs.
4. The response object contains the generated text in the

…

#### Analyzing images for practical applications

Many real-world applications need to process both text and images. For instance, e-commerce platforms need to analyze product photos, content moderation systems need to review uploads, and social media apps need to understand visual content.

The Responses API excels at multimodal tasks like image analysis without requiring separate endpoints or complex integration code:
```
def analyze_product_image(image_url):
 response = client.responses.create(
 model="gpt-4o",
 instructions="You are a product photography expert and e-commerce consultant.",
 input=[
 {"role": "user", "content": "Analyze this product image and provide the following details:\n1. Product category\n2. Key visible features\n3. Potential quality issues\n4. Suggested improvements for the product photography"},
 {
 "role": "user",
 "content": [
 {
 "type": "input_image",
 "image_url": image_url
 }
 ],
 },
 ],
 temperature=0.2
 )

 return response.output_text

# Example with a sports team image
analysis = analyze_product_image("https://upload.wikimedia.org/wikipedia/commons/a/a5/Barcelona_fc_lamina_elgrafico.jpg")
print(analysis)
```

…

This function could be integrated into an e-commerce platform to automatically analyze product photos when merchants upload them. The system could provide immediate feedback about image quality and suggest improvements, ultimately leading to better conversion rates through higher quality listings — all without manual review.

When working with images, you should pass an array of message objects to the input parameter instead of a string, each with a role and content values.

…

### Implementing streaming for responsive applications

Users expect instant feedback. Waiting several seconds for an AI response can kill engagement — that’s why streaming is essential for creating responsive user experiences, especially in chat or real-time applications.

Imagine you’re building a customer feedback analysis tool for a product team. Instead of making them wait for the complete analysis, you can stream the results as they’re generated:
```
def analyze_customer_feedback(feedback_text):
 print("Analyzing customer feedback in real-time:")

 stream = client.responses.create(
 model="gpt-4o",
 instructions="Extract key sentiments, product issues, and actionable insights from this feedback.",
 input=feedback_text,
 stream=True,
 temperature=0.3,
 max_output_tokens=500
 )

 full_response = ""
 print("\nAnalysis results:")
 for event in stream:
 if event.type == "response.output_text.delta":
 print(event.delta, end="")
 full_response += event.delta
 elif event.type == "response.error":
 print(f"\nError occurred: {event.error}")

 return full_response

# Example with a complex customer review
feedback = """
I've been using the SmartHome Hub for about 3 months now. The voice recognition is fantastic
and the integration with my existing devices was mostly seamless. However, the app crashes
at least once a day, and the night mode feature often gets stuck until I restart the system.
Customer support was helpful but couldn't fully resolve the app stability issues.
"""

analysis_result = analyze_customer_feedback(feedback)
```
In a real application, you would replace the

The streaming implementation works by:

1. Setting

…

in the create method
2. Processing the response as an iterable of events with specific types
3. Handling different event types separately:

…

for errors

Now that we’ve covered the basic functionality of the Responses API, let’s explore its built-in tools that further enhance its capabilities.

…

```
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
 model="gpt-4o",
 tools=[{"type": "web_search_preview"}],
 input="What are some news related to the stock market?",

print(response.output_text)
```

…

### Computer use: interface interaction capabilities

Building on the foundation of text and document understanding, the computer use tool extends AI capabilities into the realm of interface interaction. This tool represents a significant advancement that bridges the gap between language understanding and user interface manipulation.

The computer use tool can perform a variety of interface interactions:

- Navigate websites and web applications autonomously.
- Fill out forms with appropriate information.
- Extract data from web pages and applications.
- Execute multi-step processes across different screens.
- Interact with elements like buttons, dropdowns, and text fields.
- Understand the context and purpose of different interface elements.
Potential applications include process automation for repetitive tasks, guided assistance for complex workflows, and accessibility improvements for users who have difficulty with traditional interfaces. The tool could be used to automate form filling, navigate complex websites, or perform testing of user interfaces.

The technology works by allowing the AI to see and interact with screen elements, understand context, and execute actions based on natural language instructions. This creates possibilities for automation and assistance that would otherwise require specialized development of interface-specific code.

…

1. You define functions that the AI can use, specifying parameters and their types.
2. The AI decides when to call these functions based on user queries.
3. Your code executes the functions with the AI-provided parameters.
4. You return the results to the AI, which incorporates them into its response.

…

#### Returning function results to the model

Finally, we send the results back to the model so it can generate a user-friendly response:
```
input_messages.append(tool_call) # append model's function call message
input_messages.append(
 { # append result message
 "type": "function_call_output",
 "call_id": tool_call.call_id,
 "output": json.dumps(conversion_result)
 }

response_2 = client.responses.create(
 model="gpt-4o",
 input=input_messages,
 tools=tools,

print(response_2.output_text)

```

…

### Putting everything together

In a real application, you’ll want to encapsulate this entire process into a single interface that handles the conversation flow seamlessly. Here’s how you might create a complete assistant that manages the entire function calling process:
```
def currency_assistant(user_message, conversation_history=None):
 """A complete assistant that handles currency conversion queries."""
 if conversation_history is None:
 conversation_history = []

 # Add the user's new message to the conversation
 conversation_history.append({"role": "user", "content": user_message})

 # Define available tools (our currency conversion function)
 tools = [{
 "type": "function",
 "name": "convert_currency",
 "description": "Convert an amount from one currency to another using current exchange rates",
 "parameters": {
 "type": "object",
 "properties": {
 "amount": {
 "type": "number",
 "description": "The amount of money to convert"
 },
 "from_currency": {
 "type": "string",
 "description": "The currency code to convert from (e.g., USD, EUR, GBP)"
 },
 "to_currency": {
 "type": "string",
 "description": "The currency code to convert to (e.g., USD, EUR, GBP)"
 }
 },
 "required": ["amount", "from_currency", "to_currency"],
 "additionalProperties": False
 },
 "strict": True
 }]

 # Get initial response from the model
 response = client.responses.create(
 model="gpt-4o",
 input=conversation_history,
 tools=tools,
 )

 # Check if the model wants to call a function
 if response.output and isinstance(response.output, list) and response.output[0].type == "function_call":
 tool_call = response.output[0]

 # Process the function call
 args = json.loads(tool_call.arguments)
 result = convert_currency(**args)

 # Add the function call and its result to the conversation
 conversation_history.append(tool_call)
 conversation_history.append({
 "type": "function_call_output",
 "call_id": tool_call.call_id,
 "output": json.dumps(result)
 })

 # Get the final response with the function results incorporated
 final_response = client.responses.create(
 model="gpt-4o",
 input=conversation_history,
 tools=tools,
 )

 return final_response.output_text, conversation_history
 else:
 # If no function call was needed, return the direct response
 return response.output_text, conversation_history

# Example usage
response, conversation = currency_assistant("How much is 50 British pounds in Australian dollars?")
print("Assistant:", response)

# Continue the conversation
response, conversation = currency_assistant("And what if I wanted to convert 200 Canadian dollars instead?", conversation)
print("Assistant:", response)
```
This implementation:

1. Maintains conversation history to provide context for follow-up questions.
2. Handles the entire process of function calling in a single interface.
3. Determines when function calling is necessary and when the model can respond directly.
4. Supports multi-turn conversations where previous context matters.

With this approach, you can create seamless conversational experiences where users interact naturally without being aware of the complex function calling happening behind the scenes. The assistant handles the transition between natural language understanding, structured function calls, and natural language generation.

…

Function calling enables the Responses API to connect natural language inputs with your services and data. This creates a bridge between user requests and your business systems, allowing users to make requests in plain language while your application handles the technical implementation details in the background.

Beyond function calling, another powerful capability of the Responses API is the ability to generate structured outputs. This feature complements function calling by providing a way to receive responses in specific formats that align with your application’s needs.

## Structured Outputs With the Responses API

When building AI applications, you often need responses in a specific format for easier integration with your systems. The Responses API supports structured outputs that enable you to receive data in a well-defined, consistent format rather than free-form text. This feature is particularly valuable when you need to:

1. Extract specific information from unstructured text.
2. Transform user inputs into structured data.
3. Ensure consistent response formats for downstream processing.
4. Integrate AI outputs directly with databases or APIs.

…

### Extracting product information from descriptions

Let’s explore a practical example: imagine you’re building an e-commerce platform and need to automatically extract product details from unstructured product descriptions to populate your database.

…

```
text={
 "format": {
 "type": "json_schema", # Specifies we're using JSON Schema
 "name": "product_details", # A descriptive name for this schema
 "schema": {
 # Your JSON Schema definition here
 "type": "object",
 "properties": {
 # Each property with type information, e.g.
 "product_name": {"type": "string"},
 # ... other properties
 },
 "required": ["product_name", ...], # All other properties
 "additionalProperties": False
 },
 "strict": True # Enforce schema constraints strictly
 }

```
The most important components are:

1. Schema definition: Describes the structure, including all properties and their types.
2. Required fields: Lists properties that must be included in the response.
3. Additional properties: When set to

…

```
from pydantic import BaseModel, Field
from typing import List, Optional
from openai import OpenAI

client = OpenAI()

class ProductDetails(BaseModel):
 product_name: str
 category: str = Field(default=None)
 features: List[str]
 specifications: Optional[dict] = None
 colors: List[str]
 pricing: dict

# With Chat Completions API
completion = client.beta.chat.completions.parse(
 model="gpt-4o",
 messages=[
 {"role": "system", "content": "Extract structured product information."},
 {"role": "user", "content": product_description}
 ],
 response_format=ProductDetails

pydantic_product = completion.choices[0].message.parsed
```

…

## Conclusion

The OpenAI Responses API simplifies how developers interact with language models by combining previous APIs’ strengths into a unified interface that requires less code and complexity. It supports text generation, image analysis, function calling, and structured outputs, making AI capabilities more accessible while allowing developers to focus on solving business problems instead of integration challenges.

As you continue your journey with the Responses API, you might find these additional resources helpful for deepening your understanding and expanding your implementation skills:

…

### How do I implement function calling with the Responses API?

**Implement function calling by defining functions with parameters and types, letting the model decide when to call them, executing the functions with model-provided parameters, and returning results to the model for incorporation into responses.**

# Guide: Stream OpenAI responses using the message-per-token pattern

Open in

This guide shows you how to stream AI responses from OpenAI's Responses API over Ably using the message-per-token pattern. Specifically, it implements the explicit start/stop events approach, which publishes each response token as an individual message, along with explicit lifecycle events to signal when responses begin and end.
Using Ably to distribute tokens from the OpenAI SDK enables you to broadcast AI responses to thousands of concurrent subscribers with reliable message delivery and ordering guarantees, ensuring that each client receives the complete response stream with all tokens delivered in order. This approach decouples your AI inference from client connections, enabling you to scale agents independently and handle reconnections gracefully.

## Prerequisites

To follow this guide, you need:

- Node.js 20 or higher
- An OpenAI API key
- An Ably API key

Useful links:

- OpenAI developer quickstart
- Ably JavaScript SDK getting started

Create a new Node project, which will contain the publisher and subscriber code:
```
mkdir ably-openai-example && cd ably-openai-example
npm init -y
```
Install the required packages using NPM:
```
npm install openai@^4 ably@^2
```
Export your OpenAI API key to the environment, which will be used later in the guide by the OpenAI SDK:
```
export OPENAI_API_KEY="your_api_key_here"
```

## Step 1: Get a streamed response from OpenAI

Initialize an OpenAI client and use the Responses API to stream model output as a series of events.

Create a new file `agent.mjs` with the following contents:

JavaScript

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

26

27
```
import OpenAI from 'openai';

// Initialize OpenAI client
const openai = new OpenAI();

// Process each streaming event
function processEvent(event) {
console.log(JSON.stringify(event));
// This function is updated in the next sections
}

// Create streaming response from OpenAI
async function streamOpenAIResponse(prompt) {
const stream = await openai.responses.create({
model: "gpt-5",
input: prompt,
stream: true,
});

// Iterate through streaming events
for await (const event of stream) {
processEvent(event);
}
}

// Usage example
streamOpenAIResponse("Tell me a short joke");
```

### Understand OpenAI streaming events

OpenAI's Responses API streams model output as a series of events when you set `stream: true`. Each streamed event includes a `type` property which describes the event type. A complete text response can be constructed from the following event types:
- `response.created`: Signals the start of a response. Contains `response.id` to correlate subsequent events.
- `response.output_item.added`: Indicates a new output item. If `item.type === "message"` the item contains model response text; other types may be specified, such as `"reasoning"` for internal reasoning tokens. The `output_index` indicates the position of this item in the response's `output` array.
- `response.content_part.added`: Indicates a new content part within an output item. If `part.type === "output_text"` the part contains model response text; other types may be specified, such as `"reasoning_text"` for internal reasoning tokens. The `content_index` indicates the position of this item in the output items's `content` array.
- `response.output_text.delta`: Contains a single token in the `delta` field. Use the `item_id`, `output_index`, and `content_index` to correlate tokens relating to a specific content part.
- `response.content_part.done`: Signals completion of a content part. Contains the complete `part` object with full text, along with `item_id`, `output_index`, and `content_index`.
- `response.output_item.done`: Signals completion of an output item. Contains the complete `item` object and `output_index`.
- `response.completed`: Signals the end of the response. Contains the complete `response` object.

The following example shows the event sequence received when streaming a response:

JSON

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

26

27

28

29

30

31

32
```
// 1. Response starts
{"type":"response.created","response":{"id":"resp_abc123","status":"in_progress"}}

// 2. First output item (reasoning) is added
{"type":"response.output_item.added","output_index":0,"item":{"id":"rs_456","type":"reasoning"}}
{"type":"response.output_item.done","output_index":0,"item":{"id":"rs_456","type":"reasoning"}}

// 3. Second output item (message) is added
{"type":"response.output_item.added","output_index":1,"item":{"id":"msg_789","type":"message"}}
{"type":"response.content_part.added","item_id":"msg_789","output_index":1,"content_index":0}

// 4. Text tokens stream in as delta events
{"type":"response.output_text.delta","item_id":"msg_789","output_index":1,"content_index":0,"delta":"Why"}
{"type":"response.output_text.delta","item_id":"msg_789","output_index":1,"content_index":0,"delta":" don"}
{"type":"response.output_text.delta","item_id":"msg_789","output_index":1,"content_index":0,"delta":"'t"}
{"type":"response.output_text.delta","item_id":"msg_789","output_index":1,"content_index":0,"delta":" scientists"}
{"type":"response.output_text.delta","item_id":"msg_789","output_index":1,"content_index":0,"delta":" trust"}
{"type":"response.output_text.delta","item_id":"msg_789","output_index":1,"content_index":0,"delta":" atoms"}
{"type":"response.output_text.delta","item_id":"msg_789","output_index":1,"content_index":0,"delta":"?"}
{"type":"response.output_text.delta","item_id":"msg_789","output_index":1,"content_index":0,"delta":" Because"}
{"type":"response.output_text.delta","item_id":"msg_789","output_index":1,"content_index":0,"delta":" they"}
{"type":"response.output_text.delta","item_id":"msg_789","output_index":1,"content_index":0,"delta":" make"}
{"type":"response.output_text.delta","item_id":"msg_789","output_index":1,"content_index":0,"delta":" up"}
{"type":"response.output_text.delta","item_id":"msg_789","output_index":1,"content_index":0,"delta":" everything"}
{"type":"response.output_text.delta","item_id":"msg_789","output_index":1,"content_index":0,"delta":"."}

// 5. Content part and output item complete
{"type":"response.content_part.done","item_id":"msg_789","output_index":1,"content_index":0,"part":{"type":"output_text","text":"Why don't scientists trust atoms? Because they make up everything."}}
{"type":"response.output_item.done","output_index":1,"item":{"id":"msg_789","type":"message","status":"completed","content":[{"type":"output_text","text":"Why don't scientists trust atoms? Because they make up everything."}]}}

// 6. Response completes
{"type":"response.completed","response":{"id":"resp_abc123","status":"completed","output":[{"id":"rs_456","type":"reasoning"},{"id":"msg_789","type":"message","status":"completed","content":[{"type":"output_text","text":"Why don't scientists trust atoms? Because they make up everything."}]}]}}
```

## Step 2: Publish streaming events to Ably

Publish OpenAI streaming events to Ably to reliably and scalably distribute them to subscribers.

This implementation follows the explicit start/stop events pattern, which provides clear response boundaries.

### Initialize the Ably client

Add the Ably client initialization to your `agent.mjs` file:

JavaScript

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
```
import Ably from 'ably';

// Initialize Ably Realtime client
const realtime = new Ably.Realtime({
key: 'demokey:*****',
echoMessages: false
});

// Create a channel for publishing streamed AI responses
const channel = realtime.channels.get('who-tax-beg');
```
API key:

DEMO ONLY

The Ably Realtime client maintains a persistent connection to the Ably service, which allows you to publish tokens at high message rates with low latency.

### Map OpenAI streaming events to Ably messages

Choose how to map OpenAI streaming events to Ably messages. You can choose any mapping strategy that suits your application's needs. This guide uses the following pattern as an example:

- `start`: Signals the beginning of a response
- `token`: Contains the incremental text content for each delta
- `stop`: Signals the completion of a response
Update your `agent.mjs` file to initialize the Ably client and update the `processEvent()` function to publish events to Ably:

JavaScript

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

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50
51
```
// Track state across events
let responseId = null;
let messageItemId = null;

// Process each streaming event and publish to Ably
function processEvent(event) {
switch (event.type) {
case 'response.created':
// Capture response ID when response starts
responseId = event.response.id;

// Publish start event
channel.publish({
name: 'start',
extras: {
headers: { responseId }
}
});
break;

case 'response.output_item.added':
// Capture message item ID when a message output item is added
if (event.item.type === 'message') {
messageItemId = event.item.id;
}
break;

case 'response.output_text.delta':
// Publish tokens from message output items only
if (event.item_id === messageItemId) {
channel.publish({
name: 'token',
data: event.delta,
extras: {
headers: { responseId }
}
});
}
break;

case 'response.completed':
// Publish stop event when response completes
channel.publish({
name: 'stop',
extras: {
headers: { responseId }
}
});
break;
}
}
```
This implementation:

- Publishes a `start` event when the response begins
- Filters for `response.output_text.delta` events from `message` type output items and publishes them as `token` events
- Publishes a `stop` event when the response completes
- All published events include the `responseId` in message `extras` to allow the client to correlate events relating to a particular response
Run the publisher to see tokens streaming to Ably:
```
node agent.mjs
```

## Step 3: Subscribe to streaming tokens

Create a subscriber that receives the streaming events from Ably and reconstructs the response.

Create a new file `client.mjs` with the following contents:

JavaScript

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

…

```
import Ably from 'ably';

// Initialize Ably Realtime client
const realtime = new Ably.Realtime({ key: 'demokey:*****' });

// Get the same channel used by the publisher
const channel = realtime.channels.get('who-tax-beg');

// Track responses by ID
const responses = new Map();

// Handle response start
await channel.subscribe('start', (message) => {
const responseId = message.extras?.headers?.responseId;
console.log('\n[Response started]', responseId);
responses.set(responseId, '');
});

// Handle tokens
await channel.subscribe('token', (message) => {
const responseId = message.extras?.headers?.responseId;
const token = message.data;

// Append token to response
const currentText = responses.get(responseId) || '';
responses.set(responseId, currentText + token);

// Display token as it arrives
process.stdout.write(token);
});

// Handle response stop
await channel.subscribe('stop', (message) => {
const responseId = message.extras?.headers?.responseId;
const finalText = responses.get(responseId);
console.log('\n[Response completed]', responseId);
});

console.log('Subscriber ready, waiting for tokens...');
```
API key:

DEMO ONLY

Run the subscriber in a separate terminal:

…

With the subscriber running, run the publisher in another terminal. The tokens stream in realtime as the OpenAI model generates them.

## Step 4: Stream with multiple publishers and subscribers

Ably's channel-oriented sessions enables multiple AI agents to publish responses and multiple users to receive them on a single channel simultaneously. Ably handles message delivery to all participants, eliminating the need to implement routing logic or manage state synchronization across connections.

### Broadcasting to multiple subscribers

Each subscriber receives the complete stream of tokens independently, enabling you to build collaborative experiences or multi-device applications.

Run a subscriber in multiple separate terminals:
```
# Terminal 1
node client.mjs

# Terminal 2
node client.mjs

# Terminal 3
node client.mjs
```
All subscribers receive the same stream of tokens in realtime.

### Publishing concurrent responses

The implementation uses `responseId` in message `extras` to correlate tokens with their originating response. This enables multiple publishers to stream different responses concurrently on the same channel, with each subscriber correctly tracking all responses independently.

To demonstrate this, run a publisher in multiple separate terminals:
```
# Terminal 1
node agent.mjs

# Terminal 2
node agent.mjs

# Terminal 3
node agent.mjs
```
All running subscribers receive tokens from all responses concurrently. Each subscriber correctly reconstructs each response separately using the `responseId` to correlate tokens.

## Next steps
- Learn more about the message-per-token pattern used in this guide
- Learn about client hydration strategies for handling late joiners and reconnections
- Understand sessions and identity in AI enabled applications
- Explore the message-per-response pattern for storing complete AI responses as single messages in history