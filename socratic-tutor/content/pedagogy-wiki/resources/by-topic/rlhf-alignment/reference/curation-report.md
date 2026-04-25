# Curation Report: Alignment & RLHF
**Topic:** `rlhf-alignment` | **Date:** 2026-04-09 13:33
**Library:** 6 existing → 19 sources (13 added, 9 downloaded)
**Candidates evaluated:** 48
**Reviewer verdict:** needs_additions

## Added (13)
- **[paper]** [Learning to summarize from human feedback](https://proceedings.neurips.cc/paper/2020/file/1f89885d556929e98d3ef9b86448f951-Paper.pdf)
  This is a primary-source, equation-bearing RLHF paper that explicitly formalizes preference modeling from comparisons and connects it to RL optimization, giving the tutor citable math beyond blog-level summaries.
- **[paper]** [Training language models to follow instructions with human feedback](https://proceedings.neurips.cc/paper_files/paper/2022/file/b1efde53be364a73914f58805a001731-Paper-Conference.pdf)
  It provides the most authoritative procedural description of the modern RLHF loop (data collection, RM training, PPO fine-tuning) that a tutor can walk through line-by-line with students.
- **[paper]** [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073)
  This is the canonical source for Constitutional AI/RLAIF, with concrete pipeline stages and design rationale that explain how alignment can be bootstrapped with minimal human labeling.
- **[benchmark]** [Unpacking DPO and PPO: Disentangling Best Practices for Learning ...](https://arxiv.org/html/2406.09279v2)
  Among the candidates, this is the most directly aimed at head-to-head empirical understanding of DPO vs PPO and what actually drives gains, which is exactly what the tutor needs for numbers and ablations.
- **[reference_doc]** [Safety evaluations hub | OpenAI](https://openai.com/safety/evaluations-hub/)
  It gives an operational, deployment-facing view of how a major provider measures safety/robustness over time, which supports teaching monitoring, red-teaming, and post-training evaluation practices.
- **[paper]** [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://proceedings.neurips.cc/paper_files/paper/2023/file/a85b405ed65c6477a4fe8302b5e06ce7-Paper-Conference.pdf)
  The library currently lacks a primary-source, equation-bearing derivation of DPO; this NeurIPS paper is the canonical math reference and directly fills the DPO formula gap.
- **[paper]** [Understanding Reference Policies in Direct Preference Optimization](https://arxiv.org/html/2407.13709v2)
  Students routinely get confused about what the reference model is doing in DPO; this paper is narrowly focused on that missing conceptual+mathematical piece.
- **[paper]** [A Comprehensive Survey of Direct Preference Optimization](https://arxiv.org/html/2410.15595v2)
  While not a primary method paper, it efficiently fills concept coverage gaps around the growing DPO family and gives a single citable map of objectives/assumptions.
- **[code]** [Hugging Face TRL (source code as API reference for PPOTrainer/DPOTrainer defaults)](https://github.com/huggingface/trl)
  Forum threads are rightly non-authoritative, but the repo itself is the authoritative ground truth for defaults; the library should explicitly treat TRL code/config definitions as the API reference.
- **[paper]** [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://proceedings.neurips.cc/paper_files/paper/2023/file/a85b405ed65c6477a4fe8302b5e06ce7-Paper-Conference.pdf) *(promoted by reviewer)*
  The library currently lacks a primary-source, equation-bearing derivation of DPO; this NeurIPS paper is the canonical math reference and directly fills the DPO formula gap.
- **[paper]** [Understanding Reference Policies in Direct Preference Optimization](https://arxiv.org/html/2407.13709v2) *(promoted by reviewer)*
  Students routinely get confused about what the reference model is doing in DPO; this paper is narrowly focused on that missing conceptual+mathematical piece.
- **[paper]** [A Comprehensive Survey of Direct Preference Optimization](https://arxiv.org/html/2410.15595v2) *(promoted by reviewer)*
  While not a primary method paper, it efficiently fills concept coverage gaps around the growing DPO family and gives a single citable map of objectives/assumptions.
- **[code]** [Hugging Face TRL (source code as API reference for PPOTrainer/DPOTrainer defaults)](https://github.com/huggingface/trl) *(promoted by reviewer)*
  Forum threads are rightly non-authoritative, but the repo itself is the authoritative ground truth for defaults; the library should explicitly treat TRL code/config definitions as the API reference.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Is DPO Superior to PPO for LLM Alignment? A Comprehensive St** — [Is DPO Superior to PPO for LLM Alignment? A Comprehensive Study](https://arxiv.org/abs/2404.10719)
  _Skipped because:_ Likely strong for empirical comparisons, but the provided candidate entry is too thin/duplicative here versus the more general best-practices disentangling focus of the selected Unpacking DPO/PPO source.
- **New Version of PPOTrainer - 🤗Transformers** — [New Version of PPOTrainer - 🤗Transformers](https://discuss.huggingface.co/t/new-version-of-ppotrainer/118316)
  _Skipped because:_ Forum threads are not authoritative API references for defaults; the tutor needs stable docs or code-level config definitions rather than community troubleshooting.
- **Improving Model Safety Behavior with Rule-Based Rewards** — [Improving Model Safety Behavior with Rule-Based Rewards](https://openai.com/index/improving-model-safety-behavior-with-rule-based-rewards/)
  _Skipped because:_ Useful deployment-adjacent narrative, but it is less of a concrete, ongoing operational reference than the evaluations hub for teaching monitoring and measurable safety outcomes.

## Reasoning
**Curator:** Selections prioritize primary-source papers and official operational references that add equations, concrete pipelines, and empirical comparisons not already covered by the existing library. Forum posts were avoided as non-authoritative for defaults; remaining gaps are best filled by official TRL config/code references and the original DPO/IPO/KTO papers plus benchmark-heavy alignment studies.
**Reviewer:** The curator’s picks are strong for RLHF/PPO and deployment evaluation, but the library still needs primary-source DPO math and an authoritative defaults reference (best satisfied by the DPO paper(s) and TRL config/code).

---

# Curation Report: Alignment & RLHF
**Topic:** `rlhf-alignment` | **Date:** 2026-04-09 13:54
**Library:** 6 existing → 15 sources (9 added, 5 downloaded)
**Candidates evaluated:** 46
**Reviewer verdict:** needs_additions

## Added (9)
- **[paper]** [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)
  This is the primary source for the exact PPO-clip objective and update logic that RLHF implementations cite and reuse, enabling precise derivations and correct explanations of why clipping stabilizes policy updates.
- **[paper]** [Training language models to follow instructions with human feedback](https://proceedings.neurips.cc/paper_files/paper/2022/file/b1efde53be364a73914f58805a001731-Paper-Conference.pdf)
  Provides the most authoritative, citable empirical comparisons isolating the effect of SFT vs RLHF in a real deployed setting, with tables/figures the tutor can quote.
- **[code]** [github-huggingface-trl](https://github.com/huggingface/trl)
  Forum threads are not authoritative for defaults; the TRL repository code and docs are the most reliable place to map trainer arguments to the underlying PPO/DPO algorithms and to quote actual default values.
- **[paper]** [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/pdf/2212.08073.pdf)
  This is the original, detailed description of Constitutional AI and RLAIF, including the rationale for replacing human labels with principle-guided AI feedback and the concrete training loop.
- **[paper]** [[PDF] Training language models to follow instructions with human feedback](https://cdn.openai.com/papers/Training_language_models_to_follow_instructions_with_human_feedback.pdf)
  Among the candidates, this contains the most concrete real-world RLHF deployment constraints and process details (data ops + safety/quality mitigations) from the team that deployed InstructGPT.
- **[reference_doc]** [Proximal Policy Optimization (PPO) — Spinning Up documentation](https://spinningup.openai.com/en/latest/algorithms/ppo.html)
  Even though it’s “thin,” it’s official, stable algorithm documentation that helps a tutor connect the Schulman paper equations to the exact knobs used in RLHF implementations (KL target, early stopping, penalty vs clip).
- **[paper]** [Proximal Policy Optimization Algorithms](https://arxiv.org/pdf/1707.06347.pdf)
  The curator already intends to add PPO, but the PDF should be explicitly included as the canonical formula source (not just an arXiv stub), since tutors will need to quote exact equations and variants.
- **[reference_doc]** [Proximal Policy Optimization (PPO) — Spinning Up documentation](https://spinningup.openai.com/en/latest/algorithms/ppo.html) *(promoted by reviewer)*
  Even though it’s “thin,” it’s official, stable algorithm documentation that helps a tutor connect the Schulman paper equations to the exact knobs used in RLHF implementations (KL target, early stopping, penalty vs clip).
- **[paper]** [Proximal Policy Optimization Algorithms](https://arxiv.org/pdf/1707.06347.pdf) *(promoted by reviewer)*
  The curator already intends to add PPO, but the PDF should be explicitly included as the canonical formula source (not just an arXiv stub), since tutors will need to quote exact equations and variants.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Aligning language models to follow instructions** — [Aligning language models to follow instructions](https://openai.com/index/instruction-following/)
  _Skipped because:_ Useful high-level deployment narrative, but it is less precise than the paper PDF (fewer equations, fewer procedural details, fewer citable tables).
- **Enhancing RLHF with Weighted Preference Optimization** — [Enhancing RLHF with Weighted Preference Optimization](https://arxiv.org/html/2406.11827v2)
  _Skipped because:_ Has modern preference-optimization experiments, but it does not directly provide the clean SFT vs RLHF vs DPO baseline ablations the tutor is missing, and it is less canonical than the core RLHF/DPO sources.
- **New Version of PPOTrainer - 🤗Transformers** — [New Version of PPOTrainer - 🤗Transformers](https://discuss.huggingface.co/t/new-version-of-ppotrainer/118316)
  _Skipped because:_ May contain practical tips, but forum posts are not stable/authoritative references for defaults and can drift from the actual implementation.

## Reasoning
**Curator:** Selections prioritize primary sources and authoritative implementations that directly supply equations, defaults, and citable ablations, while avoiding unstable forum content. Where candidates did not include canonical DPO/KL-shaping derivations or modern head-to-head benchmark ablations, those needs are explicitly left unfilled with targeted search hints.
**Reviewer:** The curator’s core picks are strong, but adding the PPO Spinning Up reference doc (and explicitly the PPO PDF) materially improves formula-level and implementation-level teaching precision; the remaining candidates listed don’t clearly fill the stated unfilled needs.

---

# Curation Report: Alignment & RLHF
**Topic:** `rlhf-alignment` | **Date:** 2026-04-09 14:10
**Library:** 6 existing → 22 sources (16 added, 8 downloaded)
**Candidates evaluated:** 46
**Reviewer verdict:** needs_additions

## Added (16)
- **[paper]** [[PDF] Training language models to follow instructions with human feedback](https://cdn.openai.com/papers/Training_language_models_to_follow_instructions_with_human_feedback.pdf)
  This is the most authoritative primary source for the InstructGPT-style RLHF recipe and includes concrete, citable human-preference evaluation numbers and key design choices used in production.
- **[paper]** [[PDF] Direct Preference Optimization: Your Language Model is Secretly a ...](https://proceedings.neurips.cc/paper_files/paper/2023/file/a85b405ed65c6477a4fe8302b5e06ce7-Paper-Conference.pdf)
  Provides the canonical mathematical formulation and derivation for DPO, enabling precise explanations of why it works and how it relates to KL-regularized RLHF.
- **[benchmark]** [Is DPO Superior to PPO for LLM Alignment? A Comprehensive Study](https://arxiv.org/abs/2404.10719)
  Directly targets the tutor’s missing empirical comparisons between PPO-based RLHF and DPO, with systematic ablations that help explain when each method wins and why.
- **[code]** [lm-human-preferences/lm_human_preferences/train_policy.py at cbfd210bb8b08f6bc5c26878c10984b90f516c66 · openai/lm-human-preferences](https://github.com/openai/lm-human-preferences/blob/cbfd210bb8b08f6bc5c26878c10984b90f516c66/lm_human_preferences/train_policy.py)
  An official OpenAI repo gives concrete, inspectable defaults and semantics in code—useful for answering “what exactly did they set?” beyond high-level TRL docs.
- **[paper]** [Constitutional AI: Harmlessness from AI Feedback](https://www.anthropic.com/news/constitutional-ai-harmlessness-from-ai-feedback)
  Even if it’s not classic RM+PPO RLHF, it is a production-grade alignment pipeline description that fills the library’s gap on alternative feedback sources (AI feedback) and system-level process details.
- **[paper]** [Deep Reinforcement Learning from Human Preferences](https://arxiv.org/abs/1706.03741)
  This is the canonical origin of the pairwise preference reward-model objective that RLHF inherits; it directly fills the missing primary-source math for preference/RM training.
- **[paper]** [Learning to Summarize from Human Feedback](https://arxiv.org/abs/2009.01325)
  Often overlooked because InstructGPT gets the spotlight, but this paper provides a clear, earlier end-to-end RLHF instantiation with numbers and procedural detail useful for teaching.
- **[reference_doc]** [TRL Documentation: PPOTrainer](https://huggingface.co/docs/trl/main/en/ppo_trainer)
  Forum threads are noisy; the official docs (even if thin) are exactly what’s needed to ground discussions of PPOConfig/PPOTrainer semantics in a stable reference.
- **[reference_doc]** [TRL Documentation: DPOTrainer](https://huggingface.co/docs/trl/main/en/dpo_trainer)
  Complements the DPO paper with implementation-facing semantics and defaults in widely used tooling, directly addressing the “production-grade tooling beyond forum discussions” gap.
- **[paper]** [The N+ Implementation Details of RLHF with PPO: A Case Study on TL](https://arxiv.org/html/2403.17031v1)
  This is one of the few candidates explicitly aiming at an end-to-end, implementation-detailed RLHF pipeline; even if not the most authoritative, it targets the library’s biggest unfilled need.
- **[paper]** [Constitutional AI: Harmlessness from AI Feedback](https://www.anthropic.com/news/constitutional-ai-harmlessness-from-ai-feedback) *(promoted by reviewer)*
  Even if it’s not classic RM+PPO RLHF, it is a production-grade alignment pipeline description that fills the library’s gap on alternative feedback sources (AI feedback) and system-level process details.
- **[paper]** [Deep Reinforcement Learning from Human Preferences](https://arxiv.org/abs/1706.03741) *(promoted by reviewer)*
  This is the canonical origin of the pairwise preference reward-model objective that RLHF inherits; it directly fills the missing primary-source math for preference/RM training.
- **[paper]** [Learning to Summarize from Human Feedback](https://arxiv.org/abs/2009.01325) *(promoted by reviewer)*
  Often overlooked because InstructGPT gets the spotlight, but this paper provides a clear, earlier end-to-end RLHF instantiation with numbers and procedural detail useful for teaching.
- **[reference_doc]** [TRL Documentation: PPOTrainer](https://huggingface.co/docs/trl/main/en/ppo_trainer) *(promoted by reviewer)*
  Forum threads are noisy; the official docs (even if thin) are exactly what’s needed to ground discussions of PPOConfig/PPOTrainer semantics in a stable reference.
- **[reference_doc]** [TRL Documentation: DPOTrainer](https://huggingface.co/docs/trl/main/en/dpo_trainer) *(promoted by reviewer)*
  Complements the DPO paper with implementation-facing semantics and defaults in widely used tooling, directly addressing the “production-grade tooling beyond forum discussions” gap.
- **[paper]** [The N+ Implementation Details of RLHF with PPO: A Case Study on TL](https://arxiv.org/html/2403.17031v1) *(promoted by reviewer)*
  This is one of the few candidates explicitly aiming at an end-to-end, implementation-detailed RLHF pipeline; even if not the most authoritative, it targets the library’s biggest unfilled need.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Constitutional AI: Harmlessness from AI Feedback - Anthropic** — [Constitutional AI: Harmlessness from AI Feedback - Anthropic](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)
  _Skipped because:_ Excellent production-oriented process description (RLAIF) but less directly focused on classic RLHF (pairwise RM + PPO) and the specific missing benchmark/API-default details.
- **[PDF] Unpacking DPO and PPO: Disentangling Best Practices fo** — [[PDF] Unpacking DPO and PPO: Disentangling Best Practices for Learning ...](https://proceedings.neurips.cc/paper_files/paper/2024/file/404df2480b6eef0486a1679e371894b0-Paper-Conference.pdf)
  _Skipped because:_ Likely strong for best-practices comparisons, but the selected DPO-vs-PPO comprehensive study is a more direct match to the requested head-to-head/ablations need.
- **Secrets of RLHF in Large Language Models Part II - Reward Mo** — [Secrets of RLHF in Large Language Models Part II - Reward Modeling](https://arxiv.org/html/2401.06080v2)
  _Skipped because:_ Appears to be a project-style implementation writeup, but it’s not clearly an authoritative, widely-used reproducible pipeline with known expected outputs on a standard dataset from the candidate snippet.

## Reasoning
**Curator:** Selections prioritize primary/seminal sources that directly supply missing equations (DPO), citable production RLHF pipeline + numbers (InstructGPT), systematic PPO-vs-DPO empirical comparisons, and an official reference implementation for concrete hyperparameters/defaults. Forum threads and less-authoritative project writeups were deprioritized.
**Reviewer:** The curator’s core picks are strong for InstructGPT/DPO and empirical PPO-vs-DPO, but the library still needs primary-source preference-model math, official TRL API docs for config semantics, and at least one reproducibility-oriented end-to-end pipeline reference.

---

# Curation Report: Alignment & RLHF
**Topic:** `rlhf-alignment` | **Date:** 2026-04-09 14:16
**Library:** 6 existing → 23 sources (17 added, 9 downloaded)
**Candidates evaluated:** 50
**Reviewer verdict:** needs_additions

## Added (17)
- **[benchmark]** [[PDF] Unpacking DPO and PPO: Disentangling Best Practices for Learning ...](https://proceedings.neurips.cc/paper_files/paper/2024/file/404df2480b6eef0486a1679e371894b0-Paper-Conference.pdf)
  Provides concrete comparative numbers and controlled ablations directly addressing SFT/RLHF-style best practices and the PPO-vs-DPO trade space, which the tutor can cite when students ask “which works better and why?”.
- **[paper]** [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/pdf/2212.08073.pdf)
  This is the primary-source, end-to-end description of Constitutional AI, enabling the tutor to explain the full system design (not just definitions) and how preference pairs are produced without human labelers.
- **[reference_doc]** [[PDF] GPT-4 System Card | OpenAI](https://cdn.openai.com/papers/gpt-4-system-card.pdf)
  While not a full RLHF ops runbook, it is an authoritative deployment-facing document with concrete safety evaluation structure and mitigations that a tutor can use to discuss real-world alignment deployment considerations.
- **[paper]** [Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback](https://arxiv.org/abs/2204.05862)
  This is a core RLHF/HH assistant paper with the kind of end-to-end procedural detail and objective framing students ask for; it also serves as a concrete case study beyond blog-level summaries.
- **[paper]** [Training language models to follow instructions with human feedback (InstructGPT)](https://arxiv.org/abs/2203.02155)
  Even if already present in the library, it is the primary mathematical reference that directly fills the stated objective/derivation gap (PPO-ptx + pairwise preference loss) and should be treated as the canonical formula source.
- **[paper]** [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290)
  The library has DPO/PPO comparisons but lacks the canonical DPO derivation; this paper is the standard reference for teaching where the DPO loss comes from and how it relates to KL-regularized RLHF.
- **[reference_doc]** [TRL Documentation: PPOTrainer](https://huggingface.co/docs/trl/en/ppo_trainer)
  Forum threads are noisy, but the official TRL docs (even if thin) are exactly what a reference library needs for default meanings and configuration semantics.
- **[reference_doc]** [TRL Documentation: DPOTrainer](https://huggingface.co/docs/trl/en/dpo_trainer)
  This directly addresses the unfilled need for trainer parameter semantics and reduces confusion when students try to map the DPO paper objective to an actual implementation.
- **[reference_doc]** [Hugging Face Accelerate Documentation](https://huggingface.co/docs/accelerate/index)
  The lesson explicitly calls out Accelerate/DeepSpeed settings affecting training; the official docs are the most reliable place to ground those discussions.
- **[reference_doc]** [DeepSpeed Configuration JSON Documentation](https://www.deepspeed.ai/docs/config-json/)
  This is the canonical reference for the exact parameter names and meanings students need when reproducing RLHF runs at scale.
- **[paper]** [Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback](https://arxiv.org/abs/2204.05862) *(promoted by reviewer)*
  This is a core RLHF/HH assistant paper with the kind of end-to-end procedural detail and objective framing students ask for; it also serves as a concrete case study beyond blog-level summaries.
- **[paper]** [Training language models to follow instructions with human feedback (InstructGPT)](https://arxiv.org/abs/2203.02155) *(promoted by reviewer)*
  Even if already present in the library, it is the primary mathematical reference that directly fills the stated objective/derivation gap (PPO-ptx + pairwise preference loss) and should be treated as the canonical formula source.
- **[paper]** [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290) *(promoted by reviewer)*
  The library has DPO/PPO comparisons but lacks the canonical DPO derivation; this paper is the standard reference for teaching where the DPO loss comes from and how it relates to KL-regularized RLHF.
- **[reference_doc]** [TRL Documentation: PPOTrainer](https://huggingface.co/docs/trl/en/ppo_trainer) *(promoted by reviewer)*
  Forum threads are noisy, but the official TRL docs (even if thin) are exactly what a reference library needs for default meanings and configuration semantics.
- **[reference_doc]** [TRL Documentation: DPOTrainer](https://huggingface.co/docs/trl/en/dpo_trainer) *(promoted by reviewer)*
  This directly addresses the unfilled need for trainer parameter semantics and reduces confusion when students try to map the DPO paper objective to an actual implementation.
- **[reference_doc]** [Hugging Face Accelerate Documentation](https://huggingface.co/docs/accelerate/index) *(promoted by reviewer)*
  The lesson explicitly calls out Accelerate/DeepSpeed settings affecting training; the official docs are the most reliable place to ground those discussions.
- **[reference_doc]** [DeepSpeed Configuration JSON Documentation](https://www.deepspeed.ai/docs/config-json/) *(promoted by reviewer)*
  This is the canonical reference for the exact parameter names and meanings students need when reproducing RLHF runs at scale.

## Near-Misses (4) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Aligning language models to follow instructions** — [Aligning language models to follow instructions](https://openai.com/index/instruction-following/)
  _Skipped because:_ Highly relevant to RLHF deployment context, but overlaps with existing InstructGPT-style coverage and is less of a detailed ops case study than the system card PDF.
- **DPO Meets PPO: Reinforced Token Optimization for RLHF - arXi** — [DPO Meets PPO: Reinforced Token Optimization for RLHF - arXiv](https://arxiv.org/html/2404.18922v4)
  _Skipped because:_ Potentially useful for bridging PPO/DPO concepts, but the provided candidate snippet appears mismatched/duplicative and is less directly aligned to the requested head-to-head benchmark/ablation focus than the NeurIPS “Unpacking DPO and PPO” paper.
- **Confusing (and possibly misleading) PPO Trainer Code from TR** — [Confusing (and possibly misleading) PPO Trainer Code from TRL ...](https://discuss.huggingface.co/t/confusing-and-possibly-misleading-ppo-trainer-code-from-trl-api-doc-tutorial/67531)
  _Skipped because:_ Contains hints about defaults, but it is a forum thread (not authoritative API documentation) and may be outdated relative to current TRL config defaults/semantics.
- **Reward Shaping to Mitigate Reward Hacking in RLHF - arXiv** — [Reward Shaping to Mitigate Reward Hacking in RLHF - arXiv](https://arxiv.org/html/2502.18770v5)
  _Skipped because:_ Good for reward-hacking mitigation details, but it is more a research study than a production deployment case study with concrete operational metrics (cost/latency/incident rates) requested.

## Reasoning
**Curator:** Selections prioritize primary-source, high-authority materials that add missing empirical comparisons (PPO vs DPO ablations) and a definitive Constitutional AI pipeline description, plus at least one credible deployment-facing document; forum threads and non-authoritative snippets were deprioritized for API-default precision.
**Reviewer:** The curator’s additions are strong, but the library still needs canonical objective/derivation papers (especially DPO) and official TRL/Accelerate/DeepSpeed docs to satisfy the stated formula and API-reference gaps.

---

# Curation Report: Alignment & RLHF
**Topic:** `rlhf-alignment` | **Date:** 2026-04-09 15:10
**Library:** 6 existing → 22 sources (16 added, 6 downloaded)
**Candidates evaluated:** 40
**Reviewer verdict:** needs_additions

## Added (16)
- **[paper]** [[PDF] Proximal Policy Optimization Algorithms - arXiv](https://arxiv.org/pdf/1707.06347.pdf)
  This is the primary source for the exact PPO objective used inside PPO-RLHF implementations, including the clipped ratio form and the standard combined loss terms.
- **[paper]** [Direct Preference Optimization: Your Language Model is ...](https://arxiv.org/html/2305.18290v3)
  Provides the exact mathematical bridge from preference likelihood modeling to the closed-form DPO loss, and explicitly connects it to the KL-regularized RLHF objective.
- **[paper]** [[PDF] Training language models to follow instructions with human feedback](https://cdn.openai.com/papers/Training_language_models_to_follow_instructions_with_human_feedback.pdf)
  This is the most authoritative step-by-step description of the classic ChatGPT/InstructGPT-style RLHF workflow, including data collection protocol and why each stage exists.
- **[explainer]** [Aligning language models to follow instructions](https://openai.com/index/instruction-following/)
  Adds concrete, citable preference-win outcomes and high-level comparative results that are frequently referenced in alignment discussions and student questions.
- **[paper]** [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)
  Even if already mentioned in the added track, it should be explicitly included as a canonical primary source because PPO is the core optimizer inside PPO-RLHF and students will ask for the exact objective and its variants.
- **[paper]** [Truly Proximal Policy Optimization (supplementary)](http://proceedings.mlr.press/v115/wang20b/wang20b-supp.pdf)
  This fills a common conceptual gap in RLHF tutoring—why PPO can be unstable and how clipping relates to trust regions—useful when explaining KL control and failure modes in PPO-RLHF.
- **[reference_doc]** [New Version of PPOTrainer - Hugging Face Forums](https://discuss.huggingface.co/t/new-version-of-ppotrainer/118316)
  Thin but high-value operational detail: TRL’s PPOTrainer semantics change over time, and forum threads often become the de facto reference for defaults and breaking changes.
- **[reference_doc]** [Negative KL values during PPO training (TRL library) - Hugging Face Forums](https://discuss.huggingface.co/t/negative-kl-values-during-ppo-training-trl-library/84143)
  Directly supports tutoring/debugging: negative KL is a frequent confusion point in PPO-RLHF implementations and this thread provides concrete interpretation tied to TRL behavior.
- **[reference_doc]** [ORPO/DPO dataset clarification - Hugging Face Forums (lewtun reply)](https://discuss.huggingface.co/t/orpo-dpo-dataset-clarification/103637/2)
  This is precisely the kind of “thin” but essential reference that prevents silent training bugs and answers common student questions about how preference datasets must be structured.
- **[paper]** [The N+ Implementation Details of RLHF with PPO: A Case Study on TL](https://arxiv.org/html/2403.17031v1)
  This directly targets the unfilled “deployment/process” need: it’s not just theory, but a procedural/engineering account that helps a tutor explain what actually matters in practice.
- **[paper]** [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347) *(promoted by reviewer)*
  Even if already mentioned in the added track, it should be explicitly included as a canonical primary source because PPO is the core optimizer inside PPO-RLHF and students will ask for the exact objective and its variants.
- **[paper]** [Truly Proximal Policy Optimization (supplementary)](http://proceedings.mlr.press/v115/wang20b/wang20b-supp.pdf) *(promoted by reviewer)*
  This fills a common conceptual gap in RLHF tutoring—why PPO can be unstable and how clipping relates to trust regions—useful when explaining KL control and failure modes in PPO-RLHF.
- **[reference_doc]** [New Version of PPOTrainer - Hugging Face Forums](https://discuss.huggingface.co/t/new-version-of-ppotrainer/118316) *(promoted by reviewer)*
  Thin but high-value operational detail: TRL’s PPOTrainer semantics change over time, and forum threads often become the de facto reference for defaults and breaking changes.
- **[reference_doc]** [Negative KL values during PPO training (TRL library) - Hugging Face Forums](https://discuss.huggingface.co/t/negative-kl-values-during-ppo-training-trl-library/84143) *(promoted by reviewer)*
  Directly supports tutoring/debugging: negative KL is a frequent confusion point in PPO-RLHF implementations and this thread provides concrete interpretation tied to TRL behavior.
- **[reference_doc]** [ORPO/DPO dataset clarification - Hugging Face Forums (lewtun reply)](https://discuss.huggingface.co/t/orpo-dpo-dataset-clarification/103637/2) *(promoted by reviewer)*
  This is precisely the kind of “thin” but essential reference that prevents silent training bugs and answers common student questions about how preference datasets must be structured.
- **[paper]** [The N+ Implementation Details of RLHF with PPO: A Case Study on TL](https://arxiv.org/html/2403.17031v1) *(promoted by reviewer)*
  This directly targets the unfilled “deployment/process” need: it’s not just theory, but a procedural/engineering account that helps a tutor explain what actually matters in practice.

## Near-Misses (2) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **[PDF] Direct Preference Optimization: Your Language Model is** — [[PDF] Direct Preference Optimization: Your Language Model is Secretly a ...](https://proceedings.neurips.cc/paper_files/paper/2023/file/a85b405ed65c6477a4fe8302b5e06ce7-Paper-Conference.pdf)
  _Skipped because:_ Redundant with the arXiv HTML version; the arXiv page is easier to deep-link to specific appendix derivations for tutoring.
- **Training language models to follow instructions with human f** — [Training language models to follow instructions with human feedback](https://proceedings.neurips.cc/paper_files/paper/2022/file/b1efde53be364a73914f58805a001731-Paper-Conference.pdf)
  _Skipped because:_ Same content as the OpenAI-hosted PDF; keeping one canonical copy avoids duplication.

## Reasoning
**Curator:** Selections prioritize primary sources that (1) pin down exact objectives/derivations (PPO and DPO) and (2) document the canonical RLHF pipeline and its empirical preference outcomes (InstructGPT). The remaining gaps require either code-level default documentation or true production postmortems, which the provided candidates did not authoritatively supply.
**Reviewer:** The core conceptual papers are well-chosen, but the library still needs a few canonical PPO references plus thin-but-critical TRL parameter/behavior documentation and at least one concrete PPO-RLHF implementation case study.
