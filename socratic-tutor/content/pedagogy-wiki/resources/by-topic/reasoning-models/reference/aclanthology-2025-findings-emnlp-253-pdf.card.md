# Card: PRM for reflective (long-CoT) math reasoning
**Source:** https://aclanthology.org/2025.findings-emnlp.253.pdf  
**Role:** paper | **Need:** [FORMULA_SOURCE]  
**Anchor:** Formal PRM training objective + reflective-step labeling rules (Error Propagation/Cessation) + evaluation procedures (BoN vs step-search) with concrete results.

## Key Content
- **PRM vs ORM (Section 2):**  
  - **ORM** scores whole solutions via final answer.  
  - **PRM** scores **individual steps** to provide granular intermediate feedback for search/RL.
- **Reflective long-CoT labeling problem (Section 1, 3):** Traditional PRM datasets truncate incorrect solutions at the **first error**, assuming all later steps wrong—fails when models **self-correct** after mistakes.
- **New step-label rules (Section 4.2):**  
  - **Error Propagation:** if earlier steps are incorrect and current step **builds on** them without correction/new approach ⇒ label **incorrect**.  
  - **Error Cessation:** if earlier steps are incorrect but current step **corrects** them or starts a **new error-free approach** ⇒ label **correct**.
- **LLM judge annotation (Section 4.3, Appx B/E):** Incorporate the above rules into a judge prompt; reported step-annotation accuracy: **o1 = 0.963**, **claude-3.5-sonnet = 0.726**, **gpt-4o-2024-08-06 = 0.668** (Table 8).
- **PRM training objective (Eq. 1):** binary step classification with cross-entropy over steps  
  \[
  L_{\text{PRM}}=\sum_{i=0}^{K}\hat y_i\log y_i+(1-\hat y_i)\log(1-y_i)
  \]
  where \(K\)=#steps; \(y_i\)=gold label for step \(s_i\); \(\hat y_i=\text{PRM}(\text{prompt}, s_{\le i})\)=predicted probability/score for step \(s_i\).
- **Evaluation metrics (Section 5.1.3):**  
  - **PRM@N (Best-of-N):** pick best among N candidates using **final-step score**.  
  - **PRM@N-step (Online search):** at each step sample N continuations, choose top-scoring step to continue.
- **Key results (Table 2):** “Ours” PRM: **MATH500 PRM@64 = 0.816**, **PRM@8-step = 0.750**; **AIME2024 PRM@64 = 0.267**, **PRM@8-step = 0.167**; step-level **F1 = 0.828** (Precision 0.850, Recall 0.806).
- **Hyperparameters:** Generator SFT: lr **1e-5**, epochs **3**, batch **24**, max len **16384** (Table 6). PRM training: lr **1e-6**, epochs **1**, batch **256**, max len **10240** (Table 7).

## When to surface
Use when students ask how PRMs are **formally trained/scored per step**, how to label steps in **self-correcting long-CoT**, or how PRMs are evaluated via **BoN vs step-level search** with concrete metrics.