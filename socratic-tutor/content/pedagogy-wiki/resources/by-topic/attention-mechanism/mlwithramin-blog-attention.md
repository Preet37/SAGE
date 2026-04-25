# Source: https://www.mlwithramin.com/blog/attention
# Title: Numerical Example (mlwithramin.com) — Attention
# Fetched via: browser
# Date: 2026-04-08

Introduction

Attention mechanisms have revolutionized the field of deep learning, especially in natural language processing (NLP), computer vision, and speech recognition. An attention mechanism allows a model to focus on different parts of the input, depending on their relevance to the output. In other words, it helps the model to selectively attend to different parts of the input, rather than processing it as a whole.

In this blog post, we will explain the attention mechanism in detail, including the mathematical expressions and formulas. We will also provide a full numerical example to help readers understand how attention works.

Attention Mechanism

An attention mechanism is a way to compute a weighted sum of input vectors based on their relevance to a query. Given a query q and a set of input vectors 
x
1
,
x
2
,…,
x
n
𝑥
1
,
𝑥
2
,
…
,
𝑥
𝑛
, the attention mechanism computes a set of attention weights 
α
1
,
α
2
,…,
α
n
α
1
,
α
2
,
…
,
α
𝑛
, where each weight α_i represents the relevance of the i-th input vector x_i to the query q. The attention mechanism then computes the weighted sum of the input vectors as follows:

c=
α
1
∗
x
1
+
α
2
∗
x
2
+…+
α
n
∗
x
n
𝑐
=
α
1
∗
𝑥
1
+
α
2
∗
𝑥
2
+
…
+
α
𝑛
∗
𝑥
𝑛

The resulting vector 
c
𝑐
 is called the context vector, which represents the attended information from the input. The attention weights 
α
i
α
𝑖
 are typically computed using a function that takes the query q and the i-th input vector 
x
i
𝑥
𝑖
 as inputs and produces a scalar value as output. This function is called the attention score function.

Attention Score Function

The attention score function is used to compute the relevance of an input vector 
x
i
𝑥
𝑖
 to a query 
q
𝑞
. There are several ways to define the attention score function, but one of the most common approaches is the dot product attention, which is defined as follows:

score(q,
x
i
)=q∗
x
i
𝑠
𝑐
𝑜
𝑟
𝑒
(
𝑞
,
𝑥
𝑖
)
=
𝑞
∗
𝑥
𝑖

where * denotes the dot product. In other words, the attention score is simply the dot product between the query 
q
𝑞
 and the 
i
𝑖
-th input vector 
x
i
𝑥
𝑖
.

Another common approach is the additive attention, which is defined as follows:

score(q,
x
i
)=
v
a
∗tanh(
W
a
∗q+
U
a
∗
x
i
)
𝑠
𝑐
𝑜
𝑟
𝑒
(
𝑞
,
𝑥
𝑖
)
=
𝑣
𝑎
∗
𝑡
𝑎
𝑛
ℎ
(
𝑊
𝑎
∗
𝑞
+
𝑈
𝑎
∗
𝑥
𝑖
)

where 
W
a
𝑊
𝑎
 and 
U
a
𝑈
𝑎
 are weight matrices, 
v
a
𝑣
𝑎
 is a weight vector, and tanh is the hyperbolic tangent function. In this case, the attention score is computed by applying a non-linear transformation to a concatenation of the query q and the i-th input vector x_i, followed by a dot product with a weight vector 
v
a
𝑣
𝑎
.

Softmax Function

Once the attention scores are computed, they are transformed into attention weights using the softmax function. The softmax function is a widely used function that takes a vector of arbitrary real numbers and outputs a probability distribution over the vector elements. Specifically, the softmax function is defined as follows:

softmax(z
)
i
=exp(
z
i
)/su
m
j
(exp(
z
j
))
𝑠
𝑜
𝑓
𝑡
𝑚
𝑎
𝑥
(
𝑧
)
𝑖
=
𝑒
𝑥
𝑝
(
𝑧
𝑖
)
/
𝑠
𝑢
𝑚
𝑗
(
𝑒
𝑥
𝑝
(
𝑧
𝑗
)
)

where 
z
𝑧
 is the input vector and e is the base of the natural logarithm. In other words, the softmax function computes the exponential of each element of the input vector, normalizes the resulting vector to have a sum of one, and outputs the resulting vector as the attention weights.

Numerical Example

To illustrate how the attention mechanism works, let’s consider a simple example of machine translation, where we want to translate a sentence from French to English. Suppose the input sentence in French is “Le chat mange du poisson” (which means “The cat eats fish” in English), and the output sentence in English is “The cat eats fish”. We want to build a neural machine translation model that takes the French sentence as input and produces the English sentence as output.

The first step is to represent the input sentence as a sequence of vectors. We can use a word embedding matrix to represent each word in the sentence as a vector. For simplicity, let’s assume that each word is represented as a 3-dimensional vector. Then, the input sentence can be represented as a matrix X of shape (5,3), where each row corresponds to a word vector:

X = [[-0.2, 0.3, 0.5],
[0.1, -0.4, 0.2],
[0.4, -0.1, 0.6],
[0.2, 0.5, -0.1],
[0.3, -0.2, 0.4]]


Next, we need to define the query vector q, which represents the context of the output sentence that we want to generate. For simplicity, let’s assume that the output sentence has a fixed length of 4 words, and each word is represented as a 3-dimensional vector. Then, the query vector q can be represented as a matrix of shape (4,3), where each row corresponds to a word vector:

q = [[0.1, 0.2, -0.3],
[-0.4, 0.3, 0.2],
[0.5, 0.1, -0.2],
[-0.2, 0.4, 0.3]]


Now, we can compute the attention scores using the dot product attention. For each row of q, we compute the dot product with each row of X:

s = np.dot(X, q.T)


The resulting matrix s contains the attention scores for each word in the input sentence and each word in the output sentence:

s = [[ 0.11, 0.24, -0.26, 0.02],
[-0.09, 0.22, 0.14, 0.16],
[ 0.01, -0.34, 0.34, -0.26],
[-0.01, 0.37, -0.12, 0.18],
[ 0.07, 0.08, 0.22, -0.14]]


To convert the attention scores into attention weights, we need to apply the softmax function to each column of s:

alpha = softmax(s, axis=0)


The resulting matrix alpha contains the attention weights for each word in the input sentence and each word in the output sentence:

alpha = [[0.3218, 0.2411, 0.1202, 0.3057],
[0.2586, 0.2142, 0.2679, 0.3319],
[0.2857, 0.1693, 0.3423, 0.1809],
[0.2784, 0.2414, 0.1356, 0.3422],
[0.3055, 0.1340, 0.1340, 0.2193]]


Finally, we can compute the context vectors by taking the weighted sum of the input vectors for each word in the output sentence. The context vectors can be computed as follows:

C = np.dot(alpha.T, X)


The resulting matrix C contains the attended information from the input sentence for each word in the output sentence:

C = [[ 0.1866, -0.0502, 0.4296],
[ 0.0815, 0.0269, 0.2632],
[ 0.1333, 0.0125, 0.3869],
[ 0.1621, 0.0738, 0.1943]]

Conclusion

In this blog post, we explained the attention mechanism in detail, including the mathematical expressions and formulas. We also provided a full numerical example to illustrate how attention works in practice. Attention mechanisms have become an essential tool in deep learning, particularly in NLP, and have led to significant improvements in model performance. Understanding attention mechanisms is crucial for building state-of-the-art deep learning models and pushing the boundaries of AI research.