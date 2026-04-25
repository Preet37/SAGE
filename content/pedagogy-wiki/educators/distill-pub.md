# Distill.pub

## Style
Distill.pub is a research publication platform with a distinctive **visual-first, narrative-driven** teaching style that sets it apart from traditional academic papers. Articles are written as interactive, web-native essays that combine:
- **Rich interactive visualizations** — readers can manipulate parameters, watch animations, and explore concepts dynamically rather than reading static figures
- **Narrative explanation** — complex ideas are built up through careful prose that prioritizes intuition before formalism
- **Mathematical rigor** — equations are present and precise, but always contextualized within explanatory text rather than leading it
- **Diagrams and illustrations** — custom-built, high-quality graphics that make abstract concepts (e.g., attention heads, feature curves) visually concrete
- **Minimal assumed knowledge** — authors are expected to explain their work accessibly, not just report results

The platform was explicitly designed to reward *clarity of explanation* as a first-class research contribution, not just novelty of results.

## Best For
- **Attention mechanisms and Transformers** — including the landmark "A Mathematical Framework for Transformer Circuits" and "In-context Learning and Induction Heads"
- **Neural network interpretability / mechanistic interpretability** — feature visualization, circuits, superposition
- **Feature visualization in CNNs** — "Feature Visualization" and "The Building Blocks of Interpretability" articles
- **Dimensionality reduction intuition** — t-SNE explained interactively
- **Differentiable programming concepts**
- **Distillation of complex ML research** — making cutting-edge papers accessible without sacrificing accuracy
- **Attention and memory in sequence models**
- **Grokking and neural network generalization phenomena**
- **Multimodal neurons and polysemanticity**

## Not Good For
- **Practical coding tutorials** — no runnable notebooks, no step-by-step implementation walkthroughs
- **Beginner ML fundamentals** — assumes familiarity with basic ML concepts; not a starting point for newcomers
- **Breadth of topic coverage** — the catalog is intentionally small and curated; many important ML topics have no Distill article
- **MLOps, deployment, or production engineering** — entirely absent
- **Classical ML algorithms** (SVMs, decision trees, ensemble methods)
- **Data preprocessing and pipelines**
- **Reinforcement learning** (very limited coverage)
- **Keeping up with the latest research** — the platform went on hiatus in 2021 and has not published new articles since; content does not reflect post-2021 developments
- **Video learners** — entirely text/web format, no video content

## Canonical Resources
- Feature visualization in neural networks: url=https://distill.pub/2017/feature-visualization/
- The building blocks of interpretability (activation atlases precursor): url=https://distill.pub/2018/building-blocks/
- Attention and augmented recurrent neural networks: url=https://distill.pub/2016/augmented-rnns/
- How to use t-SNE effectively (interactive): url=https://distill.pub/2016/misread-tsne/
- Exploring neural networks with activation atlases: url=https://distill.pub/2019/activation-atlas/
- A mathematical framework for transformer circuits: url=https://transformer-circuits.pub/2021/framework/index.html
- In-context learning and induction heads: url=https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html
- Toy models of superposition (polysemanticity): url=https://transformer-circuits.pub/2022/toy_model/index.html
- Circuits: curve detectors: url=https://distill.pub/2020/circuits/curve-detectors/
- Why momentum really works (optimization): url=https://distill.pub/2017/momentum/
- Deconvolution and checkerboard artifacts: url=https://distill.pub/2016/deconv-checkerboard/
- Visualizing memorization in RNNs: url=https://distill.pub/2019/memorization-in-rnns/

## Pairs Well With
- **3Blue1Brown → Distill.pub**: 3B1B provides foundational geometric/mathematical intuition (linear algebra, calculus, basic neural nets); Distill.pub then extends that intuition into specific, cutting-edge ML phenomena at a deeper level
- **Distill.pub → Andrej Karpathy**: Distill builds the conceptual and visual understanding of mechanisms (e.g., attention, transformers); Karpathy then provides the hands-on coding implementation of those same ideas
- **Distill.pub → Anthropic/DeepMind papers**: Distill articles (especially transformer-circuits.pub) serve as the accessible entry point before reading dense primary research literature
- **Chris Olah's blog (colah.github.io) → Distill.pub**: Olah's personal blog covers similar visual/intuitive territory and many Distill articles are authored by him — they form a natural continuum
- **Fast.ai (Jeremy Howard) for practical grounding → Distill.pub for mechanistic depth**: Fast.ai gives learners working code intuition; Distill.pub explains *why* the internals behave as they do
- **Distill.pub → Neel Nanda (mechanistic interpretability)**: Distill's circuits work is the theoretical foundation; Nanda's tutorials and TransformerLens library are the practical follow-on for interpretability practitioners

## Level
**Intermediate to Advanced**

Readers should already be comfortable with:
- Basic neural network architecture (layers, activations, backpropagation)
- Fundamental calculus and linear algebra
- At least some exposure to modern deep learning (CNNs, RNNs, or Transformers)

The interactive format lowers the barrier somewhat compared to raw papers, but Distill is *not* appropriate as a first resource. It is ideal for learners who have completed an introductory ML course and want to build deep, principled understanding of specific phenomena — particularly those interested in **interpretability, attention mechanisms, or understanding what neural networks are actually computing**.

## Last Verified
2026-04-06

> **Note:** Distill.pub announced an indefinite editorial hiatus in September 2021. The existing articles remain publicly accessible and are still among the highest-quality explanatory resources in ML, but no new content has been published since then. The transformer-circuits.pub domain (maintained by Anthropic researchers, many of whom were Distill contributors) continues to publish related interpretability work and is considered a spiritual successor for that subdomain.