# Source: https://github.com/langchain-ai/langgraph/issues/2831
# Author: LangChain
# Author Slug: langchain
# Title: graph stream with stream_mode=updates miss tool messages when using tools that return Command · Issue #2831 · langchain-ai/langgraph
# Fetched via: trafilatura
# Date: 2026-04-10

import os
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langgraph.types import Command
from typing_extensions import Annotated
@tool
def add(
a: int,
b: int,
tool_call_id: Annotated[str, InjectedToolCallId],
config: RunnableConfig,
):
"""add two numbers"""
result = a + b
return Command(
update={
"messages": [
ToolMessage(f"add result: {result}", tool_call_id=tool_call_id)
],
}
)
@tool
def sub(
a: int,
b: int,
tool_call_id: Annotated[str, InjectedToolCallId],
config: RunnableConfig,
):
"""sub two numbers"""
result = a + b
return f"sub result: {result}"
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
model = ChatOpenAI(
model="gpt-4o",
)
from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()
tools = [add, sub]
agent = create_react_agent(model, tools=tools, checkpointer=memory)
config = {
"configurable": {"thread_id": "1"},
}
# use add tool
for chunk in agent.stream(
input={
"messages": [
(
"user",
"add(1,1), add(1,2), add(1,3) at once",
),
]
},
config=config,
stream_mode="updates",
):
for node, values in chunk.items():
print(f"Receiving update from node: '{node}'")
print(values)
print("\n\n")
# use sub tool
for chunk in agent.stream(
input={
"messages": [
(
"user",
"sub(1,1), sub(1,2), sub(1,3) at once",
),
]
},
config=config,
stream_mode="updates",
):
for node, values in chunk.items():
print(f"Receiving update from node: '{node}'")
print(values)
print("\n\n")
print("======================message history=================\n\n")
cur_state = agent.get_state(config)
messages = cur_state.values.get("messages", [])
for message in messages:
message.pretty_print()
Receiving update from node: 'agent'
{'messages': [AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_vvaLfOBoaWoxaCtkF0kKAWAJ', 'function': {'arguments': '{"a": 1, "b": 1}', 'name': 'add'}, 'type': 'function'}, {'id': 'call_aYTuKfiWaF8ldAR4cfqU5VXj', 'function': {'arguments': '{"a": 1, "b": 2}', 'name': 'add'}, 'type': 'function'}, {'id': 'call_qO6RfVysJhQ8gP6DaSNpSg6v', 'function': {'arguments': '{"a": 1, "b": 3}', 'name': 'add'}, 'type': 'function'}], 'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 67, 'prompt_tokens': 85, 'total_tokens': 152, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_f3927aa00d', 'finish_reason': 'tool_calls', 'logprobs': None}, id='run-63311600-238f-4c51-a4cf-70617c0e9da3-0', tool_calls=[{'name': 'add', 'args': {'a': 1, 'b': 1}, 'id': 'call_vvaLfOBoaWoxaCtkF0kKAWAJ', 'type': 'tool_call'}, {'name': 'add', 'args': {'a': 1, 'b': 2}, 'id': 'call_aYTuKfiWaF8ldAR4cfqU5VXj', 'type': 'tool_call'}, {'name': 'add', 'args': {'a': 1, 'b': 3}, 'id': 'call_qO6RfVysJhQ8gP6DaSNpSg6v', 'type': 'tool_call'}], usage_metadata={'input_tokens': 85, 'output_tokens': 67, 'total_tokens': 152, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})]}
Receiving update from node: 'tools'
{'messages': [ToolMessage(content='add result: 4', name='add', id='11837479-f7b7-4f4d-b245-8a32e5d02776', tool_call_id='call_qO6RfVysJhQ8gP6DaSNpSg6v')]}
Receiving update from node: 'agent'
{'messages': [AIMessage(content='The results of the additions are as follows:\n- \\(1 + 1 = 2\\)\n- \\(1 + 2 = 3\\)\n- \\(1 + 3 = 4\\)', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 43, 'prompt_tokens': 183, 'total_tokens': 226, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_f3927aa00d', 'finish_reason': 'stop', 'logprobs': None}, id='run-8b12c0d2-9b5a-4a6a-8d5f-56cc773c83a4-0', usage_metadata={'input_tokens': 183, 'output_tokens': 43, 'total_tokens': 226, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})]}
Receiving update from node: 'agent'
{'messages': [AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_vMYScsWHPGVSLMD9hS8fDA5Q', 'function': {'arguments': '{"a": 1, "b": 1}', 'name': 'sub'}, 'type': 'function'}, {'id': 'call_nxtqJoafmwh6qtFO9f5lhVBt', 'function': {'arguments': '{"a": 1, "b": 2}', 'name': 'sub'}, 'type': 'function'}, {'id': 'call_vXrXRc4IClKzKZ3dRmABGISU', 'function': {'arguments': '{"a": 1, "b": 3}', 'name': 'sub'}, 'type': 'function'}], 'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 67, 'prompt_tokens': 253, 'total_tokens': 320, 'completion_tokens_details': None, 'prompt_tokens_details': None}, 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_04751d0b65', 'finish_reason': 'tool_calls', 'logprobs': None}, id='run-bb8e32b7-eea5-4d59-a7a1-69973a99a1be-0', tool_calls=[{'name': 'sub', 'args': {'a': 1, 'b': 1}, 'id': 'call_vMYScsWHPGVSLMD9hS8fDA5Q', 'type': 'tool_call'}, {'name': 'sub', 'args': {'a': 1, 'b': 2}, 'id': 'call_nxtqJoafmwh6qtFO9f5lhVBt', 'type': 'tool_call'}, {'name': 'sub', 'args': {'a': 1, 'b': 3}, 'id': 'call_vXrXRc4IClKzKZ3dRmABGISU', 'type': 'tool_call'}], usage_metadata={'input_tokens': 253, 'output_tokens': 67, 'total_tokens': 320, 'input_token_details': {}, 'output_token_details': {}})]}
Receiving update from node: 'tools'
{'messages': [ToolMessage(content='sub result: 2', name='sub', id='f7dfa2fb-d578-46b6-a39d-4523ac1abaed', tool_call_id='call_vMYScsWHPGVSLMD9hS8fDA5Q'), ToolMessage(content='sub result: 3', name='sub', id='c3be1d0d-7575-4ec0-be00-4e181964241a', tool_call_id='call_nxtqJoafmwh6qtFO9f5lhVBt'), ToolMessage(content='sub result: 4', name='sub', id='8d5fad1f-9fbb-4acf-be78-a766de53d322', tool_call_id='call_vXrXRc4IClKzKZ3dRmABGISU')]}
Receiving update from node: 'agent'
{'messages': [AIMessage(content='The results of the subtractions are as follows:\n- \\(1 - 1 = 0\\)\n- \\(1 - 2 = -1\\)\n- \\(1 - 3 = -2\\)', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 44, 'prompt_tokens': 351, 'total_tokens': 395, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_f3927aa00d', 'finish_reason': 'stop', 'logprobs': None}, id='run-f94e074c-18ce-4513-9f1a-ff19be9c2532-0', usage_metadata={'input_tokens': 351, 'output_tokens': 44, 'total_tokens': 395, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})]}
======================message history=================
================================ Human Message =================================
add(1,1), add(1,2), add(1,3) at once
================================== Ai Message ==================================
Tool Calls:
add (call_vvaLfOBoaWoxaCtkF0kKAWAJ)
Call ID: call_vvaLfOBoaWoxaCtkF0kKAWAJ
Args:
a: 1
b: 1
add (call_aYTuKfiWaF8ldAR4cfqU5VXj)
Call ID: call_aYTuKfiWaF8ldAR4cfqU5VXj
Args:
a: 1
b: 2
add (call_qO6RfVysJhQ8gP6DaSNpSg6v)
Call ID: call_qO6RfVysJhQ8gP6DaSNpSg6v
Args:
a: 1
b: 3
================================= Tool Message =================================
Name: add
add result: 2
================================= Tool Message =================================
Name: add
add result: 3
================================= Tool Message =================================
Name: add
add result: 4
================================== Ai Message ==================================
The results of the additions are as follows:
- \(1 + 1 = 2\)
- \(1 + 2 = 3\)
- \(1 + 3 = 4\)
================================ Human Message =================================
sub(1,1), sub(1,2), sub(1,3) at once
================================== Ai Message ==================================
Tool Calls:
sub (call_vMYScsWHPGVSLMD9hS8fDA5Q)
Call ID: call_vMYScsWHPGVSLMD9hS8fDA5Q
Args:
a: 1
b: 1
sub (call_nxtqJoafmwh6qtFO9f5lhVBt)
Call ID: call_nxtqJoafmwh6qtFO9f5lhVBt
Args:
a: 1
b: 2
sub (call_vXrXRc4IClKzKZ3dRmABGISU)
Call ID: call_vXrXRc4IClKzKZ3dRmABGISU
Args:
a: 1
b: 3
================================= Tool Message =================================
Name: sub
sub result: 2
================================= Tool Message =================================
Name: sub
sub result: 3
================================= Tool Message =================================
Name: sub
sub result: 4
================================== Ai Message ==================================
The results of the subtractions are as follows:
- \(1 - 1 = 0\)
- \(1 - 2 = -1\)
- \(1 - 3 = -2\)
if i define tool without return command, it works.
Checked other resources
Example Code
Error Message and Stack Trace (if applicable)
Description
I'm trying to use Command in tools to update graph state from tools,
when i call stream func with stream_mode=updates, if the llm call multiple tools at once, only the tool messages related to last tool is stream out, others not output.
if i define tool without return command, it works.
System Info
System Information
Package Information
Optional packages not installed
Other Dependencies