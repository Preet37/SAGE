# Source: https://www.arxiv.org/pdf/2601.00821.pdf
# Author: Tao An
# Title: Verbatim-Grounded Artifact Extraction for Long LLM Conversations
# Fetched via: trafilatura
# Date: 2026-04-09

CogCanvas: Verbatim-Grounded Artifact Extraction for Long LLM Conversations
Abstract
Conversation summarization loses nuanced details: when asked about coding preferences after 40 turns, summarization recalls “use type hints” but drops the critical constraint “everywhere” (19.0% exact match vs. 93.0% for our approach).
We present CogCanvas, a training-free framework inspired by how teams use whiteboards to anchor shared memory. Rather than compressing conversation history, CogCanvas extracts verbatim-grounded artifacts (decisions, facts, reminders) and retrieves them via temporal-aware graph.
On the LoCoMo benchmark (all 10 conversations from the ACL 2024 release), CogCanvas achieves the highest overall accuracy among training-free methods (32.4%), outperforming RAG (24.6%) by +7.8pp, with decisive advantages on complex reasoning tasks: +20.6pp on temporal reasoning (32.7% vs. 12.1% RAG) and +1.1pp on multi-hop questions (41.7% vs. 40.6% RAG). CogCanvas also leads on single-hop retrieval (26.6% vs. 24.6% RAG). Ablation studies reveal that BGE reranking contributes +7.7pp, making it the largest contributor to CogCanvas’s performance.
While heavily-optimized approaches achieve higher absolute scores through dedicated training (EverMemOS: 92%), our training-free approach provides practitioners with an immediately-deployable alternative that significantly outperforms standard baselines.
Code and data: [https://github.com/tao-hpu/cog-canvas](https://github.com/tao-hpu/cog-canvas).
Keywords: Large Language Models, Context Management, Verbatim Grounding, Information Retention, Training-Free
1 Introduction
“Please use type hints everywhere.”
This seemingly simple coding constraint, mentioned casually in turn 3 of a 50-turn programming discussion, exemplifies the kind of nuanced detail that gets systematically lost when context compression becomes necessary. Truncation discards it entirely once the context window fills; summarization paraphrases it to “the user prefers type hints,” losing the critical quantifier everywhere that changes implementation requirements.
In our controlled benchmark, summarization-based context management achieves only 19.0% exact match on such constraints, compared to 93.0% for verbatim-grounded retrieval. This 74 percentage point gap represents a fundamental trade-off: compression efficiency vs. detail fidelity.
Large language models (LLMs) excel at conducting multi-turn conversations, yet they remain constrained by finite context windows. As conversations extend over dozens or hundreds of turns, practitioners face an inevitable dilemma: truncate the context (discarding early information) or compress it through summarization (risking information loss). This tension between context capacity and information fidelity represents a core challenge in deploying LLMs for sustained, coherent interactions.
Current approaches to managing long conversations fall into two dominant paradigms, each with significant limitations. Truncation-based methods simply discard older turns when the context budget is exceeded, resulting in catastrophic forgetting of early-conversation information. Summarization-based methods employ LLMs to compress conversation history into condensed representations, but this process inherently introduces information loss—subtle details such as specific constraints (“use type hints everywhere”), nuanced preferences, or conditional decisions are often smoothed over or omitted entirely. Neither approach adequately preserves the structured knowledge that accumulates throughout extended interactions.
We observe that human experts navigating complex, long-running projects do not rely solely on verbatim transcripts or lossy summaries. Instead, they maintain cognitive artifacts—explicit records of decisions made, facts established, and tasks pending—that serve as compression-tolerant anchors for memory. These artifacts are inherently structured, semantically retrievable, and persist independently of the conversational flow that generated them.
This distinction reveals a fundamental asymmetry between two approaches to information preservation. Summarization operates as lossy compression: each pass over accumulated context “dilutes” the original signal, risking what we term recursive information decay: the compounding loss of nuance through iterative abstraction. In contrast, artifact extraction functions as semantic distillation: isolating discrete, self-contained units of meaning that crystallize into persistent anchors. These crystallized artifacts remain retrievable in their original form regardless of how much surrounding context is compressed or discarded.
Recent work has demonstrated that heavily-optimized approaches can achieve impressive performance through dedicated training infrastructure—EverMemOS [evermemos2025] achieves 92.3% on LoCoMo through categorical memory extraction and fine-tuning, while EMem [emem2024] reaches 78% via task-specific optimization. However, these methods require substantial engineering investment: domain-specific corpora, fine-tuning pipelines, or complex architectural modifications. This creates a gap for practitioners who need effective solutions immediately, without the overhead of training infrastructure.
This observation motivates our work: by combining verbatim-grounded artifact extraction with temporal-aware graph construction and reasoning-aware prompting, can we build a training-free, plug-and-play framework that substantially outperforms standard baselines (RAG, summarization) while remaining immediately deployable?
We propose CogCanvas, a session-level, graph-enhanced RAG system specialized for managing dynamic conversation history. Unlike traditional context truncation or summarization, CogCanvas structures dialogue into a lightweight in-memory graph, enabling 1-hop contextual expansion to retrieve related artifacts that vector similarity alone might miss. Our approach makes the following contributions:
-
•
We introduce a verbatim-grounded artifact extraction mechanism that identifies and extracts structured cognitive objects (Decisions, Facts, Insights, Todos) while preserving exact source quotations, enabling traceable and hallucination-tolerant retrieval.
-
•
We design an enhanced graph construction strategy that integrates semantic similarity with lexical and temporal heuristics to establish robust, causally-aware links between artifacts.
-
•
We propose a hybrid retrieval and reasoning-aware injection algorithm that fuses semantic and keyword-based retrieval, guiding LLMs to synthesize causal explanations from retrieved artifacts.
-
•
We provide a training-free, plug-and-play baseline that achieves strong performance on controlled benchmarks (97.5% recall, +78.5pp vs. summarization) and the highest accuracy among training-free methods on LoCoMo (32.4% overall, +7.8pp vs. RAG), with decisive advantages on complex reasoning tasks: +20.6pp on temporal reasoning and +1.1pp on multi-hop questions. CogCanvas leads across all question types including single-hop retrieval (26.6% vs. 24.6%).
Experimental evaluation demonstrates CogCanvas’s effectiveness across controlled benchmarks and real-world datasets. Our approach achieves 97.5% recall (+78.5pp vs. summarization) on information retention tasks. On the LoCoMo benchmark (all 10 conversations from the ACL 2024 release), CogCanvas achieves the highest accuracy among training-free methods (32.4%), outperforming RAG (24.6%) by +7.8pp overall, with decisive advantages on complex reasoning—temporal questions (+20.6pp: 32.7% vs. 12.1%) and multi-hop questions (+1.1pp: 41.7% vs. 40.6%). CogCanvas leads across all question types including single-hop (26.6% vs. 24.6%).
2 Related Work
Our work intersects with context management, memory-augmented LLMs, graph-based retrieval, and conversation summarization. Context window management approaches include sparse attention [child2019sparsetransformer, beltagy2020longformer] and retrieval-augmented methods [borgeaud2022retro, izacard2022atlas]; we focus on what to preserve rather than extending capacity.
Memory-augmented LLMs range from hierarchical systems to heavily-optimized approaches. MemGPT [packer2023memgpt] pioneered OS-inspired virtual memory management for LLMs with self-editing memory tools; the original project has since evolved into Letta,111[https://letta.ai](https://letta.ai) a production framework extending the core architecture with filesystem-based memory storage. Letta’s recent evaluation on LoCoMo reported 74.0% accuracy using GPT-4o mini [letta2024memory], demonstrating the effectiveness of stateful, database-backed memory systems—though this comes at the cost of requiring persistent infrastructure (PostgreSQL, Docker). EverMemOS [evermemos2025] achieves 92.3% on LoCoMo through categorical memory extraction and fine-tuning, while EMem [emem2024] reaches 78% via task-specific optimization. CogCanvas targets a complementary niche as a training-free baseline, prioritizing deployment simplicity over peak performance.
Graph-based methods like GraphRAG [edge2024graphrag] excel at static documents but struggle with dynamic conversational state. Summarization [xu2021dialogueSummary, chen2021dialogsum] operates on lossy compression, systematically losing specific details. See Appendix [G](https://arxiv.org/html/2601.00821v2#A7) for extended discussion.
| Method | Dynamic | Exact | Low Overhead |
|---|---|---|---|
| Truncation | ✓ | ✗ | ✓ |
| Summarization | ✓ | ✗ | ✓ |
| GraphRAG | ✗ | ✓ | ✗ |
| CogCanvas | ✓ | ✓ | ✓ |
3 Method
CogCanvas operates through three tightly coupled mechanisms: (1) typed artifact extraction that identifies cognitive objects from conversational turns, (2) semantic graph construction that organizes these objects into a queryable structure, and (3) adaptive injection that selectively reintroduces relevant artifacts into the active context. Figure [1](https://arxiv.org/html/2601.00821v2#S3.F1) illustrates the overall pipeline.
3.1 CanvasObject Structure
We define a CanvasObject as a typed tuple representing a single cognitive artifact:
| (1) |
where Decision, Todo, KeyFact, Reminder, Insight is the semantic type, is the content string, is the grounding quote (verbatim excerpt from the source message), indicates the message source, is the embedding vector, is the turn index, and is the extraction confidence score.
The type taxonomy reflects cognitive categories that humans naturally employ when tracking project state. Critically, each object maintains its grounding quote , enabling verbatim retrieval and preventing hallucinated reconstructions.
3.2 Graph Construction
Extraction via LLM with Gleaning.
At each conversation turn , we invoke an extraction LLM to identify cognitive objects:
| (2) |
where represents previously extracted objects, provided as context to enable the extractor to avoid duplicates and resolve references.
To capture implicit entities that may be missed in a single pass, we employ gleaning—a two-pass extraction strategy inspired by LightRAG [guo2024lightrag]. The second pass reviews the initial extraction results and specifically targets: (1) entities referred to by pronouns, (2) omitted subjects, (3) implicit causal relationships, and (4) temporal expressions. The results are merged and deduplicated, improving extraction recall by capturing nuanced information.
Linking via Vector Similarity.
Upon extraction, each new object receives an embedding computed by a sentence encoder :
| (3) |
We establish graph edges by computing pairwise cosine similarity:
| (4) |
Edges are created according to an enhanced set of rules: (1) Reference edges if or if strong keyword overlap exists, and (2) Causal edges for specific type pairs if similarity exceeds and temporal constraints are satisfied. Additionally, (3) Temporal-heuristic causal edges are established for recent KeyFacts or Reminders influencing subsequent Decisions, irrespective of semantic similarity. This multi-faceted approach addresses limitations of pure semantic linking in capturing complex causal dependencies.
3.3 Adaptive Injection
When generating a response to query , CogCanvas retrieves and injects relevant artifacts through a multi-stage pipeline.
Hybrid Retrieval with Adaptive Top-k.
We employ a Hybrid Retrieval strategy that combines semantic similarity with lexical keyword matching. We compute the query embedding and a keyword score for each canvas object. These are fused to generate a final relevance score.
Critically, we use adaptive top-k selection based on question complexity: multi-hop questions (containing causal indicators like “because”, “after”, “why did”) retrieve objects; temporal questions (“when”, “how long”) retrieve ; simple factual questions use . This allocates more context to complex queries while avoiding noise for simple ones.
Two-Stage Retrieval with Reranking.
To improve precision, we employ a two-stage retrieval process: (1) coarse retrieval fetches top-20 candidates using the hybrid scorer, then (2) a neural reranker (BGE-reranker) re-scores candidates based on query-document relevance. The top- objects after reranking form the final candidate set .
Given a token budget , we greedily select objects from in score order until the budget is exhausted:
| (5) |
The complete injection pipeline operates transparently: from the LLM’s perspective, relevant context simply appears in the prompt, requiring no explicit memory management operations. Furthermore, the final stage incorporates Reasoning-aware Prompting, guiding the LLM to synthesize causal explanations from the retrieved artifacts, even if direct graph links are absent.
4 Experiments
We evaluate CogCanvas on a controlled information retention benchmark designed to measure how well different context management strategies preserve factual details under compression.
4.1 Experimental Setup
Benchmark Design.
We construct synthetic multi-turn conversations in which specific facts are “planted” at designated turns. Each planted fact belongs to one of four categories: KeyFact, Decision, Reminder, and Insight. We employ two variants of this benchmark:
-
•
Standard (): 50 turns per conversation, moderate information density. Compression occurs at turn 40. Evaluates single-hop recall.
-
•
Multi-hop Reasoning (): Based on the standard conversations, this benchmark features questions requiring causal or impact-based reasoning across multiple artifacts (e.g., "Why was X decided?", "What did Y affect?"). Evaluates the system’s ability to connect related facts.
Evaluation Metrics.
For the standard benchmark:
-
•
Recall Rate: Fraction of planted facts successfully retrieved (fuzzy match score 80%)
-
•
Exact Match Rate: Fraction where the answer contains the ground truth verbatim
For the multi-hop reasoning benchmark:
-
•
Keyword Coverage: Percentage of ground truth keywords present in the generated answer.
-
•
Pass Rate: Percentage of questions where keyword coverage is 80%.
-
•
Causal Coverage/Impact Coverage: Keyword coverage specifically for causal/impact questions.
Baselines.
We compare against both standard approaches and memory-augmented systems. This design choice reflects our focus on training-free methods; heavily-optimized approaches like EverMemOS [evermemos2025] and EMem [emem2024] represent a different design space and are discussed in Related Work.
-
•
Truncation: Retain only the most recent 5 turns after compression.
-
•
Summarization: Use GPT-4o-mini to compress conversation history into a summary, retaining recent 5 turns verbatim. This baseline captures MemGPT’s [packer2023memgpt] core hierarchical memory mechanism.
-
•
RAG: Naive chunking (1000 chars) with overlapping windows, embedded and stored in a vector database. Top-3 chunks retrieved via semantic similarity.
-
•
GraphRAG: We include the official Microsoft GraphRAG implementation [edge2024graphrag] as a graph-based baseline. GraphRAG constructs a knowledge graph via entity extraction and community detection, then generates hierarchical community summaries for global queries. Our experiments use the default configuration with local search mode (chunk size=800, overlap=100, entity types: person/technology/decision/fact/organization/concept, max_gleanings=1, community_level=2). We did not tune these parameters for conversational memory, which may underestimate GraphRAG’s potential on this task—see Limitations for discussion.
Note on Letta (MemGPT).
We attempted to include Letta (the production evolution of MemGPT [packer2023memgpt]) as a direct baseline. However, several technical barriers prevented controlled comparison:
-
1.
Code availability: Letta’s LoCoMo evaluation code from the archived letta-leaderboard repository has been migrated to letta-evals, which does not currently support LoCoMo (GitHub issue #3115222
[https://github.com/letta-ai/letta/issues/3115](https://github.com/letta-ai/letta/issues/3115)). -
2.
Infrastructure requirements: Letta requires PostgreSQL database and Docker environment for persistent memory management, introducing non-deterministic factors (database state, API rate limiting) that complicate reproducible benchmarking.
-
3.
Architectural divergence: Letta’s filesystem-based approach (storing conversations as files with semantic search) represents a fundamentally different paradigm from our stateless artifact extraction, making direct feature-level comparison less meaningful.
Nevertheless, we reference Letta’s official LoCoMo result (74.0% with GPT-4o mini [letta2024memory]) as an upper bound for stateful, database-backed systems in our discussion (§[4.7.1](https://arxiv.org/html/2601.00821v2#S4.SS7.SSS1)).
4.2 Main Results (Standard)
| Method | Recall | Exact | Cmplx. |
|---|---|---|---|
| Native | 12.5% | 7.0% | Low |
| Summarization | 19.0% | 14.0% | Low |
| GraphRAG | 83.5% | 70.0% | High |
| RAG (k=10) | 93.5% | 89.5% | Low |
| CogCanvas | 97.5% | 93.0% | Low |
| vs. RAG | +4.0pp | +3.5pp | - |
| vs. Summ. | +78.5pp | +79.0pp | - |
Table [2](https://arxiv.org/html/2601.00821v2#S4.T2) presents the results for the standard benchmark. CogCanvas achieves a recall rate of 97.5%, outperforming all baselines. The advantage is particularly striking compared to summarization (19.0%) with a +78.5pp improvement, demonstrating the catastrophic information loss inherent in lossy compression. Against retrieval-augmented approaches, CogCanvas beats RAG (93.5%) by 4.0pp in recall with a +3.5pp improvement in exact match. This demonstrates that structured extraction with graph-based relationships provides stronger retention than naive chunking. Figure [2](https://arxiv.org/html/2601.00821v2#S4.F2) visualizes these comparisons.
4.3 Multi-hop Reasoning Results
| Method | Pass | KW | Causal | Impact |
| Summarization | 0.0% | 42.5% | 48.3% | 35.8% |
| GraphRAG | 40.0% | 64.8% | 62.5% | 67.0% |
| RAG | 55.5% | 74.8% | 68.8% | 79.5% |
| CogCanvas | 81.0% | 90.2% | 87.5% | 92.6% |
| GraphRAG | +41.0pp | +25.4pp | +25.0pp | +25.6pp |
| RAG | +25.5pp | +15.4pp | +18.7pp | +13.1pp |
Table [3](https://arxiv.org/html/2601.00821v2#S4.T3) and Figure [3](https://arxiv.org/html/2601.00821v2#S4.F3) present the results for the multi-hop reasoning benchmark. CogCanvas achieves a pass rate of 81.0%, demonstrating a decisive improvement over existing methods. Summarization completely fails on this task (0.0% pass rate), confirming that lossy compression cannot preserve the causal reasoning chains required for multi-hop questions. Among retrieval-based methods, RAG achieves 55.5% pass rate, while GraphRAG [edge2024graphrag] achieves 40.0% pass rate—though its community summarization approach struggles with fine-grained causal attribution. CogCanvas outperforms all baselines decisively: +41.0pp over GraphRAG and +25.5pp over RAG, demonstrating that our artifact-centric approach with verbatim preservation and temporal-aware graph construction provides superior grounding for multi-hop reasoning. The gap is consistent across all metrics: 90.2% keyword coverage (+25.4pp vs. GraphRAG), 87.5% causal coverage (+25.0pp), and 92.6% impact coverage (+25.6pp).
4.4 Evaluation on Real-World Dataset (LoCoMo)
To validate CogCanvas’s performance on real-world data, we evaluated it on the LoCoMo benchmark (ACL 2024), a dataset specifically designed for long-context memory and multi-hop reasoning. Unlike synthetic data, LoCoMo features natural conversational noise and complex information dependencies spanning over 300 turns.
| Method | All | 1-hop | Temp. | M-hop |
| Native | 4.9% | 5.3% | 0.3% | 18.8% |
| Summ. | 5.6% | 5.3% | 0.6% | 22.9% |
| GraphRAG | 10.6% | 12.8% | 3.1% | 29.2% |
| RAG (k=10) | 24.6% | 24.6% | 12.1% | 40.6% |
| CogCanvas | 32.4% | 26.6% | 32.7% | 41.7% |
| vs. RAG | +7.8pp | +2.0pp | +20.6pp | +1.1pp |
Table [4](https://arxiv.org/html/2601.00821v2#S4.T4) summarizes the results using binary LLM-as-judge evaluation on official LoCoMo categories (single-hop, temporal, multi-hop). CogCanvas achieves the highest overall accuracy among training-free methods (32.4%), outperforming RAG (24.6%) by +7.8pp, while demonstrating advantages across all question types.
The most striking result is on Temporal questions: CogCanvas achieves 32.7% compared to 12.1% (RAG), representing a +20.6pp improvement. This substantial gap demonstrates that our verbatim artifact extraction effectively preserves time-sensitive information that chunk-based retrieval systematically loses. On Multi-hop questions, CogCanvas leads with 41.7% vs. 40.6% (RAG), a +1.1pp advantage, showing that graph-based expansion successfully connects related artifacts across conversation turns.
On Single-hop retrieval, CogCanvas also leads (26.6% vs. 24.6%), demonstrating that our enhanced retrieval parameters improve recall without sacrificing precision. The key insight is that CogCanvas provides consistent advantages across all question types, with particularly decisive gains on temporal reasoning (+20.6pp) where long-context memory matters most.
Discussion. This pattern validates our core hypothesis: structured artifact preservation provides decisive advantages for complex reasoning scenarios. CogCanvas’s overall lead (32.4% vs. RAG 24.6%) confirms that our approach excels across realistic long-context applications. Both retrieval-based methods substantially outperform GraphRAG (10.6%) and summarization (5.6%), confirming that retrieval-based approaches dominate lossy compression for long-context memory.
4.5 Case Study: Verbatim Preservation
The exact match gap reveals a qualitative difference in how methods handle nuanced constraints. Consider a Reminder planted in turn 3: “use type hints everywhere.” When queried about coding style preferences after compression, the two methods respond differently:
Summarization: “The user prefers a consistent code style with type hints.” Exact: ✗
CogCanvas: “please use type hints everywhere” Exact: ✓
The summarizer correctly identifies that type hints are relevant but loses the critical qualifier “everywhere.” CogCanvas preserves the exact constraint by maintaining the verbatim quote as a grounded artifact.
4.6 Real-World Case Study: GitHub RFC Discussion
To validate CogCanvas’s applicability beyond synthetic benchmarks, we applied it to a real-world GitHub discussion: the Next.js Deployment Adapters API RFC333[https://github.com/vercel/next.js/discussions/77740](https://github.com/vercel/next.js/discussions/77740), comprising 68 comments from stakeholders including Vercel, Netlify, Deno Deploy, and Cloudflare.
CogCanvas extracted 45 cognitive artifacts (15 key facts, 10 decisions, 14 todos, 5 insights, 1 reminder). The extracted graph successfully captured critical decisions (“No backport to 14.x”), cross-stakeholder insights (“Deno’s serverless architecture would benefit from a unified entry”), and scattered action items. When evaluated on question-answering tasks, CogCanvas retrieved precise technical details (e.g., “fallbackID references STATIC_FILE (Turn 8)”) that summarization failed to preserve. Full results are provided in Appendix [D](https://arxiv.org/html/2601.00821v2#A4).
4.7 Discussion
The experimental results reveal a nuanced picture that refines our initial hypothesis. We organize our discussion around the fundamental trade-off between stateful and stateless memory architectures.
4.7.1 Stateful vs. Stateless Memory: A Trade-off Analysis
Our results reveal a fundamental trade-off between stateful and stateless memory architectures for long conversations:
Stateful Systems (e.g., Letta, EverMemOS).
These methods maintain persistent memory state across interactions, typically backed by databases or specialized storage. Letta achieves 74.0% on LoCoMo [letta2024memory], while EverMemOS reaches 92.3% [evermemos2025]. Their advantages include:
-
•
Superior recall: Persistent storage enables exhaustive memory retention without context length constraints.
-
•
Incremental learning: Agents can accumulate knowledge over extended sessions.
However, these benefits come at significant cost:
-
•
Infrastructure overhead: Requires databases (PostgreSQL), containerization (Docker), and server management.
-
•
Training requirements: Top performers like EverMemOS rely on learned compression models.
-
•
Deployment complexity: Non-trivial setup prevents rapid prototyping and integration into existing systems.
Stateless Systems (CogCanvas).
Our approach treats each query independently, extracting artifacts on-the-fly without persistent state. We achieve 32.4% on LoCoMo overall, outperforming all training-free baselines:
-
•
+7.8pp overall vs. RAG: Best training-free performance (32.4% vs. 24.6%).
-
•
+20.6pp on temporal queries: Graph-based retrieval with time-awareness outperforms RAG (32.7% vs. 12.1%).
-
•
+1.1pp on multi-hop reasoning: Verbatim grounding preserves logical chains that summarization destroys (41.7% vs. 40.6%).
-
•
Zero infrastructure: Drop-in integration via standard LLM APIs.
-
•
Training-free: No model fine-tuning or data collection.
When to Use Each Approach.
Our findings suggest:
-
•
Letta/stateful systems: Production deployments with long-lived agents, where infrastructure investment is justified by sustained interactions.
-
•
CogCanvas/stateless systems: Rapid prototyping, research experiments, or applications requiring portability and simplicity, especially when queries involve temporal reasoning or causal chains.
The 41.6pp gap between CogCanvas (32.4%) and Letta (74.0%) quantifies the “cost of simplicity”—a trade-off that may be acceptable in resource-constrained or exploratory settings where immediate deployability without infrastructure investment is prioritized.
4.7.2 Task Complexity Determines Optimal Approach
CogCanvas achieves the highest overall accuracy (32.4%), demonstrating that structured artifact preservation provides general benefits across all question types. CogCanvas leads on single-hop retrieval (26.6% vs. 24.6%), temporal questions (32.7% vs. 12.1%, +20.6pp), and multi-hop questions (41.7% vs. 40.6%, +1.1pp). This suggests that enhanced retrieval with structured memory provides consistent advantages—connecting constraints to decisions, tracking temporal sequences, and synthesizing information across conversation segments.
Artifacts vs. Entities. The performance gap between CogCanvas and GraphRAG [edge2024graphrag] remains instructive. GraphRAG (10.6%) struggles on conversational memory despite its sophisticated community detection, because its summarization pipeline “compresses away” the fine-grained details that memory tasks require. CogCanvas succeeds precisely because it treats the verbatim artifact as the atomic unit of memory, preserving the “connective tissue” of reasoning that summarization discards.
Practical Trade-offs. CogCanvas achieves overall leadership (32.4%) with consistent advantages across all question types. For applications requiring temporal reasoning (“when did X happen?”) or multi-hop inference (“why was X decided?”)—common in project planning, technical support, and collaborative work—CogCanvas offers substantial benefits. The +20.6pp temporal advantage is particularly significant, as temporal reasoning represents the hardest aspect of long-context memory where all non-structured methods fail catastrophically (0.3%–12.1%).
Toward Hybrid Strategies. Our results suggest a practical deployment pattern: query-complexity routing. Simple queries containing direct entity references (“What is X’s email?”) can be routed to efficient RAG retrieval, while queries with temporal markers (“when,” “before,” “after”), causal indicators (“why,” “because,” “led to”), or multi-entity references can be routed to CogCanvas. A lightweight classifier—even regex-based heuristics—could achieve this routing with minimal overhead. This hybrid approach would combine RAG’s efficiency on simple lookups with CogCanvas’s strength on complex reasoning, potentially achieving higher overall accuracy than either method alone.
Target Applications. CogCanvas is particularly suited for domains where temporal and causal reasoning are critical: (1) project planning conversations tracking decisions, deadlines, and dependencies; (2) technical support sessions where constraints accumulate across turns; (3) collaborative coding where preferences and requirements must be faithfully preserved; (4) multi-stakeholder discussions (as demonstrated in our GitHub RFC case study) where cross-party decisions need structured tracking.
Exact preservation matters. The substantial exact match advantage on controlled benchmarks (93.0% vs. 89.5% for RAG) demonstrates that CogCanvas systematically preserves specifics that other approaches lose. For applications requiring faithful constraint adherence (coding assistants, technical support), this difference is practically significant.
4.8 Error Analysis
Analyzing 3,121 missing keywords across failed LoCoMo questions reveals three primary failure modes: (1) Extraction gaps (78.8%): the LLM extractor fails to identify certain facts as salient (e.g., “Caroline is single” not extracted as a key_fact); (2) Temporal blindness (14.9%): dates mentioned in passing (“last Tuesday,” “May 2023”) are not preserved as structured temporal attributes; (3) Reasoning chain breaks (6.4%): multi-hop questions requiring inference across multiple artifacts fail when intermediate links are missing.
What Gets Missed? Qualitative analysis of extraction failures reveals systematic patterns in what the LLM extractor overlooks:
-
•
Implicit personal attributes (e.g., “Caroline is single,” relationship status inferred from context rather than stated directly)—the extractor prioritizes explicit statements over implicit facts.
-
•
Emotional preferences (e.g., “she felt anxious about…”)—affective states are often not recognized as KeyFacts worth preserving.
-
•
Casual temporal references (“last Tuesday,” “a few months ago”)—relative time expressions are harder to anchor than absolute dates.
-
•
Negations and constraints (“does NOT want X”)—negative preferences are sometimes missed or inverted during extraction.
These patterns suggest that extraction prompts could be improved by explicitly instructing the LLM to attend to implicit attributes, emotional states, and negative constraints.
Gleaning contribution. Our two-pass gleaning strategy (Section 3.2) partially addresses these gaps by explicitly targeting omitted subjects and implicit relationships in the second pass. However, our ablation study reveals that gleaning provides minimal benefit on LoCoMo, likely because LoCoMo’s explicit conversational style reduces the need for implicit entity resolution. Gleaning may be more beneficial for informal dialogue with heavy pronoun usage.
The high proportion of temporal markers (14.9%) directly explains why temporal questions remain challenging (32.7% accuracy) despite substantial improvements over baselines (0.3%–12.1%). This suggests targeted improvements: explicit date/time extraction, temporal attribute modeling in artifacts, and retrieval strategies that prioritize temporal proximity for time-sensitive queries.
Performance by question type. Single-hop questions achieve 26.6% accuracy, multi-hop questions 41.7%, while temporal questions achieve 32.7%. Notably, our verbatim-grounded extraction substantially improves temporal reasoning compared to RAG (32.7% vs. 12.1%, +20.6pp), though the absolute performance remains limited due to extraction gaps in temporal markers.
4.9 Why Temporal Works
The most striking result from our LoCoMo evaluation is CogCanvas’s substantial performance gain on temporal questions, achieving 32.7% accuracy compared to 12.1% for RAG and 3.1% for GraphRAG—a +20.6pp improvement over the strongest baseline. This section delves into the mechanisms underlying this significant improvement.
Failure Cases: GraphRAG vs. CogCanvas.
To illustrate how CogCanvas effectively captures temporal information where baselines fail, we examine specific instances from the LoCoMo benchmark. Consider a question requiring knowledge of a specific date associated with an event.
-
•
Example 1: When did Caroline go to the LGBTQ support group?
-
–
GraphRAG’s Output: GraphRAG failed to provide a specific date, stating, “the specific date of her attendance is not provided in the data.” While it recognized the event, the crucial temporal detail was lost during its summarization process.
-
–
CogCanvas’s Success: CogCanvas accurately retrieved the date, providing “May 7, 2023.” This was achieved through verbatim artifact extraction that preserved the exact timestamp as a KeyFact, enabling direct retrieval of granular temporal information that summarization-based methods discard.
-
–
-
•
Example 2: When did Melanie paint a sunrise?
-
–
GraphRAG’s Output: GraphRAG could only offer a vague temporal reference, stating, “the specific date… is not provided… mentioned that she created a painting… last year.” The exact date was generalized away.
-
–
CogCanvas’s Success: CogCanvas precisely identified the date as “8 May 2022.” The verbatim-grounded extraction preserved the exact date as a structured artifact, enabling direct retrieval—highlighting CogCanvas’s superior capability in retaining time-sensitive facts that compression-based methods lose.
-
–
Ablation Study: Component Contributions.
To quantify the individual contributions of CogCanvas’s components, we conduct a systematic ablation study by removing each component from the full system and measuring the performance drop.
| Configuration | All | 1-hop | Temp. | M-hop |
| Full System | 32.4% | 26.6% | 32.7% | 41.7% |
| – Gleaning | 30.7% | 26.6% | 28.7% | 45.8% |
| – Graph Expansion | 25.8% | 19.5% | 29.0% | 33.3% |
| – Reranking | 20.9% | 16.7% | 23.1% | 26.0% |
| Minimal (Graph only) | 14.3% | 11.7% | 13.7% | 24.0% |
Key findings:
-
•
Reranking is the largest contributor. Removing BGE reranking causes a –11.5pp drop (32.4% 20.9%), making it the most impactful component. Reranking improves precision by scoring retrieval candidates with semantic relevance, particularly benefiting multi-hop questions (41.7% 26.0%, –15.7pp).
-
•
Graph expansion provides substantial gains. Removing graph expansion reduces overall accuracy by –6.6pp (32.4% 25.8%), with the largest impact on multi-hop questions (–8.4pp). This confirms that structural relationships between artifacts enable discovering connected information across turns.
-
•
Gleaning shows minimal impact on LoCoMo. Removing the two-pass extraction strategy slightly improves overall accuracy (+1.7pp: 30.7% vs. 32.4%), suggesting that LoCoMo’s explicit conversational style reduces the need for implicit entity resolution. Gleaning may be more beneficial for informal dialogue with heavy pronoun usage.
-
•
Combined system effects. The full system (32.4%) improves +18.1pp over the minimal baseline (14.3%), demonstrating strong synergy between components.
-
•
Temporal advantage stems from extraction. CogCanvas’s temporal advantage over baselines (32.7% vs. RAG’s 12.1%, +20.6pp) stems primarily from verbatim artifact extraction preserving explicit timestamps, rather than from temporal heuristic edges. The extraction mechanism ensures time-sensitive information is retained as grounded artifacts.
Retrieval Quality Analysis.
To verify that graph expansion improves retrieval quality rather than merely leveraging LLM reasoning capabilities, we conduct a retrieval-only evaluation that measures whether the retrieved context contains ground-truth keywords—without invoking the LLM for answer generation.
| Config. | Overall | 1-hop | Temp. | M-hop |
| Full System | 71.8% | 87.3% | 63.2% | 55.0% |
| – Graph Exp. | 25.8% | 32.3% | 20.5% | 24.7% |
| Improvement | +46.0pp | +55.0pp | +42.7pp | +30.3pp |
As shown in Table [6](https://arxiv.org/html/2601.00821v2#S4.T6), graph expansion increases retrieval recall from 25.8% to 71.8% (+46.0pp). This confirms that the performance gains in Table [5](https://arxiv.org/html/2601.00821v2#S4.T5) stem from improved context retrieval, not from LLM answering ability. The graph structure enables retrieving related artifacts that would otherwise be missed by pure semantic similarity matching.
Why Baselines Fall Short on Temporal Reasoning.
The consistently low performance of baselines on temporal questions (RAG: 12.1%, GraphRAG: 3.1%, Summarization: 0.6%) can be attributed to several factors:
-
•
RAG (Chunk-based): Standard RAG systems typically chunk conversations or documents into fixed-size segments. Temporal information, such as specific dates or sequences of events, can easily be fragmented across chunk boundaries, making it difficult for retrieval to reconstruct the full temporal context. The lack of explicit temporal indexing or relational understanding means that chunks are retrieved based on semantic similarity, which often overlooks the critical temporal dimension.
-
•
GraphRAG (Community Summarization): While GraphRAG constructs a sophisticated knowledge graph, its reliance on community detection and summarization for higher-level queries often leads to the generalization of information. Specific dates, times, or precise event sequences are frequently summarized away or absorbed into broader thematic summaries, losing the granular temporal detail necessary for answering precise temporal questions. The emphasis on conceptual relationships can inadvertently obscure the temporal ordering of events.
-
•
Summarization: Directly compressing conversation history into summaries fundamentally operates on a lossy principle. Temporal details are often considered less "important" than core facts or decisions by the summarization LLM, leading to their omission or vague representation. Iterative summarization, in particular, exacerbates this issue, as temporal markers are progressively lost with each compression pass, leading to recursive information decay for time-sensitive data.
In contrast, CogCanvas’s verbatim-grounded artifact extraction directly addresses these limitations by preserving explicit temporal markers as structured KeyFacts. Our ablation study (Table [5](https://arxiv.org/html/2601.00821v2#S4.T5)) confirms that the temporal advantage (32.7% vs. RAG 12.1%, +20.6pp) stems primarily from this extraction mechanism, which ensures time-sensitive information is retained as grounded artifacts. The key insight is that preserving temporal information during extraction matters more than connecting it through graph structure.
5 Conclusion
We have presented CogCanvas, a framework for maintaining compression-tolerant cognitive artifacts in long LLM conversations. Our approach draws inspiration from the whiteboard effect: in collaborative human work, teams maintain shared artifacts that serve as external anchors for distributed cognition [hutchins1995cognition, clark1998extended]. These artifacts persist independently of any individual’s memory, can be consulted when relevant, and preserve exact formulations rather than paraphrased approximations.
Our evaluation on the LoCoMo benchmark (all 10 conversations from the ACL 2024 release) demonstrates that CogCanvas achieves the highest overall accuracy among training-free methods (32.4%), outperforming RAG (24.6%) by +7.8pp. CogCanvas leads across all question types: +20.6pp on temporal reasoning (32.7% vs. 12.1%), +1.1pp on multi-hop questions (41.7% vs. 40.6%), and +2.0pp on single-hop retrieval (26.6% vs. 24.6%). This validates our core hypothesis: structured artifact preservation with enhanced retrieval provides consistent advantages for long-context memory tasks.
While stateful systems like Letta [letta2024memory] achieve higher absolute accuracy (74.0%) through persistent memory infrastructure, our work demonstrates that training-free, stateless artifact extraction can provide a competitive alternative for scenarios prioritizing deployment simplicity, particularly excelling in temporal and multi-hop reasoning tasks.
We release our code and benchmarks to facilitate future work on compression-tolerant memory systems.444[https://github.com/tao-hpu/cog-canvas](https://github.com/tao-hpu/cog-canvas) Future directions include adaptive threshold learning, cross-lingual artifact extraction, and hybrid strategies that combine structured artifacts with selective summarization. The whiteboard effect points toward a general principle: for complex reasoning over long conversations, preserving structured cognitive artifacts outperforms both lossy compression and simple retrieval.
6 Limitations
Design trade-offs. CogCanvas’s training-free design prioritizes immediate deployability over maximum accuracy. Our 32.4% overall accuracy on LoCoMo outperforms RAG (24.6%) by +7.8pp, with both substantially outperforming GraphRAG (10.6%) and summarization (5.6%). All training-free methods remain below heavily-optimized fine-tuned approaches (EverMemOS: 92.3%, EMem: 78%). This reflects our deliberate choice: we optimize for accessibility (any LLM backend, no training required) rather than peak performance.
GraphRAG baseline configuration. Our GraphRAG experiments use the official Microsoft implementation with default parameters (local search, chunk size=800, community_level=2). We did not tune entity extraction prompts, chunk strategies, or community detection for conversational memory. GraphRAG’s low performance (10.6%) may partially reflect suboptimal configuration rather than fundamental limitations. However, our core finding—that verbatim grounding outperforms lossy summarization—is validated by comparison with the Summarization baseline (5.6%), which shares GraphRAG’s compression-based philosophy.
Task-oriented dialogue bias. Our artifact taxonomy (Decisions, Facts, Todos) is optimized for task-oriented conversations (project planning, technical discussions, customer support). Informal chit-chat or emotionally-driven dialogue may contain implicit preferences that resist structured extraction.
Threshold sensitivity. Graph construction relies on fixed similarity thresholds (, ) that may require adjustment for different domains or embedding models.
English-only evaluation. All experiments were conducted on English conversations. Cross-lingual artifact extraction remains untested.
Synthetic benchmark bias. Our controlled benchmarks use planted facts with clear categorical boundaries, which may overestimate performance on real-world conversations where information boundaries are ambiguous.
Extreme context scenarios. While we conducted preliminary evaluations under extreme compression scenarios (e.g., 54k tokens with 27:1 compression ratios), these stress-test conditions, though informative, may not reflect typical deployment contexts. Our main evaluations focus on more realistic conversation lengths where CogCanvas demonstrates clear advantages.
Enhanced retrieval parameters. CogCanvas uses increased retrieval parameters (top_k=20, graph_hops=4) to achieve consistent advantages across all question types. This may increase computational overhead compared to simpler RAG configurations, though it remains modest compared to fine-tuning pipelines.
Extraction quality ceiling. CogCanvas performance is bounded by extraction quality—if the LLM extractor fails to identify a fact as salient, it cannot be retrieved later.
Computational overhead. CogCanvas requires an extraction LLM call per turn plus embedding computation, though this remains modest compared to fine-tuning pipelines.
Despite these limitations, CogCanvas fills a practical gap: a training-free, verbatim-grounded memory system that significantly outperforms naive approaches while remaining immediately deployable.
7 Future Work
Several directions could extend this work:
Adaptive thresholds. The current fixed similarity thresholds for graph construction could be replaced with learned or self-tuning mechanisms that adapt to domain-specific embedding distributions.
Further optimization. While CogCanvas now leads across all question types (temporal: +20.6pp, multi-hop: +1.1pp, single-hop: +2.0pp vs. RAG), future work could explore adaptive retrieval parameters that dynamically adjust based on query complexity.
Broader evaluation. Extending experiments to additional dialogue benchmarks (e.g., MSC) and non-English languages would strengthen generalization claims.
Extraction analysis. A systematic error analysis of artifact extraction failures—categorizing missed facts by type, ambiguity, and conversation context—could inform targeted improvements to the extraction prompt or architecture.
Hybrid approaches. Combining CogCanvas’s training-free verbatim grounding with lightweight fine-tuning (e.g., adapter layers for extraction) may offer a middle ground between maximum accessibility and maximum accuracy.
Appendix A Reproducibility Details
A.1 Prompt Templates
To ensure reproducibility, we provide the full prompts used for artifact extraction and reasoning-aware generation.
Artifact Extraction Prompt.
The extraction LLM identifies cognitive artifacts with types: decision, todo, key_fact, reminder, insight. Each artifact must include a verbatim “citation” field from the original dialogue.
Reasoning-Aware (CoT) Prompt.
The generation prompt instructs the LLM to analyze retrieved nodes, infer causal relationships between constraints and decisions, and synthesize explanations.
A.2 Hyperparameters
Models: GPT-4o-mini (extraction), text-embedding-3-small (embeddings). Retrieval: Top-15, max 2000 tokens. Temperature: 0.1 (extraction), 0.0 (generation).
Threshold Selection.
We tuned similarity thresholds on a held-out development set of 5 conversations (disjoint from evaluation data):
-
•
: Grid search over selected as optimal for balancing precision and recall in reference edge creation.
-
•
: Set to to allow slightly looser causal connections while maintaining semantic coherence.
Sensitivity analysis (Appendix [F](https://arxiv.org/html/2601.00821v2#A6)) confirms robustness: performance varies only 5pp across the tested range (57.5%–67.5%), indicating the method is not overly sensitive to threshold selection.
Appendix B Token Efficiency Analysis
Table [7](https://arxiv.org/html/2601.00821v2#A2.T7) estimates context tokens per query. CogCanvas achieves the lowest consumption (1,250 tokens) while preserving verbatim citations, compared to Full Context (10,000), GraphRAG (3,000), Summarization (2,000), and RAG (1,500).
| Method | Strategy | Tokens |
|---|---|---|
| Full Context | No compression | 10,000 |
| GraphRAG | Community summaries | 3,000 |
| Summarization | Compress to summary | 2,000 |
| RAG (top-5) | Retrieve 5 chunks | 1,500 |
| CogCanvas | Artifacts + expansion | 1,250 |
CogCanvas achieves the lowest per-query token consumption through selective artifact retrieval with graph expansion.
Appendix C Case Study: Qualitative Analysis
Multi-hop Success.
Q: “Would Melanie prefer a national park or theme park?” CogCanvas correctly answered “national park” by retrieving artifacts about her outdoor activities and nature preferences (80% keyword overlap).
Temporal Success.
Q: “When did Caroline attend the LGBTQ support group?” CogCanvas correctly retrieved the temporal context through our verbatim-grounded extraction, achieving 32.7% temporal accuracy—substantially outperforming RAG (12.1%) and GraphRAG (3.1%).
Appendix D GitHub RFC Case Study (Full Version)
D.1 Extraction Results
CogCanvas extracted 45 cognitive artifacts from the Next.js Deployment Adapters API RFC discussion, distributed as follows: 15 key facts, 10 decisions, 14 todos, 5 insights, and 1 reminder. Figure [5](https://arxiv.org/html/2601.00821v2#A4.F5) visualizes a subgraph of the resulting knowledge structure.
D.2 Qualitative Findings
The extracted graph reveals several patterns that validate CogCanvas’s design:
-
•
Decision tracking: Critical decisions such as “No backport to 14.x” and “Vercel will dogfood via their own adapter” are captured with their grounding quotes.
-
•
Cross-stakeholder insights: The system identified platform-specific concerns (e.g., “Deno’s serverless architecture would benefit from a unified entry”) that span multiple comments.
-
•
Todo aggregation: Action items scattered across the discussion (“Document routing behavior specification”, “Finalize PPR support for non-Vercel platforms”) are consolidated into a queryable structure.
This case study demonstrates that CogCanvas’s artifact extraction generalizes beyond controlled benchmarks to complex, multi-party technical discussions where structured knowledge capture provides practical value.
D.3 Retrieval & Injection Analysis
Beyond extraction, we evaluated the practical utility of the constructed graph for answering complex questions that require retrieving details from early conversation turns. While both methods performed well on high-level inquiries (e.g., Q1: “What is the main purpose of this RFC?”), significant performance divergence emerged on questions requiring retrieval of specific technical details, reasoning chains, or stakeholder preferences. We compared CogCanvas (Retrieval+Injection) against a Summarization baseline on three such discriminative questions. Table [8](https://arxiv.org/html/2601.00821v2#A4.T8) presents the qualitative comparison.
| Q2: How does fallbackID work? |
|---|
| Summ: “No specific details on fallbackID.” |
| Ours: “References STATIC_FILE (Turn 8).” |
| Q3: Why no backport to 14.x? |
| Summ: “Likely due to complexity.” |
| Ours: “Big refactors (Turn 15), breaks compat (Turn 18).” |
| Q5: Deno’s preference? |
| Summ: “No specific preference mentioned.” |
| Ours: “Singular entrypoint (Turn 42) for serverless.” |
The results highlight CogCanvas’s advantage in precision and completeness. While summarization captures high-level decisions, it fails to retain specific constraints (e.g., “fallbackID references STATIC_FILE”) or complex reasoning chains (e.g., specific reasons for rejecting backports). CogCanvas, by retrieving the exact artifact with its context, provides answers that are both factually richer and grounded in specific turns.
Appendix E RAG Baseline Sensitivity
Table [9](https://arxiv.org/html/2601.00821v2#A5.T9) shows RAG performance across configurations. The best configuration (RAG-default, 512 chunks) achieves 55.5%, demonstrating that while chunk-based retrieval can capture relevant information, CogCanvas’s structured extraction provides a decisive advantage (+25.5pp), confirming the value of artifact-centric memory organization.
| Config | Chunk | Top- | Overlap | Pass |
| RAG-small | 256 | 5 | 50 | 7.5% |
| RAG-default | 512 | 5 | 100 | 55.5% |
| RAG-large | 1024 | 5 | 200 | 2.5% |
| RAG-topk10 | 512 | 10 | 100 | 0.0% |
| CogCanvas | – | – | – | 81.0% |
Appendix F Threshold Sensitivity
Table [10](https://arxiv.org/html/2601.00821v2#A6.T10) shows CogCanvas is robust to threshold selection: performance ranges only 10pp (57.5%–67.5%) across configurations.
| Config | Ref. | Causal | Pass |
|---|---|---|---|
| Low | 0.3 | 0.25 | 62.5% |
| Default | 0.5 | 0.45 | 67.5% |
| High | 0.7 | 0.6 | 60.0% |
| Very High | 0.8 | 0.7 | 57.5% |
Appendix G Extended Related Work
This section provides detailed discussion of related work summarized in Section 2.
G.1 Context Window Management
The finite context window of transformer-based LLMs has motivated extensive research into efficient context utilization. Sparse attention mechanisms [child2019sparsetransformer, beltagy2020longformer] reduce the quadratic complexity of self-attention, enabling longer sequences but not fundamentally solving the capacity constraint. Retrieval-augmented approaches [borgeaud2022retro, izacard2022atlas] maintain external datastores that are queried at inference time, yet these systems typically assume static document collections rather than dynamically evolving conversational state. Recent work on context extension through positional interpolation [chen2023extending] pushes the practical context limit but does not eliminate the fundamental trade-off between context length and computational cost. Our approach is orthogonal to these efforts: rather than extending raw context capacity, we focus on what to preserve when compression becomes necessary.
G.2 Memory-Augmented Language Models
MemGPT [packer2023memgpt] pioneered a hierarchical memory system inspired by operating system design, introducing virtual context management where LLMs perform explicit memory management operations (moving data between “fast” and “slow” memory tiers). The original MemGPT project has since evolved into Letta,555[https://letta.ai](https://letta.ai) a production-ready framework that extends the core architecture with filesystem-based memory storage, PostgreSQL persistence, and enhanced tool integration. Letta’s recent LoCoMo evaluation achieved 74.0% accuracy using GPT-4o mini [letta2024memory] by storing conversation histories as files with semantic search capabilities. While this demonstrates the power of stateful, database-backed memory systems, it requires persistent infrastructure (PostgreSQL, Docker) that introduces deployment complexity. This architectural approach represents a fundamentally different paradigm from our stateless, inference-time retrieval.
Several concurrent approaches explore alternative memory architectures. MemoryBank [zhong2024memorybank] incorporates a memory updating mechanism inspired by the Ebbinghaus Forgetting Curve, allowing selective memory preservation based on temporal decay and significance. LongMem [wang2023longmem] employs a decoupled architecture with a frozen backbone LLM as memory encoder and a side-network for retrieval, caching attention key-value pairs from previous segments. ReadAgent [lee2024readagent] takes a human-inspired approach, compressing long documents into “gist memories” while retaining the ability to look up original passages when details are needed. These methods demonstrate creative solutions to the memory challenge, though they typically require either architectural modifications or focus primarily on document comprehension rather than dynamic conversational state.
More recently, several approaches have pushed the boundaries of memory-augmented LLMs through dedicated optimization. EMem [emem2024] achieves impressive performance (78% on LoCoMo) through fine-grained Elementary Discourse Unit (EDU) segmentation and task-specific fine-tuning. Most notably, EverMemOS [evermemos2025] achieves a breakthrough 92.3% on LoCoMo through categorical memory extraction (situational context, semantics, user profiling) and MemCell atomic storage with rich metadata (timestamps, source, tags, relational links). EverMemOS represents the current state-of-the-art, demonstrating that structured memory with explicit forgetting mechanisms can even surpass full-context approaches.
These heavily-optimized approaches occupy a fundamentally different design space: they require substantial training infrastructure, domain-specific corpora, dedicated fine-tuning pipelines, or complex architectural modifications. While ideal for high-stakes deployments where maximum accuracy justifies the engineering investment, they are less suitable for practitioners who need immediate solutions without fine-tuning overhead.
CogCanvas deliberately targets a complementary niche: a training-free, plug-and-play solution that can be deployed with any LLM backend. We do not claim to match the absolute performance of heavily-optimized systems like EverMemOS or EMem; instead, we provide a practical baseline that substantially outperforms naive approaches (RAG, summarization) while remaining immediately deployable. This positions CogCanvas as a “first-line” solution for practitioners, with fine-tuned approaches available for scenarios requiring maximum accuracy.
G.3 Graph-Based Knowledge Organization
GraphRAG [edge2024graphrag] and related approaches [yasunaga2021qagnn, zhang2022greaselm] leverage graph structures to organize and retrieve knowledge. These systems excel at capturing relational information and enabling multi-hop reasoning over structured knowledge bases. However, existing graph-based methods are predominantly designed for static document collections—corpora that are processed offline and queried at inference time. The dynamic, incremental nature of conversational knowledge poses distinct challenges: artifacts must be extracted in real-time, the graph structure must evolve with each turn, and retrieval must balance recency with relevance. CogCanvas addresses these challenges through online artifact extraction and incremental graph construction.
G.4 Conversation Summarization
Summarization-based approaches [xu2021dialogueSummary, chen2021dialogsum] offer an intuitive solution to context overflow: compress older turns into concise summaries that preserve essential information within reduced token budgets. Recent work has explored hierarchical summarization [wu2021recursively], where summaries are themselves summarized as conversations extend. While effective for capturing high-level narrative flow, summarization fundamentally operates on a lossy compression principle. Our experiments reveal that even state-of-the-art LLM-based summarizers systematically lose specific details. CogCanvas sidesteps this trade-off by maintaining artifacts in their original, structured form, retrieving them verbatim when relevant.