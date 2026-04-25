# Card: BLIP-2 two-stage objectives + Q-Former querying
**Source:** https://proceedings.mlr.press/v202/li23q/li23q.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Stage-1/Stage-2 BLIP-2 training objectives for Q-Former + query-token cross-attention bottleneck

## Key Content
- **Architecture (Sec. 3.1, Fig. 2):** Q-Former bridges a **frozen image encoder** and **frozen LLM** using **learnable query tokens**. Queries use **self-attention** among themselves and **cross-attention to frozen image features** (cross-attn layers inserted **every other transformer block**). Queries can also interact with text tokens via shared self-attn layers; interaction controlled by **attention masks** per objective.
- **Bottleneck sizing:** typically **32 queries**, each **768-d**; output query reps **Z ∈ R^{32×768}**. Example frozen ViT features: **257×1024 (ViT-L/14)**. Q-Former initialized from **BERT-base**; cross-attn layers random init; Q-Former ~**188M params** (queries count as parameters).
- **Stage-1 (Sec. 3.2): joint loss = ITC + ITM + ITG**
  - **ITC (Image-Text Contrastive):** align image rep from queries **Z** with text rep **t** (the **[CLS]** embedding). Similarity: compute sim(q_i, t) for each query output, take **max_i** as image-text similarity; uses **unimodal mask** (queries/text cannot attend each other); uses **in-batch negatives**.
  - **ITG (Image-grounded Text Generation):** LM-style generation conditioned on queries; **multimodal causal mask**: queries attend queries only; each text token attends **all queries + previous text tokens**; replace [CLS] with **[DEC]** token.
  - **ITM (Image-Text Matching):** binary matched/unmatched with **bidirectional mask** (full query-text attention). For each query output, compute 2-class logit; **average logits across queries** for match score; uses **hard negative mining**.
- **Stage-2 (Sec. 3.3, Fig. 3): vision→language generative bootstrapping**
  - Project queries via **FC layer** to LLM embedding dim; **prepend projected queries** as **soft visual prompts** to LLM input.
  - **Decoder-only LLM (e.g., OPT):** train with **language modeling loss** to generate text conditioned on visual prompts.
  - **Encoder–decoder LLM (e.g., FlanT5):** **prefix LM loss**: split text into **prefix** (encoder input with visual prompts) and **suffix** (decoder target).
- **Key results (Tables 1–2):**
  - Zero-shot **VQAv2 test-dev:** **BLIP-2 65.0** vs **Flamingo80B 56.3** (BLIP-2 uses **54× fewer trainable params**).
  - Example configs: **BLIP-2 ViT-g + FlanT5-XXL:** **VQAv2 test-dev 65.0**, **OK-VQA 45.9**, **GQA 44.7** (Table 2).
- **Pretraining defaults (Sec. 3.4):** Stage-1 **250k steps**, Stage-2 **80k steps**; image size **224×224**; optimizer **AdamW**, β1=0.9, β2=0.98, weight decay 0.05; cosine LR, peak **1e-4**, warmup **2k** steps; Stage-2 min LR **5e-5**.

## When to surface
Use when students ask how BLIP-2 aligns vision with a frozen LLM, what the **ITC/ITM/ITG** objectives are (including masking), or how **query-token cross-attention** creates a fixed-size visual bottleneck independent of image resolution.