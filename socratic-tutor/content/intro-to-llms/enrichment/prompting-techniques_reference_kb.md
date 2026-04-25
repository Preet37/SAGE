## Core Definitions

**Zero-shot prompting (0S).** Brown et al. (GPT‑3) define *zero-shot* as providing a **task description/instruction only** with **K = 0 demonstrations** (no example input→output pairs) and **no gradient updates** to model weights. Source: “Language Models are Few‑Shot Learners” (NeurIPS 2020), Section 2 “Approach” and definitions of 0S/1S/FS. https://proceedings.neurips.cc/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf

**One-shot prompting (1S).** Brown et al. define *one-shot* as few-shot prompting with **exactly one** demonstration (**K = 1**) included in the prompt, again with **no gradient updates**. Same source as above.

**Few-shot prompting (FS).** Brown et al. define *few-shot* as providing **K demonstrations** (context→completion pairs) in the prompt, with **no gradient updates**; typical **K ≈ 10–100**, limited by the model’s **context window** (GPT‑3 used **nctx = 2048 tokens**). Same source as above.

**In-context learning (ICL).** In the GPT‑3 evaluation framing, ICL is the phenomenon where a model’s behavior on a task changes when you include demonstrations in the prompt (0S→1S→FS), despite **no weight updates**. Brown et al. operationalize it via the evaluation protocol that conditions on randomly sampled demonstrations per test example. https://proceedings.neurips.cc/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf  
Related empirical ablations show demonstrations often help by specifying **format, label space, and input distribution**, not necessarily by providing correct labels. https://arxiv.org/abs/2202.12837

**Chain-of-thought (CoT) prompting.** Wei et al. define chain-of-thought prompting as eliciting a **series of intermediate reasoning steps** (a “chain of thought”) before the final answer, typically by including a few exemplars that show reasoning steps in the prompt; they report this improves performance on multi-step reasoning tasks and emerges strongly at large model scale. https://arxiv.org/abs/2201.11903 and Google Research blog summary: https://research.google/blog/language-models-perform-reasoning-via-chain-of-thought/

**Self-consistency (SC) decoding (for CoT).** Wang et al. define self-consistency as replacing greedy decoding with: **sample multiple diverse CoT reasoning paths**, then **aggregate** (e.g., majority vote) over the final answers, effectively “marginalizing out” the reasoning paths. https://arxiv.org/abs/2203.11171

**System prompts / developer instructions (API meaning).** In the OpenAI Responses API, `instructions: string` is defined as “**A system (or developer) message inserted into the model’s context**.” In the Responses API, when using `previous_response_id`, **instructions are not carried over** to the next response (you can swap system/developer guidance per turn). https://platform.openai.com/docs/api-reference/responses-streaming/response/in_progress?lang=curl  
In the Chat Completions API, messages can include `"developer"` and `"system"` roles; developer instructions are the intended mechanism for o1+ models, and instruction hierarchy places developer/system above user instructions. https://platform.openai.com/docs/api-reference/chat and https://platform.openai.com/docs/api-reference/responses/list?lang=python

**Structured output (schema-constrained decoding / Structured Outputs).** OpenAI defines **Structured Outputs** as an API feature designed to ensure outputs **exactly match developer-supplied JSON Schemas**, enabled via `strict: true` (function calling) or `response_format` / `text.format` with `type: "json_schema"` and `strict: true`. Mechanistically, it uses **constrained decoding** by converting JSON Schema to a **CFG** and **masking invalid next tokens** at each step. https://openai.com/index/introducing-structured-outputs-in-the-api/ and https://platform.openai.com/docs/guides/structured-outputs/

**JSON mode (contrast).** OpenAI defines JSON mode as improving the chance the model emits **valid JSON**, but it **does not guarantee conformance to a specific schema**. In some APIs, JSON mode requires that “JSON” appears in context; otherwise the API errors, and if not instructed properly the model may stream whitespace. https://platform.openai.com/docs/guides/structured-outputs/ and https://platform.openai.com/docs/guides/text-generation/json-mode


