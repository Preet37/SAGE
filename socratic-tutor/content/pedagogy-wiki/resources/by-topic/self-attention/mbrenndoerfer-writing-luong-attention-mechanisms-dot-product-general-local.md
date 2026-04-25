# Source: https://mbrenndoerfer.com/writing/luong-attention-mechanisms-dot-product-general-local
# Author: Marc Brenndörfer
# Author Slug: marc-brenndoerfer
# Title: Luong Attention: Dot Product, General & Local Attention Mechanisms
# Fetched via: browser
# Date: 2026-04-08

Back
Luong Attention: Dot Product, General & Local Mechanisms
Michael Brenndoerfer
Published: May 18, 2025
•
May 18, 2025
•
43 min read
BOOK CONTENTS

Part of

Language AI Handbook

View full book →

Data, Analytics & AI
Software Engineering
Machine Learning
Language AI Handbook

Explore Luong attention variants including dot product, general, and concat scoring. Learn global vs local attention, input-feeding, and how Luong differs from Bahdanau.

Track your reading progress

Sign in to mark chapters as read and track your learning journey

Sign in →
Reading Level

Choose your expertise level to adjust how many terms are explained. Beginners see more tooltips, experts see fewer to maintain reading flow. Hover over underlined terms for instant definitions.

Beginner
Maximum help
Intermediate
Medium help
Expert
Minimal help
Hide All
No tooltips
Luong Attention
Link Copied

In the previous chapter, we explored Bahdanau attention, which revolutionized sequence-to-sequence models by allowing the decoder to dynamically focus on different parts of the input sequence. Bahdanau's approach uses an additive score function and computes attention before the RNN step, feeding the context vector as input to the decoder. But is this the only way to design an attention mechanism?

In 2015, Luong et al. proposed several alternative attention mechanisms that are computationally simpler and often more effective. Their work introduced multiplicative attention variants, the distinction between global and local attention, and a different placement of attention in the decoder architecture. Understanding these variations is essential because the scaled dot-product attention used in modern transformers descends directly from Luong's multiplicative formulation.Language Resources

ADVERTISEMENT

Attention Score Functions
Link Copied

At the heart of any attention mechanism lies a fundamental question: how do we measure the relevance of each encoder state to the current decoding step? This measurement, called the alignment score or compatibility score, determines which parts of the input sequence the decoder should focus on when generating each output token.

Think of it this way: when translating "The cat sat on the mat" to French, and you're about to generate the word "chat" (cat), you need a way to identify that the English word "cat" is the most relevant source word. The score function quantifies this relevance for every source position, producing a set of numbers that attention will convert into a probability distribution.

Bahdanau attention introduced an additive score function with learned parameters. Luong et al. asked: can we achieve similar results with simpler approaches? Their answer was three alternative score functions, each representing a different trade-off between simplicity, expressiveness, and computational cost.

Dot Product Attention
Link Copied

The simplest approach to measuring relevance is to ask: how similar are the decoder and encoder representations? If the encoder has learned to represent "cat" in a particular way, and the decoder has learned to look for that same pattern when generating "chat", then similar representations should yield high scores.

The dot product provides exactly this similarity measure. Given a decoder hidden state 
ℎ
𝑡
h
t
	​

 and an encoder hidden state 
ℎ
ˉ
𝑠
h
ˉ
s
	​

, the dot product attention score is:

score
(
ℎ
𝑡
,
ℎ
ˉ
𝑠
)
=
ℎ
𝑡
⊤
ℎ
ˉ
𝑠
score(h
t
	​

,
h
ˉ
s
	​

)=h
t
⊤
	​

h
ˉ
s
	​


where:

ℎ
𝑡
∈
𝑅
𝑑
h
t
	​

∈R
d
: the decoder hidden state at timestep 
𝑡
t, encoding what the decoder is "looking for"
ℎ
ˉ
𝑠
∈
𝑅
𝑑
h
ˉ
s
	​

∈R
d
: the encoder hidden state at source position 
𝑠
s, encoding what that position "contains"
ℎ
𝑡
⊤
ℎ
ˉ
𝑠
h
t
⊤
	​

h
ˉ
s
	​

: the inner product of the two vectors, yielding a scalar score
𝑑
d: the hidden dimension, which must be equal for both encoder and decoder

Why does the dot product capture similarity? Consider what happens geometrically. When two vectors point in the same direction, their dot product is large and positive, indicating high compatibility. When they point in opposite directions, the dot product is large and negative. Orthogonal vectors, sharing no common direction, yield zero.

This geometric interpretation has a powerful implication: the encoder and decoder can learn complementary representations. The encoder learns to place semantically similar words in similar directions in the hidden space. The decoder learns to "query" for specific semantic content by producing hidden states that point toward the relevant encoder representations.

The elegance of dot product attention lies in its simplicity. No learned parameters are needed for the score function itself. All the learning happens in the encoder and decoder, which discover representations where raw similarity is a good proxy for alignment. This makes dot product attention computationally efficient and easy to implement.

However, this simplicity comes with a constraint: the decoder and encoder hidden states must have the same dimensionality. If 
ℎ
𝑡
∈
𝑅
𝑑
ℎ
h
t
	​

∈R
d
h
	​

 and 
ℎ
ˉ
𝑠
∈
𝑅
𝑑
ℎ
h
ˉ
s
	​

∈R
d
h
	​

, the dot product is well-defined. If they have different dimensions, you cannot compute a dot product directly, which motivates our next score function.

General (Bilinear) Attention
Link Copied

What if the encoder and decoder have different hidden dimensions? Or what if raw similarity isn't the right measure, and we want the model to learn a more nuanced notion of relevance?

The general score function addresses both concerns by introducing a learnable weight matrix 
𝑊
𝑎
W
a
	​

 that transforms the encoder states before computing similarity:

score
(
ℎ
𝑡
,
ℎ
ˉ
𝑠
)
=
ℎ
𝑡
⊤
𝑊
𝑎
ℎ
ˉ
𝑠
score(h
t
	​

,
h
ˉ
s
	​

)=h
t
⊤
	​

W
a
	​

h
ˉ
s
	​


where:

ℎ
𝑡
∈
𝑅
𝑑
ℎ
h
t
	​

∈R
d
h
	​

: the decoder hidden state at timestep 
𝑡
t
ℎ
ˉ
𝑠
∈
𝑅
𝑑
ℎ
ˉ
h
ˉ
s
	​

∈R
d
h
ˉ
	​

