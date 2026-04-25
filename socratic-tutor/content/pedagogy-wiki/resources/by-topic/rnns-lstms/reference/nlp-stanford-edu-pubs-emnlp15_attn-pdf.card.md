# Card: Luong et al. 2015 Attention (Global vs Local) + Scoring Ablations
**Source:** https://nlp.stanford.edu/pubs/emnlp15_attn.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Canonical benchmark tables/ablations (global vs local; dot/general/concat scoring) with BLEU + speed/architecture tradeoffs

## Key Content
- **Seq2seq objective (Eq. 1–4):**  
  \(\log p(y|x)=\sum_{j=1}^m \log p(y_j|y_{<j}, s)\). Decoder: \(p(y_j|y_{<j},s)=\text{softmax}(g(h_j))\); \(h_j=f(h_{j-1}, s)\). Train by minimizing \(J=\sum_{(x,y)\in D}-\log p(y|x)\).
- **Attention output layer (Eq. 5–6):** context \(c_t\) + decoder state \(h_t\) → attentional state  
  \(\tilde h_t=\tanh(W_c[c_t;h_t])\); \(p(y_t|y_{<t},x)=\text{softmax}(W_s\tilde h_t)\).
- **Global attention (Section 3.1, Eq. 7–8):** alignment weights over all source states \(\bar h_s\):  
  \(a_t(s)=\frac{\exp(\text{score}(h_t,\bar h_s))}{\sum_{s'}\exp(\text{score}(h_t,\bar h_{s'}))}\).  
  Scores: **dot** \(h_t^\top \bar h_s\); **general** \(h_t^\top W_a\bar h_s\); **concat** \(v_a^\top\tanh(W_a[h_t;\bar h_s])\). Location baseline: \(a_t=\text{softmax}(W_a h_t)\).
- **Local attention (Section 3.2, Eq. 9–10):** attend to window \([p_t-D,p_t+D]\), fixed \(a_t\in\mathbb{R}^{2D+1}\). Predictive center: \(p_t=S\cdot\sigma(v_p^\top\tanh(W_p h_t))\). Reweight with Gaussian: \(a_t(s)=\text{align}(h_t,\bar h_s)\exp(-(s-p_t)^2/(2\sigma^2))\), with \(\sigma=D/2\). Default **window** \(D=10\).
- **Input-feeding (Section 3.3):** feed \(\tilde h_t\) into next step input to model coverage-like dependence.
- **Training defaults (Section 4.1):** WMT’14 4.5M pairs; vocab 50K; filter length >50; 4-layer LSTM, 1000 cells/layer, 1000-d embeddings; SGD 10 epochs (dropout models 12); LR=1 then halve after epoch 5 (dropout: after 8); batch 128; grad clip norm 5; dropout \(p=0.2\). Speed: ~1K target words/s on Tesla K40; 7–10 days/train.
- **Key empirical results (Tables 1–4):**
  - **WMT’14 En→De (tokenized BLEU):** Base 11.3 → +reverse 12.6 (+1.3) → +dropout 14.0 (+1.4) → +global attn (location) 16.8 (+2.8) → +feed 18.1 (+1.3) → +local-p (general)+feed 19.0 (+0.9) → +unk replace 20.9 (+1.9) → **ensemble 8 + unk 23.0**.
  - **WMT’15 En→De (NIST BLEU):** **25.9** (ensemble 8 + unk) vs top WMT’15 NMT+5gram rerank 24.9.
  - **WMT’15 De→En (Table 3):** Base(reverse) 16.9; +global(location) 19.1 (+2.2); +feed 20.1 (+1.0); +global(dot)+drop+feed 22.8 (+2.7); +unk 24.9 (+2.1).
  - **Ablation insight (Table 4):** global(dot) 18.6 BLEU (20.5 after unk); local-p(general) best: 19.0 (20.9 after unk). Location yields weaker unk-replace gain (+1.2).

## When to surface
Use for questions about **additive/content-based attention math**, **global vs local attention tradeoffs**, **dot/general/concat scoring**, **input-feeding/coverage intuition**, and **benchmark BLEU improvements/ablations on WMT En↔De**.