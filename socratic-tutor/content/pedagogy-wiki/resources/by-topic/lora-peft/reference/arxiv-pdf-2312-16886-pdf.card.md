# Card: MobileVLM training + LoRA insertion points in VLM stacks
**Source:** https://arxiv.org/pdf/2312.16886.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** Reproducible VLM pipeline (frozen vision encoder + projector + LLM) + 2-step VLM training and LoRA results for PEFT discussion.

## Key Content
- **Architecture (Sec. 3.1):** 3 parts: (1) vision encoder, (2) LLM (MobileLLaMA), (3) efficient projector (LDP) aligning vision→text embedding space.
- **Eq. (1) (Sec. 3.1):** Projector maps visual embeddings to LLM word-embedding dimension:  
  - Input visual tokens: \(Z \in \mathbb{R}^{N \times D_v}\) (N patches/tokens, \(D_v\) vision hidden size).  
  - Output image tokens: \(V \in \mathbb{R}^{M \times D_t}\) (M visual tokens after compression/alignment, \(D_t\) LLM embedding size).
- **Eq. (2):** Autoregressive generation conditioned on multimodal tokens (image tokens + text tokens) to produce output length \(L\).
- **Projector rationale (Sec. 3.4):** Q-Former can lose spatial info + slow convergence + inefficient on edge; plain MLP keeps spatial info but injects many useless/background tokens → slows inference. LDP uses **depthwise conv** and **stride-2 downsampling** to reduce tokens while preserving spatial structure.
- **Token reduction & quality (Sec. 5.1):** LDP reduces visual tokens **576 → 144 (−75%)** with **equivalent or sometimes better** benchmark performance vs baseline.
- **Resolution vs token strategy (Sec. 5.3, Table 11):** Keeping 144 tokens via LDP beats reducing input resolution (RIR):  
  - **LDP:** GQA 56.1, SQA 54.7, VQA 41.5, POPE 84.5, MME 1196.2, MMB 53.2  
  - **RIR:** GQA 53.9, SQA 53.1, VQA 37.1, POPE 81.5, MME 1072.5, MMB 46.7
- **VLM training procedure (Sec. 4.1):** Two-step multimodal training (like LLaVA/mPLUG style):  
  1) **Pre-train:** freeze **vision encoder + LLM**, train **projector only** on **CC-595K** for **1 epoch**, lr **2e-3**, batch **256**.  
  2) **Instruction tuning:** fine-tune **projector + LLM** on **LLaVA-Instruct-158K** for **1 epoch**, lr **2e-5**, batch **128**. Optimizer AdamW, **no weight decay**, cosine LR, **3% warmup**.
- **LoRA PEFT result (Sec. 4.4):** During visual instruction tuning, freeze all LLM params except LoRA; trainable params are **8.87% (1.4B)** and **7.41% (2.7B)** of full LLM; LoRA config **r=128**, **α=256**; achieves **comparable** performance to full finetuning on **6 benchmarks**.

## When to surface
Use when students ask where to insert LoRA/adapters in VLMs (projector vs LLM), how “freeze-then-tune” alignment pipelines work, or want concrete token-reduction and PEFT tradeoff numbers.