: the encoder hidden state at source position 
𝑠
s
𝑊
𝑎
∈
𝑅
𝑑
ℎ
×
𝑑
ℎ
ˉ
W
a
	​

∈R
d
h
	​

×d
h
ˉ
	​

: a learned weight matrix that projects encoder states into the decoder's space
ℎ
𝑡
⊤
𝑊
𝑎
ℎ
ˉ
𝑠
h
t
⊤
	​

W
a
	​

h
ˉ
s
	​

: a scalar score computed by first applying 
𝑊
𝑎
W
a
	​

 to 
ℎ
ˉ
𝑠
h
ˉ
s
	​

, then taking the dot product with 
ℎ
𝑡
h
t
	​


To understand what 
𝑊
𝑎
W
a
	​

 does, trace through the computation step by step. First, 
𝑊
𝑎
ℎ
ˉ
𝑠
W
a
	​

h
ˉ
s
	​

 transforms the encoder state into a 
𝑑
ℎ
d
h
	​

-dimensional vector. Then 
ℎ
𝑡
⊤
h
t
⊤
	​

 takes the dot product with this transformed vector. The matrix 
𝑊
𝑎
W
a
	​

 effectively learns which aspects of the encoder representation are most relevant for each dimension of the decoder state.

This formulation is called bilinear attention because the score is a bilinear function of the two input vectors: linear in 
ℎ
𝑡
h
t
	​

 when 
ℎ
ˉ
𝑠
h
ˉ
s
	​

 is fixed, and linear in 
ℎ
ˉ
𝑠
h
ˉ
s
	​

 when 
ℎ
𝑡
h
t
	​

 is fixed. The weight matrix 
𝑊
𝑎
W
a
	​

 serves two purposes:

Dimension matching: When encoder and decoder have different hidden dimensions, 
𝑊
𝑎
W
a
	​

 bridges the gap by projecting encoder states into the decoder's space
Learned similarity: Rather than relying on raw vector similarity, the matrix learns what aspects of encoder states are most relevant for alignment, potentially discovering non-obvious relationships

General attention is more expressive than dot product attention but requires additional parameters. For encoder and decoder dimensions of 512, 
𝑊
𝑎
W
a
	​

 adds 
512
×
512
=
262,144
512×512=262,144 parameters. This is modest compared to the total model size but can matter for smaller models or when memory is constrained.

ADVERTISEMENT

Concat Attention
Link Copied

The most expressive score function takes a fundamentally different approach. Rather than computing a form of similarity between two vectors, it asks: given both the decoder state and an encoder state, what score should a neural network assign?Machine Learning & Artificial Intelligence

The concat score function concatenates the two states and passes them through a small neural network:

score
(
ℎ
𝑡
,
ℎ
ˉ
𝑠
)
=
𝑣
𝑎
⊤
tanh
⁡
(
𝑊
𝑎
[
ℎ
𝑡
;
ℎ
ˉ
𝑠
]
)
score(h
t
	​

,
h
ˉ
s
	​

)=v
a
⊤
	​

tanh(W
a
	​

[h
t
	​

;
h
ˉ
s
	​

])

Let's unpack this formula piece by piece:

Concatenation 
[
ℎ
𝑡
;
ℎ
ˉ
𝑠
]
[h
t
	​

;
h
ˉ
s
	​

]: We stack the decoder and encoder states into a single vector of dimension 
𝑑
ℎ
+
𝑑
ℎ
ˉ
d
h
	​

+d
h
ˉ
	​

. This gives the network access to all information from both states.

Linear projection 
𝑊
𝑎
[
ℎ
𝑡
;
ℎ
ˉ
𝑠
]
W
a
	​

[h
t
	​

;
h
ˉ
s
	​

]: The weight matrix 
𝑊
𝑎
∈
𝑅
𝑛
×
(
𝑑
ℎ
+
𝑑
ℎ
ˉ
)
W
a
	​

∈R
n×(d
h
	​

+d
h
ˉ
	​

)
 projects the concatenated vector to an intermediate space of dimension 
𝑛
n. This allows the network to learn arbitrary linear combinations of the input features.

Nonlinearity 
tanh
⁡
(
⋅
)
tanh(⋅): The hyperbolic tangent activation introduces nonlinearity, enabling the network to learn complex, non-linear relationships between decoder and encoder states.

Scalar projection 
𝑣
𝑎
⊤
v
a
⊤
	​

: Finally, the weight vector 
𝑣
𝑎
∈
𝑅
𝑛
v
a
	​

∈R
n
 projects the intermediate representation to a single scalar score.

where:

ℎ
𝑡
∈
𝑅
𝑑
ℎ
h
t
	​

∈R
d
h
	​

: the decoder hidden state at timestep 
𝑡
t
ℎ
ˉ
𝑠
∈
𝑅
𝑑
ℎ
ˉ
h
ˉ
s
	​

∈R
d
h
ˉ
	​

: the encoder hidden state at source position 
𝑠
s
[
ℎ
𝑡
;
ℎ
ˉ
𝑠
]
∈
𝑅
𝑑
ℎ
+
𝑑
ℎ
ˉ
[h
t
	​

;
h
ˉ
s
	​

]∈R
d
h
	​

+d
h
ˉ
	​

: the concatenated vector of both states
𝑊
𝑎
∈
𝑅
𝑛
×
(
𝑑
ℎ
+
𝑑
ℎ
ˉ
)
W
a
	​

∈R
n×(d
h
	​

+d
h
ˉ
	​

)
: a learned projection matrix
𝑣
𝑎
∈
𝑅
𝑛
v
a
	​

∈R
n
: a learned weight vector that collapses the intermediate representation to a scalar
𝑛
n: the intermediate dimension, a hyperparameter typically set equal to the hidden dimension

This formulation is similar to Bahdanau attention, with one key difference: Bahdanau uses the previous decoder state 
ℎ
𝑡
−
1
h
t−1
	​

, while Luong's concat uses the current decoder state 
ℎ
𝑡
h
t
	​

. This seemingly small change has significant implications for the overall architecture, which we'll explore in the section on attention placement.

OUT
[3]:
Visualization
Comparison of three Luong attention score functions. Dot product (left) is parameter-free and requires matching dimensions. General attention (center) uses a learned weight matrix to enable flexible bilinear scoring. Concat attention (right) uses a two-layer network with tanh nonlinearity, making it the most expressive but also the most computationally expensive.

ADVERTISEMENT

Computational Comparison
Link Copied

The three score functions differ significantly in their computational requirements. For a sequence of length 
𝑆
S with hidden dimension 
𝑑
d:

Computational comparison of Luong attention score functions.
SCORE FUNCTION	TIME COMPLEXITY	PARAMETERS	NOTES
Dot Product	
𝑂
(
𝑆
𝑑
)
O(Sd)	0	Fastest, requires 
𝑑
ℎ
=
𝑑
ℎ
ˉ
d
h
	​

=d
h
ˉ
	​


General	
𝑂
(
𝑆
𝑑
2
)
O(Sd
2
)	
𝑑
ℎ
×
𝑑
ℎ
ˉ
d
h
	​

×d
h
ˉ
	​

	Matrix multiplication dominates
Concat	
𝑂
(
𝑆
𝑛
𝑑
)
O(Snd)	
𝑛
(
𝑑
ℎ
+
𝑑
ℎ
ˉ
)
+
𝑛
n(d
h
	​

+d
h
ˉ
	​

)+n	Two-step transformation

As shown in Table score-functions, dot product attention is most efficient but requires matching dimensions. General attention adds a single matrix, while concat attention requires two sets of parameters (
𝑊
𝑎
W
a
	​

 and 
𝑣
𝑎
v
a
	​

).

OUT
[4]:
Visualization
Computational cost (MFLOPs) at increasing sequence lengths, with hidden dimension fixed at 256. Dot product scales linearly while general and concat scale quadratically with hidden dimension, creating a large gap at longer sequences.
Parameter count (thousands) by hidden dimension for each score function. Dot product requires zero parameters, general attention scales as d squared, and concat attention scales similarly, making dot product the most memory-efficient choice.

For modern hardware with efficient matrix operations, dot product attention is significantly faster because it can be fully parallelized as a single matrix multiplication across all encoder states simultaneously. This efficiency advantage is why transformers adopt scaled dot-product attention as their core mechanism.

ADVERTISEMENT

Global vs Local Attention
Link Copied

Beyond score functions, Luong et al. introduced an important architectural distinction: global attention attends to all encoder states, while local attention focuses on a subset of positions around a predicted alignment point.

Global Attention
Link Copied

Global attention is conceptually straightforward. At each decoder timestep 
𝑡
t, we compute attention weights over all encoder hidden states by applying softmax to the alignment scores. The attention weight for source position 
𝑠
s at decoder timestep 
𝑡
t is:

𝛼
𝑡
𝑠
=
exp
⁡
(
score
(
ℎ
𝑡
,
ℎ
ˉ
𝑠
)
)
∑
𝑠
′
=
1
𝑆
exp
⁡
(
score
(
ℎ
𝑡
,
ℎ
ˉ
𝑠
′
)
)
α
ts
	​

=
∑
s
′
=1
S
	​

exp(score(h
t
	​

,
h
ˉ
s
′
	​

))
exp(score(h
t
	​

,
h
ˉ
s
	​

))
	​


where:

𝛼
𝑡
𝑠
α
ts
	​

: the attention weight for source position 
𝑠
s when decoding at timestep 
𝑡
t
score
(
ℎ
𝑡
,
ℎ
ˉ
𝑠
)
score(h
t
	​

,
h
ˉ
s
	​

): the alignment score computed using any of the three score functions
𝑆
S: the total number of encoder positions (source sequence length)
exp
⁡
(
⋅
)
exp(⋅): the exponential function, ensuring all values are positive before normalization
The denominator normalizes the weights so they sum to 1 across all source positions

The context vector is then computed as the weighted sum of all encoder states:

𝑐
𝑡
=
∑
𝑠
=
1
𝑆
𝛼
𝑡
𝑠
ℎ
ˉ
𝑠
c
t
	​

=
s=1
∑
S
	​

α
ts
	​

h
ˉ
s
	​


where:

𝑐
𝑡
∈
𝑅
𝑑
ℎ
ˉ
c
t
	​

∈R
d
h
ˉ
	​

: the context vector at decoder timestep 
𝑡
t
𝛼
𝑡
𝑠
α
ts
	​

: the attention weight for position 
𝑠
s (how much to focus on that position)
ℎ
ˉ
𝑠
h
ˉ
s
	​

: the encoder hidden state at position 
𝑠
s

This weighted sum allows the decoder to "focus" on relevant source positions: positions with high attention weights contribute more to the context vector, while positions with low weights contribute less.

Global attention is what we typically mean when we say "attention" without qualification. It allows the model to attend to any position in the source sequence, which is essential for tasks like translation where word order can differ dramatically between languages.

The computational cost of global attention is 
𝑂
(
𝑆
)
O(S) per decoder step, where 
𝑆
S is the source sequence length. For most NLP tasks with sequences of hundreds or thousands of tokens, this is manageable. However, for very long sequences (documents, books, genomic data), global attention becomes a bottleneck.Social Sciences

Local Attention
Link Copied

Local attention restricts the attention window to a subset of encoder positions centered around an alignment point 
𝑝
𝑡
p
t
	​

. This reduces computation and can also serve as an inductive bias when alignments are expected to be roughly monotonic.

OUT
[5]:
Visualization
Global attention weights over a 12-token source sequence for each of 10 target positions. The diagonal pattern shows that each target token attends most strongly to the corresponding source region, while still maintaining non-zero weights across all positions for maximum flexibility.
Local attention with window half-width D=2 over the same source and target lengths. Attention weights are non-zero only within a narrow band around the predicted alignment point, reducing computation from O(S) to O(D) per step.

Luong et al. propose two variants for determining the alignment point 
𝑝
𝑡
p
t
	​

:

Monotonic alignment (local-m): The alignment point is simply set to 
𝑝
𝑡
=
𝑡
p
t
	​

=t, assuming the source and target sequences are roughly aligned. This works well for tasks like speech recognition where the output follows the input order.

Predictive alignment (local-p): The model learns to predict the alignment point using a small neural network. The predicted alignment point is:

𝑝
𝑡
=
𝑆
⋅
𝜎
(
𝑣
𝑝
⊤
tanh
⁡
(
𝑊
𝑝
ℎ
𝑡
)
)
p
t
	​

=S⋅σ(v
p
⊤
	​

tanh(W
p
	​

h
t
	​

))

where:Machine Learning & Artificial Intelligence

𝑝
𝑡
p
t
	​

: the predicted alignment point (center of the attention window) at decoder timestep 
𝑡
t
𝑆
S: the source sequence length, used to scale the output to a valid position
𝜎
(
⋅
)
σ(⋅): the sigmoid function, which maps any real number to 
[
0
,
1
]
[0,1]
𝑊
𝑝
∈
𝑅
𝑑
ℎ
×
𝑑
ℎ
W
p
	​

