# Function Calling

## Video (best)
- **Andrej Karpathy** — No dedicated function-calling video exists from the preferred educators.
- **Fallback: James Briggs (Pinecone)** — "OpenAI Function Calling - Full Beginner Walkthrough"
- youtube_id: aqdWSYWC_LI
- Why: James Briggs consistently produces clear, code-first walkthroughs of OpenAI tooling. This video covers the JSON schema definition, the tool-use loop, and parsing model responses — exactly the mechanics learners need before building agents.
- Level: beginner/intermediate

## Blog / Written explainer (best)
- **Lilian Weng** — "LLM Powered Autonomous Agents"
- url: https://lilianweng.github.io/posts/2023-06-23-agent/
- Why: Weng's post is the canonical written reference for how tool use / function calling fits into the broader agentic architecture. It covers the tool-use loop, JSON schema design, and the reasoning cycle (plan → act → observe) with rigorous detail and clean diagrams. It contextualizes function calling rather than treating it as an isolated API trick.
- Level: intermediate/advanced

## Deep dive
- **OpenAI Official Documentation** — "Function Calling Guide"
- url: https://platform.openai.com/docs/guides/function-calling
- Why: The authoritative technical reference covering the full lifecycle: defining tool schemas, parallel tool calling, strict mode JSON schema enforcement, streaming with tool calls, and error handling patterns. Updated as the API evolves. No third-party resource matches its completeness or accuracy for implementation details.
- Level: intermediate

## Original paper
- **Patil et al. (2023)** — "Gorilla: Large Language Model Connected with Massive APIs"
- url: https://arxiv.org/abs/2305.15334
- Why: This is the most readable seminal paper specifically on LLMs calling external APIs/tools. It introduces the retrieval-augmented approach to tool use, benchmarks hallucination in API calls, and directly motivates why structured function schemas matter. More focused on function calling mechanics than the broader ReAct or Toolformer papers.
- Level: advanced

## Code walkthrough
- **DeepLearning.AI** — "Functions, Tools and Agents with LangChain" (short course)
- url: https://www.deeplearning.ai/short-courses/functions-tools-agents-langchain/
- Why: Hands-on Jupyter notebooks co-created with LangChain covering function/tool definition, the tool-use loop, parallel tool calling, and building a complete agent. Taught by Harrison Chase. Free to audit. Covers both raw OpenAI function calling and the abstraction layer — ideal for learners who need to see both levels.
- Level: beginner/intermediate

---

## Coverage notes
- **Strong:** JSON schema definition, the tool-use loop, OpenAI API mechanics, agentic context (Weng), hands-on code (DeepLearning.AI)
- **Weak:** Model Context Protocol (MCP) specifically — no single resource covers MCP + function calling together well yet; E2B sandboxed execution in the context of tool use; text-to-SQL as a function-calling pattern
- **Gap:** No high-quality video from the *preferred* educator list (3Blue1Brown, Karpathy, Kilcher, StatQuest, Serrano, Stanford/MIT) exists specifically for function calling as of early 2025. The topic is too API-specific for their typical mathematical/conceptual focus. The James Briggs recommendation above should be ****-ed for the exact video ID before publishing. Parallel tool calling and streaming tool calls also lack dedicated deep-dive video content.
- **Gap:** Error recovery patterns (retrying malformed tool calls, fallback strategies) are covered only incidentally in existing resources — no dedicated tutorial exists.


> **[Structural note]** "The ReAct Pattern: Synergizing Reasoning and Acting" appears to have sub-concepts:
> react pattern, thought-action-observation cycle, reasoning traces, tool calling, task decomposition, grounded reasoning
> *Discovered during enrichment for course "A hands-on intermediate course for software developers and AI/ML engineers cover" | 2026-04-10*


> **[Structural note]** "Implementing a ReAct Agent with LangGraph" appears to have sub-concepts:
> react loop, thought-action-observation, langgraph state, iterative agent execution
> *Discovered during enrichment for course "A hands-on intermediate course for software developers and AI/ML engineers cover" | 2026-04-10*

## Last Verified
2025-04-06