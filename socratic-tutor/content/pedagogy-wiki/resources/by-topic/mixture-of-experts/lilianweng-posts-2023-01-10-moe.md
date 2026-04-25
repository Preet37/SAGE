# Source: https://lilianweng.github.io/posts/2023-01-10-moe/
# Fetched via: search fallback (Perplexity)
# Downloaded: 2026-04-09
# Words: 2318
# Author: Lilian Weng
# Author Slug: lilian-weng
**Mixture of experts** (**MoE**) is a machine learning technique where multiple expert networks (learners) are used to divide a problem space into homogeneous regions.
MoE represents a form of ensemble learning.
They were also called **committee machines**.
## Basic theory
MoE always has the following components, but they are implemented and combined differently according to the problem being solved:
- **Experts** \( f_{1},...,f_{n} \), each taking the same input \( x \), and producing outputs \( f_{1}(x),...,f_{n}(x) \).
- A **weighting function** (also known as a **gating function**) \( w \), which takes input \( x \) and produces a vector of outputs \( (w(x)_{1},...,w(x)_{n}) \).
This may or may not be a probability distribution, but in both cases, its entries are non-negative.
- \( \theta =(\theta _{0},\theta _{1},...,\theta _{n}) \) is the set of parameters.
The parameter \( \theta _{0} \) is for the weighting function.
The parameters \( \theta _{1},\dots ,\theta _{n} \) are for the experts.
- Given an input \( x \), the **mixture of experts** produces a single output by combining \( f_{1}(x),...,f_{n}(x) \) according to the weights \( w(x)_{1},...,w(x)_{n} \) in some way, usually by \( f(x)=\sum _{i}w(x)_{i}f_{i}(x) \).
…
### Meta-pi network
The **meta-pi network**, reported by Hampshire and Waibel, uses \( f(x)=\sum _{i}w(x)_{i}f_{i}(x) \) as the output.
The model is trained by performing gradient descent on the mean-squared error loss \( L:={\frac {1}{N}}\sum _{k}\|y_{k}-f(x_{k})\|^{2} \).
The experts may be arbitrary functions.
...
For example, a 2-level hierarchical MoE would have a first order gating function \( w_{i} \), and second order gating functions \( w_{j|i} \) and experts \( f_{j|i} \).
The total prediction is then \( \sum _{i}w_{i}(x)\sum _{j}w_{j|i}(x)f_{j|i}(x) \).
…
The choice of gating function is often softmax.
Other than that, gating may use gaussian distributions and exponential families.
Instead of performing a weighted sum of all the experts, in hard MoE, only the highest ranked expert is chosen.
That is, \( f(x)=f_{\arg \max _{i}w_{i}(x)}(x) \).
This can accelerate training and inference time.
…
...
Specifically, each gating is a linear-ReLU-linear-softmax network, and each expert is a linear-ReLU network.
Since the output from the gating is not sparse, all expert outputs are needed, and no conditional computation is performed.
The key goal when using MoE in deep learning is to reduce computing cost.
Consequently, for each query, only a small subset of the experts should be queried.
This makes MoE in deep learning different from classical MoE.
In classical MoE, the output for each query is a weighted sum of *all* experts' outputs.
In deep learning MoE, the output for each query can only involve a few experts' outputs.
Consequently, the key design choice in MoE becomes routing: given a batch of queries, how to route the queries to the best experts.
...
Specifically, in a MoE layer, there are feedforward networks \( f_{1},...,f_{n} \), and a gating network \( w \).
The gating network is defined by \( w(x)=\mathrm {softmax} (\mathrm {top} _{k}(Wx+{\text{noise}})) \), where \( \mathrm {top} _{k} \) is a function that keeps the top-k entries of a vector the same, but sets all other entries to \( -\infty \).
The addition of noise helps with load balancing.
The choice of \( k \) is a hyperparameter that is chosen according to application.
Typical values are \( k=1,2 \).
...
They are typically sparsely-gated, with sparsity 1 or 2.

