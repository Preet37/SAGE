# Building an AI-First Tutor: Patterns and Anti-Patterns

Speaker reference for UCLA Multimodal AI Conference talk.
Pratik Mehta | April 2026

---

## The One-Line Thesis

An AI-first tutor is not a chatbot with a textbook -- it's a pipeline of specialized AI systems backed by curated knowledge.

---

## PART 1: DESIGN PRINCIPLES (What Worked)

### 1. Knowledge Before Model

The first thing we built was not a chatbot. It was a wiki.

51 topics. 466+ curated sources. 517 concepts mapped across 144 subtopics. 15 educator profiles. Before we wrote a single line of agent code, we knew *what the tutor needed to know* and *how it was organized*.

The model is the delivery mechanism, not the brain. If you swap GPT-5.2 for Claude or Llama, the tutor still knows the same things -- because the knowledge lives in the wiki, not in the weights.

**Why this matters:** Most teams start with "which model should we use?" That's the wrong first question. The right first question is: "What does our tutor need to know, and where does that knowledge come from?"

**Contrast with the other team:** They started with the model and tried to make it smart enough through prompting alone. Three months later, their tutor gives correct but generic answers because it has no curated knowledge to draw from.


### 2. Two Layers of Content, Not One

We generate two separate artifacts for every lesson:

- **Student notes** -- narrative-driven, readable, designed for humans to learn from. Analogies, code examples, comparison tables, recommended reading.
- **Reference KB** -- structured for the tutor to *consult in real time*. Teaching approaches (intuitive/technical/analogy), common misconceptions with corrections, a Socratic question bank, "show when" guidance for images and resources, key formulas and empirical results.

If you give the LLM the same content students read, it just reads it back to them. That's a textbook, not a tutor.

The reference KB is what makes the tutor Socratic. It knows *which misconceptions to probe for*. It knows *when to show a diagram* vs. when to ask a question. It has a bank of questions designed to make the student think, not just recall.

**The prompt was rewritten 3 times:**
- v1: Too constrained -- over-specified structure, every lesson looked the same
- v2: Added narrative persona (Karpathy/3Blue1Brown style) -- but too formulaic, every lesson opened with "Imagine you're..."
- v3: Relaxed prescriptions -- "write naturally, vary your openings." Tested on 5 diverse lessons. Finally got varied, high-quality output.

**Lesson:** Don't try to get the prompt right on the first attempt. Write it, generate output, evaluate, rewrite. Plan for at least three iterations.


### 3. Simple Agent Code, Complex Knowledge

The entire agent loop is 136 lines of pure Python. No framework. No LangGraph. No state machines. No annotations. Just:

```
while steps < MAX_STEPS:
    stream = await client.chat.completions.create(
        model, messages, tools, stream=True
    )
    # stream text to user
    # if tool_calls: execute tools, append results, loop
    # if stop: break
```

That's it. The model decides when to call tools. The tools are simple functions that look things up (search, curriculum, images, reference KB). The system prompt defines the behavior. The knowledge is in the wiki.

**Why no LangGraph / LangChain / CrewAI?**

Because the complexity belongs in the *knowledge*, not the *orchestration*. A multi-agent graph with routing nodes, conditional edges, and state annotations is solving the wrong problem. The hard part isn't "which agent should handle this turn" -- the hard part is "does the tutor have the right knowledge to teach this concept well?"

When you use a framework, you spend weeks debugging graph traversal, state serialization, and annotation schemas. When you use 40 lines of Python, you spend that time improving the wiki, tuning prompts, and building evals.

**The agent code hasn't changed in months. The wiki and prompts change every week.**

**Contrast with the other team:** They built elaborate multi-agent systems in LangGraph -- routing agents, planner agents, research agents, response agents. Weeks of graph architecture work. But it's all orchestrating poor-quality data. Beautiful pipes, dirty water.


### 4. Pipeline of Narrow Tasks

The content creation pipeline has 7 stages. Each stage has a focused LLM job:

1. Wiki readiness check
2. Outline generation
3. Coverage assessment (per-concept: covered / thin / missing)
4. Enrichment (search → curate → audit → download → index)
5. Content generation (student notes + reference KB)
6. Resource recommendation
7. Quality validation

Each stage is small enough that the LLM does it well. The enrichment step alone has four specialized roles: assessor, search query generator, curator, and reviewer/auditor. The curator picks the best sources; the reviewer audits the picks and promotes overlooked near-misses.

**Why not one big "generate a course" prompt?**

