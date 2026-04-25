## Core Definitions

**Benchmarks** — Standardized evaluation datasets + protocols used to measure model performance on specific tasks (e.g., multiple-choice knowledge, code generation). A benchmark score is only meaningful *relative to its exact evaluation protocol* (prompt format, few-shot count, decoding settings, answer extraction), because implementations can differ materially (see EleutherAI lm-eval harness interface docs; and Eugene Yan’s note that even MMLU prompts/logic vary across implementations). Sources: EleutherAI lm-evaluation-harness docs; Eugene Yan.

**MMLU** — A multiple-choice benchmark intended to measure “massive multitask language understanding” across many subjects; commonly evaluated in 0-shot or few-shot (e.g., 5-shot) settings with constrained answers (A/B/C/D). MMLU is widely used but vulnerable to **contamination** (training-data overlap or deliberate inclusion), which can inflate scores and distort rankings. Source: MMLU-CF paper (ACL 2025).

**HumanEval** — A code-generation benchmark where models write Python functions to satisfy unit tests; evaluation is based on *functional correctness* (tests passing), not text similarity. Performance is typically reported as **pass@k** (probability at least one of k samples passes). Source: Chen et al. 2021 (arXiv:2107.03374).

**LLM-as-judge** — Using a strong LLM to evaluate other models’ outputs (often pairwise) on open-ended tasks where automatic metrics are weak. Zheng et al. report that strong judges (e.g., GPT-4) can reach **>80% agreement** with human preferences, comparable to human–human agreement, but judges exhibit biases (position, verbosity, self-enhancement) that require mitigation. Source: Zheng et al. 2023/2024 (arXiv:2306.05685).

**Chatbot Arena** — A crowdsourced evaluation platform where users compare two anonymous models side-by-side and vote; results are aggregated into an **Elo** leaderboard. Only votes where model identities were hidden are used for analysis. Source: LMSYS Arena blog (2023-05-03).

**Red teaming** — Adversarial, stress, and boundary testing to elicit failures (safety, security, policy violations, hallucinations, etc.), often iterated across model checkpoints and mitigations. GPT-4’s system card describes iterative red teaming with **50+ external experts** across many risk domains, plus automated internal evals and monitoring. Source: GPT-4 System Card.

**Contamination** — Benchmark items (or near-duplicates) appearing in training data, causing memorization/regurgitation rather than generalization. MMLU-CF distinguishes **unintentional** overlap vs **deliberate** benchmark-in-training and proposes transformations + closed test sets to deter it. Source: MMLU-CF paper (ACL 2025).

---

## Key Formulas & Empirical Results

### HumanEval / functional correctness: unbiased **pass@k**
From Chen et al. (2021), for each problem: generate **n ≥ k** samples, run unit tests, let **c** be the number of correct samples. Unbiased estimator:
\[
\text{pass@}k = \mathbb{E}_{\text{problems}}\left[1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}\right]
\]
- **n**: number of generated samples per task  
- **c**: number of samples that pass tests  
- **k**: “best-of-k” budget  
Claim supported: pass@k should be computed with the unbiased estimator; naive transforms from pass@1 are biased. Source: arXiv:2107.03374.

**Stable computation** (same source): if \(n-c<k\), return 1.0; else compute via a product form to avoid numerical issues.

**HumanEval dataset size**: **164** Python tasks; avg **7.7** unit tests/task. Source: arXiv:2107.03374.

### Chatbot Arena: Elo update equations
Win probability (logistic base-10):
\[
E_A = \frac{1}{1 + 10^{(R_B - R_A)/400}}
\]
Rating update:
\[
R'_A = R_A + K(S_A - E_A)
\]
- \(R_A, R_B\): current Elo ratings  
- \(S_A\): actual outcome (win=1, tie=0.5, loss=0)  
- \(K\): update factor  
Claim supported: Arena aggregates pairwise votes into a single ordering incrementally. Source: LMSYS Arena blog.

### MMLU-CF: contamination-free evaluation and observed score drops
**MMLU-CF construction** (ACL 2025):
- **20,000** MCQs across **14 fields**, sourced from **200+ billion webpages**
- Split: **10k closed-source test** + **10k open-source validation** (to deter deliberate contamination while enabling transparency)

