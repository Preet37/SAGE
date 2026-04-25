# Curation Report: Tool Use and Function Calling in Agents
**Topic:** `mcp-tool-ecosystem` | **Date:** 2026-04-10 18:54
**Library:** 1 existing → 5 sources (4 added, 4 downloaded)
**Candidates evaluated:** 15
**Reviewer verdict:** good

## Added (4)
- **[paper]** [Toward a Theory of Agents as Tool-Use Decision-Makers - arXiv](https://arxiv.org/html/2506.00886v1)
  Adds a formal, decision-theoretic framing of tool use where tools/functions define the agent’s action set, including constraints and selection/routing considerations—material not covered by MCP’s protocol-level docs.
   — covers: Action space in tool-using agents: formal definition, how tools/functions constitute the action set, constraints and selection/routing policies
- **[paper]** [Schema First Tool APIs for LLM Agents: A Controlled Study of ... - arXiv](https://arxiv.org/html/2603.13404v1)
  Directly targets robust tool result handling via schema-first design, covering structured outputs, validation/parse reliability, and how schema choices affect downstream agent behavior—complementing MCP with evidence and methodology.
   — covers: Robust tool result handling: output schemas, validation, error handling, retries/timeouts, idempotency, tool-output parsing/normalization, and how results are incorporated into the plan-act-observe loop
- **[paper]** [Robust and Efficient Tool Orchestration via Layered Execution Structures with Reflective Correction](https://arxiv.org/pdf/2602.18968.pdf)
  Provides an end-to-end orchestration perspective for multi-tool execution, emphasizing failure modes, recovery/reflective correction, and organizing multiple calls—useful for designing plan→act→observe loops that remain stable under tool errors.
   — covers: Robust tool result handling: output schemas, validation, error handling, retries/timeouts, idempotency, tool-output parsing/normalization, and how results are incorporated into the plan-act-observe loop, End-to-end plan → act → observe loop examples showing multiple tool calls and iterative reasoning grounded on returned observations
- **[paper]** [Multi-Step Planning and Reasoning Improves Acting in LLM Agents](https://arxiv.org/html/2505.09970v2)
  Adds concrete multi-step agent-loop methodology (planning intertwined with acting) and empirical grounding for iterative plan→act→observe behavior across multiple steps, which MCP does not provide.
   — covers: End-to-end plan → act → observe loop examples showing multiple tool calls and iterative reasoning grounded on returned observations

## Near-Misses (11) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Unified Tool-Based Action Space** — [Unified Tool-Based Action Space](https://www.emergentmind.com/topics/unified-tool-based-action-space)
  _Skipped because:_ Potentially useful, but it’s a secondary topic page rather than a primary, citable technical source; the arXiv theory paper is a more authoritative anchor for the same gap.
- **Implementing Tool Calling Loop with Error Handling and Retry** — [Implementing Tool Calling Loop with Error Handling and Retry Logic](https://www.buzhou.io/en/articles/implementing-tool-calling-loop-with-error-handling-and-retry-logic)
  _Skipped because:_ Practical but blog-level and likely less stable/rigorous than the selected papers; kept out to avoid thin or implementation-specific guidance without broader principles.
- **Tool Use in LLM Agents: Patterns, Pitfalls, and Best Practic** — [Tool Use in LLM Agents: Patterns, Pitfalls, and Best Practices](https://www.agentengineering.io/topics/articles/tool-use-patterns)
  _Skipped because:_ Could be helpful, but as a non-peer-reviewed article it’s harder to assess authority and long-term stability versus the chosen research papers.
- **What Is the AI Agent Loop? The Core Architecture Behind ...** — [What Is the AI Agent Loop? The Core Architecture Behind ...](https://blogs.oracle.com/developers/what-is-the-ai-agent-loop-the-core-architecture-behind-autonomous-ai-systems)
  _Skipped because:_ Good conceptual overview, but likely too high-level for the requested end-to-end multi-tool, observation-grounded examples and robust handling details.
- **AI Agents in Action, Second Edition - 5 Agent Reasoning and ** — [AI Agents in Action, Second Edition - 5 Agent Reasoning and Planning](https://www.manning.com/preview/ai-agents-in-action-second-edition/chapter-5)
  _Skipped because:_ Promising, but it’s a preview/paywalled chapter rather than a fully accessible stable reference for a teaching wiki.
- **arXiv:2205.15953v4 [cs.LG] 4 Jun 2023** — [arXiv:2205.15953v4 [cs.LG] 4 Jun 2023](https://arxiv.org/pdf/2205.15953.pdf)
  _Skipped because:_ The candidate metadata/snippet appears mismatched (shows unrelated 'Unified Tool-Based Action Space' text), making it risky to include without clear relevance to tool-using agents’ action spaces.
- **[PDF] Dynamically Restricted Action Spaces for Multi-Agent R** — [[PDF] Dynamically Restricted Action Spaces for Multi-Agent Reinforcement ...](https://madoc.bib.uni-mannheim.de/67433/1/0762.pdf)
  _Skipped because:_ Relevant to action-space restriction in MARL, but not clearly focused on tool/function calling agents; would add conceptual distance without direct payoff for this lesson.
- **./sample_complexity.eps** — [./sample_complexity.eps](https://sites.usm.edu/banerjee/papers/ActDisc_ALA2010.pdf)
  _Skipped because:_ Appears to be an older/possibly misindexed file with unclear connection to tool-using agents and function calling.
- **Measuring Tool Use Correctness & Plan Adherence — AI ...** — [Measuring Tool Use Correctness & Plan Adherence — AI ...](https://rajatpandit.com/agentic-ai/tool-correctness/)
  _Skipped because:_ Focuses on evaluation/metrics rather than the core gaps (formal action space, robust result handling mechanics, and concrete multi-tool loops).
- **[PDF] arXiv:2404.11584v1 [cs.AI] 17 Apr 2024 - Rivista AI** — [[PDF] arXiv:2404.11584v1 [cs.AI] 17 Apr 2024 - Rivista AI](https://www.rivista.ai/wp-content/uploads/2024/06/2404.11584v1.pdf)
  _Skipped because:_ Insufficiently identified from the candidate list (generic title/venue mirror); hard to verify it substantively covers the specific plan→act→observe/tool-calling gaps.
- **AI Paper Reading: Agentic Reasoning Implementation Guide 202** — [AI Paper Reading: Agentic Reasoning Implementation Guide 2026](https://www.youngju.dev/blog/ai-papers/2026-03-04-ai-papers-agentic-reasoning-implementation-guide-2026.en)
  _Skipped because:_ A tertiary reading-note style resource; useful for discovery but not a primary, authoritative reference for the library.

## Reasoning
**Curator:** The existing MCP repo covers protocol/interface mechanics but not the theory of tool actions, robust execution semantics, or empirically grounded multi-step loops. The selected arXiv papers add authoritative coverage of (1) formal action-space framing, (2) schema/validation-centered robustness, and (3) multi-tool orchestration and multi-step plan→act→observe behavior.
**Reviewer:** Given the provided near-misses and the absence of any additional candidates, the curator’s selections are already strong and appropriately prioritize primary, citable research over blog-level or paywalled/unstable materials, with no clear high-authority or seminal source in the rejected list that would materially improve the lesson.