## Key Formulas & Empirical Results

### GPT‑3 0S/1S/FS definitions + benchmark deltas (Brown et al., 2020)
- **Definitions:** 0S: K=0; 1S: K=1; FS: K demonstrations; no gradient updates; GPT‑3 context window **nctx=2048** tokens.  
  Source: https://proceedings.neurips.cc/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf
- **Example benchmark gains (illustrative):**
  - **CoQA (F1):** 0S **81.5**, 1S **84.0**, FS **85.0**
  - **TriviaQA (acc):** 0S **64.3**, 1S **68.0**, FS **71.2**
  - **LAMBADA (acc):** 0S **76.2**, FS **86.4**
  - **SuperGLUE (FS, 32 examples):** Avg **69.0** (with task variation; e.g., WiC **49.4** near chance)
  Source: same paper tables (3.1–3.5).

### ICL objective framing + “labels often don’t matter” (Min et al., 2022)
For classification/multi-choice tasks, Min et al. write prediction as:
\[
\hat y=\arg\max_{y\in C} P(y\mid x)
\]
and k-shot as:
\[
\hat y=\arg\max_{y\in C} P(y\mid x_1,y_1,\ldots,x_k,y_k,x)
\]
Random-label ablation:
\[
\hat y=\arg\max_{y\in C} P(y\mid x_1,\tilde y_1,\ldots,x_k,\tilde y_k,x)
\]
Key empirical claim: replacing gold labels with random labels causes only a **marginal** drop on many classification/multi-choice tasks; demonstrations help mainly by specifying **label space**, **input distribution**, and **format**. https://arxiv.org/abs/2202.12837

### Self-consistency (Wang et al., 2022/ICLR 2023): objective + defaults + gains
- **Majority-vote aggregation objective:**
\[
a^*=\arg\max_{a\in\mathcal{A}}\sum_{i=1}^{m}\mathbf{1}(a_i=a)
\]
where each sample yields a reasoning path \(r_i\) and final answer \(a_i\). https://arxiv.org/abs/2203.11171
- **Sampling defaults reported:** typically **40 samples** per run; results averaged over **10 runs**; GPT‑3 used **temperature T=0.7** (no top‑k). https://arxiv.org/abs/2203.11171
- **Reported gains (GPT‑3 code-davinci-002):**
  - GSM8K **60.1 → 78.0 (+17.9)**
  - SVAMP **75.8 → 86.8 (+11.0)**
  - AQuA **39.8 → 52.0 (+12.2)**
  - StrategyQA **73.4 → 79.8 (+6.4)**
  - ARC‑c **83.6 → 87.5 (+3.9)**
  Source: http://arxiv.org/pdf/2203.11171v4.pdf

### Tree of Thoughts (ToT) vs CoT (Yao et al., 2023): empirical comparison + key params
- **Game of 24 (100 hard games):** IO **7.3%**, CoT **4.0%**, CoT‑SC (k=100) **9.0%**, ToT BFS **b=1: 45%**, **b=5: 74%**. Temperature **0.7**; ToT used **3 thought steps**; evaluator labels sure/maybe/impossible. https://arxiv.org/abs/2305.10601 and PDF: https://arxiv.org/pdf/2305.10601.pdf

### Structured Outputs reliability (OpenAI)
- On complex schema-following evals: `gpt-4o-2024-08-06` + Structured Outputs reported **100%**, while `gpt-4-0613` reported **<40%**. Claim supports: constrained decoding + schema enforcement can dominate “prompt-only” formatting reliability. https://openai.com/index/introducing-structured-outputs-in-the-api/

