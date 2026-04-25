# Agentic Coding

## Video (best)
- **Andrej Karpathy** — "Software Is Changing (Again)"
- youtube_id: LCEmiRjPEtQ
- Why: Clear, high-level framing of LLM-driven software development and the shift toward more autonomous/agentic tooling; good conceptual grounding before diving into specific coding agents and workflows.
- Level: Beginner → Intermediate

## Blog / Written explainer (best)
- **Simon Willison** — "Prompt injection explained"
- url: https://simonwillison.net/2023/Nov/27/prompt-injection-explained/
- Why: Essential security and workflow context for agentic coding (tool use, untrusted context, and how “instructions” can be subverted), which directly impacts rules files, context management, and agent-human collaboration.
- Level: Intermediate

## Deep dive
- **Anthropic** — "Building effective agents" [VERIFY]
- url: https://www.anthropic.com/research/building-effective-agents [VERIFY]
- Why: Practical patterns for agent design (task decomposition, tool use, feedback loops) that map well to agentic workflows like iterative debugging, multi-step prompt-to-code, and context management.
- Level: Intermediate → Advanced

## Original paper
- **Yao et al. (2022)** — "ReAct: Synergizing Reasoning and Acting in Language Models"
- url: https://arxiv.org/abs/2210.03629
- Why: Foundational approach for agentic behavior (interleaving reasoning and tool actions) that underpins many modern coding-agent workflows.
- Level: Intermediate → Advanced

## Code walkthrough
- **OpenAI Cookbook** — "Function calling" examples
- url: https://cookbook.openai.com/
- Why: Concrete, runnable patterns for tool/function calling that are directly applicable to coding agents (planning → tool invocation → result integration), and a good base for building prompt-to-code and iterative debugging loops.
- Level: Intermediate

## Coverage notes
- Strong: High-level motivation for agentic coding; foundational agent pattern (ReAct); practical tool-calling patterns; security considerations relevant to context/rules.
- Weak: Specific IDE agent products (Claude Code, Cursor, Windsurf, GitHub Copilot) and their exact feature sets change rapidly and are not covered deeply by the above evergreen resources.
- Gap: A stable, vendor-neutral “agents.md / rules files” best-practices spec and a canonical, long-lived multi-file refactor walkthrough using a modern coding agent in a real repo.

## Last Verified
2026-04-09