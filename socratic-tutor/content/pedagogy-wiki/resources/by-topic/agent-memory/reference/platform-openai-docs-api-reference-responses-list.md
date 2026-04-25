# Source: https://platform.openai.com/docs/api-reference/responses/list?lang=python
# Author: OpenAI
# Author Slug: openai
# Title: Responses | OpenAI API Reference
# Fetched via: search
# Date: 2026-04-09

## Introduction

This API reference describes the RESTful, streaming, and realtime APIs you can use to interact with the OpenAI platform. REST APIs are usable via HTTP in any environment that supports HTTP requests. Language-specific SDKs are listed on the libraries page.

…

```{

"id": "resp_67ccd2bed1ec8190b14f964abc0542670bb6a6b452d3795b",

"object": "response",

"created_at": 1741476542,

"status": "completed",

"error": null,

"incomplete_details": null,

"instructions": null,

"max_output_tokens": null,

"model": "gpt-4.1-2025-04-14",

"output": [



"type": "message",

"id": "msg_67ccd2bf17f0819081ff3bb2cf6508e60bb6a6b452d3795b",

"status": "completed",

"role": "assistant",

"content": [



"type": "output_text",

"text": "In a peaceful grove beneath a silver moon, a unicorn named Lumina discovered a hidden pool that reflected the stars. As she dipped her horn into the water, the pool began to shimmer, revealing a pathway to a magical realm of endless night skies. Filled with wonder, Lumina whispered a wish for all who dream to find their own hidden magic, and as she glanced back, her hoofprints sparkled like stardust.",

"annotations": []



],

"parallel_tool_calls": true,

"previous_response_id": null,

"reasoning": {

"effort": null,

"summary": null

},

"store": true,

"temperature": 1.0,

"text": {

"format": {

"type": "text"



},

"tool_choice": "auto",

"tools": [],

"top_p": 1.0,

"truncation": "disabled",

"usage": {

"input_tokens": 36,

"input_tokens_details": {

"cached_tokens": 0

},

"output_tokens": 87,

"output_tokens_details": {

"reasoning_tokens": 0

},

"total_tokens": 123

},

"user": null,

"metadata": {}



## Get a model responseget https://api.openai.com/v1/responses/{response_id}

Retrieves a model response with the given ID.

#### Path parameters

string

The ID of the response to retrieve.

#### Query parameters

array

Additional fields to include in the response. See the

`include`

parameter for Response creation above for more information.

boolean

When true, stream obfuscation will be enabled. Stream obfuscation adds

random characters to an

`obfuscation` field on streaming delta events

to normalize payload sizes as a mitigation to certain side-channel

attacks. These obfuscation fields are included by default, but add a

small amount of overhead to the data stream. You can set

`include_obfuscation` to false to optimize for bandwidth if you trust

the network links between your application and the OpenAI API.

integer

The sequence number of the event after which to start streaming.

boolean

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

#### Returns

The Response object matching the specified ID.

```

…

```{

"id": "resp_67cb71b351908190a308f3859487620d06981a8637e6bc44",

"object": "response",

"created_at": 1741386163,

"status": "completed",

"error": null,

"incomplete_details": null,

"instructions": null,

"max_output_tokens": null,

"model": "gpt-4o-2024-08-06",

"output": [



"type": "message",

"id": "msg_67cb71b3c2b0819084d481baaaf148f206981a8637e6bc44",

"status": "completed",

"role": "assistant",

"content": [



"type": "output_text",

"text": "Silent circuits hum, \nThoughts emerge in data streams— \nDigital dawn breaks.",

"annotations": []



],

"parallel_tool_calls": true,

"previous_response_id": null,

"reasoning": {

"effort": null,

"summary": null

},

"store": true,

"temperature": 1.0,

"text": {

"format": {

"type": "text"



},

"tool_choice": "auto",

"tools": [],

"top_p": 1.0,

"truncation": "disabled",

"usage": {

"input_tokens": 32,

"input_tokens_details": {

"cached_tokens": 0

},

"output_tokens": 18,

"output_tokens_details": {

"reasoning_tokens": 0

},

"total_tokens": 50

},

"user": null,

"metadata": {}



## List input itemsget https://api.openai.com/v1/responses/{response_id}/input_items

Returns a list of input items for a given response.

#### Path parameters

string

The ID of the response to retrieve input items for.

#### Query parameters

string

An item ID to list items after, used in pagination.

array

Additional fields to include in the response. See the

`include`

parameter for Response creation above for more information.

integer

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

string

The order to return the input items in. Default is

`desc`.

`asc`: Return the input items in ascending order.

`desc`: Return the input items in descending order.

#### Returns

A list of input item objects.

```