**Decontamination rules** (Sec. 3.2):
1) Rephrase question (LLM)  
2) Shuffle choices (special-case All/None of the above)  
3) For **50%** of items, replace one choice with **“None of the other choices”** (skip if last choice is All/None)

**Default eval settings** (Sec. 4 / Table 5–6):
- **0-shot and 5-shot**, **no CoT**
- Prompt forces: “Answer by replying A, B, C or D”
- Example decoding settings reported (varies by model): e.g., GPT-4o **T=0.7**, max tokens **2048**

**Empirical effect (5-shot test, Table 1)**: large drops vs original MMLU and rank reshuffles, e.g.
- OpenAI o1: **92.3 → 80.3** (−12.0)
- GPT-4o: **88.0 → 73.4** (−14.6)
- Qwen2-72B-instruct: **82.3 → 63.7** (−18.6), rank ↓7  
Claim supported: contamination can materially inflate MMLU scores and distort rankings. Source: ACL 2025 MMLU-CF.

**Contamination detection (“match rate”)** (Sec. 4.5): after applying rules, **97.5%** of models show **<1%** match; on MMLU-CF, **100%** of models **<0.2%** match. Source: ACL 2025 MMLU-CF.

### CMMLU (Chinese MMLU-style): construction + protocol + results
- **67 subjects**, 4-choice single-answer MCQ
- Total questions reported as **11,528** (text) / **11,582 test-set** (Table 1)
- Per-subject split: **5-question few-shot dev** + **>100-question test** (min 105 per subject)
- Data collection: **>80% from PDFs (OCR)** to reduce contamination; estimated **~2% label noise**
- Overlap check: ~**1%** overlaps with CEval/M3KE via exact-string match after normalization

**Evaluation protocol** (Sec. 4):
- Closed models: free generation + regex extract option
- Open models: next-token prediction over {A,B,C,D} using next-token logits (preferred)

**Main 5-shot results (Table 3)**:
- GPT-4 overall **70.95%** (with category breakdowns in paper)
- ChatGPT **55.51%**
- Baichuan2-13B **61.92%** (beats ChatGPT)

**Ablations**:
- CoT often doesn’t help (Table 4)
- Negation and “sub-options” significantly reduce accuracy; for sub-options, GPT-4 5-shot: **71.72 → 53.41** (~−18.3) (Table 6)  
Source: CMMLU paper (ACL Findings 2024).

### OpenAI Safety Evaluations Hub: named metrics + reported ranges
Categories (text-based): **Disallowed content**, **Jailbreaks**, **Hallucinations**, **Instruction hierarchy**.

Example autograder metrics:
- `not_unsafe`: output is not unsafe per policy
- `not_overrefuse`: model doesn’t refuse benign requests

Reported ranges (hub summary):
- Disallowed content refusal effectiveness near **0.99** for many models
- `not_overrefuse` top around **0.80** (others **0.65–0.79**)
- StrongReject robustness **0.23–0.85**
- SimpleQA accuracy **0.09–0.59**; hallucination rate **0.41–0.86**
- Instruction hierarchy: system-vs-user **0.50–0.85**, developer-vs-user **0.15–0.77**, system-vs-developer **0.55–0.93**  
Source: OpenAI Safety Evaluations Hub.

---

## How It Works

### A. Running standardized benchmarks (reproducible workflow)
1) **Pick a harness + task registry** (e.g., EleutherAI lm-eval harness).
2) **Specify the exact task(s)** (`--tasks ...`) and **few-shot count** (`--num_fewshot k`).
3) **Lock generation settings** for any generative tasks via `--gen_kwargs` (temperature/top_p/etc.).
4) **Control batching/device** (`--batch_size`, `--device`) and enable **logging** (`--log_samples`) for auditability.
5) **Save outputs** (`--output_path`) so you can diff runs across model/prompt versions.
Source: lm-eval harness interface docs.

