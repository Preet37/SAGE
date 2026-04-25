# Curation Report: What Are AI Agents? Core Concepts and Architecture
**Topic:** `agent-memory` | **Date:** 2026-04-10 18:56
**Library:** 5 existing → 7 sources (2 added, 2 downloaded)
**Candidates evaluated:** 15
**Reviewer verdict:** good

## Added (2)
- **[reference_doc]** [[PDF] 2 INTELLIGENT AGENTS](https://cse-robotics.engr.tamu.edu/dshell/cs625/ch2.pdf)
  An authoritative textbook-style treatment of agents as perceiving via sensors and acting via actuators, with clear definitions of percepts/percept sequences and agent functions—exactly the missing observation vs action interface framing.
   — covers: Perception/observation vs action interfaces in agent design (what counts as observations, environment/tool outputs, and how actions are selected/executed)
- **[paper]** [Toward a Theory of Agents as Tool-Use Decision-Makers](https://arxiv.org/pdf/2506.00886.pdf)
  Provides a principled framework for autonomous tool-use decisions (when to act externally vs reason internally) and ties stopping/tool-calling to epistemic/knowledge boundaries, adding depth beyond implementation-focused agent blogs/docs.
   — covers: Autonomous decision-making in agents: how agents decide next steps, when to call tools, when to stop, and how this differs from predetermined workflows (include concrete examples)

## Near-Misses (13) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **What Is the AI Agent Loop? The Core Architecture Behind ...** — [What Is the AI Agent Loop? The Core Architecture Behind ...](https://blogs.oracle.com/developers/what-is-the-ai-agent-loop-the-core-architecture-behind-autonomous-ai-systems)
  _Skipped because:_ Likely covers the control loop at a high level, but it’s a vendor blog and typically less rigorous/stable than adding a canonical reference or paper.
- **How AI agents work** — [How AI agents work](https://www.ibm.com/think/topics/ai-agents)
  _Skipped because:_ Good introductory overview, but tends to be conceptual/marketing-oriented and may not add substantial detail beyond what your existing agent primers already provide.
- **Observation and Action Cycles in LLM Agents - ApX Machine Le** — [Observation and Action Cycles in LLM Agents - ApX Machine Learning](https://apxml.com/courses/intro-llm-agents/chapter-2-llm-agent-building-blocks/the-agents-operational-loop)
  _Skipped because:_ Potentially on-target for the loop, but it’s a course page of uncertain authority/longevity compared with more canonical references.
- **Deep Dive into Agent Architectures, Self-Reflection, and ...** — [Deep Dive into Agent Architectures, Self-Reflection, and ...](https://dev.to/dhanashree_mohite_e87853d/deep-dive-into-agent-architectures-self-reflection-and-tool-call-loops-2ld9)
  _Skipped because:_ Dev.to posts are often uneven and less citable; likely overlaps with existing agent blog coverage without adding a uniquely authoritative treatment.
- **The Hybrid Pattern In...** — [The Hybrid Pattern In...](https://dev.to/nebulagg/agents-vs-workflows-a-decision-framework-for-2026-19ab)
  _Skipped because:_ The agents-vs-workflows contrast is relevant, but the source is a community blog with unclear rigor and may be redundant with better primary/academic treatments.
- **Action and Perception in Man-Made Environments*** — [Action and Perception in Man-Made Environments*](https://www.ijcai.org/Proceedings/95-1/Papers/061.pdf)
  _Skipped because:_ Reputable venue, but likely too specialized/older and less directly useful for a modern LLM-agent architecture lesson than a clear textbook chapter on percepts/actions.
- **Perceptions or actions? Grounding how agents interact within** — [Perceptions or actions? Grounding how agents interact within ...](https://publications.aston.ac.uk/id/eprint/40894/1/Perceptions_or_actions.pdf)
  _Skipped because:_ Seems relevant to perception/action grounding, but it’s less canonical for teaching core agent interfaces than the standard textbook framing.
- **Rational Decision Making in Autonomous Agents** — [Rational Decision Making in Autonomous Agents](http://cs.uns.edu.ar/~gis/publications/Parsons-Simari-WICC2004.pdf)
  _Skipped because:_ Could be useful background on autonomy, but it’s older and not clearly tied to modern tool-calling/stop decisions in LLM agents, so the arXiv tool-use decision paper is a better fit.
- **Toward More Efficient and Useful LLM Agents** — [Toward More Efficient and Useful LLM Agents](https://kangwooklee.com/talks/2026_03_BLISS/bliss_seminar_monograph.html)
  _Skipped because:_ Unclear provenance/content from the snippet (appears duplicated/placeholder); without clear access to a stable, substantive monograph, it’s risky to curate.
- **11** — [11](https://www.scribd.com/document/844194360/11)
  _Skipped because:_ Scribd-hosted with an opaque title and unclear authorship; not a stable or reliably citable source for a high-quality teaching wiki.
- **Fundamentals of Artificial Intelligence Chapter 02** — [Fundamentals of Artificial Intelligence Chapter 02](http://disi.unitn.it/rseba/DIDATTICA/fai_2022/SLIDES/HANDOUTS-02-intelligent-agents.pdf)
  _Skipped because:_ Likely overlaps heavily with the standard Russell & Norvig Chapter 2 material; adding one strong canonical chapter is sufficient.
- **Russell & Norvig Chapter 2** — [Russell & Norvig Chapter 2](https://cs.brynmawr.edu/Courses/cs372/spring2012/slides/02_IntelligentAgents.pdf)
  _Skipped because:_ Good content but this is a course slide deck (less stable/complete than a chapter PDF); the added Chapter 2 PDF already fills the same gap more directly.
- **Toward a Theory of Agents as Tool-Use Decision-Makers - arXi** — [Toward a Theory of Agents as Tool-Use Decision-Makers - arXiv](https://arxiv.org/html/2506.00886v1)
  _Skipped because:_ Redundant with the PDF version; the PDF is the better canonical artifact to curate.

## Uncovered Gaps (1) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- A clear, general agent control loop description (observe/perceive → plan/reason → act/tool call → update memory/state → repeat until goal/stop condition), with an explicit contrast to a single LLM call

## Reasoning
**Curator:** Only two candidates clearly add non-redundant, high-quality coverage: a canonical agents chapter for perception/action interfaces and a recent arXiv paper that deepens autonomous tool-use decision-making. The remaining loop-focused candidates are mostly vendor/community posts or have unclear provenance, so they don’t meet the bar for a curated teaching library.
**Reviewer:** Given the provided near-misses list, none clearly beat the added textbook-style agent chapter plus the tool-use decision-making paper on authority, stability, or unique coverage of the remaining control-loop gap, so the curator’s selectivity looks appropriate.

---

# Curation Report: Agent Memory: Short-Term Context and Long-Term Storage
**Topic:** `agent-memory` | **Date:** 2026-04-10 18:57
**Library:** 7 existing → 13 sources (6 added, 5 downloaded)
**Candidates evaluated:** 15
**Reviewer verdict:** needs_additions

## Added (6)
- **[tutorial]** [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  Provides concrete, production-oriented patterns for assembling and pruning in-context state (what to include, what to drop, and how to structure context) with practical guidance for keeping prompts small without losing coherence—material not covered deeply by the current library.
   — covers: In-context memory mechanics: how in-context state is constructed (system/developer/user messages, tool outputs), managed, and truncated/summarized within context windows, Examples/patterns for keeping prompts small while maintaining coherence (e.g., summarization buffers, sliding windows, selective message retention)
- **[tutorial]** [Context Summarization](https://cookbook.openai.com/examples/agents_sdk/session_memory)
  Adds an implementable reference example of session memory + context summarization (how to maintain a running summary and manage truncation) that directly addresses prompt-length management with code-level specificity.
   — covers: In-context memory mechanics: how in-context state is constructed (system/developer/user messages, tool outputs), managed, and truncated/summarized within context windows, Examples/patterns for keeping prompts small while maintaining coherence (e.g., summarization buffers, sliding windows, selective message retention)
- **[reference_doc]** [Context and Memory - AgentScope](https://docs.agentscope.io/basic-concepts/context-and-memory)
  Offers a framework-grounded, explicit mapping between 'context' (in-model prompt state) and 'memory' (agent-managed stores), helping clarify terminology and how it manifests as thread/session state vs model context in an agent system.
   — covers: Clear distinction between 'in-context memory' vs 'short-term memory' terminology and how it maps to agent frameworks (thread/session state vs model context)
- **[paper]** [Characterizing Prompt Compression Methods for Long Context ...](https://arxiv.org/html/2407.08892v1)
  Adds a research-backed view of prompt compression/summarization tradeoffs and failure modes, complementing practitioner guides with empirical characterization of methods for preserving information under tight context budgets.
   — covers: Examples/patterns for keeping prompts small while maintaining coherence (e.g., summarization buffers, sliding windows, selective message retention)
- **[tutorial]** [Anatomy of a Context Window: A Guide to Context Engineering (Letta)](https://www.letta.com/blog/anatomy-of-a-context-window)
  Worth promoting despite overlap risk because it’s one of the clearest, diagram-friendly treatments of how prompts are actually assembled (roles, tool traces, truncation points) and tends to be more concrete than generic “prompt length” posts—useful as a teaching explainer alongside production docs.
- **[tutorial]** [Anatomy of a Context Window: A Guide to Context Engineering (Letta)](https://www.letta.com/blog/anatomy-of-a-context-window) *(promoted by reviewer)*
  Worth promoting despite overlap risk because it’s one of the clearest, diagram-friendly treatments of how prompts are actually assembled (roles, tool traces, truncation points) and tends to be more concrete than generic “prompt length” posts—useful as a teaching explainer alongside production docs.

## Near-Misses (11) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Anatomy of a Context Window: A Guide to Context Engineering ** — [Anatomy of a Context Window: A Guide to Context Engineering - Letta](https://www.letta.com/blog/guide-to-context-engineering)
  _Skipped because:_ Potentially strong, but overlaps with other context-engineering tutorials being added and the snippet suggests it may mirror the same whitepaper content; add only if it contains unique diagrams/framework comparisons.
- **[PDF] Breaking the Limit of Context Window Size via Long Sho** — [[PDF] Breaking the Limit of Context Window Size via Long Short-term ...](https://aclanthology.org/2025.findings-acl.595.pdf)
  _Skipped because:_ Likely relevant to long/short-term mechanisms, but appears more about extending effective context length than practical session/context construction and truncation patterns targeted by the gaps.
- **Understanding and Improving Information Preservation in Prom** — [Understanding and Improving Information Preservation in Prompt ...](https://arxiv.org/html/2503.19114v2)
  _Skipped because:_ Research-relevant, but without clearer evidence it directly informs actionable prompt-retention/summarization strategies beyond what the selected compression paper covers.
- **SWin: A Sliding Window Summarization Approach for Coherent L** — [SWin: A Sliding Window Summarization Approach for Coherent LLM ...](https://spectrum.library.concordia.ca/id/eprint/996148/)
  _Skipped because:_ Could be useful for sliding-window summarization, but as a thesis/repository item it may be less canonical and harder to extract into broadly applicable guidance than the chosen sources.
- **Managing Prompt Length and Context Windows** — [Managing Prompt Length and Context Windows](https://apxml.com/courses/prompt-engineering-llm-application-development/chapter-3-prompt-design-iteration-evaluation/managing-prompt-length-context)
  _Skipped because:_ Covers basics but appears relatively generic and potentially thin compared to the Anthropic/OpenAI materials.
- **Making Sense of Memory in AI Agents - Leonie Monigatti** — [Making Sense of Memory in AI Agents - Leonie Monigatti](https://www.leoniemonigatti.com/blog/memory-in-ai-agents.html)
  _Skipped because:_ May clarify terminology, but it’s a personal blog and likely less authoritative/stable than framework docs for the same gap.
- **Context Engineering- Sessions & Memory | PDF - Scribd** — [Context Engineering- Sessions & Memory | PDF - Scribd](https://www.scribd.com/document/947756966/Context-Engineering-Sessions-Memory)
  _Skipped because:_ Scribd is paywalled/unstable for a teaching wiki and is not an authoritative primary host.
- **[PDF] Context Engineering: Sessions, Memory** — [[PDF] Context Engineering: Sessions, Memory](https://smallake.kr/wp-content/uploads/2025/12/Context-Engineering_-Sessions-Memory.pdf)
  _Skipped because:_ Looks like a rehosted PDF of unclear provenance; without an official publisher/author landing page it’s risky to curate.
- **[PDF] Context Engineering: Sessions, Memory** — [[PDF] Context Engineering: Sessions, Memory](https://www.cdut.edu.cn/__local/2/CC/D2/C44B0CC9F8978C5BFA029413538_450FAE19_730DBA.pdf)
  _Skipped because:_ Unclear provenance/officiality (university local file path) despite promising table of contents; prefer an official source URL.
- **[PDF] L10_Memory + Context Engineering** — [[PDF] L10_Memory + Context Engineering](https://bt5153msba.github.io/slides/w10.pdf)
  _Skipped because:_ Course slides can be good but are often context-dependent and less durable than primary tutorials/docs; would add only if uniquely clear and properly attributed.
- **Agent Short-Term Memory: Working Memory Guide | AI Wiki** — [Agent Short-Term Memory: Working Memory Guide | AI Wiki](https://artificial-intelligence-wiki.com/agentic-ai/agent-architectures-and-components/agent-short-term-memory/)
  _Skipped because:_ Wiki-style secondary content with uncertain rigor; likely redundant with stronger primary sources and framework docs.

## Reasoning
**Curator:** Selected sources prioritize authoritative, durable practitioner guidance (Anthropic/OpenAI) for concrete context construction and truncation patterns, plus one framework doc for terminology mapping and one research paper for empirical prompt-compression tradeoffs; other candidates were excluded due to provenance, redundancy, or thin/generic coverage.
**Reviewer:** The curator’s additions are strong and largely cover the stated gaps; the only near-miss that plausibly earns a slot on clarity/teachability grounds is Letta’s context-window anatomy guide.

---

# Curation Report: Building Your First LangGraph Agent
**Topic:** `agent-memory` | **Date:** 2026-04-10 19:00
**Library:** 12 existing → 17 sources (5 added, 4 downloaded)
**Candidates evaluated:** 37
**Reviewer verdict:** good

## Added (5)
- **[reference_doc]** [Quickstart - Docs by LangChain](https://docs.langchain.com/oss/python/langgraph/quickstart)
  Official, end-to-end walkthrough of the canonical LangGraph agent loop (LLM -> tools -> LLM) including ToolNode usage and stopping/termination patterns, which directly fills multiple practical implementation gaps.
   — covers: LangGraph ToolNode: purpose, required state keys, how it executes tools, and how tool results are written back to state/messages, Implementing an agent loop in LangGraph: explicit control flow pattern (LLM node -> tool node -> LLM node), stopping criteria, and handling repeated tool calls, LangChain integration end-to-end: using LangChain chat models and tools inside LangGraph nodes, including tool binding and message interoperability, Graph compilation/execution: graph.compile(), what it returns, validation, runtime behavior, streaming, and invocation API
- **[reference_doc]** [Graph API overview - Docs by LangChain](https://docs.langchain.com/oss/python/langgraph/graph-api)
  Authoritative reference for StateGraph fundamentals (state schema, node updates, reducers/merge semantics) and conditional routing APIs, providing the conceptual grounding missing from the current library.
   — covers: LangGraph state fundamentals: state schema, how nodes read/write state, reducers/merge behavior, and how state evolves across steps, Conditional routing in LangGraph: add_conditional_edges/router functions, branching patterns for tool-use vs final answer, and termination conditions, Graph compilation/execution: graph.compile(), what it returns, validation, runtime behavior, streaming, and invocation API
- **[reference_doc]** [Tool calling - GitHub Pages](https://langchain-ai.github.io/langgraph/concepts/tools/)
  Focused, official conceptual documentation on tool calling in LangGraph/LangChain (tool definitions, schemas, binding, and interpreting tool-call outputs), complementing the Quickstart with deeper explanation.
   — covers: Tool calling in LangGraph/LangChain: defining tools, tool schemas, binding tools to chat models, and interpreting tool-call outputs, LangGraph ToolNode: purpose, required state keys, how it executes tools, and how tool results are written back to state/messages
- **[reference_doc]** [ConditionalEdgeRouter | @langchain/langgraph (JavaScript Reference)](https://reference.langchain.com/javascript/langchain-langgraph/index/ConditionalEdgeRouter)
  This is canonical API reference (not a blog/mirror) and is useful for teaching precise conditional routing semantics and signatures, especially if the lesson targets JS/TS users or wants language-parity with Python docs.
- **[reference_doc]** [ConditionalEdgeRouter | @langchain/langgraph (JavaScript Reference)](https://reference.langchain.com/javascript/langchain-langgraph/index/ConditionalEdgeRouter) *(promoted by reviewer)*
  This is canonical API reference (not a blog/mirror) and is useful for teaching precise conditional routing semantics and signatures, especially if the lesson targets JS/TS users or wants language-parity with Python docs.

## Near-Misses (12) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **StateGraph and MessagesState | langchain-ai/langchain** — [StateGraph and MessagesState | langchain-ai/langchain](https://deepwiki.com/langchain-ai/langchain-academy/3.1-stategraph-and-messagesstate)
  _Skipped because:_ Likely useful, but it’s a third-party mirror/derivative (DeepWiki) rather than the canonical LangChain docs, so it’s less stable/authoritative than adding the official documentation directly.
- **Call tools - Docs by LangChain** — [Call tools - Docs by LangChain](https://docs.langchain.com/oss/python/langgraph/call-tools)
  _Skipped because:_ Overlaps heavily with the LangGraph concepts/tools page; keeping the single best official tools reference avoids redundancy.
- **Tools - Docs by LangChain** — [Tools - Docs by LangChain](https://docs.langchain.com/oss/python/langchain/tools)
  _Skipped because:_ Good general LangChain tools reference, but less LangGraph-specific than the selected LangGraph tool-calling docs and Quickstart.
- **LangGraph Tool Calling: ToolNode, Parallel Tools, and Custom** — [LangGraph Tool Calling: ToolNode, Parallel Tools, and Custom Tools](https://www.abstractalgorithms.dev/langgraph-tool-calling-toolnode-and-custom-tools)
  _Skipped because:_ Covers relevant topics but is explicitly for a v1-alpha release and is less stable than the official docs for a teaching wiki.
- **The Architecture of Agent Memory: How LangGraph Really Works** — [The Architecture of Agent Memory: How LangGraph Really Works](https://dev.to/sreeni5018/the-architecture-of-agent-memory-how-langgraph-really-works-59ne)
  _Skipped because:_ Non-official blog post with unclear technical accuracy/maintenance; the official Graph API docs better cover reducers/state semantics.
- **Understanding LangGraph State Schemas, MessagesState, and Re** — [Understanding LangGraph State Schemas, MessagesState, and Reducers (Step-by-Step Tutorial)](https://www.youtube.com/watch?v=qMO49-pZfDg)
  _Skipped because:_ Potentially helpful, but video quality/accuracy is harder to vet and less durable than the official docs for core semantics.
- **A Beginner's Guide to Getting Started in Agent State in Lang** — [A Beginner's Guide to Getting Started in Agent State in LangGraph](https://dev.to/aiengineering/a-beginners-guide-to-getting-started-in-agent-state-in-langgraph-3bkj)
  _Skipped because:_ Likely redundant with the official Graph API/Quickstart coverage and less authoritative.
- **Principle:Langchain ai Langgraph State Schema Definition** — [Principle:Langchain ai Langgraph State Schema Definition](https://leeroopedia.com/index.php/Principle:Langchain_ai_Langgraph_State_Schema_Definition)
  _Skipped because:_ Wiki-style/secondary source with uncertain provenance; prefer canonical LangChain documentation.
- **Principle:Langchain ai Langgraph Agent State Schema - Leeroo** — [Principle:Langchain ai Langgraph Agent State Schema - Leeroopedia](https://leeroopedia.com/index.php/Principle:Langchain_ai_Langgraph_Agent_State_Schema)
  _Skipped because:_ Same issue as above (secondary, less reliable) and overlaps with official docs.
- **State** — [State](https://docs.haystack.deepset.ai/docs/2.21/state)
  _Skipped because:_ High-quality but about Haystack’s state concept, not LangGraph’s StateGraph/MessagesState specifics needed for this lesson.
- **State Management | jun-sajima/langgraph-study | DeepWiki** — [State Management | jun-sajima/langgraph-study | DeepWiki](https://deepwiki.com/jun-sajima/langgraph-study/5.1-state-management)
  _Skipped because:_ Third-party summary/mirror; less authoritative and potentially redundant with official LangGraph docs.
- **State management - Deep Research Agent** — [State management - Deep Research Agent](https://www.mintlify.com/balaji1233/DEEP_RESEARCH_AGENT/architecture/state-management)
  _Skipped because:_ Project-specific documentation; may not generalize cleanly to LangGraph fundamentals and risks being less stable.

## Uncovered Gaps (1) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- MessagesState deep dive: structure, message types, how messages are appended/merged, and best practices for message-based agent state

## Reasoning
**Curator:** The best improvements are the canonical LangChain/LangGraph docs that directly teach StateGraph/reducers, conditional routing, compilation/execution, and the standard tool-using agent loop. Most other candidates are secondary mirrors, alpha-era posts, or less durable sources that would add redundancy or risk.
**Reviewer:** The curator’s additions are appropriately canonical and durable; most near-misses are rightly excluded as unstable/secondary, with the only strong add being the official JS API reference if you want authoritative coverage beyond Python.
