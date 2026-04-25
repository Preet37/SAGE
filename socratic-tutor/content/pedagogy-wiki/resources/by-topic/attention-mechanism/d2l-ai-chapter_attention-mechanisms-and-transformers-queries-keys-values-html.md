# Source: https://d2l.ai/chapter_attention-mechanisms-and-transformers/queries-keys-values.html
# Author: Dive into Deep Learning
# Author Slug: dive-into-deep-learning
# Title: 11.1. Queries, Keys, and Values - Dive into Deep Learning
# Fetched via: browser
# Date: 2026-04-08

11.1. Queries, Keys, and Values
 COLAB [PYTORCH]
Open the notebook in Colab
 SAGEMAKER STUDIO LAB
Open the notebook in SageMaker Studio Lab

So far all the networks we have reviewed crucially relied on the input being of a well-defined size. For instance, the images in ImageNet are of size 
224
×
224
 pixels and CNNs are specifically tuned to this size. Even in natural language processing the input size for RNNs is well defined and fixed. Variable size is addressed by sequentially processing one token at a time, or by specially designed convolution kernels (Kalchbrenner et al., 2014). This approach can lead to significant problems when the input is truly of varying size with varying information content, such as in Section 10.7 in the transformation of text (Sutskever et al., 2014). In particular, for long sequences it becomes quite difficult to keep track of everything that has already been generated or even viewed by the network. Even explicit tracking heuristics such as proposed by Yang et al. (2016) only offer limited benefit.

Compare this to databases. In their simplest form they are collections of keys (
𝑘
) and values (
𝑣
). For instance, our database 
𝐷
 might consist of tuples {(“Zhang”, “Aston”), (“Lipton”, “Zachary”), (“Li”, “Mu”), (“Smola”, “Alex”), (“Hu”, “Rachel”), (“Werness”, “Brent”)} with the last name being the key and the first name being the value. We can operate on 
𝐷
, for instance with the exact query (
𝑞
) for “Li” which would return the value “Mu”. If (“Li”, “Mu”) was not a record in 
𝐷
, there would be no valid answer. If we also allowed for approximate matches, we would retrieve (“Lipton”, “Zachary”) instead. This quite simple and trivial example nonetheless teaches us a number of useful things:

We can design queries 
𝑞
 that operate on (
𝑘
,
𝑣
) pairs in such a manner as to be valid regardless of the database size.

The same query can receive different answers, according to the contents of the database.

The “code” being executed for operating on a large state space (the database) can be quite simple (e.g., exact match, approximate match, top-
𝑘
).

There is no need to compress or simplify the database to make the operations effective.

Clearly we would not have introduced a simple database here if it wasn’t for the purpose of explaining deep learning. Indeed, this leads to one of the most exciting concepts introduced in deep learning in the past decade: the attention mechanism (Bahdanau et al., 2014). We will cover the specifics of its application to machine translation later. For now, simply consider the following: denote by 
𝐷
=
def
{
(
𝑘
1
,
𝑣
1
)
,
…
(
𝑘
𝑚
,
𝑣
𝑚
)
}
 a database of 
𝑚
 tuples of keys and values. Moreover, denote by 
𝑞
 a query. Then we can define the attention over 
𝐷
 as

(11.1.1)


Attention
(
𝑞
,
𝐷
)
=
def
∑
𝑖
=
1
𝑚
𝛼
(
𝑞
,
𝑘
𝑖
)
𝑣
𝑖
,

where 
𝛼
(
𝑞
,
𝑘
𝑖
)
∈
𝑅
 (
𝑖
=
1
,
…
,
𝑚
) are scalar attention weights. The operation itself is typically referred to as attention pooling. The name attention derives from the fact that the operation pays particular attention to the terms for which the weight 
𝛼
 is significant (i.e., large). As such, the attention over 
𝐷
 generates a linear combination of values contained in the database. In fact, this contains the above example as a special case where all but one weight is zero. We have a number of special cases:

The weights 
𝛼
(
𝑞
,
𝑘
𝑖
)
 are nonnegative. In this case the output of the attention mechanism is contained in the convex cone spanned by the values 
𝑣
𝑖
.

The weights 
𝛼
(
𝑞
,
𝑘
𝑖
)
 form a convex combination, i.e., 
∑
𝑖
𝛼
(
𝑞
,
𝑘
𝑖
)
=
1
 and 
𝛼
(
𝑞
,
𝑘
𝑖
)
≥
0
 for all 
𝑖
. This is the most common setting in deep learning.

Exactly one of the weights 
𝛼
(
𝑞
,
𝑘
𝑖
)
 is 
1
, while all others are 
0
. This is akin to a traditional database query.

All weights are equal, i.e., 
𝛼
(
𝑞
,
𝑘
𝑖
)
=
1
𝑚
 for all 
𝑖
. This amounts to averaging across the entire database, also called average pooling in deep learning.

A common strategy for ensuring that the weights sum up to 
1
 is to normalize them via

(11.1.2)
𝛼
(
𝑞
,
𝑘
𝑖
)
=
𝛼
(
𝑞
,
𝑘
𝑖
)
∑
𝑗
𝛼
(
𝑞
,
𝑘
𝑗
)
.

In particular, to ensure that the weights are also nonnegative, one can resort to exponentiation. This means that we can now pick any function 
𝑎
(
𝑞
,
𝑘
)
 and then apply the softmax operation used for multinomial models to it via

