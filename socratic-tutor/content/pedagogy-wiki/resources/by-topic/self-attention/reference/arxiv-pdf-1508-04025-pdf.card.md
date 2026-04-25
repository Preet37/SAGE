# Card: Luong (Multiplicative) Attention — Global & Local (2015)
**Source:** https://arxiv.org/pdf/1508.04025.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Exact equations for global attention score functions + local attention (predictive \(p_t\) + Gaussian window) and training/inference details.

## Key Content
- **Decoder objective (Eq. 1–4):**  
  \(\log p(\mathbf{y}|\mathbf{x})=\sum_{j=1}^m \log p(y_j|y_{<j},\mathbf{s})\) (Eq. 1);  
  \(p(y_j|y_{<j},\mathbf{s})=\text{softmax}(g(h_j))\) (Eq. 2); \(h_j=f(h_{j-1},\mathbf{s})\) (Eq. 3);  
  training loss \(J=\sum_{(x,y)\in D}-\log p(y|x)\) (Eq. 4).
- **Attention output layer (Eq. 5–6):**  
  \(\tilde h_t=\tanh(W_c[c_t;h_t])\) (Eq. 5);  
  \(p(y_t|y_{<t},x)=\text{softmax}(W_s\tilde h_t)\) (Eq. 6).
- **Global attention alignment (Eq. 7–8, Sec. 3.1):**  
  \(a_t(s)=\frac{\exp(\text{score}(h_t,\bar h_s))}{\sum_{s'}\exp(\text{score}(h_t,\bar h_{s'}))}\) (Eq. 7).  
  Score functions:  
  **dot:** \(\text{score}=h_t^\top \bar h_s\)  
  **general (bilinear):** \(\text{score}=h_t^\top W_a \bar h_s\)  
  **concat:** \(\text{score}=v_a^\top \tanh(W_a[h_t;\bar h_s])\)  
  Location baseline: \(a_t=\text{softmax}(W_a h_t)\) (Eq. 8).  
  Context: \(c_t=\sum_s a_t(s)\bar h_s\) (described after Eq. 7).
- **Local attention (Sec. 3.2):** window \([p_t-D,p_t+D]\), fixed \(a_t\in\mathbb{R}^{2D+1}\).  
  **local-m:** \(p_t=t\).  
  **local-p predictive position:** \(p_t=S\cdot \sigma(v_p^\top\tanh(W_p h_t))\) (Eq. 9), \(S=\) source length.  
  Gaussian bias: \(a_t(s)=\text{align}(h_t,\bar h_s)\exp\!\left(-\frac{(s-p_t)^2}{2\sigma^2}\right)\) (Eq. 10), with \(\sigma=D/2\).
- **Input-feeding (Sec. 3.3):** feed \(\tilde h_t\) as part of next-step input to model past alignment/coverage; if LSTM size \(n\), first-layer input becomes \(2n\).
- **Defaults / training (Sec. 4.1):** WMT’14 4.5M pairs; vocab top 50K each; filter length \(>50\); 4-layer LSTM, 1000 cells/layer, 1000-d embeddings; init \([-0.1,0.1]\); SGD 10 epochs (LR=1, halve after epoch 5); batch 128; clip/rescale grad norm \(>5\); dropout \(0.2\) (train 12 epochs, halve after epoch 8); local window \(D=10\).
- **Key results (Tables 1–4):** En→De: baseline+reverse+dropout BLEU 14.0; +global(location) 16.8; +feed 18.1; +local-p(general)+feed 19.0; +unk replace 20.9; ensemble(8)+unk 23.0 (tokenized BLEU, newstest2014). WMT’15 En→De: 25.9 NIST BLEU (Table 2). Architecture comparison (Table 4): global(dot) 18.6→20.5 after unk; local-p(general) best 19.0→20.9.

## When to surface
Use when students ask for the *exact Luong attention equations* (dot/general/concat; local-p \(p_t\) and Gaussian window), or for concrete training hyperparameters and reported BLEU gains of global vs local attention and input-feeding.