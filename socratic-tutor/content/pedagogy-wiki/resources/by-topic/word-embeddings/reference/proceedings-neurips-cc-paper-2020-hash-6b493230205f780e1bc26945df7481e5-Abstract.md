# Source: https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html
# Title: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
# Fetched via: search
# Date: 2026-04-10

Tom B. Brown∗
Benjamin Mann∗
Nick Ryder∗
Melanie Subbiah∗
Jared Kaplan†
Prafulla Dhariwal
Arvind Neelakantan
Pranav Shyam
Girish Sastry
Amanda Askell
Sandhini Agarwal
Ariel Herbert-Voss

…

language model with 175 billion parameters, 10x more than any previous non-
sparse language model, and test its performance in the few-shot setting. For all
tasks, GPT-3 is applied without any gradient updates or fine-tuning, with tasks
and few-shot demonstrations specified purely via text interaction with the model.

…

agnostic, a final task-specific step remains: fine-tuning on a large dataset of examples to adapt a task
agnostic model to perform a desired task.
Recent work [RWC+19] suggested this final step may not be necessary. [RWC+19] demonstrated
that a single pretrained language model can be zero-shot transferred to perform standard NLP tasks
∗Equal contribution
†Johns Hopkins University, OpenAI
34th Conference on Neural Information Processing Systems (NeurIPS 2020), Vancouver, Canada.

…

which we call GPT-3, and measure its transfer learning abilities.
As part of this investigation, we also clarify and systematize the approach introduced in [RWC+19].
While [RWC+19] describe their work as “zero-shot task transfer” they sometimes provide examples
of the relevant task in the context. Due to the use of what are effectively training examples, these
cases are better described as “one-shot” or “few-shot” transfer. We study these one-shot and few-shot
settings in detail comparing them with the zero-shot setting which only uses a natural language
description or invocation of the task to be performed. Our findings are summarized in Figure 1.1. We

…

2
Approach
Our basic pre-training approach, including model, data, and training, is similar to the process
described in [RWC+19], with relatively straightforward scaling up of the model size, dataset size and
diversity, and length of training. Our use of in-context learning is also similar to [RWC+19], but in
this work we systematically explore different settings for learning within the context:
• Fine-Tuning (FT) - updates the weights of a pre-trained model by training on thousands of
supervised labels specific to the desired task. The main advantage of fine-tuning is strong
performance on many benchmarks. The main disadvantages are the need for a new large
dataset for every task, the potential for poor generalization out-of-distribution [MPL19], and
the potential to exploit spurious features of the training data [GSL+18, NK19]. We focus
on task-agnostic performance, leaving fine-tuning for future work.
• Few-Shot (FS) - the model is given a few demonstrations of the task at inference time as
conditioning [RWC+19], but no weights are updated. An example typically has a context
and a desired completion (for example an English sentence and the French translation),
and few-shot works by giving K examples of context and completion, and then one final
example of context, with the model expected to provide the completion (see appendix for
more details). We typically set K in the range of 10 to 100, as this is how many examples can
fit in the model’s context window (nctx = 2048). The main advantage of few-shot is a major
reduction in the need for task-specific data. The main disadvantage is that results from this

…

and then rapidly adapting to a new task.
• One-Shot (1S) - similar to few-shot but with K = 1.
• Zero-Shot (0S) - similar to few-shot but with a natural language description of the task
instead of any examples.
The appendix includes a demonstration of the four methods using the example of translating English
to French. While the few-shot results we present in this paper achieve the highest performance,
one-shot, or even sometimes zero-shot, seem like the fairest comparisons to human performance, and
are important targets for future work.
2.1
Model and Architectures
We use the same model and architecture as GPT-2 [RWC+19], including the modified initialization,

…

last being the model we call GPT-3. This range of model sizes allows us to test the scaling laws
introduced in [KMH+20].
More details on the sizes and architectures of our models can be found in the appendix. We partition
each model across GPUs along both the depth and width dimension in order to minimize data-transfer
between nodes.
2.2
Training Dataset
To create our training data, we (1) downloaded and filtered a version of CommonCrawl1 [RSR+19]
based on similarity to a range of high-quality reference corpora, (2) performed fuzzy deduplication at
the document level, within and across datasets, to prevent redundancy and preserve the integrity of
our held-out validation set as an accurate measure of overfitting, and (3) added known high-quality
reference corpora to the training mix to augment CommonCrawl and increase its diversity. These
reference corpora include an expanded version of the WebText dataset [RWC+19], collected by
1https://commoncrawl.org/the-data/
3