∈R
d
h
	​

×d
h
	​

: a learned weight matrix that transforms the decoder hidden state
𝑣
𝑝
∈
𝑅
𝑑
ℎ
v
p
	​

∈R
d
h
	​

: a learned weight vector that projects to a scalar
ℎ
𝑡
h
t
	​

: the current decoder hidden state

The sigmoid ensures the output is between 0 and 1, and multiplying by 
𝑆
S scales it to a valid source position. This allows the model to learn non-monotonic alignments while still restricting attention to a local window.

Within the window 
[
𝑝
𝑡
−
𝐷
,
𝑝
𝑡
+
𝐷
]
[p
t
	​

−D,p
t
	​

+D], attention weights are computed normally but multiplied by a Gaussian centered at 
𝑝
𝑡
p
t
	​

:

𝛼
𝑡
𝑠
=
align
(
ℎ
𝑡
,
ℎ
ˉ
𝑠
)
⋅
exp
⁡
(
−
(
𝑠
−
𝑝
𝑡
)
2
2
𝜎
2
)
α
ts
	​

=align(h
t
	​

,
h
ˉ
s
	​

)⋅exp(−
2σ
2
(s−p
t
	​

)
2
	​

)

where:

𝛼
𝑡
𝑠
α
ts
	​

: the final attention weight for position 
𝑠
s at decoder timestep 
𝑡
t
align
(
ℎ
𝑡
,
ℎ
ˉ
𝑠
)
align(h
t
	​

,
h
ˉ
s
	​

): the base attention weight from softmax over the local window
𝑠
s: the source position being attended to
𝑝
𝑡
p
t
	​

: the predicted center of the attention window
𝜎
σ: the standard deviation of the Gaussian (controls window sharpness), typically set to 
𝐷
/
2
D/2
The exponential term is a Gaussian that peaks at 
𝑠
=
𝑝
𝑡
s=p
t
	​

 and decays for positions farther from the center

The Gaussian favors positions near the center of the window, providing a soft boundary rather than a hard cutoff. Positions at the edge of the window receive lower weights even if their alignment scores are high.

ADVERTISEMENT

When to Use Each
Link Copied

The choice between global and local attention depends on your task:

Global attention is the default choice for most NLP tasks. Translation, summarization, and question answering all benefit from the ability to attend to any position. The computational overhead is acceptable for typical sequence lengths.Social Sciences

Local attention shines when you have prior knowledge about alignment structure. Speech recognition, where phonemes appear in order, is a natural fit. Document-level tasks with very long sequences can also benefit from the reduced computation.

In practice, global attention dominates because modern hardware handles the 
𝑂
(
𝑆
)
O(S) computation efficiently, and the flexibility to attend anywhere is valuable. Local attention is more of a historical curiosity, though its ideas influenced later work on sparse attention patterns in transformers.

ADVERTISEMENT

Newsletter

Enjoying this article?

I write about AI, data science, machine learning, finance, economics and entrepreneurship. Subscribe to get updates delivered straight to your inbox.Machine Learning & Artificial Intelligence

No popups
Unobstructed reading
Commenting

No spam, unsubscribe anytime.

Join Community

Michael Brenndoerfer

Attention Placement: Input vs Output
Link Copied

A subtle but important difference between Bahdanau and Luong attention is where the attention mechanism fits into the decoder architecture. This choice affects both the information flow and the computational graph.

Bahdanau: Attention as Input
Link Copied

In Bahdanau attention, the context vector is computed using the previous decoder hidden state and then concatenated with the input embedding to form the input to the current decoder step. The computation proceeds as:

𝑐
𝑡
	
=
Attention
(
ℎ
𝑡
−
1
,
𝐻
ˉ
)


𝑥
~
𝑡
	
=
[
𝑥
𝑡
;
𝑐
𝑡
]


ℎ
𝑡
	
=
RNN
(
𝑥
~
𝑡
,
ℎ
𝑡
−
1
)
c
t
	​

x
~
t
	​

h
t
	​

	​

=Attention(h
t−1
	​

,
H
ˉ
)
=[x
t
	​

;c
t
	​

]
=RNN(
x
~
t
	​

,h
t−1
	​

)
	​


where:

ℎ
𝑡
−
1
h
t−1
	​

: the decoder hidden state from the previous timestep
𝐻
ˉ
=
[
ℎ
ˉ
1
,
ℎ
ˉ
2
,
…
,
ℎ
ˉ
𝑆
]
H
ˉ
=[
h
ˉ
1
	​

,
h
ˉ
2
	​

,…,
h
ˉ
S
	​

]: the matrix of all encoder hidden states
𝑐
𝑡
c
t
	​

: the context vector computed by attending over encoder states using 
ℎ
𝑡
−
1
h
t−1
	​

𝑥
𝑡
x
t
	​

: the input embedding at timestep 
𝑡
t (typically the previous output token)
𝑥
~
𝑡
x
~
t
	​

: the augmented input formed by concatenating 
𝑥
𝑡
x
t
	​

 and 
𝑐
𝑡
c
t
	​

ℎ
𝑡
h
t
	​

: the new decoder hidden state

The context vector influences the RNN computation directly. This means the decoder can use information about which source positions are relevant when updating its hidden state.

Luong: Attention as Output
Link Copied

In Luong attention, the decoder RNN runs first, producing the current hidden state. Then attention is computed using this new state, and the results are combined. The computation proceeds as:

ℎ
𝑡
	
=
RNN
(
𝑥
𝑡
,
ℎ
𝑡
−
1
)


𝑐
𝑡
	
=
Attention
(
ℎ
𝑡
,
𝐻
ˉ
)


ℎ
~
𝑡
	
=
tanh
⁡
(
𝑊
𝑐
[
𝑐
𝑡
;
ℎ
𝑡
]
)
h
t
	​

c
t
	​

h
~
t
	​

	​

=RNN(x
t
	​

,h
t−1
	​

)
=Attention(h
t
	​

,
H
ˉ
)
=tanh(W
c
	​

[c
t
	​

;h
t
	​

])
	​


where:

𝑥
𝑡
x
t
	​

: the input embedding at timestep 
𝑡
t
ℎ
𝑡
−
1
h
t−1
	​

: the decoder hidden state from the previous timestep
ℎ
𝑡
h
t
	​

