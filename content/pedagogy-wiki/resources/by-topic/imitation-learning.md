# Imitation Learning

## Video (best)
- **Sergey Levine (UC Berkeley CS285)** — "Imitation Learning" (CS285 Lecture 2)
- youtube_id: zDvcNTVkDxk
- Why: Levine's CS285 Deep RL course is the gold standard academic treatment. The imitation learning lecture covers behavior cloning, DAgger, distribution shift, and the compounding error problem with rigorous mathematical grounding — exactly the conceptual scaffolding learners need before tackling IRL and GAIL.
- Level: intermediate/advanced

## Blog / Written explainer (best)
- **Lilian Weng** — "Imitation Learning Overview"
- url: https://lilianweng.github.io/posts/2018-04-08-policy-gradient/
- Why: Lilian Weng's blog posts are renowned for combining intuitive explanation with mathematical precision. Her coverage of behavior cloning, DAgger, GAIL, and IRL in a single structured post makes it ideal for learners who want a map of the entire landscape before diving into papers.
- Level: intermediate

> ⚠️ **[VERIFY]** — Weng's exact IL post URL is uncertain. Her confirmed IL post may be at `https://lilianweng.github.io/posts/2018-04-08-policy-gradient/` or a dedicated imitation learning post. Check her blog index directly.

## Deep dive
- **Sergey Levine** — CS285 Course Notes / Slides on Imitation Learning
- url: https://rail.eecs.berkeley.edu/deeprlcourse/
- Why: The CS285 lecture slides and notes provide the most comprehensive technical treatment available freely online — covering the formal problem setup, behavioral cloning failure modes (covariate shift), DAgger's theoretical guarantees, inverse RL formulations, and GAIL. Used in graduate-level RL courses worldwide.
- Level: advanced

## Original paper
- **Stéphane Ross, Geoffrey Gordon, Drew Bagnell** — "A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning" (DAgger paper)
- url: https://arxiv.org/abs/1011.0686
- Why: DAgger is the canonical algorithmic contribution that formally characterizes the distribution shift problem in behavior cloning and proposes a principled fix. It remains the most cited and pedagogically important paper in imitation learning — every serious treatment of the topic references it. Highly readable for an academic paper.
- Level: advanced

## Code walkthrough
- **None identified with high confidence**
- Why: No single widely-recognized hands-on IL code walkthrough (YouTube or blog) with verified existence stands out clearly. The closest candidates are:
  - The `imitation` library by CHAI/Adam Gleave: https://github.com/HumanCompatibleAI/imitation
  - Spinning Up by OpenAI covers related RL but not IL specifically.

> Recommend pairing the `imitation` library's documented examples with the CS285 lectures as a substitute until a dedicated walkthrough is identified.

---

## Coverage notes
- **Strong:** Behavior cloning fundamentals, DAgger algorithm, distribution shift problem, IRL vs. GAIL distinction — all well-covered in Levine's CS285 and Weng-style blog posts.
- **Weak:** Robotics-specific IL (RT-1, RT-2, SayCan, VLA models, affordance grounding) — these are cutting-edge topics with limited pedagogical video content; most resources are primary papers only.
- **Weak:** Teleoperation data collection pipelines and open-vocabulary manipulation — almost no beginner-friendly explainers exist; learners must go directly to papers (e.g., RT-2 arxiv).
- **Gap:** No high-quality 3Blue1Brown / Andrej Karpathy style visual explainer exists specifically for imitation learning. The best videos are graduate lecture recordings, which assume significant RL background.
- **Gap:** GAIL specifically lacks a standalone accessible explainer video — it is typically covered briefly within broader IL or GAN lectures.
- **Gap:** Code walkthrough — no single canonical hands-on tutorial analogous to Karpathy's nanoGPT exists for IL.

---

## Last Verified
2025-01-01 (resource existence assessed from training knowledge; all URLs marked should be checked before publishing to platform)