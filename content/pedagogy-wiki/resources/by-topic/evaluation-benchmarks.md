# Evaluation Benchmarks

## Video (best)
- **Andrej Karpathy** — "State of GPT" (Microsoft Build 2023)
- youtube_id: bZQun8Y4L2A
- Why: Karpathy dedicates a substantial segment to how LLMs are evaluated, covering benchmark design philosophy, contamination risks, and the limitations of static benchmarks — directly relevant to this topic and highly accessible.
- Level: beginner/intermediate

---

## Blog / Written explainer (best)
- **Eugene Yan** — "Patterns for Building LLM-based Systems & Products"
- url: https://eugeneyan.com/writing/llm-patterns/
- Why: Widely cited in the ML community, covers evaluation patterns including LLM-as-judge, human eval, and benchmark contamination with concrete examples and practical framing. Bridges research and production concerns.
- Level: intermediate

**Supplementary:**
- **Chip Huyen** — "Open Challenges in LLM Research" (evaluation section)
- url: https://huyenchip.com/2023/08/16/llm-research-open-challenges.html
- Why: Covers hallucination measurement, benchmark limitations, and production evaluation challenges from a practitioner perspective.
- Level: intermediate

---

## Deep dive
- **EleutherAI** — Open LLM Leaderboard documentation + evaluation harness docs
- url: https://github.com/EleutherAI/lm-evaluation-harness
- Why: The `lm-evaluation-harness` repository is the de facto standard implementation for running MMLU, HellaSwag, HumanEval, and dozens of other benchmarks. Its README and task implementations serve as the most comprehensive technical reference for *how* benchmarks actually work in practice — covering prompt formatting, few-shot setup, metric computation, and contamination concerns.
- Level: advanced

---

## Original paper
- **Hendrycks et al.** — "Measuring Massive Multitask Language Understanding" (MMLU, 2020)
- url: https://arxiv.org/abs/2009.03300
- Why: MMLU is the single most referenced LLM benchmark and this paper established the paradigm of broad, multi-domain academic evaluation. It is readable, well-structured, and directly motivates discussions of contamination, task diversity, and benchmark saturation that define the field. HumanEval (Chen et al., 2021, arxiv 2107.03374) is the complementary seminal paper for code evaluation.
- Level: intermediate

**Honorable mention:**
- **Zheng et al.** — "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (2023)
- url: https://arxiv.org/abs/2306.05685
- Why: Foundational paper for the LLM-as-judge paradigm and Chatbot Arena (LMSYS), directly covering two of the related concepts in this topic.
- Level: intermediate/advanced

---

## Code walkthrough
- **EleutherAI** — `lm-evaluation-harness` — running MMLU and HumanEval end-to-end
- url: https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks
- Why: Walking through actual task implementations (e.g., `mmlu/`, `humaneval/`) shows learners exactly how prompts are constructed, how metrics are computed, and where contamination can enter — far more instructive than any tutorial video. Pairs naturally with the deep dive above.
- Level: advanced

**Supplementary notebook-style walkthrough:**
- **Hugging Face** — "Evaluate" library documentation with worked examples
- url: https://huggingface.co/docs/evaluate/index
- Why: More beginner-friendly entry point with runnable code for common metrics (accuracy, BLEU, ROUGE, exact match) before tackling full benchmark harnesses.
- Level: beginner/intermediate

---

## Coverage notes
- **Strong:** Static benchmark evaluation (MMLU, HumanEval), LLM-as-judge / Chatbot Arena, contamination concerns, VQA evaluation — all have solid papers and written resources
- **Weak:** Agent evaluation and trajectory analysis — emerging area with limited consolidated pedagogical resources; most material is in recent papers (GAIA, AgentBench, τ-bench) rather than polished explainers
- **Weak:** Observability and task completion rate in production settings — covered in MLOps literature but rarely connected explicitly to benchmark framing
- **Gap:** No single high-quality YouTube video cleanly covers the *full* evaluation benchmarks landscape (static + arena + agent + multimodal) in one explainer. Most videos focus on a single benchmark or paper.
- **Gap:** VQA evaluation specifically (as distinct from general multimodal) lacks a strong standalone explainer video outside of original paper presentations.

---

## Cross-validation
This topic appears in **3 courses**: `intro-to-agentic-ai`, `intro-to-llms`, `intro-to-multimodal`

| Concept | intro-to-llms | intro-to-agentic-ai | intro-to-multimodal |
|---|---|---|---|
| MMLU / HumanEval | ✅ Core | ➖ Reference | ➖ Reference |
| Chatbot Arena / LLM-as-judge | ✅ Core | ✅ Relevant | ➖ Peripheral |
| Agent eval / trajectory analysis | ➖ Peripheral | ✅ Core | ➖ Peripheral |
| VQA evaluation | ➖ Not covered | ➖ Peripheral | ✅ Core |
| Contamination | ✅ Core | ✅ Relevant | ✅ Relevant |
| Observability / task completion | ➖ Peripheral | ✅ Core | ➖ Peripheral |

---


> **[Structural note]** "Streaming, Debugging, and Observability in LangGraph" appears to have sub-concepts:
> agent streaming, intermediate state inspection, graph debugging, execution tracing
> *Discovered during enrichment for course "A hands-on intermediate course for software developers and AI/ML engineers cover" | 2026-04-10*


> **[Structural note]** "Real-World Agent Use Cases and Production Patterns" appears to have sub-concepts:
> production agent deployment, research assistant agent, code generation agent, error handling and retries, agent reliability and evals
> *Discovered during enrichment for course "A hands-on intermediate course for software developers and AI/ML engineers cover" | 2026-04-10*


> **[Structural note]** "Capstone: Designing and Building a Production-Ready Agent" appears to have sub-concepts:
> end-to-end agent design, langgraph orchestration, retrieval-augmented generation, structured tool calling, human-in-the-loop checkpointing, observability and tracing, agent evaluation
> *Discovered during enrichment for course "A hands-on intermediate course for software developers and AI/ML engineers cover" | 2026-04-10*


> **[Structural note]** "Framework Selection Criteria: Choosing the Right Tool for the Job" appears to have sub-concepts:
> framework selection, use case requirements, task complexity, human oversight, observability and evals
> *Discovered during enrichment for course "A hands-on intermediate course for software developers and AI/ML engineers cover" | 2026-04-10*

## Last Verified
2025-01-01 (knowledge cutoff basis; all URLs marked should be confirmed before publishing)