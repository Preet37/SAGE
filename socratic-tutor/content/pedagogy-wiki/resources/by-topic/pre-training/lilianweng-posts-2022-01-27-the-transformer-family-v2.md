# Source: https://lilianweng.github.io/posts/2022-01-27-the-transformer-family-v2/
# Author: Lilian Weng
# Author Slug: lilian-weng
# Fetched via: search fallback (Perplexity)
# Downloaded: 2026-04-06
# Words: 2183
Many new Transformer architecture improvements have been proposed since my last post on about three years ago. Here I did a big refactoring and enrichment of that 2020 post — restructure the hierarchy of sections and improve many sections with more recent papers. Version 2.0 is a superset of the old version, about twice the length.

# Notations
|Symbol|Meaning|
|--|--|
|$d$|The model size / hidden state dimension / positional encoding size.|
|$h$|The number of heads in multi-head attention layer.|
|$L$|The segment length of input sequence.|
|$N$|The total number of attention layers in the model; not considering MoE.|
|$\mathbf{X} \in \mathbb{R}^{L \times d}$|The input sequence where each element has been mapped into an embedding vector of shape $d$, same as the model size.|
|$\mathbf{W}^k \in \mathbb{R}^{d \times d_k}$|The key weight matrix.|
|$\mathbf{W}^q \in \mathbb{R}^{d \times d_k}$|The query weight matrix.|
|$\mathbf{W}^v \in \mathbb{R}^{d \times d_v}$|The value weight matrix. Often we have $d_k = d_v = d$.|
|$\mathbf{W}^k_i, \mathbf{W}^q_i \in \mathbb{R}^{d \times d_k/h}; \mathbf{W}^v_i \in \mathbb{R}^{d \times d_v/h}$|The weight matrices per head.|
|$\mathbf{W}^o \in \mathbb{R}^{d_v \times d}$|The output weight matrix.|
|$\mathbf{Q} = \mathbf{X}\mathbf{W}^q \in \mathbb{R}^{L \times d_k}$|The query embedding inputs.|
|$\mathbf{K} = \mathbf{X}\mathbf{W}^k \in \mathbb{R}^{L \times d_k}$|The key embedding inputs.|
|$\mathbf{V} = \mathbf{X}\mathbf{W}^v \in \mathbb{R}^{L \times d_v}$|The value embedding inputs.|
|$\mathbf{q}_i, \mathbf{k}_i \in \mathbb{R}^{d_k}, \mathbf{v}_i \in \mathbb{R}^{d_v}$|Row vectors in query, key, value matrices, $\mathbf{Q}$, $\mathbf{K}$ and $\mathbf{V}$.|
|$S_i$|A collection of key positions for the $i$-th query $\mathbf{q}_i$ to attend to.|

…

# Transformer Basics

The **Transformer** (which will be referred to as “vanilla Transformer” to distinguish it from other enhanced versions; Vaswani, et al., 2017) model has an encoder-decoder architecture, as commonly used in many NMT models. Later simplified Transformer was shown to achieve great performance in language modeling tasks, like in encoder-only BERT or decoder-only GPT.

…

## Multi-Head Self-Attention

The **multi-head self-attention** module is a key component in Transformer. Rather than only computing the attention once, the multi-head mechanism splits the inputs into smaller chunks and then computes the scaled dot-product attention over each subspace in parallel. The independent attention outputs are simply concatenated and linearly transformed into expected dimensions.

…

where $[.;.]$ is a concatenation operation. $\mathbf{W}^q_i, \mathbf{W}^k_i \in \mathbb{R}^{d \times d_k/h}, \mathbf{W}^v_i \in \mathbb{R}^{d \times d_v/h}$ are weight matrices to map input embeddings of size $L \times d$ into query, key and value matrices. And $\mathbf{W}^o \in \mathbb{R}^{d_v \times d}$ is the output linear transformation. All the weights should be learned during training.

## Encoder-Decoder Architecture