: the new decoder hidden state after the RNN step
𝐻
ˉ
=
[
ℎ
ˉ
1
,
ℎ
ˉ
2
,
…
,
ℎ
ˉ
𝑆
]
H
ˉ
=[
h
ˉ
1
	​

,
h
ˉ
2
	​

,…,
h
ˉ
S
	​

]: the matrix of all encoder hidden states
𝑐
𝑡
c
t
	​

: the context vector computed by attending over encoder states using the current 
ℎ
𝑡
h
t
	​

[
𝑐
𝑡
;
ℎ
𝑡
]
[c
t
	​

;h
t
	​

]: the concatenation of context and hidden state
𝑊
𝑐
∈
𝑅
𝑑
ℎ
×
(
𝑑
ℎ
ˉ
+
𝑑
ℎ
)
W
c
	​

∈R
d
h
	​

×(d
h
ˉ
	​

+d
h
	​

)
: a learned weight matrix that combines context and hidden state
ℎ
~
𝑡
h
~
t
	​

: the "attentional hidden state" used for prediction

The final output 
ℎ
~
𝑡
h
~
t
	​

 combines the context vector with the decoder state through a learned transformation. This attentional state is then used for prediction, typically by projecting it to vocabulary size and applying softmax.

OUT
[6]:
Visualization
Bahdanau attention computes context using the previous hidden state h(t-1), then feeds the context concatenated with the input to the RNN. This 'attention as input' approach means source context directly influences the state update.
Luong attention runs the RNN first to produce h(t), then computes context from this current state. The context and hidden state are combined via a learned layer to produce the attentional state used for output.

ADVERTISEMENT

Implications of Placement
Link Copied

The placement choice has several practical implications:

Information flow: Bahdanau attention allows the context to influence the RNN state update, potentially enabling richer interactions. Luong attention keeps the RNN computation separate, which can be easier to reason about and debug.

Parallelization: Luong attention is slightly more amenable to parallelization during training because the RNN step doesn't depend on the attention computation. However, this advantage is minimal compared to the sequential nature of RNNs themselves.

Empirical performance: Luong et al. found their approach performed comparably or slightly better than Bahdanau attention on machine translation benchmarks. The simpler architecture and faster score functions (especially dot product) made it an attractive choice.

ADVERTISEMENT

Luong vs Bahdanau: A Complete Comparison
Link Copied

Let's consolidate the differences between these two influential attention mechanisms:

Comparison of Bahdanau and Luong attention mechanisms.
ASPECT	BAHDANAU	LUONG
Score function	Additive (concat with tanh)	Dot, general, or concat
Decoder state used	Previous (
ℎ
𝑡
−
1
h
t−1
	​

)	Current (
ℎ
𝑡
h
t
	​

)
Attention placement	Before RNN (input)	After RNN (output)
Context integration	Concatenated with input	Combined via learned layer
Encoder architecture	Bidirectional RNN	Unidirectional (stacked)
Parameters	More (additive scoring)	Fewer (dot product option)

Both mechanisms compute attention weights via softmax and produce a context vector as a weighted sum of encoder states. The differences lie in the details of scoring, timing, and integration.

In practice, the choice between Bahdanau and Luong attention often matters less than other architectural decisions like model size, number of layers, and training procedure. Modern transformer architectures have largely superseded both, but understanding these mechanisms provides essential intuition for how attention works.

ADVERTISEMENT

Implementation
Link Copied

Let's implement Luong attention in PyTorch. We'll build a complete attention module that supports all three score functions, then integrate it into a sequence-to-sequence decoder.

Attention Module
Link Copied

First, we define the core attention computation. The module takes encoder outputs and a decoder hidden state, computes attention weights, and returns the context vector.

IN
[7]:
Code
import torch
import torch.nn as nn
import torch.nn.functional as F


class LuongAttention(nn.Module):
    """Luong attention with configurable score function."""

    def __init__(self, hidden_dim, encoder_dim=None, method="dot"):
        super().__init__()
        self.method = method
        self.hidden_dim = hidden_dim
        self.encoder_dim = encoder_dim or hidden_dim

        if method == "general":
            # W_a for bilinear scoring
            self.W_a = nn.Linear(self.encoder_dim, hidden_dim, bias=False)
        elif method == "concat":
            # Two-layer scoring network
            self.W_a = nn.Linear(
                hidden_dim + self.encoder_dim, hidden_dim, bias=False
            )
            self.v_a = nn.Linear(hidden_dim, 1, bias=False)

    def score(self, decoder_hidden, encoder_outputs):
        """Compute attention scores for all encoder positions."""
        if self.method == "dot":
            scores = torch.bmm(
                encoder_outputs, decoder_hidden.unsqueeze(2)
            ).squeeze(2)
        elif self.method == "general":
            transformed = self.W_a(encoder_outputs)
            scores = torch.bmm(
                transformed, decoder_hidden.unsqueeze(2)
            ).squeeze(2)
        elif self.method == "concat":
            src_len = encoder_outputs.size(1)
            decoder_expanded = decoder_hidden.unsqueeze(1).expand(
                -1, src_len, -1
            )
            concat = torch.cat([decoder_expanded, encoder_outputs], dim=2)
            scores = self.v_a(torch.tanh(self.W_a(concat))).squeeze(2)
        return scores

    def forward(self, decoder_hidden, encoder_outputs, mask=None):
        """Compute attention weights and context vector."""
        scores = self.score(decoder_hidden, encoder_outputs)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float("-inf"))
        attention_weights = F.softmax(scores, dim=1)
        context = torch.bmm(
            attention_weights.unsqueeze(1), encoder_outputs
        ).squeeze(1)
        return context, attention_weights

The LuongAttention class implements all three score functions. The constructor accepts the hidden dimension, an optional encoder dimension, and the scoring method. The score method computes alignment scores using dot product, general (bilinear), or concat approaches. The forward method orchestrates the full attention computation: scores, optional masking, softmax normalization, and weighted sum.Language Resources

Attentional Decoder
Link Copied

Now let's build a decoder that uses Luong attention. The key difference from a standard RNN decoder is the attention step after the RNN and the combination layer that produces the attentional hidden state.