### Nucleus (top‑p) sampling definition (Holtzman et al., 2019)
Define smallest set \(V^{(p)}\) such that:
\[
\sum_{x\in V^{(p)}} P(x\mid x_{1:i-1}) \ge p
\]
Renormalize and sample from truncated distribution \(P'\) (invalid tokens get probability 0). Supports: how decoding parameters (top‑p/temperature) affect output variability and thus prompt reliability. https://arxiv.org/abs/1904-09751


## How It Works

### A. Zero-shot vs few-shot prompting (mechanics + evaluation protocol)
(From Brown et al. GPT‑3 evaluation procedure)
1. **Choose K** (0, 1, or few-shot K).  
2. For each evaluation example:
   - **Randomly draw K demonstrations** from the task training set (or dev set if no training set exists, e.g., LAMBADA/StoryCloze).
   - Format as **context→completion pairs** with task-specific delimiters (often 1–2 newlines).
3. Append the **test input** after the demonstrations.
4. Decode the completion (GPT‑3 paper reports **beam search** with **beam width 4** and **length penalty α=0.6** for free-form completion tasks).
5. Score against the gold answer.

Why tutors care mid-conversation: when a student says “few-shot didn’t help,” check (i) demo sampling quality, (ii) formatting consistency, (iii) context window truncation, (iv) decoding strategy.  
Source: https://proceedings.neurips.cc/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf

### B. Chain-of-thought prompting → self-consistency decoding
1. **Prompt for reasoning**: include CoT exemplars (few-shot) or an instruction that elicits intermediate steps (the DAIR/OpenAI cookbook examples commonly use “Let’s think step by step,” but the formal SC method assumes you already have CoT-style outputs to sample).  
2. **Sample m outputs** (not greedy): each output contains a reasoning path \(r_i\) and final answer \(a_i\).  
3. **Aggregate answers**: choose the most frequent \(a_i\) (majority vote), i.e., marginalize out \(r_i\).  
4. Return the selected answer (optionally also return one representative rationale, but SC’s selection is based on answer agreement).  
Source: https://arxiv.org/abs/2203.11171

### C. Tree of Thoughts (ToT): deliberate search over “thoughts”
(From Yao et al.)
1. **Define “thought” granularity** (e.g., one equation line for Game of 24).  
2. **Generate multiple candidate thoughts** from current state \(s\).  
3. **Evaluate states** using:
   - **Value** prompt (score/labels like sure/maybe/impossible), or
   - **Vote** among candidates.
4. **Search**:
   - **BFS**: keep top‑b states per depth (beam-like).
   - **DFS**: expand best state; prune below threshold; backtrack.
5. Continue until solution found or step budget exhausted.  
Source: https://arxiv.org/abs/2305.10601

### D. System/developer instructions across turns (Responses API)
Key operational rule (often missed in multi-turn tutoring apps):
1. Send a response with `instructions: "...system/developer guidance..."`.
2. On the next turn, if you use `previous_response_id`, **the prior instructions are not carried over**; you must resend or replace them explicitly.  
Also: `truncation: "auto"` may drop earlier conversation items to fit context window; `"disabled"` fails with 400 if too long.  
Source: https://platform.openai.com/docs/api-reference/responses-streaming/response/in_progress?lang=curl

### E. Structured Outputs (schema-constrained decoding)
1. Developer supplies a **JSON Schema** and sets **strict: true** (via function calling or `response_format` / `text.format` with `type:"json_schema"`).  
2. System converts schema → **CFG**.
3. During generation, after **every token**, compute valid next tokens from CFG and **mask invalid tokens** (probability 0).  
4. Output is guaranteed to match schema unless interrupted (refusal, truncation via `max_tokens`, etc.).  
Sources: https://openai.com/index/introducing-structured-outputs-in-the-api/ and https://platform.openai.com/docs/guides/structured-outputs/


## Teaching Approaches

### Intuitive (no math): “Prompt = temporary task spec”
- Zero-shot: you only *tell* the model what you want.
- Few-shot: you *show* the model what you want (format + examples).
- CoT: you *ask it to show its work* so it allocates more tokens to intermediate steps.
- Self-consistency: you *ask multiple times* and trust the answer that repeats most.
Grounding: Brown et al. show 0S→FS improves many benchmarks; Wang et al. show sampling+vote boosts reasoning accuracy.

### Technical (with math): “Conditioning changes \(P(\text{output} \mid \text{context})\)”
- Few-shot changes the conditional distribution by adding \((x_i,y_i)\) pairs into the context: \(P(y \mid x_1,y_1,\dots,x_k,y_k,x)\) (Min et al.).  
- Self-consistency approximates marginalization over latent rationales \(r\) by sampling \((r_i,a_i)\) and selecting \(a\) maximizing \(\sum \mathbf{1}(a_i=a)\) (Wang et al.).  
- Structured Outputs changes decoding by constraining the support of next-token distribution via CFG masking (OpenAI Structured Outputs).

### Analogy-based: “Teaching by examples vs grading by consensus”
- Few-shot is like giving a student 10 solved problems before a quiz: they infer the pattern.
- CoT is like requiring scratch work: reduces “lucky guess” errors.
- Self-consistency is like asking 40 students independently and taking the majority answer.
- Structured Outputs is like forcing answers onto a standardized form: you can’t write outside the boxes (structure guaranteed; correctness not guaranteed).


## Common Misconceptions

1. **“Few-shot prompting is basically fine-tuning.”**  
   - Why wrong: Brown et al. explicitly define few-shot as **no gradient updates**; it’s purely conditioning within the context window.  
   - Correct model: few-shot is *inference-time conditioning*; fine-tuning changes weights. (Brown et al., Section 2)  
   Source: https://proceedings.neurips.cc/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf

2. **“If my demonstrations have wrong labels, few-shot will fail.”**  
   - Why wrong: Min et al. show replacing gold labels with **random labels** often causes only a **marginal** drop on classification/multi-choice tasks.  
   - Correct model: demonstrations often help by specifying **format**, **label space**, and **input distribution**; correctness of label mapping may be less central than students assume.  
   Source: https://arxiv.org/abs/2202.12837

3. **“Chain-of-thought guarantees correctness because the reasoning is explicit.”**  
   - Why wrong: CoT is a prompting method that can improve performance, but it’s still model-generated text; Wang et al. motivate SC because a single greedy CoT path can be wrong, and sampling multiple paths + voting improves accuracy.  
   - Correct model: CoT increases *chance* of correct reasoning; SC adds robustness by aggregating across diverse paths.  
   Source: https://arxiv.org/abs/2203.11171

4. **“JSON mode guarantees my schema.”**  
   - Why wrong: OpenAI docs state JSON mode ensures **valid JSON**, not adherence to a specific schema; Structured Outputs is the feature that enforces schema conformance.  
   - Correct model: use **Structured Outputs** (`json_schema`, `strict:true`) when you need type-safety (required keys, enums, etc.).  
   Sources: https://openai.com/index/introducing-structured-outputs-in-the-api/ and https://platform.openai.com/docs/guides/structured-outputs/

5. **“System prompts persist automatically across turns in the Responses API.”**  
   - Why wrong: Responses API explicitly says when using `previous_response_id`, **instructions are not carried over**.  
   - Correct model: treat system/developer instructions as *per-request* unless you re-inject them.  
   Source: https://platform.openai.com/docs/api-reference/responses-streaming/response/in_progress?lang=curl


## Worked Examples

### 1) Self-consistency for a reasoning question (minimal implementation sketch)
Goal: show the *procedure* (sample multiple CoT outputs → majority vote), matching Wang et al.

```python
from collections import Counter

def majority_vote(answers):
    return Counter(answers).most_common(1)[0][0]

# Pseudocode: you would replace `sample_model(prompt)` with your API call.
def self_consistency(prompt, m=40):
    samples = [sample_model(prompt, temperature=0.7) for _ in range(m)]  # Wang et al. use sampling, not greedy
    # Extract final answer a_i from each sample (task-specific parsing)
    answers = [extract_final_answer(s) for s in samples]
    return majority_vote(answers), samples
```

Tutor notes:
- Use **m ≈ 40** as the canonical default reported by Wang et al.  
- Emphasize that SC aggregates **final answers**, not “best-looking reasoning.”  
Source for method + defaults: https://arxiv.org/abs/2203.11171

### 2) Structured Outputs vs JSON mode (Responses API shape; schema constraints)
Goal: show how to *guarantee* schema adherence (Structured Outputs), and what constraints exist.

**Structured Outputs (schema enforced):** (conceptual REST shape)
```json
{
  "model": "gpt-4o-mini-2024-07-18",
  "input": "Return a JSON object with fields: answer (string), confidence (number).",
  "text": {
    "format": {
      "type": "json_schema",
      "strict": true,
      "schema": {
        "type": "object",
        "additionalProperties": false,
        "properties": {
          "answer": { "type": "string" },
          "confidence": { "type": "number" }
        },
        "required": ["answer", "confidence"]
      }
    }
  }
}
```

Key tutor-callouts (from OpenAI docs):
- Root schema **must be an object**; **all fields required** (emulate optional via union with `null`); must set `additionalProperties: false`; nesting ≤ **10**; total properties ≤ **5000**.  
Source: https://platform.openai.com/docs/guides/structured-outputs/

**JSON mode (valid JSON only):**
```json
{ "text": { "format": { "type": "json_object" } } }
```
But JSON mode does **not** guarantee schema conformance.  
Source: https://platform.openai.com/docs/guides/structured-outputs/


## Comparisons & Trade-offs

| Technique | What you change | Main benefit | Main cost / failure mode | When to choose | Sources |
|---|---|---|---|---|---|
| Zero-shot | Instruction only (K=0) | Cheapest tokens; simplest | Ambiguity; weaker task formatting | Simple tasks; strong instruction-following models | Brown et al. GPT‑3 |
| Few-shot | Add K demos in context | Better format adherence; higher accuracy on many tasks | Token cost; context limit; sensitive to formatting | When you can provide representative examples | Brown et al. GPT‑3 |
| CoT prompting | Ask for intermediate steps | Better multi-step reasoning | Single path can be wrong; verbosity | Math/logic/multi-step tasks | Wei et al. |
| Self-consistency | Decode multiple samples + vote | Large accuracy gains on reasoning | More compute (m samples) | High-stakes reasoning; when latency allows | Wang et al. |
| ToT | Search over multiple “thoughts” with evaluation | Big gains on search/planning tasks | More orchestration; evaluator prompts | Problems needing backtracking/search (e.g., Game of 24) | Yao et al. |
| JSON mode | Output valid JSON | Easier parsing than free text | No schema guarantee | Loose structure acceptable | OpenAI docs |
| Structured Outputs | Constrained decoding to JSON Schema | Schema adherence guarantee | Doesn’t ensure value correctness; can fail on refusal/truncation | When downstream code requires type-safety | OpenAI Structured Outputs docs |

(Primary sources: Brown et al. GPT‑3; Wang et al. SC; Yao et al. ToT; OpenAI Structured Outputs docs.)


## Prerequisite Connections

- **Next-token prediction & decoding basics.** Needed to understand why temperature/top‑p and constrained decoding affect outputs (Holtzman et al. nucleus sampling; OpenAI constrained decoding description).
- **Conditional probability / conditioning on context.** Needed to interpret ICL formulas \(P(y \mid x_1,y_1,\dots,x)\) (Min et al.).
- **Search concepts (BFS/DFS, pruning).** Needed to understand ToT as explicit search over intermediate states (Yao et al.).
- **API message roles & instruction precedence.** Needed to reason about system/developer prompts and why they may not persist across turns (OpenAI API references).


## Socratic Question Bank

1. **If you add 10 demonstrations and performance drops, what are two prompt-level reasons that could happen without blaming the model?**  
   Good answer: formatting mismatch, out-of-distribution demos, context window/truncation, decoding differences (Brown et al. protocol sensitivity; Min et al. distribution/format importance).

2. **In Min et al.’s random-label result, what does it suggest demonstrations are doing besides “teaching the mapping”?**  
   Good answer: specifying label space, format, and input distribution.

3. **Why might majority vote over 40 sampled CoT solutions beat picking the single most “confident-sounding” rationale?**  
   Good answer: SC marginalizes reasoning paths and uses agreement as robustness; single path can be a local optimum (Wang et al.).

4. **What problem does ToT solve that CoT doesn’t, according to the Game of 24 results?**  
   Good answer: need for branching search/backtracking; CoT is linear and can get stuck; ToT BFS b=5 reaches 74% vs CoT 4% (Yao et al.).

5. **What does Structured Outputs guarantee—and what does it explicitly not guarantee?**  
   Good answer: guarantees schema conformance; not correctness of values; can fail on refusal/truncation (OpenAI Structured Outputs).

6. **In the Responses API, if you rely on `previous_response_id`, what must you remember about `instructions`?**  
   Good answer: instructions are not carried over; must resend/replace (Responses streaming reference).

7. **How is JSON mode different from schema-constrained decoding in terms of guarantees?**  
   Good answer: JSON mode → valid JSON; Structured Outputs → schema adherence via constrained decoding (OpenAI docs).

8. **What’s the trade-off between self-consistency and latency/cost?**  
   Good answer: SC requires m samples (often 40), increasing compute and tokens (Wang et al.).


## Likely Student Questions

**Q: What exactly is “few-shot” vs “one-shot” vs “zero-shot”?**  
→ **A:** Brown et al. define: **zero-shot** = instruction only (**K=0** demos), **one-shot** = **K=1** demo, **few-shot** = **K demonstrations** (often **10–100**) in the prompt; **no gradient updates** in all cases. https://proceedings.neurips.cc/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf

**Q: How did GPT‑3 evaluate few-shot fairly?**  
→ **A:** For each test example, they **randomly draw K examples** from the task training set as demonstrations (or dev if no train set), use task-specific delimiters (often 1–2 newlines), and decode free-form completions with **beam width 4** and **length penalty α=0.6** (as reported). Same GPT‑3 paper.

**Q: Do I need correct labels in my few-shot examples?**  
→ **A:** Min et al. find that replacing gold labels with **random labels** often causes only a **marginal** drop on classification/multi-choice tasks; demonstrations help largely by specifying **label space**, **input distribution**, and **format**. https://arxiv.org/abs/2202.12837

**Q: What is self-consistency, precisely?**  
→ **A:** Wang et al.: sample **m** diverse CoT outputs \((r_i,a_i)\) and select the answer by **majority vote** \(a^*=\arg\max_a \sum_i \mathbf{1}(a_i=a)\). Typical setting: **40 samples**, averaged over **10 runs**; GPT‑3 used **T=0.7**. https://arxiv.org/abs/2203.11171

**Q: How big are the gains from self-consistency?**  
→ **A:** On GPT‑3 code-davinci-002, Wang et al. report: GSM8K **60.1→78.0 (+17.9)**, SVAMP **75.8→86.8 (+11.0)**, AQuA **39.8→52.0 (+12.2)**, StrategyQA **73.4→79.8 (+6.4)**, ARC‑c **83.6→87.5 (+3.9)**. http://arxiv.org/pdf/2203.11171v4.pdf

**Q: How is Tree of Thoughts different from Chain-of-Thought?**  
→ **A:** ToT (Yao et al.) explicitly does **search** over multiple candidate “thoughts” per step, using **value/vote** evaluation and **BFS/DFS with pruning/backtracking**; CoT is typically a single linear rationale. On Game of 24: CoT **4%** vs ToT BFS b=5 **74%**. https://arxiv.org/abs/2305.10601

**Q: Does JSON mode guarantee my output matches my schema?**  
→ **A:** No. OpenAI docs: JSON mode helps produce **valid JSON** but **does not guarantee** conformance to a specific schema; **Structured Outputs** enforces schema adherence with `strict:true` and constrained decoding. https://openai.com/index/introducing-structured-outputs-in-the-api/ and https://platform.openai.com/docs/guides/structured-outputs/

**Q: In the Responses API, do system instructions persist when I use `previous_response_id`?**  
→ **A:** No—OpenAI states **instructions from the previous response are not carried over** when using `previous_response_id`. https://platform.openai.com/docs/api-reference/responses-streaming/response/in_progress?lang=curl


## Available Resources

### Videos
- [Intro to Large Language Models](https://youtube.com/watch?v=zjkBMFhNj_g) — Surface when: student asks “why does prompting work at all?” or needs grounding in next-token prediction + decoding intuition.
- [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (Paper Explained)](https://youtube.com/watch?v=_YXnMBQjGDo) — Surface when: student wants mechanistic intuition for why intermediate steps help and what “emergent with scale” means.

### Articles & Tutorials
- [Prompt Engineering (Lilian Weng)](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/) — Surface when: student asks for a single written reference spanning zero/few-shot, CoT, self-consistency, ToT.
- [Prompt Engineering Guide (DAIR.AI)](https://www.promptingguide.ai/) — Surface when: student asks “what other prompting techniques exist?” beyond the lesson (catalog-style reference).
- [Language Models are Few-Shot Learners (GPT‑3)](https://proceedings.neurips.cc/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf) — Surface when: student asks for canonical definitions and benchmark evidence for 0S/1S/FS.
- [Self-Consistency Improves Chain of Thought Reasoning](https://arxiv.org/abs/2203.11171) — Surface when: student asks for the exact SC algorithm, formula, and default sampling settings.
- [Tree of Thoughts: Deliberate Problem Solving with LLMs](https://arxiv.org/abs/2305.10601) — Surface when: student asks how to implement branching reasoning/search beyond CoT.


## Visual Aids

![Tree of Thoughts explores branching reasoning paths vs. linear CoT. (Yao et al. 2022)](/api/wiki-images/chain-of-thought/images/lilianweng-posts-2023-03-15-prompt-engineering_002.png)  
Show when: student is stuck on “CoT vs ToT” and needs a visual of branching search vs linear reasoning.

![Number of examples needed: prompting vs. finetuning decision boundary. (Chip Huyen)](/api/wiki-images/system-prompts/images/huyenchip-2023-04-11-llm-engineering-html_004.png)  
Show when: student asks “should I fine-tune or just prompt?” and you want to anchor the data/effort trade-off discussion (prompting as low-data lever).


## Key Sources

- [Language Models are Few-Shot Learners (Brown et al., 2020)](https://proceedings.neurips.cc/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf) — Canonical definitions (0S/1S/FS) + evaluation protocol + benchmark deltas.
- [Demonstrations in ICL: labels often don’t matter (Min et al., 2022)](https://arxiv.org/abs/2202.12837) — Sharp empirical insight into *why* demonstrations help (format/label space/distribution).
- [Self-Consistency Improves Chain of Thought Reasoning (Wang et al., 2022/ICLR 2023)](https://arxiv.org/abs/2203.11171) — Exact SC procedure, formula, defaults, and large benchmark gains.
- [Tree of Thoughts (Yao et al., 2023)](https://arxiv.org/abs/2305.10601) — Concrete algorithm for deliberate search over thoughts + strong planning/search results.
- [Introducing Structured Outputs in the API (OpenAI)](https://openai.com/index/introducing-structured-outputs-in-the-api/) — Mechanism (CFG + token masking) and reliability claims for schema-constrained decoding.