### B. LLM-as-judge evaluation (pairwise, bias-aware)
A common robust pattern (from position-bias measurement protocols and LLM-judge literature):
1) For each prompt, produce candidate answers **A** and **B** (identities hidden).
2) Ask judge to choose winner (optionally allow **tie**).
3) **Swap order** (present B then A) and re-judge.
4) Aggregate: if winner flips systematically with order, you have **position bias**; if repeated identical queries vary, you have **stability** issues.
Source: “Measuring Position Bias in LLM-as-a-Judge” (arXiv:2406.07791).

### C. Chatbot Arena (crowdsourced preference → Elo)
1) User chats with two anonymous models side-by-side.
2) User votes; only **anonymous** votes (names hidden) are used.
3) Elo is updated incrementally using expected win probability and observed outcomes.
4) Sampling policy matters: non-uniform pairing can bias coverage; LMSYS notes switching toward uniform sampling for better coverage.
Source: LMSYS Arena blog.

### D. Contamination-free benchmark construction (MMLU-CF pipeline)
1) **Collect** MCQs at scale (2.7M extracted from 3000+ domains).
2) **Clean + normalize** (English-only, dedup, enforce ≥4 choices, normalize labels A/B/C/D).
3) **Sample difficulty** using LLM difficulty ratings (0–9) and target a distribution centered around ~6.
4) **Quality check** with multiple LLMs; filter unsafe content; detect redundancy.
5) **Apply decontamination transformations**: rephrase question, shuffle choices, sometimes inject “None of the other choices.”
6) **Split** into open validation and closed test to deter deliberate contamination.
Source: ACL 2025 MMLU-CF.

### E. Production regression monitoring with LLM judges (OpenAI Evals API pattern)
1) Log completions with `store=True` and attach **metadata** (prompt_version, usecase).
2) Define an **Eval** (data source slice + testing criteria).
3) Run the eval for v1 vs v2 slices; compare pass rates to detect regressions.
4) Optionally re-run stored inputs on a new model to isolate model vs prompt changes.
Source: OpenAI Cookbook “completion monitoring” eval use case.

---

## Teaching Approaches

### Intuitive (no math): “Four lenses”
- **Benchmarks**: quick, repeatable “unit tests” for capabilities.
- **LLM-as-judge**: scalable approximation of human taste for open-ended outputs.
- **Human eval**: gold standard when stakes are high or metrics are unclear.
- **Red teaming**: adversarial probing for rare but critical failures.
Ground with: Arena (human preference at scale), Safety Hub (safety categories), MMLU-CF (contamination risk).

### Technical (with math): “What is the random variable?”
- For code: pass@k is estimating \(P(\exists\ \text{a correct sample among k})\) using the unbiased combinatorial estimator (Chen et al.).
- For pairwise preference: Elo is a probabilistic model of win rates; LLM-as-judge bias can be measured by swapped-order consistency metrics (PC/PF/RS).
- For contamination: compare scores under transformations; measure “match rate” to detect regurgitation (MMLU-CF).

### Analogy-based: “Exam vs interview vs penetration test”
- **Benchmarks** = standardized exam (but can be leaked).
- **LLM-as-judge / Arena** = interview panel (subjective, needs calibration).
- **Human eval** = expert committee review.
- **Red teaming** = penetration testing / adversarial audit.

---

## Common Misconceptions

1) **“A benchmark score is a property of the model.”**  
Why wrong: scores depend on *protocol details* (prompt, few-shot, decoding, answer extraction, evaluation logic). Even MMLU implementations differ in prompts and logic (Eugene Yan; lm-eval harness emphasizes explicit config).  
Correct model: treat a score as **(model, dataset, protocol)**, not model alone.

2) **“High MMLU means strong reasoning; rankings are stable.”**  
Why wrong: MMLU can be contaminated; MMLU-CF shows large drops and rank reshuffles (e.g., GPT-4o 88.0→73.4; Qwen2-72B 82.3→63.7).  
Correct model: MMLU is informative but must be checked for **contamination** and compared under controlled settings.

3) **“LLM-as-judge is objective because it’s automated.”**  
Why wrong: judges exhibit systematic biases (e.g., **position bias**). The position-bias paper shows how to measure primacy/recency effects via swapped-order protocols and PF/PC metrics.  
Correct model: LLM-judge is a *measurement instrument* that needs calibration, bias checks, and sometimes order randomization.

