# Diffusion Models

## Video (best)
- **Yannic Kilcher** — "DDPM - Denoising Diffusion Probabilistic Models | Paper Explained"
- youtube_id: fbLgFrlTnGU
- Why: Kilcher walks through the DDPM paper rigorously, explaining the math behind the forward/reverse diffusion process, the noise schedule, and the training objective. He balances formalism with intuition, making it ideal for learners who want to understand *why* the math works, not just *what* the algorithm does.
- Level: intermediate/advanced

## Blog / Written explainer (best)
- **Lilian Weng** — "What are Diffusion Models?"
- url: https://lilianweng.github.io/posts/2021-07-11-diffusion-models/
- Why: Weng's post is the gold standard written explainer for diffusion models. It covers DDPM, score matching, SMLD, and the connections between them in a single coherent narrative. The mathematical derivations are complete but well-motivated, and the post has been updated over time to include newer developments. It serves as both an introduction and a lasting reference.
- Level: intermediate

## Deep dive
- **Lilian Weng** — "What are Diffusion Models?" (extended/updated version) + **Hugging Face Annotated Diffusion Models**
- url: https://huggingface.co/blog/annotated-diffusion
- Why: The Hugging Face annotated diffusion post by Niels Rogge and Kashif Rasul walks line-by-line through a full DDPM implementation in PyTorch, with inline explanations of every design choice. It bridges the gap between the mathematical formulation and working code better than almost any other resource, making it the best deep-dive for learners who need to go from theory to implementation.
- Level: advanced

## Original paper
- **Ho et al. (2020)** — "Denoising Diffusion Probabilistic Models"
- url: https://arxiv.org/abs/2006.11239
- Why: DDPM is the clearest and most pedagogically accessible entry point into the diffusion model literature. Unlike earlier score-based papers, it frames the problem in terms of a simple noise-prediction objective that is easy to implement and reason about. It is the paper that made diffusion models practically accessible and is the standard starting point for the field.
- Level: advanced

## Code walkthrough
- **Hugging Face / Niels Rogge & Kashif Rasul** — "The Annotated Diffusion Model" (notebook)
- url: https://colab.research.google.com/github/huggingface/notebooks/blob/main/examples/annotated_diffusion.ipynb
- Why: This Colab notebook implements DDPM from scratch on a small dataset (Fashion-MNIST / flowers), with every block of code directly annotated to the corresponding equation in the Ho et al. paper. It is the most direct "paper → code" walkthrough available and is maintained by Hugging Face, ensuring code quality and compatibility.
- Level: intermediate/advanced

---

## Coverage notes
- **Strong:** Core DDPM theory, score matching connections, mathematical derivations (Weng blog), paper-to-code translation (HF annotated diffusion)
- **Weak:** Classifier-free guidance and ControlNet have no single dedicated resource of comparable quality — they are typically covered as addenda in broader diffusion posts or in their own papers rather than in polished tutorials
- **Gap:** No excellent standalone beginner-friendly *video* exists that covers the full arc from DDPM → latent diffusion → Stable Diffusion in one place without either oversimplifying or assuming heavy prior knowledge. Most videos either stay at a high level or dive straight into paper-level math with little scaffolding. A 3Blue1Brown-style visual treatment of the diffusion process does not yet exist as of this writing.
- **Gap:** ControlNet specifically lacks a strong written pedagogical explainer at the level of Weng's diffusion post.

## Last Verified
2025-01-01 (YouTube ID and Colab URL marked — confirm before publishing to platform)