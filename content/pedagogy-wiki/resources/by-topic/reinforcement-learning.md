# Reinforcement Learning

## Video (best)
- **Pieter Abbeel (UC Berkeley)** — "Deep Reinforcement Learning" (CS285 Lecture 1 / intro lecture)
- youtube_id: 2GwTxsAcmJQ
- Why: Abbeel is one of the foremost RL educators; the CS285 series systematically builds from MDPs through policy gradients to modern deep RL methods including PPO and SAC, covering the full conceptual arc needed for physical AI and multimodal applications. The lecture style balances intuition with mathematical rigor.
- Level: intermediate

> **Note:** The CS285 (Deep RL) playlist from UC Berkeley is the gold-standard lecture series. The specific video ID above should be verified against the current YouTube upload. The playlist URL `https://www.youtube.com/playlist?list=PL_iWQOsE6TfURIIhCrlt-wj9ByIVpbfGc` is well-established.

---

## Blog / Written explainer (best)
- **Lilian Weng** — "A (Long) Peek into Reinforcement Learning"
- url: https://lilianweng.github.io/posts/2018-02-19-rl-overview/
- Why: Lilian Weng's post is the definitive written survey for practitioners entering RL. It covers MDPs, value functions, policy gradients, actor-critic methods, and model-based RL in a single coherent narrative with clean notation. Her follow-up posts on PPO and SAC extend this foundation directly into the related concepts listed.
- Level: intermediate

---

## Deep dive
- **Lilian Weng** — "Policy Gradient Algorithms" (comprehensive technical reference covering REINFORCE, A3C, PPO, SAC, and reward shaping)
- url: https://lilianweng.github.io/posts/2018-04-08-policy-gradient/
- Why: This post is the most thorough single-document treatment of the policy gradient family — the algorithmic backbone of modern RL for locomotion and physical AI. It derives each algorithm from first principles, shows the connections between them, and includes reward shaping discussion. Pairs directly with the related concepts (PPO, SAC, policy gradient) listed for this topic.
- Level: advanced

---

## Original paper
- **Schulman et al. (2017)** — "Proximal Policy Optimization Algorithms"
- url: https://arxiv.org/abs/1707.06347
- Why: PPO is the dominant practical RL algorithm used in physical AI, robotics locomotion, and RLHF for multimodal models. This paper is unusually readable for a seminal work — short, clearly motivated, and directly applicable. It represents the convergence point of the policy gradient thread and is the algorithm students will encounter most in real deployments.
- Level: advanced

---

## Code walkthrough
- **CleanRL** — "PPO Implementation Walkthrough" (single-file, heavily annotated PPO implementation)
- url: https://docs.cleanrl.dev/rl-algorithms/ppo/
- Why: CleanRL's philosophy of single-file, fully annotated implementations is pedagogically superior to framework-heavy alternatives. Every design decision is explained inline. The PPO walkthrough covers discrete and continuous action spaces (relevant to locomotion), includes W&B logging, and has a companion paper. This is the resource most likely to bridge theory → working code for learners in physical AI contexts.
- Level: intermediate

---

## Coverage notes
- **Strong:** Policy gradient theory (PPO, SAC), written explainers (Lilian Weng's blog is exceptional), practical implementation (CleanRL)
- **Weak:** World models and perception-prediction-planning as a unified RL framework — most resources treat these separately; no single resource covers the full end-to-end learning pipeline from raw perception through planning to control
- **Gap:** No single excellent YouTube video exists that specifically connects RL to multimodal/physical AI contexts (locomotion + world models + end-to-end learning together). The CS285 series is the closest but requires watching multiple lectures. A dedicated explainer on reward shaping for robotics locomotion specifically is also absent from top-tier educators.

---

## Cross-validation
This topic appears in 2 courses: **intro-to-multimodal**, **intro-to-physical-ai**

- For `intro-to-physical-ai`: the locomotion, SAC, PPO, and end-to-end learning concepts are central — CleanRL + CS285 + PPO paper form a strong trio
- For `intro-to-multimodal`: the world models and perception-prediction-planning angle is less well served by existing resources; instructors may need to supplement with the Dreamer/DreamerV3 paper (`https://arxiv.org/abs/2301.04104`) for the world models thread

---

## Last Verified
2026-04-06