4) **“Chatbot Arena Elo is just accuracy on a fixed test set.”**  
Why wrong: Arena is **crowdsourced pairwise preference** on in-the-wild prompts; Elo depends on matchups and sampling policy (LMSYS notes non-uniform pairing early on).  
Correct model: Elo is a **relative preference ranking** under a particular prompt distribution and pairing policy.

5) **“Red teaming is just running a jailbreak benchmark once.”**  
Why wrong: GPT-4 system card describes iterative red teaming with many external experts across domains, plus automated internal evals and monitoring—an ongoing process, not a one-off test.  
Correct model: red teaming is **iterative adversarial evaluation** integrated into deployment readiness.

---

## Worked Examples

### 1) Compute pass@k for a single HumanEval-style task (unbiased estimator)
Assume you generated **n=200** samples for one task and **c=30** passed unit tests. What is pass@10?

Use Chen et al. estimator:
\[
1 - \frac{\binom{n-c}{k}}{\binom{n}{k}} = 1 - \frac{\binom{170}{10}}{\binom{200}{10}}
\]

Python snippet (direct, using Python’s `math.comb`):
```python
import math

def pass_at_k(n, c, k):
    if n - c < k:
        return 1.0
    return 1 - (math.comb(n - c, k) / math.comb(n, k))

print(pass_at_k(200, 30, 10))
```
Tutor move: ask student to interpret the combinatorics: numerator = ways to pick k all-failing samples; denominator = all k-sample subsets.

Source: arXiv:2107.03374.

### 2) Minimal swapped-order check for LLM-judge position bias (pairwise)
For each prompt:
- Collect two candidate answers A and B.
- Judge once with order (A then B), once with swapped (B then A).
- If the judge picks “first” disproportionately, you have primacy bias.

Pseudo-protocol (from arXiv:2406.07791):
```text
for prompt in prompts:
  verdict1 = judge(prompt, A, B)   # order AB
  verdict2 = judge(prompt, B, A)   # order BA
  record(verdict1, verdict2)
analyze: how often winner changes under swap?
```
Tutor move: connect to PF/PC: “Do we get consistent winners (PC) and is there a systematic first/last preference (PF)?”

Source: arXiv:2406.07791.

### 3) Production regression eval using stored completions + LLM grader (OpenAI Cookbook pattern)
Key idea: log real traffic, then grade later.

Skeleton (conceptual, from the Cookbook):
- Store completions with metadata:
  - `metadata={"prompt_version":"v1","usecase":"push_notifications_summarizer"}`
- Create Eval with:
  - `data_source_config={"type":"stored_completions","metadata":{"usecase":"push_notifications_summarizer"}}`
  - LLM grader labels `correct/incorrect`
- Run twice filtering v1 vs v2 metadata; compare pass rates.

Source: OpenAI Cookbook “completion monitoring”.

---

## Comparisons & Trade-offs

| Method | What it measures well | Strengths | Failure modes / caveats | Choose when |
|---|---|---|---|---|
| Standard benchmarks (e.g., MMLU, CMMLU) | Specific skills on fixed datasets | Cheap, repeatable, comparable *if protocol fixed* | Contamination; protocol sensitivity; saturation | You need fast iteration + regression tracking |
| Code functional eval (HumanEval pass@k) | Executable correctness | Objective unit tests; avoids BLEU pitfalls | Test coverage limits; sampling variance | You evaluate code generation quality |
| LLM-as-judge (MT-Bench style) | Open-ended quality | Scalable; can match humans **>80%** agreement (Zheng et al.) | Bias (position/verbosity); judge limitations | You need scalable preference-like scoring |
| Chatbot Arena (Elo) | Real-user preference | In-the-wild prompts; large-scale human votes | Sampling/pairing effects; distribution shift | You want “how users like it” ranking |
| Red teaming + safety evals | Rare/high-impact failures | Finds boundary cases; deployment-focused | Not exhaustive; needs iteration | Safety/security readiness and monitoring |

Sources: Zheng et al. (LLM-as-judge), LMSYS Arena blog, MMLU-CF, CMMLU, HumanEval pass@k paper, GPT-4 system card, OpenAI Safety Evaluations Hub.

---

## Prerequisite Connections

