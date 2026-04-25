# Card: OpenAI Agents SDK — Examples Index (Patterns & Multi-Agent Building Blocks)
**Source:** https://openai.github.io/openai-agents-python/examples/  
**Role:** code | **Need:** WORKING_EXAMPLE  
**Anchor:** Runnable end-to-end examples demonstrating agent composition and handoffs (supervisor-to-specialist patterns) with concrete execution flow and payload shapes.

## Key Content
- **Where to find runnable implementations:** All examples live in the repo under `examples/` with categorized subfolders: https://github.com/openai/openai-agents-python/tree/main/examples
- **Agent design patterns (multi-agent relevant):** `examples/agent_patterns/` includes concrete patterns for:
  - **Agents as tools** (including streaming events):  
    - `examples/agent_patterns/agents_as_tools_streaming.py`  
    - **Structured tool inputs:** `examples/agent_patterns/agents_as_tools_structured.py`
  - **Parallel agent execution** (pattern category explicitly listed).
  - **Conditional tool usage** and **forcing tool use**: `examples/agent_patterns/forcing_tool_use.py`
  - **Guardrails & judging:** input/output guardrails, “LLM as a judge,” routing, streaming guardrails.
  - **Human-in-the-loop (HITL)** with approval + state serialization:  
    - `examples/agent_patterns/human_in_the_loop.py`  
    - Streaming HITL: `examples/agent_patterns/human_in_the_loop_stream.py`  
    - Custom rejection messages: `examples/agent_patterns/human_in_the_loop_custom_rejection.py`
- **Handoffs (delegation/message filtering):** `examples/handoffs/` provides practical handoff flows with message filtering:
  - `examples/handoffs/message_filter.py`
  - Streaming variant: `examples/handoffs/message_filter_streaming.py`
- **Basic execution plumbing useful for orchestration:** `examples/basic/` includes lifecycle hooks (`examples/basic/lifecycle_example.py`), streaming outputs, retry management (`examples/basic/retry.py`), and websocket streaming with shared session helper (`examples/basic/stream_ws.py`).

## When to surface
Use this card when a student asks “Where’s a working example of supervisor→specialist delegation, handoffs, message filtering, parallel agents, or HITL approvals/streaming in the OpenAI Agents Python SDK?”