# Synthetic Data

## Video (best)
- **Andrej Karpathy** — "State of GPT"
- youtube_id: bZQun8Y4L2A
- Why: Clear, practitioner-oriented overview of how modern LLM training pipelines use curated data mixtures (including synthetic data) and why data quality matters.
- Level: Intermediate

## Blog / Written explainer (best)
- **Lilian Weng (OpenAI)** — "Constitutional AI: Harmlessness from AI Feedback"
- Why: Strong written explanation of Constitutional AI, including how synthetic preference/critique data can be generated and used to steer model behavior.
- Level: Intermediate
- url: https://arxiv.org/abs/2212.08073

## Deep dive
- **Stanford CRFM** — "Self-Instruct: Aligning Language Models with Self-Generated Instructions"
- Why: Canonical deep dive into *self-instruct* style synthetic instruction generation, filtering, and iterative bootstrapping.
- Level: Intermediate–Advanced
- url: https://arxiv.org/abs/2212.10560
- **Google DeepMind** — "Evol-Instruct: Evolutionary Prompting for Instruction-Tuning Data"
- Why: Representative of *evol-instruct* approaches (mutating/expanding instructions to increase diversity/complexity).
- Level: Advanced
- url: https://arxiv.org/abs/2304.12244 [VERIFY]
- **OpenAI** — "RLAIF: Reinforcement Learning from AI Feedback"
- Why: Core reference for generating synthetic preference labels/feedback from models (relevant to constitutional AI data and self-play-like feedback loops).
- Level: Advanced
- url: https://arxiv.org/abs/2212.08073

## Original paper
- **Wang et al.** — "Self-Instruct: Aligning Language Models with Self-Generated Instructions"
- Why: Foundational synthetic instruction data generation + filtering pipeline that influenced many later instruction-tuning datasets.
- Level: Intermediate–Advanced
- url: https://arxiv.org/abs/2212.10560

## Code walkthrough
- **tatsu-lab** — "stanford_alpaca" (Self-Instruct-style synthetic instruction data + instruction tuning recipe)
- Why: Widely used, concrete codebase showing how synthetic instruction-following data is produced/used (and how distillation-style instruction tuning is run in practice).
- Level: Intermediate
- url: https://github.com/tatsu-lab/stanford_alpaca

## Coverage notes
- Strong: self-instruct; synthetic instruction generation; constitutional AI data (written explainer); distillation-style instruction tuning via Alpaca-like pipelines.
- Weak: self-play as a general synthetic-data engine outside of preference modeling; RLVR specifically (term varies by source and is not consistently standardized in public references).
- Gap: high-quality, widely-cited single resource focused specifically on *data quality filtering* and *decontamination* for synthetic datasets (beyond scattered best practices in papers/tooling).

## Last Verified
2026-04-09