- **Probability & sampling** — needed to interpret pass@k and why n≥k sampling reduces variance (Chen et al.).
- **Evaluation protocol control** — needed to understand why prompt/decoding differences break comparability (lm-eval harness; Eugene Yan).
- **Basic statistics of bias/reliability** — needed for judge stability and position bias concepts (RS/PC/PF in arXiv:2406.07791).
- **Security mindset / adversarial thinking** — needed to understand red teaming and jailbreak evaluation categories (GPT-4 system card; Safety Evaluations Hub).

---

## Socratic Question Bank

1) **If two papers report “MMLU 80%,” what would you check before concluding the models are equal?**  
Good answer: prompt format, few-shot count, CoT allowed, decoding params, answer extraction, dataset version, contamination controls.

2) **Why is pass@k not the same as “take pass@1 and compute \(1-(1-p)^k\)”?**  
Good answer: that transform is biased; Chen et al. give an unbiased combinatorial estimator using n samples and c correct.

3) **How could an LLM judge be “consistent” but still “unfair”?**  
Good answer: high position consistency (PC) can coexist with systematic primacy/recency bias (PF); swapped-order tests reveal it.

4) **What does Elo assume about comparisons, and what breaks if matchups aren’t sampled uniformly?**  
Good answer: Elo models win probabilities from ratings; biased pairing can skew rating estimates/uncertainty and coverage.

5) **What evidence would convince you a benchmark is contaminated?**  
Good answer: large score drops under decontamination transformations; high “match rate” to original choices; widening val–test gap over time (MMLU-CF).

6) **Why do safety evals include both `not_unsafe` and `not_overrefuse`?**  
Good answer: you need to measure both refusing harmful requests and not refusing benign ones; otherwise you can “game” safety by refusing everything.

7) **What’s the difference between red teaming and a static jailbreak benchmark?**  
Good answer: red teaming is iterative, adversarial, and broad (experts + new attacks); static benchmarks can saturate and miss new vectors.

---

## Likely Student Questions

**Q: How do I compute pass@10 if I generated 200 samples and 30 passed?**  
→ **A:** Use Chen et al.’s unbiased estimator: \(1 - \binom{n-c}{k}/\binom{n}{k}\). Here: \(1 - \binom{170}{10}/\binom{200}{10}\). Source: https://arxiv.org/pdf/2107.03374.pdf

**Q: Why did MMLU-CF create a closed test set?**  
→ **A:** To deter deliberate contamination (benchmark added to training). MMLU-CF uses **10k closed-source test** + **10k open-source validation** so evaluation remains meaningful while still enabling transparency. Source: https://aclanthology.org/2025.acl-long.656.pdf

**Q: What’s a concrete sign contamination is affecting rankings?**  
→ **A:** MMLU-CF reports large 5-shot drops and rank reshuffles vs MMLU, e.g., GPT-4o **88.0→73.4** (−14.6), Qwen2-72B **82.3→63.7** (−18.6). Source: https://aclanthology.org/2025.acl-long.656.pdf

