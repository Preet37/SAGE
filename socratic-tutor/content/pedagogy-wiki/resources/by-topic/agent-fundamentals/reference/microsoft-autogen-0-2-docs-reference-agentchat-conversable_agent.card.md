# Card: AutoGen ConversableAgent knobs (init + reply loop)
**Source:** https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/conversable_agent/  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** `ConversableAgent.__init__` signature + defaults; `human_input_mode`; `MAX_CONSECUTIVE_AUTO_REPLY` behavior; default reply-function order

## Key Content
- **Core behavior (agent loop):** After receiving each message, agent sends a reply unless message is a termination message. Override `generate_reply()` to change auto-reply behavior.
- **Constructor signature + defaults:**
  - `__init__(name, system_message="You are a helpful AI Assistant.", is_termination_msg=None, max_consecutive_auto_reply=None, human_input_mode="TERMINATE", function_map=None, code_execution_config=False, llm_config=None, default_auto_reply="", description=None, chat_messages=None, silent=None)`
  - `description` default: `system_message`.
  - `llm_config`: `None` ⇒ uses `self.DEFAULT_CONFIG` (defaults to `False`); `False` disables LLM-based auto reply.
  - `code_execution_config=False` disables code execution; if dict: keys include `work_dir`, `use_docker` (default `True`), `timeout`, `last_n_messages` (default `"auto"`).
- **Consecutive auto-reply limit (Eq. 1):**
  - Let `N = max_consecutive_auto_reply`.
  - If `N is None`: use class attribute `MAX_CONSECUTIVE_AUTO_REPLY` as limit.
  - If `N = 0`: **no auto reply** generated.
- **Human input modes (procedural rules):**
  - `"ALWAYS"`: prompt human every received message; stop if human input is `"exit"` OR (`is_termination_msg` true and no human input).
  - `"TERMINATE"` (default): prompt human only on termination msg OR when auto-reply count reaches `N`.
  - `"NEVER"`: never prompt; stop when auto-reply count reaches `N` OR `is_termination_msg` true.
- **Default reply-function chain (order matters):**
  1) `check_termination_and_human_reply` → 2) `generate_function_call_reply` (deprecated) → 3) `generate_tool_calls_reply` → 4) `generate_code_execution_reply` → 5) `generate_oai_reply`.  
  Each returns `(final, reply)`; if `final=False`, continue to next.

## When to surface
Use when students ask how AutoGen agents decide to reply/stop, how to control autonomy vs human-in-the-loop, or how tool/code/LLM replies are prioritized and limited.