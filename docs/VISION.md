# Vision: What We Are Building and Why

## Purpose

SocraticTutor is one spine: **grounded dialogue on real material**. Under that:

**Customized learning.** You follow real curricula—ordered lessons in a course—but the chat is not a canned script every time. The tutor asks before it lectures, and the model can shift tone and pace with how you show up—still anchored in real reference material, not “make it up as you go” for facts.

**Teach yourself, your way.** You pick the topic and how you walk in: a short prompt, a paper, transcripts, a blog post, a YouTube talk, or a course someone already set up in the app. This is not a tool to **invent** a course from nothing. It is for **finding and keeping strong material** on that subject—a handful of great sources, not hundreds of shallow searches—then shaping it into lessons with a clear reference layer underneath. The LLM does the **interactive** work: dialogue, tone, pace, checks. The spine is the content you gathered and chose, not a one-shot generated textbook.

What stays the same in both: we still care about **questions that make you think**, and we still **tie what the tutor says to solid sources**—what you curated, prepared, or looked up—not vibes.

---

## The core idea

Training someone at work and teaching a student are the same job at heart. You do not open with the final answer. You ask what they tried, what they expected, where it broke. They learn more when they walk to the answer than when you hand it over.

That is the bar for the tutor. Not smarter wording — better questions.

---

## LLM first, grounded first

The experience is built around an LLM on purpose. The thread is not meant to feel like a fixed script every run. Tone and pace can shift with the person in front of you, with how lost or how bored they sound, with what they say they want next. That non‑determinism is a feature, not a bug — as long as we keep one thing tight: **grounding in real sources**.

We invest in reference material, search, curation, and clear rules about what counts as “known” in-session. The learner can start almost anywhere and aim at almost anything; the model flexes the dialogue. The facts and claims should still lean on rich input we prepared or looked up, not on vibes.

The product will keep moving. Better models, new tools, new UI patterns. Grounding is the part we try not to pretend away.

---

## Who it is for

Grounded in what the repo actually ships—not a wish list.

- **Learners** — Anyone using the main app: ordered lessons, tutor chat, quizzes, concept pages, curriculum tools, assessments. Self‑study or a group using the same course. Optional web search and teaching modes when you wire them up.

- **Doers** — People who learn hands‑on, not only by reading chat. The **Projects** surface ties capstone‑style work to courses: outcomes, challenges, demos, repos—so study connects to something you build.

- **Course creators** — People who use the **course creator** (wizard + APIs): turn a topic, paper, or transcripts into researched sources, reference text per lesson, lesson copy, then publish into the database. Same “gather good material first” story as in **Purpose**—here it is productized in the UI.

- **Content builders** — People who prefer **files and version control**: `content/<course>/` packages, `seed.py`, and direct edits. Often the same job as course creators, different door — git‑friendly course packs you own.

- **Developers & operators** — People who **run or extend** SocraticTutor: FastAPI backend, Next.js learner app and course creator, SQLite (or another DB later), env and LLM keys. Also anyone adding routers, agent tools, integrations, or running the **eval** harness to stress‑test tutor quality—not the primary learner audience, but the group that keeps the platform honest and deployable.

---

## Session in the tutor

Someone sits down with: *I want to understand this.*

The tutor uses lesson text, a reference article for that lesson (`reference_kb`), and sometimes video transcripts or live search if you turned them on. It is supposed to nudge with questions, pictures, and quick checks — not to dump a wall of text.

You know it worked when they can explain the idea without rereading the slide.

---

## The tutor does not explain everything itself

A great human tutor does not try to be the best explainer of every topic. They know the landscape — who wrote the clearest walkthrough, which diagram nails the concept, where the best 12‑minute video explanation lives. They point you to the right one, set up the viewing ("watch how he builds from single‑head to multi‑head attention — pay attention to the database lookup analogy"), and then make the real magic happen in the conversation after.

That is what the tutor should do here.

The session might say: *"Before we dig in, watch this segment from 4:20 to 16:30 — it covers exactly what we need."* Then when you come back: *"What clicked? What is still fuzzy?"* — and the Socratic dialogue is grounded in something you both just looked at, not in a wall of generated prose the model improvised.