(11.1.3)
𝛼
(
𝑞
,
𝑘
𝑖
)
=
exp
⁡
(
𝑎
(
𝑞
,
𝑘
𝑖
)
)
∑
𝑗
exp
⁡
(
𝑎
(
𝑞
,
𝑘
𝑗
)
)
.

This operation is readily available in all deep learning frameworks. It is differentiable and its gradient never vanishes, all of which are desirable properties in a model. Note though, the attention mechanism introduced above is not the only option. For instance, we can design a non-differentiable attention model that can be trained using reinforcement learning methods (Mnih et al., 2014). As one would expect, training such a model is quite complex. Consequently the bulk of modern attention research follows the framework outlined in Fig. 11.1.1. We thus focus our exposition on this family of differentiable mechanisms.

Fig. 11.1.1 The attention mechanism computes a linear combination over values 
𝑣
𝑖
 via attention pooling, where weights are derived according to the compatibility between a query 
𝑞
 and keys 
𝑘
𝑖
.

What is quite remarkable is that the actual “code” for executing on the set of keys and values, namely the query, can be quite concise, even though the space to operate on is significant. This is a desirable property for a network layer as it does not require too many parameters to learn. Just as convenient is the fact that attention can operate on arbitrarily large databases without the need to change the way the attention pooling operation is performed.

PYTORCH
MXNET
JAX
TENSORFLOW
import torch
from d2l import torch as d2l

11.1.1. Visualization

One of the benefits of the attention mechanism is that it can be quite intuitive, particularly when the weights are nonnegative and sum to 
1
. In this case we might interpret large weights as a way for the model to select components of relevance. While this is a good intuition, it is important to remember that it is just that, an intuition. Regardless, we may want to visualize its effect on the given set of keys when applying a variety of different queries. This function will come in handy later.

We thus define the show_heatmaps function. Note that it does not take a matrix (of attention weights) as its input but rather a tensor with four axes, allowing for an array of different queries and weights. Consequently the input matrices has the shape (number of rows for display, number of columns for display, number of queries, number of keys). This will come in handy later on when we want to visualize the workings that are to design Transformers.

PYTORCH
MXNET
JAX
TENSORFLOW
#@save
def show_heatmaps(matrices, xlabel, ylabel, titles=None, figsize=(2.5, 2.5),
                  cmap='Reds'):
    """Show heatmaps of matrices."""
    d2l.use_svg_display()
    num_rows, num_cols, _, _ = matrices.shape
    fig, axes = d2l.plt.subplots(num_rows, num_cols, figsize=figsize,
                                 sharex=True, sharey=True, squeeze=False)
    for i, (row_axes, row_matrices) in enumerate(zip(axes, matrices)):
        for j, (ax, matrix) in enumerate(zip(row_axes, row_matrices)):
            pcm = ax.imshow(matrix.detach().numpy(), cmap=cmap)
            if i == num_rows - 1:
                ax.set_xlabel(xlabel)
            if j == 0:
                ax.set_ylabel(ylabel)
            if titles:
                ax.set_title(titles[j])
    fig.colorbar(pcm, ax=axes, shrink=0.6);


As a quick sanity check let’s visualize the identity matrix, representing a case where the attention weight is 
1
 only when the query and the key are the same.

PYTORCH
MXNET
JAX
TENSORFLOW
attention_weights = torch.eye(10).reshape((1, 1, 10, 10))
show_heatmaps(attention_weights, xlabel='Keys', ylabel='Queries')

11.1.2. Summary

The attention mechanism allows us to aggregate data from many (key, value) pairs. So far our discussion was quite abstract, simply describing a way to pool data. We have not explained yet where those mysterious queries, keys, and values might arise from. Some intuition might help here: for instance, in a regression setting, the query might correspond to the location where the regression should be carried out. The keys are the locations where past data was observed and the values are the (regression) values themselves. This is the so-called Nadaraya–Watson estimator (Nadaraya, 1964, Watson, 1964) that we will be studying in the next section.

By design, the attention mechanism provides a differentiable means of control by which a neural network can select elements from a set and to construct an associated weighted sum over representations.

11.1.3. Exercises

Suppose that you wanted to reimplement approximate (key, query) matches as used in classical databases, which attention function would you pick?

Suppose that the attention function is given by 
𝑎
(
𝑞
,
𝑘
𝑖
)
=
𝑞
⊤
𝑘
𝑖
 and that 
𝑘
𝑖
=
𝑣
𝑖
 for 
𝑖
=
1
,
…
,
𝑚
. Denote by 
𝑝
(
𝑘
𝑖
;
𝑞
)
 the probability distribution over keys when using the softmax normalization in (11.1.3). Prove that 
∇
𝑞
Attention
⁡
(
𝑞
,
𝐷
)
=
Cov
𝑝
(
𝑘
𝑖
;
𝑞
)
[
𝑘
𝑖
]
.

Design a differentiable search engine using the attention mechanism.

Review the design of the Squeeze and Excitation Networks (Hu et al., 2018) and interpret them through the lens of the attention mechanism.

PYTORCH
MXNET
JAX
TENSORFLOW

Table Of Contents

1. Visualization
2. Summary
3. Exercises
Previous
11. Attention Mechanisms and Transformers
Next
11.2. Attention Pooling by Similarity