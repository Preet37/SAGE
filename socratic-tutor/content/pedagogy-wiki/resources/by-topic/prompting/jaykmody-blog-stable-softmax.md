# Source: https://jaykmody.com/blog/stable-softmax/
# Author: Jay Mody
# Author Slug: jay-mody
# Title: Numerically Stable Softmax and Cross Entropy
# Fetched via: browser
# Date: 2026-04-08

Numerically Stable Softmax and Cross Entropy

December 15, 2022

In this post, we'll take a look at softmax and cross entropy loss, two very common mathematical functions used in deep learning. We'll see that naive implementations are numerically unstable, and then we'll derive implementations that are numerically stable.

Symbols
𝑥
: Input vector of dimensionality 
𝑑
.
𝑦
: Correct class, an integer on the range 
𝑦
∈
[
1
…
𝐾
]
.
𝑦
^
: Raw outputs (i.e. logits) of our neural network, vector of dimensionality 
𝐾
.
We use 
log
 to denote the natural logarithm.
Softmax

The softmax function is defined as:

softmax
(
𝑥
)
𝑖
=
𝑒
𝑥
𝑖
∑
𝑗
𝑒
𝑥
𝑗

The softmax function converts a vector of real numbers (
𝑥
) to a vector of probabilities (such that 
∑
𝑖
softmax
(
𝑥
)
𝑖
=
1
 and 
0
≤
softmax
(
𝑥
)
𝑖
≤
1
). This is useful for converting the raw final output of a neural network (often referred to as logits) into probabilities.

In code:

def softmax(x):
    # assumes x is a vector
    return np.exp(x) / np.sum(np.exp(x))

x = np.array([1.2, 2, -4, 0.0]) # might represent raw output logits of a neural network
softmax(x)
# outputs: [0.28310553, 0.63006295, 0.00156177, 0.08526975]


For very large inputs, we start seeing some numerical instability:

x = np.array([1.2, 2000, -4000, 0.0])
softmax(x)
# outputs: [0., nan, 0.,  0.]


Why? Because floating point numbers aren't magic, they have limits:

np.finfo(np.float64).max
# 1.7976931348623157e+308, largest positive number

np.finfo(np.float64).tiny
# 2.2250738585072014e-308, smallest positive number at full precision

np.finfo(np.float64).smallest_subnormal
# 5e-324, smallest positive number


When we go beyond these limits, we start seeing funky behavior:

np.finfo(np.float64).max * 2
# inf, overflow error

np.inf - np.inf
# nan, not a number error

np.finfo(np.float64).smallest_subnormal / 2
# 0.0, underflow error


Looking back at our softmax example that resulted in [0., nan, 0., 0.], we can see that the overflow of np.exp(2000) = np.inf is causing the nan, since we end up with np.inf / np.inf = nan.

If we want to avoid nans, we need to avoid infs.

To avoid infs, we need to avoid overflows.

To avoid overflows, we need to prevent our numbers from growing too large.

Underflows on the other hand don't seem quite as detrimental. Worst case scenario, we get the result 0 and lose all precision (i.e. np.exp(-4000) = 0). While this is not ideal, this is a lot better than running into inf and nan.

Given the relative stability of floating point underflows vs overflows, how can we fix softmax?

Let's revisit our softmax equation and apply some tricks:

softmax
(
𝑥
)
𝑖
	
=
𝑒
𝑥
𝑖
∑
𝑗
𝑒
𝑥
𝑗

	
=
1
⋅
𝑒
𝑥
𝑖
∑
𝑗
𝑒
𝑥
𝑗

	
=
𝐶
𝐶
𝑒
𝑥
𝑖
∑
𝑗
𝑒
𝑥
𝑗

	
=
𝐶
𝑒
𝑥
𝑖
∑
𝑗
𝐶
𝑒
𝑥
𝑗

	
=
𝑒
𝑥
𝑖
+
log
⁡
𝐶
∑
𝑗
𝑒
𝑥
𝑗
+
log
⁡
𝐶

Here, we're taking advantage of the rule 
𝑎
⋅
𝑏
𝑥
=
𝑏
𝑥
+
log
𝑏
⁡
𝑎
. As a result, we are given the ability to offset our inputs by any constant of our choosing. For example, if we set that constant to 
log
⁡
𝐶
=
−
max
(
𝑥
)
:

softmax
(
𝑥
)
𝑖
=
𝑒
𝑥
𝑖
−
max
(
𝑥
)
∑
𝑗
𝑒
𝑥
𝑗
−
max
(
𝑥
)

We get a numerically stable version of softmax:

All exponentiated values will be between 0 and 1 (
0
≤
𝑒
𝑥
𝑖
−
max
(
𝑥
)
≤
1
) since the value in the exponent is always negative (
𝑥
𝑖
−
max
(
𝑥
)
≤
0
)
This prevents overflow errors (but we are still prone to underflows)
At least one of the exponentiated values is 1 in the case when 
𝑥
𝑖
=
max
(
𝑥
)
: 
𝑒
max
(
𝑥
)
−
max
(
𝑥
)
=
𝑒
0
=
1
i.e. at least one value is guaranteed not to underflow
Thus, our denominator will always be 
>=
1
, preventing division by zero errors
We have at least one non-zero numerator, so softmax can't result in a zero vector

