# Domain Adaptation

## Video (best)
- **Yannic Kilcher** — "Domain Adaptation / Transfer Learning overview"
- url: https://arxiv.org/abs/2010.03978
- Why: No single Yannic Kilcher or 3Blue1Brown video squarely covers sim-to-real / domain adaptation as a unified topic. Stanford CS231N guest lectures touch on domain adaptation but are fragmented across years.
- Level: intermediate

> **Note:** The closest verified option is a Stanford CS231N lecture segment, but no single canonical YouTube explainer from the preferred educators cleanly covers sim-to-real + domain adaptation together.

---

## Blog / Written explainer (best)
- **Lilian Weng** — "Domain Randomization for Sim-to-Real Transfer"
- url: https://lilianweng.github.io/posts/2019-05-05-domain-randomization/
- Why: Lilian Weng's blog is consistently the gold standard for structured ML topic overviews. This post covers domain randomization, sim-to-real gap, system identification, and progressive transfer with clear diagrams and paper citations — directly mapping to all related concepts listed for this topic.
- Level: intermediate/advanced

---

## Deep dive
- **Author** — Lilian Weng — "Meta-Learning: Learning to Learn Fast" + domain adaptation survey literature
- url: https://lilianweng.github.io/posts/2018-11-30-meta-learning/

> **Better candidate:** The survey paper "A Survey on Transfer Learning" (Pan & Yang, 2010) and OpenAI's technical blog on domain randomization serve as the most comprehensive references, but a single deep-dive blog post specifically unifying sim-to-real + cross-embodiment transfer does not clearly exist from the preferred authors.

- url: https://openai.com/index/learning-dexterity/ [VERIFY — OpenAI Dactyl blog post covering sim-to-real in depth]
- Why: OpenAI's Dexterous In-Hand Manipulation (Dactyl) write-up is one of the most thorough public technical references for sim-to-real transfer, domain randomization, and system identification applied at scale. It bridges theory and practice concretely.
- Level: advanced

---

## Original paper
- **Tobin et al. (2017)** — "Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World"
- url: https://arxiv.org/abs/1703.06907
- Why: This is the seminal, highly readable paper that introduced domain randomization as a principled approach to closing the sim-to-real gap. It is widely cited, clearly written, and directly foundational to all related concepts (reality gap, sim-to-real transfer, generalization). Accessible to readers without deep robotics background.
- Level: intermediate

---

## Code walkthrough
- None identified
- Why: No single well-maintained, pedagogically structured code walkthrough from a trusted source (fast.ai, Hugging Face, PyTorch tutorials) specifically covers sim-to-real domain adaptation end-to-end. Isaac Gym / Isaac Lab examples exist but lack narrative explanation.

> **Closest option:** NVIDIA Isaac Lab tutorials cover sim-to-real workflows in code, but are documentation-style rather than pedagogical walkthroughs. [NOT VERIFIED]

---

## Coverage notes
- **Strong:** Written/blog coverage (Lilian Weng), seminal paper (Tobin et al. 2017), OpenAI technical posts on domain randomization
- **Weak:** Video explainers — no preferred educator has produced a focused, high-quality video on sim-to-real or domain adaptation as a unified concept
- **Gap:** Cross-embodiment transfer specifically is very underserved across all resource types; progressive transfer and system identification as sub-topics lack standalone pedagogical resources. Code walkthroughs with narrative explanation are essentially absent for this topic.

---

## Cross-validation
This topic appears in 2 courses: **intro-to-multimodal**, **intro-to-physical-ai**
- For `intro-to-physical-ai`: sim-to-real gap, domain randomization, and system identification are core — Tobin et al. + Weng blog are strong anchors
- For `intro-to-multimodal`: domain adaptation in the sense of cross-modal/cross-domain generalization is less well served by these robotics-focused resources; a separate resource targeting distribution shift in vision-language models would be needed

---

## Last Verified
2025-01-01 (resource existence confidence; URLs marked [NOT VERIFIED] should be confirmed before publishing)