# Card: Scheduled Sampling (Teacher Forcing → Free-Running)
**Source:** https://proceedings.neurips.cc/paper/2015/file/e995f98d56967d946471af29d7bf99f1-Paper.pdf  
**Role:** paper | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Step-by-step teacher forcing vs inference mismatch (exposure bias) + scheduled-sampling algorithm & schedules.

## Key Content
- **Seq model likelihood (Eq. 1–3):** For target tokens \(y_{1:T}\) given input \(X\):  
  \[
  \log P(Y|X)=\sum_{t=1}^{T}\log P(y_t \mid y_{1:t-1},X)
  \]
  with RNN state \(h_t\): \(\log P(y_t|y_{1:t-1},X;\theta)=\log P(y_t|h_t;\theta)\) (Eq. 2) and  
  \[
  h_t=\begin{cases}
  f(X;\theta) & t=1\\
  f(h_{t-1}, y_{t-1};\theta) & t>1
  \end{cases}
  \]
  (Eq. 3). Softmax over vocab; add **\<EOS\>** to end sequences; decode until \<EOS\>.
- **Training objective (Eq. 4):** \(\theta^*=\arg\max_\theta \sum_{(X^i,Y^i)} \log P(Y^i|X^i;\theta)\).
- **Inference procedure (Section 2.3):** autoregressive decoding uses previous **generated** token \(\hat y_{t-1}\) (argmax or sample); beam search keeps \(m\) candidates each step, returns \(k\) best; early mistakes compound because model visits unseen states.
- **Exposure bias rationale (Abstract/2.3):** mismatch: training conditions on true \(y_{t-1}\) (teacher forcing) but inference conditions on \(\hat y_{t-1}\) → error accumulation.
- **Scheduled Sampling algorithm (Section 2.4):** during training, **flip a coin at every time step**: use true \(y_{t-1}\) w.p. \(\epsilon_i\), else use model token \(\hat y_{t-1}\) w.p. \(1-\epsilon_i\). Per-token coin worked better than per-sequence (per-sequence “much worse”).
- **Schedules for \(\epsilon_i\) (Fig. 2):**
  - Linear: \(\epsilon_i=\max(\epsilon, k-ci)\)
  - Exponential: \(\epsilon_i=k^i\) (with \(k<1\))
  - Inverse sigmoid: \(\epsilon_i=\frac{k}{k+\exp(i/k)}\)
- **No backprop through sampling decision** in experiments (noted future work).

**Key empirical results**
- **MSCOCO captioning (Table 1, dev):** Baseline BLEU-4/METEOR/CIDEr = **28.8/24.2/89.5**; Scheduled Sampling = **30.6/24.3/92.1**; Always Sampling = **11.2/15.7/49.7**; Uniform Scheduled Sampling = **29.2/24.2/90.9**; Baseline ensemble(10)=**30.7/25.1/95.7**; SS ensemble(5)=**32.3/25.4/98.7**.
- **Parsing (Table 2, WSJ22 dev F1):** Baseline **86.54**; +Dropout **87.0**; Scheduled Sampling **88.08**; SS+Dropout **88.68**; Always Sampling invalid (“-”).
- **Speech (Table 3, TIMIT):** Baseline next-step FER **15.0** but decoding FER **46.0**; Always Sampling next-step **34.6**, decoding **35.8**; Scheduled Sampling 1 (\(\epsilon_s=0.25\to \epsilon_e=0\)) decoding **34.5**.

## When to surface
Use when students ask why teacher forcing can fail at test time (exposure bias), how scheduled sampling works (coin flip + \(\epsilon_i\) schedules), or want concrete schedule formulas and benchmark improvements.