## What is mixture of experts?
Mixture of experts (MoE) is a machine learning approach that divides an artificial intelligence (AI) model into separate sub-networks (or “experts”), each specializing in a subset of the input data, to jointly perform a task.
Mixture of Experts architectures enable large-scale models, even those comprising many billions of parameters, to greatly reduce computation costs during pre-training and achieve faster performance during inference time.
Broadly speaking, it achieves this efficiency through selectively activating only the specific experts needed for a given task, rather than activating the entire neural network for every task.
Though much of the modern implementation of mixture of experts setups was developed over (roughly) the past decade, the core premise behind MoE models originates from the 1991 paper “Adaptive Mixture of Local Experts.”
The paper proposed training an AI system composed of separate networks that each specialized in a different subset of training cases.
This entailed training both the “expert networks” themselves and a *gating network* that determines which expert should be used for each subtask.
...
In recent years, as the leading deep learning models used for generative AI have grown increasingly large and computationally demanding, mixture of experts offer a means to address the tradeoff between the greater capacity of larger models and the greater efficiency of smaller models.
This has been most notably explored in the field of natural language processing (NLP): some leading large language models (LLMs) like Mistral’s Mixtral 8x7B and (according to some reports) OpenAI’s GPT-4,^2^ have employed MoE architecture.
…
Unlike conventional dense models, mixture of experts uses *conditional computation* to enforce sparsity: rather than using the entire network for every input, MoE models learn a computationally cheap mapping function that determines which portions of the network—in other words, which experts—are most effective to process a given input, like an individual *token* used to represent a word or word fragment in NLP tasks.
…
## How do mixture of experts models work?
MoE models process data by designating a number of “*experts*,” each its own sub-network within a larger neural network, and training a *gating network* (or *router*) to activate only the specific expert(s) best suited to a given input.
The primary benefit of the MoE approach is that by enforcing *sparsity*, rather than activating the entire neural network for each input token, model capacity can be increased while essentially keeping computational costs constant.
On an architectural level, this is achieved by replacing traditional, dense feed-forward network (FFN) layers with sparse MoE layers (or *blocks*).
In the parlance of neural networks, “block” refers to a recurring structural element that performs a specific function.
In a sparse MoE model (SMoE), these expert blocks can be single layers, self-contained FFNs or even nested MoEs unto themselves.
For example, in Mistral’s *Mixtral 8x7B* language model, each layer is composed of 8 feedforward blocks—that is, experts—each of which has 7 billion parameters.
For every token, at each layer, a router network selects two of those eight experts to process the data.
It then combines the outputs of those two experts and passes the result to the following layer.
The specific experts selected by the router at a given layer may be different experts from those selected at the previous or next layer.^3^
...
This overall parameter count is commonly referenced as the *sparse parameter count* and can generally be understood as a measure of model capacity.
The number of parameters that will actually be used to process an individual token (as it transits through some expert blocks and bypasses others) is called the *active parameter count*, and can be understood as a measure of the model’s computational costs.
Though each token input to Mixtral has access to 46.7 billion parameters, only 12.9 billion active parameters are used to process a given example.
...
Key to the concept (and efficiency) of MoEs is that only some of the experts (and therefore parameters) in a sparse layer will be activated at any given time, thereby reducing active computational requirements.
...
This sparsity is achieved through conditional computation: the dynamic activation of specific parameters in response to specific inputs.
The effective design of the gating network (or “router”), which enforces that conditional computation, is thus essential to the success of MoE models.
…
A typical gating mechanism in a traditional MoE setup, introduced in Shazeer’s seminal paper, uses the *softmax* function: for each of the experts, on a per-example basis, the router predicts a probability value (based on the weights of that expert’s connections to the current parameter) of that expert yielding the best output for a given input; rather than computing the output of all the experts, the router computes only the output of (what it predicts to be) the top *k* experts for that example.
…
...
- Fine-tuning only Attention parameters resulted in a minor decrease in performance.
- Updating only the MoE parameters significantly *degraded* model performance, despite the fact that roughly 80% of model parameters resided in the sparse MoE layers.
- FFN was the only approach that improved performance relative to the All baseline.
...
A July 2023 paper, “Mixture-of-Experts Meets Instruction Tuning,” explored the impact of instruction tuning on MoE models using equivalents of Google’s T5 and Flan-T5—a version of T5 instruction-tuned with Google’s Flan protocol —LLMs as a baseline.
Their experiment compared four setups: fine-tuning a dense T5 model, fine-tuning a dense Flan-T5 model, fine-tuning an MoE model and fine-tuning an instruction-tuned Flan-MoE model.

