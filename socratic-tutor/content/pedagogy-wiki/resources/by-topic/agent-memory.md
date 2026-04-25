# Agent Memory

## Video (best)
- **Sam Witteveen** — "LangChain - Conversations with Memory (explanation & code walkthrough)"
- youtube_id: X550Zbz_ROE
- Why: Covers LangChain memory types (buffer, window, summary, entity) with code walkthroughs — the most accessible video introduction to memory patterns in LLM agents.
- Level: intermediate

---

## Blog / Written explainer (best)
- **Lilian Weng** — "LLM Powered Autonomous Agents"
- url: https://lilianweng.github.io/posts/2023-06-23-agent/
- Why: Weng's post has a dedicated, well-structured section on agent memory — explicitly breaking down sensory, short-term, and long-term memory, with coverage of vector stores, episodic memory, and knowledge retrieval. It is the most cited written explainer in the agentic AI space and connects memory to the broader agent architecture in a pedagogically coherent way.
- Level: intermediate

---

## Deep dive
- **LangChain / LangGraph Documentation** — "Memory in LangGraph"
- url: https://langchain-ai.github.io/langgraph/concepts/memory/
- Why: Provides the most comprehensive technical breakdown of how memory is implemented in a production agentic framework — covering in-thread vs. cross-thread memory, semantic memory stores, episodic recall, and integration with vector databases. Bridges theory and implementation better than any standalone article.
- Level: advanced

---

## Original paper
- **Generative Agents: Interactive Simulacra of Human Behavior** — Park et al., 2023
- url: https://arxiv.org/abs/2304.03442
- Why: This is the clearest seminal paper on agent memory architectures. It explicitly introduces a memory stream (episodic storage), retrieval mechanisms combining recency + importance + relevance, and reflection/synthesis into higher-level memories. Highly readable and directly maps to the concepts taught in this topic (episodic memory, semantic memory, long-term memory, personalization).
- Level: intermediate/advanced

---

## Code walkthrough
- **mem0ai/mem0 GitHub repository** — Official mem0 quickstart and examples
- url: https://github.com/mem0ai/mem0
- Why: mem0 is the most focused open-source library specifically built for agent memory (long-term, personalized memory for LLM applications). The repository includes working examples of adding, retrieving, and updating memories across sessions — directly demonstrating vector store integration, user-level personalization, and semantic search over memory. Hands-on and immediately runnable.
- Level: intermediate

---

## Coverage notes
- **Strong:** Written explainers (Lilian Weng's agent post is excellent), original research (Generative Agents paper is canonical), and code-level implementations (mem0, LangGraph memory docs).
- **Weak:** Video content from top-tier ML educators. Agent memory is a relatively applied/systems topic that hasn't attracted the same deep-learning-theory video treatment as transformers or backprop.
- **Gap:** No high-quality video from the preferred educator list (3Blue1Brown, Karpathy, Yannic, StatQuest, Serrano, Stanford/MIT) specifically addresses agent memory architectures. Knowledge graphs as a memory substrate are also underserved in beginner-friendly formats. A dedicated explainer video on the episodic/semantic/procedural memory taxonomy in agents would be a valuable addition to this platform.

---


> **[Structural note]** "What Are AI Agents? Core Concepts and Architecture" appears to have sub-concepts:
> reasoning loop, perception and action, autonomous decision-making
> *Discovered during enrichment for course "A hands-on intermediate course for software developers and AI/ML engineers cover" | 2026-04-10*


> **[Structural note]** "Agent Memory: Short-Term Context and Long-Term Storage" appears to have sub-concepts:
> in-context memory
> *Discovered during enrichment for course "A hands-on intermediate course for software developers and AI/ML engineers cover" | 2026-04-10*


> **[Structural note]** "Building Your First LangGraph Agent" appears to have sub-concepts:
> langgraph state, messagesstate, tool calling, graph compilation, agent loop, langchain integration
> *Discovered during enrichment for course "A hands-on intermediate course for software developers and AI/ML engineers cover" | 2026-04-10*

## Last Verified
2025-01-01 (resource existence confirmed to knowledge cutoff; URLs marked should be checked before publishing)