In code:

def softmax(x):
    # assumes x is a vector
    x = x - np.max(x)
    return np.exp(x) / np.sum(np.exp(x))

x = np.array([1.2, 2, -4, 0])
softmax(x)
# outputs: [0.28310553, 0.63006295, 0.00156177, 0.08526975]

# works for large numbers!!!
x = np.array([1.2, 2, -4, 0]) * 1000
softmax(x)
# outputs: [0., 1., 0., 0.]

Cross Entropy and Log Softmax

The cross entropy between two probability distributions is defined as.

𝐻
(
𝑝
,
𝑞
)
=
−
∑
𝑖
𝑝
𝑖
log
⁡
(
𝑞
𝑖
)

where 
𝑝
 and 
𝑞
 are our probability distributions represented as probability vectors (that is 
𝑝
𝑖
 and 
𝑞
𝑖
 are the probabilities of event 
𝑖
 occurring for 
𝑝
 and 
𝑞
 respectively). This video has a great explanation for cross entropy.

Roughly speaking, cross entropy measures the similarity of two probability distributions. In the context of neural networks, it's common to use cross entropy as a loss function for classification problems where:

𝑞
 is our predicted probabilities vector (i.e. the softmax of our raw network outputs, also called logits, denoted as 
𝑦
^
), that is 
𝑞
=
softmax
(
𝑦
^
)
𝑝
 is a one-hot encoded vector of our label, that is a probability vector that assigns 100% probability to the position 
𝑦
 (our label for the correct class): 
𝑝
𝑖
=
{
1
	
𝑖
=
𝑦


0
	
𝑖
≠
𝑦

In this setup, cross entropy simplifies to:

𝐻
(
𝑝
,
𝑞
)
	
=
−
∑
𝑖
𝑝
𝑖
log
⁡
(
𝑞
𝑖
)

	
=
−
𝑝
𝑦
⋅
log
⁡
(
𝑞
𝑦
)
−
∑
𝑖
≠
𝑦
𝑝
𝑖
log
⁡
(
𝑞
𝑖
)

	
=
−
1
⋅
log
⁡
(
𝑞
𝑦
)
−
∑
𝑖
≠
𝑦
0
⋅
log
⁡
(
𝑞
𝑖
)

	
=
−
log
⁡
(
𝑞
𝑦
)
−
0
∑
𝑖
≠
𝑦
log
⁡
(
𝑞
𝑖
)

	
=
−
log
⁡
(
𝑞
𝑦
)

	
=
−
log
⁡
(
softmax
(
𝑦
^
)
𝑦
)

In code:

def cross_entropy(y_hat, y_true):
    # assume y_hat is a vector and y_true is an integer
    return -np.log(softmax(y_hat)[y_true])

cross_entropy(
    y_hat=np.random.normal(size=(10)),
    y_true=3,
)
# 2.580982279204241


For large numbers in y_hat, we start seeing inf:

cross_entropy(
    y_hat = np.array([-1000, 1000]),
    y_true = 0,
)
# inf


The problem is that softmax([-1000, 1000]) = [0, 1], and since y_true = 0, we get -log(0) = inf. So we need some way to avoid taking the log of zero. To prevent this, we can rearrange our equation for log(softmax(x)):

log
⁡
(
softmax
(
𝑥
)
𝑖
)
	
=
log
⁡
(
𝑒
𝑥
𝑖
−
max
(
𝑥
)
∑
𝑗
𝑒
𝑥
𝑗
−
max
(
𝑥
)
)

	
=
log
⁡
(
𝑒
𝑥
𝑖
−
max
(
𝑥
)
)
−
log
⁡
(
∑
𝑗
𝑒
𝑥
𝑗
−
max
(
𝑥
)
)

	
=
(
𝑥
𝑖
−
max
(
𝑥
)
)
log
⁡
(
𝑒
)
−
log
⁡
(
∑
𝑗
𝑒
𝑥
𝑗
−
max
(
𝑥
)
)

	
=
(
𝑥
𝑖
−
max
(
𝑥
)
)
⋅
1
−
log
⁡
(
∑
𝑗
𝑒
𝑥
𝑗
−
max
(
𝑥
)
)

	
=
𝑥
𝑖
−
max
(
𝑥
)
−
log
⁡
(
∑
𝑗
𝑒
𝑥
𝑗
−
max
(
𝑥
)
)

This new equation guarantees that the sum inside the log will always be 
≥
1
, so we no longer need to worry about log(0) errors.

In code:

def log_softmax(x):
    # assumes x is a vector
    x_max = np.max(x)
    return x - x_max - np.log(np.sum(np.exp(x - x_max)))

def cross_entropy(y_hat, y_true):
    return -log_softmax(y_hat)[y_true]

cross_entropy(
    y_hat=np.random.normal(size=(10)),
    y_true=3,
)
# 2.580982279204241

# works for large inputs!!!!
cross_entropy(
    y_hat = np.array([-1000, 1000]),
    y_true = 0,
)
# 2000.0