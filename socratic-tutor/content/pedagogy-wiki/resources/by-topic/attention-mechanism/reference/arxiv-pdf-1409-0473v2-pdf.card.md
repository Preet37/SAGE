# Card: Attention vs Fixed-Vector Bottleneck in Seq2Seq NMT (Bahdanau et al., 2014)
**Source:** https://www.arxiv.org/pdf/1409.0473v2.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** Empirical evidence that fixed-length context-vector encoder–decoder degrades with longer sentences; attention model stays robust (Fig. 2, Table 1).

## Key Content
- **Baseline encoder–decoder (fixed context)**
  - Encoder RNN: \(h_t=f(x_t,h_{t-1})\) (Eq. 1); context \(c=q(\{h_1,\dots,h_{T_x}\})\) (often \(c=h_{T_x}\)).
  - Decoder factorization: \(p(y)=\prod_{t=1}^{T_y} p(y_t\mid y_{<t},c)\) (Eq. 2); modeled as \(p(y_t\mid y_{<t},c)=g(y_{t-1},s_t,c)\) (Eq. 3).
- **Attention / “RNNsearch” (variable context per target word)**
  - \(p(y_i\mid y_{<i},x)=g(y_{i-1},s_i,c_i)\) (Eq. 4), with \(s_i=f(s_{i-1},y_{i-1},c_i)\).
  - Context: \(c_i=\sum_{j=1}^{T_x}\alpha_{ij}h_j\) (Eq. 5).
  - Soft alignment: \(\alpha_{ij}=\frac{\exp(e_{ij})}{\sum_{k=1}^{T_x}\exp(e_{ik})}\) (Eq. 6), \(e_{ij}=a(s_{i-1},h_j)\); \(a\) is a small FFNN (Sec. 3.1, 3.3.2).
  - Encoder uses **BiRNN** annotations \(h_j=[\overrightarrow{h_j};\overleftarrow{h_j}]\) (Sec. 3.2).
- **Design rationale:** fixed-length \(c\) is an **information bottleneck**; attention “soft-searches” relevant source positions each step, improving long-sentence handling (Intro, Sec. 5.2.2).
- **Empirical results (WMT’14 En→Fr)**
  - **BLEU (Table 1, All / No-UNK):** RNNenc-30 **13.93 / 24.19**; RNNsearch-30 **21.50 / 31.44**; RNNenc-50 **17.82 / 26.71**; RNNsearch-50 **26.75 / 34.16**; Moses **33.30 / 35.63**.
  - **Length effect (Fig. 2):** RNNenc BLEU drops sharply as sentence length increases; RNNsearch-50 shows **no deterioration up to ≥50 words**.
- **Training/config defaults (Secs. 4, Appx A/B):** vocab shortlist 30k each side; hidden size \(n=1000\), embeddings \(m=620\), maxout layer \(l=500\), alignment MLP hidden \(n'=1000\); minibatch 80; Adadelta \(\rho=0.95,\epsilon=10^{-6}\); gradient norm clip to 1; beam search decoding.

## When to surface
Use when students ask why vanilla seq2seq struggles on long inputs, what “context vector bottleneck” means, or what empirical evidence motivated attention (length-bucketed BLEU + Table 1 comparisons).