Because a single prompt with 15 requirements reliably delivers on about 8 of them. The model drops the constraints it finds hardest. By splitting into focused stages, each stage has 2-3 requirements and delivers on all of them.

**Checkpointing:** Every stage saves its output. You can `--resume-from stage3` after fixing a coverage gap without re-running the entire pipeline. This makes iteration fast.


### 5. Curation Over Volume

The pedagogy track curates 8-15 sources per topic. The reference track curates 3-6 precision sources per topic. That's it. Total: 466 sources across 51 topics.

Compare this to a RAG approach that indexes 10,000 documents and hopes cosine similarity finds the right paragraph at query time.

**The curator + reviewer pattern:**
1. LLM curator analyzes candidates and picks the best sources for each gap
2. LLM reviewer audits the curator's picks and promotes overlooked near-misses
3. Human-readable curation report shows only the near-misses (not all 90+ candidates)

**Reference track design:**
- Needs-driven, not strategy-driven. An LLM analyzes each topic and outputs typed precision needs (FORMULA_SOURCE, EMPIRICAL_DATA, API_REFERENCE, WORKING_EXAMPLE)
- Small library: 3-6 sources, not 8-15. The tutor has web search for everything else.
- Source cards: Full papers/posts are distilled into ~200-300 word reference cards. Cards (not raw text) are what the KB generator sees, fitting more sources in the context window.
- Ramps over gaps: when no source fills a need, a search hint is stored for runtime lookup. No fake coverage.


### 6. Evaluation From Day One

You cannot improve what you cannot measure.

**Three-tier evaluation:**
- **Tier 1: Structural** -- required sections present, word counts in range, LaTeX balanced, code blocks valid, URLs not broken. Runs in <1 second. Catches 80% of obvious failures.
- **Tier 2: Grounding** -- citations verified against wiki ground truth. Concept coverage checked against outline. Source diversity across lessons. Catches hallucinated URLs and dropped concepts.
- **Tier 3: LLM-as-judge** -- rubric scoring on accuracy, pedagogical flow, engagement, source grounding. Format-probe scenarios that test specific behaviors (does the model use quiz cards when asked to test? does it include URLs in resource cards?).

**Citation validation** is a standalone script. It scans every URL in every lesson and checks it against wiki ground truth. URLs are classified as verified (in wiki), unverified (external/hallucinated), or video. This caught dozens of hallucinated Lilian Weng blog posts that the LLM fabricated during initial content generation.

**Format-probe scenarios:** Automated multi-turn conversations that probe specific format behaviors. "Quiz me on self-attention" should produce `<quiz>` cards, not plain text A/B/C options. "Give me reading material" should produce `<resource>` cards with URLs, not a prose list. These catch prompt regressions before deploy.

**Baseline results tracked:** Every eval run is timestamped and saved. When you change a prompt, you compare against the baseline. "v3 prompt won 4/7 lessons vs v2" is a decision you can make confidently.


### 7. Break It Down, Rebuild It

This project has been broken down and rebuilt multiple times. The pipeline architecture, the prompt strategy, the wiki structure -- all iterated.

- Student notes prompt: 3 versions
- Reference KB prompt: 2 versions
- Content packing: character-based → word-based with per-source cap
- Wiki: 37 topics → 51 topics (14 added mid-project)
- Image pipeline: added after content was already working
- Reference track: entire second track added after pedagogy track was stable

**The pattern:** Get something working end-to-end first. Then improve one piece at a time with evals to prove the improvement. Never rewrite everything at once.

**Contrast with the other team:** Still on v1 of everything after three months because they're trying to get the architecture right before building. Architecture is discovered through iteration, not designed in advance.


### 8. AI-First UX, Not Content-First

The lesson page is chat-first. The tutor takes center stage. Student notes are a reference panel, not the main event.

The tutor has 7 tools it can use *at its own discretion*: web search, curriculum lookup, images, reference KB, curated resources, transcripts, and curriculum search. The system prompt defines *when* to use each tool, but the model makes the decision in context.

Multimodal output isn't about supporting many formats. It's about knowing WHEN to use each one:
- Text for explanations
- LaTeX for math
- Mermaid diagrams for architecture
- Curated images with "show when" metadata
- Quiz cards for knowledge checks
- Resource cards for further reading
- Code blocks with syntax highlighting

The reference KB's "show when" metadata is the secret sauce. The tutor doesn't randomly show images -- it knows "show the attention heatmap diagram when the student asks about how attention weights are computed."


