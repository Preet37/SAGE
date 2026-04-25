# Card: NeMo ReAct Agent (Thought/Action/Observation Loop)
**Source:** https://docs.nvidia.com/nemo/agent-toolkit/1.3/workflows/about/react-agent.html  
**Role:** reference_doc | **Need:** WORKING_EXAMPLE  
**Anchor:** End-to-end ReAct agent workflow structure + tool registration/invocation + loop orchestration in NeMo Agent Toolkit

## Key Content
- **ReAct loop (workflow):** Observation (receive question) → **Thought** (reason step-by-step) → **Action** (select tool by name/description) → **Action Input** → **Observation** (tool result) → repeat until **Final Answer**.
- **Required ReAct output formats (prompt contract):**
  - Tool call:
    - `Question: ...`
    - `Thought: ...`
    - `Action: <one of [{tool_names}]>`
    - `Action Input: <JSON object or "None">`
    - `Observation: wait for the human/tool response; do not assume`
  - Final:
    - `Thought: I now know the final answer`
    - `Final Answer: ...`
- **Prompt variables required when customizing:** must include `{tools}` and `{tool_names}` and instruct the model to emit the ReAct format.
- **YAML configuration (as workflow):**
  - `workflow: _type: react_agent`
  - `tool_names: [wikipedia_search, current_datetime, code_generation, math_agent]`
  - `llm_name: nim_llm`
  - Example: `verbose: true`, `parse_agent_response_max_retries: 2`
- **YAML configuration (as function/tool):** define tools under `functions:` then `_type: react_agent`, `tool_names: [...]`, optional `description` (tool description when exposed to other agents).
- **Defaults/parameters:**
  - `verbose: False`
  - `retry_agent_response_parsing_errors: True`
  - `parse_agent_response_max_retries: 1`
  - `tool_call_max_retries: 1`
  - `max_tool_calls: 15`
  - `pass_tool_call_errors_to_agent: True`
  - `normalize_tool_input_quotes: True` (fallback: replace single→double quotes for JSON parsing)
  - `max_history: 15`
  - `include_tool_input_schema_in_tool_description: True` (appends: `Arguments must be provided as a valid JSON object following this format: {tool_schema}`)
  - `workflow_alias: None`
  - `description: "ReAct Agent Workflow"`
- **Design rationale / limitations:** sequential Think→Act→Observe increases LLM calls (latency/cost), prompt-sensitive, hallucination risk, error propagation in long chains, no parallelism.
- **Requirement:** install `nvidia-nat[langchain]`.

## When to surface
Use when students ask how a ReAct agent is structured in practice (prompt format, tool routing, YAML setup) or how NeMo controls retries, max tool calls, history, and tool-input parsing.