This means the tutor's reference layer is not just text. It is a media‑rich reservoir: diagrams from blog posts, timestamped segments from conference talks, figures from papers, code walkthroughs. The main lesson gets the essential few inline. The rest stays in the KB, ready to be pulled when the conversation needs it — a diagram when someone is confused about architecture, a code snippet when they want to try something, a video segment when reading is not landing.

We are not generating these visuals. The value is in the **original author's own work** — purpose‑built to explain their content. We curate, attribute, and surface it at the right moment.

---

## More than text

The current reference KB is markdown. That is a starting point, not the ceiling.

Authoritative sources come with high‑value media that text alone cannot replace: architecture diagrams, API flow charts, annotated screenshots, conference‑talk walkthroughs. Stripping all of that out and going text‑only throws away teaching power.

What we want per lesson, alongside the text KB:

- **Images and diagrams** from the source material — with alt text, captions, and which concepts they cover
- **Video segments** — not "here is a 45‑minute talk" but "here is the 3‑minute segment where she explains exactly this concept," with a timestamp link
- **Code examples** — runnable snippets pulled from the source, tagged by concept
- **Figures from papers** — often the most information‑dense part of any academic source

During a live session, different learners absorb differently. Some want the diagram first. Some want code. Some want to watch someone walk through it on video. The tutor should be able to pick the right medium for the person in front of it, based on what it is seeing in the conversation — not locked into one format because that is all we stored.

This is a curation problem at course creation time and a surfacing problem at tutoring time. The course creator collects and catalogs. The tutor chooses and presents.

---

## Learning by building your own course

The typical user is not a course designer building content for others. They are a learner building a course **for themselves** — *"I want to understand reinforcement learning"* — and the process of finding good sources is the beginning of their learning journey, not a chore before the real work starts.

That changes the design of course creation. It should feel like a guided discovery session, not a batch pipeline:

- The system searches and narrates what it finds: *"This tutorial is referenced everywhere — I think it will be a strong foundation for us."*
- Each source is presented with context: why it is good, what it covers, what it assumes you already know.
- The learner reacts — skip, include, "find more like this," "I already know this part." Those reactions tell us their level, their interests, their preferred learning style.
- The system adapts: if you skip all the beginner sources, it shifts to intermediate material.

By the time we have 5–10 approved sources and start building the outline, we already know a lot about the learner. That knowledge shapes the course — depth, tone, which subtopics get more space.

Not everyone wants this. Some people want "just build it, I will review." So there are two modes: an interactive discovery mode for self‑learners, and an auto mode for people who prefer review gates. Same pipeline underneath — the difference is how much the system pauses and narrates.

---

## Source‑first, not search‑heavy

The original course creation pipeline ran hundreds of web searches — a dozen per lesson, across every lesson. It produced wide but shallow coverage.

The better approach: find a small number of great sources for the whole course (5–10), ingest them deeply (full text, not snippets), and build the entire curriculum from that material. A well‑built course reads like it was written by someone who actually studied the sources, not like a collage of search results.

For the tutor's reference KB, we can do a second pass of targeted, per‑lesson searches in the background — filling gaps, finding supplementary angles. But the core learning content comes from sources the learner (or creator) saw and approved.

---

## Being honest about facts

We use four levels so the model does not sound equally sure about everything:

1. **From the lesson reference_kb** — We prepared this; say it straight.
2. **From web search in this session** — Say where it came from.
3. **Ordinary textbook‑level background** — Fine to teach; do not dress it up as a citation.
4. **Anything else** — Say you are not sure, look it up, or skip it. Never invent.

Reference_kb can come from search + human cleanup, or you can write it by hand. Either way it is the line between *we meant this for the tutor* and *the model made it up on the spot*.

---

## Small example

| Weaker | Stronger |
|--------|----------|
| “Here is the low‑rank update: \(W \leftarrow W + BA\).” | “Before we write that down — if \( \Delta W \) is low rank, what does that cap, in plain terms?” |