…

LAMBADA while achieving respectable performance on two difficult completion prediction datasets.
a[Tur20] b[RWC+19] c[LDL19] d[LCH+20]
scraping links over a longer period of time, and first described in [KMH+20], two internet-based
books corpora (Books1 and Books2) and English-language Wikipedia (details in the appendix).

…

larger models without running out of memory, we use a mixture of model parallelism within each
matrix multiply and model parallelism across the layers of the network. All models were trained on
V100 GPU’s on part of a high-bandwidth cluster. Details of the training process and hyperparameter
settings are described in the appendix.
2.4
Evaluation
For few-shot learning, we evaluate each example in the evaluation set by randomly drawing K
examples from that task’s training set as conditioning, delimited by 1 or 2 newlines depending on
the task. For LAMBADA and Storycloze there is no supervised training set available so we draw

…

On tasks with free-form completion, we use beam search with the same parameters as [RSR+19]: a
beam width of 4 and a length penalty of α = 0.6.
Final results are reported on the test set when publicly available, for each model size and learning
setting (zero-, one-, and few-shot). When the test set is private, our model is often too large to fit on

…

primarily consists of English (93% by word count), it also includes 7% non-English content (full list
at GPT-3 GitHub). Existing unsupervised machine translation approaches often combine pretraining
on a pair of monolingual datasets with back-translation [SHB15] to bridge the two languages in a

…

unsupervised pretraining, finetuning on 608K labeled examples, and backtranslation [LHCG19b].
3.4
SuperGLUE
The SuperGLUE benchmark is a standardized collection of datasets [WPN+19]. In the few-shot
setting, we used 32 examples for all tasks, sampled randomly from the training set. For all tasks
except WSC and MultiRC, we sampled a new set of examples to use in the context for each problem.
For WSC and MultiRC, we used the same set of randomly drawn examples from the training set
6

…

the clean subset is similar to the score on the entire dataset, this suggests that contamination, even if
present, does not have a significant effect on reported results. In most cases performance changes only
negligibly, and we see no evidence that contamination level and performance difference are correlated.
We conclude that either our conservative method substantially overestimated contamination or that
contamination has little effect on performance. We provide full details of the methodology and
analysis on the most problematic tasks in the appendix.
7

…

denoising. Our design decision comes at the cost of potentially worse performance on tasks which
empirically benefit from bidirectionality, such as fill-in-the-blank tasks, tasks that involve looking
back and comparing two pieces of content (ANLI, WIC), or tasks that require re-reading or carefully
considering a long passage and then generating a very short answer (QuAC, RACE).
Our objective weights every token equally and lacks a notion of what is most important to predict
and what is less important. [RRS20] demonstrate benefits of customizing prediction to entities of
interest. Also, with self-supervised objectives, task specification relies on forcing the desired task into

…

focused on increasing parameter count but not computation by using the conditional computation
framework [BLC13]. Specifically, the mixture-of-experts method [SMM+17] has produced 100
billion parameter models and 50 billion parameter translation models [AJF19]. One way to decrease
the computational cost of our models would be to draw from work such as ALBERT [LCG+19] or
general [HVD15] or task-specific [SDCW19, JYS+19, KR16] approaches to distillation. Lastly, a
third approach to scale increases computation without increasing parameters through methods like
adaptive computation time [Gra16] and the universal transformer [DGV+18].
There are many approaches to building multi-task models. Giving task instructions in natural language

…

[FAL17]. Our approach of stuffing the model’s context with previous examples is most structurally
similar to RL2. It also resembles [HYC01], in that an inner loop adapts to a task, while an outer
loop updates the weights. Our inner loop performs few-shot in-context learning, but prior work has

…

We presented a 175 billion parameter language model which shows strong performance on many
NLP tasks and benchmarks in the zero-shot, one-shot, and few-shot settings, in some cases nearly
matching the performance of state-of-the-art fine-tuned systems, as well as generating high-quality
samples and strong qualitative performance at tasks defined on-the-fly. We documented roughly

