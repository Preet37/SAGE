# Curation Report: Agentic Coding
**Topic:** `agentic-coding` | **Date:** 2026-04-09 18:31
**Library:** 2 existing → 15 sources (13 added, 9 downloaded)
**Candidates evaluated:** 49
**Reviewer verdict:** needs_additions

## Added (13)
- **[reference_doc]** [docs.anthropic.com](https://docs.anthropic.com/en/docs/claude-code/cli-reference.md)
  This is official documentation that the tutor can quote for exact commands, defaults/behaviors implied by flags, and how Claude Code exposes tool/server configuration via MCP.
- **[benchmark]** [Introducing SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/)
  Gives the tutor citable, quantitative evaluation framing for real repo-level bug-fix tasks and a canonical place to reference success rates/leaderboard results and evaluation constraints.
- **[benchmark]** [[PDF] REPOBENCH: BENCHMARKING REPOSITORY-LEVEL CODE ...](https://proceedings.iclr.cc/paper_files/paper/2024/file/d191ba4c8923ed8fd8935b7c98658b5f-Paper-Conference.pdf)
  Adds a peer-reviewed benchmark with concrete experimental setup and metrics for repo-level coding, useful for teaching why retrieval/file-selection matters and how it’s measured.
- **[paper]** [Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761)
  Provides an authoritative, step-by-step rationale for tool-use learning that maps directly onto coding-agent tool invocation, helping explain how agents decide when to call tools.
- **[explainer]** [Settings](https://cacm.acm.org/research/measuring-github-copilots-impact-on-productivity/)
  Gives the tutor a more citable, higher-authority venue than vendor blogs for discussing real-world productivity measurement and adoption outcomes.
- **[reference_doc]** [Common workflows - Claude Code Docs](https://code.claude.com/docs/en/common-workflows)
  This directly fills the missing authoritative end-to-end agentic coding workflow need; even if “thin,” it’s exactly the kind of procedural, quotable workflow reference a tutor can ground lessons in.
- **[explainer]** [How Anthropic teams use Claude Code (PDF)](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf)
  The library lacks production agentic-coding case studies; this is unusually authoritative (first-party) and provides concrete process/architecture details beyond generic productivity claims.
- **[reference_doc]** [Best Practices for Claude Code - Claude Code Docs](https://code.claude.com/docs/en/best-practices)
  Complements “common workflows” with the reusable patterns a Socratic tutor needs to teach agentic loops (plan→edit→run→fix) with precision and consistency.
- **[benchmark]** [A Benchmark for Evaluating Repository-Level Code Agents](https://arxiv.org/html/2603.26337v1)
  RepoBench and SWE-bench cover important slices, but this appears to specifically benchmark repo-level *agents*; that fills a concept/measurement gap for “agentic coding” beyond autocomplete.
- **[reference_doc]** [Common workflows - Claude Code Docs](https://code.claude.com/docs/en/common-workflows) *(promoted by reviewer)*
  This directly fills the missing authoritative end-to-end agentic coding workflow need; even if “thin,” it’s exactly the kind of procedural, quotable workflow reference a tutor can ground lessons in.
- **[explainer]** [How Anthropic teams use Claude Code (PDF)](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf) *(promoted by reviewer)*
  The library lacks production agentic-coding case studies; this is unusually authoritative (first-party) and provides concrete process/architecture details beyond generic productivity claims.
- **[reference_doc]** [Best Practices for Claude Code - Claude Code Docs](https://code.claude.com/docs/en/best-practices) *(promoted by reviewer)*
  Complements “common workflows” with the reusable patterns a Socratic tutor needs to teach agentic loops (plan→edit→run→fix) with precision and consistency.
- **[benchmark]** [A Benchmark for Evaluating Repository-Level Code Agents](https://arxiv.org/html/2603.26337v1) *(promoted by reviewer)*
  RepoBench and SWE-bench cover important slices, but this appears to specifically benchmark repo-level *agents*; that fills a concept/measurement gap for “agentic coding” beyond autocomplete.

## Near-Misses (4) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **The Impact of Github Copilot on Developer Productivity: A Ca** — [The Impact of Github Copilot on Developer Productivity: A Case Study](https://www.harness.io/blog/the-impact-of-github-copilot-on-developer-productivity-a-case-study)
  _Skipped because:_ Useful metrics, but it’s a vendor blog post and is less citable/authoritative than the ACM CACM write-up covering similar claims.
- **quantifying GitHub Copilot's impact on developer productivit** — [quantifying GitHub Copilot's impact on developer productivity and ...](https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-on-developer-productivity-and-happiness/)
  _Skipped because:_ Primary-source perspective is valuable, but it overlaps with the selected CACM piece and is more marketing-adjacent for a small, high-authority library.
- **RepoBench: Benchmarking Repository-Level Code** — [RepoBench: Benchmarking Repository-Level Code](https://arxiv.org/pdf/2306.03091.pdf)
  _Skipped because:_ Redundant with the selected ICLR proceedings PDF version of the same work; kept only one canonical, peer-reviewed copy.
- **Claude Code 概述 - Anthropic** — [Claude Code 概述 - Anthropic](https://docs.anthropic.com/zh-TW/docs/agents-and-tools/claude-code/overview)
  _Skipped because:_ An overview page is less precise than the CLI reference for quoting exact commands/flags and configuration surfaces.

## Reasoning
**Curator:** Selections prioritize official documentation for precise operational details, peer-reviewed or canonical benchmark sources for quantitative repo-level performance, and foundational tool-use methodology for explaining agent architectures; weaker/duplicative sources were excluded to keep the library small and authoritative.
**Reviewer:** The curator’s core picks are strong, but the library still needs at least one authoritative end-to-end workflow reference and a production agentic-coding case study, plus a repo-level agent benchmark to round out evaluation coverage.
