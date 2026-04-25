# Card: Luong et al. 2015 Attention Variants + Benchmarks (WMT En↔De)
**Source:** https://aclanthology.org/anthology-files/pdf/D/D15/D15-1166.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Benchmark tables comparing attention variants (global/local; dot/general/concat scoring) with BLEU on WMT tasks + speed/architecture tradeoffs.

## Key Content
- **NMT objective (Eq. 1–4):**  
  \(\log p(y|x)=\sum_{j=1}^m \log p(y_j|y_{<j}, s)\) (Eq.1);  
  \(p(y_j|y_{<j},s)=\text{softmax}(g(h_j))\) (Eq.2); \(h_j=f(h_{j-1},s)\) (Eq.3); training minimizes \(J=\sum_{(x,y)\in D}-\log p(y|x)\) (Eq.4).
- **Attention output layer (Eq. 5–6):**  
  \(\tilde h_t=\tanh(W_c[c_t;h_t])\) (Eq.5); \(p(y_t|y_{<t},x)=\text{softmax}(W_s\tilde h_t)\) (Eq.6).
- **Global attention (Section 3.1, Eq. 7–9):**  
  \(a_t(s)=\frac{\exp(\text{score}(h_t,\bar h_s))}{\sum_{s'}\exp(\text{score}(h_t,\bar h_{s'}))}\) (Eq.7);  
  score options (Eq.8): dot \(h_t^\top \bar h_s\); general \(h_t^\top W_a\bar h_s\); concat \(W_a[h_t;\bar h_s]\).  
  Location baseline: \(a_t=\text{softmax}(W_a h_t)\) (Eq.9). Context \(c_t=\sum_s a_t(s)\bar h_s\).
- **Local attention (Section 3.2, Eq. 10–11):** attend to window \([p_t-D,p_t+D]\), \(a_t\in\mathbb{R}^{2D+1}\).  
  local-m: \(p_t=t\). local-p: \(p_t=S\cdot\sigma(v_p^\top\tanh(W_p h_t))\) (Eq.10); Gaussian bias: multiply by \(\exp(-(s-p_t)^2/(2\sigma^2))\), with \(\sigma=D/2\) (Eq.11).
- **Input-feeding (Section 3.3):** feed \(\tilde h_t\) as part of next-step input to model coverage-like behavior; deepens network horizontally/vertically.
- **Training defaults (Section 4.1):** WMT’14 4.5M pairs; vocab 50K each; filter length >50; 4-layer LSTM, 1000 cells/layer, 1000-d embeddings; SGD 10 epochs (LR=1, halve after epoch 5); batch 128; grad clip norm 5; init U[-0.1,0.1]; dropout variant trains 12 epochs, halve after epoch 8. Speed: ~1K target words/sec on Tesla K40; 7–10 days/model.
- **Key empirical results (Tables 1–4):**
  - En→De newstest2014 tokenized BLEU: Base+rev+dropout **14.0** → +global attn(location) **16.8** (+2.8) → +feed **18.1** (+1.3) → +local-p(general)+feed **19.0** (+0.9) → +unk replace **20.9** (+1.9). Ensemble 8 + unk: **23.0**.
  - WMT’15 En→De (Table 2, NIST BLEU): prior SOTA 24.9 vs **25.9** (ensemble 8 + unk).
  - De→En newstest2015 (Table 3): Base(reverse) 16.9 → +global(location) 19.1 (+2.2) → +feed 20.1 (+1.0) → +global(dot)+drop+feed 22.8 (+2.7) → +unk 24.9 (+2.1).
  - Attention scoring comparison (Table 4): global(dot) BLEU 18.6 (20.5 after unk); local-p(general) BLEU 19.0 (20.9 after unk). Location learns weaker alignments (smaller unk-replace gain).
- **Alignment quality (Table 6):** AER: global(location) 0.39; local-m(general) 0.34; local-p(general) 0.36; ensemble 0.34; Berkeley aligner 0.32.

## When to surface
Use when students ask for the **exact attention equations** (global vs local, dot/general/concat), **why local attention is cheaper/differentiable**, or for **benchmark BLEU/AER comparisons and training hyperparameters** on WMT En↔De.