…

```from openai import OpenAI

client = OpenAI()

response = client.responses.input_items.list("resp_123")

print(response.data)

```

…

```{

"object": "list",

"data": [



"id": "msg_abc123",

"type": "message",

"role": "user",

"content": [



"type": "input_text",

"text": "Tell me a three sentence bedtime story about a unicorn."



],

"first_id": "msg_abc123",

"last_id": "msg_abc123",

"has_more": false



## The response object

boolean or null

Whether to run the model response in the background. Learn more.

object or null

The conversation that this response belongs to. Input items and output items from this response are automatically added to this conversation.

number

Unix timestamp (in seconds) of when this Response was created.

object or null

An error object returned when the model fails to generate a Response.

string

Unique identifier for this Response.

object or null

Details about why the response is incomplete.

string or array

A system (or developer) message inserted into the model's context.

When using along with

`previous_response_id`, the instructions from a previous

response will not be carried over to the next response. This makes it simple

to swap out system (or developer) messages in new responses.

integer or null

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

integer or null

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

map

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

string

Model ID used to generate the response, like

`gpt-4o` or

`o3`. OpenAI

offers a wide range of models with different capabilities, performance

characteristics, and price points. Refer to the model guide

to browse and compare available models.

string

The object type of this resource - always set to

`response`.

array

An array of content items generated by the model.

- The length and order of items in the

`output`array is dependent on the model's response.

- Rather than accessing the first item in the

`output`array and assuming it's an

`assistant`message with the content generated by the model, you might consider using the

`output_text`property where supported in SDKs.

string or null

SDK-only convenience property that contains the aggregated text output

from all

`output_text` items in the

`output` array, if any are present.

Supported in the Python and JavaScript SDKs.

boolean

Whether to allow the model to run tool calls in parallel.

string or null

The unique ID of the previous response to the model. Use this to

create multi-turn conversations. Learn more about

conversation state. Cannot be used in conjunction with

`conversation`.

object or null

Reference to a prompt template and its variables. Learn more.

string

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the

`user` field. Learn more.

object or null

**gpt-5 and o-series models only**

Configuration options for reasoning models.

string

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

string or null

Specifies the processing type used for serving the request.

- If set to 'auto', then the request will be processed with the service tier configured in the Project settings. Unless otherwise configured, the Project will use 'default'.

- If set to 'default', then the request will be processed with the standard pricing and performance for the selected model.

- If set to 'flex' or 'priority', then the request will be processed with the corresponding service tier.

- When not set, the default behavior is 'auto'.

When the

`service_tier` parameter is set, the response body will include the

`service_tier` value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

string

The status of the response generation. One of

`completed`,

`failed`,

`in_progress`,

`cancelled`,

`queued`, or

`incomplete`.

number or null

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.

We generally recommend altering this or

`top_p` but not both.

object

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

string or object

How the model should select which tool (or tools) to use when generating

a response. See the

`tools` parameter to see how to specify which tools

the model can call.

array

An array of tools the model may call while generating a response. You

can specify which tool to use by setting the

`tool_choice` parameter.

We support the following categories of tools:

**Built-in tools**: Tools that are provided by OpenAI that extend the model's capabilities, like web search or file search. Learn more about built-in tools. **MCP Tools**: Integrations with third-party systems via custom MCP servers or predefined connectors such as Google Drive and SharePoint. Learn more about MCP Tools. **Function calls (custom tools)**: Functions that are defined by you, enabling the model to call your own code with strongly typed arguments and outputs. Learn more about function calling. You can also use custom tools to call your own code.

integer or null

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

number or null

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or

`temperature` but not both.

string or null

The truncation strategy to use for the model response.

`auto`: If the context of this response and previous ones exceeds the model's context window size, the model will truncate the response to fit the context window by dropping input items in the middle of the conversation.

`disabled`(default): If a model response will exceed the context window size for a model, the request will fail with a 400 error.

object

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

string

This field is being replaced by

`safety_identifier` and

`prompt_cache_key`. Use

`prompt_cache_key` instead to maintain caching optimizations.

A stable identifier for your end-users.

Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

```

