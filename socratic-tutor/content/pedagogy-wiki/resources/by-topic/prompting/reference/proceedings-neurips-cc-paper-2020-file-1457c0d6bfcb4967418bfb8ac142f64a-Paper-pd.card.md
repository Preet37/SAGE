# Card: GPT-3 Few-shot / One-shot / Zero-shot Evaluation Protocol & Benchmarks
**Source:** https://proceedings.neurips.cc/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Definitions + evaluation protocol for 0S/1S/FS; benchmark tables showing scaling trends with model size and # in-context examples.

## Key Content
- **Learning settings (Section 2 “Approach”):**
  - **Fine-tuning (FT):** update weights on supervised task data.
  - **Few-shot (FS):** provide **K demonstrations** (context→completion pairs) in the prompt; **no gradient updates**. Typical **K ≈ 10–100**, limited by **context window nctx = 2048** tokens.
  - **One-shot (1S):** FS with **K = 1**.
  - **Zero-shot (0S):** **task description/instruction only**, **K = 0**.
- **Few-shot evaluation procedure (Section 2.4):**
  - For each eval example, **randomly draw K examples from the task training set** as conditioning; delimiter **1–2 newlines** depending on task.
  - If no training set (e.g., **LAMBADA, StoryCloze**): draw conditioning examples from **dev**, evaluate on **test**.
  - Some tasks add a **natural-language prompt** and/or **answer formatting** changes.
  - **Free-form completion decoding:** **beam search** with **beam width = 4**, **length penalty α = 0.6**.
- **Key empirical results (Tables 3.1–3.5):**
  - **CoQA (F1):** 0S **81.5**, 1S **84.0**, FS **85.0**.
  - **TriviaQA (acc):** 0S **64.3**, 1S **68.0**, FS **71.2** (FS reported as SOTA in closed-book comparison).
  - **LAMBADA (acc):** 0S **76.2**, FS **86.4**.
  - **SuperGLUE (FS, 32 examples):** Avg **69.0**; notable: **COPA 52.0**, **ReCoRD F1 91.1**, **WiC 49.4** (near chance).
- **Design rationale (Intro/Fig 1.1):** performance improves with **model size** and **# in-context examples**; **gap between 0S/1S/FS often grows with capacity**, suggesting larger models are better at **in-context learning/meta-learning**.

## When to surface
Use when students ask how to define/implement zero-shot vs one-shot vs few-shot prompting, how to run fair in-context evaluations (K sampling, formatting, decoding), or want concrete benchmark numbers showing gains from more examples/model scale.