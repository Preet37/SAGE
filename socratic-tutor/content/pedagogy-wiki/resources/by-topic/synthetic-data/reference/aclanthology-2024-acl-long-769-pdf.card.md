# Card: Superfiltering (Weak-to-Strong Instruction-Data Filtering via IFD)
**Source:** https://aclanthology.org/2024.acl-long.769.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** Ablation results + threshold/budget trade-offs for weak-to-strong instruction-data filtering and downstream benchmark impacts.

## Key Content
- **Perplexity (Eq. 1):**  
  \[
  \mathrm{PPL}(y_i|x_i)=\exp\left(-\frac{1}{N}\sum_{j=1}^{N}\log p(y_{i,j}\mid x_i,y_{i,1..j-1})\right)
  \]  
  *Defs:* \(x_i\)=instruction (incl. optional input), \(y_i\)=response, \(N\)=#tokens in \(y_i\).
- **Instruction-Following Difficulty (IFD) (Eq. 2):**  
  \[
  \mathrm{IFD}(y_i|x_i)=\frac{\mathrm{PPL}(y_i|x_i)}{\mathrm{PPL}(y_i)}
  \]  
  Higher IFD ⇒ instruction provides less help ⇒ “harder” sample.
- **Procedure (Section 3.3):** Use a *weak* pretrained LM (GPT-2 124M) **without extra training** to compute IFD for each sample; select **top k% with highest IFD under 1**; finetune *strong* student (LLaMA2-7B/13B).
- **Weak-to-strong consistency (Table 1):** Spearman rank correlation vs LLaMA2-7B is high even for GPT-2. Example (Alpaca): ρ(PPL)=0.726, ρ(IFD)=0.679. Wizard70k: ρ(IFD)=0.802 (GPT-2). Overlap of selected sets increases with budget (e.g., Alpaca GPT-2 overlap: 5%→0.28, 10%→0.41, 15%→0.49).
- **Downstream gains with small budgets (Table 2):**  
  Alpaca + LLaMA2-7B: **5%** data (2,600) Pairwise Winning Score **1.133** vs 100%; AlpacaEval win rate **33.04** vs **27.75**.  
  Alpaca-GPT4 + LLaMA2-13B: **10%** data (5,200) Avg **63.65** vs **60.81** (100%).
- **Ablation—strategy & filter model (Table 3, Alpaca→LLaMA2-7B):**  
  Random (5%): **0.936**; Diversity (5%): **0.927**; **Perplexity-based** (5%): **0.261** (bad).  
  IFD filters: GPT-2 (Superfilter) **1.133**; GPT-NEO **1.096**; LLaMA2-7B filter **1.303** (best).
- **Cost/latency (Table 4):** Filtering time: Superfiltering **8 min** vs ChatGPT-score **120 min**, reward-model **1400 min**, IFD using LLaMA2-7B **161 min**; Superfiltering reported **~20× faster** than filtering with LLaMA2-7B.
- **Training defaults (Section 4.2):** Adam; LR **2e-5** (LLaMA2-7B), **1e-5** (13B); batch **128**; **3 epochs**; max length **2048**; warmup **0.03**.

## When to surface
Use when students ask how to **filter synthetic/self-instruct instruction data cheaply**, how **filtering thresholds (5/10/15%)** affect quality, or why **IFD beats perplexity/random/diversity** and what the **measured speed/performance trade-offs** are.