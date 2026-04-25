# Card: Luong Attention (Global vs Local) + Scoring Functions (EMNLP’15)
**Source:** https://aclanthology.org/anthology-files/pdf/D/D15/D15-1166.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Benchmark tables/ablations comparing global vs local attention + score functions; BLEU on WMT En↔De.

## Key Content
- **Decoder with attention (Section 3):** given top-layer decoder state \(h_t\), compute context \(c_t\), then attentional state  
  \(\tilde{h}_t=\tanh(W_c[c_t;h_t])\) (Eq. 5), output \(p(y_t|y_{<t},x)=\text{softmax}(W_s\tilde{h}_t)\) (Eq. 6).
- **Global attention (Eq. 7–8):** alignment over all source states \(\bar{h}_s\):  
  \(a_t(s)=\frac{\exp(\text{score}(h_t,\bar{h}_s))}{\sum_{s'}\exp(\text{score}(h_t,\bar{h}_{s'}))}\).  
  Scores (Eq. 8): **dot** \(h_t^\top\bar{h}_s\); **general** \(h_t^\top W_a\bar{h}_s\); **concat** \(W_a[h_t;\bar{h}_s]\).  
  Location baseline: \(a_t=\text{softmax}(W_a h_t)\) (Eq. 9). Context \(c_t=\sum_s a_t(s)\bar{h}_s\).
- **Local attention (Section 3.2):** attend to window \([p_t-D,p_t+D]\), fixed \(a_t\in\mathbb{R}^{2D+1}\).  
  - **local-m:** \(p_t=t\).  
  - **local-p:** \(p_t=S\cdot\sigma(v_p^\top\tanh(W_p h_t))\) (Eq. 10); apply Gaussian bias  
    \(a_t(s)=\text{align}(h_t,\bar{h}_s)\exp(-(s-p_t)^2/(2\sigma^2))\), with \(\sigma=D/2\) (Eq. 11).
- **Input-feeding (Section 3.3):** feed \(\tilde{h}_t\) as part of next-step input to model coverage; if LSTM size \(n\), first-layer input becomes \(2n\).
- **Training defaults (Section 4.1):** WMT’14 4.5M pairs; vocab 50K each; filter length >50; 4-layer LSTM, 1000 cells/layer, 1000-d embeddings; SGD 10 epochs (dropout: 12); LR=1 then halve after epoch 5 (dropout: after 8); batch 128; grad clip norm 5; init U[-0.1,0.1].
- **Key En→De results (Table 1, tokenized BLEU newstest2014):**  
  Base 11.3; +reverse 12.6 (+1.3); +dropout 14.0 (+1.4); +global attn (location) 16.8 (+2.8); +feed 18.1 (+1.3); +local-p (general)+feed 19.0 (+0.9); +unk replace 20.9 (+1.9); ensemble(8)+unk 23.0.
- **WMT’15 En→De (Table 2, NIST BLEU newstest2015):** ensemble(8)+unk **25.9** vs prior SOTA 24.9.
- **De→En (Table 3, BLEU):** base(reverse) 16.9; +global(location) 19.1 (+2.2); +feed 20.1 (+1.0); +global(dot)+drop+feed 22.8 (+2.7); +unk 24.9 (+2.1).
- **Architecture ablation (Table 4):** global(dot) BLEU 18.6 (20.5 after unk); local-p(general) BLEU 19.0 (20.9 after unk). Location aligns poorly (smaller unk-replace gain: +1.2).
- **Alignment quality (Table 6, AER):** global(location) 0.39; local-m(general) 0.34; local-p(general) 0.36; ensemble 0.34; Berkeley aligner 0.32.

## When to surface
Use when students ask how Luong attention is computed (global/local, dot vs general vs concat), why local attention is cheaper, or what empirical BLEU/AER gains come from input-feeding, local-p, and different scoring functions on WMT En↔De.