# Curation Report: Agent Skills and Safety
**Topic:** `agent-skills-safety` | **Date:** 2026-04-09 16:13
**Library:** 5 existing → 18 sources (13 added, 9 downloaded)
**Candidates evaluated:** 44
**Reviewer verdict:** needs_additions

## Added (13)
- **[reference_doc]** [docs.anthropic.com](https://docs.anthropic.com/en/docs/claude-code/cli-reference.md)
  This is the most authoritative candidate for precise, citable API/SDK surface details and operational defaults for Claude Code in production workflows.
- **[benchmark]** [AgentDojo: A Dynamic Environment to Evaluate](https://proceedings.neurips.cc/paper_files/paper/2024/file/97091a5177d8dc64b1da8bf3e1f6fb54-Paper-Datasets_and_Benchmarks_Track.pdf)
  Provides quantitative, peer-reviewed measurements for prompt-injection robustness in tool-using agents, enabling the tutor to cite concrete success rates and trade-offs.
- **[paper]** [[PDF] CAPTURE: Context-Aware Prompt Injection Testing and Robustness ...](https://aclanthology.org/2025.llmsec-1.13.pdf)
  Adds a complementary evaluation framework focused on systematic testing, helping the tutor teach how to build and measure prompt-injection regression suites beyond a single benchmark.
- **[explainer]** [Production LLM Guardrails: NeMo, Guardrails AI, Llama Guard ...](https://blog.premai.io/production-llm-guardrails-nemo-guardrails-ai-llama-guard-compared/)
  While not primary research, it directly targets the requested framework comparison and can seed a feature matrix discussion (policy expression, placement in stack, and operational trade-offs).
- **[paper]** [Building a Generalizable Guardrail for Web Agents](https://arxiv.org/html/2507.14293v1)
  Gives a concrete, step-by-step blueprint for deploying guardrails in an agent loop with measurable outcomes, closer to real operational constraints than generic safety discussions.
- **[benchmark]** [AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents](https://arxiv.org/abs/2406.13352)
  The curator cited AgentDojo but didn’t pin the canonical arXiv landing page; this is the stable, citable reference for methodology, tables, and exact experimental setup.
- **[paper]** [CAPTURE: Context-Aware Prompt Injection Testing and Robustness Enhancement](https://aclanthology.org/anthology-files/pdf/llmsec/2025.llmsec-1.13.pdf)
  If the curator only kept an arXiv/PDF link, the ACL Anthology version is the authoritative camera-ready with stable pagination for quoting exact procedures and results.
- **[paper]** [Designing Multi-layered Runtime Guardrails for Foundation Model-based Web Agents](https://arxiv.org/html/2408.02205v3)
  This is the actual full paper behind the “web agents guardrail” idea and contains the step-by-step system design and evaluation details that an abstract/snippet would miss.
- **[reference_doc]** [Input validation and guardrails for agentic AI systems on AWS (Agentic AI Security Prescriptive Guidance)](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-security/best-practices-input-validation.html)
  Even if “thin,” this is operationally-oriented official guidance that helps fill the missing runnable defense-in-depth story (controls, placement, and failure modes) better than research papers alone.
- **[benchmark]** [AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents](https://arxiv.org/abs/2406.13352) *(promoted by reviewer)*
  The curator cited AgentDojo but didn’t pin the canonical arXiv landing page; this is the stable, citable reference for methodology, tables, and exact experimental setup.
- **[paper]** [CAPTURE: Context-Aware Prompt Injection Testing and Robustness Enhancement](https://aclanthology.org/anthology-files/pdf/llmsec/2025.llmsec-1.13.pdf) *(promoted by reviewer)*
  If the curator only kept an arXiv/PDF link, the ACL Anthology version is the authoritative camera-ready with stable pagination for quoting exact procedures and results.
- **[paper]** [Designing Multi-layered Runtime Guardrails for Foundation Model-based Web Agents](https://arxiv.org/html/2408.02205v3) *(promoted by reviewer)*
  This is the actual full paper behind the “web agents guardrail” idea and contains the step-by-step system design and evaluation details that an abstract/snippet would miss.
- **[reference_doc]** [Input validation and guardrails for agentic AI systems on AWS (Agentic AI Security Prescriptive Guidance)](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-security/best-practices-input-validation.html) *(promoted by reviewer)*
  Even if “thin,” this is operationally-oriented official guidance that helps fill the missing runnable defense-in-depth story (controls, placement, and failure modes) better than research papers alone.

## Near-Misses (4) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **4.3 Neural-Symbolic Approach...** — [4.3 Neural-Symbolic Approach...](https://arxiv.org/html/2402.01822v1)
  _Skipped because:_ Looks relevant but is an HTML section snippet without clear identification of the full paper and its definitive feature-matrix-style comparisons.
- **THINKGUARD: Deliberative Slow Thinking Leads to Cautious Gua** — [THINKGUARD: Deliberative Slow Thinking Leads to Cautious Guardrails](https://arxiv.org/pdf/2502.13458.pdf)
  _Skipped because:_ Strong guardrail modeling paper, but it doesn’t directly provide the requested cross-framework comparison matrix or agent/tooling integration focus.
- **4.1 Promptarmor Vs. Existing...** — [4.1 Promptarmor Vs. Existing...](https://arxiv.org/html/2507.15219v1)
  _Skipped because:_ Promising defense with empirical results, but the candidate is a partial HTML view; CAPTURE + AgentDojo better cover benchmark/testing needs with clearer evaluation framing.
- **Just-in-Time Model Routing for Scalable Serving of Agentic .** — [Just-in-Time Model Routing for Scalable Serving of Agentic ...](https://arxiv.org/pdf/2511.20975.pdf)
  _Skipped because:_ Likely excellent for cost/latency routing metrics, but the candidate set already needed a clearer safety-controls-in-agent-loop case; this is more LLMOps/routing than safety deployment.

## Reasoning
**Curator:** Selections prioritize (1) official docs for exact operational defaults and (2) peer-reviewed benchmarks/papers with measurable robustness and integration procedures. Where candidates were blog-level or partial snippets, they were used only when they uniquely addressed a missing comparison need.
**Reviewer:** The curator’s core picks are strong for prompt-injection benchmarking/testing and guardrail design, but they should add the canonical/stable versions of AgentDojo and CAPTURE plus at least one official, deployment-oriented architecture reference to better support end-to-end defense-in-depth teaching.
