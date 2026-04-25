# Source: https://platform.openai.com/docs/guides/reasoning
# Author: OpenAI
# Author Slug: openai
# Title: OpenAI Platform: Reasoning Guide
# Fetched via: browser
# Date: 2026-04-09

Responses
Copy Page
More page actions

Reasoning models like GPT-5.4 allocate internal reasoning tokens before producing a response. They work especially well for complex problem solving, coding, scientific reasoning, and multi-step agentic workflows. They’re also the best models for Codex CLI, our lightweight coding agent.

Start with gpt-5.4 for most reasoning workloads. If you need the highest-intelligence API option for tougher problems that can tolerate more latency, use gpt-5.4-pro. For lower cost and latency, consider gpt-5-mini or gpt-5-nano.

Reasoning models work better with the Responses API. While the Chat Completions API is still supported, you’ll get improved model intelligence and performance by using Responses.

Get started with reasoning

Call the Responses API and specify your reasoning model and reasoning effort:

Using a reasoning model in the Responses API
python
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

from openai import OpenAI

client = OpenAI()

prompt = """
Write a bash script that takes a matrix represented as a string with 
format '[1,2],[3,4],[5,6]' and prints the transpose in the same format.
"""

response = client.responses.create(
    model="gpt-5.4",
    reasoning={"effort": "low"},
    input=[
        {
            "role": "user", 
            "content": prompt
        }
    ]
)

print(response.output_text)

In the example above, the reasoning.effort parameter guides the model on how many reasoning tokens to generate before creating a response to the prompt.

Supported values are model-dependent and can include none, minimal, low, medium, high, and xhigh. Lower effort favors speed and lower token usage, while higher effort favors more complete reasoning. Defaults are also model-dependent rather than universal. For example, gpt-5.4 defaults to none, while older GPT-5 models default to medium.

Effort	Start here when…
none	You want the lowest latency for execution-heavy tasks such as extraction, routing, or simple transforms
low	A small amount of extra thinking can improve reliability without adding much latency
medium or high	The task involves planning, coding, synthesis, or harder reasoning
xhigh	Only when your evals show a clear benefit that justifies the extra latency and cost

Some models support only a subset of these values, so check the relevant model page before choosing a setting.

How reasoning works

Reasoning models introduce reasoning tokens in addition to input and output tokens. The models use these reasoning tokens to “think,” breaking down the prompt and considering multiple approaches to generating a response. After generating reasoning tokens, the model produces an answer as visible completion tokens and discards the reasoning tokens from its context.

Here is an example of a multi-step conversation between a user and an assistant. Input and output tokens from each step are carried over, while reasoning tokens are discarded.

While reasoning tokens are not visible via the API, they still occupy space in the model’s context window and are billed as output tokens.

Managing the context window

It’s important to ensure there’s enough space in the context window for reasoning tokens when creating responses. Depending on the problem’s complexity, the models may generate anywhere from a few hundred to tens of thousands of reasoning tokens. The exact number of reasoning tokens used is visible in the usage object of the response object, under output_tokens_details:

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

{
  "usage": {
    "input_tokens": 75,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 1186,
    "output_tokens_details": {
      "reasoning_tokens": 1024
    },
    "total_tokens": 1261
  }
}

Context window lengths are found on the model reference page, and will differ across model snapshots.

Controlling costs

To manage costs with reasoning models, you can limit the total number of tokens the model generates (including both reasoning and final output tokens) by using the max_output_tokens parameter.

Allocating space for reasoning

If the generated tokens reach the context window limit or the max_output_tokens value you’ve set, you’ll receive a response with a status of incomplete and incomplete_details with reason set to max_output_tokens. This might occur before any visible output tokens are produced, meaning you could incur costs for input and reasoning tokens without receiving a visible response.

To prevent this, ensure there’s sufficient space in the context window or adjust the max_output_tokens value to a higher number. OpenAI recommends reserving at least 25,000 tokens for reasoning and outputs when you start experimenting with these models. As you become familiar with the number of reasoning tokens your prompts require, you can adjust this buffer accordingly.

Handling incomplete responses
python
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

from openai import OpenAI

client = OpenAI()

prompt = """
Write a bash script that takes a matrix represented as a string with 
format '[1,2],[3,4],[5,6]' and prints the transpose in the same format.
"""

response = client.responses.create(
    model="gpt-5.4",
    reasoning={"effort": "medium"},
    input=[
        {
            "role": "user", 
            "content": prompt
        }
    ],
    max_output_tokens=300,
)