---

## Learn by building

Reading about a concept and building with it are different kinds of understanding. You can read about attention mechanisms and pass a quiz. But when you build a retrieval pipeline and it returns garbage because your chunking strategy is wrong — and you have to figure out *why* — that is when the concept actually lands.

The deepest version of this system is not "read lesson, chat with tutor, take quiz." It is: **here is a project, start building, and the tutor walks alongside you** — explaining principles when you hit them naturally, not in a predetermined order. The learning path emerges from the work.

What this looks like in practice:

- A guided project: "Build a document Q&A system." The learner starts coding. The tutor watches.
- When they hit a design decision ("how should I chunk these documents?"), the tutor turns it into a learning moment — Socratic questions, a pointer to the right source material, maybe a diagram showing the trade‑offs.
- When something breaks, the tutor does not just fix it. It asks what they expected, what happened instead, and helps them reason through the gap. The failure *is* the curriculum.
- Concepts are covered because the project requires them, not because a syllabus said so. The ordering is organic.

This is much harder to design than a linear course. The course creator would need to think carefully about:

- What project is rich enough to surface the right concepts?
- What are the likely failure modes, and what does each one teach?
- Where are the natural decision points where a concept becomes relevant?
- How do you guide without railroading — let the learner explore, but make sure the important ideas get covered?

We are not there yet. The Projects surface today is a structured capstone: outcomes, challenges, architecture diagrams, demo links. But the vision is a tutor that can sit inside a live coding or design session and turn the work itself into the lesson — not after the fact, but while it is happening.

This is the hardest thing to build and the most valuable. Content‑first learning, multimodal sessions, source curation — all of that feeds into this. The richer and more grounded the KB, the better the tutor can respond to the unpredictable path a hands‑on session takes.

---

## What we are not building

Not search with a chat box on top. Not one FAQ answer per question. Not homework autocomplete.

We care whether someone leaves knowing **why**, not whether the page looked smart.

---

## Getting better over time

A tutor that does not learn from its sessions is stuck. The product should get better with use, not just with code changes.

- **What worked** — When a learner says "oh, that makes sense now" after a specific diagram or video segment, that is signal. When they re‑ask the same concept three different ways, that is signal too.
- **What did not** — If learners consistently skip a source, or if a certain explanation style leads to more confusion than clarity, we should notice.
- **Evaluation as a habit** — The eval harness already simulates student personas and scores tutor quality. Over time, we expand it: more lessons, more personas, more rubric dimensions. Regressions get caught before they ship.
- **Closing the loop** — Learner signals (what they engage with, what they skip, where they struggle) feed back into source curation and KB quality. The reference layer is not static — it improves as more people use it.

This is a data flywheel, not a one‑shot build. The course creator gathers good material. The tutor uses it. Learner signals tell us what is working. We refine. Repeat.

---

## Experiments we are trying

We are still kicking the tires on several directions, not as promises — as bets:

- **Project‑first learning** — The vision is a tutor that sits inside a live build session and turns the work itself into the lesson (see "Learn by building" above). Getting there incrementally — starting with structured project guides, then more adaptive scaffolding.
- **AI‑assisted knowledge checks** — Faster, more targeted ways to see what stuck.
- **Generative UI** — Let the conversation surface controls, visuals, or structure when they help, instead of locking everything into static templates.
- **Multimodal sessions** — The tutor assigns a video segment or diagram as "homework" mid‑conversation, then debriefs with Socratic questions about what the learner saw. Shared context, not just text back and forth.
- **Learner modality adaptation** — Over time, notice whether someone responds better to diagrams, code, video, or written explanation. Lean into what works for them.
- **Interactive course discovery** — Course creation as a guided conversation where the system narrates what it finds, the learner reacts, and the discovery process itself teaches.

Some of this will ship, some will not. The vision above is what survives the experiments.

---

## Code and docs

We keep platform and course data separate so you can swap content without rewriting the app. Wizard details: `docs/ARCHITECTURE-COURSE-CREATOR.md`. Repo layout and design notes: root `README.md`.
