# Reasoning Models

## Video (best)
- **Andrej Karpathy** — "Deep Dive into LLMs like ChatGPT"
- Why: Clear, high-signal overview of how modern LLMs are trained and used, including RLHF and inference-time behavior that connects to “reasoning” and test-time compute ideas.
- Level: Intermediate

## Blog / Written explainer (best)
- **Lilian Weng (OpenAI)** — "LLM Powered Autonomous Agents"
- url: https://lilianweng.github.io/posts/2023-06-23-agent/
- Why: Strong conceptual grounding for reasoning-like behaviors in LLM systems (planning, reflection, tool use), and how inference-time scaffolding changes capabilities.
- Level: Intermediate

## Deep dive
- **Lilian Weng (OpenAI)** — "Reinforcement Learning with Human Feedback"
- url: https://lilianweng.github.io/posts/2024-11-28-reward-hacking/
- Why: One of the clearest end-to-end explainers of RLHF-style training loops and reward modeling; useful background for “reinforcement learning for reasoning,” outcome vs process supervision, and reward model design.
- Level: Intermediate–Advanced
- **OpenAI** — "Learning to summarize with human feedback"
- url: https://openai.com/research/learning-to-summarize-with-human-feedback
- Why: Canonical, readable RLHF case study (reward modeling + policy optimization) that transfers directly to reasoning-focused RL setups.
- Level: Intermediate

## Original paper
- **Ouyang et al. (OpenAI, 2022)** — "Training language models to follow instructions with human feedback" (InstructGPT)
- url: https://arxiv.org/abs/2203.02155
- Why: Foundational paper for reward modeling + RL fine-tuning; core prerequisite for understanding later “reasoning model” training recipes.
- Level: Advanced
- **Cobbe et al. (OpenAI, 2021)** — "Training Verifiers to Solve Math Word Problems"
- url: https://arxiv.org/abs/2110.14168
- Why: Directly targets verification at test time (verifier/reranker) and connects to test-time compute scaling via sampling + selection.
- Level: Advanced

## Code walkthrough
- **Hugging Face TRL** — "TRL (Transformer Reinforcement Learning)"
- url: https://github.com/huggingface/trl
- Why: Widely used, practical RLHF/RLAIF tooling (PPO/DPO-style training, reward modeling utilities) suitable for implementing outcome-reward training pipelines.
- Level: Intermediate–Advanced
- **CarperAI** — "trlx"
- url: https://github.com/CarperAI/trlx
- Why: Another established RLHF training codebase; useful for seeing end-to-end reward model + policy optimization in practice.
- Level: Advanced

## Coverage notes
- Strong: RLHF fundamentals; reward modeling; verifier-based selection; practical RL tooling (TRL/trlx).
- Weak: Specific “reasoning-architectures” branding (o1, o3, deepseek-r1) and their proprietary details; “thinking tokens” as an explicit mechanism.
- Gap: High-confidence, primary sources that explicitly define/standardize “process reward models” vs “outcome reward models” for reasoning, and authoritative public docs for o1/o3/deepseek-r1 and “reasoning traces” policies.

## Last Verified
2026-04-09