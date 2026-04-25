# Card: Pick-a-Pic & PickScore (preference-based scoring for T2I)
**Source:** https://proceedings.neurips.cc/paper_files/paper/2023/file/73aacd8b3b05b4b503d58310b523553c-Paper-Conference.pdf  
**Role:** paper | **Need:** COMPARISON_DATA  
**Anchor:** Pick-a-Pic dataset construction; PickScore model/objective; evidence PickScore correlates with human preferences better than baselines; guidance for evaluation/reranking.

## Key Content
- **Dataset (Section 2):** Each example = *(prompt x, two generated images y1,y2, label: prefer y1 / prefer y2 / tie)*. Built via web app loop: user sees 2 images → picks preferred/tie → rejected image replaced → repeat until prompt changes (Fig. 2).  
  - Paper experiments use NSFW-filtered snapshot: **583,747 train**, **500 val**, **500 test**; **37,523 prompts**, **4,375 users** (train). Overall logged: **968,965 rankings**, **66,798 prompts**, **6,394 users**.
  - Images generated from **SD 2.1**, **Dreamlike Photoreal 2.0**, **SDXL variants**, varying **classifier-free guidance (CFG)**.
  - Split procedure: sample **1000 prompts** (unique users) → split into val/test prompts; **1 example per prompt** in val/test; train excludes those prompts.
- **PickScore model (Eq. 1, Section 3):** CLIP-style scorer  
  - \(s(x,y)=E_{txt}(x)\cdot E_{img}(y)\cdot T\) where \(T\) is learned scalar temperature.
- **Preference objective (Eqs. 2–3):** preference distribution \(p=[1,0]\) (y1 wins), \([0,1]\) (y2 wins), \([0.5,0.5]\) (tie).  
  - \(\hat p_i=\frac{\exp s(x,y_i)}{\sum_{j=1}^2 \exp s(x,y_j)}\)  
  - \(L_{pref}=\sum_{i=1}^2 p_i(\log p_i-\log \hat p_i)\) (KL). Batch loss weighted inversely by prompt frequency (reduce overfitting to frequent prompts). In-batch negatives tried; worse (**65.2** vs PickScore **70.5** accuracy).
- **Training defaults (Section 3):** finetune **CLIP-H** for **4000 steps**, **lr 3e-6**, **batch 128**, **warmup 500**, linear decay; best checkpoint by val accuracy every 100 steps; ~<1 hour on **8×A100**.
- **Preference prediction results (Table 1b):** Accuracy on test (tie-aware metric): **PickScore 70.5%**, **Human expert 68.0%**, **HPS 66.7%**, **ImageReward 61.1%**, **CLIP-H 60.8%**, **Aesthetics 56.8%**, **Random 56.8%**. Tie threshold \(t\): predict tie if \(|\hat p_1-\hat p_2|<t\) (selected on val).
- **Model evaluation (Section 5):**
  - On **MS-COCO** captions: Spearman correlation with human win-rates: **PickScore 0.917** vs **FID -0.900** (FID prompt-agnostic; CFG confound—higher CFG preferred by humans but worsens FID).
  - Using real user prefs (Pick-a-Pic test; **14k** prefs; **45 models**) Elo correlation with users: **PickScore 0.790±0.054**, **HPS 0.670±0.071**, **ImageReward 0.492±0.086**, **CLIP-H 0.313±0.075**.
- **Reranking (Section 6, Table 2):** Generate **100 images/prompt** (Dreamlike Photoreal 2.0, **CFG 7.5**, **5 seeds × 20 prompt templates**). Humans prefer PickScore-selected image vs: **Random seed+null template 71.4%**, **Random template 82.0%**, **Aesthetics 85.1%**, **CLIP-H 71.3%**.

## When to surface
Use when students ask how to **evaluate/rerank text-to-image models** with human-aligned metrics, why **FID can mislead**, or how **preference datasets + CLIP-based reward models** (PickScore) are trained and validated.