The **encoder** generates an attention-based representation with capability to locate a specific piece of information from a large context. It consists of a stack of 6 identity modules, each containing two submodules, a *multi-head self-attention* layer and a *point-wise* fully connected feed-forward network. By point-wise, it means that it applies the same linear transformation (with same weights) to each element in the sequence. This can also be viewed as a convolutional layer with filter size 1. Each submodule has a residual connection and layer normalization. All the submodules output data of the same dimension $d$.
The function of Transformer **decoder** is to retrieve information from the encoded representation. The architecture is quite similar to the encoder, except that the decoder contains two multi-head attention submodules instead of one in each identical repeating module. The first multi-head attention submodule is *masked* to prevent positions from attending to the future.

## Positional Encoding

Because self-attention operation is permutation invariant, it is important to use proper **positional encoding** to provide *order information* to the model. The positional encoding $\mathbf{P} \in \mathbb{R}^{L \times d}$ has the same dimension as the input embedding, so it can be added on the input directly. The vanilla Transformer considered two types of encodings:

…

\text{PE}(i,\delta) =
\begin{cases}
\sin(\frac{i}{10000^{2\delta'/d}}) & \text{if } \delta = 2\delta'\\
\cos(\frac{i}{10000^{2\delta'/d}}) & \text{if } \delta = 2\delta' + 1\\
\end{cases}
$$

In this way each dimension of the positional encoding corresponds to a sinusoid of different wavelengths in different dimensions, from $2\pi$ to $10000 \cdot 2\pi$.

### Learned Positional Encoding

Learned positional encoding assigns each element with a *learned* column vector which encodes its absolute position (Gehring, et al. 2017) and furthermroe this encoding can be learned differently per layer (Al-Rfou et al. 2018).

### Relative Position Encoding

Shaw et al. (2018)) incorporated relative positional information into $\mathbf{W}^k$ and $\mathbf{W}^v$. Maximum relative position is clipped to a maximum absolute value of $k$ and this clipping operation enables the model to generalize to unseen sequence lengths. Therefore, $2k + 1$ unique edge labels are considered and let us denote $\mathbf{P}^k, \mathbf{P}^v \in \mathbb{R}^{2k+1}$ as learnable relative position representations.

…

$$

Transformer-XL reparameterizes the above four terms as follows:

$$

…

$$

- Replace $\mathbf{p}_j$ with relative positional encoding $\mathbf{r}_{i-j} \in \mathbf{R}^{d}$;
- Replace $\mathbf{p}_i\mathbf{W}^q$ with two trainable parameters $\mathbf{u}$ (for content) and $\mathbf{v}$ (for location) in two different terms;
- Split $\mathbf{W}^k$ into two matrices, $\mathbf{W}^k_E$ for content information and $\mathbf{W}^k_R$ for location information.

### Rotary Position Embedding

Rotary position embedding (*RoPE*; Su et al. 2021) encodes the absolution position with a rotation matrix and multiplies key and value matrices of every attention layer with it to inject relative positional information at every layer.
When encoding relative positional information into the inner product of the $i$-th key and the $j$-th query, we would like to formulate the function in a way that the inner product is only about the relative position $i-j$. Rotary Position Embedding (RoPE) makes use of the rotation operation in Euclidean space and frames the relative position embedding as simply rotating feature matrix by an angle proportional to its position index.

…

R = \begin{bmatrix}
\cos\theta & -\sin\theta \\
\sin\theta & \cos\theta
\end{bmatrix}
$$

When generalizing to higher dimensional space, RoPE divide the $d$-dimensional space into $d/2$ subspaces and constructs a rotation matrix $R$ of size $d \times d$ for token at position $i$:

$$
R^d_{\Theta, i} = \begin{bmatrix}
\cos i\theta_1 & -\sin i\theta_1 & 0 & 0 & \dots & 0 & 0 \\
\sin i\theta_1 & \cos i\theta_1 & 0 & 0 & \dots & 0 & 0 \\
0 & 0 & \cos i\theta_2 & -\sin i\theta_2 & \dots & 0 & 0 \\
0 & 0 & \sin i\theta_2 & \cos i\theta_2 & \dots & 0 & 0 \\
\vdots & \vdots & \vdots & \vdots & \ddots & \vdots & \vdots \\
0 & 0 & 0 & 0 & \dots & \cos i\theta_{d/2} & -\sin i\theta_{d/2} \\
0 & 0 & 0 & 0 & \dots & \sin i\theta_{d/2} & \cos i\theta_{d/2} \\
\end{bmatrix}
$$

where in the paper we have $\Theta = {\theta_i = 10000^{-2(i−1)/d}, i \in [1, 2, …, d/2]}$. Note that this is essentially equivalent to sinusoidal positional encoding but formulated as a rotation matrix.

Then both key and query matrices incorporates the positional information by multiplying with this rotation matrix:

…

\begin{aligned}
& \mathbf{q}_i^\top \mathbf{k}_j = (R^d_{\Theta, i} \mathbf{W}^q\mathbf{x}_i)^\top (R^d_{\Theta, j} \mathbf{W}^k\mathbf{x}_j) = \mathbf{x}_i^\top\mathbf{W}^q R^d_{\Theta, j-i}\mathbf{W}^k\mathbf{x}_j \\
& \text{ where } R^d_{\Theta, j-i} = (R^d_{\Theta, i})^\top R^d_{\Theta, j}
\end{aligned}

…

This section introduces several improvements in transformer architecture to better support long context at inference; E.g. using additional memory, design for better context extrapolation, or recurrency mechanism.

## Context Memory

The vanilla Transformer has a fixed and limited attention span. The model can only attend to other elements in the same segments during each update step and no information can flow across separated fixed-length segments. This *context segmentation* causes several issues:

- The model cannot capture very long term dependencies.
- It is hard to predict the first few tokens in each segment given no or thin context.
- The evaluation is expensive. Whenever the segment is shifted to the right by one, the new segment is re-processed from scratch, although there are a lot of overlapped tokens.

…

$$

Note that both keys and values rely on extended hidden states, while queries only consume hidden states at the current step. The concatenation operation $[. \circ .]$ is along the sequence length dimension. And Transformer-XL needs to use relative positional encoding because previous and current segments would be assigned with the same encoding if we encode absolute positions, which is undesired.
**Compressive Transformer** (Rae et al. 2019) extends Transformer-XL by compressing past memories to support longer sequences. It explicitly adds *memory* slots of size $m_m$ per layer for storing past activations of this layer to preserve long context. When some past activations become old enough, they are compressed and saved in an additional *compressed memory* of size $m_{cm}$ per layer.

…

This datastore is preprocessed to save a *large* number of pairs, (LM embedding representation of context, next token) and the nearest neighbor retrieval happens in the LM embedding space. Because the datastore can be gigantic, we need to rely on libraries for fast dense vector search such as FAISS or ScaNN. The indexing process only happens once and parallelism is easy to implement at inference time.

…

During training, the key representations in the long-term memory stay constant, produced by a pretrained LM, but the value encoder, aka the word embedding matrix, gets updated.

**Memorizing Transformer** (Wu et al. 2022) adds a $k$NN-augmented attention layer near the top stack of a decoder-only Transformer. This special layer maintains a Transformer-XL style FIFO cache of past key-value pairs.

…

On a high level, the universal transformer can be viewed as a recurrent function for learning the hidden state representation per token. The recurrent function evolves in parallel across token positions and the information between positions is shared through self-attention.
Given an input sequence of length $L$, Universal Transformer iteratively updates the representation $\mathbf{h}^t \in \mathbb{R}^{L \times d}$ at step $t$ for an adjustable number of steps. At step 0, $\mathbf{h}^0$ is initialized to be same as the input embedding matrix. All the positions are processed in parallel in the multi-head self-attention mechanism and then go through a recurrent transition function.

…

$$

where $\text{Transition}(.)$ is either a separable convolution or a fully-connected neural network that consists of two position-wise (i.e. applied to each row of $\mathbf{A}^t$ individually) affine transformation + one ReLU.

The positional encoding $\mathbf{P}^t$ uses sinusoidal position signal but with an additional time dimension:

…

$$

In the adaptive version of Universal Transformer, the number of recurrent steps $T$ is dynamically determined by ACT. Each position is equipped with a dynamic ACT halting mechanism. Once a per-token recurrent block halts, it stops taking more recurrent updates but simply copies the current value to the next step until all the blocks halt or until the model reaches a maximum step limit.

…

## Adaptive Attention Span

One key advantage of Transformer is the capability of capturing long-term dependencies. Depending on the context, the model may prefer to attend further sometime than others; or one attention head may had different attention pattern from the other. If the attention span could adapt its length flexibly and only attend further back when needed, it would help reduce both computation and memory cost to support longer maximum context size in the model.

…

$$

A *soft mask function* $m_z$ is added to control for an effective adjustable attention span, which maps the distance between query and key into a [0, 1] value. $m_z$ is parameterized by $z \in [0, s]$ and $z$ is to be learned:

…

1. *Sequence-specific depth classifier*: All tokens of the same sequence share the same exit block. It depends on the average of the encoder representation of the sequence. Given an input sequence $\mathbf{x}$ of length $L$, the classifier takes $\bar{\mathbf{x}} = \frac{1}{L} \sum_{t=1}^L \mathbf{x}_t$ as input and outputs a multinomial distribution of $N$ dimensions, corresponding to $N$ layers.

   $$

…

$$

   where $\delta$ is dirac delta (unit impulse) function and $-\lambda n$ is a regularization term to encourage lower layer exits. The ground truth $q^*$ can be prepared in two way, based on maximum likelihood $q_\text{lik}^*$ or correctness $q_\text{corr}^*$.
2. *Token-specific depth classifier (multinomial)*: Each token is decoded with different exit block, predicted conditioned on the first decoder hidden state $\mathbf{h}^1_t$:

…

\begin{aligned}
   \mathcal{X}^n_t &= \text{sigmoid}(\mathbf{w}_n^\top \mathbf{h}^n_t + b_n)\quad \forall n \in [1, \dots, N-1] \\
   q_t(n \vert \mathbf{x}, \mathbf{y}_{< t}) &= \begin{cases}
   \mathcal{X}^n_t \prod_{n' < n} (1 - \mathcal{X}^{n'}_t) & \text{if } n < N\\
   \prod_{n' < N} (1 - \mathcal{X}^{n'}_t) & \text{otherwise}
   \end{cases} \\
   q_\text{lik}^*(\mathbf{x}, \mathbf{y}) &= \delta(\arg\max_n \widetilde{\text{LL}}^n_t - \lambda n) \text{ where } \widetilde{\text{LL}}^n_t = \sum_{t'=1}^{\vert\mathbf{y}\vert}\kappa(t, t') LL^n_{t'} \\
   \text{or }q_\text{cor}^*(\mathbf{x}, \mathbf{y}) &= \delta(\arg\max_n \tilde{C}_t^n - \lambda n) \text{ where }C_t^n = \mathbb{1}[y_t = \arg\max_y p(y \vert \mathbf{h}^n_{t-1})],\; \tilde{C}^n_t = \sum_{t'=1}^{\vert\mathbf{y}\vert}\kappa(t, t') C^n_{t'} \\
   \end{aligned}

[Updated on **2023-01-27**: After almost three years, I did a big refactoring update of this post to incorporate a bunch of new Transformer models since 2020. The enhanced version of this post is here: **The Transformer Family Version 2.0**. Please refer to that post on this topic.]
It has been almost two years since my last post on attention. Recent progress on new and enhanced versions of Transformer motivates me to write another post on this specific topic, focusing on how the vanilla Transformer can be improved for longer-term attention span, less memory and computation consumption, RL