if response.status == "incomplete" and response.incomplete_details.reason == "max_output_tokens":
    print("Ran out of tokens")
    if response.output_text:
        print("Partial output:", response.output_text)
    else: 
        print("Ran out of tokens during reasoning")
Keeping reasoning items in context

When doing function calling with a reasoning model in the Responses API, we highly recommend you pass back any reasoning items returned with the last function call (in addition to the output of your function). If the model calls multiple functions consecutively, you should pass back all reasoning items, function call items, and function call output items, since the last user message. This allows the model to continue its reasoning process to produce better results in the most token-efficient manner.

The simplest way to do this is to pass in all reasoning items from a previous response into the next one. Our systems will smartly ignore any reasoning items that aren’t relevant to your functions, and only retain those in context that are relevant. You can pass reasoning items from previous responses either using the previous_response_id parameter, or by manually passing in all the output items from a past response into the input of a new one.

For advanced use cases where you might be truncating and optimizing parts of the context window before passing them on to the next response, just ensure all items between the last user message and your function call output are passed into the next response untouched. This will ensure that the model has all the context it needs.

Check out this guide to learn more about manual context management.

Encrypted reasoning items

When using the Responses API in a stateless mode (either with store set to false, or when an organization is enrolled in zero data retention), you must still retain reasoning items across conversation turns using the techniques described above. But in order to have reasoning items that can be sent with subsequent API requests, each of your API requests must have reasoning.encrypted_content in the include parameter of API requests, like so:

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

curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "o4-mini",
    "reasoning": {"effort": "medium"},
    "input": "What is the weather like today?",
    "tools": [ ... function config here ... ],
    "include": [ "reasoning.encrypted_content" ]
  }'

Any reasoning items in the output array will now have an encrypted_content property, which will contain encrypted reasoning tokens that can be passed along with future conversation turns.

Reasoning summaries

While we don’t expose the raw reasoning tokens emitted by the model, you can view a summary of the model’s reasoning using the summary parameter. See our model documentation to check which reasoning models support summaries.

Different models support different reasoning summary settings. For example, our computer use model supports the concise summarizer, while o4-mini supports detailed. To access the most detailed summarizer available for a model, set the value of this parameter to auto. auto will be equivalent to detailed for most reasoning models today, but there may be more granular settings in the future.

Reasoning summary output is part of the summary array in the reasoning output item. This output will not be included unless you explicitly opt in to including reasoning summaries.

The example below shows how to make an API request that includes a reasoning summary.

Include a reasoning summary with the API response
python
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

from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5.4",
    input="What is the capital of France?",
    reasoning={
        "effort": "low",
        "summary": "auto"
    }
)

print(response.output)

This API request will return an output array with both an assistant message and a summary of the model’s reasoning in generating that response.

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

[
  {
    "id": "rs_6876cf02e0bc8192b74af0fb64b715ff06fa2fcced15a5ac",
    "type": "reasoning",
    "summary": [
      {
        "type": "summary_text",
        "text": "**Answering a simple question**\n\nI\u2019m looking at a straightforward question: the capital of France is Paris. It\u2019s a well-known fact, and I want to keep it brief and to the point. Paris is known for its history, art, and culture, so it might be nice to add just a hint of that charm. But mostly, I\u2019ll aim to focus on delivering a clear and direct answer, ensuring the user gets what they\u2019re looking for without any extra fluff."
      }
    ]
  },
  {
    "id": "msg_6876cf054f58819284ecc1058131305506fa2fcced15a5ac",
    "type": "message",
    "status": "completed",
    "content": [
      {
        "type": "output_text",
        "annotations": [],
        "logprobs": [],
        "text": "The capital of France is Paris."
      }
    ],
    "role": "assistant"
  }
]

Before using summarizers with our latest reasoning models, you may need to complete organization verification to ensure safe deployment. Get started with verification on the platform settings page.

Advice on prompting

There are some differences to consider when prompting a reasoning model. Reasoning-capable GPT-5 models usually work best when you give them a clear goal, strong constraints, and an explicit output contract without prescribing every intermediate step.

Give the model the task, constraints, and desired output format.
Treat reasoning.effort as a tuning knob, not the primary way to recover quality.
For agentic or research-heavy workflows, define what counts as done and how the model should verify its work.

For more information on best practices when using reasoning models, refer to this guide.

Prompt examples
Coding (refactoring)
Coding (planning)
STEM Research
Use case examples

Some examples of using reasoning models for real-world use cases can be found in the cookbook.

Using reasoning for data validation

Evaluate a synthetic medical data set for discrepancies.

Using reasoning for routine generation

Use help center articles to generate actions that an agent could perform.