…

frameworks, which outline key steps such as identifying threats and potential impacts, assessing
likelihood, and determining risk as a combination of likelihood and impact [Ros12]. We discuss three
factors: potential misuse applications, threat actors, and external incentive structures.
7.1.1
Potential Misuse Applications
Any socially harmful activity that relies on generating text could be augmented by powerful lan-

NeurIPS 2021 papers

1.
Near-Optimal No-Regret Learning in General Games

Constantinos Costis Daskalakis, Maxwell Fishelson, Noah Golowich

rating :

8.75 - [9, 10, 8, 8] - Accept (Oral)

…

This simple density representation has three benefits: (i) it provides a useful inductive bias to the geometry learned in the neural volume rendering process; (ii) it facilitates a bound on the opacity approximation error, leading to an accurate sampling of the viewing ray. Accurate sampling is important to provide a precise coupling of geometry and radiance; and (iii) it allows efficient unsupervised disentanglement of shape and appearance in volume rendering.

…

We show that, depending on the data properties, the nonlinear response model, and the loss function, the Hessian can have *qualitatively* different spectral behaviors: of bounded or unbounded support, with single- or multi-bulk, and with isolated eigenvalues on the left- or right-hand side of the main eigenvalue bulk. By focusing on such a simple but nontrivial model, our analysis takes a step forward to unveil the theoretical origin of many visually striking features observed in more realistic machine learning models.
4.
List-Decodable Mean Estimation in Nearly-PCA Time

Ilias Diakonikolas, Daniel Kane, Daniel Kongsgaard, Jerry Li, Kevin Tian

rating :

8.33 - [8, 10, 7] - Accept (Spotlight)

tl;dr:
We give a state-of-the-art algorithm for list-decodable mean estimation, the robust generalization of learning mixture models, attaining optimal error in polylogarithmic calls to approximate PCA.

…

We study the fundamental task of list-decodable mean estimation in high dimensions. Our main result is a new algorithm for bounded covariance distributions with optimal sample complexity and near-optimal error guarantee, running in {\em nearly-PCA time}. Assuming the ground truth distribution on Rd has identity-bounded covariance, our algorithm outputs O(k) candidate means, one of which is within distance O(klog⁡k) from the truth.
Our algorithm runs in time O~(ndk) , where n is the dataset size. This runtime nearly matches the cost of performing k -PCA on the data, a natural bottleneck of known algorithms for (very) special cases of our problem, such as clustering well-separated mixtures. Prior to our work, the fastest runtimes were O~(n2dk2) ~\cite{DiakonikolasKK20}, and O~(ndkC) \cite{CherapanamjeriMY20} for an unspecified constant C≥6 .

…

Our key idea is that there are two components of exploration: (1) an agent-centric component encouraging exploration of unseen parts of the environment based on an agent’s belief; (2) an environment-centric component encouraging exploration of inherently interesting objects. We show that our formulation is effective and provides the most consistent exploration across several training-testing environment pairs. We also introduce benchmarks and metrics for evaluating task-agnostic exploration strategies. The source code is available at https://github.com/sparisi/cbet/.

…

The problem requires we estimate the average treatment effect τ∗:=∑ijTijZij/∑ijZij . The synthetic control paradigm provides an approach to estimating τ∗ when Z places support on a single row. This paper extends that framework to allow rate-optimal recovery of τ∗ for general Z , thus broadly expanding its applicability. Our guarantees are the first of their type in this general setting. Computational experiments on synthetic and real-world data show a substantial advantage over competing estimators.

…

Interpreting all signals in the network as continuous, we derive generally applicable, small architectural changes that guarantee that unwanted information cannot leak into the hierarchical synthesis process. The resulting networks match the FID of StyleGAN2 but differ dramatically in their internal representations, and they are fully equivariant to translation and rotation even at subpixel scales. Our results pave the way for generative models better suited for video and animation.

…

10.
Coresets for Clustering with Missing Values

Vladimir Braverman, Shaofeng H.-C. Jiang, Robert Krauthgamer, Xuan Wu

rating :

8.25 - [9, 8, 8, 8] - Accept (Spotlight)

tl;dr:
We provide the first coreset and near-linear time PTAS for clustering with (multiple) missing values

…