…

```{

"id": "resp_67ccd3a9da748190baa7f1570fe91ac604becb25c45c1d41",

"object": "response",

"created_at": 1741476777,

"status": "completed",

"error": null,

"incomplete_details": null,

"instructions": null,

"max_output_tokens": null,

"model": "gpt-4o-2024-08-06",

"output": [



"type": "message",

"id": "msg_67ccd3acc8d48190a77525dc6de64b4104becb25c45c1d41",

"status": "completed",

"role": "assistant",

"content": [



"type": "output_text",

"text": "The image depicts a scenic landscape with a wooden boardwalk or pathway leading through lush, green grass under a blue sky with some clouds. The setting suggests a peaceful natural area, possibly a park or nature reserve. There are trees and shrubs in the background.",

"annotations": []



],

"parallel_tool_calls": true,

"previous_response_id": null,

"reasoning": {

"effort": null,

"summary": null

},

"store": true,

"temperature": 1,

"text": {

"format": {

"type": "text"



},

"tool_choice": "auto",

"tools": [],

"top_p": 1,

"truncation": "disabled",

"usage": {

"input_tokens": 328,

"input_tokens_details": {

"cached_tokens": 0

},

"output_tokens": 52,

"output_tokens_details": {

"reasoning_tokens": 0

},

"total_tokens": 380

},

"user": null,

"metadata": {}



## The input item list

A list of Response items.

array

A list of items used to generate this response.

string

The ID of the first item in the list.

boolean

Whether there are more items available.

string

The ID of the last item in the list.

string

The type of object returned, must be

`list`.

```

…

```{

"object": "list",

"data": [



"id": "msg_abc123",

"type": "message",

"role": "user",

"content": [



"type": "input_text",

"text": "Tell me a three sentence bedtime story about a unicorn."



],

"first_id": "msg_abc123",

"last_id": "msg_abc123",

"has_more": false



## Conversations

Create and manage conversations to store and retrieve conversation state across Response API calls.

## Create a conversationpost https://api.openai.com/v1/conversations

Create a conversation.

#### Request body

array or null

Initial items to include in the conversation context. You may add up to 20 items at a time.

map

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

#### Returns

Returns a Conversation object.

```

…

```{

"id": "conv_123",

"object": "conversation.deleted",

"deleted": true



## List itemsget https://api.openai.com/v1/conversations/{conversation_id}/items

List all items for a conversation with the given ID.

#### Path parameters

string

The ID of the conversation to list items for.

#### Query parameters

string

An item ID to list items after, used in pagination.

array

Specify additional output data to include in the model response. Currently supported values are:

`web_search_call.action.sources`: Include the sources of the web search tool call.

`code_interpreter_call.outputs`: Includes the outputs of python code execution in code interpreter tool call items.

`computer_call_output.output.image_url`: Include image urls from the computer call output.

`file_search_call.results`: Include the search results of the file search tool call.

`message.input_image.image_url`: Include image urls from the input message.

`message.output_text.logprobs`: Include logprobs with assistant messages.

`reasoning.encrypted_content`: Includes an encrypted version of reasoning tokens in reasoning item outputs. This enables reasoning items to be used in multi-turn conversations when using the Responses API statelessly (like when the

`store`parameter is set to

`false`, or when an organization is enrolled in the zero data retention program).

integer

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

string

The order to return the input items in. Default is

`desc`.

`asc`: Return the input items in ascending order.

`desc`: Return the input items in descending order.

#### Returns

Returns a list object containing Conversation items.

```

…

```{

"object": "list",

"data": [



"type": "message",

"id": "msg_abc",

"status": "completed",

"role": "user",

"content": [

{"type": "input_text", "text": "Hello!"}



},



"type": "message",

"id": "msg_def",

"status": "completed",

"role": "user",

"content": [

{"type": "input_text", "text": "How are you?"}



],

"first_id": "msg_abc",

"last_id": "msg_def",

"has_more": false



## Retrieve an itemget https://api.openai.com/v1/conversations/{conversation_id}/items/{item_id}

Get a single item from a conversation with the given IDs.

#### Path parameters

string

The ID of the conversation that contains the item.

string

The ID of the item to retrieve.

#### Query parameters

array

Additional fields to include in the response. See the

`include`

parameter for listing Conversation items above for more information.

#### Returns

Returns a Conversation Item.

```

