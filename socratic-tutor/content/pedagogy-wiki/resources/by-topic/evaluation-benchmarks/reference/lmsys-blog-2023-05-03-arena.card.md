# Card: Chatbot Arena Elo Leaderboard (Anonymous Pairwise Human Votes)
**Source:** https://www.lmsys.org/blog/2023-05-03-arena/  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Elo-based leaderboard methodology for Chatbot Arena (anonymous randomized battles, Elo computation framing, initial results)

## Key Content
- **Benchmark setup (workflow):**
  - Users chat with **two anonymous models side-by-side** and **vote** for the better answer; **model names revealed only after voting**.
  - Platform **logs interactions**; analysis uses **only votes where names were hidden** (anonymous votes).
  - Initial launch collected **4.7k valid anonymous votes** in ~1 week.
  - Pairing policy: initially **non-uniform** (biased toward “strong pairings” based on prior ranking), later switched to **uniform sampling** for better coverage; introduced **fastchat-t5-3b** late → non-uniform model frequency.
  - Prompts are “in the wild”; language distribution: **mostly English** (top-15 languages plotted).
- **Elo model (Eq. 1–2):**
  - **Win probability (logistic, base 10):**  
    **Eq. 1:** \(E_A = \frac{1}{1 + 10^{(R_B - R_A)/400}}\)  
    where \(R_A, R_B\) are Elo ratings; \(E_A\) is expected score/probability A wins.
  - **Rating update:**  
    **Eq. 2:** \(R'_A = R_A + K(S_A - E_A)\)  
    where \(S_A\) is actual score (win=1, tie=0.5, loss=0); \(K\) is update factor.
- **Empirical results (initial leaderboard):**
  - **Timeframe:** **Apr 24 – May 1, 2023**; **9 models** listed; ratings computed from the **4.7k votes** (notebook linked in post).
  - Pairwise win-rate heatmap shown; **Elo-predicted win rates match observed win rates “relatively well.”**
- **Design rationale:** Pairwise human preference handles **open-ended** assistant quality; Elo provides **scalability**, **incrementality** (new model needs fewer trials), and a **unique ordering** across many models.

## When to surface
Use when students ask how Chatbot Arena ranks LLMs, how Elo is computed/updated from pairwise votes, or why Elo-style crowdsourced evaluation is used for open-ended chatbot benchmarking.