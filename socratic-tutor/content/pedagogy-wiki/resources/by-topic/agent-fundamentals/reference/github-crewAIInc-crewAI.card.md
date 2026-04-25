# Card: CrewAI Agent/Crew/Flow Fundamentals (repo + docs entrypoints)
**Source:** https://github.com/crewAIInc/crewAI  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Authoritative surfaces for creating Agents/Tasks/Crews, selecting process modes, and orchestrating Crews inside Flows; install/run defaults and telemetry controls.

## Key Content
- **Install / environment**
  - Requires **Python >= 3.10 and < 3.14**.
  - Install: `uv pip install crewai`; optional tools: `uv pip install 'crewai[tools]'`; embeddings/tiktoken fix: `uv pip install 'crewai[embeddings]'`.
  - Default model connection: **OpenAI API by default** (set `OPENAI_API_KEY`); other LLMs via docs “LLM Connections” (e.g., local models).
- **Project scaffold (CLI procedure)**
  - Create: `crewai create crew <project_name>` → generates `src/<project>/main.py`, `crew.py`, `config/agents.yaml`, `config/tasks.yaml`, `tools/`.
  - Run: `crewai run` or `python src/<project>/main.py`. Dependency ops: `crewai install` (optional), `crewai update` if poetry-related error.
- **Core orchestration parameters (shown in examples)**
  - `Crew(agents=[...], tasks=[...], process=Process.sequential, verbose=True)`  
  - Process modes mentioned: **sequential** and **hierarchical** (hierarchical “assigns a manager” for planning/delegation/validation).
  - `Task(description="... {var} ...", expected_output="...", agent=<Agent>, output_file="report.md")`
  - `Crew.kickoff(inputs={...})` passes named template variables into task descriptions.
- **Flows: event-driven control + conditions**
  - Decorators: `@start`, `@listen`, `@router`; logical combinators: `or_(...)`, `and_(...)`.
  - Pattern: Flow step returns dict matching task template vars; later step runs a Crew and routes based on state.
- **Empirical comparison (repo claim)**
  - CrewAI Flows reported **5.76× faster** than LangGraph in a QA task example (linked notebook).
- **Telemetry defaults/control**
  - Anonymous telemetry collects: CrewAI/Python versions, OS/CPU class, #agents/#tasks, process type, whether memory/delegation used, parallel vs sequential, model used, roles, tool names.
  - Disable via env var: `OTEL_SDK_DISABLED=true`. Opt-in detailed telemetry: `Crew(share_crew=True)`.

## When to surface
Use when students ask how to *instantiate/run* CrewAI agents/crews/flows, choose **process** (sequential vs hierarchical), pass **inputs** into tasks, or control **telemetry** and installation/runtime defaults.