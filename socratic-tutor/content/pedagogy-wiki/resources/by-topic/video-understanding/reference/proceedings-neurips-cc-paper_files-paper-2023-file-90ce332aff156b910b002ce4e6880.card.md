# Card: EgoSchema (Very Long-form VideoQA + Temporal Certificates)
**Source:** https://proceedings.neurips.cc/paper_files/paper/2023/file/90ce332aff156b910b002ce4e6880dec-Paper-Datasets_and_Benchmarks.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Dataset/task spec + “temporal certificate” metric + zero-shot baselines/human results diagnosing long-horizon video reasoning failures.

## Key Content
- **Dataset spec (Abstract, Fig. 1, Datasheet):**
  - **5063 instances**; each instance = **3-minute** egocentric clip + **1 question** + **5 answer options** (label **1–5** indicates correct option).
  - Sourced from **Ego4D**; total coverage **>250 hours** of real video.
  - Raw video: **mp4**, **30 fps**, high resolution.
- **Filtering defaults (Stage I, §3.1.1):**
  - Extract **non-overlapping 3-minute clips** with **≥30 timestamped human narrations** per clip.
- **QA generation defaults (Stage II, §3.1.2):**
  - Generate **N = 3** questions per clip; **M = 4** wrong answers per question (5-way MCQ total).
  - Preferred prompting chain: **Q(AW)-shot** (2 LLM calls): generate N questions jointly, then generate all correct+wrong answers conditioned on questions.
  - LLMs found to yield good Q/A/W quality: **GPT-4, Bard, Claude**.
- **Filtering & curation (Stage III–IV, §3.1.3–§3.1.4):**
  - Rule-based keyword/format filtering.
  - **Blind filtering baseline:** LLM guesses answer from **question only**; if it can answer “blindly,” discard (precision-over-recall).
  - Human curation round 1 verifies: (A) Q well-formed & A correct, (B) all distractors wrong, (C) **temporal certificate length ≥30s**; reduces admissible Qs by **~4–5×**. Round 2: **>97%** of round-1 pass also pass.
- **Key definition (Temporal certificate, §3.2):**
  - **Temporal certificate set** = *minimum set of subclips* **necessary and sufficient** for a human to verify the annotation without watching the rest.
  - **Certificate length** = **sum of durations** of subclips in the certificate set.
  - Conventions: min subclip **0.1s**; merge certificates if gap **<5s**.
- **Empirical results (Fig. 3, Table 6–7):**
  - EgoSchema **median certificate length ~100s**; **5.7×** longer than next closest dataset; **10×–100×** longer than most others.
  - **Zero-shot model accuracy <33%** (random **20%**); **human ~76%**.
  - Table 6 examples: FrozenBiLM **26.4% (10 frames)** / **26.9% (90)**; InternVideo **31.4% (10)** / **32.0% (90)**; mPLUG-Owl peaks **30.2% (5 frames)** (non-monotonic).
  - Human settings (Table 7): **67.2% @ 1 fps (180 frames)**; **67.0% <1 min**; **68.0% <3 min**; **75.1% no constraint**; **76.2% Video→Text**.

## When to surface
Use when students ask how to *measure* “long-horizon” video understanding beyond clip length, or want concrete benchmark specs/baselines for very long-form VideoQA and why current VLMs fail on long temporal reasoning.