IN
[8]:
Code
class LuongDecoder(nn.Module):
    """Decoder with Luong attention."""

    def __init__(
        self,
        vocab_size,
        embed_dim,
        hidden_dim,
        encoder_dim=None,
        attention_method="dot",
        num_layers=1,
        dropout=0.1,
    ):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.encoder_dim = encoder_dim or hidden_dim

        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.rnn = nn.GRU(
            embed_dim,
            hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0,
        )
        self.attention = LuongAttention(
            hidden_dim, self.encoder_dim, attention_method
        )
        self.W_c = nn.Linear(
            self.encoder_dim + hidden_dim, hidden_dim, bias=False
        )
        self.output_projection = nn.Linear(hidden_dim, vocab_size)
        self.dropout = nn.Dropout(dropout)

    def forward_step(self, input_token, hidden, encoder_outputs, mask=None):
        """Single decoding step with attention."""
        embedded = self.dropout(self.embedding(input_token.unsqueeze(1)))
        rnn_output, hidden = self.rnn(embedded, hidden)
        rnn_output = rnn_output.squeeze(1)
        context, attention_weights = self.attention(
            hidden[-1], encoder_outputs, mask
        )
        combined = torch.cat([context, rnn_output], dim=1)
        attentional_hidden = torch.tanh(self.W_c(combined))
        output = self.output_projection(self.dropout(attentional_hidden))
        return output, hidden, attention_weights

The LuongDecoder class combines an embedding layer, a GRU, the attention module, a combination layer for producing the attentional hidden state, and an output projection. The forward_step method implements a single decoding step: embed, RNN, then attention. This order is the defining characteristic of Luong attention.

ADVERTISEMENT

Testing the Implementation
Link Copied

Let's verify our implementation works correctly with some example data.

IN
[9]:
Code
# Create sample data
batch_size = 4
src_len = 10
hidden_dim = 64
vocab_size = 1000

# Simulated encoder outputs (normally from an encoder RNN)
encoder_outputs = torch.randn(batch_size, src_len, hidden_dim)

# Padding mask (last 2 positions are padding)
mask = torch.ones(batch_size, src_len)
mask[:, -2:] = 0

# Initialize decoder
decoder = LuongDecoder(
    vocab_size=vocab_size,
    embed_dim=32,
    hidden_dim=hidden_dim,
    attention_method="dot",
)

# Initial hidden state
hidden = torch.zeros(1, batch_size, hidden_dim)

# Input token (e.g., start token)
input_token = torch.zeros(batch_size, dtype=torch.long)

# Run one decoding step
output, new_hidden, attention_weights = decoder.forward_step(
    input_token, hidden, encoder_outputs, mask
)
OUT
[10]:
Console
Output shape: torch.Size([4, 1000])
Hidden shape: torch.Size([1, 4, 64])
Attention weights shape: torch.Size([4, 10])

Attention weights sum to 1: 1.0000
Attention on padded positions: 0.000000

The output has the expected shape for vocabulary logits, and attention weights sum to 1 (ignoring padded positions). The near-zero attention on padded positions confirms our masking works correctly.

ADVERTISEMENT

Visualizing Attention Patterns
Link Copied

Let's compare the attention patterns produced by different score functions on the same input.

IN
[11]:
Code
# Create decoders with different attention methods
methods = ["dot", "general", "concat"]
decoders = {
    method: LuongDecoder(vocab_size, 32, hidden_dim, attention_method=method)
    for method in methods
}

# Run decoding steps and collect attention weights
all_attention = {}
for method, dec in decoders.items():
    hidden = torch.zeros(1, batch_size, hidden_dim)
    _, _, attn = dec.forward_step(
        input_token, hidden, encoder_outputs, mask
    )
    all_attention[method] = attn.detach()
OUT
[12]:
Visualization
Dot product attention weights across 10 source positions for the first batch item. Parameter-free scoring based on direct vector similarity produces a peaked distribution.
General (bilinear) attention weights for the same input. The learned weight matrix W_a allows more flexible scoring, often producing a different distribution than dot product.
Concat attention weights for the same input. The two-layer network with tanh nonlinearity can capture complex compatibility patterns. Gray shading marks the two padded positions.

With random weights, the attention patterns are similar across methods. After training, each method would develop distinct patterns based on what it learns about alignment. Dot product attention tends to produce sharper distributions when encoder and decoder representations align well, while concat attention can learn more complex compatibility functions.

To see what trained attention looks like, let's simulate a full translation with realistic attention patterns. The heatmap below shows attention weights across multiple decoding steps, revealing how the decoder systematically aligns with different source positions.

OUT
[13]:
Visualization
Simulated attention heatmap for translating 'The black cat sat quietly' to 'Le chat noir etait assis tranquillement'. Each row shows attention weights when generating one target word. The roughly diagonal pattern reflects word-order correspondence between the two languages, while deviations (e.g., 'noir' attending to 'black' at position 1) demonstrate how attention handles the French adjective-noun reordering.

ADVERTISEMENT

Worked Example: English-French Alignment
Link Copied

The formulas we've discussed can feel abstract until you see them in action. Let's trace through a complete attention computation for a concrete translation example, following each step from raw hidden states to final attention weights.

Consider translating the English sentence "The cat sat" to French "Le chat assis". We'll focus on the moment when the decoder is about to generate the second French word "chat". At this point, the decoder needs to figure out which English word to focus on. Intuitively, it should attend to "cat" since that's the word being translated.

Setting Up the Problem
Link Copied

First, let's create simulated encoder hidden states for each English word. In a real model, these would come from running a bidirectional LSTM or transformer encoder over the input. Here, we'll craft vectors that capture the intuition: "cat" and the decoder state for "chat" should be similar, while "The" and "sat" should be less relevant.

IN
[14]:
Code
import numpy as np
import torch
import torch.nn.functional as F

np.random.seed(42)
torch.manual_seed(42)

# Create encoder representations that reflect semantic content:
# - "The": article with low semantic content (small magnitude)
# - "cat": noun with distinct pattern (will match decoder query)
# - "sat": verb with different pattern (won't match as well)
encoder_states = torch.tensor(
    [
        [0.1, 0.2, -0.1, 0.3],   # "The" - low magnitude, generic
        [0.8, -0.3, 0.9, 0.2],   # "cat" - strong noun pattern
        [0.2, 0.7, 0.1, -0.4],   # "sat" - different verb pattern
    ],
    dtype=torch.float32,
).unsqueeze(0)  # Add batch dimension for PyTorch

# Decoder hidden state when generating "chat"
# Designed to be similar to "cat" encoding
decoder_state = torch.tensor(
    [[0.7, -0.2, 0.8, 0.3]],  # Query vector looking for noun-like content
    dtype=torch.float32,
)
OUT
[15]:
Console
Encoder states shape: torch.Size([1, 3, 4])
Decoder state shape: torch.Size([1, 4])

