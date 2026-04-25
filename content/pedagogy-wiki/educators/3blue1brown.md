# 3Blue1Brown

## Style

Grant Sanderson's 3Blue1Brown channel is defined by **visual-mathematical storytelling**. His signature approach uses custom-built animation software (Manim) to render abstract mathematical concepts as fluid, intuitive geometric and graphical transformations. Rather than leading with code or rote formulas, he builds *why* something is true before *what* it is — a Socratic, narrative-driven pedagogy that prioritizes deep conceptual intuition over procedural fluency. Lectures feel like guided discovery rather than instruction. Heavy use of color, motion, and spatial reasoning makes him uniquely effective for learners who think visually or who have hit a wall with purely symbolic explanations.

## Best For

- **Linear algebra fundamentals** — vector spaces, matrix transformations, eigenvectors/eigenvalues, dot products, and change of basis, all framed geometrically
- **Calculus intuition** — derivatives as slopes of tangent lines, integrals as accumulated area, the chain rule visualized through nested transformations
- **Neural network foundations** — what a neural network is, how backpropagation works conceptually, gradient descent as a loss-landscape navigation problem
- **Attention and Transformers (conceptual)** — high-level intuition for how attention mechanisms work and why they matter for LLMs
- **Probability and statistics intuition** — Bayes' theorem, the normal distribution, and why statistical results are often counterintuitive
- **Fourier transforms** — one of the clearest visual explanations available anywhere of what a Fourier transform actually *does*
- **Differential equations** — phase portraits, stability, and the geometric meaning of solutions
- **Mathematical proof intuition** — e.g., why Euler's formula is true, visual proofs of the Pythagorean theorem

## Not Good For

- **Hands-on coding or implementation** — virtually no code is written; learners will not leave knowing how to build or train a model
- **Software engineering and MLOps** — no coverage of pipelines, deployment, experiment tracking, or production concerns
- **Advanced ML research topics** — reinforcement learning, diffusion models, fine-tuning strategies, RLHF, quantization, etc. are not covered
- **Deep dives into specific frameworks** — PyTorch, TensorFlow, JAX, HuggingFace are absent
- **Data preprocessing, feature engineering, or EDA**
- **LLM engineering specifics** — tokenization details, context windows, KV cache, inference optimization
- **Breadth of ML algorithms** — SVMs, decision trees, ensemble methods, clustering, etc. are not systematically covered
- **Keeping pace with fast-moving research** — content is deliberately timeless and foundational, not current

## Canonical Resources

- Essence of Linear Algebra (full playlist): url=https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab
- Vectors, what even are they? (EoLA Ch.1): youtube_id=fNk_zzaMoSs
- Linear transformations and matrices (EoLA Ch.3): youtube_id=kYB8IZa5AuE
- Eigenvectors and eigenvalues (EoLA Ch.14): youtube_id=PFDu9oVAE-g
- Essence of Calculus (full playlist): url=https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr
- But what is a neural network? (DL Ch.1): youtube_id=aircAruvnKk
- Gradient descent, how neural networks learn (DL Ch.2): youtube_id=IHZwWFHWa-w
- What is backpropagation really doing? (DL Ch.3): youtube_id=Ilg3gGewQ5U
- Backpropagation calculus (DL Ch.4): youtube_id=tIeHLnjs5U8
- But what is the Fourier Transform? A visual introduction: youtube_id=spUNpyF58BY
- Bayes theorem, the geometry of changing beliefs: youtube_id=HZGCoVF3YvM
- But what is a GPT? Visual intro to Transformers (DL Ch.5): youtube_id=wjZofJX0v4M [NOT VERIFIED]
- Attention in transformers, visually explained (DL Ch.6): youtube_id=eMlx5fFNoYc [NOT VERIFIED]
- Neural networks full playlist (Deep Learning series): url=https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi

## Pairs Well With

- **3B1B → Andrej Karpathy**: The canonical pairing for neural networks and LLMs. 3B1B supplies the geometric/conceptual intuition for what attention and backprop *mean*; Karpathy's *Neural Networks: Zero to Hero* series then implements every concept from scratch in PyTorch. Ideal for the `intro-to-llms` and `ml-engineering-foundations` tracks.
- **3B1B → StatQuest (Josh Starmer)**: 3B1B for mathematical beauty and geometry; StatQuest for step-by-step statistical and ML algorithm walkthroughs with plain-language narration. Together they cover both the *why* and the *what* of foundational ML math.
- **3B1B → fast.ai (Jeremy Howard)**: 3B1B builds bottom-up mathematical intuition; fast.ai takes a top-down, code-first, practical approach. The contrast is productive — students who start with fast.ai and feel lost on the math can use 3B1B to backfill; students who start with 3B1B and want to build things move to fast.ai.
- **3B1B → Gilbert Strang (MIT 18.06)**: For students who need rigorous linear algebra beyond intuition, Strang's MIT OCW lectures are the natural next step after 3B1B's Essence of Linear Algebra playlist.
- **3B1B → Distill.pub**: Both prioritize visual, intuition-first explanations of ML concepts. Distill articles (e.g., on attention, feature visualization) complement 3B1B videos for learners who want interactive, research-grade visual explanations in written form.

## Level

**Beginner to Intermediate** (mathematical foundations); content assumes curiosity and high-school-level math comfort but not prior university mathematics. The neural network and transformer series are accessible to motivated beginners but deliver the most value to intermediate learners who already have some exposure to the concepts and want to solidify intuition. Not appropriate as a primary resource for advanced practitioners seeking research depth.

## Last Verified

2026-04-06