We further design an algorithm to construct these coresets in near-linear time, and consequently improve a recent quadratic-time PTAS for k -Means with missing values [Eiben et al., SODA 2021] to near-linear time. We validate our coreset construction, which is based on importance sampling and is easy to implement, on various real data sets. Our coreset exhibits a flexible tradeoff between coreset size and accuracy, and generally outperforms the uniform-sampling baseline. Furthermore, it significantly speeds up a Lloyd's-style heuristic for k -Means with missing values.

…

The differentiable PSR layer allows us to efficiently and differentiably bridge the explicit 3D point representation with the 3D mesh via the implicit indicator field, enabling end-to-end optimization of surface reconstruction metrics such as Chamfer distance. This duality between points and meshes hence allows us to represent shapes as oriented point clouds, which are explicit, lightweight and expressive.
Compared to neural implicit representations, our Shape-As-Points (SAP) model is more interpretable, lightweight, and accelerates inference time by one order of magnitude. Compared to other explicit representations such as points, patches, and meshes, SAP produces topology-agnostic, watertight manifold surfaces. We demonstrate the effectiveness of SAP on the task of surface reconstruction from unoriented point clouds and learning-based reconstruction.

…

14.
Oracle Complexity in Nonsmooth Nonconvex Optimization

Guy Kornowski, Ohad Shamir

rating :

8.0 - [8, 7, 8, 8, 9] - Accept (Oral)

tl;dr:
We theoretically study nonsmooth nonconvex optimization from an oracle complexity viewpoint, proving both hardness results and tradeoffs between computational efficiency and performance

…

In this paper, we study nonsmooth nonconvex optimization from an oracle complexity viewpoint, where the algorithm is assumed to be given access only to local information about the function at various points. We provide two main results (under mild assumptions): First, we consider the problem of getting \emph{near} ϵ -stationary points.

…

For this approach, we prove an inherent trade-off between oracle complexity and smoothness: On the one hand, smoothing a nonsmooth nonconvex function can be done very efficiently (e.g., by randomized smoothing), but with dimension-dependent factors in the smoothness parameter, which can strongly affect iteration complexity when plugging into standard smooth optimization methods. On the other hand, these dimension factors can be eliminated with suitable smoothing methods, but only by making the oracle complexity of the smoothing process exponentially large.

…

We introduce Latent Equilibrium, a new framework for inference and learning in networks of slow components which avoids these issues by harnessing the ability of biological neurons to phase-advance their output with respect to their membrane potential. This principle enables quasi-instantaneous inference independent of network depth and avoids the need for phased plasticity or computationally expensive network relaxation phases.
We jointly derive disentangled neuron and synapse dynamics from a prospective energy function that depends on a network's generalized position and momentum. The resulting model can be interpreted as a biologically plausible approximation of error backpropagation in deep cortical networks with continuous-time, leaky neuronal dynamics and continuously active, local plasticity. We demonstrate successful learning of standard benchmark datasets, achieving competitive performance using both fully-connected and convolutional architectures, and show how our principle can be applied to detailed models of cortical microcircuitry.

…

Prior work has approached similar problems with a two-stage process, first learning a reward function and then optimizing this reward function using another reinforcement learning algorithm. In contrast, our method directly learns a value function from transitions and successful outcomes, without learning this intermediate reward function. Our method therefore requires fewer hyperparameters to tune and lines of code to debug. We show that our method satisfies a new data-driven Bellman equation, where examples take the place of the typical reward function term. Experiments show that our approach outperforms prior methods that learn explicit reward functions.

…

As a further advantage, DAIS allows for mini-batch gradients. We provide a detailed convergence analysis for Bayesian linear regression which goes beyond previous analyses by explicitly accounting for the sampler not having reached equilibrium. Using this analysis, we prove that DAIS is consistent in the full-batch setting and provide a sublinear convergence rate.

…

This paper investigates how to realize better and more efficient embedding learning to tackle the semi-supervised video object segmentation under challenging multi-object scenarios. The state-of-the-art methods learn to decode features with a single positive object and thus have to match and segment each target separately under multi-object scenarios, consuming multiple times computing resources. To solve the problem, we propose an Associating Objects with Transformers (AOT) approach to match and decode multiple objects uniformly.
In detail, AOT employs an identification mechanism to associate multiple targets into the same high-dimensional embedding space. Thus, we can simultaneously process multiple objects' matching and segmentation decoding as efficiently as processing a single object. For sufficiently modeling multi-object association, a Long Short-Term Transformer is designed for constructing hierarchical matching and propagation. We conduct extensive experiments on both multi-object and single-object benchmarks to examine AOT variant networks with different complexities.