The encoder states have shape (1, 3, 4): batch size 1, 3 source words, and 4-dimensional hidden states. The decoder state has shape (1, 4): a single 4-dimensional vector representing what the decoder is "looking for" when generating "chat".

Step 1: Computing Alignment Scores
Link Copied

Now we apply the dot product score function. For each encoder state, we compute its dot product with the decoder state. The dot product measures how much two vectors point in the same direction.

IN
[16]:
Code
# Compute dot product scores: decoder_state · each encoder_state
scores = torch.bmm(encoder_states, decoder_state.unsqueeze(2)).squeeze()

# Apply softmax to convert scores to probabilities
attention_weights = F.softmax(scores, dim=0)

# Compute context vector as weighted sum of encoder states
context = torch.bmm(
    attention_weights.unsqueeze(0).unsqueeze(0), encoder_states
).squeeze()

ADVERTISEMENT

Step 2: Examining the Results
Link Copied

Let's see what scores each word received and how softmax transforms them into attention weights:

OUT
[17]:
Console
Step-by-step attention computation:
----------------------------------------

Dot product scores (raw alignment):
  The: 0.0400
  cat: 1.4000
  sat: -0.0400

Attention weights (after softmax):
  The: 0.1718
  cat: 0.6695
  sat: 0.1586

Context vector: [0.585, -0.055, 0.601, 0.122]

Highest attention on: 'cat'

The results reveal exactly what we hoped to see. The decoder state for generating "chat" produces the highest alignment score with "cat" because their vectors point in similar directions. The softmax function then amplifies this difference: "cat" receives about 70% of the attention weight, while "The" and "sat" share the remaining 30%.

Notice how the context vector ends up being dominated by the "cat" representation. This is attention in action: the decoder has learned to extract the relevant information from the source sequence by focusing on the semantically corresponding word.

OUT
[18]:
Visualization
Attention weights when generating 'chat' from 'The cat sat'. The model correctly focuses on 'cat' (shown in red), the source word that semantically corresponds to the French target. This alignment emerges from the similarity between the decoder hidden state and the 'cat' encoder representation, with 'cat' receiving roughly 70% of the attention weight.

The visualization below shows how the context vector is constructed as a weighted blend of the encoder states. Each dimension of the context vector is a weighted sum of that dimension across all encoder states, with the weights determined by attention.

OUT
[19]:
Visualization
Weighted contributions from each source word to the context vector dimensions. The 'cat' representation (red) dominates all four dimensions since it receives the highest attention weight (~70%). Diamond markers show the final context vector values, which closely match the stacked bar totals.
Comparison of the final context vector against each encoder state. The context closely resembles the 'cat' encoding (red bars) but is a smoothed blend across all three source words, shifted slightly toward 'The' and 'sat' by their small attention weights.

ADVERTISEMENT

Newsletter

Enjoying this article?

I write about AI, data science, machine learning, finance, economics and entrepreneurship. Subscribe to get updates delivered straight to your inbox.Machine Learning & Artificial Intelligence

No popups
Unobstructed reading
Commenting

No spam, unsubscribe anytime.

Join Community

Michael Brenndoerfer

Limitations and Impact
Link Copied

Luong attention addressed several limitations of Bahdanau attention while introducing its own trade-offs. Understanding these helps contextualize attention's evolution toward transformers.

Computational Efficiency
Link Copied

The dot product score function is significantly faster than additive attention, especially for long sequences. With hidden dimension 
𝑑
d and sequence length 
𝑆
S, dot product requires 
𝑂
(
𝑆
𝑑
)
O(Sd) operations compared to 
𝑂
(
𝑆
𝑛
𝑑
)
O(Snd) for additive attention (where 
𝑛
n is the intermediate dimension). This efficiency gain compounds during training when attention is computed millions of times.

However, dot product attention has a subtle numerical issue: when the hidden dimension is large, dot products can become very large in magnitude. This pushes softmax toward extreme values (near 0 or 1), causing gradient saturation. The transformer architecture addresses this with scaled dot-product attention, dividing by 
𝑑
d
	​

 to keep values in a reasonable range.

OUT
[20]:
Visualization
Standard deviation of dot product scores as hidden dimension increases, for unit-variance random vectors. Unscaled scores (red) grow as the square root of the dimension, reaching std above 30 at d=1024. Dividing by the square root of d (green) keeps scores near unit variance regardless of dimension.
Effect of score magnitude on softmax output. As the score scale increases from 1 to 50, attention concentrates almost entirely on the highest-scoring position. Large dot products in high-dimensional spaces produce this same sharpening effect, causing gradient saturation during training.
Expressiveness vs Simplicity
Link Copied

General and concat attention are more expressive than dot product, able to learn arbitrary compatibility functions. But this expressiveness comes at a cost: more parameters, slower computation, and potential overfitting on small datasets. Empirically, the simpler dot product often performs comparably or better, suggesting that the encoder and decoder learn representations where raw similarity is a good proxy for alignment.

This finding influenced the design of transformers, which use dot product attention exclusively. The lesson is that with sufficient model capacity and data, simple mechanisms can match or exceed complex ones.

ADVERTISEMENT

Sequential Bottleneck
Link Copied

Both Bahdanau and Luong attention still rely on RNNs for the encoder and decoder. This creates a sequential bottleneck: each timestep must wait for the previous one, preventing parallelization. Attention helps by providing direct connections to encoder states, but the fundamental limitation remains.

Transformers eliminate this bottleneck entirely by using self-attention instead of recurrence. Each position can attend to all other positions in parallel, enabling massive speedups on modern hardware. Luong's dot product attention, combined with the key-query-value formulation, became the foundation for this revolution.

ADVERTISEMENT

Legacy and Influence
Link Copied

Luong attention's most lasting contribution is demonstrating that simple, efficient attention mechanisms work well. The dot product score function, attention after the decoder step, and the idea of multiple attention variants all influenced subsequent research. When Vaswani et al. designed the transformer, they chose scaled dot-product attention, directly building on Luong's work.

The distinction between global and local attention also foreshadowed later work on sparse attention patterns. Transformers face quadratic complexity in sequence length, and researchers have explored various ways to restrict attention to local windows or learned patterns. Luong's local attention was an early exploration of this trade-off between expressiveness and efficiency.

ADVERTISEMENT

Summary
Link Copied

This chapter explored Luong attention, a family of attention mechanisms that simplified and extended Bahdanau's original formulation.

The key innovations include three score functions for computing alignment:

Dot product: Parameter-free, efficient, requires matching dimensions
General: Learned bilinear transformation, handles different dimensions
Concat: Two-layer network with nonlinearity, most expressive

