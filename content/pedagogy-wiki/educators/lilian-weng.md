# Lilian Weng

## Style
Lilian Weng writes in a **dense, mathematically rigorous, narrative-driven** style. Her primary medium is long-form written blog posts rather than video content. She builds understanding through careful derivation of equations, precise formal definitions, and structured taxonomies of concepts. Posts typically follow a pattern of: motivation → formal definition → mathematical treatment → worked examples → curated literature survey. She uses diagrams and figures (often adapted from papers) to supplement mathematical explanations, but the writing itself is the core pedagogical vehicle. Her tone is authoritative and encyclopedic — closer to a well-written survey paper than a casual tutorial. She does not use a code-first or hands-on notebook approach.

## Best For
- **Transformer architecture internals** — attention mechanisms, positional encodings, architectural variants
- **Reinforcement Learning from Human Feedback (RLHF)** — reward modeling, PPO in LLM context, preference learning
- **LLM agent frameworks** — planning, memory, tool use, ReAct, reflexion-style agents
- **Diffusion models** — DDPM, score matching, DDIM, classifier-free guidance, mathematical derivations
- **Prompt engineering** — systematic taxonomy of techniques (chain-of-thought, self-consistency, etc.)
- **Exploration strategies in deep RL** — curiosity-driven learning, count-based methods
- **Generative model families** — VAEs, GANs, normalizing flows, with rigorous probabilistic framing
- **Attention and memory mechanisms** — neural Turing machines, memory-augmented networks
- **Multimodal foundations** — contrastive learning, vision-language alignment concepts
- **AI safety and alignment concepts** — reward hacking, specification gaming (at a conceptual/survey level)

## Not Good For
- **Beginner-friendly introductions** — assumes significant mathematical maturity (linear algebra, probability, calculus)
- **Hands-on coding tutorials** — virtually no runnable code, no notebooks, no implementation walkthroughs
- **Video learners** — she has no substantial YouTube presence or lecture series
- **Very recent breaking developments** — blog posts are periodic; not a source for week-to-week news
- **Systems/infrastructure topics** — distributed training, serving, quantization, deployment engineering
- **Computer vision fundamentals** (CNNs, detection pipelines) beyond what intersects with generative models
- **Audio/speech modalities** — not a focus area
- **Physical AI / robotics specifics** — her agent content is software-agent focused, not embodied robotics
- **Step-by-step project building** — not structured as project-based learning

## Canonical Resources
- Attention mechanisms and Transformer internals: url=https://lilianweng.github.io/posts/2018-06-24-attention/
- LLM-powered autonomous agents (agentic AI survey): url=https://lilianweng.github.io/posts/2023-06-23-agent/
- Prompt engineering techniques (comprehensive taxonomy): url=https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/
- RLHF — reinforcement learning from human feedback: url=https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/
- Diffusion models explained (DDPM, score matching, DDIM): url=https://lilianweng.github.io/posts/2021-07-11-diffusion-models/
- Generative adversarial networks overview: url=https://lilianweng.github.io/posts/2017-08-20-gan/
- VAEs — variational autoencoders: url=https://lilianweng.github.io/posts/2018-08-12-vae/
- Contrastive representation learning: url=https://lilianweng.github.io/posts/2021-05-31-contrastive/
- Exploration strategies in deep RL: url=https://lilianweng.github.io/posts/2020-06-07-exploration-drl/
- Lilian Weng's blog homepage (full archive): url=https://lilianweng.github.io/

## Pairs Well With
- **Andrej Karpathy → Lilian Weng**: Karpathy provides code-first intuition (e.g., building a GPT from scratch); Weng then supplies the rigorous mathematical and architectural survey to deepen understanding
- **3Blue1Brown → Lilian Weng**: 3B1B builds visual geometric intuition for attention and neural networks; Weng extends this into formal derivations and literature context
- **Lilian Weng → Hugging Face courses**: Weng establishes deep conceptual grounding; HF courses then provide the practical, code-based implementation layer
- **Lilian Weng → original papers**: Her posts function as guided entry points into dense literature (she cites prolifically), making her a natural bridge to reading primary sources
- **Sebastian Raschka → Lilian Weng**: Raschka covers implementation and applied ML; Weng covers the theoretical and survey dimension of the same topics
- **DeepMind / OpenAI technical blog posts → Lilian Weng**: She often synthesizes and contextualizes findings from major lab publications into coherent frameworks

## Level
**Intermediate to Advanced**

Best suited for students who already understand neural network basics, backpropagation, and foundational probability/statistics. Ideal for practitioners who want to move from "I can use these tools" to "I understand why these architectures and algorithms work." Not recommended as a first resource for any topic — use after building baseline familiarity. Graduate students, ML engineers deepening their knowledge, and researchers will get the most value.

## Last Verified
2026-04-06