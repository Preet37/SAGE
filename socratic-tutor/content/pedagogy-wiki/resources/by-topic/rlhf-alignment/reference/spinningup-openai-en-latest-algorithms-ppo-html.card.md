# Card: PPO-Clip objective + KL early stopping (Spinning Up)
**Source:** https://spinningup.openai.com/en/latest/algorithms/ppo.html  
**Role:** reference_doc | **Need:** FORMULA_SOURCE  
**Anchor:** Side-by-side PPO-Clip vs PPO-Penalty framing; explicit PPO-Clip surrogate objective + intuition; practical KL target / early stopping; implementation hyperparameters.

## Key Content
- **Motivation (Background):** Take the largest improvement step using current on-policy data **without** moving policy so far that performance collapses. PPO is a simpler first-order alternative to TRPO.
- **Two PPO variants:**
  - **PPO-Penalty:** adds a **KL-divergence penalty** to approximate a KL-constrained update; **automatically adjusts** penalty coefficient during training.
  - **PPO-Clip (focus; “primary variant used at OpenAI”):** **no KL term / no hard constraint**; uses **clipping** to remove incentives to move far from old policy.
- **PPO-Clip surrogate objective (Eq. 1, simplified form):**  
  Let \(r_t(\theta)=\frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)}\), advantage \(\hat A_t\), clip \(\epsilon\).  
  \[
  L^{\text{CLIP}}(\theta)=\mathbb{E}_t\Big[\min\big(r_t(\theta)\hat A_t,\ \text{clip}(r_t(\theta),1-\epsilon,1+\epsilon)\hat A_t\big)\Big].
  \]
  **Intuition:**  
  - If \(\hat A_t>0\): objective increases with \(r_t\) until \(r_t>1+\epsilon\), then capped at \((1+\epsilon)\hat A_t\).  
  - If \(\hat A_t<0\): objective increases as \(r_t\) decreases until \(r_t<1-\epsilon\), then capped at \((1-\epsilon)\hat A_t\).
- **Procedure detail (“You Should Know”):** Despite clipping, policy can drift; Spinning Up uses **early stopping**: stop policy gradient steps if **mean KL(new‖old)** exceeds a threshold.
- **Defaults / key hyperparameters (PyTorch/TF docs):**
  - `clip_ratio` \(\epsilon\): **0.1–0.3 typical**, default **0.2**
  - `target_kl`: **0.01 or 0.05 typical**, default **0.01** (used for early stopping)
  - `steps_per_epoch` **4000**, `epochs` **50**, `gamma` **0.99**, `lam` **0.97**
  - `train_pi_iters` **80** (max; may stop early), `train_v_iters` **80**
  - `pi_lr` **3e-4**, `vf_lr` **1e-3**, `max_ep_len` **1000**
- **Implementation note:** PPO does **multiple minibatch SGD steps** per epoch to maximize \(L^{CLIP}\); on-policy sampling from current stochastic policy.

## When to surface
Use when students ask for the **exact PPO-Clip loss**, what **clip_ratio/target_kl** mean, or how PPO trainers (incl. RLHF-style PPO) use **KL monitoring / early stopping** to prevent overly large policy updates.