The world of Large Language Models (LLMs) is in a constant state of evolution.
We're witnessing a rapid
increase in model size, with parameter counts reaching into the trillions.
However, training and running
these massive "dense" models, where every parameter is used for every input, is becoming increasingly
unsustainable.
Enter the
**Mixture of Experts (MoE)** architecture, a paradigm shift that
promises to deliver the power of enormous models with a fraction of the computational cost.
In this deep dive, we'll explore the ins and outs of MoEs, from their fundamental architecture to the latest cutting-edge techniques used in models like DeepSeek and Mixtral.
We'll be drawing on insights from a recent lecture on MoEs and the excellent Hugging Face blog post on the topic to provide a comprehensive technical overview.
🔗 Open in Colab - Try the Mixture of Experts demo notebook
## What is a Mixture of Experts (MoE)?
At its core, an MoE is a neural network architecture that employs a "divide and conquer" strategy.
Instead of a single, monolithic model that processes all data, an MoE is comprised of numerous smaller, specialized sub-networks called "experts".
For any given input, a "gating network" or "router" dynamically selects which experts are best suited to handle the task.
In the context of Transformer models, which form the backbone of most modern LLMs, MoE layers are used to replace the dense feed-forward network (FFN) layers.
While the other components of the Transformer (like the self-attention mechanism) remain shared, the FFNs are split into multiple experts.
This means that for any given token, only a fraction of the model's total parameters are activated, leading to a significant reduction in computational cost.
This sparse activation is the key to the efficiency of MoEs.
It allows for the creation of models with a massive number of parameters, but with a computational cost (measured in FLOPs) that's comparable to a much smaller dense model.
…
**Faster Training:**MoEs can be trained significantly faster than their dense counterparts.
For a given computational budget, you can either train a larger MoE model or train a model on a larger dataset.
The charts below from the OIMOE paper show a 7x speedup in training time to reach the same performance as a dense model.
**Better Performance for the Same FLOPs:**With the same amount of computation, a sparse MoE model can achieve better performance than a dense model.
This is because the MoE can have a much larger number of parameters, allowing it to learn a wider range of features and specialize its experts for different tasks.
...
Each expert can be placed on a different device (GPU/TPU), allowing for efficient scaling to large clusters of machines.
This "expert parallelism" is a key enabler for training massive MoE models.
...
The magic of MoEs lies in the
**routing mechanism**.
The router is responsible for deciding
which expert(s) each token should be sent to.
The most common approach is **"Top-K" routing"**,
where the router selects the top 'k' experts with the highest scores for a given token.
Let's break down the math of Top-K routing as presented on page 19 of the lecture notes.
For a given input token embedding \(u_t^l\) at layer \(l\), the process is as follows:
**Calculate Expert Scores:**A learnable weight matrix \(e_i^l\) (one for each expert \(i\)) is used to compute a score, \(s_{i,t}\), for each expert.
This score represents the affinity of the token for that expert.
The scores for all experts are then typically normalized using a Softmax function.
\[s_{i,t}=\text{Softmax}_{i}(u_{t}^{lT}e_{i}^{l})\] **Select Top-K Experts:**The router selects the \(K\) experts with the highest scores.
The gating value \(g_{i,t}\) is set to the expert's score \(s_{i,t}\) if it's in the top K, and zero otherwise.
\[g_{i,t}=\begin{cases}s_{i,t},& \text{if } s_{i,t} \in
\text{TopK}(\{s_{j,t}|1\le j\le N\},K) \\ 0, & \text{otherwise} \end{cases}\] *Note: Some modern models like Mixtral and DeepSeek v3 apply a second Softmax to the gating values* **after**the Top-K selection to re-normalize the weights among the chosen experts.
**Compute Final Output:**The output of the MoE layer, \(h_t^l\), is a weighted sum of the outputs of the selected experts, combined with the original input via a residual connection.
\[h_{t}^{l}=\sum_{i=1}^{N}(g_{i,t} \cdot \text{FFN}_{i}(u_{t}^{l}))+u_{t}^{l}\]
Most modern MoEs use k=2 or k=4.
For example, Mixtral uses Top-2 routing, while DBRX uses Top-4.
...
The formulation used in the Switch Transformer is a popular choice.
The loss is the scaled dot-product between the fraction of tokens dispatched to each expert (\(f_i\)) and the fraction of the router's probability mass allocated to each expert (\(P_i\)).\[\text{loss}_{\text{aux}}=\alpha \cdot N \cdot\sum_{i=1}^{N}f_{i}\cdot P_{i}\]
Where:
- \(N\) is the number of experts.
- \(\alpha\) is a hyperparameter to scale the loss.
- \(f_{i}\) is the fraction of tokens in a batch dispatched to expert \(i\): \(f_{i}=\frac{1}{T}\sum_{x\in\mathcal{B}}\mathbb{I}\{\text{argmax } p(x)=i\}\).
- \(P_{i}\) is the average router probability for expert \(i\) over the batch: \(P_{i}=\frac{1}{T}\sum_{x\in\mathcal{B}}p_{i}(x)\).
...
This loss penalizes the squared log of the sum of the exponentials of the router logits, which helps keep the logits small and manageable.\[L_{z}(x)=\frac{1}{B}\sum_{i=1}^{B}(\log\sum_{j=1}^{N}e^{x_{j}})^{2}\]

1. I Introduction and Fundamentals
2. II Core Architectures and Routing Mechanisms 1. II-A Foundational MoE Architectures
   2. II-B Advanced Architectural