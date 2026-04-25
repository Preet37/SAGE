## Key Facts & Specifications

### Canonical agent definitions & properties (classical AI / MAS)
- **Agent (Russell & Norvig / AIMA)**: “An agent is anything that can be viewed as perceiving its environment through sensors and acting upon that environment through effectors.” (Russell & Norvig, *AIMA* Ch. 2 PDF: https://people.eecs.berkeley.edu/~russell/aima1e/chapter02.pdf)
- **Intelligent agent (Russell & Norvig lecture slides)**: “An intelligent agent perceives its environment via sensors and acts rationally upon that environment with its effectors.” (Russell & Norvig Ch. 2 slides: https://cs.brynmawr.edu/Courses/cs372/spring2012/slides/02_IntelligentAgents.pdf)
- **Discrete agent mapping**: “A discrete agent receives percepts one at a time, and maps this percept sequence to a sequence of discrete actions.” (Russell & Norvig Ch. 2 slides: https://cs.brynmawr.edu/Courses/cs372/spring2012/slides/02_IntelligentAgents.pdf)
- **Agent properties listed in Russell & Norvig slides**:
  - Autonomous
  - Reactive to the environment
  - Pro-active (goal-directed)
  - Interacts with other agents via the environment  
  (Russell & Norvig Ch. 2 slides: https://cs.brynmawr.edu/Courses/cs372/spring2012/slides/02_IntelligentAgents.pdf)
- **“Flexible autonomous action” properties (Wooldridge)**: An intelligent agent is capable of flexible autonomous action, where “flexible” means:
  - **reactivity** (respond in a timely fashion to changes),
  - **pro-activeness** (goal-directed, taking initiative),
  - **social ability** (interacting with other agents/humans).  
  (Wooldridge, *MAS99* PDF: https://www.cs.ox.ac.uk/people/michael.wooldridge/pubs/mas99.pdf)
- **Wooldridge & Jennings (1995) attributes** (as summarized in their “Software Agents” article):
  - **Autonomy**: perform most tasks without direct intervention; control over actions/internal state
  - **Social ability**
  - **Responsiveness** (timely response to environment changes)
  - **Proactiveness** (opportunistic, goal-directed initiative)  
  (Wooldridge & Jennings, “Software Agents” PDF: http://www.cs.ox.ac.uk/people/michael.wooldridge/pubs/iee-review96.pdf; and “Intelligent Agents: Theory and Practice” record: https://eprints.soton.ac.uk/252102/)

### Rationality & autonomy (Russell & Norvig)
- **Ideal rational agent**: for each percept sequence, choose actions that **maximize expected performance measure** based on (1) percept sequence and (2) built-in/acquired knowledge. (Russell & Norvig Ch. 2 slides: https://cs.brynmawr.edu/Courses/cs372/spring2012/slides/02_IntelligentAgents.pdf)
- **Autonomy (degree)**: “A system is autonomous to the extent that its own behavior is determined by its own experience.” Not autonomous if guided by designer’s a priori decisions; to survive, agents need enough built-in knowledge + ability to learn. (Russell & Norvig Ch. 2 slides: https://cs.brynmawr.edu/Courses/cs372/spring2012/slides/02_IntelligentAgents.pdf)

### Environment taxonomy (Russell & Norvig)
- Environment property pairs defined (with definitions) in the slides:
  - Fully observable vs partially observable
  - Deterministic vs stochastic
  - Episodic vs sequential
  - Static vs dynamic
  - Discrete vs continuous
  - Single-agent vs multi-agent  
  (Russell & Norvig Ch. 2 slides: https://cs.brynmawr.edu/Courses/cs372/spring2012/slides/02_IntelligentAgents.pdf)

### ReAct: verified benchmark deltas (paper/blog summary)
- ReAct interleaves **reasoning traces** and **actions**, with **observation feedback** from an external environment. (Google Research blog: https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/; arXiv: https://arxiv.org/abs/2210.03629)
- Reported results:
  - On **ALFWorld** and **WebShop**, ReAct outperforms imitation and reinforcement learning methods trained with **~10^5 task instances**, with **absolute improvements of 34% and 10%** in success rates, respectively, using **one-shot or two-shot prompting**. (Google Research blog: https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/; arXiv: https://arxiv.org/abs/2210.03629)

### AutoGPT operational/safety facts (CLI + sandboxing)
- AutoGPT CLI entrypoints:
  - `python -m autogpt run` (CLI mode)
  - `python -m autogpt serve` (Agent Protocol server + UI)  
  (AutoGPT docs: https://docs.agpt.co/classic/usage/)
- **Continuous Mode warning**: “Run the AI without user authorization, 100% automated. Continuous mode is NOT recommended. It is potentially dangerous and may cause your AI to run forever or carry out actions you would not usually authorize.” (AutoGPT docs: https://docs.agpt.co/classic/usage/)
- **Agent state storage location**: `data/agents` folder. (AutoGPT docs: https://docs.agpt.co/classic/usage/)
- **Workspace restriction**:
  - Agent workspace is `data/agents/<agent_id>/workspace`
  - Files outside workspace cannot be accessed **unless** `RESTRICT_TO_WORKSPACE` is set to `False`
  - Disabling restriction is not recommended unless sandboxed (Docker/VM).  
  (AutoGPT docs: https://docs.agpt.co/classic/usage/)

### OpenAI tool/function calling: schema fields & strictness
- Function tools are defined with JSON Schema in the `tools` parameter; function definition fields include:
  - `type` (always `function`)
  - `name`
  - `description`
  - `parameters` (JSON schema)
  - `strict` (enforce strict mode)  
  (OpenAI Function calling guide: https://platform.openai.com/docs/guides/function-calling)
- Example schema includes `additionalProperties: false` and `strict: true`. (OpenAI Function calling guide: https://platform.openai.com/docs/guides/function-calling)

### OpenAI Agents SDK: human approval interruptions & serialization
- If a tool requires approval, the SDK pauses the run and returns pending approvals in `interruptions`; approvals are resolved via:
  - `result.state.approve(interruption)` / `result.state.reject(interruption)`
  - Optional sticky decisions: `{ alwaysApprove: true }` / `{ alwaysReject: true }`  
  (OpenAI Agents JS guide: https://openai.github.io/openai-agents-js/guides/human-in-the-loop/)
- Run state can be serialized and resumed:
  - Serialize: `result.state.toString()` (or `JSON.stringify(result.state)`)
  - Resume: `RunState.fromString(agent, serializedState)`
  - Or inject new context: `RunState.fromStringWithContext(agent, serializedState, context, { contextStrategy })`
  - `contextStrategy: 'merge'` (default) or `'replace'`  
  (OpenAI Agents JS guide: https://openai.github.io/openai-agents-js/guides/human-in-the-loop/)

### AutoGen: multi-agent conversation mechanics (0.2 docs)
- AutoGen provides a “multi-agent conversation framework” with “conversable agents” integrating LLMs, tools, and humans via automated agent chat. (AutoGen 0.2 docs: https://microsoft.github.io/autogen/0.2/docs/Use-Cases/agent_chat/)
- Two representative subclasses:
  - `AssistantAgent`: uses LLMs by default; can write Python code blocks; can receive execution results; configurable via `llm_config`. (AutoGen 0.2 docs: https://microsoft.github.io/autogen/0.2/docs/Use-Cases/agent_chat/)
  - `UserProxyAgent`: proxy for humans; can execute code; triggers code execution automatically when it detects an executable code block and no human input is provided. (AutoGen 0.2 docs: https://microsoft.github.io/autogen/0.2/docs/Use-Cases/agent_chat/)

### Retry/backoff numeric defaults (example implementation)
- Example “gold standard” exponential backoff config:
  - `initialDelayMs: 1000`
  - `maxDelayMs: 60000`
  - `maxRetries: 5`
  - `multiplier: 2`
  - `jitterFactor: 0.3`  
  (Athenic blog: https://getathenic.com/blog/ai-agent-retry-strategies-exponential-backoff)

### Vector-store “long-term memory” example parameters (practitioner tutorial)
- Example RAG memory tool configuration:
  - `toolName: "RAG_MEMORY"`
  - `qdrantCollection: "ltm"`
  - `topK: 20`
  - `useReranker: true`  
  (DEV Community tutorial: https://dev.to/einarcesar/long-term-memory-for-llms-using-vector-store-a-practical-approach-with-n8n-and-qdrant-2ha7)
- Claimed effects (note: practitioner claim, not a formal study):
  - Token consumption reduced “typically by **60–80%** in extended interactions”
  - Added latency “**200–500ms**” per query  
  (DEV Community tutorial: same URL as above)

---

## Technical Details & Procedures

### OpenAI Function/Tool Calling (API-level flow)
Verified “tool calling flow” steps (5-step loop):
1. Make a request to the model with tools it could call
2. Receive a tool call from the model
3. Execute code on the application side with input from the tool call
4. Make a second request to the model with the tool output
5. Receive a final response (or more tool calls)  
(OpenAI Function calling guide: https://platform.openai.com/docs/guides/function-calling)

**Python example skeleton (as shown in guide; key fields):**
- Request: `client.responses.create(model="gpt-5", tools=tools, input=input_list, ...)`
- Tool call items appear in `response.output` with `item.type == "function_call"`
- Tool output is appended as:
  - `{"type": "function_call_output", "call_id": item.call_id, "output": json.dumps({...})}`  
(OpenAI Function calling guide: https://platform.openai.com/docs/guides/function-calling)

**Function schema knobs explicitly shown:**
- `parameters.type: "object"`
- `properties` with types/enums/descriptions
- `required: [...]`
- `additionalProperties: false`
- `strict: true`  
(OpenAI Function calling guide: https://platform.openai.com/docs/guides/function-calling)

### OpenAI Agents SDK (JS): approval-based human-in-the-loop
**How to mark a tool as requiring approval:**
- Set `needsApproval` to `true` or to an async function returning boolean. (OpenAI Agents JS guide: https://openai.github.io/openai-agents-js/guides/human-in-the-loop/)

**Approval workflow (exact sequence):**
1. Before tool invocation executes, SDK evaluates approval rule (`needsApproval` or hosted MCP equivalent).
2. If approval required and no decision stored, tool call does not execute; run records a `RunToolApprovalItem`.
3. End of turn: run pauses and returns pending approvals in `result.interruptions` (including nested `agent.asTool()`).
4. Resolve each pending item:
   - `result.state.approve(interruption)` or `result.state.reject(interruption)`
   - Optional: `{ alwaysApprove: true }` / `{ alwaysReject: true }`
   - Reject can include `{ message: "..." }` to control text sent back to model.
5. Resume: pass updated state back into `runner.run(agent, state)` using the original top-level agent.  
(OpenAI Agents JS guide: https://openai.github.io/openai-agents-js/guides/human-in-the-loop/)

**State persistence / resumption:**
- Serialize: `result.state.toString()` (or `JSON.stringify(result.state)`)
- Resume: `RunState.fromString(agent, serializedState)`
- Resume with new context: `RunState.fromStringWithContext(agent, serializedState, context, { contextStrategy })`
  - `contextStrategy: 'merge'` (default)
  - `contextStrategy: 'replace'`  
(OpenAI Agents JS guide: https://openai.github.io/openai-agents-js/guides/human-in-the-loop/)

### OpenAI Agents SDK (Python): runner loop (high-level)
- Runner loop described as:
  1. Call the LLM for the current agent with current input
  2. LLM produces output
     - If final output, loop ends
     - If handoff, update current agent/input and continue
     - If tool calls, run tool calls, append results, and continue  
(OpenAI Agents Python “Running agents”: https://openai.github.io/openai-agents-python/running_agents/)

### AutoGPT CLI commands & configuration
**Help / entrypoints:**
- `./autogpt.sh --help`
- `./autogpt.sh run --help`
- `./autogpt.sh serve --help`  
(AutoGPT docs: https://docs.agpt.co/classic/usage/)

**Run mode options (selected, exact flags):**
- `-c, --continuous`
- `-l, --continuous-limit INTEGER`
- `--component-config-file TEXT`  
(AutoGPT docs: https://docs.agpt.co/classic/usage/)

**Serve mode:**
- Default UI/API at `http://localhost:8000`
- Port configurable via env var `AP_SERVER_PORT`  
(AutoGPT docs: https://docs.agpt.co/classic/usage/)

**State & workspace:**
- Agent state stored in `data/agents`
- Workspace in `data/agents/<agent_id>/workspace`
- Restriction toggle: `RESTRICT_TO_WORKSPACE` (recommended to keep `True` unless sandboxed)  
(AutoGPT docs: https://docs.agpt.co/classic/usage/)

**Disable commands:**
- `DISABLED_COMMANDS` in `.env`, comma-separated
- Example: `DISABLED_COMMANDS=execute_python_code,execute_python_file`  
(AutoGPT docs: https://docs.agpt.co/classic/usage/)

### AutoGen (0.2) two-agent conversation setup (code shown)
- Create agents:
  - `AssistantAgent(name="assistant", llm_config={"config_list": config_list})`
  - `UserProxyAgent(name="user_proxy", code_execution_config={"executor": code_executor})`
- Start conversation:
  - `user_proxy.initiate_chat(assistant, message="...")`  
(AutoGen 0.2 docs: https://microsoft.github.io/autogen/0.2/docs/Use-Cases/agent_chat/)

### LangChain agent creation & middleware hooks (docs snippets)
- Python:
  - `agent = create_agent("openai:gpt-5", tools=tools)`  
  (LangChain Agents docs: https://docs.langchain.com/oss/python/langchain/agents)
- JS:
  - `const agent = createAgent({ model: "openai:gpt-5", tools: [] });`  
  (LangChain JS Agents docs: https://docs.langchain.com/oss/javascript/langchain/agents)
- Tool error middleware example returns a `ToolMessage` with `tool_call_id` (Python and JS examples shown).  
  (LangChain docs: same URLs as above)

### Retry strategy procedure (example code path)
- Error taxonomy table includes:
  - Retry 429 with backoff per `Retry-After`
  - Retry 500/502/503/504 with exponential backoff
  - Do not retry 401/403
  - Context length exceeded: 400 with message containing `context_length` → do not retry same request  
(Athenic blog: https://getathenic.com/blog/ai-agent-retry-strategies-exponential-backoff)

---

## Comparisons & Trade-offs

### Chatbot vs agent (grounded in definitions)
- Classical definitions emphasize **perceive → act** in an environment (AIMA; Russell & Norvig) rather than only producing text. (AIMA Ch.2 PDF: https://people.eecs.berkeley.edu/~russell/aima1e/chapter02.pdf)
- Wooldridge frames “intelligent agents” as **flexible autonomous action** with reactivity, pro-activeness, and social ability—properties that imply ongoing interaction rather than one-shot response. (Wooldridge MAS99 PDF: https://www.cs.ox.ac.uk/people/michael.wooldridge/pubs/mas99.pdf)

### ReAct vs “reason-only” (CoT) vs “act-only”
- ReAct is proposed to combine reasoning traces and actions interleaved, with observations feeding back into subsequent steps. (Google Research blog: https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/; arXiv: https://arxiv.org/abs/2210.03629)
- Reported benchmark deltas (interactive tasks):
  - ALFWorld: **+34% absolute** success rate vs imitation/RL baselines (trained with ~10^5 instances)
  - WebShop: **+10% absolute** success rate vs imitation/RL baselines (trained with ~10^5 instances)  
  (Same sources as above)

### ReAct vs Plan-and-Execute (architectural trade-off statements in results)
- Unstructured’s agent architecture article contrasts:
  - **ReAct**: iterative Think → Act → Observe loop; described as grounding in real-world data and producing more “reliable, auditable outcomes.”  
  - **Plan-and-Execute** (e.g., ReWOO): generate a complete plan of tool calls, execute, then respond; described as “more efficient” and allowing user confirmation, but “less adaptable to dynamic environments.”  
  (Unstructured blog: https://www.unstructured.io/blog/defining-the-autonomous-enterprise-reasoning-memory-and-the-core-capabilities-of-agentic-ai)

### Human-in-the-loop vs fully autonomous execution (safety/throughput)
- AutoGPT explicitly warns that continuous mode runs “without user authorization” and is “potentially dangerous.” (AutoGPT docs: https://docs.agpt.co/classic/usage/)
- OpenAI Agents SDK provides a concrete mechanism to implement human approval gates by pausing runs and resuming from `RunState`. (OpenAI Agents JS guide: https://openai.github.io/openai-agents-js/guides/human-in-the-loop/)

### Workspace sandboxing vs unrestricted file access (AutoGPT)
- Default: agent reads/writes within `data/agents/<agent_id>/workspace`.
- Unrestricted access requires `RESTRICT_TO_WORKSPACE=False`, which docs warn against unless sandboxed (Docker/VM).  
(AutoGPT docs: https://docs.agpt.co/classic/usage/)

### Long-term memory via vector store: benefits vs costs (practitioner claims)
- Benefits claimed: “60–80%” token reduction in extended interactions; “virtually unlimited memory capacity.” (DEV tutorial: https://dev.to/einarcesar/long-term-memory-for-llms-using-vector-store-a-practical-approach-with-n8n-and-qdrant-2ha7)
- Costs claimed: adds “200–500ms” latency due to vector search + reranking + extra calls. (Same DEV tutorial)

---

## Architecture & Design Rationale

### Why “looping” is central to agents (classical + modern)
- Classical agent framing: agents map percept sequences to action sequences; rationality is defined over percept histories and expected performance. (Russell & Norvig Ch. 2 slides: https://cs.brynmawr.edu/Courses/cs372/spring2012/slides/02_IntelligentAgents.pdf)
- ReAct rationale: chain-of-thought alone is “not grounded in the external world”; act-only approaches “do not reason abstractly about high-level goals or maintain a working memory.” ReAct combines both to enable dynamic planning and environment interaction. (Google Research blog: https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/)

### OODA framing for agent loops (conceptual mapping + security caveat)
- OODA phases: Observe, Orient, Decide, Act; “Orient is everything.” (ASDLC OODA page: https://asdlc.io/concepts/ooda-loop/)
- Security critique: applying OODA to agentic AI highlights integrity risks at each stage; notes Anthropic definition quoted: “Agents are models using tools in a loop.” (Schneier blog: https://www.schneier.com/blog/archives/2025/10/agentic-ais-ooda-loop-problem.html)
  - Also states prompt injection (attributed to Simon Willison, 2022) is architectural due to lack of privilege separation between instructions and data. (Same Schneier URL)

### Tool calling as a control boundary (why JSON schema + strictness)
- OpenAI function tools are defined by JSON schema; schema provides types/enums/required fields; example uses `additionalProperties: false` and `strict: true`, reflecting a design intent to constrain tool inputs. (OpenAI Function calling guide: https://platform.openai.com/docs/guides/function-calling)

### Human approval as an explicit safety gate (OpenAI Agents SDK)
- The SDK’s interruption mechanism is designed so approvals surface at the **outer run** even for nested `agent.asTool()` calls, enabling centralized governance of tool execution. (OpenAI Agents JS guide: https://openai.github.io/openai-agents-js/guides/human-in-the-loop/)
- Sticky approvals (`alwaysApprove`/`alwaysReject`) persist in run state and survive serialization, supporting long-lived workflows without keeping servers running. (Same source)

### Multi-agent orchestration rationale (AutoGen)
- AutoGen’s framework is positioned as simplifying orchestration/automation/optimization of complex workflows by automating chat among multiple agents, integrating tools and humans. (AutoGen 0.2 docs: https://microsoft.github.io/autogen/0.2/docs/Use-Cases/agent_chat/)
- The `UserProxyAgent` executing code blocks provides a concrete mechanism for tool/action execution mediated by a proxy that can solicit human input or auto-execute. (Same source)

---

## Common Questions & Answers

### Q1: What is the most defensible definition of an “agent” I can cite?
- An agent is anything that can be viewed as **perceiving its environment through sensors and acting upon that environment through effectors**. (Russell & Norvig, *AIMA* Ch. 2: https://people.eecs.berkeley.edu/~russell/aima1e/chapter02.pdf)

### Q2: What properties distinguish “intelligent agents” in the multi-agent systems literature?
- Wooldridge defines flexible autonomous action via **reactivity**, **pro-activeness**, and **social ability**. (Wooldridge MAS99: https://www.cs.ox.ac.uk/people/michael.wooldridge/pubs/mas99.pdf)
- Wooldridge & Jennings list **autonomy**, **social ability**, **responsiveness**, and **proactiveness**. (Software Agents PDF: http://www.cs.ox.ac.uk/people/michael.wooldridge/pubs/iee-review96.pdf)

### Q3: How does Russell & Norvig define autonomy?
- “A system is autonomous to the extent that its own behavior is determined by its own experience.” (Russell & Norvig Ch. 2 slides: https://cs.brynmawr.edu/Courses/cs372/spring2012/slides/02_IntelligentAgents.pdf)

### Q4: What is ReAct, precisely, and what did it improve?
- ReAct interleaves **verbal reasoning traces** and **actions**, where actions produce **observations** from an external environment that feed back into subsequent steps. (arXiv: https://arxiv.org/abs/2210.03629)
- Reported improvements: **+34%** absolute success on **ALFWorld** and **+10%** on **WebShop** vs imitation/RL baselines trained with **~10^5** instances, using **one-shot/two-shot prompting**. (Google Research blog: https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/)

### Q5: What is the standard tool-calling loop when using OpenAI APIs?
- The OpenAI guide specifies a 5-step loop: request with tools → receive tool call → execute tool in your app → send tool output → receive final response (or more tool calls). (OpenAI Function calling guide: https://platform.openai.com/docs/guides/function-calling)

### Q6: How do I enforce human approval before a tool executes in OpenAI’s Agents SDK?
- Mark tools with `needsApproval`; when approval is required, the run pauses and returns `interruptions`. Approve/reject via `result.state.approve(...)` / `result.state.reject(...)`, then resume with `runner.run(agent, state)`. (OpenAI Agents JS guide: https://openai.github.io/openai-agents-js/guides/human-in-the-loop/)

### Q7: How can an agent run be paused and resumed later (e.g., after a human approves)?
- Serialize run state with `result.state.toString()` and resume with `RunState.fromString(agent, serializedState)` (or `fromStringWithContext` with `contextStrategy: 'merge'|'replace'`). (OpenAI Agents JS guide: https://openai.github.io/openai-agents-js/guides/human-in-the-loop/)

### Q8: What makes AutoGPT “dangerous” in continuous mode, according to its docs?
- Continuous mode runs “without user authorization, 100% automated,” is “NOT recommended,” and “may cause your AI to run forever or carry out actions you would not usually authorize.” (AutoGPT docs: https://docs.agpt.co/classic/usage/)

### Q9: Where does AutoGPT store agent state and what file access boundaries exist?
- State: `data/agents`. Workspace: `data/agents/<agent_id>/workspace`. Access outside workspace requires `RESTRICT_TO_WORKSPACE=False`, which is not recommended unless sandboxed (Docker/VM). (AutoGPT docs: https://docs.agpt.co/classic/usage/)

### Q10: How does AutoGen implement multi-agent autonomy with tool/code execution?
- In the two-agent pattern, `AssistantAgent` can write Python code blocks; `UserProxyAgent` can execute code automatically when it detects an executable code block and no human input is provided, then returns results back into the conversation loop. (AutoGen 0.2 docs: https://microsoft.github.io/autogen/0.2/docs/Use-Cases/agent_chat/)

### Q11: What are concrete numeric defaults for exponential backoff in one published agent reliability example?
- Example config: initial delay **1000ms**, max delay **60000ms**, max retries **5**, multiplier **2**, jitter factor **0.3**. (Athenic blog: https://getathenic.com/blog/ai-agent-retry-strategies-exponential-backoff)

### Q12: What are example parameters for a vector-store “long-term memory” tool?
- Example config includes `topK: 20`, `qdrantCollection: "ltm"`, `useReranker: true`. (DEV tutorial: https://dev.to/einarcesar/long-term-memory-for-llms-using-vector-store-a-practical-approach-with-n8n-and-qdrant-2ha7)

---

### Notes on discrepancies / evidence strength
- Some sources are **primary/academic** (AIMA PDF; Wooldridge PDFs; ReAct arXiv) while others are **vendor docs** (OpenAI, AutoGPT, LangChain, AutoGen) or **practitioner blogs** (DEV tutorial, Athenic, ASDLC). Where numeric claims come from practitioner blogs (e.g., “60–80% token reduction,” “200–500ms latency”), treat them as **claims** rather than peer-reviewed findings.