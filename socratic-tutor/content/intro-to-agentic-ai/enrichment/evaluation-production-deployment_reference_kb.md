## Core Definitions

**Agent evaluation** — A family of methods for measuring how well an LLM-powered agent achieves goals and behaves over multi-step interactions, including metrics for task success, tool-use quality, reliability, safety, and operational properties like latency and cost. The agent-eval taxonomy in *LLM Agent Evaluation Metrics & Benchmark Construction* organizes evaluation along two axes: **objectives** (behavior/capabilities/reliability/safety) and **process** (interaction mode, data, metrics computation, tooling, contexts). (https://arxiv.org/html/2507.21504v1)

**Task completion rate (success rate / SR)** — A task-level metric that assigns a **binary reward {0,1}** for whether the agent achieved the goal, aggregated across tasks as a **Success Rate (SR)** (also called Task Success Rate / Overall Success Rate / Pass Rate). The same source distinguishes multi-trial variants like **pass@k** (succeeds at least once in *k* attempts) and stricter “succeeds every time” variants for mission-critical reliability. (https://arxiv.org/html/2507.21504v1)

**Trajectory analysis** — Evaluation that inspects the *sequence* of agent steps (e.g., tool calls, plan structure, intermediate decisions) rather than only the final answer. In the agent-eval survey, trajectory metrics include step/plan alignment measures such as **Node F1** (tool set), **Edge F1** / **Normalized Edit Distance** (tool sequence/graph structure), and stepwise “next tool” alignment; these aim to diagnose *how* the agent solved (or failed) the task. (https://arxiv.org/html/2507.21504v1)

**LLM-as-judge** — Using an LLM to score, label, or compare model/agent outputs when rule-based metrics are insufficient (e.g., summarization quality, “snappy” style). OpenAI’s eval workflow example uses a **label_model** grader (e.g., model `"o3-mini"`) that outputs labels like `correct/incorrect` based on a rubric prompt; the summarization eval notebook similarly motivates LLM-based evaluation for open-ended quality dimensions. (https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring, https://cookbook.openai.com/examples/evaluation/how_to_eval_abstractive_summarization)

**Observability (for deployed agents)** — The practice of logging and structuring runtime data (inputs, outputs, metadata, traces) so you can later slice, analyze, and evaluate behavior, detect regressions, and debug failures. In OpenAI’s “completion monitoring” workflow, setting `store=True` logs completions for later evaluation, and attaching **metadata** (e.g., `prompt_version`, `usecase`) enables segmentation and regression comparisons across versions. (https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring)

**Cost optimization (agent loop)** — Managing and reducing the cost of running an agent, commonly proxied by **#input tokens + #output tokens** (usage-based pricing proxy) and by avoiding unnecessary tool calls or repeated work. The agent-eval survey explicitly lists cost as estimated from token counts; speculative execution papers highlight a cost/latency trade-off where more speculation (e.g., larger top-*k*) increases cost. (https://arxiv.org/html/2507.21504v1, https://arxiv.org/html/2510.04371v1)

**Latency management (agent loop)** — Measuring and reducing end-to-end time in multi-step agent systems, including model inference time and tool/API time. The agent-eval survey defines **TTFT (Time To First Token)** and **End-to-End Request Latency**; speculation papers propose parallelizing predicted next actions to overlap tool latency and reduce wall-clock time, with measured end-to-end reductions under certain loads. (https://arxiv.org/html/2507.21504v1, https://arxiv.org/html/2510.04371v1, https://arxiv.org/html/2511-20048v1)

---

## Key Formulas & Empirical Results

### pass@k (functional correctness; unbiased estimator)
From Chen et al. (HumanEval/Codex), for each problem generate **n ≥ k** samples, with **c** correct (unit-test passing) samples. The unbiased estimator is:  
\[
\text{pass@}k = \mathbb{E}_{\text{problems}}\left[1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}\right]
\]
- **n**: number of generated samples per task  
- **c**: number of correct samples among the n  
- **k**: “budget” (best-of-k)  
Supports: measuring “succeeds at least once in k tries” without biased shortcuts. (https://arxiv.org/pdf/2107.03374.pdf)

**Numerically stable computation** (same source):  
- If \(n-c<k\): return 1.0  
- Else: \(1 - \prod_{i=n-c+1}^{n}\left(1-\frac{k}{i}\right)\) (https://arxiv.org/pdf/2107.03374.pdf)

### Agent latency metrics (definitions)
- **TTFT** = time until first streamed token  
- **End-to-End Request Latency** = time until complete response (noted as more relevant for async agents)  
Supports: what to measure when optimizing production agent responsiveness. (https://arxiv.org/html/2507.21504v1)

### Speculative Actions: expected runtime ratio (predict–verify)
From *Speculative Actions*, with:
- **L** = mean latency of actual API call  
- **l** = mean latency of speculative model (with \(l < L\))  
- **p** = probability the speculated next call matches the true next call (per step)  

Expected runtime ratio:
\[
\frac{\mathbb{E}[T_{\text{spec}}]}{\mathbb{E}[T_{\text{seq}}]}=\frac{1}{2-p}\left(1+\frac{l}{L}\right)
\]
Supports: why speculation has an upper bound on speedup in the simple setting and depends on p and l/L. (https://arxiv.org/html/2510.04371v1)

**Empirical claims (same paper):**
- Next-action prediction accuracy **up to 55%**; **up to 20% end-to-end lossless speedup**. (https://arxiv.org/html/2510.04371v1)

### SPAgent (speculation + scheduling) end-to-end latency results
- Directly sampled speculative actions match the post-reasoning action **73.4% at step 1**, dropping to **~11%** in later steps.  
- Serving results: **24.2% mean latency reduction on avg, up to 69.6%** vs naive & “Speculative Actions”; under load > **2 rps**, “Speculative Actions” can be **up to 49.3% slower than naive**.  
- Tool latency in setup: Wikipedia API **~1.5 s/request**.  
Supports: speculation must be load-aware/scheduled; naive speculation can hurt latency under concurrency. (https://arxiv.org/html/2511-20048v1)

### LLM-as-judge position bias metrics (pairwise/list-wise)
From *Measuring Position Bias in LLM-as-a-Judge*:

**Repetition Stability (RS)** (reliability under repeats):
\[
RS=\frac{1}{N}\sum_{i=1}^{N}\frac{\max_{c\in C}\text{count}_i(c)}{T}
\]
- **N**: number of queries  
- **T**: repeats per query  
- **C**: choice set (e.g., {A,B} or {A,B,tie}) (https://arxiv.org/abs/2406.07791)

**Position Consistency (PC)**:
\[
PC=\frac{\#\text{consistent series}}{\#\text{valid series}}
\]
(https://arxiv.org/abs/2406.07791)

**Preference Fairness (PF)**: min–max scaled score centered at 0; sign indicates primacy vs recency bias; extended list-wise via “one-vs-all”. (https://arxiv.org/abs/2406.07791)

**Defaults used in that study:**
- Judge temperature **= 1**
- RS computed with **3 repeats**
- Pairwise protocol uses original prompt (A then B) and swapped prompt (B then A) as a **judgment pair** (https://arxiv.org/abs/2406.07791)

### Chatbot Arena Elo (pairwise human preference)
From LMSYS Arena blog:

**Expected win probability**:
\[
E_A = \frac{1}{1 + 10^{(R_B - R_A)/400}}
\]

**Rating update**:
\[
R'_A = R_A + K(S_A - E_A)
\]
- **S_A**: actual score (win=1, tie=0.5, loss=0)  
Supports: how pairwise preference votes become a global ranking. (https://www.lmsys.org/blog/2023-05-03-arena/)

### OpenAI Evals API: stored completions + metadata slicing (implementation defaults)
- Log production completions by setting `store=True` on `client.chat.completions.create(...)`.
- Segment by `metadata` such as `{"prompt_version":"v1","usecase":"..."}`.
- LLM grader example: `"type":"label_model"`, model `"o3-mini"`, labels `["correct","incorrect"]`, passing `["correct"]`.  
Supports: regression detection across prompt/model versions using stored traffic. (https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring)

---

## How It Works

### A. Production-ish evaluation loop with stored completions (OpenAI Evals API pattern)
1. **Instrument the app to log completions**
   - In the completion call, set `store=True` so requests/responses are saved for later evaluation.
   - Attach **metadata** for slicing (use-case, prompt version, model version).
   - Source pattern: OpenAI “completion monitoring” cookbook. (https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring)

2. **Define an Eval (configuration)**
   - Create an **Eval** object that specifies:
     - `data_source_config` (e.g., stored completions filtered by metadata)
     - `testing_criteria` (grader definition, labels, rubric prompt)

3. **Run the Eval (execution)**
   - Create a **Run** over a slice of stored completions (e.g., only `prompt_version=v1`).
   - Repeat for `prompt_version=v2` to compare regression.

4. **Optionally: re-run new models on old inputs**
   - Use stored `item.input` messages as the input to generate new completions with a different model, then grade them with the same criteria.

5. **Inspect report + iterate**
   - Use run reports to identify regressions, then update prompts/models and repeat.

**Key variables exposed to graders** (stored completions):
- `{{item.input}}` = messages sent to the completion call  
- `{{sample.output_text}}` = assistant response text (https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring)

---

### B. Trajectory analysis workflow (agent-focused)
Use when final success rate is insufficient to debug.

1. **Log the full agent trajectory**
   - Capture each step: model message, tool call name/args, tool result, and timestamps.
   - (The agent-eval survey frames trajectory metrics around tool sequences/graphs and step success.) (https://arxiv.org/html/2507.21504v1)

2. **Choose a trajectory metric aligned to the failure mode**
   - Tool selection correctness → **Tool Selection Accuracy**
   - Tool sequence correctness → **Node F1 / Edge F1 / Normalized Edit Distance**
   - Stepwise correctness → “next tool” alignment / step success rate (https://arxiv.org/html/2507.21504v1)

3. **Compute metrics**
   - Against a reference trajectory (offline benchmark) or against expected step constraints (code-based assertions), or via LLM-as-judge for qualitative steps.

4. **Slice by metadata**
   - Prompt version, model version, tool latency bucket, etc. (mirrors stored-completions slicing idea). (https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring)

---

### C. LLM-as-judge: reduce bias with swapped-order protocol (pairwise)
When comparing two candidate outputs A and B:

1. Create **two prompts** for the judge:
   - Original order: show A then B
   - Swapped order: show B then A
2. Collect the **judgment pair** and measure:
   - **PC**: does the same candidate win across permutations?
   - **PF**: does the judge systematically prefer first vs later positions?
3. Optionally add a **tie** option (three-option mode). (https://arxiv.org/abs/2406.07791)

---

### D. Latency management via speculative tool execution (predict–verify)
(From *Speculative Actions* and SPAgent)

1. **While waiting** for the current tool/API response at step *t*, run a **speculator** model to predict likely next tool calls for step *t+1*.
2. **Pre-launch** predicted tool calls asynchronously; store futures in a cache keyed by “API call specifier”.
3. When the agent reaches step *t+1*:
   - If the predicted call matches, **await** the already-running future (overlap achieved).
   - If not, execute the correct call normally (and discard/ignore speculative result).
4. Keep it **lossless** by:
   - semantic guards (actor validates equivalence before commit)
   - restricting speculation to idempotent/reversible/sandboxed actions
   - repair/rollback paths (https://arxiv.org/html/2510.04371v1)

SPAgent adds:
- **Two-phase** speculation (aggressive then verified) and **scheduling** so speculation doesn’t increase inference latency under load. (https://arxiv.org/html/2511-20048v1)

---

## Teaching Approaches

### Intuitive (no math): “Three dashboards”
- **Did it work?** → task completion / success rate.
- **How did it work?** → trajectory analysis (what tools, what order, where it went wrong).
- **Can we ship it?** → observability + latency + cost (log everything, measure TTFT/E2E, watch token/tool spend).
Ground with: stored completions + metadata slicing for regressions (OpenAI cookbook). (https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring)

### Technical (with math): “Best-of-k + judge reliability + overlap speedup”
- Reliability: **pass@k** (unbiased estimator) for “succeeds at least once” (HumanEval). (https://arxiv.org/pdf/2107.03374.pdf)
- Judge reliability/bias: **RS/PC/PF** with swapped-order prompts. (https://arxiv.org/abs/2406.07791)
- Latency overlap: speculative execution runtime ratio depends on **p** and **l/L**. (https://arxiv.org/html/2510.04371v1)

### Analogy-based: “Factory QA + black box flight recorder”
- **Success rate** is like “did the product pass final inspection?”
- **Trajectory analysis** is like “inspect the assembly line steps to find the defect station.”
- **Observability** is the “flight recorder”: without logs/metadata, you can’t reproduce regressions.
- **Speculation** is “pre-staging parts while the previous station is still working,” but only safe if parts are reversible/unused unless confirmed. (https://arxiv.org/html/2510.04371v1)

---

## Common Misconceptions

1. **“If success rate is high, the agent is good—no need to look at trajectories.”**  
   - Why wrong: SR is a *final outcome* metric; it can hide brittle behavior (e.g., succeeds but uses wrong tools, or succeeds only with lucky tool ordering).  
   - Correct model: Use **trajectory analysis** (Node/Edge F1, edit distance, step success) to diagnose *how* the agent behaves and where it fails. (https://arxiv.org/html/2507.21504v1)

2. **“LLM-as-judge is basically objective, so one judge score is enough.”**  
   - Why wrong: Judges can have systematic **position bias** (primacy/recency) and varying consistency; the position-bias paper defines protocols (swap order, permutations) and metrics (PC/PF/RS) precisely because single-order judgments can be biased.  
   - Correct model: Use **swapped-order** (pairwise) or **permutations** (list-wise) and track **PC/PF/RS** to quantify bias and reliability. (https://arxiv.org/abs/2406.07791)

3. **“pass@k is just ‘1 − (1 − pass@1)^k’.”**  
   - Why wrong: Chen et al. explicitly warn that estimating pass@k from pass@1 via \(1-(1-\hat p)^k\) is **biased**; they provide an **unbiased estimator** requiring n samples and c correct.  
   - Correct model: Compute pass@k using \(1 - \binom{n-c}{k}/\binom{n}{k}\) with **n ≥ k** samples. (https://arxiv.org/pdf/2107.03374.pdf)

4. **“Observability is just printing logs; it doesn’t affect evaluation.”**  
   - Why wrong: The OpenAI eval workflow depends on **stored completions** and **metadata** to slice by use-case/version and run regression evals; without structured logging, you can’t reproduce or compare runs.  
   - Correct model: Treat logging (`store=True`) + metadata as the *data source* for offline evals and regression detection. (https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring)

5. **“Speculation always reduces latency if it’s correct often enough.”**  
   - Why wrong: SPAgent reports that naive “Speculative Actions” can become **slower than naive** under load (e.g., >2 rps) due to inference overhead and scheduling effects.  
   - Correct model: Latency gains depend on **overlap vs overhead**; you need scheduling/load-awareness and constraints on speculative work. (https://arxiv.org/html/2511-20048v1)

---

## Worked Examples

### 1) Regression monitoring with stored completions + LLM grader (OpenAI Evals API pattern)

**Goal:** Compare prompt v1 vs v2 on real production traffic for a summarizer use-case.

**A. Log completions in production**
```python
from openai import OpenAI
client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,  # key: log for later eval
    metadata={"usecase": "push_notifications_summarizer", "prompt_version": "v1"},
    messages=[
        {"role": "system", "content": "Summarize push notifications concisely."},
        {"role": "user", "content": "Your package shipped. Track it in the app."},
    ],
)
```
Source: stored completions + metadata pattern. (https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring)

**B. Define an Eval over stored completions**
- Data source: stored completions filtered by `metadata.usecase`.
- Grader: label model with `correct/incorrect` based on “concise and snappy”.

Key config elements (as described in the cookbook):
- `data_source_config = {"type":"stored_completions","metadata":{"usecase":"push_notifications_summarizer"}}`
- Grader variables available:
  - `{{item.input}}` (messages)
  - `{{sample.output_text}}` (assistant output)
- Testing criteria: `"type":"label_model"`, model `"o3-mini"`, labels `["correct","incorrect"]`, passing `["correct"]`. (https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring)

**C. Run two slices to detect regression**
- Run for v1: filter `metadata={"prompt_version":"v1"}`
- Run for v2: filter `metadata={"prompt_version":"v2"}`
Compare pass rates across runs; investigate failures by inspecting stored samples.

**Tutor move mid-conversation:** If a student asks “how do I compare prompt versions on real traffic?”, point to: `store=True` + metadata slicing + two runs.

---

### 2) Computing pass@k from n samples and c correct (HumanEval-style)

**Scenario:** For one coding task, you generated **n=20** solutions; **c=3** pass unit tests. Compute pass@5.

Use the unbiased estimator:
\[
\text{pass@}5 = 1 - \frac{\binom{n-c}{5}}{\binom{n}{5}}
= 1 - \frac{\binom{17}{5}}{\binom{20}{5}}
\]
This is the probability that a random set of 5 samples contains at least one correct solution, given c correct among n. (https://arxiv.org/pdf/2107.03374.pdf)

**Tutor move:** Emphasize this is *not* derived from pass@1; it uses (n,c,k).

---

### 3) Pairwise LLM-as-judge with swapped order (bias check)

**Goal:** Compare two agent outputs A and B fairly.

**Procedure (from position-bias paper):**
1. Prompt judge with (A then B) → record winner (or tie).
2. Prompt judge with (B then A) → record winner (or tie).
3. If the winner flips frequently across swaps, **PC** will be low; if the judge tends to pick the first option, **PF** indicates primacy bias. (https://arxiv.org/abs/2406.07791)

**Tutor move:** When a student says “my judge says A wins but I don’t trust it,” recommend swapped-order evaluation and tracking PC/PF.

---

## Comparisons & Trade-offs

| Topic | Option A | Option B | Trade-off / When to choose |
|---|---|---|---|
| Outcome metric | **Success Rate (SR)** (binary goal achieved) | **Trajectory metrics** (Node/Edge F1, edit distance, step success) | SR is simple and product-aligned; trajectory metrics diagnose *why* failures happen and catch “looks successful but wrong process.” (https://arxiv.org/html/2507.21504v1) |
| Multi-trial reliability | **pass@k** (succeeds at least once) | “succeeds in all k attempts” (survey calls stricter variant) | pass@k measures best-of-k capability; stricter variant targets mission-critical consistency. (https://arxiv.org/html/2507.21504v1) |
| Evaluation method | **Code-based assertions/unit tests** | **LLM-as-judge** | Code-based is crisp when you can formalize correctness (e.g., unit tests); LLM-as-judge helps for subjective qualities but needs bias controls (swap order, PC/PF/RS). (https://arxiv.org/pdf/2107.03374.pdf, https://arxiv.org/abs/2406.07791, https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring) |
| Latency reduction | **Sequential ReAct-style loop** | **Speculation (predict–verify)** | Speculation can overlap tool latency but adds overhead and can hurt under load without scheduling; SPAgent shows load-aware scheduling matters. (https://arxiv.org/html/2510.04371v1, https://arxiv.org/html/2511-20048v1, https://arxiv.org/abs/2210.03629) |
| Preference ranking | **Elo from human pairwise votes** | **Single-score judge rating** | Elo scales via incremental pairwise comparisons; single-score ratings can be easier but may hide judge bias/variance. (https://www.lmsys.org/blog/2023-05-03-arena/, https://arxiv.org/abs/2406.07791) |

---

## Prerequisite Connections

- **Tool-using agent loops (ReAct)** — Needed to understand what a “trajectory” is (reason → act → observe) and why tool latency dominates wall-clock time. (https://arxiv.org/abs/2210.03629)
- **Basic evaluation concepts (datasets, metrics, regressions)** — Needed to understand why you log production data and run repeated evals to detect prompt/model regressions. (https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring, https://eugeneyan.com/writing/llm-patterns/)
- **Sampling / multiple attempts** — Needed to interpret pass@k and why n≥k sampling is used. (https://arxiv.org/pdf/2107.03374.pdf)
- **Concurrency/overlap intuition** — Needed to reason about speculative execution benefits vs overhead under load. (https://arxiv.org/html/2510.04371v1, https://arxiv.org/html/2511-20048v1)

---

## Socratic Question Bank

1. **“If your agent’s success rate stayed constant but users complain more, what other metrics would you inspect first—and why?”**  
   *Good answer:* trajectory/tool-use metrics, latency (TTFT/E2E), cost; SR can hide regressions in style, tool misuse, or responsiveness. (https://arxiv.org/html/2507.21504v1)

2. **“What’s a concrete example where final-answer grading would miss a serious agent bug that trajectory analysis would catch?”**  
   *Good answer:* agent reaches correct answer but calls wrong tool or leaks sensitive tool calls; trajectory metrics (tool selection accuracy, sequence edit distance) reveal it. (https://arxiv.org/html/2507.21504v1)

3. **“How would you test whether your LLM judge is biased toward the first option?”**  
   *Good answer:* swapped-order pairwise prompts; compute PF/PC; include tie option if appropriate. (https://arxiv.org/abs/2406.07791)

4. **“Why does pass@k require n samples and c correct, instead of only pass@1?”**  
   *Good answer:* pass@k-from-pass@1 shortcut is biased; unbiased estimator uses combinatorics over n,c,k. (https://arxiv.org/pdf/2107.03374.pdf)

5. **“What metadata would you attach to production completions to make regression debugging easier later?”**  
   *Good answer:* prompt_version, usecase, model version; enables slicing stored completions into eval runs. (https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring)

6. **“Speculation sounds great—what conditions must hold for it to be ‘lossless’?”**  
   *Good answer:* actor validates equivalence; speculative calls are idempotent/reversible/sandboxed; repair/rollback exists. (https://arxiv.org/html/2510.04371v1)

7. **“Why might speculation make latency worse under high request load?”**  
   *Good answer:* inference overhead and scheduling contention; SPAgent reports naive speculation can be slower than naive under load (>2 rps). (https://arxiv.org/html/2511-20048v1)

8. **“If you had to pick one latency metric for a streaming chatbot vs an async agent, what would you pick?”**  
   *Good answer:* streaming chatbot: TTFT matters; async agent: end-to-end request latency matters more. (https://arxiv.org/html/2507.21504v1)

---

## Likely Student Questions

**Q: How do I set up evaluation on real production traffic and detect prompt regressions?**  
→ **A:** Log completions with `store=True` and attach metadata like `{"usecase": "...", "prompt_version": "v1"}`. Create an **Eval** whose `data_source_config` is `{"type":"stored_completions","metadata":{"usecase":"..."}}`, define `testing_criteria` with an LLM grader (example: `"type":"label_model"`, model `"o3-mini"`, labels `["correct","incorrect"]`), then create separate **Runs** filtered by `prompt_version` to compare v1 vs v2. (https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring)

**Q: What variables can the OpenAI grader prompt reference when grading stored completions?**  
→ **A:** The cookbook states graders can access `{{item.input}}` (the messages sent to the completion call) and `{{sample.output_text}}` (assistant response text). (https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring)

**Q: What’s the correct formula for pass@k?**  
→ **A:** Chen et al. define an unbiased estimator: \(\text{pass@}k = 1 - \binom{n-c}{k}/\binom{n}{k}\), where **n** is samples generated, **c** is number correct, **k** is the budget. (https://arxiv.org/pdf/2107.03374.pdf)

**Q: Why is “pass@k = 1 − (1 − pass@1)^k” not correct?**  
→ **A:** Chen et al. explicitly warn that estimating pass@k from empirical pass@1 via \(1-(1-\hat p)^k\) is **biased**; they provide the unbiased estimator requiring n and c. (https://arxiv.org/pdf/2107.03374.pdf)

**Q: How do I measure whether my LLM judge is biased by answer position?**  
→ **A:** Use the paper’s protocol: for each comparison, ask the judge twice—original order (A then B) and swapped order (B then A)—forming a **judgment pair**; then compute metrics like **PC** (consistency across permutations) and **PF** (primacy vs recency bias), and **RS** via repeated identical queries. (https://arxiv.org/abs/2406.07791)

**Q: What latency metrics should I track for agents?**  
→ **A:** The agent-eval survey defines **TTFT** (time to first token) and **End-to-End Request Latency** (time until complete response), noting end-to-end is often more relevant for async agents. (https://arxiv.org/html/2507.21504v1)

**Q: What’s the core idea behind speculative actions for faster agents, and what speedups are reported?**  
→ **A:** Run a cheap **speculator** in parallel to predict next tool/API calls and pre-launch them; when the agent needs the call, reuse the already-running future if it matches, with actor verification for losslessness. The paper reports next-action prediction accuracy up to **55%** and up to **20% end-to-end lossless speedup**. (https://arxiv.org/html/2510.04371v1)

**Q: Why can naive speculation be slower in production serving?**  
→ **A:** SPAgent reports that under load (> **2 rps**), “Speculative Actions” can be **up to 49.3% slower than naive**, motivating scheduling and phase-adaptive speculation. (https://arxiv.org/html/2511-20048v1)

---

## Available Resources

### Videos
- [State of GPT (Microsoft Build 2023)](https://youtube.com/watch?v=QNQHRjU3DoM) — Surface when: students ask “how do people *really* evaluate LLMs?” or want high-level evaluation philosophy and pitfalls.

### Articles & Tutorials
- [OpenAI Cookbook — Monitoring stored completions for regressions (Evals API)](https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring) — Surface when: “How do I evaluate prompts/models on production logs and catch regressions?”
- [OpenAI Cookbook — How to eval abstractive summarization](https://cookbook.openai.com/examples/evaluation/how_to_eval_abstractive_summarization) — Surface when: “ROUGE vs LLM-as-judge—what should I use for summarization?”
- [Eugene Yan — Patterns for Building LLM-based Systems & Products](https://eugeneyan.com/writing/llm-patterns/) — Surface when: students need a production framing tying evals to cost/latency/guardrails.
- [ReAct paper](https://arxiv.org/abs/2210.03629) — Surface when: students need the canonical “reason→act→observe” loop to understand trajectories and tool latency.
- [LangGraph docs](https://langchain-ai.github.io/langgraph/) — Surface when: students ask about orchestrating long-running/stateful agents with durable execution and tracing hooks.
- [LangGraph (GitHub)](https://github.com/langchain-ai/langgraph) — Surface when: students want implementation entry points for orchestration + deployment ecosystem (LangSmith).
- [Microsoft AutoGen (GitHub)](https://github.com/microsoft/autogen) — Surface when: students ask about multi-agent orchestration patterns and tool execution setups.

---

## Visual Aids

![G-Eval uses CoT and token probabilities for reference-free LLM evaluation.](/api/wiki-images/evaluation-benchmarks/images/eugeneyan-writing-llm-patterns_006.webp)  
Show when: a student asks “what does LLM-as-judge look like in practice for open-ended tasks like summarization?”

![Qwen model card showing author-reported evaluation results on Hugging Face Hub.](/api/wiki-images/evaluation-benchmarks/images/huggingface-co-docs-evaluate-index_001.png)  
Show when: a student asks “how do I interpret model card eval numbers vs leaderboards?” (author-reported vs community evaluation framing). (https://huggingface.co/docs/evaluate/index)

---

## Key Sources

- [LLM Agent Evaluation Metrics & Benchmark Construction](https://arxiv.org/html/2507.21504v1) — Core taxonomy + concrete agent metrics (success, tool-use, trajectory, latency, cost).
- [OpenAI Cookbook — Monitoring stored completions for regressions (Evals API)](https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring) — Practical production-style eval loop: stored completions, metadata slicing, LLM grader, regression runs.
- [Unbiased pass@k for code functional correctness (HumanEval/Codex)](https://arxiv.org/pdf/2107.03374.pdf) — Primary-source pass@k definition + unbiased estimator and stable computation.
- [Measuring Position Bias in LLM-as-a-Judge](https://arxiv.org/abs/2406.07791) — Operational protocol + metrics (RS/PC/PF) for judge reliability and position bias.
- [SPAgent — Speculation to Reduce Search-Agent Latency](https://arxiv.org/html/2511-20048v1) — End-to-end latency results and the key warning that naive speculation can hurt under load.