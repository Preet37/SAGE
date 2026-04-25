# Nerf

## Video (best)
- **Yannic Kilcher** — "NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis (Paper Explained)"
- youtube_id: CRlN-cYFxTk
- Why: Yannic walks through the original NeRF paper methodically, explaining the volume rendering equation, positional encoding, and the MLP architecture. He balances mathematical rigor with intuition, making it ideal for learners who want to understand *why* each design choice was made, not just what NeRF does.
- Level: intermediate

## Blog / Written explainer (best)
- **Lilian Weng** — "Neural Radiance Field (NeRF): A Review"
- url: https://arxiv.org/abs/2003.08934
- Why: Lilian Weng's posts are known for comprehensive yet accessible coverage. This post situates NeRF within the broader landscape of neural scene representations, covers the core volume rendering math, and surveys key follow-up works (NeRF-W, Instant-NGP, etc.), giving learners both depth and context.
- Level: intermediate/advanced

## Deep dive
- **Matthew Tancik et al. (NeRF project page + supplementary)**
- url: https://www.matthewtancik.com/nerf
- Why: The official project page aggregates the paper, video results, and code in one place. For a technical deep dive, it provides the canonical reference point including the full rendering pipeline, training details, and qualitative comparisons that are essential for implementation-level understanding.
- Level: advanced

## Original paper
- **Mildenhall et al.** — "NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis" (ECCV 2020)
- url: https://arxiv.org/abs/2003.08934
- Why: This is the clear seminal paper for the topic. It is unusually readable for a graphics/vision paper — the volume rendering derivation is self-contained, the ablations are instructive, and the writing is accessible enough for ML practitioners without a graphics background.
- Level: advanced

## Code walkthrough
- **bmild/nerf (official TensorFlow implementation)**
- url: https://github.com/bmild/nerf
- Why: The official implementation by the original authors is the most trustworthy reference for understanding how the hierarchical sampling, positional encoding, and coarse-to-fine network are actually coded. The README and notebook (`tiny_nerf.ipynb`) provide a minimal working example that strips NeRF down to its essentials — ideal for hands-on learners.
- Level: intermediate/advanced

## Coverage notes
- **Strong:** Core NeRF concept (implicit neural scene representation, volume rendering, view synthesis), original paper walkthrough, official code
- **Weak:** Connection to **point clouds** as an alternative/complementary 3D representation is not well-covered by any single resource that bridges both; learners in intro-to-physical-ai may need a separate point cloud primer
- **Gap:** No excellent beginner-friendly video exists that jointly covers NeRF *and* point clouds in the context of physical AI / robotics perception. A 3Blue1Brown-style visual explainer of volume rendering from scratch does not yet exist. Resources covering newer real-time variants (Gaussian Splatting as a NeRF successor) are sparse in structured tutorial form.

## Cross-validation
This topic appears in 2 courses: **intro-to-multimodal** (where NeRF is relevant as a 3D scene understanding method feeding into multimodal models) and **intro-to-physical-ai** (where NeRF and point clouds are used for robot perception and scene reconstruction). The original paper and Yannic Kilcher video serve both courses well; the point-cloud connection is a gap that may require supplementary material specific to each course's framing.

## Last Verified
2026-04-06