# Source: https://arxiv.org/pdf/2601.22513.pdf
# Author: Shi Fu et al.
# Title: Why Self-Rewarding Works: Theoretical Guarantees for Iterative Alignment of Language Models
# Fetched via: trafilatura
# Date: 2026-04-09

Why Self-Rewarding Works: Theoretical Guarantees for
Iterative Alignment of Language Models
Abstract
Self-Rewarding Language Models (SRLMs) achieve notable success in iteratively improving alignment without external feedback. Yet, despite their striking empirical progress, the core mechanisms driving their capabilities remain unelucidated, leaving a critical gap in theoretical understanding. This paper provides the first rigorous theoretical guarantees for SRLMs. We first establish a lower bound that characterizes the fundamental limits of a single update step, revealing a critical dependence on the quality of the initial model. We then derive finite-sample error bounds for the full iterative paradigm, showing that performance improves at a rate of with sample size . Crucially, our analysis reveals that the dependence on the initial model decays exponentially with the number of iterations . This provides a formal explanation for why self-rewarding succeeds: it robustly overcomes poor initialization by steering the dynamics toward internal stability and consistency. Finally, we instantiate our theoretical framework for the linear softmax model class, yielding tailored guarantees that connect our high-level insights to practical model architectures.
1 Introduction
Contemporary language models have achieved unprecedented success in numerous areas of natural language processing. Aligning these powerful models with human preferences is critical for their safe deployment, a task conventionally addressed by Reinforcement Learning from Human Feedback (RLHF) (Ouyang et al., [2022](https://arxiv.org/html/2601.22513v2#bib.bib715); Rafailov et al., [2023](https://arxiv.org/html/2601.22513v2#bib.bib716)). However, the efficacy of RLHF is fundamentally predicated on the availability of large-scale, high-quality human preference data. This reliance introduces two major challenges: first, the process of collecting human annotations is expensive and difficult to scale (Gao et al., [2023](https://arxiv.org/html/2601.22513v2#bib.bib717)); second, the inherent cognitive limitations of human evaluators may cap the performance of models intended to achieve superhuman capabilities (Burns et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib699)). Consequently, this dependence on external supervision forms a critical bottleneck, hindering the development of more autonomous and capable AI systems (Huang et al., [2022](https://arxiv.org/html/2601.22513v2#bib.bib617), [2025](https://arxiv.org/html/2601.22513v2#bib.bib657)).
To overcome these limitations, the paradigm of Self-Rewarding Language Models (SRLMs) has emerged, demonstrating considerable potential (Yuan et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib692); Wu et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib700); Prasad et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib693)). This approach facilitates iterative self-alignment without external feedback by enabling the language model to serve as both its own policy and reward model. Within this framework, the model generates candidate responses and leverages its intrinsic judgment to assign rewards, using this self-generated supervision to produce a refined policy that serves as the reward model for the subsequent iteration. The efficacy of this approach has been empirically validated in recent studies (Yuan et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib692); Zhou et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib704); Wang et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib694); Xiong et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib706); Li et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib703)), which report significant performance gains across a variety of tasks.
However, despite the remarkable empirical success of SRLMs, our understanding of their core working mechanisms remains limited. Why do these models achieve stable and continuous improvement rather than succumbing to degeneration or even collapse (Shumailov et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib622))? Current research largely remains at the level of empirical observation and methodological refinement, lacking a solid theoretical foundation to explain the reasons for their success or to characterize their performance boundaries. This theoretical gap prevents us from deeply understanding the capability limits and potential risks of SRLMs, and it constrains our ability to pursue more profound improvements.
To fill this critical theoretical void, this paper provides the first rigorous theoretical guarantees for the iterative self-rewarding alignment process in language models. Our main contributions can be summarized as follows:
-
•
Fundamental Limitations of Single-Step Updates. We establish a theoretical lower bound on the failure probability of a single-step update, proving its critical dependence on the initial model’s quality. This result theoretically explains why poorly initialized models fail to achieve effective alignment in one step.
-
•
Finite-Sample Guarantees for Iteration. We derive finite-sample error bounds for the iterative self-rewarding paradigm, proving that its performance steadily improves at a rate of as the sample size increases. Our analysis explicitly shows that the dependence on the initial model’s quality decays exponentially with the number of iterations .
-
•
The Core Mechanism of Iterative Alignment. We identify the mechanism that explains why self-rewarding works: the iterative update operates as a contraction mapping on the policy condition number , which reflects both the model’s internal consistency and alignment stability. This dynamic causes the impact of poor initialization to vanish exponentially, allowing the system to self-stabilize and achieve internal consistency before improving performance, thus overcoming the single-step failure barrier.
-
•
Application to Linear Softmax Models. We apply our general theoretical framework to the linear softmax model class, deriving performance guarantees for this specific model architecture. This connects our theoretical insights with practical application.
2 Related Work
In this section, we review the literature most relevant to our work. We discuss recent advancements in SRLMs, followed by theoretical guarantees for self-training.
Self-Rewarding Language Models. Existing alignment methods, particularly RLHF, heavily rely on high-quality reward models or continuous human feedback, which creates a major bottleneck for scalability. To overcome this, Yuan et al. ([2024](https://arxiv.org/html/2601.22513v2#bib.bib692)) proposed the SRLM paradigm, which leverages the language model itself to act as both the policy and the reward model. In this framework, the policy model generates response candidates for unlabeled prompts, while the reward model employs intrinsic self-evaluation to score these responses based on their quality (Zheng et al., [2023](https://arxiv.org/html/2601.22513v2#bib.bib695); Wataoka et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib697); Gu et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib698)). This process can be iteratively repeated to improve alignment performance without human intervention (Zhao et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib705); Xiong et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib706); Chen et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib707)).
Recent research has concentrated on further refining the SRLM framework, with a particular emphasis on improving training stability and data quality. For instance, Wang et al. ([2025](https://arxiv.org/html/2601.22513v2#bib.bib694)) introduced regularization to enhance the consistency of DPO rewards across different iterations, thus providing more robust preference data. Additionally, Prasad et al. ([2025](https://arxiv.org/html/2601.22513v2#bib.bib693)) and Zhou et al. ([2025](https://arxiv.org/html/2601.22513v2#bib.bib702)) focused on enhancing consistency to improve the reliability of both the reward models and the preference data. The paradigm has also been extended to new modalities, with Zhou et al. ([2024](https://arxiv.org/html/2601.22513v2#bib.bib704)) and Li et al. ([2025](https://arxiv.org/html/2601.22513v2#bib.bib703)) successfully applying it to Vision-Language Models (VLMs). However, despite significant empirical progress and effectiveness, to the best of our knowledge, a complete and rigorous theoretical analysis of SRLMs is still missing. This gap prevents a deep understanding of the internal mechanisms that explain why this paradigm is successful.
Theoretical Guarantees for Self-Training. Theoretical work on self-training remains limited. Existing research has predominantly focused on the self-distillation objective (Hinton et al., [2015](https://arxiv.org/html/2601.22513v2#bib.bib708)) in classification and regression tasks, aiming to provide convergence guarantees. Several studies have established theoretical guarantees for self-training under idealized settings, such as linear models (Mobahi et al., [2020](https://arxiv.org/html/2601.22513v2#bib.bib709); Frei et al., [2022](https://arxiv.org/html/2601.22513v2#bib.bib711); Das and Sanghavi, [2023](https://arxiv.org/html/2601.22513v2#bib.bib710); Pareek et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib712)). Furthermore, Allen-Zhu and Li ([2023](https://arxiv.org/html/2601.22513v2#bib.bib713)) offered guarantees for feed-forward neural networks, while Boix-Adsera ([2024](https://arxiv.org/html/2601.22513v2#bib.bib714)) proposed a more general PAC-style framework. Another line of related work investigates the problem of model collapse in self-consuming training loops (Alemohammad et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib624); Bertrand et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib626)). These works explore this direction by analyzing population risk dynamics under specific modeling assumptions, such as linear contexts (Dohmatob et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib628); Feng et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib660)), Gaussian models (Shumailov et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib622); Alemohammad et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib624); Suresh et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib672); Jain et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib673)), and asymptotic regimes (Marchi et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib650)). Further explorations have been conducted in the context of simplified diffusion models (Fu et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib618)) and attention-based architectures (Fu et al., [2025b](https://arxiv.org/html/2601.22513v2#bib.bib658)). In the area of self-improvement, Huang et al. ([2025](https://arxiv.org/html/2601.22513v2#bib.bib657)) proposed a sharpening mechanism as a key driver of self-improvement and extended the theoretical framework of self-training to language models. However, their work is confined to a non-iterative setting.
In contrast to all prior work, this paper establishes the first rigorous theoretical framework for the iterative alignment paradigm of SRLMs. By deeply analyzing the underlying mechanisms that enable stable and progressive performance improvements, we theoretically explain the success of this paradigm and provide stringent convergence rates and performance guarantees.
3 Preliminaries
This section establishes the notation and theoretical background. We formally define the core components of the SRLM paradigm (Yuan et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib692); Wang et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib694)), to be the model class, the reward mechanism, and the DPO-style training objective that governs model updates.
Notations and Setup.
Let denote a prompt and be a response, where for a vocabulary space and a sequence length . A language model is a conditional distribution that maps a prompt to a distribution over responses. We assume prompts are drawn from a distribution over the prompt space . The term denotes the probability that the model generates response given . The self-rewarding process iteratively applies updates at each round , starting from an initial model and yielding the sequence of models .
Self-Reward Mechanism and Data Generation.
The process relies on a self-reward signal generated by the model itself. Consistent with prior work (Yoon et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib734); Zhang et al., [2025a](https://arxiv.org/html/2601.22513v2#bib.bib735), [b](https://arxiv.org/html/2601.22513v2#bib.bib736)), we utilize the model’s own likelihood assignment as a proxy for its intrinsic assessment of generation quality. Specifically, aligning with the formulation in the literature (Huang et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib657); Agarwal et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib732); Du et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib733)), the reward for a response given a prompt under the current policy is defined as its log-probability:
| (1) |
This self-referential reward function encourages the model to assign higher probability mass to sequences it already deems plausible, effectively reinforcing regions of high internal consistency within the response space. To prepare for the update at round , a dataset of examples is constructed. Each example is formed by first sampling a prompt , then generating two responses . Subsequently, their relative quality is measured by the self-reward difference, .
This stylized self-reward function has been widely adopted in the literature (Huang et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib657); Agarwal et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib732); Du et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib733)). Moreover, recent empirical breakthroughs (Du et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib733)) demonstrate that such raw log-probability rewards can surprisingly outperform complex, trained reward models in reasoning tasks. Consequently, our work provides the rigorous theoretical grounding for this emerging paradigm, isolating the internal stability mechanisms that drive its empirical success.
Model Update via DPO.
The goal of each training round is to improve the model via a KL-regularized objective. We seek a new model that maximizes the expected reward while remaining close to the current model , which acts as the reference . This is formulated as:
| (2) |
In practice, this optimization can be achieved by minimizing a DPO-style regression objective (Rafailov et al., [2023](https://arxiv.org/html/2601.22513v2#bib.bib716); Gao et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib718); Huang et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib657)). Specifically, for round where the reference model is , the loss function is defined as:
| (3) |
where . Minimizing this loss, , effectively executes the model improvement step outlined in Eq. ([2](https://arxiv.org/html/2601.22513v2#S3.E2)). This entire update can be conceptualized as the application of an operator , which maps the current model to the improved model by minimizing the DPO loss with the reference model set to :
| (4) |
After rounds, the final model is the result of composing these operators: . Since the reward is determined by , the training loop is entirely self-contained.
4 Fundamental Limitations of Single-Step Self-Rewarding
This section introduces the Policy Condition Number111This quantity is analogous to what is sometimes called the concentrability or coverage coefficient, a concept studied in the theory of offline reinforcement learning and self-improvement (Xie et al., [2023](https://arxiv.org/html/2601.22513v2#bib.bib719); Gao et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib718); Amortila et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib720); Huang et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib657))., a metric designed to quantify a model’s suitability for self-alignment. It characterizes both the model’s internal consistency and the numerical stability of the self-rewarding update process. Building on this concept, we derive a formal lower bound on the failure rate of a single update step, revealing its fundamental limitations. Furthermore, we show how these learning failures inevitably translate into inference errors under greedy decoding, highlighting the necessity of an iterative framework.
The policy condition number, denoted , is formally defined as the expected inverse probability of the policy’s own most likely response:
| (5) |
where . Drawing an analogy from numerical analysis, this parameter measures how well-conditioned the policy is for self-reward. A large value of signifies an ill-conditioned policy, one that is diffuse and lacks confidence in its own predictions by assigning low probability to its modal outputs. This ill-conditioning makes the single-step update unreliable and heightens the risk of model collapse (Shumailov et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib622)). A central finding of our work is that while a large initial condition number can lead to failure, the iterative process progressively controls this quantity and ensures that its influence diminishes over time.
We now present a formal lower bound on the failure rate for any self-rewarding algorithm operating within a single iteration. The result is established by considering a worst-case instance where subtle statistical signals are intentionally obscured by an information-sparse prompt distribution.
Theorem 4.1 (Single-Step Failure Rate Lower Bound).
Let any self-rewarding algorithm produce a model using samples generated from a base model . There exists a hard problem instance, characterized by a model class and an initial policy condition number , such that the failure rate of any algorithm with a fixed budget is lower-bounded. Failure is defined as the event that the policy assigns a probability of at most to its own optimal response . The risk-form of the lower bound is given by:
| (6) |
where hides logarithmic factors with respect to and .
Remark 4.2.
Theorem [4.1](https://arxiv.org/html/2601.22513v2#S4.Thmtheorem1) formalizes the statistical barriers of a single self-rewarding step. This expression makes clear that when the effective difficulty is on the same order as the sample size , the failure rate lower bound remains a constant. In such cases, a single self-rewarding update cannot reliably improve the model, regardless of the algorithmic details. Two concrete scenarios illustrate when can be on the same order as :
-
•
Near-uniform base policy. Suppose the base model assigns a nearly uniform distribution over a large response space of size . Then the most likely response has probability only slightly larger than , so
If the sample budget is not significantly larger than , then is a constant, leading to a constant failure probability.
-
•
Autoregressive low-confidence base policy. Consider an -step autoregressive model where at each step the top-1 token probability is at most . Along the modal path, the probability of the full sequence satisfies , so that
If we set , then , which implies that is of the same order as the sample budget , leading to a failure rate lower bounded away from zero.
These examples show that diffuse or low-confidence base policies naturally yield on the scale of , which makes a single self-rewarding update statistically unreliable.
The failure condition , adopted in Theorem [4.1](https://arxiv.org/html/2601.22513v2#S4.Thmtheorem1), is a natural threshold. As the subsequent proposition reveals, it precisely identifies the circumstances under which greedy decoding fails. Consequently, the lower bound reflects a meaningful and practically relevant notion of decoder breakdown.
Proposition 4.3 (Greedy Decoding Fails for Unaligned Models).
There exist autoregressive models over the space and prompts for which the optimal sequence is unique, and its probability satisfies . Then, the greedy decoding strategy, defined as for all , fails to recover the optimal sequence, i.e., .
Remark 4.4.
Proposition [4.3](https://arxiv.org/html/2601.22513v2#S4.Thmtheorem3) demonstrates the direct and severe consequence of a low-confidence model at inference time. It establishes that for certain models, standard decoding algorithms such as greedy search are guaranteed to fail. This failure occurs because the model’s confidence in its single best prediction is outweighed by its collective uncertainty over all other alternatives, allowing a locally optimal yet globally incorrect token to trap a myopic decoder and ensure a suboptimal sequence.
This result bridges learning failure and inference failure. The low-confidence condition is not a pathological corner case but a statistically predictable outcome of learning. As shown by Theorem [4.1](https://arxiv.org/html/2601.22513v2#S4.Thmtheorem1), a single self-rewarding update initialized with a poorly conditioned base policy (large policy condition number ) has a non-negligible probability of producing exactly such a low-confidence model.
Taken together, the two results yield a stark conclusion. When the effective difficulty satisfies , Theorem [4.1](https://arxiv.org/html/2601.22513v2#S4.Thmtheorem1) implies a constant-order lower bound on the probability of learning failure. Consequently, for sufficiently weak initialization, there is a constant probability that a single update produces a policy that, by Proposition [4.3](https://arxiv.org/html/2601.22513v2#S4.Thmtheorem3), is certain to output low-quality sequences under greedy decoding. This cascade of failure, from a high probability of learning error to a deterministic inference error, exposes the fundamental vulnerability of single-step self-improvement and its critical dependence on the initial model. This motivates the iterative self-rewarding framework developed in the subsequent sections, which progressively mitigates this dependence and enables robust alignment even from weak initialization.
5 Finite-Sample Analysis for Iterative Self-Rewarding Alignment
This section addresses the fundamental limitations of single-step updates identified in Section [4](https://arxiv.org/html/2601.22513v2#S4) by developing a theoretical framework for iterative self-rewarding alignment. Within this framework, we establish finite-sample guarantees showing that sustained improvements across iterations overcome the fragility of a single step, yielding a provably stable process that ensures robust alignment even from poorly conditioned initial models. To formalize this, we first introduce a standard realizability assumption and define key analytical constants.
Assumption 5.1 (Realizability).
Let be the optimal model that maximizes the KL-regularized objective in Eq. ([2](https://arxiv.org/html/2601.22513v2#S3.E2)). We assume that this model is contained within our model class, i.e., .
Assumption [5.1](https://arxiv.org/html/2601.22513v2#S5.Thmtheorem1) is a natural and standard requirement in statistical learning theory (Vapnik, [2013](https://arxiv.org/html/2601.22513v2#bib.bib76); Shalev-Shwartz and Ben-David, [2014](https://arxiv.org/html/2601.22513v2#bib.bib602)), ensuring that the target model lies within the considered class. Then, we define analytical constants that capture the stability of iterative self-rewarding updates.
Definition 5.2 (Confidence and Margin Constants).
We introduce two analytical constants that quantify the stability of self-rewarding updates:
-
•
Minimum confidence. The minimum confidence across all inputs and update rounds is defined as
-
•
Margin constant. The margin quantifies the minimum log-probability gap between the optimal action and the strongest suboptimal competitor across all rounds:
The minimum confidence threshold ensures that the model retains a non-trivial level of certainty in its predictions during the iterative process. This requirement is a standard practice in the literature (Zhang et al., [2023](https://arxiv.org/html/2601.22513v2#bib.bib621); Huang et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib657); Fu et al., [2025a](https://arxiv.org/html/2601.22513v2#bib.bib737)). The margin , which quantifies the separation between the optimal action and its closest competitor, is similarly well-established (Simchowitz and Jamieson, [2019](https://arxiv.org/html/2601.22513v2#bib.bib738); Velegkas et al., [2022](https://arxiv.org/html/2601.22513v2#bib.bib739); Huang et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib657)). The assumption of a unique optimal sequence implies a strictly positive margin, as identifiability necessitates that the optimal response be distinguishable from suboptimal alternatives. Furthermore, in continuously parameterized models, exact ties () constitute a set of measure zero and are therefore negligible in practice.
Theorem 5.3 (Finite-Sample Guarantee for Iterative Self-Rewarding Alignment).
Remark 5.4.
Theorem [5.3](https://arxiv.org/html/2601.22513v2#S5.Thmtheorem3) provides the first finite-sample guarantee for the iterative self-rewarding alignment paradigm, establishing a foundational theoretical framework for a class of methods that, despite their empirical success, have lacked rigorous understanding. To further clarify the asymptotic behavior of Eq. (7): When the sample size is sufficiently large and the number of iterations is large enough (as shown in Corollary [5.7](https://arxiv.org/html/2601.22513v2#S5.Thmtheorem7), i.e., ), the initialization-dependent term vanishes. Consequently, up to logarithmic factors and problem-dependent constants (), the error bound simplifies to , demonstrating that the iterative process achieves the standard parametric convergence rate. The theorem formally quantifies the risk that the final model, , assigns insufficient probability mass to its own optimal response after rounds of updates. The structure of the bound in Eq. ([7](https://arxiv.org/html/2601.22513v2#S5.E7)) reveals a compelling interplay between two key error components. The overall error probability is upper-bounded by a product of the standard statistical learning rate, , and a term, , that comprises both a stable and a transient error component. The constituents of this bound can be interpreted as follows:
-
•
Statistical Efficiency: The rate confirms that the iterative process is statistically efficient, with performance improving predictably as the sample size per iteration increases.
-
•
Stable Error Component: The first term in the parentheses, , represents an asymptotic, irreducible error floor that is independent of the initial model’s quality. This error is governed by the model’s minimum confidence, , reflecting the best possible stability the system can achieve after sufficient iteration.
-
•
Transient Error Component: The second term, , captures the influence of the initial model’s quality, as measured by the policy condition number . Crucially, this term decays exponentially with the number of iterations . This finding not only theoretically validates the intuition that the iterative process progressively mitigates the adverse effects of a poor initialization, but also aligns with the experimental results in (Yuan et al.,
[2024](https://arxiv.org/html/2601.22513v2#bib.bib692); Zhou et al.,[2025](https://arxiv.org/html/2601.22513v2#bib.bib702); Xiong et al.,[2025](https://arxiv.org/html/2601.22513v2#bib.bib706)). Specifically, these results show that performance improves significantly in the early stages of iteration before plateauing, a pattern characteristic of exponential decay.
Furthermore, the bound’s dependence on and is shown to be tight for the single-step () case. Consider this special case, where the exponential decay term’s denominator becomes one. For an ill-conditioned initial model where is large, the term will dominate the term. Ignoring logarithmic factors and constants, the upper bound on the failure probability simplifies to . This rate precisely matches the fundamental lower bound of established in Theorem [4.1](https://arxiv.org/html/2601.22513v2#S4.Thmtheorem1) for any single-step self-rewarding algorithm. This correspondence demonstrates that our multi-step analysis correctly captures the problem’s intrinsic difficulty for the single-step scenario and confirms as a central parameter governing the challenge of self-alignment.
Remark 5.5.
Why Self-Rewarding Works.
Theorem [5.3](https://arxiv.org/html/2601.22513v2#S5.Thmtheorem3) provides a fundamental explanation for the success of iterative self-rewarding: it transforms a single-step learning problem that would almost certainly fail under poor initialization (large ) into a robust two-stage process.
A large initial condition number corresponds to an ill-conditioned model. Theorem [4.1](https://arxiv.org/html/2601.22513v2#S4.Thmtheorem1) shows that for such models, a single update fails with probability . Thus, naive one-shot fine-tuning cannot overcome poor initialization. In contrast, iterative self-rewarding acts as an internal self-correction mechanism, thereby avoiding this difficulty.
Stage I: Self-Correction and Stabilization. The early iterations are not aimed at fitting an external true preference. Instead, the model aligns internally by rewarding its own high-confidence outputs. This self-reinforcing process induces a contraction mapping on the policy condition number , ensuring exponential convergence toward a stable fixed point. The proof in Appendix [C](https://arxiv.org/html/2601.22513v2#A3) formalizes this effect, showing that under mild assumptions, the sequence satisfies
where is the fixed-point condition number as , and is the transient initialization component, which decays geometrically with each iteration. Hence, the adverse influence of poor initialization quickly disappears, guiding the model into a well-conditioned regime. This stage functions as an implicit regularization, prioritizing internal consistency before external generalization.
Stage II: Efficient Statistical Learning. Once stabilized, the effect of becomes negligible. As the initialization-dependent term in Theorem [5.3](https://arxiv.org/html/2601.22513v2#S5.Thmtheorem3) vanishes exponentially, the learning dynamics undergo a fundamental shift: they are no longer constrained by the starting point, but are governed by statistical efficiency. Performance improvements follow the standard rate, determined solely by the per-round sample size . Ultimately, the process converges to a stable error floor that is independent of initialization, with the final accuracy dictated only by problem difficulty and statistical error.
Iterative self-rewarding succeeds by decomposing the learning problem into two phases: first stabilizing the model through self-alignment dynamics, and then leveraging this stable foundation for efficient statistical learning. In doing so, the framework enforces internal consistency of the model, thereby creating the necessary conditions for effective learning and turning a seemingly hopeless single-step task into a standard, well-behaved learning process.
Remark 5.6 (Proof Sketch for Theorem [5.3](https://arxiv.org/html/2601.22513v2#S5.Thmtheorem3)).
This proof establishes finite-sample guarantees for iterative self-rewarding alignment, showing it overcomes the limitations of a poor initial model. The core technique is to recursively control the policy condition number . Controlling prevents model collapse and ensures the influence of the initial model’s quality, , diminishes over time.
Step 1. Single-Step Optimality Gap. First, we bound the single-step failure probability, the chance that an updated policy assigns low probability to its own optimal response. This probability is linked to a performance gap that is controlled by statistical error and the stability of the previous policy . This yields guarantees connecting the performance to the policy condition number:
This inequality forms the inductive link for the analysis.
Step 2. Recursive Control of the Policy Condition Numbers. To ensure stability, we derive a recursive inequality for . We start with its tail-integral representation:
The integrand is the failure probability bounded in Step 1. Substituting this bound into the integral yields the core recurrence relation:
where are constants. The sub-linear dependency on is crucial, as it prevents explosive growth and ensures the process is stable.
Step 3. Asymptotic Stability and Final Bound. Finally, we analyze the recurrence for . It simplifies to a contraction mapping that converges exponentially fast to a fixed point . This gives an explicit bound on the condition number at iteration :
where the contraction rate scales as approximately . This decomposition reveals that comprises a stable term and an exponentially decaying transient term that depends on the initial condition . Substituting this bound for into the single-step guarantee for the final iteration yields the main result of Theorem [5.3](https://arxiv.org/html/2601.22513v2#S5.Thmtheorem3). The final bound consists of a stable error term with a rate of and a transient error term, which depends on and decays exponentially with . This proves that the iterative process robustly mitigates the influence of a poor initialization.
Corollary 5.7 (Iterations to Suppress Initialization Effects).
Building on Theorem [5.3](https://arxiv.org/html/2601.22513v2#S5.Thmtheorem3), if the number of iterations satisfies
then the initialization-dependent part of the bound becomes negligible, and with probability at least ,
Remark 5.8.
Corollary [5.7](https://arxiv.org/html/2601.22513v2#S5.Thmtheorem7) distills and clarifies the core mechanism that underpins the success of iterative self-rewarding alignment. The self-correcting property provides a theoretical safeguard against model collapse, where a flawed initial model might otherwise amplify its own biases through iteration. The theory demonstrates that the iterative process effectively mitigates the influence of the initial unaligned model, allowing the policy to bootstrap its way to improvement based on the signal generated during training.
The corollary also establishes that this self-correction process is both efficient and practical. The number of iterations required to suppress the initial model’s influence to a negligible level, given by , depends only logarithmically on the initial condition number . This suggests that even an initially ill-conditioned model can be reliably aligned without requiring an excessive number of iterations, which is consistent with experimental findings (Yuan et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib692); Zhou et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib702); Xiong et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib706)).
Furthermore, the denominator confirms the theoretical intuition that increasing the per-iteration sample size accelerates the decay of the initial model’s influence. Consequently, this reduces the total number of iterations required for alignment. This relationship is consistent with the principle that a larger sample size enables the model to learn more effectively within each round, thereby diminishing the number of iterative steps needed. This finding provides clear guidance for allocating computational resources during the alignment process.
Ultimately, after a sufficient number of iterations, the process fundamentally overcomes the bottleneck inherent in single-step alignment. The resulting error bound, , becomes entirely independent of the initial condition number . This demonstrates that the iterative framework transforms the learning problem from one constrained by initial model quality, as captured by the lower bound in Theorem [4.1](https://arxiv.org/html/2601.22513v2#S4.Thmtheorem1), into a standard statistical learning problem where performance is governed by sample size. The iterative process is therefore not merely a refinement but a powerful mechanism. It enables the model to overcome the constraining influence of its initialization, breaking the barrier to achieve a level of performance unattainable through single-step methods.
6 Application to Parametric Models: The Linear Softmax Case
In this section, we instantiate our general framework for SRLMs within the parametric setting of linear softmax models.
Definition 6.1 (Linear Softmax Model).
Let be the feature dimension, and let be a feature map such that . Given a radius , the linear softmax model class is defined as:
where the policy is formally defined as: . This class is parameterized by a vector within a -dimensional ball of radius .
By adapting our proof framework with tools from statistical learning theory, we establish a performance guarantee for the linear softmax model class, analogous to Theorem [5.3](https://arxiv.org/html/2601.22513v2#S5.Thmtheorem3), thereby demonstrating that the self-rewarding process remains both stable and effective.
Theorem 6.2 (Performance Guarantee for Linear Softmax Models).
Under the same conditions as Theorem [5.3](https://arxiv.org/html/2601.22513v2#S5.Thmtheorem3), but applied to the linear softmax class , after rounds of self-rewarding updates, the final policy ensures that with probability at least :
Furthermore, if the number of iterations satisfies , then we obtain:
Remark 6.3.
Theorem [6.2](https://arxiv.org/html/2601.22513v2#S6.Thmtheorem2) above instantiates our general framework in Theorem [5.3](https://arxiv.org/html/2601.22513v2#S5.Thmtheorem3) for a continuous parametric model class. Notably, the complexity term from the finite class setting is replaced by a geometric entropy term arising from covering the parameter space. In particular, the bound’s complexity factor scales as , reflecting the metric entropy of a -dimensional parameter ball instead of the simple count . This signifies a shift from combinatorial complexity to the complexity of a continuous function class, introducing an explicit polynomial dependence on the ambient feature dimension . Moreover, while the iterative procedure eventually cancels out the effect of initialization, we note that the iteration threshold still carries an implicit dependence on through the initial condition . In worst-case high-dimensional scenarios (e.g. an uninformative initial policy in a large feature space), can grow with , meaning that more iterations may be required for the benefits of self-alignment to fully manifest.
Despite the above guarantee, the statistical rate in Theorem [6.2](https://arxiv.org/html/2601.22513v2#S6.Thmtheorem2) still exhibits a polynomial dependence on the ambient dimension , which can be overly conservative in modern high-dimensional settings. To mitigate this apparent curse of dimensionality, we refine the analysis by introducing a data-dependent complexity measure grounded in the spectral structure of the feature space. In particular, the ambient dimension is replaced with an effective dimension that reflects the eigenvalue decay of the feature covariance . By aligning the complexity term with the concentration of variance within a lower-dimensional subspace, we obtain stronger bounds that adapt to the true intrinsic dimensionality of the data, as formalized in Corollary [6.4](https://arxiv.org/html/2601.22513v2#S6.Thmtheorem4).
Corollary 6.4 (Linear-Softmax under Exponential Spectral Decay).
Assume the feature covariance has eigenvalues satisfying exponential decay for some . Using the effective-dimension argument with ridge parameter , the iteration threshold that suppresses initialization is . Moreover, with probability at least ,
In particular, the ambient-dimensional factor is replaced by a doubly logarithmic dependence via .
Remark 6.5 (Effective Dimension and Spectral Decay).
Corollary [6.4](https://arxiv.org/html/2601.22513v2#S6.Thmtheorem4) introduces a refined assumption that the eigenvalues of the feature covariance decay exponentially, which is consistent with the feature geometry observed in modern large-scale language models (Dong et al., [2021](https://arxiv.org/html/2601.22513v2#bib.bib691)). In practice, pretrained model representations often exhibit a rapidly decaying spectrum, with most of the variance concentrated in the top principal components (Ethayarajh, [2019](https://arxiv.org/html/2601.22513v2#bib.bib689); Saglam et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib690)). This structural property implies that the feature space is effectively low-dimensional. Under an exponential decay profile , the ridge effective dimension remains substantially smaller than the ambient dimension for moderate regularization . For instance, choosing yields rather than . This shows that although the model may have parameters, the complexity of its learned representation is governed by a much smaller effective number of directions. This observation provides a natural explanation for the apparent paradox that overparameterized models can still generalize effectively. Intuitively, most parameters correspond to directions in the feature space with negligible variance and thus do not significantly affect generalization error, allowing an overparameterized model to behave as if it were much smaller. A more detailed discussion is provided in Section [G](https://arxiv.org/html/2601.22513v2#A7) of the Appendix. The key insight is that generalization is governed by the effective dimension , not the ambient dimension . Scaling laws emerge because larger models have the capacity to learn feature representations with faster spectral decay. This aligns with benign overfitting, where models generalize well despite over-parameterization by using a low-dimensional signal structure. While our guarantees hold for linear softmax models, extending this analysis to full Transformers remains a significant challenge and valuable future direction.
7 Conclusion
In this paper, we establish the first rigorous theoretical framework for Self-Rewarding Language Models (SRLMs), effectively bridging the gap between their striking empirical success and the previous lack of formal guarantees. By analyzing the underlying self-rewarding mechanisms, our work provides a mathematical explanation for how language models can iteratively improve their alignment capabilities without relying on external human supervision.
We first characterize the fundamental limits of single-step updates by establishing a sharp lower bound on the failure probability. This reveals that non-iterative approaches critically depend on the quality of the initial model and are prone to failure under poor initialization. In contrast, for the full iterative paradigm, we derive finite-sample error bounds showing that performance improves at a rate of , while dependence on the initial model decays exponentially. This result uncovers the core mechanism behind the success of SRLMs: iterative dynamics act as a stabilization process that robustly overcomes weak initialization by steering the model toward internal consistency. We further substantiate this framework within the linear softmax model class, connecting our high-level theoretical insights to parametric architectures. As language models scale, such theoretical foundations are essential for designing robust, continuously self-evolving systems.
References
-
The unreasonable effectiveness of entropy minimization in llm reasoning.
arXiv preprint arXiv:2505.15134.
Cited by:
[§3](https://arxiv.org/html/2601.22513v2#S3.SS0.SSS0.Px2.p1.3),[§3](https://arxiv.org/html/2601.22513v2#S3.SS0.SSS0.Px2.p2.1). -
Self-consuming generative models go mad.
In The Twelfth International Conference on Learning Representations,
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p4.1). -
Towards understanding ensemble, knowledge distillation and self-distillation in deep learning.
In The Eleventh International Conference on Learning Representations,
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p4.1). -
An information-theoretical approach to semi-supervised learning under covariate-shift.
In International Conference on Artificial Intelligence and Statistics,
pp. 7433–7449.
Cited by:
[Appendix A](https://arxiv.org/html/2601.22513v2#A1.p2.2). -
Robust semi-supervised learning via f-divergence and -rényi divergence.
In 2024 IEEE International Symposium on Information Theory (ISIT),
pp. 1842–1847.
Cited by:
[Appendix A](https://arxiv.org/html/2601.22513v2#A1.p2.2). -
Semi-supervised batch learning from logged data.
arXiv preprint arXiv:2209.07148.
Cited by:
[Appendix A](https://arxiv.org/html/2601.22513v2#A1.p4.1). -
Scalable online exploration via coverability.
In International Conference on Machine Learning,
pp. 1392–1455.
Cited by:
[footnote 1](https://arxiv.org/html/2601.22513v2#footnote1). -
Batch learning via log-sum-exponential estimator from logged bandit feedback.
In ICML 2024 Workshop: Aligning Reinforcement Learning Experimentalists and Theorists,
Cited by:
[Appendix A](https://arxiv.org/html/2601.22513v2#A1.p4.1). -
Log-sum-exponential estimator for off-policy evaluation and learning.
In Forty-second International Conference on Machine Learning,
Cited by:
[Appendix A](https://arxiv.org/html/2601.22513v2#A1.p4.1). -
Remixmatch: semi-supervised learning with distribution alignment and augmentation anchoring.
arXiv preprint arXiv:1911.09785.
Cited by:
[Appendix A](https://arxiv.org/html/2601.22513v2#A1.p2.2). -
Mixmatch: a holistic approach to semi-supervised learning.
Advances in neural information processing systems 32.
Cited by:
[Appendix A](https://arxiv.org/html/2601.22513v2#A1.p2.2). -
On the stability of iterative retraining of generative models on their own data.
In The Twelfth International Conference on Learning Representations,
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p4.1). -
Towards a theory of model distillation.
arXiv preprint arXiv:2403.09053.
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p4.1). -
Weak-to-strong generalization: eliciting strong capabilities with weak supervision.
In Forty-first International Conference on Machine Learning,
Cited by:
[§1](https://arxiv.org/html/2601.22513v2#S1.p1.1). -
Language models are hidden reasoners: unlocking latent reasoning capabilities via self-rewarding.
arXiv preprint arXiv:2411.04282.
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p2.1). -
Understanding self-distillation in the presence of label noise.
In International Conference on Machine Learning,
pp. 7102–7140.
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p4.1). -
Model collapse demystified: the case of regression.
arXiv preprint arXiv:2402.07712.
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p4.1). -
Attention is not all you need: pure attention loses rank doubly exponentially with depth.
In International conference on machine learning,
pp. 2793–2803.
Cited by:
[Remark 6.5](https://arxiv.org/html/2601.22513v2#S6.Thmtheorem5.p1.11). -
Confidence as a reward: transforming llms into reward models.
arXiv preprint arXiv:2510.13501.
Cited by:
[§3](https://arxiv.org/html/2601.22513v2#S3.SS0.SSS0.Px2.p1.3),[§3](https://arxiv.org/html/2601.22513v2#S3.SS0.SSS0.Px2.p2.1). -
How contextual are contextualized word representations? comparing the geometry of bert, elmo, and gpt-2 embeddings.
arXiv preprint arXiv:1909.00512.
Cited by:
[Remark 6.5](https://arxiv.org/html/2601.22513v2#S6.Thmtheorem5.p1.11). -
Beyond model collapse: scaling up with synthesized data requires verification.
In The Thirteenth International Conference on Learning Representations,
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p4.1). -
Self-training converts weak learners to strong learners in mixture models.
In International Conference on Artificial Intelligence and Statistics,
pp. 8003–8021.
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p4.1). -
Self-verification provably prevents model collapse in recursive synthetic training.
In The Thirty-ninth Annual Conference on Neural Information Processing Systems,
External Links:
[Link](https://openreview.net/forum?id=X5Hk8aMs6w)Cited by:[§5](https://arxiv.org/html/2601.22513v2#S5.p3.3). -
A theoretical perspective: how to prevent model collapse in self-consuming training loops.
In The Thirteenth International Conference on Learning Representations,
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p4.1). -
Towards theoretical understandings of self-consuming generative models.
In Forty-first International Conference on Machine Learning,
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p4.1). -
Scaling laws for reward model overoptimization.
In International Conference on Machine Learning,
pp. 10835–10866.
Cited by:
[§1](https://arxiv.org/html/2601.22513v2#S1.p1.1). -
Rebel: reinforcement learning via regressing relative rewards.
Advances in Neural Information Processing Systems 37, pp. 52354–52400.
Cited by:
[§3](https://arxiv.org/html/2601.22513v2#S3.SS0.SSS0.Px3.p2.2),[footnote 1](https://arxiv.org/html/2601.22513v2#footnote1). -
Semi-supervised learning by entropy minimization.
Advances in neural information processing systems 17.
Cited by:
[Appendix A](https://arxiv.org/html/2601.22513v2#A1.p2.2). -
A survey on llm-as-a-judge.
arXiv preprint arXiv:2411.15594.
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p2.1). -
Distilling the knowledge in a neural network.
arXiv preprint arXiv:1503.02531.
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p4.1). -
Self-improvement in language models: the sharpening mechanism.
In The Thirteenth International Conference on Learning Representations,
Cited by:
[§C.3](https://arxiv.org/html/2601.22513v2#A3.SS3.SSS0.Px3.p4.6),[§C.4](https://arxiv.org/html/2601.22513v2#A3.SS4.SSS0.Px2.p7.1),[§C.5](https://arxiv.org/html/2601.22513v2#A3.SS5.SSS0.Px1.p2.1),[Appendix C](https://arxiv.org/html/2601.22513v2#A3.p1.1),[§1](https://arxiv.org/html/2601.22513v2#S1.p1.1),[§2](https://arxiv.org/html/2601.22513v2#S2.p4.1),[§3](https://arxiv.org/html/2601.22513v2#S3.SS0.SSS0.Px2.p1.3),[§3](https://arxiv.org/html/2601.22513v2#S3.SS0.SSS0.Px2.p2.1),[§3](https://arxiv.org/html/2601.22513v2#S3.SS0.SSS0.Px3.p2.2),[§5](https://arxiv.org/html/2601.22513v2#S5.p3.3),[footnote 1](https://arxiv.org/html/2601.22513v2#footnote1). -
Large language models can self-improve.
arXiv preprint arXiv:2210.11610.
Cited by:
[§1](https://arxiv.org/html/2601.22513v2#S1.p1.1). -
Scaling laws for learning with real and surrogate data.
In The Thirty-eighth Annual Conference on Neural Information Processing Systems,
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p4.1). -
Deep learning with logged bandit feedback.
In International Conference on Learning Representations,
Cited by:
[Appendix A](https://arxiv.org/html/2601.22513v2#A1.p4.1). -
Crafting papers on machine learning.
In Proceedings of the 17th International Conference
on Machine Learning (ICML 2000), P. Langley (Ed.),
Stanford, CA, pp. 1207–1216.
Cited by:
[Appendix G](https://arxiv.org/html/2601.22513v2#A7.SS0.SSS0.Px1.p5.1). -
Pseudo-label: the simple and efficient semi-supervised learning method for deep neural networks.
In Workshop on challenges in representation learning, ICML,
Vol. 3, pp. 896.
Cited by:
[Appendix A](https://arxiv.org/html/2601.22513v2#A1.p2.2). -
Self-rewarding vision-language model via reasoning decomposition.
arXiv preprint arXiv:2508.19652.
Cited by:
[§1](https://arxiv.org/html/2601.22513v2#S1.p2.1),[§2](https://arxiv.org/html/2601.22513v2#S2.p3.1). -
Heat death of generative models in closed-loop learning.
arXiv preprint arXiv:2404.02325.
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p4.1). -
Self-distillation amplifies regularization in hilbert space.
Advances in Neural Information Processing Systems 33, pp. 3351–3361.
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p4.1). -
Training language models to follow instructions with human feedback.
Advances in neural information processing systems 35, pp. 27730–27744.
Cited by:
[§1](https://arxiv.org/html/2601.22513v2#S1.p1.1). -
Understanding the gains from repeated self-distillation.
Advances in Neural Information Processing Systems 37, pp. 7759–7796.
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p4.1). -
Self-consistency preference optimization.
In Forty-second International Conference on Machine Learning,
Cited by:
[§1](https://arxiv.org/html/2601.22513v2#S1.p2.1),[§2](https://arxiv.org/html/2601.22513v2#S2.p3.1). -
Direct preference optimization: your language model is secretly a reward model.
Advances in neural information processing systems 36, pp. 53728–53741.
Cited by:
[§1](https://arxiv.org/html/2601.22513v2#S1.p1.1),[§3](https://arxiv.org/html/2601.22513v2#S3.SS0.SSS0.Px3.p2.2). -
Large language models encode semantics in low-dimensional linear subspaces.
arXiv preprint arXiv:2507.09709.
Cited by:
[Remark 6.5](https://arxiv.org/html/2601.22513v2#S6.Thmtheorem5.p1.11). -
Understanding machine learning: from theory to algorithms.
Cambridge university press.
Cited by:
[§5](https://arxiv.org/html/2601.22513v2#S5.p2.1). -
AI models collapse when trained on recursively generated data.
Nature 631 (8022), pp. 755–759.
Cited by:
[§1](https://arxiv.org/html/2601.22513v2#S1.p3.1),[§2](https://arxiv.org/html/2601.22513v2#S2.p4.1),[§4](https://arxiv.org/html/2601.22513v2#S4.p2.4). -
Non-asymptotic gap-dependent regret bounds for tabular mdps.
Advances in Neural Information Processing Systems 32.
Cited by:
[§5](https://arxiv.org/html/2601.22513v2#S5.p3.3). -
Fixmatch: simplifying semi-supervised learning with consistency and confidence.
Advances in neural information processing systems 33, pp. 596–608.
Cited by:
[Appendix A](https://arxiv.org/html/2601.22513v2#A1.p2.2). -
Rate of model collapse in recursive training.
arXiv preprint arXiv:2412.17646.
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p4.1). -
Batch learning from logged bandit feedback through counterfactual risk minimization.
The Journal of Machine Learning Research 16 (1), pp. 1731–1755.
Cited by:
[Appendix A](https://arxiv.org/html/2601.22513v2#A1.p4.1). -
The nature of statistical learning theory.
Springer.
Cited by:
[§5](https://arxiv.org/html/2601.22513v2#S5.p2.1). -
The best of both worlds: reinforcement learning with logarithmic regret and policy switches.
arXiv preprint arXiv:2203.01491.
Cited by:
[§5](https://arxiv.org/html/2601.22513v2#S5.p3.3). -
CREAM: consistency regularized self-rewarding language models.
In The Thirteenth International Conference on Learning Representations,
Cited by:
[§1](https://arxiv.org/html/2601.22513v2#S1.p2.1),[§2](https://arxiv.org/html/2601.22513v2#S2.p3.1),[§3](https://arxiv.org/html/2601.22513v2#S3.p1.1). -
Self-preference bias in llm-as-a-judge.
In Neurips Safe Generative AI Workshop 2024,
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p2.1). -
Meta-rewarding language models: self-improving alignment with llm-as-a-meta-judge.
arXiv preprint arXiv:2407.19594.
Cited by:
[§1](https://arxiv.org/html/2601.22513v2#S1.p2.1). -
The role of coverage in online reinforcement learning.
In The Eleventh International Conference on Learning Representations,
Cited by:
[footnote 1](https://arxiv.org/html/2601.22513v2#footnote1). -
Self-rewarding correction for mathematical reasoning.
arXiv preprint arXiv:2502.19613.
Cited by:
[§1](https://arxiv.org/html/2601.22513v2#S1.p2.1),[§2](https://arxiv.org/html/2601.22513v2#S2.p2.1),[3rd item](https://arxiv.org/html/2601.22513v2#S5.I2.i3.p1.3),[Remark 5.8](https://arxiv.org/html/2601.22513v2#S5.Thmtheorem8.p2.2). -
PACR: progressively ascending confidence reward for llm reasoning.
arXiv preprint arXiv:2510.22255.
Cited by:
[§3](https://arxiv.org/html/2601.22513v2#S3.SS0.SSS0.Px2.p1.3). -
Self-rewarding language models.
In Forty-first International Conference on Machine Learning,
Cited by:
[§1](https://arxiv.org/html/2601.22513v2#S1.p2.1),[§2](https://arxiv.org/html/2601.22513v2#S2.p2.1),[§3](https://arxiv.org/html/2601.22513v2#S3.p1.1),[3rd item](https://arxiv.org/html/2601.22513v2#S5.I2.i3.p1.3),[Remark 5.8](https://arxiv.org/html/2601.22513v2#S5.Thmtheorem8.p2.2). -
Self-rewarding ppo: aligning large language models with demonstrations only.
arXiv preprint arXiv:2510.21090.
Cited by:
[§3](https://arxiv.org/html/2601.22513v2#S3.SS0.SSS0.Px2.p1.3). -
Right question is already half the answer: fully unsupervised llm reasoning incentivization.
arXiv preprint arXiv:2504.05812.
Cited by:
[§3](https://arxiv.org/html/2601.22513v2#S3.SS0.SSS0.Px2.p1.3). -
What and how does in-context learning learn? bayesian model averaging, parameterization, and generalization.
arXiv preprint arXiv:2305.19420.
Cited by:
[§5](https://arxiv.org/html/2601.22513v2#S5.p3.3). -
Learning to reason without external rewards.
arXiv preprint arXiv:2505.19590.
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p2.1). -
Judging llm-as-a-judge with mt-bench and chatbot arena.
Advances in neural information processing systems 36, pp. 46595–46623.
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p2.1). -
Self-consistency of the internal reward models improves self-rewarding language models.
arXiv preprint arXiv:2502.08922.
Cited by:
[§2](https://arxiv.org/html/2601.22513v2#S2.p3.1),[3rd item](https://arxiv.org/html/2601.22513v2#S5.I2.i3.p1.3),[Remark 5.8](https://arxiv.org/html/2601.22513v2#S5.Thmtheorem8.p2.2). -
Calibrated self-rewarding vision language models.
Advances in Neural Information Processing Systems 37, pp. 51503–51531.
Cited by:
[§1](https://arxiv.org/html/2601.22513v2#S1.p2.1),[§2](https://arxiv.org/html/2601.22513v2#S2.p3.1).
Appendix
Overview
In this supplementary material, we provide additional details and complete proofs to support the theoretical developments presented in the main paper. The appendix is organized as follows:
-
•
Appendix
[A](https://arxiv.org/html/2601.22513v2#A1). Additional Related Work. We discuss connections to classical pseudo-labelling in semi-supervised learning and off-policy batch learning from logged data. We clarify the conceptual distinctions of our framework, emphasizing the non-stationary, endogenous nature of the self-rewarding data generation process. -
•
Appendix
[B](https://arxiv.org/html/2601.22513v2#A2). Limitation. We acknowledge the technical challenges in extending our rigorous guarantees from linear models to full Transformer architectures. We discuss the complexities introduced by non-linear dynamics and non-convex optimization landscapes, highlighting this extension as a critical direction for future research. -
•
Appendix
[C](https://arxiv.org/html/2601.22513v2#A3). Proof of Theorem[5.3](https://arxiv.org/html/2601.22513v2#S5.Thmtheorem3): Finite-Sample Guarantees for Iterative Alignment. We provide the complete mathematical proof for the finite-sample guarantee of the iterative self-rewarding process. This section details how the influence of the initial model decays exponentially by recursively controlling the policy condition number. -
•
Appendix
[D](https://arxiv.org/html/2601.22513v2#A4). Proof of Theorem[4.1](https://arxiv.org/html/2601.22513v2#S4.Thmtheorem1): Lower Bound on Single-Step Failure Rate. We establish the proof for the failure rate lower bound of a single-step update. This is achieved by constructing a hard problem instance to reveal the inherent limitations of a single update step, especially when the initial model is of poor quality. - •
-
•
Appendix
[F](https://arxiv.org/html/2601.22513v2#A6). Proof of Theorem[6.2](https://arxiv.org/html/2601.22513v2#S6.Thmtheorem2): Performance Guarantees for Linear Softmax Models. We extend the general theoretical framework to the continuous, parametric case of linear softmax models. This section details how covering numbers are used to derive performance guarantees for this specific model class. -
•
Appendix
[G](https://arxiv.org/html/2601.22513v2#A7). Proof of Corollary[6.4](https://arxiv.org/html/2601.22513v2#S6.Thmtheorem4): Data-Dependent Bounds via Effective Dimension. We refine the performance bounds for parametric models by introducing the concept of effective dimension, which is based on the spectral structure of the feature covariance. This allows the bound to depend on the intrinsic data complexity rather than the ambient dimension.
This appendix provides the full mathematical foundations of our results and demonstrates their applicability to modern high-capacity models used in practice.
Appendix A Additional Related Work
In this section, we discuss additional lines of work related to classical pseudo-labelling and off-policy batch learning, with the goal of further clarifying the conceptual position of our framework within the broader literature.
Classical Pseudo-Labelling in Semi-Supervised Learning. Our work shares connections with classical pseudo-labelling methods in semi-supervised learning (SSL), where a model trained on labeled data predicts discrete pseudo-labels for unlabeled examples and is subsequently retrained on the combined dataset (Grandvalet and Bengio, [2004](https://arxiv.org/html/2601.22513v2#bib.bib9); Lee and others, [2013](https://arxiv.org/html/2601.22513v2#bib.bib721)). Modern approaches integrate pseudo-labelling with entropy minimization, consistency regularization, and strong augmentation strategies, yielding methods such as MixMatch, ReMixMatch, and FixMatch (Berthelot et al., [2019b](https://arxiv.org/html/2601.22513v2#bib.bib722), [a](https://arxiv.org/html/2601.22513v2#bib.bib723); Sohn et al., [2020](https://arxiv.org/html/2601.22513v2#bib.bib724)). Beyond these algorithmic developments, recent work (Aminian et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib725)) has proposed divergence-based and information-theoretic formulations of self-training. For instance, some studies design empirical risk functions and regularizers based on -divergences and -Rényi divergences to make pseudo-labelling more robust to noisy pseudo-labels, thereby placing classical self-training on a divergence-regularization footing. Other work (Aminian et al., [2022a](https://arxiv.org/html/2601.22513v2#bib.bib726)) provides an information-theoretic framework for self-training under covariate shift, recovering pseudo-labelling and entropy minimization as special cases.
While conceptually related in leveraging model-generated supervision, our SRLM framework diverges significantly from classical SSL. SSL approaches typically assume a semi-supervised setting with a static pool of unlabeled inputs and a fixed pseudo-labelling mechanism that outputs (possibly softened) class labels. In contrast, SRLMs operate in an off-policy sequential decision-making setting. Here, the data distribution is inherently non-stationary due to the evolving policy ; the supervisory signals are continuous self-rewards derived from model log-likelihoods; and the policy and reward mechanism co-evolve, forming a coupled dynamical system rather than a unidirectional teacher–student update.
Pseudo-Reward and Off-Policy Batch Learning from Logged Data. Learning from logged interaction data is extensively studied in contextual bandits and offline reinforcement learning. Counterfactual Risk Minimization (CRM) formulates batch learning from logged feedback via propensity-weighted empirical risk minimization (Swaminathan and Joachims, [2015](https://arxiv.org/html/2601.22513v2#bib.bib727); Joachims et al., [2018](https://arxiv.org/html/2601.22513v2#bib.bib731)). In addition, (Aminian et al., [2022b](https://arxiv.org/html/2601.22513v2#bib.bib728)) consider semi-supervised batch learning from logged data, where only a subset of samples contains feedback, and provide upper bounds that motivate divergence-based regularization terms between the target and logging policies. More recently, other work has proposed log-sum-exponential (LSE) estimators for off-policy evaluation and learning from logged bandit feedback, aiming to improve robustness and reinforcing the regularization-centric perspective (Behnamnia et al., [2024](https://arxiv.org/html/2601.22513v2#bib.bib730), [2025](https://arxiv.org/html/2601.22513v2#bib.bib729)).
Our SRLM framework shares conceptual alignment with this line of work, as we also optimize a policy under explicit regularization with respect to a reference (or logging) policy. However, a critical distinction arises from the data-generation process. The aforementioned logged-data methods assume a fixed logging policy and operate on a static historical dataset. In contrast, SRLMs iteratively generate new trajectories, meaning the effective logging policy co-evolves with , producing a non-stationary and endogenous data distribution. Consequently, since our analysis focuses on bootstrapping from weak initialization and stabilizing the evolving interaction between policy and reward, it lies outside the static batch-learning assumptions underlying CRM, semi-supervised logged-data methods, and LSE-based estimators.
Appendix B Limitation
We acknowledge the significant challenge of extending the rigorous guarantees established in this work to full, modern Transformer architectures. The intricate components of these models, such as multi-head attention and deep residual connections, introduce complex non-linear dynamics and high-dimensional, non-convex optimization landscapes that are not captured by our current linear setting. Establishing a complete theoretical framework, such as a benign overfitting theorem or a proof of stable convergence, for such systems remains a major open problem in the theoretical deep learning community. At present, rigorous theories are largely confined to more tractable settings, primarily linear models (as adopted in our analysis) or two-layer neural networks. Therefore, bridging this substantial gap by extending the analytical framework to full-scale Transformers constitutes a highly valuable and essential direction for future research.
Appendix C Proof of Theorem [5.3](https://arxiv.org/html/2601.22513v2#S5.Thmtheorem3): Finite-Sample Guarantee for Iterative Self-Rewarding Alignment
This section provides the complete and rigorous proof for Theorem [5.3](https://arxiv.org/html/2601.22513v2#S5.Thmtheorem3), our main result establishing finite-sample guarantees for the iterative self-rewarding alignment process. The proof is structured to first analyze the performance bounds of a single update step. We then construct a recursive argument that tracks the evolution of the policy condition number, , across successive iterations. By showing that this parameter is controlled and converges, we formally demonstrate that the influence of the initial model’s quality decays exponentially, thus ensuring the stability and statistical efficiency of the iterative alignment framework. Our analysis draws inspiration from the theoretical self-improvement framework introduced in (Huang et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib657)), but extends it to the more complex iterative self-rewarding paradigm.
Proof.
We begin by formalizing the notation and assumptions underlying the proof. We then establish a foundational lemma that connects the probability of a model being suboptimal to its performance gap relative to an optimal comparator.
Notation and Assumptions.
For each , assume there exists a maximizer
and that for all . We define the deterministic comparator model as
The performance of any model is measured by the functional
In addition, we recall the margin parameter , which quantifies the minimum log-probability gap between the optimal action and any suboptimal action:
The assumption of uniqueness ensures .
C.1 From Performance Gap to Suboptimality Probability.
The central step is to upper bound the probability that the model assigns insufficient probability mass to the unique maximizer . The following lemma formalizes this connection.
Lemma C.1.
For any model and any , the probability of assigning insufficient mass to the optimal action satisfies
| (8) |
Proof of Lemma [C.1](https://arxiv.org/html/2601.22513v2#A3.Thmtheorem1).
The proof proceeds in two steps.
Step 1: Bounding the probability by an expectation. For any and , the indicator inequality
holds. Applying this with and averaging over gives
| (9) |
Step 2: Relating the expectation to the performance gap. By the definition of , for any and ,
Taking expectations with and , and noting that almost surely under , we obtain
Thus,
| (10) |
C.2 A Reward Identity and the Performance Gap Decomposition
To derive a tractable bound for the performance gap , we begin by introducing key notation and establishing a fundamental reward identity. This identity enables us to decompose the performance gap into components that can be bounded using statistical learning arguments.
Shorthand Notation and a Baseline-Cancellation Identity.
For any policy , we introduce the following notation for expectations:
Conditioned on , the random draws and are independent.
For any measurable function , we define the pairwise difference operator:
This leads to the following fundamental baseline-cancellation identity:
| (11) |
This identity is repeatedly used in our analysis to simplify expressions and eliminate baseline terms.
A Reward Identity via Entropy Regularization.
We now derive a pointwise representation for the reward function . Consider the entropy-regularized optimization problem for a fixed :
The unique optimizer is known to have the Gibbs form:
| (12) |
Dividing Eq. [12](https://arxiv.org/html/2601.22513v2#A3.E12) by , taking logarithms,
and multiplying by yields
Rearranging provides the identity
| (13) |
The term depends only on , and therefore cancels out in any pairwise difference. Specifically,
| (14) |
Thus, the pairwise differences of the original reward are equivalent to those of the transformed reward , which resembles the DPO reward but with replaced by .
Decomposition of the Performance Gap.
With the reward identity Eq. [13](https://arxiv.org/html/2601.22513v2#A3.E13) and the
baseline-cancellation identity Eq. [11](https://arxiv.org/html/2601.22513v2#A3.E11), we now
decompose the performance gap.
Recall that is the optimizer of the DPO objective:
This optimality condition implies that for any comparator ,
We begin by inserting and subtracting terms into the definition of the performance gap:
Applying the DPO optimality condition to the first term yields
| (15) |
We next apply the baseline-cancellation identity
Eq. [11](https://arxiv.org/html/2601.22513v2#A3.E11) to refine the two expectation terms.
For the first term:
| (16) |
Similarly, for the second term:
| (17) |
Substituting Eq. [16](https://arxiv.org/html/2601.22513v2#A3.E16) and Eq. [17](https://arxiv.org/html/2601.22513v2#A3.E17) into
Eq. [15](https://arxiv.org/html/2601.22513v2#A3.E15) and observing that the baseline terms cancel exactly,
we obtain the final decomposition:
| (18) |
This decomposition forms the foundation for subsequent statistical analysis of the performance gap.
C.3 Bounding the Difference of Reward Deltas via Region Decomposition
In this section we control the two principal terms in the performance
bound Eq. [18](https://arxiv.org/html/2601.22513v2#A3.E18), namely
and .
Our strategy is to decompose the expectation of the absolute difference
into contributions from a
good region, where the pairwise reward differences are uniformly
bounded, and a complementary bad region, which captures rare tail
events.
Preliminaries.
We recall the coupled–expectation shorthand
and the pairwise differences of interest:
| (19) | ||||
| (20) |
We also use the standard concentrability coefficient of a policy with respect to the baseline :
Good/Bad region decomposition.
Fix a threshold , and define
Let . Then
| (21) |
We now bound the two contributions on the right-hand side.
Lemma C.2 (Change of measure with concentrability).
For any nonnegative measurable function , the coupled expectation under satisfies
| (22) |
Proof.
We expand the coupled expectation explicitly:
Reweighting the distribution of from to introduces the ratio
Hence
Applying the Cauchy–Schwarz inequality on the joint law gives
Bounding the bad–region term.
We now derive a usable bound on the bad–region contribution.
Starting from Lemma [C.2](https://arxiv.org/html/2601.22513v2#A3.Thmtheorem2) and choosing the test function
, we immediately obtain
| (23) |
Thus the task reduces to bounding the second moment of restricted to the bad region.
To proceed, we invoke Hölder’s inequality (equivalently, a second application of Cauchy–Schwarz), which separates the event probability from the higher–order moment:
| (24) |
Here the first factor controls the likelihood of landing in the bad region, while the second factor controls the size of the reward differences when such events occur.
The probability of the bad region itself can be bounded via a simple union bound. Since is the event that either or exceeds the threshold , we have
| (25) |
It remains to bound the fourth moment of . By the elementary inequality , we obtain
| (26) |
Finally, by combining Eq. [23](https://arxiv.org/html/2601.22513v2#A3.E23)–Eq. [26](https://arxiv.org/html/2601.22513v2#A3.E26) and invoking the standard fourth-moment bound provided in Lemma J.2 of (Huang et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib657)), we obtain the following compact estimate.
| (27) |
where
In words, the bad–region contribution is controlled by three factors: the concentrability of the comparator policy , a logarithmic moment term stemming from higher–order tail bounds, and the tail probability , raised to the quarter power.
Bounding the good–region term.
Applying Lemma [C.2](https://arxiv.org/html/2601.22513v2#A3.Thmtheorem2) with
gives
| (28) |
Note that on both and are clipped by , so the remaining quantity is a bounded squared error that will be controlled by an empirical process argument.
Putting the pieces together.
From Eq. [21](https://arxiv.org/html/2601.22513v2#A3.E21), Eq. [27](https://arxiv.org/html/2601.22513v2#A3.E27), and
Eq. [28](https://arxiv.org/html/2601.22513v2#A3.E28), we obtain
| (29) |
By the same argument with in place of ,
| (30) |
Finally, using and substituting
Eq. [29](https://arxiv.org/html/2601.22513v2#A3.E29)–Eq. [30](https://arxiv.org/html/2601.22513v2#A3.E30) into
Eq. [18](https://arxiv.org/html/2601.22513v2#A3.E18), we obtain the intermediate performance–gap bound
| (31) |
The first (“good–region”) term will be bounded by a uniform convergence argument, while the tail term is controlled by choosing and the clipping level in the empirical loss appropriately. This completes the good/bad region analysis used to bound the differences of reward deltas.
C.4 From Empirical Risk Minimization to a Population-Level Bound
The bound derived in Eq. [C.3](https://arxiv.org/html/2601.22513v2#A3.Ex54) depends on the population-level squared difference
.
In this section, we establish a connection between this population quantity and the empirical
performance of the learned policy , which is obtained through Empirical Risk Minimization (ERM).
To achieve this, we leverage classical tools from uniform convergence theory, which allow us to
translate the ERM guarantee into a high-probability control of the population-level error term.
The ERM Solution and Its Empirical Loss.
To simplify notation, we index the pairwise difference operator by a policy :
From the reward identity in Eq. [13](https://arxiv.org/html/2601.22513v2#A3.E13), we note that
.
The policy is defined as the ERM solution over the class , minimizing
the squared loss with respect to the oracle .
Since the oracle belongs to the hypothesis class, ,
the empirical risk of must be no larger than that of , which is zero.
Formally,
| (32) |
A Uniform Convergence Bound via Bernstein’s Inequality.
To generalize the zero empirical loss to the population setting, we appeal to Bernstein’s inequality together with a union bound over the policy class. Let be i.i.d. samples with and .
To apply concentration inequalities, we require bounded variables. For any policy , we define the clipped squared loss
where the clipping threshold will be chosen later. The empirical and population losses are then
On the clipping event, both differences are bounded by , hence . Thus the clipped loss is uniformly bounded as
| (33) |
Because and by construction
,
the ERM property Eq. [32](https://arxiv.org/html/2601.22513v2#A3.E32) implies
Since the clipped loss is always nonnegative, it follows that
| (34) |
For any fixed , the variables are i.i.d. and
bounded in by Eq. [33](https://arxiv.org/html/2601.22513v2#A3.E33).
Bernstein’s inequality then yields, for all ,
Using the variance bound , a standard fixed–point calculation leads to the empirical Bernstein form: with probability at least ,
| (35) |
for a universal constant .
Applying Eq. [114](https://arxiv.org/html/2601.22513v2#A6.E114) with and union–bounding over
all , we obtain that with probability at least ,
| (36) |
Since Eq. [36](https://arxiv.org/html/2601.22513v2#A3.E36) holds uniformly over ,
it applies in particular to the ERM policy .
Combining with Eq. [34](https://arxiv.org/html/2601.22513v2#A3.E34) yields
Substituting gives the population-level bound
| (37) |
Finally, we specify the clipping level
This selection is motivated by the tail-probability bound provided in Lemma J.1 of (Huang et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib657)).
which ensures that the probability of clipping violations is sufficiently small,
of order at most .
With this selection, we conclude that
| (38) |
This completes the transition from the empirical ERM guarantee to a high-probability population-level error bound.
C.5 Finalizing the Performance Gap and Deriving the Suboptimality Bound
In this concluding part of the single-step analysis, we integrate the statistical error bound derived in the previous section with the main performance gap inequality. This synthesis yields a concrete, high-probability guarantee on the policy’s performance, which we then translate into a bound on the probability mass that the policy assigns to the optimal actions.
Simplifying the Performance Gap Bound.
We begin by substituting the statistical error term from Eq. [38](https://arxiv.org/html/2601.22513v2#A3.E38) into the performance gap inequality Eq. [C.3](https://arxiv.org/html/2601.22513v2#A3.Ex54). This yields
| (39) |
To simplify this expression, we upper bound the policy-dependent coefficients with problem-level constants. Specifically, by Lemma 4.1 in (Huang et al., [2025](https://arxiv.org/html/2601.22513v2#bib.bib657)), we have
Moreover, we control the KL divergence by the logarithm of the concentrability coefficient:
Substituting these bounds gives
For clarity, and because is typically of the same order as in single-step analysis, we further simplify to
To obtain a cleaner form, we balance the statistical error term and the tail-event term by setting
This ensures that the second term does not dominate the first. The inequality then reduces to
| (40) |
Bounding the Suboptimality Probability.
We now translate this bound into a high-probability guarantee on the probability mass assigned to optimal actions. Substituting the above inequality into Lemma [C.1](https://arxiv.org/html/2601.22513v2#A3.Thmtheorem1) (see also Eq. [8](https://arxiv.org/html/2601.22513v2#A3.E8)), we obtain
| (41) |
Recalling that the statistical error satisfies
we conclude
| (42) |
This provides a direct guarantee on the frequency with which the learned policy under-weights the oracle’s optimal action.
Extending the Bound to the Policy’s Own Optimal Action.
For practical purposes, it is natural to bound the event in which the learned policy’s own maximizer receives insufficient probability mass. Define
By construction,
Hence, whenever the event occurs, it must also be the case that . In set-theoretic form,
Taking probabilities and applying Eq. [42](https://arxiv.org/html/2601.22513v2#A3.E42) yields
| (43) |
This completes the one-step analysis. The derived inequality provides a high-probability guarantee that the learned policy assigns sufficient mass to its own optimal actions, with explicit dependence on the sample size , the policy class size , and the policy condition number .
C.6 Recursive Bound for the Policy Condition Number
The analysis so far has provided a crucial single-step guarantee on the policy’s suboptimality. However, to understand the long-term behavior of the self-rewarding process, it is essential to move beyond a single iteration and demonstrate that the policy’s quality, as measured by the policy condition number, does not degrade over successive generations of training. An uncontrolled growth in the policy condition number would signify model collapse, where the model becomes increasingly narrow and overconfident in its own outputs, thereby losing its ability to generalize. The central argument of our framework rests on proving that the policy condition number at one step is controlled by, and does not grow excessively relative to, that of the previous step. This stability property is formalized in the following lemma.
Lemma C.3 (One-Step Policy Condition Number Recurrence).
Let denote the policy condition number at step . Assume that for any policy , the probabilities assigned to any action are uniformly lower-bounded by a constant . Then, the policy condition number at step , denoted , satisfies the recursive inequality
| (44) |
Proof.
We illustrate the argument for the inductive step from to ; the general case follows by re-indexing.
C.6.1 Tail-integral representation.
We recall that the policy condition number is defined as
| (45) |
where
Introducing the random variable
we see that . A useful way to analyze such expectations is through the tail-integral (or layer-cake) representation:
| (46) |
By assumption, the policy assigns at least probability to every action, i.e. for all . Consequently, is bounded:
This bounded support implies the following trivial bounds on the tail probability:
Substituting these observations into Eq. [123](https://arxiv.org/html/2601.22513v2#A6.E123), we split the expectation into three parts:
| (47) |
Thus, the analysis of reduces to bounding the integral of the non-trivial tail probabilities over the interval .
C.6.2 Relating the tail to suboptimality.
For , the event is equivalent to
Writing , this becomes . From Eq. [43](https://arxiv.org/html/2601.22513v2#A3.E43), we know
| (48) |
Substituting gives
| (49) |
Let
Then
| (50) |
To respect probability upper bounds, we refine this as
| (51) |
C.6.3 Derivation of an Integral Bound on the Policy Condition Number
Then, We provide a complete and self–contained derivation of the integral that upper–bounds the one–step policy condition number . As shown earlier, defining and using the tail–integral identity yields
| (52) |
where is the uniform lower bound on action probabilities and is the parameter that emerges from the suboptimality bound (its explicit form is given in the main text; here we only use that ). The remainder of the argument is a careful evaluation of the integral in Eq. [52](https://arxiv.org/html/2601.22513v2#A3.E52).
Step 1: Identifying the transition point.
The integrand switches behavior at the unique solving . Solving
we obtain the explicit transition point
| (53) |
which is well defined under the nontrivial regime . For we have and hence , while for we have and hence .
Step 2: Decomposing the integral.
Using the transition point Eq. [130](https://arxiv.org/html/2601.22513v2#A6.E130), we split
| (54) |
The first term evaluates immediately to . It remains to compute the second term.
Step 3: Evaluating the second term via an antiderivative.
We simplify the integrand by the identity , and integrate term–wise:
Therefore,
where we used and the fact that ensures .
Step 4: Assembling the bound and simplifying.
Combining the pieces from Eq. [54](https://arxiv.org/html/2601.22513v2#A3.E54), we obtain
| (55) |
We now substitute from Eq. [130](https://arxiv.org/html/2601.22513v2#A6.E130). First, the linear term simplifies to
Second, . Using these identities in Eq. [55](https://arxiv.org/html/2601.22513v2#A3.E55) yields
We have thus established the explicit integral evaluation:
| (56) |
Interpretation and a relaxed form. For small (the regime of interest), and the contribution of dominates. A convenient relaxation is then
which is often more transparent in subsequent recursive arguments. (The exact definition of —a function of and —is given in the main text and can be substituted as needed.)
Step 5: Final Substitution and the Recursive Relation
We now return to the simplified linearized bound obtained in the previous section and explicitly substitute the full definition of the constant . Recall that was defined in terms of the statistical error and the KL regularization component, yielding
Substituting this expression back into the approximate linear coverage bound, we obtain
| (57) |
Expanding the terms inside the brackets distributes the dependence on the statistical complexity and the KL penalty, leading to a more transparent form of the recursion:
| (58) |
This recursive inequality explicitly highlights the threefold structure of the coverage update: (i) a constant offset due to the minimal probability assumption, (ii) a term scaling with , which reflects the statistical complexity inherited from the previous step, and (iii) a logarithmic dependence on introduced by the KL penalty.
Step 6: Extension to Arbitrary Generation Steps by Induction
The derivation so far has been presented for the transition from the base step () to the first update (). However, the underlying reasoning does not rely on any special property of these indices. At a conceptual level, the argument merely exploits two facts: (i) the tail–integral identity applies uniformly at each step, and (ii) the suboptimality bound remains valid for every policy with coverage coefficient .
Consequently, the same sequence of inequalities can be applied recursively at each generation step. By induction, the bound that relates to extends to a general recurrence relation between and for all . Formally, we obtain
| (59) |
Interpretation.
This recurrence constitutes a stability guarantee for the policy condition number.
It demonstrates that each new generation of the policy inherits its complexity from the previous generation in a controlled manner: the square–root scaling prevents explosive growth, while the logarithmic correction encapsulates the effect of KL regularization.
Therefore, the recursive inequality Eq. [59](https://arxiv.org/html/2601.22513v2#A3.E59) forms the theoretical backbone ensuring that the policy condition number does not diverge across iterations, thereby precluding collapse and preserving generalization capacity throughout the self-rewarding process.
∎
C.7 Asymptotic Stability of the Policy Condition Number
Lemma C.4 (Asymptotic Stability of the Policy Condition Number).
Let the sequence of policy condition numbers be governed by the recursive inequality derived in Eq. [59](https://arxiv.org/html/2601.22513v2#A3.E59). Then, for a sufficiently small learning rate parameter (specifically, ), the policy condition number at generation remains bounded. Moreover, the sequence converges exponentially fast to a finite stable value, ensuring the stability of the self-rewarding process. In particular, the explicit asymptotic bound satisfies
| (60) |
Proof.
We analyze the recurrence step by step, beginning with a reformulation and then studying its fixed point and rate of convergence.
Step 1: Compact Form of the Recurrence.
Let us define the shorthand
| (baseline constant) | (61) | |||||
| (square-root coefficient) | (62) | |||||
| (63) |
Then the recursive inequality in Eq. [59](https://arxiv.org/html/2601.22513v2#A3.E59) can be rewritten in the compact form
| (64) |
Step 2: Bounding the Logarithmic Term.
Since , we apply the inequality for all . Substituting into Eq. [64](https://arxiv.org/html/2601.22513v2#A3.E64) yields
| (65) |
Let , so that the recurrence simplifies to
| (66) |
This gives a cleaner functional recurrence governed by
Step 3: Fixed Point of the Recurrence.
The asymptotic behavior is determined by the fixed point of , which satisfies
| (67) |
Setting yields the quadratic equation
By the quadratic formula,
Since , we choose the positive solution. Hence,
| (68) |
Step 4: Convergence Rate via Contraction.
We now analyze the rate at which the recurrence converges to its fixed point . Recall that the recurrence is governed by
Since is monotone increasing and satisfies for all , the sequence , when initialized from , is monotonically decreasing and bounded below by . This ensures that converges to .
To quantify the convergence rate, we invoke the Mean Value Theorem. For any , there exists some such that
| (69) |
The derivative of is given by
Since is a decreasing function of , its supremum on the interval is attained at . Hence, the contraction factor is
| (70) |
Substituting the explicit expression of from Eq. [68](https://arxiv.org/html/2601.22513v2#A3.E68), we obtain
| (71) |
It is immediate that , which confirms that is a contraction mapping on . Consequently, the sequence converges geometrically to its fixed point .
Unrolling the recurrence, we arrive at the inequality
| (72) |
which provides an explicit bound on the deviation of from its fixed point . This establishes not only convergence but also the geometric rate of convergence governed by the contraction factor .
Step 5: Explicit Upper Bound for .
Since the original sequence is pointwise dominated by the auxiliary sequence , we may use the contraction analysis of Step 4 to bound . Because is monotonically decreasing from its initialization towards the fixed point , we have
Therefore, an explicit upper bound for the original policy condition number after generations is
| (73) |
where is the asymptotic fixed point defined in Eq. [68](https://arxiv.org/html/2601.22513v2#A3.E68), and is the geometric contraction factor derived in Eq. [71](https://arxiv.org/html/2601.22513v2#A3.E71).
This inequality shows that even if the initial coverage is large, the sequence converges exponentially fast towards a finite stable value . Thus the self-rewarding process is inherently stable and avoids uncontrolled growth of the policy condition number.
Expanding the bound more explicitly, we obtain
| (74) |
where we have substituted the closed-form expressions for and .
To further interpret this result, we approximate the asymptotic bound for large . Recalling that , and ignoring higher-order cross-terms, we obtain
| (75) |
Hence the recursive bound simplifies to
| (76) |
Equation Eq. [76](https://arxiv.org/html/2601.22513v2#A3.E76) makes explicit the decomposition of the bound:
the terms , , and determine the asymptotic ceiling, while the multiplicative factor ensures exponential decay of the dependence on the initial coverage .
This completes the derivation of the explicit upper bound for .
Step 6: Scaling Analysis.
Choosing balances the scaling of and , giving
and the contraction factor simplifies to
Hence,
| (77) |
This establishes both the boundedness and exponential convergence of the policy condition number sequence. ∎
C.8 Conclusion of the Proof: Bounding the Final Policy’s Tail Probability.
Having established in Lemma [C.4](https://arxiv.org/html/2601.22513v2#A3.Thmtheorem4) that the policy condition number is asymptotically stable and converges exponentially to a finite upper bound, we now translate this stability result into a final guarantee on the predictive confidence of the learned policy. Specifically, we seek to bound the probability that the policy assigns insufficient mass to its own optimal response after self-rewarding iterations.
From the preceding derivation, we have for any ,
| (78) |
The key step is to substitute the asymptotic bound for obtained in Eq. [77](https://arxiv.org/html/2601.22513v2#A3.E77) into this inequality. Recall that the policy condition number decomposes into a stable part, dominated by for large , and a transient part that decays exponentially with .
Step 1 (Square-root term). Applying the inequality to the decomposition of , we have
| (79) |
For sufficiently large , the second-order term is negligible compared to .
Step 2 (Logarithmic term). Since is bounded above by a finite constant , its logarithm is also bounded. That is,
With our choice of , the term is and therefore of the same asymptotic order as the square-root term.
Step 3 (Final substitution).
Plugging these bounds back into Eq. [78](https://arxiv.org/html/2601.22513v2#A3.E78), we obtain
| (80) |
Interpretation. The bound consists of two components:
-
•
A stable error term,
which vanishes at the parametric rate , demonstrating that the final policy becomes increasingly confident with more data.
-
•
A transient error term,
which reflects the dependence on the initial coverage but decays exponentially fast in .
Thus, even if the initial policy is weak (large ), its influence diminishes exponentially across iterations. The long-run behavior of the self-rewarding process is governed entirely by the stable error term, ensuring that the final policy allocates sufficient probability mass to its own optimal predictions.
The proof is complete.
∎
Appendix D Proof of Theorem [4.1](https://arxiv.org/html/2601.22513v2#S4.Thmtheorem1): Lower Bound on Single-Step Failure Rate.
Before proceeding to analyze the behavior of a full, multi-step iterative self-rewarding process, it is essential to first understand the fundamental limitations inherent in the mechanism itself. This section is dedicated to exploring these limits by analyzing the performance of a self-rewarding algorithm within a fixed query budget, . This scenario is equivalent to a single, non-iterative application of the process.
Our objective is to derive a lower bound on the failure rate that any algorithm must incur on some challenging problem instance. The proof proceeds via an adversarial approach: we will construct a class of problem instances designed to be maximally difficult, thereby probing for potential failure modes.
The central finding of this analysis will be that an algorithm’s success is critically dependent on the quality of the initial base model, as quantified by its policy condition number, . We will demonstrate that a large initial (representing a poor starting model) can lead to a high probability of failure, a scenario termed model collapse. This result is not a critique of a specific algorithm, but rather a revelation of an intrinsic risk. The vulnerability exposed in this section provides the primary motivation for the analysis in the subsequent sections, where we will investigate how an iterative framework can overcome this limitation and guide the process towards a stable and successful outcome.
Proof of Theorem [4.1](https://arxiv.org/html/2601.22513v2#S4.Thmtheorem1).
Our strategy is to establish a necessary condition on the sample size required for any algorithm to achieve a given success rate. Let an arbitrary algorithm, after making at most oracle calls, produce a new policy. We fix a target failure level . We will construct a specific hard problem instance and demonstrate that if the algorithm achieves an expected success rate of at least on this instance, then its sample budget must necessarily exceed a certain threshold.
By inverting this relationship, we establish the core result: for a fixed budget , there exists a worst-case scenario where the failure rate must be at least as large as the value dictated by this threshold. This provides the lower bound on the algorithm’s risk.
In this section we fix the query budget (the total number of sample-and-evaluate calls the algorithm may use), and we derive a lower bound on the failure rate that any algorithm must incur on some instance from . The proof proceeds in six explicit steps.
Step 1: Construction of a Hard Problem Instance.
To establish the lower bound, we construct a problem instance designed to be maximally challenging for any sharpening algorithm. The construction begins by defining the spaces for prompts and responses, followed by the strategic design of the data distribution and the model class itself.
Let the prompt space be a discrete set and the response space be . We fix a margin parameter (which we will later set to ) and an information-sparsity parameter .
First, we define a prompt distribution that concentrates most of its mass on a single, uninformative point:
| (81) |
where denotes the Dirac delta distribution on element . This construction serves a dual purpose. The atom at , carrying the majority of the probability mass (), acts as an uninformative sentinel; an algorithm will frequently sample prompts from this region but will learn nothing to distinguish between the candidate models. Conversely, all distinguishing information resides in the small -fraction of the distribution mass spread across the “informative” points . As will be shown later, this sparsity, controlled by , is instrumental in amplifying the overall failure rate from a more fundamental classification error.
Next, we construct a family of response distributions on , designed to be difficult to distinguish from one another. The distribution for the uninformative prompt is deterministic:
| (82) |
For the informative prompts, we define a set of nearly uniform distributions, each with a subtle bias towards a specific response:
| (83) |
For each , the distribution is constructed by taking the uniform distribution over elements and slightly increasing the probability mass of a single element , while uniformly decreasing the mass of all other elements. The parameter controls the margin by which is favored, making it the unique but only marginally most probable outcome. For instance, when , the probabilities are and for , highlighting that the distinguishing signal is subtle. This construction ensures that a large number of samples are required to reliably detect this statistical bias.
Finally, we synthesize these components to define the full model class. For any index vector , which serves as a hidden ”secret key,” we define the corresponding base model as:
| (84) |
The model class is then the set of all such models generated by every possible secret key:
| (85) |
Through this construction, the task is effectively reduced to a set of independent -way classification problems. Specifically, for each informative prompt , the algorithm’s goal is to identify the single hidden “correct” label , as is the unique maximizer under the response distribution . The overall difficulty of this task, and thus the reason this construction is suitable for proving a lower bound, is compounded by two strategically designed factors.
First, the statistical similarity of the candidate distributions makes the classification inherently challenging. The distribution is only slightly biased toward its maximizer , meaning a large number of samples at prompt are required to reliably detect this subtle statistical bump. With a limited sample budget, many of the hidden labels will therefore remain ambiguous to the algorithm. Second, an informational scarcity is enforced by the prompt distribution . The heavy probability mass concentrated at the uninformative prompt (a proportion of ) further dilutes the evidence available to the learner, as most samples drawn will provide no information about any of the hidden labels .
Together, these two effects—the need for many samples to resolve ambiguity at each informative prompt and the rarity of encountering such prompts—create the challenging family of models necessary to prove a tight lower bound on sample complexity.
Step 2: Tune via an Inlined Reduction-To-Classification Argument.
Fix an arbitrary algorithm and let be the model it outputs using at most samples. For a target failure level we set
(Here is part of the adversarially chosen prompt distribution from Step 1.) We now show that if the algorithm achieved overall success at least , then the average misclassification rate on the informative prompts must be at most .
Success event and its consequence at a fixed informative prompt. Recall from Step 1 that for each the maximizer set is a singleton, , where is the unique index of the favored label at . Define the success event at by
For let be the algorithm’s predicted label at . Because and on , the maximizer must coincide with the true index:
Equivalently, using indicator notation,
From overall success under to per-coordinate success. All probabilities and expectations below are taken over the internal randomness of the algorithm, the data it observes on instance , and over a uniformly random ; we abbreviate this by and . By definition of the prompt distribution ,
Assume the algorithm attained overall success at least , i.e. . Since , we get
Average misclassification bound at the informative prompts. Using the implication above at each ,
With our choice , the right-hand side equals . Therefore, if an algorithm with budget claimed overall success at least , then necessarily the average per-coordinate misclassification rate would not exceed . In Step 3 we will show, via a complementary counting argument on how many samples actually land on each informative prompt, that any budget smaller than a certain threshold forces a constant lower bound () on the left-hand side, whence a contradiction. This yields a necessary relation between and that we later invert to obtain the risk-form lower bound.
Step 3: Selecting to Ensure Compliance with the Policy Condition Number Constraint
We need to choose as a function of such that every model satisfies the policy condition number constraint . This constraint ensures that the model’s distribution covers the correct label with sufficient probability.
We begin by recalling the definition of the policy condition measure :
where is the probability that model assigns to the predicted label at input . The integral is taken with respect to the distribution over the inputs.
Next, we split this expectation into contributions from two parts: For , where always outputs , we have:
Thus, the contribution to the coverage from is simply , where is the mass allocated to in the prompt distribution. For each with , we assign a distribution that is a biased version of a uniform distribution. Specifically, we give the label a slightly higher probability compared to the other labels. The distribution is given by:
The mass assigned to label is higher, but the mass assigned to other labels is correspondingly lower.
Thus, the total contribution to the coverage constraint from all points is:
To satisfy the coverage constraint , we need to control the magnitude of the second term . To ensure this is bounded by a constant , we choose so that:
Solving for :
Substituting , we get
Finally, using the relationship , we obtain the desired form:
This choice of ensures that the coverage constraint is respected for all models .
Step 4: Derivation of the sample complexity bound.
To ensure that the algorithm has success at least , we need to check the sample complexity under which the per-coordinate misclassification probability remains sufficiently small. To do this, we proceed with the following steps:
(i) Markov’s Inequality for per-coordinate error. Let denote the total number of samples collected by the algorithm, where each sample is a triplet .
Let be the random variable representing the number of samples in the collected dataset of size for which the prompt is . According to the prompt distribution , the probability of any single sample being drawn for the prompt is . By the linearity of expectation, the expected value of is:
For the non-negative random variable , Markov’s inequality states that for any , . By setting , we can bound the probability that is large:
By considering the complementary event, we arrive at:
(ii) Lower bounding the per-coordinate classification error. We now derive a lower bound on the per-coordinate classification error, , by showing that a limited sample size creates unavoidable informational ambiguity.
Let be the dataset of samples. We define an event where the data is ambiguous for coordinate : this occurs if at least two responses for prompt were never sampled, and no sampled response for was the unique high-probability one. The total classification error is lower-bounded by the error conditioned on this event:
| (86) |
Conditioned on the data for which occurs, the posterior distribution over the unsampled labels for is uniform over a set of size at least two. Thus, any guess has a conditional error probability of at least . This allows us to simplify the bound:
| (87) |
To bound the probability of , we consider the likely scenario where the number of samples for prompt , denoted , is small. By Markov’s inequality, . We can therefore write:
| (88) |
The conditional probability of is at least the probability that none of the samples correspond to two specific, fixed responses (e.g., and another ), which occurs with probability at least for our construction with . On the event , this is bounded below by .
For a sufficiently small constant , this term is at least whenever the total sample size satisfies the condition . Combining these steps, we conclude that under this condition on :
| (89) |
This establishes a constant lower bound on the per-coordinate classification error when the sample size is insufficient.
(iv) Sample complexity lower bound. Now, combining all the steps, we conclude that the total number of samples needed to guarantee that the per-coordinate misclassification error is at least is related to as follows:
| (90) |
Thus, we obtain a necessary condition for the algorithm to achieve success at least : the sample complexity must be at least as large as .
Step 5: Eliminate in favor of and obtain a scalar inequality in .
Step 6: Invert the monotone constraint to get the risk-form lower bound.
Then, we derive the risk-form lower bound: for a fixed sample budget of samples, what is the minimum achievable failure rate ? This provides a more practical perspective on the intrinsic limitations of self-rewarding algorithms.
(i) Reformulating the lower Bound as a monotonic constraint
The established lower bound on the sample complexity is given by:
| (92) |
To facilitate the analysis, we consolidate the problem-dependent constants into a single term , and define a normalized quantity that represents the effective information per sample:
| (93) |
With these definitions, the lower bound inequality can be elegantly rewritten as a constraint on the failure rate :
| (94) |
We now define a function that captures the left-hand side of this inequality:
| (95) |
The function is strictly increasing for small (specifically for ), which is the regime of interest for non-trivial algorithms. This monotonicity ensures that for any given value of , the equation has a unique solution.
(ii) The Contrapositive as a Risk-Form Lower Bound
The logical contrapositive of the original theorem statement provides the foundation for our risk-form bound. The original theorem states that if an algorithm achieves a failure rate of at most , then its sample size must be large enough such that .
The contrapositive is: if an algorithm uses a sample size of at most , then it cannot guarantee a failure rate that violates this condition. Therefore, the minimum achievable failure rate for any algorithm using samples, which we denote as , is precisely the unique positive solution to the equation:
| (96) |
This leads to the risk-form lower bound: for any algorithm using at most samples, there exists a hard instance in such that its expected failure rate is at least .
| (97) |
The monotonicity of ensures that as the sample size increases, decreases, and consequently, the minimum failure rate also strictly decreases.
(iii) Explicit Solution via the Lambert W Function
To obtain a closed-form expression for , we solve the implicit equation :
| (98) |
Let us introduce a substitution , which implies . Substituting this back into the equation yields:
To isolate , we multiply both sides by to match the form :
By definition of the Lambert W function, where , we can solve for :
For the solution to be physically meaningful (, corresponding to ), we must choose the branch of the Lambert W function, denoted . Thus,
Finally, substituting back and , we obtain the exact, closed-form solution for the minimum failure rate:
| (99) |
(iv) Asymptotic Approximation for Large Sample Sizes
While exact, the Lambert W function form is not immediately intuitive. For the practical regime of large sample sizes (), the argument of , which is , approaches . We can use the well-known asymptotic expansion as . This yields a more interpretable approximation:
Substituting and simplifying the logarithmic term, we arrive at the convenient and explicit asymptotic lower bound:
| (100) |
Thus, we get:
| (101) |
This expression clearly shows that the failure rate decreases primarily as , modulated by a slower-growing logarithmic factor. It also explicitly shows how the problem difficulty, determined by coverage which we define as and model complexity , scales the error. Furthermore, we obtain
| (102) |
where hides logarithmic factors with respect to and .
∎
Appendix E Proof of Proposition [4.3](https://arxiv.org/html/2601.22513v2#S4.Thmtheorem3): From Low-Confidence Models to Greedy Decoding Failure.
We prove the proposition by construction. We explicitly design an autoregressive policy and a prompt such that the globally optimal sequence has a probability , while guaranteeing that the greedy decoding algorithm is diverted to a suboptimal sequence. The failure is engineered by creating a local-optima trap at the first decoding step, from which recovery of the true optimal sequence is impossible.
Step 1: Setup of the Adversarial Environment
Let be the target probability for the optimal sequence. Let the vocabulary be and the sequence length be . We define the unique optimal sequence as , where . We also introduce a distinct trap token where .
Step 2: Construction of the Adversarial Policy
We define the policy by specifying its conditional probabilities for each step . The construction ensures two properties: (i) is the unique optimal sequence with probability , and (ii) the greedy decoder deterministically selects the trap token at the first step.
Step 2.1: Inducing a Locally Optimal Trap at the First Step
We design the initial probability distribution to make the trap token appear more probable than the correct first token . Let be a small positive constant such that . The second condition, , ensures the total probability assigned to and does not exceed 1. We define:
The greedy decoder’s choice at step 1 is . Since , the decoder will select . Because the first token is incorrect (), the final decoded sequence is guaranteed to be different from , thus ensuring decoding failure.
Step 2.2: Ensuring Global Optimality of for Steps
To establish that is indeed the unique global optimum, we define the subsequent conditional probabilities to elevate the probability of the true optimal path while suppressing the probability of all competing paths, including the one initiated by the greedy choice .
Optimal Path: For any prefix of the optimal sequence, , we set the conditional probability of the next correct token to 1:
This deterministic transition ensures that the total probability of the optimal sequence is precisely:
By our initial choice, , satisfying the proposition’s condition.
Greedy Path: For any path beginning with the trap token , we must ensure its total probability is strictly less than . It is sufficient to control the probability at step . We set the maximum conditional probability following to be less than what is needed to compete with :
This condition is well-defined because our constraint ensures the numerator is non-negative. The total probability of the most likely sequence starting with , which we denote , is therefore bounded:
All other paths: For all other possible sequence prefixes, the remaining probability mass can be distributed (e.g., uniformly) in a way that ensures their total probabilities are also less than . This construction confirms that is the unique sequence with the highest probability, .
Step 3: Verifying the Decoding Error
The greedy decoder produces a sequence starting with , while the optimal sequence is starting with . Since , the Hamming distance is deterministically at least 1.
This confirms a non-zero error. In fact, by setting the continuation of the greedy path to be maximally different from , the Hamming distance can be made arbitrarily large, up to .
Step 4: Implications and Connection to the Paper’s Framework
This proposition provides a concrete illustration of the risks associated with unaligned policies, which are central to the motivation of our paper. Theorem [4.1](https://arxiv.org/html/2601.22513v2#S4.Thmtheorem1) establishes a lower bound on the probability of learning a policy where , particularly when the initial model quality is poor (large ). Our Proposition [4.3](https://arxiv.org/html/2601.22513v2#S4.Thmtheorem3) demonstrates the direct consequence of such a policy at inference time: it can lead to guaranteed and significant errors for standard decoding algorithms like greedy search.
This result bridges the gap between the learning failure (producing an unaligned model) and the inference failure (incorrect output generation). It underscores the practical necessity of the iterative alignment framework, which is designed to concentrate probability mass on optimal sequences to refine the policy, thereby pushing above the critical threshold and ensuring reliable decoding as per Proposition [4.3](https://arxiv.org/html/2601.22513v2#S4.Thmtheorem3).
Appendix F Proof of Theorem [6.2](https://arxiv.org/html/2601.22513v2#S6.Thmtheorem2): Performance Guarantees for Linear Softmax Models
F.1 Linear Softmax Parameterization and Self-Rewarding Training
Parameterized Policies.
In practice, a language model policy is realized by a large neural network (e.g., a Transformer) whose behavior is governed by a set of parameters . The vector encompasses all weights and biases of the model. Consequently, we denote the policy as . Optimizing over the policy space is thus equivalent to finding the optimal parameters in the parameter space .
Language models are typically autoregressive, factorizing the probability of a response into a product of conditional probabilities:
| (103) |
At each generation step , the model produces a vector of logits, , which is then transformed into a probability distribution over the vocabulary via the softmax function:
| (104) |
where denotes the logit value corresponding to token . This mechanism, applying the softmax function to the outputs of the model’s final linear layer, is what we refer to as the linear softmax parameterization.
Iterative Self-Rewarding Training
The training procedure is an iterative loop that begins with an initial model and progressively refines it. At round , we have the model parameters , corresponding to the policy .
LLM-as-a-Judge Self-Reward.
We use a self-reward that is computed by the model itself, where the reward for a given response is its log-probability under the current policy :
| (105) |
This choice of reward function systematically increases probability mass on higher-score sequences and decreases it on lower-score ones, as judged by the model’s own likelihood assignment.
Data for a Round.
Let be a dataset of triples sampled by drawing prompts and then sampling two responses . For each pair , their relative quality is measured by the difference in self-reward . This framing avoids the need for binary preference labels and instead models the continuous reward difference directly.
DPO-Style Realization (Square-Loss Form).
With the reference policy set to the current policy, , the DPO-style regression objective for round is to find the optimal parameters by minimizing the following loss with respect to :
| (106) |
where is the difference in self-reward between the two responses, calculated using the fixed reference model :
| (107) |
Minimizing drives the log-ratio difference of the policy to match the log-probability difference of the reference policy , effectively performing a regression on the reward difference. This shifts probability mass toward sequences with higher self-reward scores in a fine-grained manner.
Operator View in Parameter Space
This iterative process can be viewed as the sequential application of operators in the parameter space . For round , the optimization process defines an operator that maps the current parameters to the updated parameters :
| (108) |
After rounds of training, the final model parameters are the result of composing these operators:
| (109) |
Because the reward function is dynamically determined by the policy at each round, the entire training loop is self-contained. The model improves its capabilities through iterative generation, self-evaluation, and optimization, without requiring external human feedback.
F.2 Introduction and Problem Formulation
F.2.1 Objective
The objective of this section is to adapt a general theoretical proof in Section [C](https://arxiv.org/html/2601.22513v2#A3), originally designed for a finite policy class , to the specific case of the linear softmax model class, denoted . The core of this adaptation lies in replacing the uniform convergence argument, which relies on the cardinality of the policy class , with a more sophisticated technique based on covering numbers. This modification is necessary because the linear softmax model represents a continuous, and therefore infinite, class of policies, rendering the original proof’s dependence on inapplicable. The new derivation will provide a statistical error bound that correctly characterizes the complexity of the linear softmax model in terms of its parametric dimension, .
F.2.2 Recap of the General Analytical Framework
Our ultimate objective is to upper bound the probability that the learned policy after iterations, , assigns insufficient probability mass to its own optimal response, . To build towards this goal, we first analyze the initial case (). The established proof provides a general framework for this first step, which we will adapt.
The core strategy of the framework is to connect the probability of policy failure to a performance gap. Specifically, for the initial policy , the probability of failing to assign sufficient mass to the initial high quality response, , is bounded by a performance gap term, :
The bulk of the proof is then dedicated to bounding this performance gap. A key component in this bound is the statistical error term, , which captures the uncertainty inherent in learning from a finite dataset of size . The final bound on the performance gap takes the form:
In the original general proof, the policy class was assumed to be finite. The statistical error was consequently derived using Bernstein’s inequality and a union bound, leading to a term dependent on the size of the policy class:
Our task is to adapt this critical step. Since the linear softmax model constitutes a continuous, infinite class of policies, we must re-derive the statistical error term using tools appropriate for such spaces, namely covering numbers. This will replace the dependency on with a term that reflects the complexity of the linear softmax parameter space.
F.2.3 The Linear Softmax Model
We consider the linear softmax model class , defined as:
Definition F.1 (Linear Softmax Model).
Let be the feature dimension, and let be a feature map such that . Given a radius , the linear softmax model class is defined as:
where the policy is given by: .
This class is parameterized by a vector residing in a -dimensional ball of radius . Since the parameter space is a compact but uncountably infinite subset of , the cardinality is infinite. Consequently, any generalization bound that scales with is vacuous and must be replaced by a more appropriate measure of model complexity.
F.2.4 The Tool: Covering Numbers and -Nets
To handle infinite function classes, statistical learning theory employs the concept of covering numbers, which measure the ”effective size” or richness of the class at a specific resolution . This is formalized through the notion of an -net adapted to the linear softmax family .
Definition F.2.
(-net for ): Let . A finite subset is called an -net for the linear softmax class if for every , there exists such that
We denote by the size of the smallest such -net.
This definition provides a metric on the space of linear softmax policies. The key utility of an -net is that it provides a finite discretization of the infinite model class, which allows for the application of union bounds.
Definition F.3.
(Covering numbers) Given a model class and tolerance , the covering number is defined as the cardinality of the smallest -net for . That is,
The covering number quantifies the complexity of the function class. Establishing that this value is finite (and finding bounds for it, such as for the linear softmax class) is a cornerstone of proving generalization guarantees for learning algorithms.
F.2.5 Loss Function Definition
Recalling Equation [C.3](https://arxiv.org/html/2601.22513v2#A3.Ex54) from Section [C](https://arxiv.org/html/2601.22513v2#A3), we have:
| (110) |
where , , and the coupled-expectation shorthand denotes
and the pairwise differences defined as
| (111) | ||||
| (112) |
Then, we also define a preference scoring function, , as the difference between log-likelihood ratios:
We note that . Now, since and is the ERM solution, the empirical squared error of must be less than or equal to that of any other policy in , including itself. This implies:
| (113) |
For clarity and to ensure this report is self-contained, we restate the key definitions from the original proof framework. For any policy , the clipped squared loss for a single data point is defined as:
where is a clipping threshold to be determined. The empirical and population losses are, respectively:
and
The expectation for is over . On the clipping event, the loss is bounded:
F.3 Uniform Convergence Bound for the Linear Softmax Model
This section presents the core technical contribution: a new derivation of the uniform population bound for the linear softmax model class , replacing the original argument based on Bernstein’s inequality and a simple union bound. Our approach leverages the covering number bound for to handle the infinite nature of the policy class.
F.3.1 The Discretization Strategy
The standard methodology for establishing uniform convergence for an infinite, continuous function class involves a three-step process based on -nets:
-
1.
Construct a finite -net: Use the covering number lemma to establish the existence of a finite set that serves as a discrete approximation of the entire class.
-
2.
Establish uniform convergence over the net: Apply a concentration inequality (like Bernstein’s) and a union bound over the finite elements of the net . This yields a high-probability bound that holds simultaneously for all policies in the net.
-
3.
Extend the bound to the entire class: Show that if two policies are close with respect to the metric used for the -net, their corresponding losses are also close. This allows the bound established for the discrete net to be extended to any policy in the full class , at the cost of a small approximation error.
We now execute this strategy step-by-step.
F.3.2 Step 1: Bounding the Loss over an -Net
We begin by constructing a finite approximation of the policy space . Let be a resolution parameter to be chosen later. Our goal is to construct an -net for , which we will denote by , with respect to the metric
An -net is a finite set such that for any policy , there exists a policy with . We will explicitly construct such a net and bound its cardinality.
The construction proceeds in two stages. First, we build a net over the -dimensional parameter space . Second, we show that this parameter-space net induces the desired -net in the policy space.
1. Constructing a Net in the Parameter Space.
We need to find a finite set of points in that forms a net with a specific radius, let’s say . By a standard volumetric argument, we can bound the size of such a net. Consider a maximal set of points in that are separated by at least , i.e., for all . The open balls of radius centered at these points, , are disjoint. Furthermore, all these balls are contained within a larger ball of radius . By comparing the total volume of the small balls to the volume of the large ball, we have:
Since the volume of a -dimensional ball of radius is proportional to , this implies:
This maximal packing is also an -net. We will see that the required radius for our parameter net is . Substituting this into the bound gives a net size of at most . Standard results in high-dimensional geometry provide various bounds of this nature; for consistency with the analysis this proof is based on, we adopt the slightly looser but common bound of the form . Let us choose a net for with radius , which we denote , satisfying the size bound:
2. Mapping to a Net in the Policy Space.
Let be the set of policies corresponding to our parameter net. Now, for any policy , by construction of , there exists a parameter vector such that . We now show that .
Recall that the policy is defined as , where is the normalization constant. The log-ratio of two policies is:
We bound the magnitude of each term. For the first term, we assume a standard condition that the feature vectors are bounded, i.e., for all . Using the Cauchy-Schwarz inequality:
For the second term, we analyze the ratio of the normalization constants:
This is a weighted average of the term . From our bound on the first term, we know . Therefore, the exponential term is bounded as . Since the ratio is a weighted average of values within this range, it must also lie within the same range:
Taking the logarithm gives .
Finally, by the triangle inequality, we combine the bounds on the two terms:
Since this holds for any state-action pair , we have . We have thus shown that is a valid -net for , and its size is bounded by:
Our next objective is to derive a high-probability performance guarantee that holds uniformly over a finite set of policies . The derivation begins with a concentration inequality for a single, fixed policy and then extends it to the entire set using a union bound.
3. Performance Bound for a Single Policy.
For any fixed policy , the associated losses form a sequence of independent and identically distributed (i.i.d.) random variables. By construction, these losses are bounded within the interval . To relate the true expected loss to its empirical estimate , we can invoke Bernstein’s inequality. For any , Bernstein’s inequality gives:
A key challenge is that the variance term, , is unknown. However, for non-negative random variables bounded by , the variance can be bounded by the mean: . Substituting this into the inequality introduces on both sides, creating a recursive relationship.
Solving this inequality for in terms of —a process often referred to as a fixed-point calculation—yields a more practical, empirical version of Bernstein’s bound. Specifically, for a chosen failure probability , we can state the following: with probability at least ,
| (114) |
for some universal constant . This powerful result bounds the true loss for a single, predetermined policy.
4. Uniform Bound via the Union Bound
The bound in Eq. Eq. [114](https://arxiv.org/html/2601.22513v2#A6.E114) is insufficient for our needs, as we require a guarantee that holds simultaneously for all policies , not just one chosen in advance. To achieve this uniform convergence, we apply the union bound.
Let be the ”bad” event where the bound in Eq. Eq. [114](https://arxiv.org/html/2601.22513v2#A6.E114) fails for a specific policy . We want to bound the probability that at least one of these bad events occurs for any policy in the finite net , i.e., . The union bound states that this probability is at most the sum of the individual event probabilities:
To ensure the total probability of failure is no more than a desired level , we can enforce a much stricter failure probability for each individual policy. We set the individual failure probability for each to be .
By this construction, the total probability of at least one bound failing is at most:
Consequently, with a total probability of at least , the bound holds for all policies in simultaneously.
5. Final Uniform Bound
We now substitute our new choice of into the single-policy bound from Eq. Eq. [114](https://arxiv.org/html/2601.22513v2#A6.E114). This yields the uniform inequality: with probability at least , for all :
The term quantifies the complexity cost of generalizing from a single policy to the entire net. A larger net requires a stronger guarantee for each policy, which widens the overall bound.
Finally, by substituting the known bound on the cardinality of the -net, , which depends on the dimensionality of the policy class and the desired resolution , we arrive at the final expression:
This inequality provides a concrete, uniform performance guarantee over the discrete skeleton of our policy class. The subsequent analytical step is to extend this guarantee from the discrete net to the entire continuous policy class , ensuring our conclusions apply to any policy we might select. The next step is to extend this guarantee to the entire continuous class .
F.3.3 Step 2: Bounding the Approximation Error
To extend the bound from the net to the full class , we must demonstrate that the loss function exhibits a form of local stability or continuity. Specifically, if two policies and are close in the log-ratio metric, their corresponding losses must also be close. This property ensures that the bound on a net element provides a good approximation for the bound on any policy it covers. We formalize this in the following lemma.
Lemma F.4.
(Lipschitz-like Property of the Loss Function): Let with . Suppose that on the clipping event , we have that
Then, the difference in the clipped squared loss is bounded by:
Proof of Lemma [F.4](https://arxiv.org/html/2601.22513v2#A6.Thmtheorem4).
By definition, on the clipping event. Let . We want to bound . Using the identity , we have:
The first term is:
Let us analyze this difference:
| (115) |
By the triangle inequality and the -net property, the magnitude is bounded by:
The second term is:
On the clipping event, we have , , and . By the triangle inequality:
Combining these two bounds, we get:
This completes the proof of the lemma. ∎
Implication of Lemma [F.4](https://arxiv.org/html/2601.22513v2#A6.Thmtheorem4)
This lemma allows us to control the variation of both the population loss and the empirical loss as we move away from the points in the net. Specifically, for any and its closest neighbor :
F.3.4 Step 3: Combining the Bounds and Optimizing
We can now assemble the pieces to derive a uniform bound over the entire class . For any , let be its covering element, i.e., the policy in the net such that . Using the triangle inequality and the results from the previous steps:
This inequality holds with probability at least for all simultaneously. The right-hand side contains an error term that depends on our choice of the resolution . This term consists of an approximation error , which decreases as , and a statistical error (the term with ), which increases as due to the factor. To obtain the tightest possible bound, we must choose to balance this trade-off.
Let’s simplify the error term by substituting and ignoring constants:
A standard approach to minimize such an expression is to set the two terms to be of the same order of magnitude:
Ignoring the logarithmic dependency on for a first-order approximation, a near-optimal choice in learning theory for balancing an error of the form is achieved by
When this is done, both terms become of the order . The total error is dominated by this rate. Therefore, after optimizing for , the uniform convergence bound takes the form:
F.4 The Refined Statistical Error and Integration into the Main Proof
F.4.1 Derivation of the New
We now apply the uniform bound derived above to the empirical risk minimizer (ERM) policy, . The ERM property from the original proof states that (Eq. [34](https://arxiv.org/html/2601.22513v2#A3.E34)). Substituting and into our new uniform bound yields:
This bound on is precisely the population-level squared error on the clipped region. We can therefore define our new statistical error term, , as:
This result replaces the original Eq. [38](https://arxiv.org/html/2601.22513v2#A3.E38). The key difference is the replacement of the complexity term with , which correctly captures the dependence on the parametric dimension of the linear softmax model.
It is also necessary to update the choice of the clipping parameter . The original choice was motivated by controlling tail probabilities over a union bound of size . The analogous choice in our setting is to control tails over samples and the policies in the net. A suitable choice is:
With an optimal , this becomes
This shows that scales polynomially with and logarithmically with , which is consistent with the overall structure of the bound. For simplicity in the final expression, we can absorb these logarithmic factors into and write the rate as .
F.4.2 Integration into the Global Proof Structure
With the newly derived statistical error term, we can now return to the main flow of the proof. The inequality [C.3](https://arxiv.org/html/2601.22513v2#A3.Ex54) provides a bound on the performance gap in terms of the population squared error:
| (116) |
where , , The term under the square root is precisely bounded by what we defined as . Substituting this new bound yields:
The remainder of the proof proceeds exactly as in the original version, using this updated definition of . After bounding the concentrability coefficients and KL divergence term, and balancing the error terms, we arrive at the clean form:
Finally, we substitute this refined bound on the performance gap back into the initial inequality that connects it to the probability of failure. This yields the final, adapted result for the linear softmax model:
| (117) |
By definition of the round-1 policy maximizer, we denote
| (118) |
It immediately follows that the maximizer dominates the baseline target pointwise, in the sense that
Consequently, whenever , it must also hold that . Equivalently,
| (119) |
Taking probabilities under and invoking the previously established bound for the right-hand event, we obtain
| (120) |
This expression replaces the original Equation [43](https://arxiv.org/html/2601.22513v2#A3.E43). It successfully adapts the general proof architecture to the linear softmax model by incorporating a complexity measure, , derived from covering number arguments, instead of the inapplicable term. The recursive argument for subsequent iterations () would then proceed from this new single-step bound, with the complexity term propagating through the analysis of the policy condition numbers .
F.5 Bounding the Policy Condition Number
Our next objective is to establish a sharp upper bound for the coverage parameter
| (121) |
Define the nonnegative random variable
| (122) |
Its expectation admits the standard tail–integral representation:
| (123) |
1. Support of and reduction of the integral.
2. Relating the tail to the round-1 failure bound.
For any , set so that . Then
Invoking the round-1 bound (cf. Eq. [120](https://arxiv.org/html/2601.22513v2#A6.E120)) yields
| (127) |
For notational convenience define
| (128) |
Since probabilities are at most ,
| (129) |
3. Exact integral evaluation via the switch point .
The function is strictly decreasing on , with and . Hence there exists a unique solving , namely
| (130) |
We now distinguish two regimes:
(i) Nontrivial regime: and . Then
and therefore
| (131) |
Using the antiderivative
| (132) |
we obtain
| (133) |
Combining Eq. [126](https://arxiv.org/html/2601.22513v2#A6.E126), Eq. [131](https://arxiv.org/html/2601.22513v2#A6.E131), and Eq. [133](https://arxiv.org/html/2601.22513v2#A6.E133) yields
| (134) |
(ii) Saturated regime: either or . In this case on , hence
| (135) |
4. A concise, numerically stable upper bound.
5. Specialization to the linear softmax model.
Substituting the explicit form of ,
into Eq. [138](https://arxiv.org/html/2601.22513v2#A6.E138) and using the non-saturated branch yields the advertised bound
| (139) |
Remarks.
-
(i)
The constant aggregates the statistical error and regularization effects. The “nontrivial” case corresponds to the high–confidence regime where the failure tail is integrable with a logarithmic correction.
-
(ii)
The monotonicity of justifies the unique switch point and the split–integral evaluation. The clean relaxation Eq.
[137](https://arxiv.org/html/2601.22513v2#A6.E137)trades a small slack for algebraic transparency. -
(iii)
The dependence on and enters through the covering–number–driven statistical term, producing the characteristic factor .
F.6 Recursive Analysis and Asymptotic Behavior of Policy Condition Number
The analysis of the first iteration () provides the essential foundation for a recursive framework that extends our performance guarantees to an arbitrary number of iterations . At its core, the argument relies on the observation that the bound on the policy performance at iteration is determined by two factors: (i) the statistical accuracy of the update at that step, and (ii) the inherited coverage coefficient from the previous iteration, . The recursive nature of this dependency induces a dynamic system of bounds whose long-term stability properties must be carefully analyzed.
Recursive Formulation.
By induction on , the derivation for extends naturally to arbitrary . Specifically, the coverage parameter at iteration satisfies the recurrence
| (140) |
This recurrence encapsulates the interaction between statistical error, represented by the square-root term, and regularization effects, represented by the logarithmic term. The combination ensures that although may initially be large, successive iterations prevent uncontrolled growth, enforcing stability in the long run.
Simplification via Constants.
To streamline the analysis, we define
Substituting these definitions, the recurrence can be written more compactly as
| (141) |
The presence of both and reflects the dual statistical–regularization structure of the update process.
Bounding the Recurrence.
Although Eq. [141](https://arxiv.org/html/2601.22513v2#A6.E141) is nonlinear, we can simplify its analysis. Using the classical inequality for (a condition satisfied since as an expectation of inverse probabilities), we obtain
| (142) |
This upper bound reduces the problem to a square-root recursion, which admits tractable asymptotic analysis.
Fixed-Point Analysis.
The iterative map has a unique positive fixed point , obtained by solving . Solving this quadratic in yields
| (143) |
This fixed point represents the stable asymptotic value of the coverage parameter. Its existence guarantees that the self-rewarding process cannot diverge indefinitely; rather, it is inherently stable and bounded by problem-specific constants.
Convergence Rate.
The contraction rate of the iteration is determined by the derivative of at the fixed point:
Defining
| (144) |
we observe that , which implies that convergence to is geometric. The deviation from the fixed point shrinks by a factor of at least at each iteration, guaranteeing rapid stabilization.
Explicit Bound for Finite .
This geometric contraction yields an explicit finite- bound:
| (145) |
for all . The residual dependence on the initialization decays exponentially, while the asymptotic behavior is governed entirely by .
Asymptotic Behavior and Practical Implications.
To obtain further intuition, consider the regime where , so that the statistical term dominates the regularization term . In this case, the fixed point satisfies
leading to the explicit bound
| (146) |
This final bound highlights two crucial features. First, the influence of the initialization vanishes exponentially fast with , ensuring robustness to poor starting conditions. Second, the asymptotic stable value decreases as grows, confirming that larger sample sizes yield improved coverage and reduced statistical uncertainty. These insights reinforce the interpretation of the self-rewarding process as not only stable but also statistically efficient in the large-sample regime.
F.7 Final Performance Bound for Arbitrary Iteration
Having established the asymptotic stability of the coverage coefficient, we are now prepared to present the main performance guarantee for the policy after an arbitrary rounds of self-rewarding training. The derivation closely parallels the single-step analysis, but it crucially leverages our recursive understanding of across iterations.
From Coverage to Performance.
The probability that the policy assigns insufficient probability mass to its own optimal response is controlled by its performance gap relative to the KL-regularized optimal policy. This gap, in turn, depends on the statistical error of the learning step at iteration , which is governed by the coverage coefficient of the previous iterate . Formally, we obtain the -step analogue of the single-step bound:
| (147) |
This expression links the performance at iteration to the coverage inherited from iteration .
Substituting the Asymptotic Bound.
The crucial final step is to substitute into Eq. [147](https://arxiv.org/html/2601.22513v2#A6.E147) our explicit asymptotic bound for from Eq. [146](https://arxiv.org/html/2601.22513v2#A6.E146). This replacement eliminates the iteration-dependent and unknown , yielding an expression in terms of fundamental parameters of the problem and the initial condition .
By taking the square root of the bound on (and applying the inequality ), we obtain a clean decomposition. As grows, the dominant contribution arises from the square root of the asymptotic stable value, which scales with . The residual dependence on the initialization decays exponentially and quickly becomes negligible. Substituting these estimates back into Eq. [147](https://arxiv.org/html/2601.22513v2#A6.E147), and noting that the term is of lower order, we arrive at the final result:
| (148) |
Interpretation.
This inequality, the culmination of our analysis, provides several insights into the behavior of the self-rewarding process for the linear softmax model class:
-
•
Statistical Complexity. The leading error term scales as , quantifying the inherent learning difficulty of the parametric model. Performance improves as increases, while higher dimensionality incurs increased complexity. This replaces the inapplicable term in the finite-class setting with a refined, distribution-dependent complexity measure.
-
•
Stability and Self-Correction. The second term inside the parentheses demonstrates exponential decay of the influence of the initial coverage . Even if the initial policy is poorly calibrated (large ), its effect on performance vanishes rapidly as grows. This validates the intuition that the self-rewarding loop is self-correcting.
-
•
Long-Term Performance. In the limit , the decaying initialization term disappears entirely. The ultimate performance is dictated solely by the statistical error and the problem’s intrinsic difficulty, captured by . This confirms that the process converges to a stable, initialization-independent error floor.
Conclusion.
Equation [148](https://arxiv.org/html/2601.22513v2#A6.E148) completes the adaptation of the general recursive argument to the linear softmax model class. It provides a rigorous and interpretable guarantee: the model’s performance stabilizes to a predictable asymptotic rate, while transient initialization effects are washed out exponentially fast. This establishes both the robustness and the efficiency of self-rewarding training in this setting.
Appendix G Proof of Corollary [6.4](https://arxiv.org/html/2601.22513v2#S6.Thmtheorem4): Data-Dependent Bounds via Effective Dimension
We strengthen the parametric guarantee by replacing the ambient dimension in the statistical factor with a data-dependent effective dimension. This mitigates “curse of dimensionality” and better reflects the spectral structure of the feature covariance under the data distribution.
Definition G.1 (Ridge effective dimension).
For any define the ridge effective dimension
where are the eigenvalues of in nonincreasing order. It holds that and is nonincreasing in . In the isotropic case and for we have .
Lemma G.2 (Metric entropy with covariance geometry).
Let . For the metric induced by , the -covering number of satisfies
for a universal constant . Consequently, whenever an argument in the proof of Theorem [6.2](https://arxiv.org/html/2601.22513v2#S6.Thmtheorem2) uses the ambient-dimension entropy bound , it can be replaced by the covariance-adaptive bound above.
Proof of Lemma [G.2](https://arxiv.org/html/2601.22513v2#A7.Thmtheorem2).
Diagonalize and reparameterize . The -norm is . Cover the ellipsoid by axis-aligned slabs with granularity matched to . Summing the logarithms of the per-axis covering counts yields . A monotone integral comparison together with the ridge truncation gives the stated dependence.
Explicit regimes for the ridge effective dimension.
The following elementary bounds will be useful:
| (149) |
We quantify under concrete spectral assumptions and then substitute it into the parametric bound of Theorem [6.2](https://arxiv.org/html/2601.22513v2#S6.Thmtheorem2).
Assumption G.3 (Spectral regimes).
Let be the spectrum of in nonincreasing order. We consider the following cases.
-
(A)
Exponential decay. There exist constants and such that for all .
-
(B)
Polynomial decay. There exist constants and such that for all .
-
(C)
Spikedsmall tail. There is an integer and such that for and with possibly small.
Lemma G.4 (Effective dimension under Assumption [G.3](https://arxiv.org/html/2601.22513v2#A7.Thmtheorem3)).
Under Assumption [G.3](https://arxiv.org/html/2601.22513v2#A7.Thmtheorem3) the following bounds hold for all .
-
(A)
Exponential decay implies logarithmic scaling:
In particular, choosing gives .
-
(B)
Polynomial decay yields a power-law in :
In particular, choosing gives .
-
(C)
Spikedsmall tail gives when dominates the tail:
Hence for any we have . If moreover , then .
Proof of Lemma [G.4](https://arxiv.org/html/2601.22513v2#A7.Thmtheorem4).
(A) Let . Then and thus . The tail sum obeys , so the second term in Eq. [149](https://arxiv.org/html/2601.22513v2#A7.E149) is . (B) Let so that . Then and , making the tail contribution . (C) Split the sum at and use Eq. [149](https://arxiv.org/html/2601.22513v2#A7.E149) on the tail: .
Corollary G.5 (Parametric bound with effective dimension).
Under conditions of Theorem [6.2](https://arxiv.org/html/2601.22513v2#S6.Thmtheorem2), fix any . With probability at least ,
Proof
Repeat the proof of Theorem [6.2](https://arxiv.org/html/2601.22513v2#S6.Thmtheorem2) and Corollary [5.7](https://arxiv.org/html/2601.22513v2#S5.Thmtheorem7) replacing the ambient-dimension entropy bound by Lemma [G.2](https://arxiv.org/html/2601.22513v2#A7.Thmtheorem2). The empirical Bernstein step and the iterative self-correction argument are unchanged, yielding the same stability–transient factor and the covering-number contribution with .
Corollary G.6 (Substitution into the parametric risk bound).
Under the conditions of Theorem [6.2](https://arxiv.org/html/2601.22513v2#S6.Thmtheorem2), the following explicit forms hold when in the statistical factor is replaced by .
-
(A)
If has exponential spectral decay and , then
Thus the dependence on is replaced by a double logarithm in .
-
(B)
If has polynomial decay of order and , then
Here the ambient dimension no longer appears. The rate is governed by the spectral exponent .
-
(C)
In the spikedsmall-tail model with rank spike and tail mass , any gives
If , the -dependence is reduced to inside the statistical factor.
Remark G.7 (Choice and interpretation of ).
The parameter is an analysis device that interpolates between ambient and intrinsic complexity.
-
•
In isotropic or full-rank regimes with flat spectra, taking recovers .
-
•
With spectral decay, e.g., for , one has for moderate , tightening the bound.
-
•
A practical choice is (or any monotone schedule ), which trades a slightly larger bias in the entropy radius for a sharply reduced . The contraction threshold in remains unaffected because it depends only on and .
Remark G.8 (When does look like ?).
Two representative scenarios lead to a logarithmic-in- dependence.
-
(i)
Log-rank energy concentration. Suppose the spectrum concentrates on leading directions, in the sense that with small. Taking gives by Lemma
[G.4](https://arxiv.org/html/2601.22513v2#A7.Thmtheorem4). -
(ii)
Geometric decay until the ambient cutoff. If with , then for any above the tail floor one has . If additionally is chosen proportional to for some , then .
In both cases, substituting into the statistical factor replaces by .