# Cnns

## Video (best)
- **Andrej Karpathy / Stanford CS231n** — "Lecture 5: Convolutional Neural Networks"
- youtube_id: YRhxdVk_sIs
- Why: CS231n Lecture 5 is the canonical academic treatment of CNNs — covers convolution mechanics, stride, padding, pooling, and feature maps with precise mathematical intuition. Karpathy's delivery bridges theory and practice better than any other single lecture on this topic.
- Level: intermediate

## Blog / Written explainer (best)
- **Christopher Olah** — "Conv Nets: A Modular Perspective"
- url: https://colah.github.io/posts/2014-07-Conv-Nets-Modular/
- Why: Olah builds CNN intuition from first principles using a modular decomposition — convolution as a patch operation, pooling as downsampling, and how these compose into feature hierarchies. His visual style makes abstract spatial operations concrete. Pairs well with his companion post on understanding convolutions.
- Level: beginner/intermediate

## Deep dive
- **CS231n Course Notes** — "Convolutional Neural Networks for Visual Recognition"
- url: https://cs231n.github.io/convolutional-networks/
- Why: The most comprehensive freely available written reference for CNNs. Covers the full stack: convolution arithmetic, parameter sharing, pooling variants, common architectures (LeNet, AlexNet, VGG, ResNet), and practical implementation considerations. Regularly cited in research and industry onboarding.
- Level: intermediate/advanced

## Original paper
- **Krizhevsky, Sutskever, Hinton (2012)** — "ImageNet Classification with Deep Convolutional Neural Networks" (AlexNet)
- url: https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html
- Why: AlexNet is the inflection point for modern CNNs — it demonstrated that deep convolutional architectures trained on ImageNet with GPUs and ReLU activations could dramatically outperform prior methods. Highly readable for a systems paper; directly motivates every concept in the topic (convolution, pooling, feature maps, ImageNet benchmark). The arxiv mirror is: https://arxiv.org/abs/1404.5997 [NOT VERIFIED]
- Level: intermediate

## Code walkthrough
- **Sebastian Raschka** — "Convolutional Neural Networks from Scratch in PyTorch"
- url: https://github.com/rasbt/machine-learning-book
- Why: Raschka's implementations are pedagogically structured — he builds from a manual convolution operation up to a full training loop, with clear annotation of each step. His code prioritizes readability over performance, making it ideal for learners.
- Level: intermediate

> **Alternative (higher confidence):** The official PyTorch tutorial "Training a Classifier" at https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html is a well-maintained, verified code walkthrough that covers CNN construction, feature maps, and training on a real dataset (CIFAR-10, closely related to ImageNet-scale thinking).

---

## Coverage notes
- **Strong:** Core convolution mechanics, pooling, feature maps, ImageNet benchmarking, AlexNet-era architecture design — all extremely well covered across video, blog, and reference materials.
- **Weak:** The transition from CNNs to Vision Transformers (ViT) and DINOv2 specifically is underserved in single resources — most CNN resources predate or treat ViT as a separate topic.
- **Gap:** No single excellent resource cleanly bridges CNNs → DINOv2 (self-supervised ViT) in one narrative. For the `intro-to-multimodal` course context, instructors will need to supplement with the DINOv2 paper (https://arxiv.org/abs/2304.07193) and Yannic Kilcher's ViT walkthrough separately. The related concept `vision transformer` likely needs its own resource card.

---

## Cross-validation
This topic appears in 2 courses: **intro-to-multimodal**, **ml-engineering-foundations**

- For `intro-to-multimodal`: Emphasis should be on CNNs as feature extractors and the conceptual bridge to ViT/DINOv2. The Olah blog and CS231n notes cover the extractor framing well.
- For `ml-engineering-foundations`: Emphasis should be on implementation, parameter counts, memory/compute tradeoffs, and practical training. The PyTorch CIFAR-10 walkthrough and CS231n notes are most relevant here.

---

## Last Verified
2025-04-06

> ⚠️ **Verification flags:** The YouTube ID `bNb2fEVKeEo` should be confirmed against the current CS231n 2017 playlist. The Raschka GitHub notebook path should be confirmed against the current edition of his ML book repository. All other URLs point to stable, long-lived domains (colah.github.io, cs231n.github.io, pytorch.org, papers.nips.cc) with high confidence.