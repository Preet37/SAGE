## Core Definitions

**Language model (LM).** A language model assigns probabilities to sequences of tokens by factorizing the joint probability into a product of next-token conditional probabilities: \(P(x_{1:T})=\prod_{i=1}^{T}P(x_i\mid x_{1:i-1})\). This is the standard autoregressive factorization used for generation token-by-token. (Holtzman et al., 2019, Eq. 1: https://arxiv.org/abs/1904.09751)

**Next-token prediction.** Next-token prediction is the training/evaluation setup where, given a context \(c\) (a prefix of tokens), the model outputs a probability distribution \(p(\cdot\mid c)\) over the vocabulary for the next token, and is scored by the log-probability it assigns to the true next token \(t\): \(-\log p(t\mid c)\). (Perplexity paper, 2022, Eq. 1: https://arxiv.org/html/2212.11281v2)

**Autoregressive generation.** Autoregressive generation is the inference-time procedure that produces text by repeatedly (1) computing the next-token distribution \(P(x\mid x_{1:i-1})\) and (2) selecting a token using a decoding strategy (greedy/beam/sampling variants), appending it to the context, and continuing. This follows directly from the LM factorization. (Holtzman et al., 2019: https://arxiv.org/abs/1904.09751)

**Temperature.** Temperature is a scalar \(t>0\) applied to logits before softmax to control the sharpness of the next-token distribution: \(p(x=V_l\mid x_{1:i-1})=\frac{\exp(u_l/t)}{\sum_{l'}\exp(u_{l'}/t)}\). Lower \(t\) concentrates probability mass on high-logit tokens (less diversity); higher \(t\) flattens the distribution (more diversity). (Holtzman et al., 2019, Eq. 4: https://arxiv.org/abs/1904.09751)

**Top‑p sampling (nucleus sampling).** Nucleus (top‑p) sampling truncates the next-token distribution to the *smallest* set of tokens whose cumulative probability mass is at least \(p\), renormalizes probabilities within that set, and samples from the truncated distribution. The candidate set size is dynamic across time steps. (Holtzman et al., 2019, Sec. 3.1, Eq. 2–3: https://arxiv.org/abs/1904.09751)

**Perplexity (PPL).** Perplexity is the exponentiated per-token cross-entropy loss: if \(\mathcal{L}=\mathbb{E}_{(c,t)}[-\log p(t\mid c)]\), then \(\mathrm{PPL}=\exp(\mathcal{L})\) (natural log), or \(\mathrm{PPL}=2^{\mathcal{L}}\) if \(\log\) is base-2. It measures how “surprised” a predictor is by the true next token on average. (https://arxiv.org/html/2212.11281v2)

---

## Key Formulas & Empirical Results

### Autoregressive factorization (supports: “LMs predict next token”)
For tokens \(x_{1:m+n}\),
\[
P(x_{1:m+n})=\prod_{i=1}^{m+n} P(x_i \mid x_{1}\ldots x_{i-1})
\]
(Holtzman et al., 2019, Eq. 1: https://arxiv.org/abs/1904.09751)

**Tutor note:** Use this to justify why generation is inherently sequential and why decoding choices matter.

### Temperature softmax (supports: “temperature changes randomness/diversity”)
Given logits \(u_l\) and temperature \(t\),
\[
p(x=V_l\mid x_{1:i-1})=\frac{\exp(u_l/t)}{\sum_{l'}\exp(u_{l'}/t)}
\]
(Holtzman et al., 2019, Eq. 4: https://arxiv.org/abs/1904.09751)

**Variables:** \(V_l\) token \(l\) in vocab; \(u_l\) its logit; \(t\) temperature.

### Nucleus (top‑p) truncation + renormalization (supports: “top‑p is dynamic truncation”)
Define the nucleus \(V^{(p)}\subset V\) as the smallest set such that
\[
\sum_{x\in V^{(p)}} P(x\mid x_{1:i-1}) \ge p
\]
Then renormalize:
\[
P'(x\mid x_{1:i-1})=
\begin{cases}
P(x\mid x_{1:i-1})/p' & x\in V^{(p)}\\
0 & \text{otherwise}
\end{cases}
\quad\text{where }p'=\sum_{x\in V^{(p)}}P(x\mid x_{1:i-1})
\]
(Holtzman et al., 2019, Eq. 2–3: https://arxiv.org/abs/1904.09751)

### Cross-entropy loss and perplexity (supports: “PPL is exp(loss)”)
\[
\mathcal{L}=\mathbb{E}_{(c,t)}[-\log p(t\mid c)],\qquad \mathrm{PPL}=\exp(\mathcal{L})
\]
(https://arxiv.org/html/2212.11281v2)

### Human vs LM next-token prediction (supports: “objective is hard; LMs can outperform humans on webtext next-token”)
On OpenWebText:
- Humans: mean **29%** top‑1 accuracy (subset with ≥50 answers: **30%**)
- GPT‑3: **56%** top‑1 accuracy  
(https://arxiv.org/html/2212.11281v2, Sec. 3.2)

### GPT‑3 few-shot protocol defaults (supports: “few-shot = in-context examples, no weight updates”)
- Few-shot: provide **K demonstrations** in prompt; **no gradient updates**; typical **K ≈ 10–100** limited by **context window nctx = 2048** tokens.
- Evaluation: randomly draw K examples from training set per test example; delimiter 1–2 newlines depending on task.
- Free-form completion decoding: **beam search**, beam width **4**, length penalty **α = 0.6**.  
(GPT‑3 paper, NeurIPS 2020 PDF: https://proceedings.neurips.cc/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf)

### Nucleus sampling experimental defaults (useful “what did the paper do?” lookup)
Holtzman et al. report experiments with:
- GPT‑2 Large (762M)
- 5,000 conditional generations; max length 200 tokens; context truncated to 1–40 tokens  
(https://arxiv.org/abs/1904.09751)

---

## How It Works

### A. Training loop for next-token prediction (mechanics)
1. **Tokenize** text into tokens \(x_{1:T}\) (tokenization details are model-specific; not formalized in provided sources).
2. For each position \(i\) from 1 to \(T\!-\!1\):
   - Input context \(c = x_{1:i}\)
   - Model outputs logits over vocab for \(x_{i+1}\)
   - Convert logits to probabilities with softmax (optionally temperature at inference; training typically uses \(t=1\))
3. **Compute loss** at each position: \(-\log p(x_{i+1}\mid x_{1:i})\).
4. **Average** over positions/batch to get cross-entropy \(\mathcal{L}\).
5. **Update weights** to minimize \(\mathcal{L}\) (optimizer specifics not in this lesson’s key concepts; skip unless asked).

Tutor move: if student asks “why does this learn knowledge?”, point to the pressure to reduce \(-\log p(t\mid c)\) across diverse contexts; the only way is to internalize statistical/semantic regularities.

### B. Autoregressive generation (decoding) loop
Given a prompt (context) \(x_{1:i-1}\), repeat:
1. Compute next-token distribution \(P(x\mid x_{1:i-1})\).
2. Apply a **decoding strategy**:
   - **Greedy:** pick \(\arg\max_x P(x\mid \cdot)\).
   - **Sampling:** sample from \(P(\cdot\mid \cdot)\) (often after temperature/top‑p truncation).
3. Append chosen token to context; stop on EOS/stop condition/max length.

### C. Nucleus (top‑p) sampling algorithm (exact steps)
At each generation step:
1. Sort tokens by probability \(P(x\mid x_{1:i-1})\) descending.
2. Take the **smallest** prefix set \(V^{(p)}\) whose cumulative mass ≥ \(p\). (Holtzman Eq. 2)
3. Renormalize probabilities within \(V^{(p)}\) to get \(P'\). (Holtzman Eq. 3)
4. Sample next token from \(P'\).

**Tutor note:** Emphasize “dynamic set size” vs top‑k’s fixed size; this is the key operational difference.

### D. Computing perplexity from model probabilities
1. For each token position with true next token \(t\) and context \(c\), record \(-\log p(t\mid c)\).
2. Average over positions/examples to get \(\mathcal{L}\).
3. Convert to perplexity: \(\mathrm{PPL}=\exp(\mathcal{L})\). (https://arxiv.org/html/2212.11281v2)

---

## Teaching Approaches

### Intuitive (no math)
- “The model is playing an extremely hard autocomplete game.” It sees a prefix and must guess what comes next. To do well across the internet, it has to pick up grammar, facts, style, and patterns of reasoning because those patterns help predict what people write next.
- Temperature/top‑p are “creativity knobs” that change how adventurous the model is when choosing the next word-piece.

### Technical (with math)
- Use the factorization \(P(x_{1:T})=\prod_i P(x_i\mid x_{<i})\) (Holtzman Eq. 1) to show training decomposes into many conditional prediction problems.
- Show evaluation loss \(\mathcal{L}=\mathbb{E}[-\log p(t\mid c)]\) and perplexity \(\exp(\mathcal{L})\) (Perplexity paper Eq. 1).
- Show decoding transforms logits via temperature \(t\) (Holtzman Eq. 4), then optionally truncates via nucleus set \(V^{(p)}\) (Holtzman Eq. 2–3).

### Analogy-based
- **Compression analogy (Karpathy talk framing):** training is like compressing text; better compression requires discovering structure. The “next token” objective is the operational way to measure compression quality (lower surprise).
- **Dice with loaded probabilities:** the model rolls a weighted die each token. Temperature changes how “loaded” the die is; top‑p removes the “weird tail faces” before rolling (Holtzman’s “unreliable tail” rationale).

---

## Common Misconceptions

1. **“The model stores sentences and retrieves them like a database.”**  
   - **Why wrong:** The objective is to assign probabilities to next tokens across many contexts, not to retrieve exact strings. The model outputs a distribution \(p(\cdot\mid c)\) and is trained by \(-\log p(t\mid c)\) (https://arxiv.org/html/2212.11281v2).  
   - **Correct model:** It learns parameters that *generalize* statistical patterns; memorization can happen, but the core mechanism is probabilistic next-token prediction.

2. **“Perplexity is the probability the model is correct.”**  
   - **Why wrong:** Perplexity is \(\exp(\mathcal{L})\), where \(\mathcal{L}\) is average negative log-probability of the true token (https://arxiv.org/html/2212.11281v2). It’s not an accuracy percentage.  
   - **Correct model:** Lower PPL means the model assigns higher probability to the true next tokens on average; it’s tied to cross-entropy, not directly to top‑1 accuracy.

3. **“Temperature and top‑p are the same thing.”**  
   - **Why wrong:** Temperature rescales logits globally before softmax (Holtzman Eq. 4). Top‑p truncates the distribution to a minimal cumulative-mass set and renormalizes (Holtzman Eq. 2–3).  
   - **Correct model:** Temperature changes *shape* of the whole distribution; top‑p changes the *support* (which tokens are even allowed).

4. **“Top‑p keeps a fixed number of tokens like top‑k.”**  
   - **Why wrong:** Holtzman et al. explicitly define \(V^{(p)}\) as the smallest set reaching mass \(p\), so its size varies by step (https://arxiv.org/abs/1904.09751).  
   - **Correct model:** When the model is confident, nucleus may be small; when uncertain, nucleus grows.

5. **“Few-shot learning means the model is being trained during the prompt.”**  
   - **Why wrong:** GPT‑3 few-shot is defined as providing K demonstrations in the prompt with **no gradient updates** (NeurIPS 2020 GPT‑3 paper PDF).  
   - **Correct model:** It’s inference conditioned on extra text; the model’s weights are unchanged.

---

## Worked Examples

### 1) Compute perplexity from next-token probabilities (fully worked numeric)
Suppose we evaluate 3 next-token positions and the model assigns probabilities to the true next token:
- Position 1: \(p(t\mid c)=0.50\)
- Position 2: \(p(t\mid c)=0.25\)
- Position 3: \(p(t\mid c)=0.10\)

Per-token negative log-likelihoods (natural log):
- \(-\log 0.50 = 0.6931\)
- \(-\log 0.25 = 1.3863\)
- \(-\log 0.10 = 2.3026\)

Average loss:
\[
\mathcal{L}=\frac{0.6931+1.3863+2.3026}{3}=1.4607
\]

Perplexity:
\[
\mathrm{PPL}=\exp(\mathcal{L})=\exp(1.4607)\approx 4.31
\]
This uses the definition \(\mathrm{PPL}=\exp(\mathcal{L})\). (https://arxiv.org/html/2212.11281v2)

### 2) Nucleus (top‑p) sampling on a toy distribution (step-by-step)
Next-token distribution over tokens \(\{A,B,C,D\}\):
- \(P(A)=0.40\)
- \(P(B)=0.30\)
- \(P(C)=0.20\)
- \(P(D)=0.10\)

Let \(p=0.75\). Sort descending: A (0.40), B (0.30), C (0.20), D (0.10).  
Cumulative mass:
- {A}: 0.40
- {A,B}: 0.70
- {A,B,C}: 0.90  → first ≥ 0.75, so \(V^{(p)}=\{A,B,C\}\) (smallest set meeting threshold). (Holtzman Eq. 2)

Renormalize within nucleus: \(p' = 0.90\). (Holtzman Eq. 3)
- \(P'(A)=0.40/0.90=0.444...\)
- \(P'(B)=0.30/0.90=0.333...\)
- \(P'(C)=0.20/0.90=0.222...\)
- \(P'(D)=0\)

Then sample from \(P'\).

### 3) Minimal pseudocode: temperature + top‑p decoding
```python
# logits: vector over vocab for next token
# t: temperature, p: nucleus threshold

probs = softmax(logits / t)  # Holtzman et al. Eq. 4

# nucleus set V^(p): smallest set with cumulative mass >= p (Holtzman Eq. 2)
sorted_tokens = argsort_desc(probs)
cum = 0.0
V = []
for tok in sorted_tokens:
    V.append(tok)
    cum += probs[tok]
    if cum >= p:
        break

# renormalize (Holtzman Eq. 3)
Z = sum(probs[tok] for tok in V)
probs_trunc = {tok: probs[tok]/Z for tok in V}

next_tok = sample(probs_trunc)
```

---

## Comparisons & Trade-offs

| Method / Metric | What it does | Key trade-off / when to use | Source |
|---|---|---|---|
| **Greedy decoding** | Choose highest-prob token each step | Deterministic but can lead to repetitive/generic outputs (“degeneration” in practice) | Holtzman et al., 2019 |
| **Beam search** | Search over multiple high-prob sequences | Can improve likelihood but may worsen human-perceived quality; GPT‑3 eval used beam width 4, length penalty 0.6 for free-form tasks | GPT‑3 paper PDF |
| **Pure sampling** | Sample from full distribution | More diverse but can become incoherent due to low-probability “tail” tokens | Holtzman et al., 2019 |
| **Top‑k sampling** | Keep top k tokens, renormalize, sample | Fixed candidate size; retained probability mass can vary a lot step-to-step | Holtzman et al., 2019 |
| **Top‑p (nucleus) sampling** | Keep smallest set with mass ≥ p, renormalize, sample | Dynamic candidate size; designed to avoid “unreliable tail” while preserving diversity | Holtzman et al., 2019 |
| **Temperature** | Rescale logits before softmax | Global diversity control; interacts with top‑p/top‑k | Holtzman et al., 2019 |
| **Cross-entropy loss** | \(\mathbb{E}[-\log p(t\mid c)]\) | Training/eval objective for next-token prediction | Perplexity paper, 2022 |
| **Perplexity** | \(\exp(\mathcal{L})\) | Interpretable transform of loss; not accuracy | Perplexity paper, 2022 |

**Tutor guidance:** If student asks “why not always greedy/beam?”, cite Holtzman’s claim that maximization-based decoding can degenerate, and that nucleus sampling targets the “unreliable tail” problem in pure sampling.

---

## Prerequisite Connections

- **Probability distributions & conditional probability:** Needed to interpret \(P(x_i\mid x_{<i})\) and why joint probability factorizes (Holtzman Eq. 1).
- **Logarithms / negative log-likelihood:** Needed to understand cross-entropy loss and why perplexity is \(\exp(\mathcal{L})\). (https://arxiv.org/html/2212.11281v2)
- **Softmax & logits:** Needed to understand temperature scaling \(u/t\) before softmax. (Holtzman Eq. 4)
- **Sampling vs argmax:** Needed to reason about decoding strategies and diversity/coherence trade-offs (Holtzman et al., 2019).

---

## Socratic Question Bank

1. **If a model assigns probability 1.0 to the correct next token at every position, what would its perplexity be?**  
   *Good answer:* Loss \(\mathcal{L}=0\) so \(\mathrm{PPL}=\exp(0)=1\). (Perplexity definition)

2. **How can two models have similar perplexity but different “feel” in generated text?**  
   *Good answer:* PPL is an average next-token metric; decoding strategy (greedy vs sampling, temperature/top‑p) changes outputs without changing the underlying trained distribution.

3. **What exactly makes top‑p “dynamic,” and why might that matter?**  
   *Good answer:* \(V^{(p)}\) is the smallest set reaching mass \(p\), so size changes with distribution sharpness; avoids fixed-k issues where retained mass varies wildly. (Holtzman)

4. **What does lowering temperature do to the softmax distribution, mechanically?**  
   *Good answer:* Dividing logits by smaller \(t\) increases relative gaps, concentrating mass on top tokens. (Holtzman Eq. 4)

5. **In few-shot prompting, what changes: the model weights or the context?**  
   *Good answer:* Only the context; GPT‑3 few-shot uses demonstrations with no gradient updates. (GPT‑3 paper protocol)

6. **Why might “maximizing probability” (greedy/beam) produce repetitive text?**  
   *Good answer:* Holtzman et al. report degeneration under maximization-based decoding; sampling methods mitigate by allowing lower-prob but still plausible continuations.

7. **If a model’s top‑1 accuracy is 56% on a dataset, does that mean it’s “wrong” 44% of the time in generation?**  
   *Good answer:* Not directly; top‑1 accuracy is about matching the dataset’s exact next token, not about producing acceptable continuations; many alternatives can be valid.

8. **What information does the next-token objective force the model to represent?**  
   *Good answer:* Anything predictive of continuation—syntax, semantics, facts, discourse patterns—because those reduce \(-\log p(t\mid c)\) across data.

---

## Likely Student Questions

**Q: What’s the actual loss function for next-token prediction?**  
→ **A:** Per-token cross-entropy: \(\mathcal{L}=\mathbb{E}_{(c,t)}[-\log p(t\mid c)]\), where \(c\) is context and \(t\) is the true next token. (https://arxiv.org/html/2212.11281v2)

**Q: How do you convert cross-entropy loss to perplexity?**  
→ **A:** \(\mathrm{PPL}=\exp(\mathcal{L})\) if \(\log\) is natural; if \(\log\) is base-2, \(\mathrm{PPL}=2^{\mathcal{L}}\). (https://arxiv.org/html/2212.11281v2)

**Q: What is nucleus (top‑p) sampling, precisely?**  
→ **A:** Choose the smallest token set \(V^{(p)}\) with cumulative probability ≥ \(p\), renormalize probabilities within it, and sample from the truncated distribution. (Holtzman et al., Eq. 2–3: https://arxiv.org/abs/1904.09751)

**Q: How is top‑p different from top‑k?**  
→ **A:** Top‑k keeps a fixed number \(k\) of tokens; top‑p keeps a variable number such that retained probability mass is at least \(p\). Holtzman et al. note top‑k’s retained mass can “vary wildly” across steps, while top‑p adapts to distribution shape. (https://arxiv.org/abs/1904.09751)

**Q: What does temperature do mathematically?**  
→ **A:** It rescales logits before softmax: \(p(x=V_l\mid \cdot)=\frac{\exp(u_l/t)}{\sum_{l'}\exp(u_{l'}/t)}\). Lower \(t\) makes the distribution peakier (less diverse). (Holtzman et al., Eq. 4: https://arxiv.org/abs/1904.09751)

**Q: Do humans actually do well at next-token prediction?**  
→ **A:** On OpenWebText, humans achieved about **29%** mean top‑1 accuracy, while GPT‑3 achieved **56%** top‑1 accuracy in the reported study. (https://arxiv.org/html/2212.11281v2)

**Q: In GPT‑3’s few-shot setting, how many examples are typically included, and what limits it?**  
→ **A:** GPT‑3 describes few-shot as typically **K ≈ 10–100** demonstrations, limited by the **2048-token** context window (nctx=2048). (GPT‑3 paper PDF: https://proceedings.neurips.cc/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf)

**Q: What decoding settings did GPT‑3 use for free-form completion in evaluation?**  
→ **A:** Beam search with **beam width = 4** and **length penalty α = 0.6** for free-form completion tasks. (GPT‑3 paper PDF)

---

## Available Resources

### Videos
- [Intro to Large Language Models](https://youtube.com/watch?v=zjkBMFhNj_g) — **Surface when:** student asks for a concrete mental model of “next-token prediction → generation,” or why this objective can yield broad capabilities.
- [Let’s build GPT: from scratch, in code, spelled out](https://youtube.com/watch?v=kCc8FmEb1nY) — **Surface when:** student wants implementation-level intuition for autoregressive transformers and training a small LM.

### Articles & Tutorials
- [Lilian Weng — The Transformer Family v2](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/) — **Surface when:** student asks “what’s inside the model?” (attention/transformer mechanics) beyond the next-token objective.
- [Sebastian Raschka — New LLM Pre-training and Post-training Paradigms](https://magazine.sebastianraschka.com/p/new-llm-pre-training-and-post-training) — **Surface when:** student asks how pretraining relates to post-training (SFT/alignment) and practical training pipeline considerations.
- [Brown et al. (2020) — Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) — **Surface when:** student asks for the canonical few-shot/zero-shot definitions and evaluation framing at scale.
- [Lilian Weng — Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/) — **Surface when:** student asks how prompting/ICL relates to next-token prediction and how to structure demonstrations.
- [DAIR.AI — Prompt Engineering Guide](https://www.promptingguide.ai/) — **Surface when:** student wants a broad reference for decoding knobs (temperature/top‑p) and prompting patterns.

---

## Visual Aids

![Language models generate text token-by-token via next-token prediction. (Huyenchip.com)](/api/wiki-images/pre-training/images/huyenchip-2023-05-02-rlhf-html_002.gif)  
**Show when:** student is confused about “how does the model actually produce a whole paragraph?” Use to anchor autoregressive generation.

---

## Key Sources

- [The Curious Case of Neural Text Degeneration (Holtzman et al., 2019)](https://arxiv.org/abs/1904.09751) — Primary-source definitions and equations for temperature and nucleus (top‑p) sampling; contrasts decoding strategies.
- [Perplexity and next-token prediction (arxiv HTML 2212.11281v2)](https://arxiv.org/html/2212.11281v2) — Explicit cross-entropy ↔ perplexity definition plus human vs GPT‑3 next-token accuracy numbers.
- [Language Models are Few-Shot Learners (GPT‑3; NeurIPS 2020 PDF)](https://proceedings.neurips.cc/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf) — Canonical definitions and protocol for zero/one/few-shot prompting and key decoding defaults used in evaluation.
- [Intro to Large Language Models (Karpathy talk)](https://youtube.com/watch?v=zjkBMFhNj_g) — High-signal pedagogical framing for next-token prediction and autoregressive generation (useful for live tutoring pivots).