### 9. Ship Early, Enrich Later

The platform launched with 6 courses (74 lessons) generated from the wiki. Not perfect -- but complete and functional. Users can learn from day one.

Enrichment happens iteratively:
- Course creator enriches the wiki every time a new course is built
- Nightly enrichment workflow planned for production (pull DB, enrich locally, push)
- Wiki self-enrichment: the `--enrich` flag on regeneration assesses coverage and grows the wiki before generating

**The wiki grows with usage.** Every course created is an investment in future courses. Topics enriched for Course A benefit Course B automatically.


### 10. One Person + AI Coding Assistants

This entire system -- wiki pipeline, content generation, agent loop, evaluation framework, course creator, frontend, deployment -- was built by one person using AI coding assistants (Cursor + Claude).

This is the meta-point for the audience: AI-first development isn't just the product. It's the process. The same principle that makes the tutor work (AI doing focused tasks with human direction) is what makes the development work.

---

## PART 2: ANTI-PATTERNS (What Goes Wrong)

### Anti-Pattern 1: Start With the UI

**Symptom:** Beautiful course viewer. Polished chat interface. No content pipeline. Team spends months on frontend while the tutor gives generic answers.

**Why it happens:** The UI is visible progress. Stakeholders can see it. The content pipeline is invisible -- it runs in a terminal and produces markdown files.

**The fix:** Get the pipeline producing good content first. A terminal that prints excellent lesson notes is more valuable than a React app rendering mediocre ones.


### Anti-Pattern 2: Framework-First Development

**Symptom:** Weeks spent on LangGraph state machines, agent routing, conditional edges, and annotation schemas. The graph is impressive. The output is mediocre.

**Why it happens:** Frameworks promise to solve the hard problem (making AI behave correctly) through architecture. But the hard problem is actually data quality and prompt design, not orchestration.

**The numbers:** Our agent loop is 136 lines. No framework. The model calls tools when it needs them. The tools are simple lookup functions. The system prompt defines behavior. It's been stable for months while the wiki and prompts evolve weekly.

**The framework trap:** When your agent misbehaves, you debug the graph. When our agent misbehaves, we fix the prompt or improve the wiki. One of these takes hours, the other takes minutes.

**When frameworks ARE appropriate:** If you have 10+ agents with genuinely different capabilities, complex handoffs, and stateful workflows (like a customer service system with escalation paths). For a tutor? The model IS the agent. Tools are lookups. You don't need a graph for that.


### Anti-Pattern 3: RAG Everything

**Symptom:** 10,000 documents in a vector store. Cosine similarity retrieval. Some queries get great context, others get irrelevant paragraphs. No way to control quality.

**Why it happens:** RAG is the default architecture in every AI tutorial. "Just embed your docs and query them!" It works for simple Q&A. It fails for teaching because:
- Teaching needs *organized* knowledge, not *retrieved* chunks
- A good explanation requires context from multiple sources, not the top-3 similar paragraphs
- Pedagogy-specific knowledge (misconceptions, analogies, question banks) doesn't exist in source documents -- it needs to be synthesized

**The wiki-first alternative:** Curate sources into a structured knowledge base with concept mapping, teaching tracks, and precision tracks. The LLM sees organized context, not random chunks.

**Key stat:** Our citation validator caught dozens of hallucinated URLs in early generations. RAG systems can't validate citations because they don't have a ground-truth index of what sources exist.


### Anti-Pattern 4: One Giant Prompt

**Symptom:** A 3,000-word system prompt that tries to make the model Socratic, citation-grounded, format-compliant, curriculum-aware, and pedagogically sound -- all at once. The model reliably drops 30-40% of the constraints.

**Why it happens:** It's the simplest architecture. One prompt, one model, one call. But LLMs have a constraint budget -- the more rules you add, the more they selectively ignore.

**The fix:** Split the work. The system prompt defines *behavior* (be Socratic, use tools). The reference KB provides *knowledge* (misconceptions, teaching approaches). The tools provide *capabilities* (search, images, quizzes). Each component does one thing well.


### Anti-Pattern 5: No Evaluation

**Symptom:** "I changed the prompt and it seems better." No metrics. No comparison. No regression detection. Every change is a guess.

**Why it happens:** Building eval infrastructure feels like overhead when you could be building features. The payoff is invisible until you ship a prompt regression that breaks quiz formatting for two weeks.

