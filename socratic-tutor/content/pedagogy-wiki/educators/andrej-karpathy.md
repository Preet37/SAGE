# Andrej Karpathy

## Style
Karpathy's teaching style is **code-first and bottom-up**, with a strong emphasis on building everything from scratch to develop genuine intuition. He favors live-coding sessions where he writes neural networks line-by-line in Python/PyTorch, narrating his thought process in real time. His explanations blend mathematical intuition with immediate implementation — he rarely presents theory in isolation without grounding it in runnable code. He uses a conversational, self-deprecating tone that makes dense material feel approachable. Visualizations (matplotlib plots, hand-drawn diagrams) are used tactically to reinforce concepts like backpropagation graphs or attention patterns, but code is always the primary medium. His lectures tend to be long-form (1–3+ hours), rewarding patient learners who want depth over breadth.

## Best For
- **Backpropagation and autograd** — building micrograd from scratch, understanding the chain rule at the implementation level
- **Language model internals** — character-level RNNs, bigram models, and transformer architecture built from first principles
- **The GPT architecture** — attention mechanisms, positional encoding, and the full transformer stack implemented in clean PyTorch
- **Training dynamics** — learning rate schedules, batch normalization, dropout, and diagnosing training instability
- **Tokenization** — byte-pair encoding (BPE) implemented from scratch, understanding how tokenizers actually work
- **Neural network training intuition** — weight initialization, vanishing/exploding gradients, activation functions
- **makemore / nanoGPT projects** — character-level generative models as pedagogical tools
- **LLM mental models** — conceptual framing of what LLMs are, how RLHF fits in, and the "stochastic parrot vs. reasoning" landscape (his "Intro to LLMs" talk)

## Not Good For
- **Rigorous mathematical proofs** — he builds intuition but does not derive theorems formally; not a substitute for a real analysis or probability theory course
- **Computer vision (modern)** — his CV work is research-era; he does not produce updated teaching content on ViTs, diffusion models, or modern CV pipelines
- **Reinforcement learning** — minimal pedagogical coverage beyond brief mentions in the LLM/RLHF context
- **MLOps and production deployment** — no substantive content on serving infrastructure, monitoring, CI/CD for ML, or cloud tooling
- **Data engineering and pipelines** — data preprocessing at scale, feature stores, and data-centric AI are not covered
- **Probabilistic graphical models or Bayesian ML** — essentially absent from his curriculum
- **Breadth-first surveys** — his style rewards depth; learners needing a quick overview of many techniques will find his format inefficient
- **Non-Python frameworks** — JAX, TensorFlow, and other ecosystems are not addressed

## Canonical Resources
- Intro to Large Language Models (1hr talk): `youtube_id=zjkBMFhNj_g`
- The spelled-out intro to neural networks and backpropagation (micrograd): `youtube_id=VMj-3S1tku0`
- Building makemore Part 1 — bigram language model: `youtube_id=PaCmpygFfXo`
- Building makemore Part 2 — MLP: `youtube_id=TCH_1BHY58I`
- Building makemore Part 3 — BatchNorm / activations / gradients: `youtube_id=P6sfmUTpUmc`
- Building makemore Part 4 — Becoming a Backprop Ninja: `youtube_id=q8SA3rM6ckI`
- Building makemore Part 5 — WaveNet: `youtube_id=t3YJ5hKiMQ0`
- Let's build GPT from scratch (nanoGPT): `youtube_id=kCc8FmEb1nY`
- Let's build the GPT Tokenizer (BPE from scratch): `youtube_id=zduSFxRajkE`
- Let's reproduce GPT-2 (124M): `youtube_id=l8pRSuU81PU`
- Karpathy's blog — "The Unreasonable Effectiveness of Recurrent Neural Networks": `url=http://karpathy.github.io/2015/05/21/rnn-effectiveness/`
- Karpathy's blog — "A Recipe for Training Neural Networks": `url=http://karpathy.github.io/2019/04/25/recipe/`
- nanoGPT GitHub repository: `url=https://github.com/karpathy/nanoGPT`
- micrograd GitHub repository: `url=https://github.com/karpathy/micrograd`
- llm.c GitHub repository: `url=https://github.com/karpathy/llm.c`

## Pairs Well With
- **3Blue1Brown → Karpathy**: Use 3B1B's *Neural Networks* series for pure visual/mathematical intuition on backprop and gradient descent, then move to Karpathy to implement those same concepts in code. Ideal transition for visual learners.
- **fast.ai (Jeremy Howard) ↔ Karpathy**: fast.ai is top-down ("run it first, understand later") while Karpathy is bottom-up ("build it from scratch"). Pairing them gives learners both practical fluency and deep mechanistic understanding.
- **Sebastian Raschka → Karpathy**: Raschka provides rigorous, textbook-style coverage of ML fundamentals and PyTorch; Karpathy then extends that into LLM-specific architecture and training at scale.
- **Andrej Karpathy → Yannic Kilcher**: After building intuition with Karpathy, use Kilcher's paper walkthroughs to connect implementations to the research literature (original Transformer paper, GPT-3, etc.).
- **Karpathy → Stanford CS229 (Andrew Ng)**: For learners who want formal mathematical grounding *after* gaining code intuition, CS229 provides the statistical learning theory that Karpathy deliberately skips.
- **Karpathy → Chip Huyen**: Karpathy covers model internals; Huyen covers ML systems design and production — a natural handoff for ML engineering tracks.

## Level
**Intermediate** — primary audience.

- *Beginners* can access his content if they have Python fluency and basic calculus, but will need supplementary resources for mathematical foundations (linear algebra, probability).
- *Advanced practitioners* still find value in his from-scratch implementations as a clarity exercise, but will not find cutting-edge research coverage.
- His neural network / backprop series is approachable at the **beginner-to-intermediate** boundary; his GPT-2 reproduction and llm.c work skews **intermediate-to-advanced**.

## Last Verified
2026-04-06