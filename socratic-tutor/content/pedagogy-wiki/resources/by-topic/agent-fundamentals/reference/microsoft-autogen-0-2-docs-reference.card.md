# Card: AutoGen 0.2 AgentChat API—core knobs & orchestration entry points
**Source:** https://microsoft.github.io/autogen/0.2/docs/reference/  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Cross-class defaults/knobs beyond `ConversableAgent` (multi-agent orchestration, tool/code execution utilities, termination/turn limits)

## Key Content
- **Agent definition (conceptual contract):** In AutoGen, an *agent* is an entity that can **send messages**, **receive messages**, and **generate a reply** using **models, tools, human inputs, or mixtures**.
- **Built-in agent baseline:** `ConversableAgent` supports configurable components including:
  - **List of LLMs** via `llm_config`
  - **Function/tool executor**
  - **Human-in-the-loop component**
  - Extensibility via `registered_reply` (add custom reply behaviors/components).
- **Key configuration defaults/knobs shown:**
  - `code_execution_config=False` → code execution **off** (example explicitly notes default off).
  - `human_input_mode="NEVER"` → fully autonomous (never asks user for input).
  - `llm_config={"config_list":[{"model":"gpt-4","api_key":...}]}` → canonical multi-config pattern.
- **Core procedures (agent loop entry points):**
  - Single-turn reply: `generate_reply(messages=[{"role":"user","content":...}])`
  - Multi-turn agent-to-agent chat: `initiate_chat(other_agent, message=..., max_turns=2)` (example uses `max_turns=2` to cap dialogue length).
- **Code execution utilities (executors):**
  - Local: `autogen.coding.LocalCommandLineCodeExecutor(work_dir="coding")`
  - Docker (context-managed): `with autogen.coding.DockerCommandLineCodeExecutor(work_dir="coding") as code_executor: ...`
  - Passed into `UserProxyAgent(..., code_execution_config={"executor": code_executor})`
- **Design rationale (stated):** Multi-agent conversations simplify **orchestration/automation/optimization** of complex LLM workflows; modular components enable composability and maintainability.

## When to surface
Use when students ask how to configure AutoGen 0.2 agents (LLM config, autonomy/human input, code execution), start agent-to-agent chats, cap turns/termination via `max_turns`, or choose Local vs Docker code executors.