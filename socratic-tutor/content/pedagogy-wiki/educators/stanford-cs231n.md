# Stanford CS231n

## Style
Mathematical-first with strong visual reinforcement. Lectures follow a rigorous academic structure: motivation → mathematical formulation → intuition-building visualizations → practical implementation. Slides are dense with equations, diagrams, and annotated examples. Code assignments (in Python/NumPy/PyTorch) are central to the curriculum — students are expected to implement core algorithms from scratch rather than just call library functions. The teaching style assumes comfort with linear algebra and calculus, and builds toward deep theoretical understanding rather than quick practical application. Guest lectures from industry practitioners (Google Brain, OpenAI, etc.) add applied perspective.

## Best For
- **Convolutional Neural Networks (CNNs)** — architecture deep-dives, filter visualization, receptive fields
- **Image classification pipelines** — from raw pixels through softmax, SVM losses, backpropagation
- **Backpropagation and computational graphs** — one of the clearest academic treatments available
- **Optimization algorithms** — SGD, momentum, Adam, learning rate schedules with mathematical grounding
- **Regularization techniques** — dropout, batch normalization, weight decay with theoretical justification
- **Transfer learning and fine-tuning** — practical strategies with CNN feature extraction
- **Object detection architectures** — R-CNN family, YOLO, SSD with architectural comparisons
- **Segmentation** — semantic and instance segmentation methods
- **Recurrent networks and sequence modeling** — LSTMs, GRUs in the context of vision+language
- **Generative models** — VAEs and GANs with mathematical derivations
- **Attention mechanisms and Vision Transformers (ViTs)** — covered in more recent iterations

## Not Good For
- **Tabular/structured data ML** — course is almost exclusively vision-focused
- **Classical machine learning** — no coverage of SVMs, decision trees, ensemble methods as standalone topics
- **NLP-first deep learning** — language modeling, tokenization, and LLM-specific architectures are peripheral
- **MLOps and production deployment** — no coverage of serving, monitoring, CI/CD for ML systems
- **Reinforcement learning** — not covered; see CS234 for that
- **Data engineering and pipelines** — no ETL, feature stores, or data infrastructure
- **Beginner Python or math onboarding** — assumes prerequisites are already met
- **Business/product context for AI** — purely technical and academic in framing

## Canonical Resources
- Full lecture playlist (2017, widely cited edition): youtube_id=vT1JzLTH4G4
- Lecture 2 — Image Classification and kNN: youtube_id=OoUX-nOEjG0 [NOT VERIFIED]
- Lecture 3 — Loss Functions and Optimization: youtube_id=h7iBpEHGVNc [NOT VERIFIED]
- Lecture 4 — Backpropagation and Neural Networks: youtube_id=d14TUNcbn1k [NOT VERIFIED]
- Lecture 5 — Convolutional Neural Networks: youtube_id=bNb2fEVKeEo [NOT VERIFIED]
- Lecture 7 — Training Neural Networks Part II: youtube_id=_JB0AO7QxSA [NOT VERIFIED]
- Course notes — Neural Networks Part 1 (Andrej Karpathy authored): url=https://cs231n.github.io/neural-networks-1/
- Course notes — Backpropagation intuition: url=https://cs231n.github.io/optimization-2/
- Course notes — CNNs for visual recognition: url=https://cs231n.github.io/convolutional-networks/
- Full course website and syllabus: url=https://cs231n.github.io/
- Assignment 2 (BatchNorm, Dropout, CNN): url=https://cs231n.github.io/assignments2024/assignment2/

## Pairs Well With
- **3Blue1Brown** → for linear algebra and calculus prerequisites before starting CS231n lectures
- **Andrej Karpathy (micrograd/makemore series)** → CS231n provides the formal framework; Karpathy's solo work provides intimate code-first intuition for the same concepts
- **fast.ai (Jeremy Howard)** → CS231n for bottom-up mathematical rigor; fast.ai for top-down practical application — excellent complementary pair for CNNs and transfer learning
- **Yannic Kilcher** → for paper-level deep dives on architectures introduced in CS231n (ResNet, GANs, ViT)
- **deeplearning.ai (Andrew Ng)** → Ng for gentler mathematical onboarding and broader ML context; CS231n for vision-specific depth
- **Two Minute Papers** → for staying current on research directions that extend CS231n foundations

## Level
**Intermediate to Advanced**
Requires prior exposure to: multivariable calculus, linear algebra, probability, and Python programming. Suitable for upper-division undergraduates, graduate students, and self-taught practitioners who have completed at least one introductory ML course. Not appropriate as a first ML resource.

## Last Verified
2026-04-06