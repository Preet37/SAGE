# Mixture Of Experts

## Video (best)
- **Yannic Kilcher** — "Switch Transformer (Mixture of Experts) - Paper Explained"
- youtube_id: ccBMRryxGog
- Why: Clear, paper-focused walkthrough of sparse MoE routing, top-k/top-1 gating, and the load-balancing objective used in Switch Transformer.
- Level: Intermediate

## Blog / Written explainer (best)
- **Lilian Weng (OpenAI)** — "Mixture-of-Experts (MoE)"
- url: https://lilianweng.github.io/posts/2021-09-25-train-large/
- Why: One of the most complete written explainers of MoE fundamentals (sparse routing, expert specialization, top-k routing) and training issues (load balancing, auxiliary losses, expert collapse).
- Level: Intermediate

## Deep dive
- **NVIDIA Developer Blog** — "Mixture of Experts Explained"
- url: https://developer.nvidia.com/blog/applying-mixture-of-experts-in-llm-architectures/
- Why: Systems-and-training oriented deep dive; useful for understanding practical MoE implementation concerns (capacity, routing, throughput) alongside conceptual grounding.
- Level: Intermediate

## Original paper
- **Fedus, Zoph, Shazeer (2021)** — "Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity"
- url: https://arxiv.org/abs/2101.03961
- Why: Canonical modern sparse MoE Transformer design; introduces top-1 routing variant, capacity factor, and the auxiliary load-balancing loss widely reused in later MoE models.
- Level: Advanced

## Code walkthrough
- **Hugging Face Transformers Docs** — "SwitchTransformers"
- url: https://huggingface.co/docs/transformers/model_doc/switch_transformers
- Why: Practical reference for how Switch Transformer is exposed in a mainstream library; helpful for mapping paper concepts (router, experts, capacity) to code-level components.
- Level: Intermediate

## Coverage notes
- Strong: MoE fundamentals (mixture of experts, sparse routing, expert specialization, top-k/top-1 routing); training mechanics (load balancing, auxiliary losses); Switch Transformer as the reference architecture.
- Weak: High-confidence, single-source deep dives specifically on **Mixtral**, **DeepSeek-V2**, and **Grok** MoE design details (beyond general MoE concepts and scattered release materials).
- Gap: A reliable, step-by-step code walkthrough for **Mixtral**-style MoE (and/or DeepSeek-V2) that explains router math, capacity management, and load-balancing losses end-to-end in one place.

## Last Verified
2026-04-09