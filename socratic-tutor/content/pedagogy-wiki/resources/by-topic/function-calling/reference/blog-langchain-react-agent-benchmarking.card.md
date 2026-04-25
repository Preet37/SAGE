# Card: ReAct Agent Benchmarking (LangChain Email Assistant)
**Source:** https://blog.langchain.com/react-agent-benchmarking/  
**Role:** benchmark | **Need:** DEPLOYMENT_CASE  
**Anchor:** Methodology + results on how adding domains/tools/context affects single ReAct agent performance (tool trajectories + rubric-judged outputs)

## Key Content
- **Core question:** When does a *single* ReAct agent become overloaded as domains (instructions+tools) are added, causing performance drop?
- **Definitions:**  
  - *Domain* = conceptual responsibility bundle = **instructions + tools** (e.g., Calendar Scheduling, Customer Support).  
  - *Trajectory* = ordered sequence of tool calls.
- **Evaluation metric (Eq. 1: Pass rate):**  
  \[
  \text{PassRate}=\frac{\#\text{passed runs}}{90}
  \]
  where **90 runs** = 30 tasks × 3 stochastic repeats. Scores reported as “passing tests / 90”.
- **Pass condition:** task **passes iff** (1) tool-calling trajectory matches expected (correct tools + order; “nothing more, nothing less”) **and** (2) final email (via `send_email`) satisfies an **LLM-as-judge rubric** (boolean checks like `valid_email`, `more_deployments`).
- **Task sets / defaults:**  
  - Calendar Scheduling: 30 tasks; tools `get_cal`, `schedule_cal` (+ `send_email`); avg expected trajectory **1.4** tool calls.  
  - Customer Support: 30 tasks; **7 tools** (`get_org_info`, `get_customer_info`, `set_seats`, `set_deployments`, `apply_grant`, `get_billing_id`, `get_customer_invoices` + `send_email`); avg expected trajectory **2.7** tool calls.
- **Experimental procedure:** control agents have only their domain; then **append** additional generated domains’ instructions to the **system prompt** and **bind** their tools; same instructions/tool descriptions across models (not optimized per model). Stop testing a model when pass rate **<10%**.
- **Models benchmarked:** claude-3.5-sonnet, gpt-4o, o1, o3-mini, llama-3.3-70B.
- **Key results (1-domain controls):**
  - Calendar Scheduling: **o1 71%**, **o3-mini 68%** best; **gpt-4o** and **llama-3.3-70B** worst; llama-3.3-70B **0%** (failed to call `send_email` even with only scheduling domain).
  - Customer Support: **claude-3.5-sonnet 83%**, **o3-mini 83%**, **o1 77%**; llama-3.3-70B **21%**.
- **Scaling domains/context:** more domains/tools → worse instruction recall (“Lost in the Middle” expectation). Examples: Calendar Scheduling **gpt-4o drops to 2% at 7 domains**; **o3-mini drops sharply** with irrelevant domains; **o1 more stable**; claude-3.5-sonnet initially lower on scheduling but **more stable** as domains increase.
- **Trajectory-length effect:** longer trajectories degrade faster. For Customer Support, grouped as **<3 vs ≥3** tool calls; sample sizes **17 tasks (51 runs)** short vs **13 tasks (39 runs)** long; all top models show steeper decline for **≥3** when moving from 1 domain → 7 domains.
- **Overall conclusions:** (1) more context + more tools degrade performance, (2) longer trajectories degrade more quickly, (3) **o1/o3-mini/claude-3.5-sonnet** outperform **gpt-4o/llama-3.3-70B**, (4) **o3-mini** matches top models at small context but drops more as context grows.

## When to surface
Use when students ask how to *benchmark* ReAct/tool-using agents, how to score tool trajectories + final outputs, or what happens to agent reliability as you add more tools/domains/context in production-like setups.