…

In addition, we embed a noise adaptation module into the training phase to compensate the approximation error. The experiments on several benchmark datasets and neural architectures illustrate that the binary network learned using our method achieves the state-of-the-art accuracy. Code will be available at https://gitee.com/mindspore/models/tree/master/research/cv/FDA-BNN.

In 2021, NeurIPS introduced a new track, Datasets and Benchmarks.
The first year of that
track, 2021, has its own proceedings, accessible by the link below.
From 2022 on, the Datasets and
Benchmarks papers are in the main NeurIPS proceedings.
- Advances in Neural Information Processing Systems 37 NeurIPS 2024
- Advances in Neural Information Processing Systems 36 NeurIPS 2023
- Advances in Neural Information Processing Systems 35 NeurIPS 2022
- Advances in Neural Information Processing Systems 34 NeurIPS 2021
- Advances in Neural Information Processing Systems 33 NeurIPS 2020

|Test of Time Award|Online Learning for Latent Dirichlet Allocation Matthew Hoffman · Francis Bach · David Blei Abstract This paper introduces a stochastic variational gradient based inference procedure for training Latent Dirichlet Allocation (LDA) models on very large text corpora. On the theoretical side it is shown that the training procedure converges to a local optimum and that, surprisingly, the simple stochastic gradient updates correspond to a stochastic natural gradient of the evidence lower bound (ELBO) objective. On the empirical side the authors show that for the first time LDA can be comfortably trained on text corpora of several hundreds of thousands of documents, making it a practical technique for “big data” problems. The idea has made a large impact in the ML community because it represented the first stepping stone for general stochastic gradient variational inference procedures for a much broader class of models. After this paper, there would be no good reason to ever use full batch training procedures for variational inference anymore.|
|--|--|
|Outstanding Paper|MAUVE: Measuring the Gap Between Neural Text and Human Text using Divergence Frontiers Krishna Pillutla · Swabha Swayamdipta · Rowan Zellers · John Thickstun · Sean Welleck · Yejin Choi · Zaid Harchaoui Abstract As major progress is made in open-ended text generation, measuring how close machine-generated text is to human language remains a critical open problem. We introduce Mauve, a comparison measure for open-ended text generation, which directly compares the learnt distribution from a text generation model to the distribution of human-written text using divergence frontiers. Mauve scales up to modern text generation models by computing information divergences in a quantized embedding space. Through an extensive empirical study on three open-ended generation tasks, we find that Mauve identifies known properties of generated text, scales naturally with model size, and correlates with human judgments, with fewer restrictions than existing distributional evaluation metrics.|
|Outstanding Paper|A Universal Law of Robustness via Isoperimetry Sebastien Bubeck · Mark Sellke Abstract Classically, data interpolation with a parametrized model class is possible as long as the number of parameters is larger than the number of equations to be satisfied. A puzzling phenomenon in the current practice of deep learning is that models are trained with many more parameters than what this classical theory would suggest. We propose a theoretical explanation for this phenomenon. We prove that for a broad class of data distributions and model classes, overparametrization is {\em necessary} if one wants to interpolate the data {\em smoothly}. Namely we show that {\em smooth} interpolation requires $d$ times more parameters than mere interpolation, where $d$ is the ambient data dimension. We prove this universal law of robustness for any smoothly parametrized function class with polynomial size weights, and any covariate distribution verifying isoperimetry. In the case of two-layers neural networks and Gaussian covariates, this law was conjectured in prior work by Bubeck, Li and Nagaraj. We also give an interpretation of our result as an improved generalization bound for model classes consisting of smooth functions.|
|Outstanding Paper|Continuized Accelerations of Deterministic and Stochastic Gradient Descents, and of Gossip Algorithms Mathieu Even · Raphaël Berthier · Francis Bach · Nicolas Flammarion · Hadrien Hendrikx · Pierre Gaillard · Laurent Massoulié · Adrien Taylor Abstract We introduce the ``continuized'' Nesterov acceleration, a close variant of Nesterov acceleration whose variables are indexed by a continuous time parameter. The two variables continuously mix following a linear ordinary differential equation and take gradient steps at random times. This continuized variant benefits from the best of the continuous and the discrete frameworks: as a continuous process, one can use differential calculus to analyze convergence and obtain analytical expressions for the parameters; but a discretization of the continuized process can be computed exactly with convergence rates similar to those of Nesterov original acceleration. We show that the discretization has the same structure as Nesterov acceleration, but with random parameters. We provide continuized Nesterov acceleration under deterministic as well as stochastic gradients, with either additive or multiplicative noise. Finally, using our continuized framework and expressing the gossip averaging problem as the stochastic minimization of a certain energy function, we provide the first rigorous acceleration of asynchronous gossip algorithms.|
|Outstanding Paper|On the Expressivity of Markov Reward David Abel · Will Dabney · Anna Harutyunyan · Mark Ho · Michael Littman · Doina Precup · Satinder Singh Abstract Reward is the driving force for reinforcement-learning agents. This paper is dedicated to understanding the expressivity of reward as a way to capture tasks that we would want an agent to perform. We frame this study around three new abstract notions of “task” that might be desirable: (1) a set of acceptable behaviors, (2) a partial ordering over behaviors, or (3) a partial ordering over trajectories. Our main results prove that while reward can express many of these tasks, there exist instances of each task type that no Markov reward function can capture. We then provide a set of polynomial-time algorithms that construct a Markov reward function that allows an agent to optimize tasks of each of these three types, and correctly determine when no such reward function exists. We conclude with an empirical study that corroborates and illustrates our theoretical findings.|
|Outstanding Paper|Moser Flow: Divergence-based Generative Modeling on Manifolds Noam Rozen · Aditya Grover · Maximilian Nickel · Yaron Lipman Abstract We are interested in learning generative models for complex geometries described via manifolds, such as spheres, tori, and other implicit surfaces. Current extensions of existing (Euclidean) generative models are restricted to specific geometries and typically suffer from high computational costs. We introduce Moser Flow (MF), a new class of generative models within the family of continuous normalizing flows (CNF). MF also produces a CNF via a solution to the change-of-variable formula, however differently from other CNF methods, its model (learned) density is parameterized as the source (prior) density minus the divergence of a neural network (NN). The divergence is a local, linear differential operator, easy to approximate and calculate on manifolds. Therefore, unlike other CNFs, MF does not require invoking or backpropagating through an ODE solver during training. Furthermore, representing the model density explicitly as the divergence of a NN rather than as a solution of an ODE facilitates learning high fidelity densities. Theoretically, we prove that MF constitutes a universal density approximator under suitable assumptions. Empirically, we demonstrate for the first time the use of flow models for sampling from general curved surfaces and achieve significant improvements in density estimation, sample quality, and training complexity over existing CNFs on …|
|Outstanding Paper|On the Expressivity of Markov Reward David Abel · Will Dabney · Anna Harutyunyan · Mark Ho · Michael Littman · Doina Precup · Satinder Singh Abstract Reward is the driving force for reinforcement-learning agents. This paper is dedicated to understanding the expressivity of reward as a way to capture tasks that we would want an agent to perform. We frame this study around three new abstract notions of “task” that might be desirable: (1) a set of acceptable behaviors, (2) a partial ordering over behaviors, or (3) a partial ordering over trajectories. Our main results prove that while reward can express many of these tasks, there exist instances of each task type that no Markov reward function can capture. We then provide a set of polynomial-time algorithms that construct a Markov reward function that allows an agent to optimize tasks of each of these three types, and correctly determine when no such reward function exists. We conclude with an empirical study that corroborates and illustrates our theoretical findings.|
|Outstanding Paper|A Universal Law of Robustness via Isoperimetry Sebastien Bubeck · Mark Sellke [ Virtual ] Abstract Classically, data interpolation with a parametrized model class is possible as long as the number of parameters is larger than the number of equations to be satisfied. A puzzling phenomenon in the current practice of deep learning is that models are trained with many more parameters than what this classical theory would suggest. We propose a theoretical explanation for this phenomenon. We prove that for a broad class of data distributions and model classes, overparametrization is {\em necessary} if one wants to interpolate the data {\em smoothly}. Namely we show that {\em smooth} interpolation requires $d$ times more parameters than mere interpolation, where $d$ is the ambient data dimension. We prove this universal law of robustness for any smoothly parametrized function class with polynomial size weights, and any covariate distribution verifying isoperimetry. In the case of two-layers neural networks and Gaussian covariates, this law was conjectured in prior work by Bubeck, Li and Nagaraj. We also give an interpretation of our result as an improved generalization bound for model classes consisting of smooth functions.|
|Outstanding Paper|Continuized Accelerations of Deterministic and Stochastic Gradient Descents, and of Gossip Algorithms Mathieu Even · Raphaël Berthier · Francis Bach · Nicolas Flammarion · Hadrien Hendrikx · Pierre Gaillard · Laurent Massoulié · Adrien Taylor Abstract We introduce the ``continuized'' Nesterov acceleration, a close variant of Nesterov acceleration whose variables are indexed by a continuous time parameter. The two variables continuously mix following a linear ordinary differential equation and take gradient steps at random times. This continuized variant benefits from the best of the continuous and the discrete frameworks: as a continuous process, one can use differential calculus to analyze convergence and obtain analytical expressions for the parameters; but a discretization of the continuized process can be computed exactly with convergence rates similar to those of Nesterov original acceleration. We show that the discretization has the same structure as Nesterov acceleration, but with random parameters. We provide continuized Nesterov acceleration under deterministic as well as stochastic gradients, with either additive or multiplicative noise. Finally, using our continuized framework and expressing the gossip averaging problem as the stochastic minimization of a certain energy function, we provide the first rigorous acceleration of asynchronous gossip algorithms.|
|Outstanding Paper|Moser Flow: Divergence-based Generative Modeling on Manifolds Noam Rozen · Aditya Grover · Maximilian Nickel · Yaron Lipman Abstract We are interested in learning generative models for complex geometries described via manifolds, such as spheres, tori, and other implicit surfaces. Current extensions of existing (Euclidean) generative models are restricted to specific geometries and typically suffer from high computational costs. We introduce Moser Flow (MF), a new class of generative models within the family of continuous normalizing flows (CNF). MF also produces a CNF via a solution to the change-of-variable formula, however differently from other CNF methods, its model (learned) density is parameterized as the source (prior) density minus the divergence of a neural network (NN). The divergence is a local, linear differential operator, easy to approximate and calculate on manifolds. Therefore, unlike other CNFs, MF does not require invoking or backpropagating through an ODE solver during training. Furthermore, representing the model density explicitly as the divergence of a NN rather than as a solution of an ODE facilitates learning high fidelity densities. Theoretically, we prove that MF constitutes a universal density approximator under suitable assumptions. Empirically, we demonstrate for the first time the use of flow models for sampling from general curved surfaces and achieve significant improvements in density estimation, sample quality, and training complexity over existing CNFs on …|
|Outstanding Paper|Deep Reinforcement Learning at the Edge of the Statistical Precipice Rishabh Agarwal · Max Schwarzer · Pablo Samuel Castro · Aaron Courville · Marc Bellemare [ Virtual ] Abstract Deep reinforcement learning (RL) algorithms are predominantly evaluated by comparing their relative performance on a large suite of tasks. Most published results on deep RL benchmarks compare point estimates of aggregate performance such as mean and median scores across tasks, ignoring the statistical uncertainty implied by the use of a finite number of training runs. Beginning with the Arcade Learning Environment (ALE), the shift towards computationally-demanding benchmarks has led to the practice of evaluating only a small number of runs per task, exacerbating the statistical uncertainty in point estimates. In this paper, we argue that reliable evaluation in the few run deep RL regime cannot ignore the uncertainty in results without running the risk of slowing down progress in the field. We illustrate this point using a case study on the Atari 100k benchmark, where we find substantial discrepancies between conclusions drawn from point estimates alone versus a more thorough statistical analysis. With the aim of increasing the field's confidence in reported results with a handful of runs, we advocate for reporting interval estimates of aggregate performance and propose performance profiles to account for the variability in results, as well as present more robust and efficient aggregate metrics, such as …|
|Outstanding Paper|MAUVE: Measuring the Gap Between Neural Text and Human Text using Divergence Frontiers Krishna Pillutla · Swabha Swayamdipta · Rowan Zellers · John Thickstun · Sean Welleck · Yejin Choi · Zaid Harchaoui Abstract As major progress is made in open-ended text generation, measuring how close machine-generated text is to human language remains a critical open problem. We introduce Mauve, a comparison measure for open-ended text generation, which directly compares the learnt distribution from a text generation model to the distribution of human-written text using divergence frontiers. Mauve scales up to modern text generation models by computing information divergences in a quantized embedding space. Through an extensive empirical study on three open-ended generation tasks, we find that Mauve identifies known properties of generated text, scales naturally with model size, and correlates with human judgments, with fewer restrictions than existing distributional evaluation metrics.|
|Outstanding Paper|Deep Reinforcement Learning at the Edge of the Statistical Precipice Rishabh Agarwal · Max Schwarzer · Pablo Samuel Castro · Aaron Courville · Marc Bellemare Abstract Deep reinforcement learning (RL) algorithms are predominantly evaluated by comparing their relative performance on a large suite of tasks. Most published results on deep RL benchmarks compare point estimates of aggregate performance such as mean and median scores across tasks, ignoring the statistical uncertainty implied by the use of a finite number of training runs. Beginning with the Arcade Learning Environment (ALE), the shift towards computationally-demanding benchmarks has led to the practice of evaluating only a small number of runs per task, exacerbating the statistical uncertainty in point estimates. In this paper, we argue that reliable evaluation in the few run deep RL regime cannot ignore the uncertainty in results without running the risk of slowing down progress in the field. We illustrate this point using a case study on the Atari 100k benchmark, where we find substantial discrepancies between conclusions drawn from point estimates alone versus a more thorough statistical analysis. With the aim of increasing the field's confidence in reported results with a handful of runs, we advocate for reporting interval estimates of aggregate performance and propose performance profiles to account for the variability in results, as well as present more robust and efficient aggregate metrics, such as …|
|Datasets and Benchmarks Award|ATOM3D: Tasks on Molecules in Three Dimensions Raphael Townshend · Martin Vögele · Patricia Suriana · Alex Derry · Alexander Powers · Yianni Laloudakis · Sidhika Balachandar · Bowen Jing · Brandon Anderson · Stephan Eismann · Risi Kondor · Russ Altman · Ron Dror Abstract Computational methods that operate on three-dimensional (3D) molecular structure have the potential to solve important problems in biology and chemistry. Deep neural networks have gained significant attention, but their widespread adoption in the biomolecular domain has been limited by a lack of either systematic performance benchmarks or a unified toolkit for interacting with 3D molecular data. To address this, we present ATOM3D, a collection of both novel and existing benchmark datasets spanning several key classes of biomolecules. We implement several types of 3D molecular learning methods for each of these tasks and show that they consistently improve performance relative to methods based on one- and two-dimensional representations. The choice of architecture proves to be important for performance, with 3D convolutional networks excelling at tasks involving complex geometries, graph networks performing well on systems requiring detailed positional information, and the more recently developed equivariant networks showing significant promise. Our results indicate that many molecular problems stand to gain from 3D molecular learning, and that there is potential for substantial further improvement on many tasks. To lower the barrier to entry and facilitate further developments in the field, we also provide a comprehensive suite of tools for dataset processing, model training, and …|
|Datasets and Benchmarks Award|Reduced, Reused and Recycled: The Life of a Dataset in Machine Learning Research Bernard Koch · Emily Denton · Alex Hanna · Jacob G Foster Abstract Benchmark datasets play a central role in the organization of machine learning research. They coordinate researchers around shared research problems and serve as a measure of progress towards shared goals. Despite the foundational role of benchmarking practices in this field, relatively little attention has been paid to the dynamics of benchmark dataset use and reuse, within or across machine learning subcommunities. In this paper, we dig into these dynamics. We study how dataset usage patterns differ across machine learning subcommunities and across time from 2015-2020. We find increasing concentration on fewer and fewer datasets within task communities, significant adoption of datasets from other tasks, and concentration across the field on datasets that have been introduced by researchers situated within a small number of elite institutions. Our results have implications for scientific evaluation, AI ethics, and equity/access within the field.|