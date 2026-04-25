# Source: https://arpitbhayani.me/blogs/qkv-matrices/
# Author: Arpit Bhayani
# Author Slug: arpit-bhayani
# Title: The Weight Matrices
# Fetched via: trafilatura
# Date: 2026-04-07

At the core of the attention mechanism in LLMs are three matrices: Query, Key, and Value. These matrices are how transformers actually pay attention to different parts of the input. In this write-up, we will go through the construction of these matrices from the ground up.
Why Q, K, V Matrices Matter
When we read a sentence like “The cat sat on the mat because it was comfortable,” our brain automatically knows that “it” refers to “the mat” and not “the cat.” This is attention in action. Our brain is selectively focusing on relevant words to understand the context.
In neural networks, we need a similar mechanism. Traditional [recurrent neural networks](https://en.wikipedia.org/wiki/Recurrent_neural_network) processed sequences one token at a time, maintaining hidden states that carry information forward from the previous steps. RNN process looks something like this
Step 1: Process "The"
→ Hidden state h1 (knows only about "The")
Step 2: Process "cat"
→ Takes h1 + "cat" → produces h2
→ Now h2 knows about "The" and "cat"
Step 3: Process "sat"
→ Takes h2 + "sat" → produces h3
→ Now h3 knows about "The", "cat", and "sat"
Step 4: Process "on"
→ Takes h3 + "on" → produces h4
... and so on
The [transformer architecture introduced in 2017](https://arxiv.org/abs/1706.03762) flipped this approach by replacing recurrence with attention. The attention mechanism solved this by allowing the model to look at all words simultaneously and decide which words are important for understanding each word.
These three matrices are what let the model decide which words matter for each other. They reshape the input so the model can highlight useful connections instead of treating every word equally.
Instead of processing tokens sequentially, allow each token to directly attend to every other token in the sequence simultaneously.
Every word can check every other word to see how much it should care about it. For example, the model can link “sat” and “cat” right away, instead of passing information along one word at a time.
"sat" attends to:
- "The": 5% (low attention)
- "cat": 60% (high attention - who is sitting?)
- "sat": 10% (some self-attention)
- "on": 15% (what comes after sitting?)
- "the": 5% (low attention)
- "mat": 5% (low attention)
Because each token looks at all the tokens that happen in parallel, this enables faster training and better capture of relationships between distant words.
The Intuition
Think of the attention mechanism like a database lookup system. When we query a database, we provide a search term (query), the database compares it against its indexed keys, and returns the corresponding values. The Q, K, V mechanism works similarly:
- Query (Q): What am I looking for?
- Key (K): What do I contain?
- Value (V): What information do I actually hold?
For each position in our input sequence, we create a query asking, “What should I pay attention to?” Then we compare this query against all the keys to find matches. Finally, we retrieve the values corresponding to the best matches.
Attention Pipeline
Before we dive deeper, here is the whole flow of self-attention in one clean sequence:
Input
→ Linear projections
→ Q, K, V
→ Attention scores
→ Softmax
→ Weighted values
→ Output
I have discussed this entire flow in one of my previous blog posts - [How LLM Inference Works](https://arpitbhayani.me/blogs/how-llm-inference-works) - give it a read.
A Simple Example
Imagine we have a very short sentence with just 3 words: “Cat eats fish”
First, we need to represent each word as a vector. In real transformers, these are learned embeddings (like [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings), BGE, E5, Nomic, and MiniLM), but for our example, let’s use simple 4-dimensional vectors:
import numpy as np
# Simple word embeddings (4-dimensional)
cat = np.array([1.0, 0.0, 0.5, 0.2])
eats = np.array([0.0, 1.0, 0.3, 0.8])
fish = np.array([0.5, 0.3, 1.0, 0.1])
# Stack them into an input matrix
# Shape: (sequence_length, embedding_dim) = (3, 4)
X = np.array([cat, eats, fish])
print("Input matrix X:")
print(X)
print(f"Shape: {X.shape}")
This gives us:
Input matrix X:
[[1. 0. 0.5 0.2]
[0. 1. 0.3 0.8]
[0.5 0.3 1. 0.1]]
Shape: (3, 4)
Each row represents one word in our sequence. Now we need to transform this input matrix into Q, K, and V matrices.
The Weight Matrices
To create Q, K, and V from our input, we need three separate weight matrices: Wq
, Wk
, and Wv
. These are learned parameters that the model trains during the learning process. For our example (similar to when model is trained), let’s initialize them with small random values.
The dimension of these weight matrices is crucial. If our input embedding dimension is d_model
(4 in our case, but popularly it is 768 in real world) and we want our attention mechanism to work in a d_k
dimensional space (let’s use 3), then:
- Wq has shape (d_model, d_k) = (4, 3)
- Wk has shape (d_model, d_k) = (4, 3)
- Wv has shape (d_model, d_k) = (4, 3)
Note: d_k = d_model / num_heads
and we will discuss this later, but the usual value for this is 768 / 12 = 64
as seen in GPT-3 Small.
# Set random seed for reproducibility
np.random.seed(42)
# Initialize weight matrices
d_model = 4 # input embedding dimension
d_k = 3 # dimension for Q, K, V
Wq = np.random.randn(d_model, d_k) * 0.1
Wk = np.random.randn(d_model, d_k) * 0.1
Wv = np.random.randn(d_model, d_k) * 0.1
Note: We used random initialization for Wq, Wk, and Wv matrices. But in real systems, these matrices are learned through backpropagation during training, which we will discuss this in another post.
Constructing the Query matrix
You can think of the Query matrix as the question each word asks while trying to understand its surroundings. We create it by multiplying our input matrix X
with the query weight matrix Wq.
# Create Query matrix
Q = np.dot(X, Wq)
print("Query matrix Q:")
print(Q)
print(f"Shape: {Q.shape}")
Let’s break down what happens:
- X has shape (3, 4): 3 words, each with 4 features
- Wq has shape (4, 3): transforms 4-dim input to 3-dim query space
- Q = X @ Wq has shape (3, 3): 3 words, each with a 3-dim query vector
Each row of Q is the query vector for one word. For example, Q[0] is the query vector for “cat”, asking “what should I attend to when processing the word cat?” (self-attention).
Constructing the Key matrix
The Key matrix represents “what each word offers” as information. Other words will compare their queries against these keys to decide how much attention to pay.
# Create Key matrix
K = np.dot(X, Wk)
print("Key matrix K:")
print(K)
print(f"Shape: {K.shape}")
Similarly:
- K = X @ Wk has shape (3, 3)
- Each row is a key vector representing what that word position contains
- K[0] is the key for “cat”, K[1] for “eats”, K[2] for “fish”
Constructing the Value matrix
The Value matrix contains the actual information that will be passed forward. After we figure out where to attend (using Q and K), we retrieve the corresponding values.
# Create Value matrix
V = np.dot(X, Wv)
print("Value matrix V:")
print(V)
print(f"Shape: {V.shape}")
Again:
- V = X @ Wv has shape (3, 3)
- Each row is a value vector containing the information from that word
- These are the actual values that get combined based on attention scores
Construction Pseudocode
Here is the complete code that constructs Q, K, V matrices from scratch:
import numpy as np
def construct_qkv_matrices(input_embeddings, d_k, seed=42):
"""
Construct Q, K, V matrices from input embeddings.
Args:
input_embeddings: numpy array of shape (seq_len, d_model)
d_k: dimension for Q, K, V projections
seed: random seed for weight initialization
Returns:
Q, K, V: Query, Key, Value matrices
Wq, Wk, Wv: Weight matrices (for inspection)
"""
np.random.seed(seed)
seq_len, d_model = input_embeddings.shape
# Initialize weight matrices
Wq = np.random.randn(d_model, d_k) * 0.1
Wk = np.random.randn(d_model, d_k) * 0.1
Wv = np.random.randn(d_model, d_k) * 0.1
# Construct Q, K, V through matrix multiplication
Q = np.dot(input_embeddings, Wq)
K = np.dot(input_embeddings, Wk)
V = np.dot(input_embeddings, Wv)
return Q, K, V, Wq, Wk, Wv
# Example usage
cat = np.array([1.0, 0.0, 0.5, 0.2])
eats = np.array([0.0, 1.0, 0.3, 0.8])
fish = np.array([0.5, 0.3, 1.0, 0.1])
X = np.array([cat, eats, fish])
Q, K, V, Wq, Wk, Wv = construct_qkv_matrices(X, d_k=3)
print("Input shape:", X.shape)
print("Q shape:", Q.shape)
print("K shape:", K.shape)
print("V shape:", V.shape)
Why Separate Weight Matrices
The reason is functional separation. Each matrix serves a different purpose:
- Wq transforms the input to create questions (queries)
- Wk transforms the input to create searchable indices (keys)
- Wv transforms the input to create the actual content (values)
If we used the same weight matrix for all three, we would lose this functional distinction. The model learns to make queries that are good at finding relevant keys, and keys that are good at being found by relevant queries. Meanwhile, values learn to encode the most useful information to pass forward.
Think of it like a search engine: the way we index documents (keys) is different from how users formulate searches (queries), and both are different from the actual content we return (values).
Impact of Chosen Dimension
The choice of d_k
(the projection dimension) affects the model’s capacity and efficiency:
Smaller d_k (like our d_k=3):
- Faster computation
- Less memory usage
- Might not capture complex relationships
- Useful for simpler tasks or as part of multi-head attention
Larger d_k (like d_k=64 or d_k=512):
- Can model more complex relationships
- More parameters to learn
- Higher computational cost
- Used in production transformers
In practice, models like BERT use d_k=64 per attention head, with 12 or 16 heads in parallel (multi-head attention), giving a total effective dimension of 768 or 1024.
Role of Matrices in Attention
# Compute attention scores (simplified)
# Score = Q @ K^T / sqrt(d_k)
attention_scores = np.dot(Q, K.T) / np.sqrt(d_k)
print("Attention scores:")
print(attention_scores)
print(f"Shape: {attention_scores.shape}")
# Each row shows how much word i attends to words j
print("\nInterpretation:")
print("Row 0 (cat): attention to [cat, eats, fish]")
print("Row 1 (eats): attention to [cat, eats, fish]")
print("Row 2 (fish): attention to [cat, eats, fish]")
The attention scores matrix tells us how much each word should attend to every other word. Higher values mean stronger attention. These scores are then used to create a weighted combination of the value vectors.
The First Step
The Q, K, V matrices are just the first step in the [attention mechanism](https://arpitbhayani.me/blogs/how-llm-inference-works). Here is how they fit into the complete self-attention process:
- Construct Q, K, V from input (what we looked at)
- Compute attention scores: score = (Q @ K^T) / sqrt(d_k)
- Apply softmax to get attention weights
- Compute weighted sum of values: output = attention_weights @ V
- Optionally apply output projection
Footnote
The Query, Key, and Value matrices are the core components that enable transformers to process sequences in parallel while maintaining context awareness.
By projecting input embeddings through three separate learned weight matrices, we create specialized representations for searching (queries), being searched (keys), and carrying information (values).
This design, combined with the attention mechanism, allows models to dynamically focus on relevant parts of the input, taking natural language processing above and beyond.