**Q: How does Chatbot Arena turn votes into a leaderboard?**  
→ **A:** It uses Elo: expected win prob \(E_A = 1/(1+10^{(R_B-R_A)/400})\), then updates \(R'_A = R_A + K(S_A - E_A)\). Votes are from anonymous side-by-side comparisons; names revealed only after voting. Source: https://www.lmsys.org/blog/2023-05-03-arena/

**Q: Do LLM judges actually agree with humans?**  
→ **A:** Zheng et al. report strong LLM judges (e.g., GPT-4) can achieve **over 80% agreement** with human preferences—about the same as human–human agreement—while noting biases (position/verbosity/self-enhancement). Source: https://arxiv.org/abs/2306.05685

**Q: How do you test whether an LLM judge has position bias?**  
→ **A:** Use swapped-order evaluation: judge (A then B) and (B then A) as a paired test; compute consistency and fairness metrics (RS/PC/PF). Source: https://arxiv.org/abs/2406.07791

**Q: What safety metrics does OpenAI publicly report?**  
→ **A:** The Safety Evaluations Hub reports categories including disallowed content, jailbreaks, hallucinations, and instruction hierarchy; includes metrics like `not_unsafe` and `not_overrefuse`, plus benchmark ranges (e.g., SimpleQA accuracy **0.09–0.59**). Source: https://openai.com/safety/evaluations-hub/

**Q: How do I run standardized evals and log per-sample outputs?**  
→ **A:** In lm-eval harness, use `--tasks ...`, `--num_fewshot ...`, set `--output_path ...` and `--log_samples` to save per-document inputs/outputs/metrics; use `--show_config` to audit task settings. Source: https://github.com/EleutherAI/lm-evaluation-harness/blob/big-refactor/docs/interface.md

---

## Available Resources

### Videos
- [State of GPT (Microsoft Build 2023)](https://youtube.com/watch?v=QNQHRjU3DoM) — Surface when: student asks why benchmark scores aren’t directly comparable, or about contamination/limitations of static benchmarks.
- [Reinforcement Learning from Human Feedback (CS224N Guest Lecture)](https://youtube.com/watch?v=zjrM-MW-0y0) — Surface when: student asks how human preference signals relate to evaluation and alignment pipelines.
- [InstructGPT paper explained (Yannic Kilcher)](https://youtube.com/watch?v=VIARnQFSeHk) — Surface when: student asks how human preference evaluation connects to RLHF training and model selection.

### Articles & Tutorials
- [Patterns for Building LLM-based Systems & Products (Eugene Yan)](https://eugeneyan.com/writing/llm-patterns/) — Surface when: student is confused about evals in production, protocol drift, and why “leaderboard scores” can mislead.
- [lm-evaluation-harness (EleutherAI)](https://github.com/EleutherAI/lm-evaluation-harness) — Surface when: student wants a standard tool to run many benchmarks reproducibly.
- [lm-eval Harness Interface docs](https://github.com/EleutherAI/lm-evaluation-harness/blob/big-refactor/docs/interface.md) — Surface when: student asks “what exact CLI flags/settings do I need?”
- [OpenAI Cookbook: completion monitoring eval](https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring) — Surface when: student asks how to set up regression testing on real logged traffic.
- [OpenAI Safety Evaluations Hub](https://openai.com/safety/evaluations-hub/) — Surface when: student asks what safety dimensions are measured and what metrics are called.

---

## Visual Aids

![Same MMLU question, three different prompts across benchmark implementations.](/api/wiki-images/evaluation-benchmarks/images/eugeneyan-writing-llm-patterns_004.webp)  
Show when: student assumes “MMLU score” is comparable across leaderboards without checking prompt templates.

![Evaluation logic differs across MMLU implementations, not just prompts.](/api/wiki-images/evaluation-benchmarks/images/eugeneyan-writing-llm-patterns_005.webp)  
Show when: student accepts prompt differences but still assumes scoring/extraction logic is identical.

![G-Eval uses CoT and token probabilities for reference-free LLM evaluation.](/api/wiki-images/evaluation-benchmarks/images/eugeneyan-writing-llm-patterns_006.webp)  
Show when: introducing LLM-as-judge / reference-free evaluation and why it differs from ROUGE/BLEU-style metrics.

![Qwen model card showing author-reported evaluation results on Hugging Face Hub.](/api/wiki-images/evaluation-benchmarks/images/huggingface-co-docs-evaluate-index_001.png)  
Show when: student asks how to interpret model card benchmark claims vs independent/community evaluations.

---

## Key Sources

- [MMLU-CF (Contamination-free MMLU) — methodology + results](https://aclanthology.org/2025.acl-long.656.pdf) — Most direct source here on contamination detection/mitigation and how rankings change under decontamination.
- [Unbiased pass@k for code functional correctness (HumanEval/Codex)](https://arxiv.org/pdf/2107.03374.pdf) — Primary formula source for pass@k and why naive estimators are biased.
- [Chatbot Arena Elo Leaderboard methodology](https://www.lmsys.org/blog/2023-05-03-arena/) — Canonical description of Arena’s anonymous pairwise voting and Elo computation.
- [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) — Key claim that strong LLM judges can match human preferences at ~human agreement levels; documents judge biases.
- [OpenAI Safety Evaluations Hub](https://openai.com/safety/evaluations-hub/) — Concrete public safety eval categories, metric names, and reported performance ranges.