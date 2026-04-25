# Card: Auto Evol-Instruct (Evol-Instruct automation)
**Source:** https://aclanthology.org/anthology-files/pdf/emnlp/2024.emnlp-main.397.pdf  
**Role:** paper | **Need:** WORKING_EXAMPLE  
**Anchor:** End-to-end evol-style synthetic instruction refinement (mutations/operators via prompts, trajectory analysis, selection by failure rate) + benchmark gains from iterative refinement.

## Key Content
- **Goal / optimization objective (Eq. 1):** find evolving method \(e^*\) maximizing post-SFT performance on evolved data:  
  \[
  e^*=\arg\max_e Q(X_e)
  \]
  where \(X=\{x_i\}\) is seed instruction-response data, \(e\) is an evolving method (prompt/rules), \(X_e\) is evolved dataset, \(Q(\cdot)\) is benchmark score after instruction tuning.
- **Core workflow (Section 3, Fig. 1):**
  1) Start with **universal initial evolving method** \(e_0\) (Fig. 2: Step1 list methods to increase complexity; Step2 plan; Step3 rewrite adding **10–20 words**; Step4 review for reasonableness; no language change).  
  2) For step \(t\): sample minibatch from \(X\); evol LLM evolves each instruction **\(l\) rounds** → trajectory \(S_t=\{X_t, X_t^{(1)},...,X_t^{(l)}\}\).  
  3) **Optimizer LLM** does **trajectory analysis** (Fig. 7 prompt) → feedback \(f_t\).  
  4) **Method optimization** updates \(e_{t-1}\to e_t\) using \(f_t\).  
  5) Run **m parallel optimizations** (sampling decoding); select \(e_t\) with lowest failure rate on dev set \(D\).
- **Selection metric (Eq. 2):** evolution failure rate  
  \[
  \lambda_{R^{e_t}}=\frac{\sum_{r\in R^{e_t}}F(r)}{|D|}
  \]
  where \(R^{e_t}\) are responses for evolved dev instructions; \(F(r)\in\{0,1\}\) flags failures (Appendix A: “Understood/Thank you…?” stagnant complexity; “Sure…?” insufficient qualification; contains “please provide” loss of key info).
- **Key results (Table 2):**  
  - **Large models:** Seed→Auto: MT-Bench **7.65→8.09 (+0.44)**; AlpacaEval **87.98→91.37 (+3.39)**; GSM8K **70.60→82.49 (+11.89)**; HumanEval **72.00→77.40 (+5.4)**.  
  - **Small models:** Seed→Auto: MT-Bench **6.88→7.51 (+0.63)**; GSM8K **56.90→70.74 (+13.84)**; HumanEval **57.90→65.85 (+7.95)**.
- **Defaults/params (Table 1):** seed sizes: ShareGPT **10K**, GSM8K-train **7K**, Code Alpaca **20K**; method-optimization uses ~**2,000** sampled entries; evol/optimizer often **GPT-4** (paper also tests GPT-3.5 vs GPT-4; Table 3: Auto with GPT-4 evol LLM on GSM8K **70.7** vs GPT-3.5 **64.4**).

## When to surface
Use when students ask how “Evol-Instruct” can be automated end-to-end, how to score/select synthetic-data mutation prompts, or what empirical gains iterative instruction evolution yields on MT-Bench/GSM8K/HumanEval.