Have the model call your own custom code or use built-in tools like web search or file search to use your own data as input for the model's response.

#### Request body

boolean or null

Whether to run the model response in the background. Learn more.

array or null

Specify additional output data to include in the model response.

…

```{
"id": "resp_67ccd2bed1ec8190b14f964abc0542670bb6a6b452d3795b",

"object": "response",

"created_at": 1741476542,

"status": "completed",

"error": null,

"incomplete_details": null,

…

"input_tokens": 36,

"input_tokens_details": {

"cached_tokens": 0

},

"output_tokens": 87,

"output_tokens_details": {

"reasoning_tokens": 0

},

"total_tokens": 123

},

"user": null,

"metadata": {}



## Get a model responseget https://api.openai.com/v1/responses/{response_id}
Retrieves a model response with the given ID.

#### Path parameters

string

The ID of the response to retrieve.

#### Query parameters

array

Additional fields to include in the response. See the

`include`

parameter for Response creation above for more information.

integer

The sequence number of the event after which to start streaming.

boolean

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

#### Returns

The Response object matching the specified ID.

```
1

2

3

```curl https://api.openai.com/v1/responses/resp_123 \

-H "Content-Type: application/json" \

-H "Authorization: Bearer $OPENAI_API_KEY"

```

1

2

3

4

5

```import OpenAI from "openai";

const client = new OpenAI();

const response = await client.responses.retrieve("resp_123");

console.log(response);

```

…

48

49

50

51

52

53

54

55

56
```{
"id": "resp_67cb71b351908190a308f3859487620d06981a8637e6bc44",

"object": "response",

"created_at": 1741386163,

"status": "completed",

"error": null,

"incomplete_details": null,

"instructions": null,

…

"status": "completed",

"role": "assistant",

"content": [



"type": "output_text",

"text": "Silent circuits hum, \nThoughts emerge in data streams— \nDigital dawn breaks.",

"annotations": []



],

"parallel_tool_calls": true,

"previous_response_id": null,
"reasoning": {

"effort": null,

"summary": null

},

"store": true,

"temperature": 1.0,

"text": {

"format": {

"type": "text"



},

"tool_choice": "auto",

"tools": [],

"top_p": 1.0,

…

```import OpenAI from "openai";

const client = new OpenAI();

const response = await client.responses.cancel("resp_123");

console.log(response);

```

1

2

3

4

5

```from openai import OpenAI

client = OpenAI()

response = client.responses.cancel("resp_123")

print(response)

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

52

53

54

55

56

```{

"id": "resp_67cb71b351908190a308f3859487620d06981a8637e6bc44",

"object": "response",

"created_at": 1741386163,

"status": "completed",

"error": null,

"incomplete_details": null,

"instructions": null,

"max_output_tokens": null,

"model": "gpt-4o-2024-08-06",

"output": [



"type": "message",

"id": "msg_67cb71b3c2b0819084d481baaaf148f206981a8637e6bc44",

"status": "completed",

"role": "assistant",

"content": [



"type": "output_text",

"text": "Silent circuits hum, \nThoughts emerge in data streams— \nDigital dawn breaks.",

"annotations": []



],

"parallel_tool_calls": true,

"previous_response_id": null,

"reasoning": {

"effort": null,

"summary": null

},

"store": true,

"temperature": 1.0,

"text": {

"format": {

"type": "text"



},

"tool_choice": "auto",

"tools": [],

"top_p": 1.0,

"truncation": "disabled",

"usage": {

"input_tokens": 32,

"input_tokens_details": {

"cached_tokens": 0

},

"output_tokens": 18,

"output_tokens_details": {

"reasoning_tokens": 0

},

"total_tokens": 50

},

"user": null,

"metadata": {}



## List input itemsget https://api.openai.com/v1/responses/{response_id}/input_items

Returns a list of input items for a given response.

#### Path parameters

string

The ID of the response to retrieve input items for.

#### Query parameters

string

An item ID to list items after, used in pagination.

string

An item ID to list items before, used in pagination.

array

Additional fields to include in the response. See the

`include`

parameter for Response creation above for more information.

integer

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

string

The order to return the input items in. Default is

`desc`.

`asc`: Return the input items in ascending order.

`desc`: Return the input items in descending order.

#### Returns

A list of input item objects.

```

