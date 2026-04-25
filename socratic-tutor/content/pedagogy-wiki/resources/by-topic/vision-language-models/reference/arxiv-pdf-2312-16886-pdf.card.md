# Card: MobileVLM (VLM training + efficient projector; contrasts Q-Former/MLP)
**Source:** https://arxiv.org/pdf/2312.16886.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Concrete equations for VLM token projection + 2-step VLM training (freeze/train projector then tune), plus empirical token-count/speed comparisons and Q-Former vs MLP rationale.

## Key Content
- **Architecture (Sec. 3.1):** Vision encoder → visual embeddings \(Z\in\mathbb{R}^{N\times D_v}\) (N patches, \(D_v\) hidden). Projector maps to LLM embedding space to form **image tokens** + **text tokens** for autoregressive decoding.
- **Eq. (1) (Sec. 3.1):** Projector converts vision features into word-embedding space: \(H_v = \Phi(Z)\) (projector \(\Phi\)); output dimension matches LLM embedding size \(D\). (Text tokens \(H_t\in\mathbb{R}^{T\times D}\); image tokens \(H_v\in\mathbb{R}^{M\times D}\).)
- **Eq. (2) (Sec. 3.1):** Autoregressive response conditioned on multimodal tokens: \(p(y\,|\,H_v,H_t)=\prod_{i=1}^{L} p(y_i\,|\,y_{<i},H_v,H_t)\).
- **Projector rationale (Sec. 3.4):**
  - **Q-Former:** controls #visual tokens via queries but “loses spatial positional information,” “slow convergence,” and is inefficient on edge.
  - **MLP projector:** retains spatial info but injects many (often background) tokens → slows inference.
  - **LDP (Lightweight Downsample Projector):** uses depth-wise conv (PEG-like) + stride-2 downsampling to keep spatial info while reducing tokens; <20M params; reduces tokens by **75%**.
- **Token-count result (Sec. 5.1):** LDP reduces visual tokens **576 → 144** (−75%) with **equivalent or sometimes better** benchmark performance.
- **Resolution vs token reduction (Sec. 5.3, Table 11):** With 144 tokens, **LDP beats reducing input resolution (RIR)**:  
  - LDP: GQA **56.1**, SQA **54.7**, VQA **41.5**, POPE **84.5**, MME **1196.2**, MMB **53.2**  
  - RIR: GQA **53.9**, SQA **53.1**, VQA **37.1**, POPE **81.5**, MME **1072.5**, MMB **46.7**
- **VLM training pipeline (Sec. 4.1):** 2-step: (1) **freeze vision encoder + LLM**, train projector only (pretrain on **CC-595K**, 1 epoch, batch **256**); (2) fine-tune **projector + LLM** (instruction tuning on **LLaVA-Instruct-158K**, 1 epoch, batch **128**). AdamW, cosine LR, warmup ratio **3%**, no weight decay.
- **Latency formula (Eq. 4, Sec. 4.5):** Total inference time decomposed into load + prompt processing + generation terms using measured tokens/s; key point: fewer visual tokens reduces prompt-processing time.

## When to surface
Use when students ask about (i) how VLMs inject visual tokens into LLMs (equations + token shapes), (ii) Q-Former vs MLP projector tradeoffs, or (iii) why reducing token count via downsampling can outperform lowering image resolution.