# Card: Global vs Local Attention in NMT (Luong et al., 2015)
**Source:** https://arxiv.org/pdf/1508.04025.pdf  
**Role:** benchmark | **Need:** COMPARISON_DATA  
**Anchor:** Structured comparison of global vs local attention (scoring functions), empirical gains vs non-attentional baselines, alignment/compute tradeoffs.

## Key Content
- **Seq2seq objective (Eq. 1–4):**  
  \(\log p(y|x)=\sum_{j=1}^m \log p(y_j|y_{<j}, s)\).  
  \(p(y_j|y_{<j},s)=\text{softmax}(g(h_j))\) (Eq. 2); \(h_j=f(h_{j-1}, s)\) (Eq. 3). Train by minimizing \(J=\sum_{(x,y)\in D}-\log p(y|x)\) (Eq. 4).
- **Attention output layer (Eq. 5–6):** context \(c_t\) + decoder state \(h_t\) → attentional state  
  \(\tilde h_t=\tanh(W_c[c_t;h_t])\) (Eq. 5); \(p(y_t|y_{<t},x)=\text{softmax}(W_s\tilde h_t)\) (Eq. 6).
- **Global attention (Sec. 3.1, Eq. 7–8):** attend over all encoder states \(\bar h_s\).  
  \(a_t(s)=\text{softmax}(\text{score}(h_t,\bar h_s))\) (Eq. 7). Scoring:  
  dot \(h_t^\top \bar h_s\); general \(h_t^\top W_a \bar h_s\); concat \(v_a^\top \tanh(W_a[h_t;\bar h_s])\). Location baseline: \(a_t=\text{softmax}(W_a h_t)\) (Eq. 8).
- **Local attention (Sec. 3.2, Eq. 9–10):** compute only a window \([p_t-D,p_t+D]\) (fixed \(2D+1\) weights).  
  local-m: \(p_t=t\). local-p: \(p_t=S\cdot \sigma(v_p^\top \tanh(W_p h_t))\) (Eq. 9); weights multiplied by Gaussian \(\exp(-(s-p_t)^2/(2\sigma^2))\) with \(\sigma=D/2\) (Eq. 10). **Default:** \(D=10\).
- **Input-feeding (Sec. 3.3):** feed \(\tilde h_t\) into next step input to model coverage-like dependence; deepens network.
- **Empirical gains (WMT’14 En→De, tokenized BLEU, Table 1):**  
  Base 11.3; +reverse 12.6 (+1.3); +dropout 14.0 (+1.4); +global attn (location) 16.8 (+2.8); +feed 18.1 (+1.3); +local-p (general)+feed 19.0 (+0.9). **Total:** +5.0 BLEU over non-attentional (reverse+dropout). +unk replace → 20.9 (+1.9). Ensemble(8)+unk: 23.0.
- **WMT’15 En→De (Table 2, NIST BLEU):** their ensemble+unk 25.9 vs best WMT’15 NMT+5gram rerank 24.9 (+1.0).
- **Alignment quality (Table 6, AER):** global(location) 0.39; local-m(general) 0.34; local-p(general) 0.36; ensemble 0.34; Berkeley Aligner 0.32. Local attention alignments sharper; AER not tightly correlated with BLEU.

## When to surface
Use when students ask how attention fixes the seq2seq bottleneck, or to compare **global vs local attention**, scoring functions (dot/general/concat/location), and the **compute–alignment–BLEU** tradeoffs with concrete WMT results.