**What we built:**
- Structural checks: <1 second, catches 80% of failures
- Citation validation: verifies every URL against wiki ground truth
- Format probes: automated conversations that test specific behaviors
- LLM-as-judge: rubric scoring with baseline tracking
- Side-by-side comparison: old vs new prompt, scored on 5 dimensions, wins/losses tallied

**The payoff:** When we rewrote the student notes prompt from v2 to v3, we tested on 5 diverse lessons and proved the improvement before deploying. When we rewrote the reference KB prompt, we ran LLM-as-judge on 7 lessons and got "4 new wins, 1 old win, 2 ties." That's a confident ship.


### Anti-Pattern 6: Perfect Before Progress

**Symptom:** Three months of architecture planning. Detailed design documents. No working tutor.

**Why it happens:** Fear of rework. "If we design it right, we won't have to rebuild." But you can't design an AI system correctly without building and evaluating it. The prompt that works on paper fails on real data. The pipeline that looks clean produces mediocre output.

**Our timeline:**
- Week 1: Working end-to-end pipeline (ugly output, but complete)
- Week 2-3: Wiki populated, content quality improving
- Week 4-6: Agent loop, eval framework, prompt iterations
- Week 7+: UI polish, course creator, deployment

The pipeline architecture was "discovered" through iteration, not "designed" upfront. The reference track (entire second knowledge pipeline) was added *after* the first track was stable and evaluated.

**Rule of thumb:** If you haven't generated a full lesson and read it critically in the first week, you're moving too slowly.


### Anti-Pattern 7: Treating Multimodal as a Feature

**Symptom:** "We need to add image support" as a feature request. Images added as an afterthought -- randomly inserted, no teaching context, no guidance on when to show them.

**The right approach:** Multimodal is an orchestration problem. The hard part isn't rendering images or embedding videos. It's knowing WHEN each modality adds pedagogical value.

Our image pipeline:
1. Extract images from wiki sources (HTML parsing + heuristic filtering)
2. Annotate with a vision LLM (caption, concepts, teaching value, "when to show")
3. Store metadata per topic with "show when" guidance
4. Tutor decides at runtime whether an image helps THIS student at THIS moment

1,499 annotated images. Each one has metadata telling the tutor when it's useful. That's not "image support" -- it's *pedagogically-informed visual orchestration*.


### Anti-Pattern 8: Manual Content at Scale

**Symptom:** Hiring subject matter experts to write every lesson by hand. High quality per lesson, but doesn't scale. One course takes months.

**Why it's tempting:** Human-written content is better than naive LLM content. But human-written content backed by curated sources and LLM generation is better than both, and scales.

**Our approach:** Humans curate the wiki (quality control at the source level). LLMs generate content from curated sources (scale at the content level). Humans evaluate the output (quality control at the output level). The pipeline generates 74 lessons across 6 courses in one batch run.

**The content still gets reviewed.** But reviewing generated content is 10x faster than writing it from scratch.

---

## PART 3: THE META-PATTERN

The pattern that connects everything: **put complexity where it compounds.**

- Knowledge in the wiki compounds -- every source enriched benefits every future course.
- Evaluation infrastructure compounds -- every test scenario catches regressions forever.
- Prompt iterations compound -- each version builds on lessons from the last.

Things that DON'T compound:
- Framework architecture -- complexity in the orchestration layer doesn't make the output better.
- UI polish before content quality -- a beautiful wrapper around mediocre content is still mediocre.
- Manual content creation -- each lesson is a one-time effort that doesn't improve the system.

**The closing line:** "The best AI tutors won't be the ones with the smartest model -- they'll be the ones with the best knowledge pipeline."

---

## QUICK REFERENCE: Numbers for the Talk

| Metric | Value |
|---|---|
| Wiki topics | 51 |
| Curated sources | 466+ |
| Concepts mapped | 517 across 144 subtopics |
| Annotated images | 1,499+ |
| Educator profiles | 15 |
| Courses generated | 6 (74 lessons) |
| Agent loop code | 136 lines, no framework |
| Student notes prompt | 3 iterations |
| Reference KB prompt | 2 iterations |
| Citation issues caught | 153 in first audit |
| Hallucinated URLs found | Dozens (Lilian Weng posts the LLM fabricated) |
| Image deduplication savings | 224 duplicate downloads / 430 MB |
| Full pipeline test time | ~6 minutes |
| Reference track enrichment | ~137 seconds per lesson |
| Parallel team timeline | 3 months, not shipping |
| This project | One person + AI coding assistants |
