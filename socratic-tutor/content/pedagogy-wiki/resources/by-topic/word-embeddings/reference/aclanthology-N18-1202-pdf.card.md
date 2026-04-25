# Card: Deep contextualized word representations (ELMo)
**Source:** https://aclanthology.org/N18-1202.pdf  
**Role:** paper | **Need:** COMPARISON_DATA  
**Anchor:** Concrete contextual-vs-static embedding definition via biLM token embeddings + six-task benchmark gains

## Key Content
- **Contextual vs. static:** Traditional word *type* embeddings (e.g., GloVe/word2vec) give **one context-independent vector per word**. ELMo assigns **each token** a vector **as a function of the entire sentence** (Sec. 1, 3).
- **biLM objective (Sec. 3.1):** For tokens \((t_1,\dots,t_N)\)  
  Forward LM: \(p(t_{1:N})=\prod_{k=1}^N p(t_k\mid t_{1:k-1})\)  
  Backward LM: \(p(t_{1:N})=\prod_{k=1}^N p(t_k\mid t_{k+1:N})\)  
  Joint training maximizes \(\sum_{k=1}^N [\log p(t_k\mid t_{1:k-1})+\log p(t_k\mid t_{k+1:N})]\), tying token-repr params \(\Theta_x\) and softmax \(\Theta_s\) across directions.
- **ELMo layer mixing (Eq. 1, Sec. 3.2):** For token \(k\), representations  
  \(R_k=\{h^{LM}_{k,j}\mid j=0..L\}\), where \(h^{LM}_{k,0}=x^{LM}_k\) (token layer) and \(h^{LM}_{k,j}=[\overrightarrow{h}^{LM}_{k,j};\overleftarrow{h}^{LM}_{k,j}]\).  
  Task vector: \(\mathrm{ELMo}^{task}_k=\gamma^{task}\sum_{j=0}^L s^{task}_j\, h^{LM}_{k,j}\), with \(s^{task}\) softmax-normalized; \(\gamma\) is a learned scalar.
- **Pipeline (Sec. 3.3):** Pretrain biLM → **freeze** biLM weights → concatenate \([x_k;\mathrm{ELMo}_k]\) into supervised model input; sometimes also concatenate at RNN output \([h_k;\mathrm{ELMo}_k]\). Use dropout on ELMo; optional L2 regularization on layer weights toward uniform average.
- **biLM architecture/defaults (Sec. 3.4):** \(L=2\) biLSTM layers; **4096** units with **512-d** projections; residual connection between layers. Character CNN: **2048** char n-gram filters → 2 highway layers → project to **512**. Trained **10 epochs** on **1B Word Benchmark (~30M sentences)**; avg forward/backward perplexity **39.7**.
- **Six-task gains (Table 1):**  
  - **SQuAD F1:** 81.1 → **85.8** (+4.7; **24.9%** rel. error reduction)  
  - **SNLI acc:** 88.0 → **88.7** (+0.7; 5.8%)  
  - **SRL F1:** 81.4 → **84.6** (+3.2; 17.2%)  
  - **Coref avg F1:** 67.2 → **70.4** (+3.2; 9.8%)  
  - **NER F1:** 90.15 → **92.22** (+2.06; 21%)  
  - **SST-5 acc:** 51.4 → **54.7** (+3.3; 6.8%)
- **Ablations (Tables 2,7):** Using **all layers** > last-only (e.g., SQuAD dev: baseline 80.8; last-only 84.7; all layers up to **85.2** with \(\lambda=0.001\)). Gains mainly from **contextual** layers, not just char/subword token layer (SQuAD dev: GloVe 80.8 vs char-only 81.4 vs full ELMo 85.6 with GloVe).

## When to surface
Use when students ask how **contextual embeddings** differ from **static** ones, how ELMo is computed (biLM + **layer mixing Eq. 1**), or when they want **benchmark evidence** that contextual embeddings improve downstream NLP tasks.