1

2

3

```curl https://api.openai.com/v1/responses/resp_abc123/input_items \

-H "Content-Type: application/json" \

-H "Authorization: Bearer $OPENAI_API_KEY"

```

1

2

3

4

5

```import OpenAI from "openai";

const client = new OpenAI();

const response = await client.responses.inputItems.list("resp_123");

console.log(response.data);

```

1

2

3

4

5

```from openai import OpenAI

client = OpenAI()

response = client.responses.input_items.list("resp_123")

print(response.data)

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
```{

"object": "list",

"data": [



"id": "msg_abc123",

"type": "message",

"role": "user",

"content": [



"type": "input_text",

"text": "Tell me a three sentence bedtime story about a unicorn."



],

"first_id": "msg_abc123",

"last_id": "msg_abc123",

"has_more": false



## The response object

boolean or null

Whether to run the model response in the background. Learn more.

number

Unix timestamp (in seconds) of when this Response was created.

object or null

An error object returned when the model fails to generate a Response.

string

Unique identifier for this Response.

object or null

Details about why the response is incomplete.

string or array

A system (or developer) message inserted into the model's context.

When using along with

`previous_response_id`, the instructions from a previous

response will not be carried over to the next response. This makes it simple

to swap out system (or developer) messages in new responses.

integer or null

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

integer or null

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

map

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

string

Model ID used to generate the response, like

`gpt-4o` or

`o3`. OpenAI

offers a wide range of models with different capabilities, performance

characteristics, and price points. Refer to the model guide

to browse and compare available models.

string

The object type of this resource - always set to

`response`.

array

An array of content items generated by the model.

- The length and order of items in the

`output`array is dependent on the model's response.

- Rather than accessing the first item in the

`output`array and assuming it's an

`assistant`message with the content generated by the model, you might consider using the

`output_text`property where supported in SDKs.

string or null

SDK-only convenience property that contains the aggregated text output

from all

`output_text` items in the

`output` array, if any are present.

Supported in the Python and JavaScript SDKs.

boolean

Whether to allow the model to run tool calls in parallel.

string or null

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state.

object or null

Reference to a prompt template and its variables. Learn more.

string

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the

`user` field. Learn more.

object or null

**o-series models only**

Configuration options for reasoning models.

string

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

string or null

Specifies the processing type used for serving the request.

- If set to 'auto', then the request will be processed with the service tier configured in the Project settings. Unless otherwise configured, the Project will use 'default'.

- If set to 'default', then the request will be processed with the standard pricing and performance for the selected model.

- If set to 'flex' or 'priority', then the request will be processed with the corresponding service tier. Contact sales to learn more about Priority processing.

- When not set, the default behavior is 'auto'.

When the

`service_tier` parameter is set, the response body will include the

`service_tier` value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

string

The status of the response generation. One of

`completed`,

`failed`,

`in_progress`,

`cancelled`,

`queued`, or

`incomplete`.

number or null

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.

We generally recommend altering this or

`top_p` but not both.

object

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

string or object

How the model should select which tool (or tools) to use when generating

a response. See the

`tools` parameter to see how to specify which tools

the model can call.

array

An array of tools the model may call while generating a response. You

can specify which tool to use by setting the

`tool_choice` parameter.

The two categories of tools you can provide the model are:

**Built-in tools**: Tools that are provided by OpenAI that extend the model's capabilities, like web search or file search. Learn more about built-in tools. **Function calls (custom tools)**: Functions that are defined by you, enabling the model to call your own code. Learn more about function calling.

integer or null

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

number or null

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or

`temperature` but not both.

string or null

The truncation strategy to use for the model response.

`auto`: If the context of this response and previous ones exceeds the model's context window size, the model will truncate the response to fit the context window by dropping input items in the middle of the conversation.

`disabled`(default): If a model response will exceed the context window size for a model, the request will fail with a 400 error.

object

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

string

This field is being replaced by

`safety_identifier` and

`prompt_cache_key`. Use

`prompt_cache_key` instead to maintain caching optimizations.

A stable identifier for your end-users.

Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

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

52

53

54

55

56

```{

"id": "resp_67ccd3a9da748190baa7f1570fe91ac604becb25c45c1d41",

"object": "response",

"created_at": 1741476777,

"status": "completed",

"error": null,

"incomplete_details": null,

"instructions": null,

"max_output_tokens": null,

"model": "gpt-4o-2024-08-06",

"output": [



"type": "message",

"id": "msg_67ccd3acc8d48190a77525dc6de64b4104becb25c45c1d41",

"status": "completed",

"role": "assistant",

"content": [



"type": "output_text",

"text": "The image depicts a scenic landscape with a wooden boardwalk or pathway leading through lush, green grass under a blue sky with some clouds. The setting suggests a peaceful natural area, possibly a park or nature reserve. There are trees and shrubs in the background.",

"annotations": []



],

"parallel_tool_calls": true,

"previous_response_id": null,

"reasoning": {

"effort": null,

"summary": null

},

"store": true,

"temperature": 1,

"text": {

"format": {

"type": "text"



},

"tool_choice": "auto",

"tools": [],

"top_p": 1,

"truncation": "disabled",

"usage": {

"input_tokens": 328,

"input_tokens_details": {

"cached_tokens": 0

},

"output_tokens": 52,

"output_tokens_details": {

"reasoning_tokens": 0

},

"total_tokens": 380

},

"user": null,

"metadata": {}



## The input item list

A list of Response items.

array

A list of items used to generate this response.

string

The ID of the first item in the list.

boolean

Whether there are more items available.

string

The ID of the last item in the list.

string

The type of object returned, must be

`list`.

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
```{
"object": "list",

"data": [



"id": "msg_abc123",

"type": "message",

"role": "user",

"content": [



"type": "input_text",

"text": "Tell me a three sentence bedtime story about a unicorn."



],

"first_id": "msg_abc123",

## Quick Start ¶
```
import instructor
from pydantic import BaseModel
# Initialize the client
client = instructor.from_provider(
"openai/gpt-4.1-mini", mode=instructor.Mode.RESPONSES_TOOLS
)
# Define your response model
class User(BaseModel):
name: str
age: int
# Create structured output
profile = client.responses.create(
input="Extract out Ivan is 28 years old",
response_model=User,
)
print(profile)
#> name='Ivan' age=28
```
## Response Modes ¶
The Responses API supports two main modes:
1. `instructor.Mode.RESPONSES_TOOLS`: Standard mode for structured outputs
2. `instructor.Mode.RESPONSES_TOOLS_WITH_INBUILT_TOOLS`: Enhanced mode that includes built-in tools like web search and file search
…
## Core Methods ¶
The Responses API provides several methods for creating structured outputs.
Here's how to use each one:
### Basic Creation ¶
The `create` method is the simplest way to get a structured output:
…
```
from pydantic import BaseModel
import instructor
import asyncio
class User(BaseModel):
name: str
age: int
client = instructor.from_provider(
"openai/gpt-4.1-mini",
mode=instructor.Mode.RESPONSES_TOOLS,
async_client=True
)
async def main():
profile = await client.responses.create(
input="Extract: Jason is 25 years old",
response_model=User,
)
print(profile) # User(name='Jason', age=25)
asyncio.run(main())
```
### Create with Completion ¶
If you need the original completion object from OpenAI, you can do so with the `create_with_completion` method.
This is useful when you have specific methods and data that you need to work from.
```
from pydantic import BaseModel
import instructor
class User(BaseModel):
name: str
age: int
client = instructor.from_provider(
"openai/gpt-4.1-mini",
mode=instructor.Mode.RESPONSES_TOOLS
)
response, completion = client.responses.create_with_completion(
input="Extract: Jason is 25 years old",
response_model=User,
)
print(response) # User(name='Jason', age=25)
print(completion) # Raw completion object
```
```
from pydantic import BaseModel
import instructor
import asyncio
class User(BaseModel):
name: str
age: int
client = instructor.from_provider(
"openai/gpt-4.1-mini",
mode=instructor.Mode.RESPONSES_TOOLS,
async_client=True
...
async def main():
response, completion = await client.responses.create_with_completion(
input="Extract: Jason is 25 years old",
response_model=User,
)
print(response) # User(name='Jason', age=25)
print(completion) # Raw completion object
asyncio.run(main())
...
### Web Search ¶
The web search tool allows models to search the internet for real-time information.
This is particularly useful for getting up-to-date information or verifying facts.
Model responses that use the web search tool will include two parts:
- A web_search_call output item with the ID of the search call.
- A message output item containing: 1.
The text result in message.content[0].text
2.
Annotations message.content[0].annotations for the cited URLs
By default, the model's response will include inline citations for URLs found in the web search results.
In addition to this, the url_citation annotation object will contain the URL, title and location of the cited source.
You can extract this information using the `create_with_completion` method.
```
from pydantic import BaseModel
import instructor
class Citation(BaseModel):
id: int
url: str
class Summary(BaseModel):
citations: list[Citation]
summary: str
client = instructor.from_provider(
"openai/gpt-4.1-mini",
mode=instructor.Mode.RESPONSES_TOOLS_WITH_INBUILT_TOOLS,
async_client=False,
)
response, completion = client.responses.create_with_completion(
input="What are some of the best places to visit in New York for Latin American food?",
tools=[{"type": "web_search_preview"}],
response_model=Summary,
)
print(response)
# > citations=[Citation(id=1,url=....)]
# > summary = New York City offers a rich variety of ...
```
```
from pydantic import BaseModel
...
summary: str
...
response = await client.responses.create(
input="What are some of the best places to visit in New York for Latin American food?",
tools=[{"type": "web_search_preview"}],
response_model=Summary,
)
print(response)
asyncio.run(main())
# > citations=[Citation(id=1,url=....)]

## What Is OpenAI’s Responses API?
The Responses API is OpenAI’s newest and most advanced API.
It combines the strengths of the Chat Completions and Assistants APIs into a single streamlined interface.
Released in March 2025, it maintains familiar capabilities while providing a more integrated approach to building AI applications.
The key innovation is how it simplifies development by automatically handling orchestration logic and natively integrating OpenAI’s built-in tools for web search and file search without requiring custom implementation.
In this tutorial, we’ll walk through how to use the Responses API in your projects.
You’ll see how it handles text generation, works with images, and delivers streaming responses.
We’ll examine the built-in tools that make development faster and more straightforward than before, showing you how these tools work together within the API’s framework.
…
### Generating content with the Responses API
The most straightforward use of the Responses API is generating text content.
Let’s explore a real-world scenario: suppose you’re building an e-commerce platform and need to automatically generate compelling product descriptions based on basic product details.
Traditionally, this would require careful prompt engineering and multiple iterations.
With the Responses API, you can create a simple function that handles this elegantly:
```
def generate_product_description(product_name, features, target_audience):
response = client.responses.create(
model="gpt-4o",
instructions="You are a professional copywriter specialized in creating concise, compelling product descriptions.
Focus on benefits rather than just features.",
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
With just a few lines of code, we’ve created marketing-quality copy that would normally require a professional writer.
The function is also reusable — just change the parameters, and you can generate descriptions for any product in your catalog.
This example demonstrates key patterns when using the Responses API:
1. The
…
1. You define functions that the AI can use, specifying parameters and their types.
2. The AI decides when to call these functions based on user queries.
3. Your code executes the functions with the AI-provided parameters.
4. You return the results to the AI, which incorporates them into its response.
…
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
Function calling enables the Responses API to connect natural language inputs with your services and data.
This creates a bridge between user requests and your business systems, allowing users to make requests in plain language while your application handles the technical implementation details in the background.
Beyond function calling, another powerful capability of the Responses API is the ability to generate structured outputs.
This feature complements function calling by providing a way to receive responses in specific formats that align with your application’s needs.
## Structured Outputs With the Responses API
When building AI applications, you often need responses in a specific format for easier integration with your systems.
The Responses API supports structured outputs that enable you to receive data in a well-defined, consistent format rather than free-form text.
This feature is particularly valuable when you need to:
1. Extract specific information from unstructured text.
2. Transform user inputs into structured data.
3. Ensure consistent response formats for downstream processing.
4. Integrate AI outputs directly with databases or APIs.
…
### Extracting product information from descriptions
Let’s explore a practical example: imagine you’re building an e-commerce platform and need to automatically extract product details from unstructured product descriptions to populate your database.
...
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

const { output } = await generateText({
model: openai.responses('gpt-4o'),
output: Output.object({
schema: z.object({
recipe: z.object({
name: z.string(),
ingredients: z.array(
z.object({ name: z.string(), amount: z.string() }),
),
steps: z.array(z.string()),
}),
}),
}),
prompt: 'Generate a lasagna recipe.',
});
```