# Source: https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/conversable_agent/
# Author: Microsoft
# Author Slug: microsoft
# Title: agentchat.conversable_agent | AutoGen 0.2
# Fetched via: trafilatura
# Date: 2026-04-09

agentchat.conversable_agent
ConversableAgent[](#conversableagent)
class ConversableAgent(LLMAgent)
(In preview) A class for generic conversable agents which can be configured as assistant or user proxy.
After receiving each message, the agent will send a reply to the sender unless the msg is a termination msg. For example, AssistantAgent and UserProxyAgent are subclasses of this class, configured with different default settings.
To modify auto reply, override generate_reply
method.
To disable/enable human response in every turn, set human_input_mode
to "NEVER" or "ALWAYS".
To modify the way to get human input, override get_human_input
method.
To modify the way to execute code blocks, single code block, or function call, override execute_code_blocks
,
run_code
, and execute_function
methods respectively.
DEFAULT_CONFIG[](#default_config)
False or dict, the default config for llm inference
MAX_CONSECUTIVE_AUTO_REPLY[](#max_consecutive_auto_reply)
maximum number of consecutive auto replies (subject to future change)
__init__[](#__init__)
def __init__(name: str,
system_message: Optional[Union[
str, List]] = "You are a helpful AI Assistant.",
is_termination_msg: Optional[Callable[[Dict], bool]] = None,
max_consecutive_auto_reply: Optional[int] = None,
human_input_mode: Literal["ALWAYS", "NEVER",
"TERMINATE"] = "TERMINATE",
function_map: Optional[Dict[str, Callable]] = None,
code_execution_config: Union[Dict, Literal[False]] = False,
llm_config: Optional[Union[Dict, Literal[False]]] = None,
default_auto_reply: Union[str, Dict] = "",
description: Optional[str] = None,
chat_messages: Optional[Dict[Agent, List[Dict]]] = None,
silent: Optional[bool] = None)
Arguments:
name
str - name of the agent.system_message
str or list - system message for the ChatCompletion inference.is_termination_msg
function - a function that takes a message in the form of a dictionary and returns a boolean value indicating if this received message is a termination message. The dict can contain the following keys: "content", "role", "name", "function_call".max_consecutive_auto_reply
int - the maximum number of consecutive auto replies. default to None (no limit provided, class attribute MAX_CONSECUTIVE_AUTO_REPLY will be used as the limit in this case). When set to 0, no auto reply will be generated.human_input_mode
str - whether to ask for human inputs every time a message is received. Possible values are "ALWAYS", "TERMINATE", "NEVER". (1) When "ALWAYS", the agent prompts for human input every time a message is received. Under this mode, the conversation stops when the human input is "exit", or when is_termination_msg is True and there is no human input. (2) When "TERMINATE", the agent only prompts for human input only when a termination message is received or the number of auto reply reaches the max_consecutive_auto_reply. (3) When "NEVER", the agent will never prompt for human input. Under this mode, the conversation stops when the number of auto reply reaches the max_consecutive_auto_reply or when is_termination_msg is True.function_map
dict[str, callable] - Mapping function names (passed to openai) to callable functions, also used for tool calls.code_execution_config
dict or False - config for the code execution. To disable code execution, set to False. Otherwise, set to a dictionary with the following keys:- work_dir (Optional, str): The working directory for the code execution. If None, a default working directory will be used. The default working directory is the "extensions" directory under "path_to_autogen".
- use_docker (Optional, list, str or bool): The docker image to use for code execution. Default is True, which means the code will be executed in a docker container. A default list of images will be used. If a list or a str of image name(s) is provided, the code will be executed in a docker container with the first image successfully pulled. If False, the code will be executed in the current environment. We strongly recommend using docker for code execution.
- timeout (Optional, int): The maximum execution time in seconds.
- last_n_messages (Experimental, int or str): The number of messages to look back for code execution. If set to 'auto', it will scan backwards through all messages arriving since the agent last spoke, which is typically the last time execution was attempted. (Default: auto)
llm_config
dict or False or None - llm inference configuration. Please refer to[OpenAIWrapper.create](/autogen/0.2/docs/reference/oai/client#create)for available options. When using OpenAI or Azure OpenAI endpoints, please specify a non-empty 'model' either inllm_config
or in each config of 'config_list' inllm_config
. To disable llm-based auto reply, set to False. When set to None, will use self.DEFAULT_CONFIG, which defaults to False.default_auto_reply
str or dict - default auto reply when no code execution or llm-based reply is generated.description
str - a short description of the agent. This description is used by other agents (e.g. the GroupChatManager) to decide when to call upon this agent. (Default: system_message)chat_messages
dict or None - the previous chat messages that this agent had in the past with other agents. Can be used to give the agent a memory by providing the chat history. This will allow the agent to resume previous had conversations. Defaults to an empty chat history.silent
bool or None - (Experimental) whether to print the message sent. If None, will use the value of silent in each function.
name[](#name)
@property
def name() -> str
Get the name of the agent.
description[](#description)
@property
def description() -> str
Get the description of the agent.
description[](#description-1)
@description.setter
def description(description: str)
Set the description of the agent.
code_executor[](#code_executor)
@property
def code_executor() -> Optional[CodeExecutor]
The code executor used by this agent. Returns None if code execution is disabled.
register_reply[](#register_reply)
def register_reply(trigger: Union[Type[Agent], str, Agent,
Callable[[Agent], bool], List],
reply_func: Callable,
position: int = 0,
config: Optional[Any] = None,
reset_config: Optional[Callable] = None,
*,
ignore_async_in_sync_chat: bool = False,
remove_other_reply_funcs: bool = False)
Register a reply function.
The reply function will be called when the trigger matches the sender. The function registered later will be checked earlier by default. To change the order, set the position to a positive integer.
Both sync and async reply functions can be registered. The sync reply function will be triggered
from both sync and async chats. However, an async reply function will only be triggered from async
chats (initiated with ConversableAgent.a_initiate_chat
). If an async
reply function is registered
and a chat is initialized with a sync function, ignore_async_in_sync_chat
determines the behaviour as follows:
if ignore_async_in_sync_chat
is set to False
(default value), an exception will be raised, and
if ignore_async_in_sync_chat
is set to True
, the reply function will be ignored.
Arguments:
-
trigger
Agent class, str, Agent instance, callable, or list - the trigger. If a class is provided, the reply function will be called when the sender is an instance of the class. If a string is provided, the reply function will be called when the sender's name matches the string. If an agent instance is provided, the reply function will be called when the sender is the agent instance. If a callable is provided, the reply function will be called when the callable returns True. If a list is provided, the reply function will be called when any of the triggers in the list is activated. If None is provided, the reply function will be called only when the sender is None. -
Note
- Be sure to registerNone
as a trigger if you would like to trigger an auto-reply function with non-empty messages andsender=None
. -
reply_func
Callable - the reply function. The function takes a recipient agent, a list of messages, a sender agent and a config as input and returns a reply message.```python
def reply_func(
recipient: ConversableAgent,
messages: Optional[List[Dict]] = None,
sender: Optional[Agent] = None,
config: Optional[Any] = None,
) -> Tuple[bool, Union[str, Dict, None]]:
``` -
position
int - the position of the reply function in the reply function list. The function registered later will be checked earlier by default. To change the order, set the position to a positive integer. -
config
Any - the config to be passed to the reply function. When an agent is reset, the config will be reset to the original value. -
reset_config
Callable - the function to reset the config. The function returns None. Signature:def reset_config(config: Any)
-
ignore_async_in_sync_chat
bool - whether to ignore the async reply function in sync chats. IfFalse
, an exception will be raised if an async reply function is registered and a chat is initialized with a sync function. -
remove_other_reply_funcs
bool - whether to remove other reply functions when registering this reply function.
replace_reply_func[](#replace_reply_func)
def replace_reply_func(old_reply_func: Callable, new_reply_func: Callable)
Replace a registered reply function with a new one.
Arguments:
old_reply_func
Callable - the old reply function to be replaced.new_reply_func
Callable - the new reply function to replace the old one.
register_nested_chats[](#register_nested_chats)
def register_nested_chats(chat_queue: List[Dict[str, Any]],
trigger: Union[Type[Agent], str, Agent,
Callable[[Agent], bool], List],
reply_func_from_nested_chats: Union[
str, Callable] = "summary_from_nested_chats",
position: int = 2,
use_async: Union[bool, None] = None,
**kwargs) -> None
Register a nested chat reply function.
Arguments:
chat_queue
list - a list of chat objects to be initiated. If use_async is used, then all messages in chat_queue must have a chat-id associated with them.trigger
Agent class, str, Agent instance, callable, or list - refer toregister_reply
for details.reply_func_from_nested_chats
Callable, str - the reply function for the nested chat. The function takes a chat_queue for nested chat, recipient agent, a list of messages, a sender agent and a config as input and returns a reply message. Default to "summary_from_nested_chats", which corresponds to a built-in reply function that get summary from the nested chat_queue.def reply_func_from_nested_chats(
chat_queue: List[Dict],
recipient: ConversableAgent,
messages: Optional[List[Dict]] = None,
sender: Optional[Agent] = None,
config: Optional[Any] = None,
) -> Tuple[bool, Union[str, Dict, None]]:position
int - Ref toregister_reply
for details. Default to 2. It means we first check the termination and human reply, then check the registered nested chat reply.use_async
- Uses a_initiate_chats internally to start nested chats. If the original chat is initiated with a_initiate_chats, you may set this to true so nested chats do not run in sync.kwargs
- Ref toregister_reply
for details.
system_message[](#system_message)
@property
def system_message() -> str
Return the system message.
update_system_message[](#update_system_message)
def update_system_message(system_message: str) -> None
Update the system message.
Arguments:
system_message
str - system message for the ChatCompletion inference.
update_max_consecutive_auto_reply[](#update_max_consecutive_auto_reply)
def update_max_consecutive_auto_reply(value: int,
sender: Optional[Agent] = None)
Update the maximum number of consecutive auto replies.
Arguments:
value
int - the maximum number of consecutive auto replies.sender
Agent - when the sender is provided, only update the max_consecutive_auto_reply for that sender.
max_consecutive_auto_reply[](#max_consecutive_auto_reply-1)
def max_consecutive_auto_reply(sender: Optional[Agent] = None) -> int
The maximum number of consecutive auto replies.
chat_messages[](#chat_messages)
@property
def chat_messages() -> Dict[Agent, List[Dict]]
A dictionary of conversations from agent to list of messages.
chat_messages_for_summary[](#chat_messages_for_summary)
def chat_messages_for_summary(agent: Agent) -> List[Dict]
A list of messages as a conversation to summarize.
last_message[](#last_message)
def last_message(agent: Optional[Agent] = None) -> Optional[Dict]
The last message exchanged with the agent.
Arguments:
agent
Agent - The agent in the conversation. If None and more than one agent's conversations are found, an error will be raised. If None and only one conversation is found, the last message of the only conversation will be returned.
Returns:
The last message exchanged with the agent.
use_docker[](#use_docker)
@property
def use_docker() -> Union[bool, str, None]
Bool value of whether to use docker to execute the code, or str value of the docker image name to use, or None when code execution is disabled.
send[](#send)
def send(message: Union[Dict, str],
recipient: Agent,
request_reply: Optional[bool] = None,
silent: Optional[bool] = False)
Send a message to another agent.
Arguments:
message
dict or str - message to be sent. The message could contain the following fields:- content (str or List): Required, the content of the message. (Can be None)
- function_call (str): the name of the function to be called.
- name (str): the name of the function to be called.
- role (str): the role of the message, any role that is not "function" will be modified to "assistant".
- context (dict): the context of the message, which will be passed to
[OpenAIWrapper.create](/autogen/0.2/docs/reference/oai/client#create). For example, one agent can send a message A as:
{
"content": lambda context: context["use_tool_msg"],
"context": {
"use_tool_msg": "Use tool X if they are relevant."
}
}
Next time, one agent can send a message B with a different "use_tool_msg". Then the content of message A will be refreshed to the new "use_tool_msg". So effectively, this provides a way for an agent to send a "link" and modify the content of the "link" later.
recipient
Agent - the recipient of the message.request_reply
bool or None - whether to request a reply from the recipient.silent
bool or None - (Experimental) whether to print the message sent.
Raises:
ValueError
- if the message can't be converted into a valid ChatCompletion message.
a_send[](#a_send)
async def a_send(message: Union[Dict, str],
recipient: Agent,
request_reply: Optional[bool] = None,
silent: Optional[bool] = False)
(async) Send a message to another agent.
Arguments:
message
dict or str - message to be sent. The message could contain the following fields:- content (str or List): Required, the content of the message. (Can be None)
- function_call (str): the name of the function to be called.
- name (str): the name of the function to be called.
- role (str): the role of the message, any role that is not "function" will be modified to "assistant".
- context (dict): the context of the message, which will be passed to
[OpenAIWrapper.create](/autogen/0.2/docs/reference/oai/client#create). For example, one agent can send a message A as:
{
"content": lambda context: context["use_tool_msg"],
"context": {
"use_tool_msg": "Use tool X if they are relevant."
}
}
Next time, one agent can send a message B with a different "use_tool_msg". Then the content of message A will be refreshed to the new "use_tool_msg". So effectively, this provides a way for an agent to send a "link" and modify the content of the "link" later.
recipient
Agent - the recipient of the message.request_reply
bool or None - whether to request a reply from the recipient.silent
bool or None - (Experimental) whether to print the message sent.
Raises:
ValueError
- if the message can't be converted into a valid ChatCompletion message.
receive[](#receive)
def receive(message: Union[Dict, str],
sender: Agent,
request_reply: Optional[bool] = None,
silent: Optional[bool] = False)
Receive a message from another agent.
Once a message is received, this function sends a reply to the sender or stop. The reply can be generated automatically or entered manually by a human.
Arguments:
message
dict or str - message from the sender. If the type is dict, it may contain the following reserved fields (either content or function_call need to be provided).- "content": content of the message, can be None.
- "function_call": a dictionary containing the function name and arguments. (deprecated in favor of "tool_calls")
- "tool_calls": a list of dictionaries containing the function name and arguments.
- "role": role of the message, can be "assistant", "user", "function", "tool". This field is only needed to distinguish between "function" or "assistant"/"user".
- "name": In most cases, this field is not needed. When the role is "function", this field is needed to indicate the function name.
- "context" (dict): the context of the message, which will be passed to
[OpenAIWrapper.create](/autogen/0.2/docs/reference/oai/client#create).
sender
- sender of an Agent instance.request_reply
bool or None - whether a reply is requested from the sender. If None, the value is determined byself.reply_at_receive[sender]
.silent
bool or None - (Experimental) whether to print the message received.
Raises:
ValueError
- if the message can't be converted into a valid ChatCompletion message.
a_receive[](#a_receive)
async def a_receive(message: Union[Dict, str],
sender: Agent,
request_reply: Optional[bool] = None,
silent: Optional[bool] = False)
(async) Receive a message from another agent.
Once a message is received, this function sends a reply to the sender or stop. The reply can be generated automatically or entered manually by a human.
Arguments:
message
dict or str - message from the sender. If the type is dict, it may contain the following reserved fields (either content or function_call need to be provided).- "content": content of the message, can be None.
- "function_call": a dictionary containing the function name and arguments. (deprecated in favor of "tool_calls")
- "tool_calls": a list of dictionaries containing the function name and arguments.
- "role": role of the message, can be "assistant", "user", "function". This field is only needed to distinguish between "function" or "assistant"/"user".
- "name": In most cases, this field is not needed. When the role is "function", this field is needed to indicate the function name.
- "context" (dict): the context of the message, which will be passed to
[OpenAIWrapper.create](/autogen/0.2/docs/reference/oai/client#create).
sender
- sender of an Agent instance.request_reply
bool or None - whether a reply is requested from the sender. If None, the value is determined byself.reply_at_receive[sender]
.silent
bool or None - (Experimental) whether to print the message received.
Raises:
ValueError
- if the message can't be converted into a valid ChatCompletion message.
initiate_chat[](#initiate_chat)
def initiate_chat(recipient: "ConversableAgent",
clear_history: bool = True,
silent: Optional[bool] = False,
cache: Optional[AbstractCache] = None,
max_turns: Optional[int] = None,
summary_method: Optional[Union[
str, Callable]] = DEFAULT_SUMMARY_METHOD,
summary_args: Optional[dict] = {},
message: Optional[Union[Dict, str, Callable]] = None,
**kwargs) -> ChatResult
Initiate a chat with the recipient agent.
Reset the consecutive auto reply counter.
If clear_history
is True, the chat history with the recipient agent will be cleared.
Arguments:
-
recipient
- the recipient agent. -
clear_history
bool - whether to clear the chat history with the agent. Default is True. -
silent
bool or None - (Experimental) whether to print the messages for this conversation. Default is False. -
cache
AbstractCache or None - the cache client to be used for this conversation. Default is None. -
max_turns
int or None - the maximum number of turns for the chat between the two agents. One turn means one conversation round trip. Note that this is different from[max_consecutive_auto_reply](#max_consecutive_auto_reply)which is the maximum number of consecutive auto replies; and it is also different from[max_rounds in GroupChat](/autogen/0.2/docs/reference/agentchat/groupchat#groupchat-objects)which is the maximum number of rounds in a group chat session. If max_turns is set to None, the chat will continue until a termination condition is met. Default is None. -
summary_method
str or callable - a method to get a summary from the chat. Default is DEFAULT_SUMMARY_METHOD, i.e., "last_msg".Supported strings are "last_msg" and "reflection_with_llm":
- when set to "last_msg", it returns the last message of the dialog as the summary.
- when set to "reflection_with_llm", it returns a summary extracted using an llm client.
llm_config
must be set in either the recipient or sender.
A callable summary_method should take the recipient and sender agent in a chat as input and return a string of summary. E.g.,
def my_summary_method(
sender: ConversableAgent,
recipient: ConversableAgent,
summary_args: dict,
):
return recipient.last_message(sender)["content"] -
summary_args
dict - a dictionary of arguments to be passed to the summary_method. One example key is "summary_prompt", and value is a string of text used to prompt a LLM-based agent (the sender or receiver agent) to reflect on the conversation and extract a summary when summary_method is "reflection_with_llm". The default summary_prompt is DEFAULT_SUMMARY_PROMPT, i.e., "Summarize takeaway from the conversation. Do not add any introductory phrases. If the intended request is NOT properly addressed, please point it out." Another available key is "summary_role", which is the role of the message sent to the agent in charge of summarizing. Default is "system". -
message
str, dict or Callable - the initial message to be sent to the recipient. Needs to be provided. Otherwise, input() will be called to get the initial message.-
If a string or a dict is provided, it will be used as the initial message.
generate_init_message
is called to generate the initial message for the agent based on this string and the context. If dict, it may contain the following reserved fields (either content or tool_calls need to be provided).
-
"content": content of the message, can be None.
-
"function_call": a dictionary containing the function name and arguments. (deprecated in favor of "tool_calls")
-
"tool_calls": a list of dictionaries containing the function name and arguments.
-
"role": role of the message, can be "assistant", "user", "function". This field is only needed to distinguish between "function" or "assistant"/"user".
-
"name": In most cases, this field is not needed. When the role is "function", this field is needed to indicate the function name.
-
"context" (dict): the context of the message, which will be passed to
[OpenAIWrapper.create](/autogen/0.2/docs/reference/oai/client#create).
- If a callable is provided, it will be called to get the initial message in the form of a string or a dict. If the returned type is dict, it may contain the reserved fields mentioned above.
Example of a callable message (returning a string):
def my_message(sender: ConversableAgent, recipient: ConversableAgent, context: dict) -> Union[str, Dict]:
carryover = context.get("carryover", "")
if isinstance(message, list):
carryover = carryover[-1]
final_msg = "Write a blogpost." + "\nContext: \n" + carryover
return final_msgExample of a callable message (returning a dict):
def my_message(sender: ConversableAgent, recipient: ConversableAgent, context: dict) -> Union[str, Dict]:
final_msg = {}
carryover = context.get("carryover", "")
if isinstance(message, list):
carryover = carryover[-1]
final_msg["content"] = "Write a blogpost." + "\nContext: \n" + carryover
final_msg["context"] = {"prefix": "Today I feel"}
return final_msg -
-
**kwargs
- any additional information. It has the following reserved fields:- "carryover": a string or a list of string to specify the carryover information to be passed to this chat.
If provided, we will combine this carryover (by attaching a "context: " string and the carryover content after the message content) with the "message" content when generating the initial chat
message in
generate_init_message
. - "verbose": a boolean to specify whether to print the message and carryover in a chat. Default is False.
- "carryover": a string or a list of string to specify the carryover information to be passed to this chat.
If provided, we will combine this carryover (by attaching a "context: " string and the carryover content after the message content) with the "message" content when generating the initial chat
message in
Raises:
RuntimeError
- if any async reply functions are registered and not ignored in sync chat.
Returns:
ChatResult
- an ChatResult object.
a_initiate_chat[](#a_initiate_chat)
async def a_initiate_chat(recipient: "ConversableAgent",
clear_history: bool = True,
silent: Optional[bool] = False,
cache: Optional[AbstractCache] = None,
max_turns: Optional[int] = None,
summary_method: Optional[Union[
str, Callable]] = DEFAULT_SUMMARY_METHOD,
summary_args: Optional[dict] = {},
message: Optional[Union[str, Callable]] = None,
**kwargs) -> ChatResult
(async) Initiate a chat with the recipient agent.
Reset the consecutive auto reply counter.
If clear_history
is True, the chat history with the recipient agent will be cleared.
a_generate_init_message
is called to generate the initial message for the agent.
Args: Please refer to initiate_chat
.
Returns:
ChatResult
- an ChatResult object.
initiate_chats[](#initiate_chats)
def initiate_chats(chat_queue: List[Dict[str, Any]]) -> List[ChatResult]
(Experimental) Initiate chats with multiple agents.
Arguments:
-
chat_queue
List[Dict] - a list of dictionaries containing the information of the chats. Each dictionary should contain the input arguments forinitiate_chat
-
Returns
- a list of ChatResult objects corresponding to the finished chats in the chat_queue.
get_chat_results[](#get_chat_results)
def get_chat_results(
chat_index: Optional[int] = None
) -> Union[List[ChatResult], ChatResult]
A summary from the finished chats of particular agents.
reset[](#reset)
def reset()
Reset the agent.
stop_reply_at_receive[](#stop_reply_at_receive)
def stop_reply_at_receive(sender: Optional[Agent] = None)
Reset the reply_at_receive of the sender.
reset_consecutive_auto_reply_counter[](#reset_consecutive_auto_reply_counter)
def reset_consecutive_auto_reply_counter(sender: Optional[Agent] = None)
Reset the consecutive_auto_reply_counter of the sender.
clear_history[](#clear_history)
def clear_history(recipient: Optional[Agent] = None,
nr_messages_to_preserve: Optional[int] = None)
Clear the chat history of the agent.
Arguments:
recipient
- the agent with whom the chat history to clear. If None, clear the chat history with all agents.nr_messages_to_preserve
- the number of newest messages to preserve in the chat history.
generate_oai_reply[](#generate_oai_reply)
def generate_oai_reply(
messages: Optional[List[Dict]] = None,
sender: Optional[Agent] = None,
config: Optional[OpenAIWrapper] = None
) -> Tuple[bool, Union[str, Dict, None]]
Generate a reply using autogen.oai.
a_generate_oai_reply[](#a_generate_oai_reply)
async def a_generate_oai_reply(
messages: Optional[List[Dict]] = None,
sender: Optional[Agent] = None,
config: Optional[Any] = None) -> Tuple[bool, Union[str, Dict, None]]
Generate a reply using autogen.oai asynchronously.
generate_code_execution_reply[](#generate_code_execution_reply)
def generate_code_execution_reply(
messages: Optional[List[Dict]] = None,
sender: Optional[Agent] = None,
config: Optional[Union[Dict, Literal[False]]] = None)
Generate a reply using code execution.
generate_function_call_reply[](#generate_function_call_reply)
def generate_function_call_reply(
messages: Optional[List[Dict]] = None,
sender: Optional[Agent] = None,
config: Optional[Any] = None) -> Tuple[bool, Union[Dict, None]]
Generate a reply using function call.
"function_call" replaced by "tool_calls" as of [OpenAI API v1.1.0](https://github.com/openai/openai-python/releases/tag/v1.1.0)
See [https://platform.openai.com/docs/api-reference/chat/create#chat-create-functions](https://platform.openai.com/docs/api-reference/chat/create#chat-create-functions)
a_generate_function_call_reply[](#a_generate_function_call_reply)
async def a_generate_function_call_reply(
messages: Optional[List[Dict]] = None,
sender: Optional[Agent] = None,
config: Optional[Any] = None) -> Tuple[bool, Union[Dict, None]]
Generate a reply using async function call.
"function_call" replaced by "tool_calls" as of [OpenAI API v1.1.0](https://github.com/openai/openai-python/releases/tag/v1.1.0)
See [https://platform.openai.com/docs/api-reference/chat/create#chat-create-functions](https://platform.openai.com/docs/api-reference/chat/create#chat-create-functions)
generate_tool_calls_reply[](#generate_tool_calls_reply)
def generate_tool_calls_reply(
messages: Optional[List[Dict]] = None,
sender: Optional[Agent] = None,
config: Optional[Any] = None) -> Tuple[bool, Union[Dict, None]]
Generate a reply using tool call.
a_generate_tool_calls_reply[](#a_generate_tool_calls_reply)
async def a_generate_tool_calls_reply(
messages: Optional[List[Dict]] = None,
sender: Optional[Agent] = None,
config: Optional[Any] = None) -> Tuple[bool, Union[Dict, None]]
Generate a reply using async function call.
check_termination_and_human_reply[](#check_termination_and_human_reply)
def check_termination_and_human_reply(
messages: Optional[List[Dict]] = None,
sender: Optional[Agent] = None,
config: Optional[Any] = None) -> Tuple[bool, Union[str, None]]
Check if the conversation should be terminated, and if human reply is provided.
This method checks for conditions that require the conversation to be terminated, such as reaching a maximum number of consecutive auto-replies or encountering a termination message. Additionally, it prompts for and processes human input based on the configured human input mode, which can be 'ALWAYS', 'NEVER', or 'TERMINATE'. The method also manages the consecutive auto-reply counter for the conversation and prints relevant messages based on the human input received.
Arguments:
- messages (Optional[List[Dict]]): A list of message dictionaries, representing the conversation history.
- sender (Optional[Agent]): The agent object representing the sender of the message.
- config (Optional[Any]): Configuration object, defaults to the current instance if not provided.
Returns:
- Tuple[bool, Union[str, Dict, None]]: A tuple containing a boolean indicating if the conversation should be terminated, and a human reply which can be a string, a dictionary, or None.
a_check_termination_and_human_reply[](#a_check_termination_and_human_reply)
async def a_check_termination_and_human_reply(
messages: Optional[List[Dict]] = None,
sender: Optional[Agent] = None,
config: Optional[Any] = None) -> Tuple[bool, Union[str, None]]
(async) Check if the conversation should be terminated, and if human reply is provided.
This method checks for conditions that require the conversation to be terminated, such as reaching a maximum number of consecutive auto-replies or encountering a termination message. Additionally, it prompts for and processes human input based on the configured human input mode, which can be 'ALWAYS', 'NEVER', or 'TERMINATE'. The method also manages the consecutive auto-reply counter for the conversation and prints relevant messages based on the human input received.
Arguments:
- messages (Optional[List[Dict]]): A list of message dictionaries, representing the conversation history.
- sender (Optional[Agent]): The agent object representing the sender of the message.
- config (Optional[Any]): Configuration object, defaults to the current instance if not provided.
Returns:
- Tuple[bool, Union[str, Dict, None]]: A tuple containing a boolean indicating if the conversation should be terminated, and a human reply which can be a string, a dictionary, or None.
generate_reply[](#generate_reply)
def generate_reply(messages: Optional[List[Dict[str, Any]]] = None,
sender: Optional["Agent"] = None,
**kwargs: Any) -> Union[str, Dict, None]
Reply based on the conversation history and the sender.
Either messages or sender must be provided.
Register a reply_func with None
as one trigger for it to be activated when messages
is non-empty and sender
is None
.
Use registered auto reply functions to generate replies.
By default, the following functions are checked in order:
- check_termination_and_human_reply
- generate_function_call_reply (deprecated in favor of tool_calls)
- generate_tool_calls_reply
- generate_code_execution_reply
- generate_oai_reply Every function returns a tuple (final, reply). When a function returns final=False, the next function will be checked. So by default, termination and human reply will be checked first. If not terminating and human reply is skipped, execute function or code and return the result. AI replies are generated only when no code execution is performed.
Arguments:
-
messages
- a list of messages in the conversation history. -
sender
- sender of an Agent instance.Additional keyword arguments:
-
exclude
List[Callable] - a list of reply functions to be excluded.
Returns:
str or dict or None: reply. None if no reply is generated.
a_generate_reply[](#a_generate_reply)
async def a_generate_reply(messages: Optional[List[Dict[str, Any]]] = None,
sender: Optional["Agent"] = None,
**kwargs: Any) -> Union[str, Dict[str, Any], None]
(async) Reply based on the conversation history and the sender.
Either messages or sender must be provided.
Register a reply_func with None
as one trigger for it to be activated when messages
is non-empty and sender
is None
.
Use registered auto reply functions to generate replies.
By default, the following functions are checked in order:
- check_termination_and_human_reply
- generate_function_call_reply
- generate_tool_calls_reply
- generate_code_execution_reply
- generate_oai_reply Every function returns a tuple (final, reply). When a function returns final=False, the next function will be checked. So by default, termination and human reply will be checked first. If not terminating and human reply is skipped, execute function or code and return the result. AI replies are generated only when no code execution is performed.
Arguments:
-
messages
- a list of messages in the conversation history. -
sender
- sender of an Agent instance.Additional keyword arguments:
-
exclude
List[Callable] - a list of reply functions to be excluded.
Returns:
str or dict or None: reply. None if no reply is generated.
get_human_input[](#get_human_input)
def get_human_input(prompt: str) -> str
Get human input.
Override this method to customize the way to get human input.
Arguments:
prompt
str - prompt for the human input.
Returns:
str
- human input.
a_get_human_input[](#a_get_human_input)
async def a_get_human_input(prompt: str) -> str
(Async) Get human input.
Override this method to customize the way to get human input.
Arguments:
prompt
str - prompt for the human input.
Returns:
str
- human input.
run_code[](#run_code)
def run_code(code, **kwargs)
Run the code and return the result.
Override this function to modify the way to run the code.
Arguments:
code
str - the code to be executed.**kwargs
- other keyword arguments.
Returns:
A tuple of (exitcode, logs, image).
exitcode
int - the exit code of the code execution.logs
str - the logs of the code execution.image
str or None - the docker image used for the code execution.
execute_code_blocks[](#execute_code_blocks)
def execute_code_blocks(code_blocks)
Execute the code blocks and return the result.
execute_function[](#execute_function)
def execute_function(func_call,
verbose: bool = False) -> Tuple[bool, Dict[str, str]]
Execute a function call and return the result.
Override this function to modify the way to execute function and tool calls.
Arguments:
func_call
- a dictionary extracted from openai message at "function_call" or "tool_calls" with keys "name" and "arguments".
Returns:
A tuple of (is_exec_success, result_dict).
-
is_exec_success
boolean - whether the execution is successful. -
result_dict
- a dictionary with keys "name", "role", and "content". Value of "role" is "function"."function_call" deprecated as of
[OpenAI API v1.1.0](https://github.com/openai/openai-python/releases/tag/v1.1.0)See[https://platform.openai.com/docs/api-reference/chat/create#chat-create-function_call](https://platform.openai.com/docs/api-reference/chat/create#chat-create-function_call)
a_execute_function[](#a_execute_function)
async def a_execute_function(func_call)
Execute an async function call and return the result.
Override this function to modify the way async functions and tools are executed.
Arguments:
func_call
- a dictionary extracted from openai message at key "function_call" or "tool_calls" with keys "name" and "arguments".
Returns:
A tuple of (is_exec_success, result_dict).
-
is_exec_success
boolean - whether the execution is successful. -
result_dict
- a dictionary with keys "name", "role", and "content". Value of "role" is "function"."function_call" deprecated as of
[OpenAI API v1.1.0](https://github.com/openai/openai-python/releases/tag/v1.1.0)See[https://platform.openai.com/docs/api-reference/chat/create#chat-create-function_call](https://platform.openai.com/docs/api-reference/chat/create#chat-create-function_call)
generate_init_message[](#generate_init_message)
def generate_init_message(message: Union[Dict, str, None],
**kwargs) -> Union[str, Dict]
Generate the initial message for the agent. If message is None, input() will be called to get the initial message.
Arguments:
message
str or None - the message to be processed.**kwargs
- any additional information. It has the following reserved fields:"carryover"
- a string or a list of string to specify the carryover information to be passed to this chat. It can be a string or a list of string. If provided, we will combine this carryover with the "message" content when generating the initial chat message.
Returns:
str or dict: the processed message.
a_generate_init_message[](#a_generate_init_message)
async def a_generate_init_message(message: Union[Dict, str, None],
**kwargs) -> Union[str, Dict]
Generate the initial message for the agent. If message is None, input() will be called to get the initial message.
Arguments:
Please refer to generate_init_message
for the description of the arguments.
Returns:
str or dict: the processed message.
register_function[](#register_function)
def register_function(function_map: Dict[str, Union[Callable, None]])
Register functions to the agent.
Arguments:
function_map
- a dictionary mapping function names to functions. if function_map[name] is None, the function will be removed from the function_map.
update_function_signature[](#update_function_signature)
def update_function_signature(func_sig: Union[str, Dict], is_remove: None)
update a function_signature in the LLM configuration for function_call.
Arguments:
-
func_sig
str or dict - description/name of the function to update/remove to the model. See:[https://platform.openai.com/docs/api-reference/chat/create#chat/create-functions](https://platform.openai.com/docs/api-reference/chat/create#chat/create-functions) -
is_remove
- whether removing the function from llm_config with name 'func_sig'Deprecated as of
[OpenAI API v1.1.0](https://github.com/openai/openai-python/releases/tag/v1.1.0)See[https://platform.openai.com/docs/api-reference/chat/create#chat-create-function_call](https://platform.openai.com/docs/api-reference/chat/create#chat-create-function_call)
update_tool_signature[](#update_tool_signature)
def update_tool_signature(tool_sig: Union[str, Dict], is_remove: None)
update a tool_signature in the LLM configuration for tool_call.
Arguments:
tool_sig
str or dict - description/name of the tool to update/remove to the model. See:[https://platform.openai.com/docs/api-reference/chat/create#chat-create-tools](https://platform.openai.com/docs/api-reference/chat/create#chat-create-tools)is_remove
- whether removing the tool from llm_config with name 'tool_sig'
can_execute_function[](#can_execute_function)
def can_execute_function(name: Union[List[str], str]) -> bool
Whether the agent can execute the function.
function_map[](#function_map)
@property
def function_map() -> Dict[str, Callable]
Return the function map.
register_for_llm[](#register_for_llm)
def register_for_llm(
*,
name: Optional[str] = None,
description: Optional[str] = None,
api_style: Literal["function", "tool"] = "tool") -> Callable[[F], F]
Decorator factory for registering a function to be used by an agent.
It's return value is used to decorate a function to be registered to the agent. The function uses type hints to specify the arguments and return type. The function name is used as the default name for the function, but a custom name can be provided. The function description is used to describe the function in the agent's configuration.
Arguments:
name (optional(str)): name of the function. If None, the function name will be used (default: None). description (optional(str)): description of the function (default: None). It is mandatory for the initial decorator, but the following ones can omit it.
api_style
- (literal): the API style for function call. For Azure OpenAI API, use version 2023-12-01-preview or later."function"
style will be deprecated. For earlier version use"function"
if"tool"
doesn't work. See[Azure OpenAI documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/function-calling?tabs=python)for details.
Returns:
The decorator for registering a function to be used by an agent.
Examples:
```
@user_proxy.register_for_execution()
@agent2.register_for_llm()
@agent1.register_for_llm(description="This is a very useful function")
def my_function(a: Annotated[str, "description of a parameter"] = "a", b: int, c=3.14) -> str:
return a + str(b * c)
```
For Azure OpenAI versions prior to 2023-12-01-preview, set api_style
to "function"
if "tool"
doesn't work:
@agent2.register_for_llm(api_style="function") def my_function(a: Annotated[str, "description of a parameter"] = "a", b: int, c=3.14) -> str: return a + str(b * c)
register_for_execution[](#register_for_execution)
def register_for_execution(name: Optional[str] = None) -> Callable[[F], F]
Decorator factory for registering a function to be executed by an agent.
It's return value is used to decorate a function to be registered to the agent.
Arguments:
name (optional(str)): name of the function. If None, the function name will be used (default: None).
Returns:
The decorator for registering a function to be used by an agent.
Examples:
```
@user_proxy.register_for_execution()
@agent2.register_for_llm()
@agent1.register_for_llm(description="This is a very useful function")
def my_function(a: Annotated[str, "description of a parameter"] = "a", b: int, c=3.14):
return a + str(b * c)
```
register_model_client[](#register_model_client)
def register_model_client(model_client_cls: ModelClient, **kwargs)
Register a model client.
Arguments:
model_client_cls
- A custom client class that follows the Client interface**kwargs
- The kwargs for the custom client class to be initialized with
register_hook[](#register_hook)
def register_hook(hookable_method: str, hook: Callable)
Registers a hook to be called by a hookable method, in order to add a capability to the agent. Registered hooks are kept in lists (one per hookable method), and are called in their order of registration.
Arguments:
hookable_method
- A hookable method name implemented by ConversableAgent.hook
- A method implemented by a subclass of AgentCapability.
process_all_messages_before_reply[](#process_all_messages_before_reply)
def process_all_messages_before_reply(messages: List[Dict]) -> List[Dict]
Calls any registered capability hooks to process all messages, potentially modifying the messages.
a_process_all_messages_before_reply[](#a_process_all_messages_before_reply)
async def a_process_all_messages_before_reply(
messages: List[Dict]) -> List[Dict]
Calls any registered capability hooks to process all messages, potentially modifying the messages.
process_last_received_message[](#process_last_received_message)
def process_last_received_message(messages: List[Dict]) -> List[Dict]
Calls any registered capability hooks to use and potentially modify the text of the last message, as long as the last message is not a function call or exit command.
a_process_last_received_message[](#a_process_last_received_message)
async def a_process_last_received_message(messages: List[Dict]) -> List[Dict]
Calls any registered capability hooks to use and potentially modify the text of the last message, as long as the last message is not a function call or exit command.
print_usage_summary[](#print_usage_summary)
def print_usage_summary(
mode: Union[str, List[str]] = ["actual", "total"]) -> None
Print the usage summary.
get_actual_usage[](#get_actual_usage)
def get_actual_usage() -> Union[None, Dict[str, int]]
Get the actual usage summary.
get_total_usage[](#get_total_usage)
def get_total_usage() -> Union[None, Dict[str, int]]
Get the total usage summary.
register_function[](#register_function-1)
def register_function(f: Callable[..., Any],
*,
caller: ConversableAgent,
executor: ConversableAgent,
name: Optional[str] = None,
description: str) -> None
Register a function to be proposed by an agent and executed for an executor.
This function can be used instead of function decorators @ConversationAgent.register_for_llm
and
@ConversationAgent.register_for_execution
.
Arguments:
f
- the function to be registered.caller
- the agent calling the function, typically an instance of ConversableAgent.executor
- the agent executing the function, typically an instance of UserProxy.name
- name of the function. If None, the function name will be used (default: None).description
- description of the function. The description is used by LLM to decode whether the function is called. Make sure the description is properly describing what the function does or it might not be called by LLM when needed.