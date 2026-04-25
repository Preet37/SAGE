# Card: RLHF for Summarization (Reward Model + PPO w/ KL)
**Source:** https://proceedings.neurips.cc/paper/2020/file/1f89885d556929e98d3ef9b86448f951-Paper.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Pairwise preference reward-model likelihood (Bradley–Terry/logistic) + KL-regularized PPO fine-tuning setup end-to-end.

## Key Content
- **Pipeline (Section 3.1; Fig. 2):**
  1) Start from **SFT policy** on TL;DR.  
  2) **Collect human comparisons**: for each post *x*, sample summaries from multiple sources (current policy, initial policy, reference, baselines); humans choose better of a pair.  
  3) **Train reward model (RM)** on comparisons.  
  4) **RL fine-tune policy** with PPO to maximize RM reward; repeat iteratively.
- **RM objective = pairwise preference logistic (Section 3.4; Fig. 2):**  
  For comparison data \((x, y^0, y^1, i)\sim D\) where human prefers \(y^i\):  
  **(Eq. RM-loss)** \[
  \text{loss}(r_\theta)=\mathbb{E}\big[\log \sigma(r_\theta(x,y^i)-r_\theta(x,y^{1-i}))\big]
  \]
  - \(r_\theta(x,y)\): scalar RM score (logit); \(\sigma\): logistic sigmoid; \(D\): human judgments dataset.  
  - RM outputs **normalized** so dataset reference summaries have **mean score 0**.
- **RL reward with KL penalty (Section 3.4):**  
  **(Eq. PPO-reward)** \[
  R(x,y)=r_\theta(x,y)-\beta \log\frac{\pi^{RL}_\phi(y|x)}{\pi^{SFT}(y|x)}
  \]
  - \(\pi^{RL}_\phi\): learned policy; \(\pi^{SFT}\): original supervised model; \(\beta\): KL coefficient.  
  - Rationale: KL term (i) encourages exploration / prevents mode collapse, (ii) keeps policy near RM training distribution.
- **RL setup defaults (Section 3.4):** reward only at end of summary; episode ends at EOS; **discount \(\gamma=1\)**; PPO time step = **BPE token**. Separate **value network** (Transformer) to avoid damaging pretrained policy; value net initialized from RM parameters.
- **Key empirical numbers (Section 4.1):**
  - On TL;DR, **1.3B RLHF** preferred over reference **61%** vs **6.7B SFT 43%** (raw preference vs reference).  
  - Length-control reduces RLHF-vs-reference preference by **~5%**, but **6.7B RLHF still ~65%** preferred vs reference.
- **Over-optimization finding (Section 4.3; Fig. 5):** increasing optimization strength (via KL coefficient/penalty) initially improves human preference, then degrades; RM predictions can become **anti-correlated** with human preferences.
- **Data scale (Section 4.3; Fig. 6):** doubling RM training data → **~+1.1%** validation accuracy; doubling model size → **~+1.8%**.
- **Human data quality (Section 3.3):** labeler–researcher agreement **77% ± 2%**; researcher–researcher **73% ± 4%**.
- **Compute cost (Section 5):** 6.7B RL fine-tuning ≈ **320 GPU-days**.

## When to surface
Use for questions about **RLHF math** (pairwise preference RM / Bradley–Terry likelihood), **KL-regularized PPO reward**, and concrete evidence on **RLHF vs SFT** and **over-optimizing reward models**.