Luong attention also introduced the distinction between global and local attention. Global attention considers all encoder positions, while local attention focuses on a predicted window. Global attention dominates in practice due to its flexibility and the efficiency of modern hardware.

The architectural placement differs from Bahdanau: Luong computes attention after the RNN step using the current hidden state, then combines the context with the hidden state through a learned transformation. This "attention as output" approach is simpler and slightly more parallelizable.

Perhaps most importantly, Luong's work demonstrated that simple attention mechanisms, particularly dot product attention, can match or exceed more complex alternatives. This insight directly influenced the transformer architecture, which uses scaled dot-product attention as its core mechanism. Understanding Luong attention provides essential context for the self-attention mechanisms we'll explore in the next part of this book.

ADVERTISEMENT

Key Parameters
Link Copied

When implementing Luong attention, several parameters significantly impact model behavior and performance:

Attention method (method): Chooses between "dot", "general", or "concat" score functions. Dot product is fastest and parameter-free but requires matching encoder/decoder dimensions. General attention adds a learned projection matrix, enabling different dimensions and learned similarity. Concat attention is most expressive but slowest. Start with dot product for most applications.

Hidden dimension (hidden_dim): The dimensionality of the decoder hidden state. Larger values (256-512) provide more representational capacity but increase computation. For attention, this determines the space in which similarity is computed. Values of 256-512 work well for most sequence-to-sequence tasks.Language Resources

Encoder dimension (encoder_dim): The dimensionality of encoder hidden states. Can differ from hidden_dim when using general or concat attention. For bidirectional encoders, this is typically 
2
×
hidden_dim
2×hidden_dim since forward and backward states are concatenated.

Local attention window (D): For local attention, controls the half-width of the attention window. Positions outside 
[
𝑝
𝑡
−
𝐷
,
𝑝
𝑡
+
𝐷
]
[p
t
	​

−D,p
t
	​

+D] receive zero attention. Larger windows (D=10-20) provide more flexibility but increase computation. Smaller windows (D=2-5) work well when alignments are expected to be monotonic.

Dropout (dropout): Applied to embeddings and the attentional hidden state before output projection. Values of 0.1-0.3 help prevent overfitting, especially important for attention weights which can become overly peaked during training.

Quiz
Link Copied

Ready to test your understanding? Take this quick quiz to reinforce what you've learned about Luong attention mechanisms.

Luong Attention Quiz
Question 1 of 10
0 of 10 completed
What is the main advantage of dot product attention over additive (Bahdanau) attention?
It can handle different encoder and decoder dimensions
It requires no learned parameters and is computationally efficient
It produces sharper attention distributions
It works better for long sequences
Track your reading progress

Sign in to mark chapters as read and track your learning journey

Sign in →
Comments
Back to Language AI Handbook
Previous Chapter
Bahdanau Attention
Next Chapter
Copy Mechanism
Reference
BIBTEX
Academic
Copy
@misc{luongattentiondotproductgenerallocalmechanisms,
  author = {Michael Brenndoerfer},
  title = {Luong Attention: Dot Product, General & Local Mechanisms},
  year = {2025},
  url = {https://mbrenndoerfer.com/writing/luong-attention-mechanisms-dot-product-general-local},
  organization = {mbrenndoerfer.com},
  note = {Accessed: 2026-04-08}
}
Show other formats
(APA, MLA, Chicago, Harvard, Simple)
APA
Academic
Copy
Michael Brenndoerfer (2025). Luong Attention: Dot Product, General & Local Mechanisms. Retrieved from https://mbrenndoerfer.com/writing/luong-attention-mechanisms-dot-product-general-local
MLA
Academic
Copy
Michael Brenndoerfer. "Luong Attention: Dot Product, General & Local Mechanisms." 2026. Web. 4/8/2026. <https://mbrenndoerfer.com/writing/luong-attention-mechanisms-dot-product-general-local>.
CHICAGO
Academic
Copy
Michael Brenndoerfer. "Luong Attention: Dot Product, General & Local Mechanisms." Accessed 4/8/2026. https://mbrenndoerfer.com/writing/luong-attention-mechanisms-dot-product-general-local.
HARVARD
Academic
Copy
Michael Brenndoerfer (2025) 'Luong Attention: Dot Product, General & Local Mechanisms'. Available at: https://mbrenndoerfer.com/writing/luong-attention-mechanisms-dot-product-general-local (Accessed: 4/8/2026).
Simple
Basic
Copy
Michael Brenndoerfer (2025). Luong Attention: Dot Product, General & Local Mechanisms. https://mbrenndoerfer.com/writing/luong-attention-mechanisms-dot-product-general-local
DIRECT LINK
URL
Copy
https://mbrenndoerfer.com/writing/luong-attention-mechanisms-dot-product-general-local
About the author
Michael Brenndoerfer

All opinions expressed here are my own and do not reflect the views of my employer.

Michael currently works as an Associate Director of Data Science at EQT Partners in Singapore, leading AI and data initiatives across private capital investments.Machine Learning & Artificial Intelligence

With a background spanning private equity, management consulting, and software engineering, he focuses on building practical analytics solutions and helping teams work more effectively with data. He has contributed research to AI conferences and enjoys exploring applications of machine learning and natural language processing.

View Full Resume
Publications
Contact
Books
Newsletter
Related
Related Content
Data, Analytics & AI
Software Engineering
Beam Search: Decoding and Sequence Generation
May 22, 2025
•
48 min read

Learn how beam search balances quality and compute in sequence generation, covering greedy decoding limits, length normalization, diverse beam search, and sampling alternatives.

Data, Analytics & AI
Software Engineering
Teacher Forcing: Training Seq2Seq with Ground Truth Context
May 21, 2025
•
44 min read

Learn how teacher forcing trains sequence-to-sequence models efficiently, understand exposure bias, and explore scheduled sampling and REINFORCE to close the train-test gap.

Data, Analytics & AI
Machine Learning
Bahdanau Attention: Dynamic Context for Neural Machine Translation
May 19, 2025
•
55 min read

Learn how Bahdanau attention solves the encoder-decoder bottleneck with dynamic context vectors, softmax alignment, and interpretable attention weights for sequence-to-sequence models.

All writing

ADVERTISEMENT

Newsletter
Stay up to date.

Get articles, book updates, and news delivered to your inbox.

No spam, unsubscribe anytime.

or
Join the community.

Sign in to remove popups, track your reading progress, and join the discussion.

Join the community
ON THIS PAGE