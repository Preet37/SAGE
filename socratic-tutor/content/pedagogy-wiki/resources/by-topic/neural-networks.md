# Neural Networks

## Video (best)
- **3Blue1Brown** — "But what is a neural network?"
- youtube_id: aircAruvnKk
- Why: Exceptional visual intuition for neurons, layers, weights, and activations. Grant Sanderson's animation-driven pedagogy makes abstract concepts concrete without sacrificing mathematical honesty. The best entry point for understanding *what* a neural network is before diving into training mechanics.
- Level: beginner

---

## Blog / Written explainer (best)
- **Christopher Olah** — "Neural Networks, Manifolds, and Topology"
- url: https://colah.github.io/posts/2014-03-NN-Manifolds-Topology/
- Why: Olah builds geometric intuition for *why* neural networks work — how layers progressively untangle data manifolds. Uniquely insightful for understanding depth and activation functions conceptually, not just mechanically. Complements formula-heavy resources by answering the "why does this architecture work?" question.
- Level: intermediate

> **Note:** For a more introductory written explainer, Olah's "Understanding LSTM Networks" (https://colah.github.io/posts/2015-08-Understanding-LSTMs/) is also excellent, though more specific. For the general feedforward case, his manifolds post is the strongest pedagogical choice.

---

## Deep dive
- **Lilian Weng** — "A Peek into the Basics of Neural Networks" / General ML foundations posts
- url: https://lilianweng.github.io/posts/2017-06-21-overview/ [NOT VERIFIED]
- Why: Weng's posts are exhaustively referenced, mathematically rigorous, and cover the full stack — forward pass, loss functions, backpropagation, regularization (dropout, weight decay, batch normalization), and optimization. Serves as a reliable technical reference that bridges intuition and implementation.
- Level: intermediate–advanced

---

## Original paper
- **Rumelhart, Hinton & Williams (1986)** — "Learning representations by back-propagating errors"
- url: https://www.nature.com/articles/323533a0
- Why: The seminal paper that established backpropagation as a practical training algorithm for multi-layer networks. Remarkably readable for its age and historically essential. Most modern neural network training traces directly to this work.
- Level: advanced

> **Note:** Because this predates arXiv, no arxiv URL exists. A freely accessible scan is often found at http://www.cs.toronto.edu/~hinton/absps/naturebp.pdf

---

## Code walkthrough
- **Andrej Karpathy** — "The spelled-out intro to neural networks and backpropagation: building micrograd"
- youtube_id: VMj-3S1tku0
- Why: Karpathy builds a scalar-valued autograd engine and a neural network from absolute scratch in pure Python (~150 lines). Every concept — neurons, layers, forward pass, loss, backpropagation via chain rule, gradient descent — is implemented explicitly with no framework magic. The best existing resource for understanding *how* these pieces connect in code. Pairs perfectly with the 3Blue1Brown video above.
- url: https://github.com/karpathy/micrograd
- Level: beginner–intermediate

---

## Coverage notes
- **Strong:** Forward pass mechanics, neuron/layer abstraction, backpropagation intuition, visual explanations (3B1B), from-scratch implementation (Karpathy/micrograd)
- **Weak:** Batch normalization and dropout as standalone topics are underserved by the resources above — they appear as supporting concepts but rarely as the *focus* of a dedicated best-in-class explainer
- **Gap:** No single resource above gives deep, dedicated treatment to **batch normalization** specifically. Ioffe & Szegedy's original paper (https://arxiv.org/abs/1502.03167) is the best available reference for that sub-topic. Similarly, **data augmentation** as a neural network regularization strategy has no outstanding standalone explainer in the preferred educator list — most coverage is framework-specific (PyTorch/TF docs) rather than conceptual.
- **Duplicate alert:** The existing curated list contains 4 duplicate entries each for `aircAruvnKk` and `Ilg3gGewQ5U` — deduplication is strongly recommended before publishing.

---

> **[Structural note]** "Scaled Dot-Product Attention in Depth" appears to have sub-concepts:
> scaling factor derivation, variance of dot products, softmax saturation
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-07*

> **[Structural note]** "Bahdanau (Additive) Attention: Equations and Intuition" appears to have sub-concepts:
> additive attention, alignment model, mlp scoring, decoder state, encoder hidden states, context vector
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-08*

## Last Verified
2025-01-01 (resource existence confirmed to knowledge cutoff; URLs marked [NOT VERIFIED] should be checked before publication)