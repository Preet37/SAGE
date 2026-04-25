# Source: http://www.cs.cmu.edu/~mgormley/courses/10423-f24/slides/lecture3-learning.pdf
# Title: Henry Chai & Matt Gormley
# Fetched via: jina
# Date: 2026-04-11

Title: lecture3-learning.pdf



Number of Pages: 59

Henry Chai & Matt Gormley 

> 9/4/24

# 10 -423/623: Generative AI 

# Lecture 3 – Learning LLMs 

# and Decoding Front Matter 

 Announcements: 

 HW0 released 8/28, due 9/9 (next Monday) at 11:59 PM 

 Two components: written and programming 

 Separate assignments on Gradescope 

 Unique policy specific to HW0: we will grant (almost) 

any extension request 

 Quiz 1 in -class on 9/11 (next Wednesday) 

 Instructor OH start this week; see the OH calendar for 

more details  

> 9/4/24 2

## Recall: 

## Scaled Dot -

## Product 

## Attention 

9/4/24  3

𝒒 1 𝒒 2 𝒒 3 𝒒 4

𝒗 1 𝒗 2 𝒗 3 𝒗 4

softmax 

𝒌 1 𝒌 2 𝒌 3 𝒌 4

𝒙 1 𝒙 2 𝒙 3 𝒙 4

𝑾 𝑘 

𝑾 𝑞 

𝑾 𝑣 

𝑎 4,1 𝑎 4,2 𝑎 4,3

𝑠 4,1 𝑠 4,2 𝑠 4,3 𝑠 4,4

𝑎 4,4

𝒗 𝑗 = 𝑾 𝑣 

𝑇 𝒙 𝑗 

𝒌 𝑗 = 𝑾 𝑘 

𝑇 𝒙 𝑗 

𝒒 𝑗 = 𝑾 𝑞 

𝑇 𝒙 𝑗 

𝑠 4,𝑗 = 𝒌 𝑗 

𝑇 𝒒 4

𝑑 𝑘 

𝑎 4,𝑗 = softmax 𝑠 4,𝑗 

𝒙 4

′ = ෍

𝑗 =1

4

𝑎 4,𝑗 𝒗 𝑗 

Values 

Keys 

Queries 

Scores 

Attention 

weights 

# attention Scaled Dot -

## Product 

## Attention: 

## Matrix Form  

> 9/4/24

4

𝒒 1 𝒒 2 𝒒 3 𝒒 4

𝒗 1 𝒗 2 𝒗 3 𝒗 4

softmax 

𝒌 1 𝒌 2 𝒌 3 𝒌 4

𝒙 1 𝒙 2 𝒙 3 𝒙 4

𝑾 𝑘 

𝑾 𝑞 

𝑾 𝑣 

𝑉 = 𝒗 1, ⋯ , 𝒗 𝑁 = 𝑾 𝑣 

𝑇 𝒙 1, ⋯ , 𝒙 𝑁 

𝐾 = 𝒌 1, ⋯ , 𝒌 𝑁 = 𝑾 𝑘 

𝑇 𝒙 1, ⋯ , 𝒙 𝑁 

𝑄 = 𝒒 1, ⋯ , 𝒒 𝑁 = 𝑾 𝑞 

𝑇 𝒙 1, ⋯ , 𝒙 𝑁 Scaled Dot -

## Product 

## Attention: 

## Matrix Form  

> 9/4/24

5

𝒒 1 𝒒 2 𝒒 3 𝒒 4

𝒗 1 𝒗 2 𝒗 3 𝒗 4

softmax 

𝒌 1 𝒌 2 𝒌 3 𝒌 4

𝒙 1 𝒙 2 𝒙 3 𝒙 4

𝑾 𝑘 

𝑾 𝑞 

𝑾 𝑣 

𝑉 = 𝒗 1, ⋯ , 𝒗 𝑁 𝑇 = 𝒙 1, ⋯ , 𝒙 𝑁 𝑇 𝑾 𝑣 

𝐾 = 𝒌 1, ⋯ , 𝒌 𝑁 𝑇 = 𝒙 1, ⋯ , 𝒙 𝑁 𝑇 𝑾 𝑘 

𝑄 = 𝒒 1, ⋯ , 𝒒 𝑁 𝑇 = 𝒙 1, ⋯ , 𝒙 𝑁 𝑇 𝑾 𝑞 Scaled Dot -

## Product 

## Attention: 

## Matrix Form  

> 9/4/24 6

𝒒 1 𝒒 2 𝒒 3 𝒒 4

𝒗 1 𝒗 2 𝒗 3 𝒗 4

softmax 

𝒌 1 𝒌 2 𝒌 3 𝒌 4

𝒙 1 𝒙 2 𝒙 3 𝒙 4

𝑾 𝑘 

𝑾 𝑞 

𝑾 𝑣 

𝑉 = 𝑋 𝑾 𝑣 

𝐾 = 𝑋 𝑾 𝑘 

𝑄 = 𝑋 𝑾 𝑞 Scaled Dot -

## Product 

## Attention: 

## Matrix Form  

> 9/4/24 7

𝒒 1 𝒒 2 𝒒 3 𝒒 4

𝒗 1 𝒗 2 𝒗 3 𝒗 4

softmax 

𝒌 1 𝒌 2 𝒌 3 𝒌 4

𝒙 1 𝒙 2 𝒙 3 𝒙 4

𝑾 𝑘 

𝑾 𝑞 

𝑾 𝑣 

𝑆 = 𝑄 𝐾 𝑇 

𝑑 𝑘 

𝐴 = softmax 𝑆 

𝑉 = 𝑋 𝑾 𝑣 

𝐾 = 𝑋 𝑾 𝑘 

𝑄 = 𝑋 𝑾 𝑞 Scaled Dot -

## Product 

## Attention: 

## Matrix Form  

> 9/4/24 8

𝒒 1 𝒒 2 𝒒 3 𝒒 4

𝒗 1 𝒗 2 𝒗 3 𝒗 4

softmax 

𝒌 1 𝒌 2 𝒌 3 𝒌 4

𝒙 1 𝒙 2 𝒙 3 𝒙 4

𝑾 𝑘 

𝑾 𝑞 

𝑾 𝑣 

𝐴 = softmax 𝑆 

𝑋 ′ = 𝐴𝑉 = softmax 𝑄 𝐾 𝑇 

𝑑 𝑘 

𝑉 

𝑆 = 𝑄 𝐾 𝑇 

𝑑 𝑘 

𝑉 = 𝑋 𝑾 𝑣 

𝐾 = 𝑋 𝑾 𝑘 

𝑄 = 𝑋 𝑾 𝑞 Which 

## dimension is 

## the softmax 

## applied over: 

## row -wise or 

## column -wise?  

> 9/4/24 9

𝒒 1 𝒒 2 𝒒 3 𝒒 4

𝒗 1 𝒗 2 𝒗 3 𝒗 4

softmax 

𝒌 1 𝒌 2 𝒌 3 𝒌 4

𝒙 1 𝒙 2 𝒙 3 𝒙 4

𝑾 𝑘 

𝑾 𝑞 

𝑾 𝑣 

𝐴 = softmax 𝑆 

𝑋 ′ = 𝐴𝑉 = softmax 𝑄 𝐾 𝑇 

𝑑 𝑘 

𝑉 

𝑆 = 𝑄 𝐾 𝑇 

𝑑 𝑘 

𝑉 = 𝑋 𝑾 𝑣 

𝐾 = 𝑋 𝑾 𝑘 

𝑄 = 𝑋 𝑾 𝑞 Holy cow, 

## that’s a lot of 

## new arrows… 

## do we always 

## want/need all 

## of those?  

> 9/4/24 10

𝒒 1 𝒒 2 𝒒 3 𝒒 4

𝒗 1 𝒗 2 𝒗 3 𝒗 4

softmax 

𝒌 1 𝒌 2 𝒌 3 𝒌 4

𝒙 1 𝒙 2 𝒙 3 𝒙 4

𝑾 𝑘 

𝑾 𝑞 

𝑾 𝑣 

𝐴 = softmax 𝑆 

𝑋 ′ = 𝐴𝑉 = softmax 𝑄 𝐾 𝑇 

𝑑 𝑘 

𝑉 

𝑆 = 𝑄 𝐾 𝑇 

𝑑 𝑘 

𝑉 = 𝑋 𝑾 𝑣 

𝐾 = 𝑋 𝑾 𝑘 

𝑄 = 𝑋 𝑾 𝑞 Causal 

## Attention  

> 9/4/24 11

𝒒 1 𝒒 2 𝒒 3 𝒒 4

𝒗 1 𝒗 2 𝒗 3 𝒗 4

softmax 

𝒌 1 𝒌 2 𝒌 3 𝒌 4

𝒙 1 𝒙 2 𝒙 3 𝒙 4

𝑾 𝑘 

𝑾 𝑞 

𝑾 𝑣 

• Suppose we’re training 

our transformer to 

predict the next token(s) 

given the input… 

• … then attending to 

tokens that come after 

the current token is 

cheating! 

𝐴 = softmax 𝑆 

𝑋 ′ = 𝐴𝑉 = softmax 𝑄 𝐾 𝑇 

𝑑 𝑘 

𝑉 Masking  

> 9/4/24 12

𝒒 1 𝒒 2 𝒒 3 𝒒 4

𝒗 1 𝒗 2 𝒗 3 𝒗 4

softmax 

𝒌 1 𝒌 2 𝒌 3 𝒌 4

𝒙 1 𝒙 2 𝒙 3 𝒙 4

𝑾 𝑘 

𝑾 𝑞 

𝑾 𝑣 

𝐴 = softmax 𝑆 

Idea: we can effectively delete or “mask” some of these 

arrows by selectively setting attention weights to 0 

𝑋 ′ = 𝐴𝑉 = softmax 𝑄 𝐾 𝑇 

𝑑 𝑘 

𝑉 Masking  

> 9/4/24 13

𝒒 1 𝒒 2 𝒒 3 𝒒 4

𝒗 1 𝒗 2 𝒗 3 𝒗 4

softmax 

𝒌 1 𝒌 2 𝒌 3 𝒌 4

𝒙 1 𝒙 2 𝒙 3 𝒙 4

𝑾 𝑘 

𝑾 𝑞 

𝑾 𝑣 

𝐴 = softmax 𝑆 

Insight: if some 

element in the input to 

the softmax is -∞, then 

the corresponding 

output is 0!

exp −∞

σ𝑗 exp 𝑠 𝑗 

= 0

σ𝑗 exp 𝑠 𝑗 

Idea: we can effectively delete or “mask” some of these 

arrows by selectively setting attention weights to 0 

𝑋 ′ = 𝐴𝑉 = softmax 𝑄 𝐾 𝑇 

𝑑 𝑘 

𝑉 Which of the 

## mask matrices 

## corresponds to 

## this set of 

## arrows?  

> 9/4/24 14

𝒒 1 𝒒 2 𝒒 3 𝒒 4

𝒗 1 𝒗 2 𝒗 3 𝒗 4

softmax 

𝒌 1 𝒌 2 𝒌 3 𝒌 4

𝒙 1 𝒙 2 𝒙 3 𝒙 4

𝑾 𝑘 

𝑾 𝑞 

𝑾 𝑣 

𝑋 ′ = softmax 𝑄 𝐾 𝑇 

𝑑 𝑘 

+ 𝑀 𝑉 

𝑀  =

0 0 0 0

−∞ 0 0 0

−∞ −∞ 0 0

−∞ −∞ −∞ 0

𝐴 𝑚𝑎𝑠𝑘 = softmax 𝑆 + 𝑀 

𝑀  =

0 −∞ −∞ −∞

0 0 −∞ −∞

0 0 0 −∞

0 0 0 0

𝑀  =

0 −∞ −∞ −∞

−∞ 0 −∞ −∞

−∞ −∞ 0 −∞

−∞ −∞ −∞ 0

A. 

B. 

C. 

Idea: we can effectively delete or “mask” some of these 

arrows by selectively setting attention weights to 0 Masked Scaled 

## Dot -Product 

## Attention: 

## Matrix Form  

> 9/4/24 15

𝒒 1 𝒒 2 𝒒 3 𝒒 4

𝒗 1 𝒗 2 𝒗 3 𝒗 4

softmax 

𝒌 1 𝒌 2 𝒌 3 𝒌 4

𝒙 1 𝒙 2 𝒙 3 𝒙 4

𝑾 𝑘 

𝑾 𝑞 

𝑾 𝑣 

𝑋 ′ = softmax 𝑄 𝐾 𝑇 

𝑑 𝑘 

+ 𝑀 𝑉 

𝐴 𝑚𝑎𝑠𝑘 = softmax 𝑆 + 𝑀 

Idea: we can effectively delete or “mask” some of these 

arrows by selectively setting attention weights to 0 

𝑀  =

0 −∞ −∞ −∞

0 0 −∞ −∞

0 0 0 −∞

0 0 0 0Masked 

## Multi -headed 

## Attention: 

## Matrix Form  

> 9/4/24 16

𝒙 1 𝒙 2 𝒙 3 𝒙 4

𝑾 𝑞 𝑖 

𝑾 𝑘 

𝑖 

𝑾 𝑣 𝑖 

multi -headed attention 

𝒙 1

′ 𝒙 2

′ 𝒙 3

′ 𝒙 4

′

𝑋 ′ = concat 

𝑖 softmax 𝑄 𝑖 𝐾 𝑖 𝑇 

𝑑 𝑘 

+ 𝑀 𝑉 𝑖 

𝑉 𝑖 = 𝑋 𝑾 𝑏 

𝑖 

𝐾 𝑖 = 𝑋 𝑾 𝑘 

𝑖 

𝑄 𝑖 = 𝑋 𝑾 𝑞 𝑖 

where Summary 

## thus Far  

> 9/4/24 17

1. Language Modeling 

 Key idea: condition on previous words to sample the next word 

 To define the probability of the next word, we can… 

 use conditional independence assumption ( 𝑛 -grams) 

 throw a neural network at it (RNN -LM or Transformer -LM) 

2. (Module -based) AutoDiff 

 A tool for computing gradients of a differentiable function, 

𝑏 = 𝑓 (𝑎 )

 Key building block: modules with forward() and backward() 

 Can define 𝑓 as code in forward() by chaining existing 

modules together 

 Can define 𝑓 as a computation graph 1. Language Modeling 

 Key idea: condition on previous words to sample the next word 

 To define the probability of the next word, we can… 

 use conditional independence assumption ( 𝑛 -grams) 

 throw a neural network at it (RNN -LM or Transformer -LM) 

2. (Module -based) AutoDiff 

 A tool for computing gradients of a differentiable function, 

𝑏 = 𝑓 (𝑎 )

 Key building block: modules with forward() and backward() 

 Can define 𝑓 as code in forward() by chaining existing 

modules together 

 Can define 𝑓 as a computation graph 

## Summary 

## thus Far  

> 9/4/24 18

## How can we use this stuff… 

## …to learn one of these? Stochastic 

## Gradient 

## Descent 

 Input: training dataset 𝒟 = 𝒙 𝑛 , 𝑦 𝑛  

> 𝑛 =1
> 𝑁

, step size 𝛾 

1. Randomly initialize the parameters of your neural LM 𝜽 0

and set 𝑡 = 0

2. While TERMINATION CRITERION is not satisfied 

a. Randomly sample a data point from 𝒟 , 𝒙 𝑖 , 𝑦 𝑖 

> 𝑏 =1
> 𝐵

b. Compute the gradient of the loss w.r.t. the sample 

using (module -based) AutoDiff : ∇𝐽 𝑖 𝜽 𝑡 

c. Update 𝜽 : 𝜽 𝑡 +1 ← 𝜽 𝑡 − 𝛾 ∇𝐽 𝑖 𝜽 𝑡 

d. Increment 𝑡 : 𝑡 ← 𝑡 + 1

 Output: 𝜽 𝑡  

> 9/4/24 19

## Mini -batch 

## Stochastic 

## Gradient 

## Descent 

 Input: training dataset 𝒟 = 𝒙 𝑛 , 𝑦 𝑛  

> 𝑛 =1
> 𝑁

, step size 𝛾 ,

and batch size 𝐵 

1. Randomly initialize the parameters of your neural LM 𝜽 0

and set 𝑡 = 0

2. While TERMINATION CRITERION is not satisfied 

a. Randomly sample 𝐵 data points from 𝒟 , 𝒙 𝑏 , 𝑦 𝑏 

> 𝑏 =1
> 𝐵

b. Compute the gradient of the loss w.r.t. the sampled batch 

using (module -based) AutoDiff : ∇𝐽 𝐵 𝜽 𝑡 

c. Update 𝜽 : 𝜽 𝑡 +1 ← 𝜽 𝑡 − 𝛾 ∇𝐽 𝐵 𝜽 𝑡 

d. Increment 𝑡 : 𝑡 ← 𝑡 + 1

 Output: 𝜽 𝑡  

> 9/4/24 20

 How do we train an 𝑛 -gram language model? 

 Using training data! Simply count frequency of next words, 

which maximizes the likelihood of the data under the 

various categorial distributions in the model 

## Recall: 

## 𝑛 -gram 

## Language 

## Model 

## Training 

> 9/4/24

Narwhals are big aquatic mammals that… 

Who knows what narwhals are hiding? 

Watch out, the narwhals are coming! 

These narwhals are friendly! 

Narwhals are a surprisingly large part of this lecture. 

The narwhals are a punk rock band from… 

Narwhals are big fans of machine learning 

Narwhals are generated by AI. 

𝒙 𝒕  𝒑 𝒙 𝒕 𝐧𝐚𝐫𝐰𝐡𝐚𝐥𝐬 , 𝐚𝐫𝐞 

big  2/8 

hiding  1/8 

coming  1/8 

friendly  1/8 

a 2/8 

generated  1/8 

> 21

 How do we train an 𝑛 -gram language model? 

 Using training data! Simply count frequency of next words, 

which maximizes the likelihood of the data under the 

various categorial distributions in the model We can use the 

## same principle 

## of MLE to 

## optimize the 

## parameters of 

## our Neural LMs! 

> 9/4/24

Narwhals are big aquatic mammals that… 

Who knows what narwhals are hiding? 

Watch out, the narwhals are coming! 

These narwhals are friendly! 

Narwhals are a surprisingly large part of this lecture. 

The narwhals are a punk rock band from… 

Narwhals are big fans of machine learning 

Narwhals are generated by AI. 

𝒙 𝒕  𝒑 𝒙 𝒕 𝐧𝐚𝐫𝐰𝐡𝐚𝐥𝐬 , 𝐚𝐫𝐞 

big  2/8 

hiding  1/8 

coming  1/8 

friendly  1/8 

a 2/8 

generated  1/8 

> 22

## Recurrent 

## Neural 

## Networks 

> 9/4/24

ℎ𝑡 = 𝜙 𝑊 𝑥ℎ 𝑥 𝑡 + 𝑊 ℎℎ ℎ𝑡 −1 + 𝑏 ℎ

𝑥 1

ℎ1

𝑦 1

𝑥 2

ℎ2

𝑦 2

𝑥 3

ℎ3

𝑦 3

𝑥 4

ℎ4

𝑦 4

𝑥 5

ℎ5

𝑦 5

ℎ0

Inputs 

Hidden 

Units 

Outputs 

> 23

𝑦 𝑡 = 𝜓 𝑊 ℎ𝑦 ℎ𝑡 + 𝑏 𝑦 Recurrent 

## Neural 

## Networks for 

## Part of Speech 

## Tagging 

> 9/4/24

ℎ1 ℎ2 ℎ3 ℎ4 ℎ5ℎ0

Hidden 

Units 

Outputs, 𝒚 

> 24

𝑥 2    

> A V N P… A V N P… A V N P… A V N P… A V N P…

are  generated  by Narwhals 

ℎ𝑡 = 𝜙 𝑊 𝑥ℎ 𝑥 𝑡 + 𝑊 ℎℎ ℎ𝑡 −1 + 𝑏 ℎ

𝑦 𝑡 = softmax 𝑊 ℎ𝑦 ℎ𝑡 + 𝑏 𝑦 

Labels, 𝒚 ∗

Inputs, 𝒙 

Verb  Preposition Noun 

AI 

Noun Verb Recurrent 

## Neural 

## Networks for 

## Part of Speech 

## Tagging 

> 9/4/24

ℎ1 ℎ2 ℎ3 ℎ4 ℎ5ℎ0

Hidden 

Units 

Outputs, 𝒚 

𝑥 2

A V N … 

are  generated  by Narwhals 

ℎ𝑡 = 𝜙 𝑊 𝑥ℎ 𝑥 𝑡 + 𝑊 ℎℎ ℎ𝑡 −1 + 𝑏 ℎ

𝑦 𝑡 = softmax 𝑊 ℎ𝑦 ℎ𝑡 + 𝑏 𝑦 

Labels, 𝒚 ∗

Inputs, 𝒙  AI 

A V N P…  A V N P…  A V N P… 

0 0 1 0 0 1 0 0 0 1 0 0

A V N P… 

0 0 0 1

A V N P… 

0 0 1 0

0.1  0.2  0.5  …

A V N … 

0.1  0.7  0.1  …

A V N … 

0.4  0.4  0.1  …

A V N … 

0.2  0.1  0.1  …

A V N … 

0.3  0.1  0.5  …

> 25

 Intuition: we want the true label to have high 

probability under the output distribution 

 Idea: use 𝒚 ∗ to index into the desired element of 𝒚 

## Recurrent 

## Neural 

## Networks for 

## Part of Speech 

## Tagging 

> 9/4/24

ℎ1 ℎ2 ℎ3 ℎ4 ℎ5ℎ0

Hidden 

Units 

Outputs, 𝒚 

𝑥 2

A V N … 

are  generated  by Narwhals 

ℎ𝑡 = 𝜙 𝑊 𝑥ℎ 𝑥 𝑡 + 𝑊 ℎℎ ℎ𝑡 −1 + 𝑏 ℎ

𝑦 𝑡 = softmax 𝑊 ℎ𝑦 ℎ𝑡 + 𝑏 𝑦 

Labels, 𝒚 ∗

Inputs, 𝒙  AI 

A V N P…  A V N P…  A V N P… 

0 0 1 0 0 1 0 0 0 1 0 0

A V N P… 

0 0 0 1

A V N P… 

0 0 1 0

0.1  0.2  0.5  …

A V N … 

0.1  0.7  0.1  …

A V N … 

0.4  0.4  0.1  …

A V N … 

0.2  0.1  0.1  …

A V N … 

0.3  0.1  0.5  …

> 26

## Recurrent 

## Neural 

## Networks for 

## Part of Speech 

## Tagging 

> 9/4/24

ℎ1 ℎ2 ℎ3 ℎ4 ℎ5ℎ0

Hidden 

Units 

Outputs, 𝒚 

𝑥 2

A V N … 

are  generated  by Narwhals 

ℎ𝑡 = 𝜙 𝑊 𝑥ℎ 𝑥 𝑡 + 𝑊 ℎℎ ℎ𝑡 −1 + 𝑏 ℎ

𝑦 𝑡 = softmax 𝑊 ℎ𝑦 ℎ𝑡 + 𝑏 𝑦 

Labels, 𝒚 ∗

Inputs, 𝒙  AI 

A V N P…  A V N P…  A V N P… 

0 0 1 0 0 1 0 0 0 1 0 0

A V N P… 

0 0 0 1

A V N P… 

0 0 1 0

0.1  0.2  0.5  …

A V N … 

0.1  0.7  0.1  …

A V N … 

0.4  0.4  0.1  …

A V N … 

0.2  0.1  0.1  …

A V N … 

0.3  0.1  0.5  …

maximize  ෍

𝑐 =1

𝐶 

𝒚 𝑡 

∗ 𝑐  log  𝒚 𝑡  𝑐 

> 27

## Recurrent 

## Neural 

## Networks for 

## Part of Speech 

## Tagging 

> 9/4/24

ℎ1 ℎ2 ℎ3 ℎ4 ℎ5ℎ0

Hidden 

Units 

Outputs, 𝒚 

𝑥 2

A V N … 

are  generated  by Narwhals 

ℎ𝑡 = 𝜙 𝑊 𝑥ℎ 𝑥 𝑡 + 𝑊 ℎℎ ℎ𝑡 −1 + 𝑏 ℎ

𝑦 𝑡 = softmax 𝑊 ℎ𝑦 ℎ𝑡 + 𝑏 𝑦 

Labels, 𝒚 ∗

Inputs, 𝒙  AI 

A V N P…  A V N P…  A V N P… 

0 0 1 0 0 1 0 0 0 1 0 0

A V N P… 

0 0 0 1

A V N P… 

0 0 1 0

0.1  0.2  0.5  …

A V N … 

0.1  0.7  0.1  …

A V N … 

0.4  0.4  0.1  …

A V N … 

0.2  0.1  0.1  …

A V N … 

0.3  0.1  0.5  …

minimize  ℓ𝑡  = − ෍

𝑐 =1

𝐶 

𝒚 𝑡 

∗ 𝑐  log  𝒚 𝑡  𝑐 

> 28

## Recurrent 

## Neural 

## Networks for 

## Part of Speech 

## Tagging 

> 9/4/24

ℎ1 ℎ2 ℎ3 ℎ4 ℎ5ℎ0

Hidden 

Units 

Outputs, 𝒚 

𝑥 2

A V N … 

are  generated  by Narwhals 

ℎ𝑡 = 𝜙 𝑊 𝑥ℎ 𝑥 𝑡 + 𝑊 ℎℎ ℎ𝑡 −1 + 𝑏 ℎ

𝑦 𝑡 = softmax 𝑊 ℎ𝑦 ℎ𝑡 + 𝑏 𝑦 

Labels, 𝒚 ∗

Inputs, 𝒙  AI 

A V N P…  A V N P…  A V N P… 

0 0 1 0 0 1 0 0 0 1 0 0

A V N P… 

0 0 0 1

A V N P… 

0 0 1 0

0.1  0.2  0.5  …

A V N … 

0.1  0.7  0.1  …

A V N … 

0.4  0.4  0.1  …

A V N … 

0.2  0.1  0.1  …

A V N … 

0.3  0.1  0.5  …

minimize  𝐽  = ෍

𝑡 =1

𝑇 

ℓ𝑡  = ෍

𝑡 =1

𝑇 

− ෍

𝑐 =1

𝐶 

𝒚 𝑡 

∗ 𝑐  log  𝒚 𝑡  𝑐 

> 29

## Recurrent 

## Neural 

## Network 

## Language 

## Models: 

## Loss 

> 9/4/24

ℎ1 ℎ2 ℎ3 ℎ4 ℎ5ℎ0

Hidden 

Units 

Outputs? 

𝑥 2are  generated  by Narwhals 

ℎ𝑡 = 𝜙 𝑊 𝑥ℎ 𝑥 𝑡 + 𝑊 ℎℎ ℎ𝑡 −1 + 𝑏 ℎ

𝑦 𝑡 = softmax 𝑊 ℎ𝑦 ℎ𝑡 + 𝑏 𝑦 

Labels? 

Inputs, 𝒙  AI 

minimize  𝐽  = ෍

𝑡 =1

𝑇 

ℓ𝑡  = ෍

𝑡 =1

𝑇 

− ෍

𝑐 =1

𝐶 

𝒚 𝑡 

∗ 𝑐  log  𝒚 𝑡  𝑐 

> 30

## Recurrent 

## Neural 

## Network 

## Language 

## Models: 

## Loss 

> 9/4/24

ℎ1 ℎ2 ℎ3 ℎ4 ℎ5ℎ0

Hidden 

Units 

𝑥 2are  generated  by Narwhals 

ℎ𝑡 = 𝜙 𝑊 𝑥ℎ 𝑥 𝑡 + 𝑊 ℎℎ ℎ𝑡 −1 + 𝑏 ℎ

𝑦 𝑡 = softmax 𝑊 ℎ𝑦 ℎ𝑡 + 𝑏 𝑦 

Inputs, 𝒙  AI 

minimize  𝐽  = ෍

𝑡 =1

𝑇 

ℓ𝑡  = ෍

𝑡 =1

𝑇 

− ෍

𝑐 =1

𝐶 

𝒚 𝑡 

∗ 𝑐  log  𝒚 𝑡  𝑐 

Outputs, 𝒚 

Labels, 𝒚 ∗ are  generated  by  AI  ???  31 Recurrent 

## Neural 

## Network 

## Language 

## Models: 

## Loss 

> 9/4/24

ℎ1 ℎ2 ℎ3 ℎ4 ℎ5ℎ0

Hidden 

Units 

𝑥 2are  generated  by Narwhals 

ℎ𝑡 = 𝜙 𝑊 𝑥ℎ 𝑥 𝑡 + 𝑊 ℎℎ ℎ𝑡 −1 + 𝑏 ℎ

𝑦 𝑡 = softmax 𝑊 ℎ𝑦 ℎ𝑡 + 𝑏 𝑦 

Inputs, 𝒙  AI 

minimize  𝐽  = ෍

𝑡 =1

𝑇 

ℓ𝑡  = ෍

𝑡 =1

𝑇 

− ෍

𝑐 =1

𝐶 

𝒚 𝑡 

∗ 𝑐  log  𝒚 𝑡  𝑐 

Outputs, 𝒚 

Labels, 𝒚 ∗ are  generated  by  AI  EOS  32 Recurrent 

## Neural 

## Network 

## Language 

## Models: 

## Loss 

> 9/4/24

ℎ2 ℎ3 ℎ4 ℎ5 ℎ6

𝑥 2are  generated  by Narwhals 

ℎ𝑡 = 𝜙 𝑊 𝑥ℎ 𝑥 𝑡 + 𝑊 ℎℎ ℎ𝑡 −1 + 𝑏 ℎ

𝑦 𝑡 = softmax 𝑊 ℎ𝑦 ℎ𝑡 + 𝑏 𝑦 

AI 

minimize  𝐽  = ෍

𝑡 =1

𝑇 

ℓ𝑡  = ෍

𝑡 =1

𝑇 

− ෍

𝑐 =1

𝐶 

𝒚 𝑡 

∗ 𝑐  log  𝒚 𝑡  𝑐 

are  generated  by  AI  EOS 

ℎ1ℎ0

SOS 

Narwhals  33 Recurrent 

## Neural 

## Network 

## Language 

## Models: 

## Training 

 Each training data point is a sequence 𝒙 (𝑖 ) = 𝒙 1

> (𝑖 )

, … , 𝒙 𝑇 𝑖 

> (𝑖 )

 The objective function is the log -likelihood of a mini -batch: 

𝐽  𝐵  𝜽  = log  ෑ

> 𝑏 =1
> 𝐵

𝑝 𝜽 (𝒙  𝑏  ) = ෍

> 𝑏 =1
> 𝐵

log  𝑝 𝜽 (𝒙  𝑏  )

(assuming i.i.d. sequences) where 

log 𝑝 𝜽 (𝒙 𝑏 ) ≔ log 𝑝 𝜽 𝒙 1 

> 𝑏

𝒉 1 + ⋯ + log 𝑝 𝜽 𝒙 𝑇 𝑏  

> 𝑏

𝒉 𝑇 𝑏 

log 𝑝 𝜽 (𝒙 𝑏 ) ≔ 𝑙 1 + ⋯ + 𝑙 𝑇 𝑏  

> 9/4/24 34

## Recurrent 

## Neural 

## Network 

## Language 

## Models: 

## Training 

> 9/4/24

ℎ2 ℎ3 ℎ4

𝑥 2are  generated  EOS Narwhals 

ℎ1ℎ0

SOS 

ℓ2 ℓ3 ℓ4ℓ1

> 35

𝐽 Transformer Layer 

## Transformer 

## Language 

## Models: 

## Training     

> 9/4/24
> 𝑥 2are generated EOS Narwhals SOS
> ℓ2ℓ3ℓ4ℓ1
> 36
> 𝐽

## Key Takeaway: Training a transformer 

## LM is equivalent to training an RNN LM: 

## we use the same loss function and 

## optimization algorithms, just with a 

## different (differentiable) computation 

## graph in the middle Transformer Layer 

## Are we really 

## passing in 

## “words” to this 

## transformer? 

> 9/4/24

𝑥 2are  generated  EOS Narwhals SOS 

ℓ2 ℓ3 ℓ4ℓ1

> 37

𝐽  How can we break a sequence of text into individual units? 

 Example: “Henry is giving a lecture on transformers” 

 Word -based tokenization: 

[“henry”, “is”, ”giving” “a”, “lecture”, “on”, “transformers”] 

 Can have difficulty trading off between vocabulary 

size and computational tractability 

 Similar words e.g., “transformers” and “transformer” 

can get mapped to completely disparate 

representations 

 Typos will typically be out -of -vocabulary (OOV) 

## Tokenization  

> 9/4/24 38

## Tokenization  

> 9/4/24 39

 How can we break a sequence of text into individual units? 

 Example: “Henry is givin ’ a lectrue on transformers” 

 Word -based tokenization: 

[“henry”, “is”, ???, “a”, ???, “on”, “transformers”] 

 Can have difficulty trading off between vocabulary 

size and computational tractability 

 Similar words e.g., “transformers” and “transformer” 

can get mapped to completely disparate 

representations 

 Typos will typically be out -of -vocabulary (OOV) Tokenization  

> 9/4/24 40

 How can we break a sequence of text into individual units? 

 Example: “Henry is givin ’ a lectrue on transformers” 

 Character -based tokenization: 

[“h”, “e”, “n”, “r”, “y”, “ i”, “s”, “g”, “ i”, “v”, “ i”, “n”, “ ’ ”, … ] 

 Much smaller vocabularies but a lot of semantic 

meaning is lost… 

 Sequences will be much longer than word -based 

tokenization, potentially causing computational issues 

 Can do well on logographic languages e.g., Kanji  漢字 Tokenization  

> 9/4/24 41

 How can we break a sequence of text into individual units? 

 Example: “Henry is givin ’ a lectrue on transformers” 

 Subword tokenization: 

[“henry”, “is”, “ giv ”, “##in”, “ ‘ ”, “a”, “ lect ”, “#u”, “##re”, “on”, 

“transform”, “## ers ”] 

 Split long or rare words into smaller, semantically 

meaningful components or subwords 

 No out -of -vocabulary words – any non -subword 

token can be constructed from other subwords 

(all individual characters are subwords )Okay, but these 

## are still strings: 

## how do I 

## convert these 

## into things my 

## transformer 

## can work with?  

> 9/4/24 42

 How can we break a sequence of text into individual units? 

 Example: “Henry is givin ’ a lectrue on transformers” 

 Subword tokenization: 

[“henry”, “is”, “ giv ”, “##in”, “ ‘ ”, “a”, “ lect ”, “#u”, “##re”, “on”, 

“transform”, “## ers ”] 

 Split long or rare words into smaller, semantically 

meaningful components or subwords 

 No out -of -vocabulary words – any non -subword token 

can be constructed from other subwords (all 

individual characters are subwords )Embeddings  

> 9/4/24 43

 Given a vocabulary 𝑉 with 𝑉 tokens: 

1. Map each token to a (non -negative) integer 

2. Define a 𝑉 × 𝑑 𝑒 lookup table, where each row 

is a dense, numerical vector of length 𝑑 𝑒 

3. The row corresponding to each token’s integer 

assignment is that token’s embedding Are we really 

## passing in 

## “words” to this 

## transformer?  

> 9/4/24 44

are  generated  EOS Narwhals SOS 

Transformer Layer 

ℓ2 ℓ3 ℓ4ℓ1

𝐽 Transformer Layer 

## Are we really 

## passing in 

## “words” to this 

## transformer? 

## NO  

> 9/4/24

generat  #ed Narwhal SOS 

ℓ2 ℓ3 ℓ4ℓ1

> 45

𝐽 

#s  EOS 

50  787 1 11  128 12 

are 

ℓ5 ℓ6

2.1  4.3  7.1  3.2  1.1  0.7  0.1  0.5  1.8  2.2  8.0  5.5  3.8  3.8  1.0  7.6  6.5  5.4 Recall: 

## Transformer 

## Computational 

## Complexity    

> 46
> x1x2x3x4
> p(w 1|h 1)
> h1
> p(w 2|h 2)
> h2
> p(w 3|h 3)
> h3
> p(w 4|h 4)
> h4

## …

Important! 

• RNN computation 

graph grows linearly 

with the number of 

input tokens 

• Transformer LM 

computation graph 

grows quadratically 

with the number of 

input tokens 

• However, this 

computation (and 

therefore, the training 

of transformer LMs) is 

highly parallelizable 

> 9/4/24

## Parallelizing 

## Transformer LM 

## Computation 

 Scaled dot -product attention can be easily parallelized 

because the attention scores at one timestep do not 

depend on other timesteps. 

 In multi -headed attention , each head is also independent 

of the other heads, which permits yet more parallelism. 

 The core computation in attention is matrix multiplication ,

and GPUs/TPUs make this very fast. 

 Model parallelism: for large models, we can divide the 

model over multiple GPUs/machines. 

 Key -value caching : keys and values are re -used over many 

timesteps so we can cache them for faster access 

 Batching : rather than process one sequence at a time, 

transformers take in a batch ; the computation is identical 

for each sequence (if they’re of the same length)  

> 9/4/24 47

## Parallelizing 

## Transformer LM 

## Computation 

 Scaled dot -product attention can be easily parallelized 

because the attention scores at one timestep do not 

depend on other timesteps. 

 In multi -headed attention , each head is also independent 

of the other heads, which permits yet more parallelism. 

 The core computation in attention is matrix multiplication ,

and GPUs/TPUs make this very fast. 

 Model parallelism: for large models, we can divide the 

model over multiple GPUs/machines. 

 Key -value caching : keys and values are re -used over many 

timesteps so we can cache them for faster access 

 Batching : rather than process one sequence at a time, 

transformers take in a batch ; the computation is identical 

for each sequence (if they’re of the same length)  

> 9/4/24 48

## Batching: 

## Padding & 

## Truncation 

𝒙 1 

> (𝑖 )

𝒙 𝟐  

> (𝑖 )

𝒙 𝟑  

> (𝑖 )

𝒙 𝟒  

> (𝑖 )

𝒙 𝟓  

> (𝑖 )

𝒙 𝟔  

> (𝑖 )

𝒙 𝟕  

> (𝑖 )

𝒙 𝟖  

> (𝑖 )

𝒙 𝟗  

> (𝑖 )

𝒙 1𝟎 

> (𝑖 )

Narwhals  are  generated  by  AI 

Watch  out  , the  narwhals  are  coming  !

How  many  sequences  contain  “ narwhals  are  ” ?

Narwhals  are  way  cooler  than  axolotls 

Of  the  large  aquatic  mammals  , narwhals  are  the  best 

Who  knows  what  the  narwhals  are  hiding  ? 

> 9/4/24 49

 Given a block size or maximum length, 𝐿 (typically a power of 2): 

 Truncate sequences longer than 𝐿 by deleting excess tokens 

 Pad sequences shorter than 𝐿 by adding PAD tokens Batching: 

## Padding & 

## Truncation  

> 9/4/24 50

 Given a block size or maximum length, 𝐿 (typically a power of 2): 

 Truncate sequences longer than 𝐿 by deleting excess tokens 

 Pad sequences shorter than 𝐿 by adding PAD tokens 

𝒙 1 

> (𝑖 )

𝒙 𝟐  

> (𝑖 )

𝒙 𝟑  

> (𝑖 )

𝒙 𝟒  

> (𝑖 )

𝒙 𝟓  

> (𝑖 )

𝒙 𝟔  

> (𝑖 )

𝒙 𝟕  

> (𝑖 )

𝒙 𝟖 

> (𝑖 )

Narwhals  are  generated  by  AI 

Watch  out  , the  narwhals  are  coming  !

How  many  sequences  contain  “ narwhals  are  ”

Narwhals  are  way  cooler  than  axolotls 

Of  the  large  aquatic  mammals  , narwhals  are 

Who  knows  what  the  narwhals  are  hiding  ?Batching: 

## Padding & 

## Truncation  

> 9/4/24 51

 Given a block size or maximum length, 𝐿 (typically a power of 2): 

 Truncate sequences longer than 𝐿 by deleting excess tokens 

 Pad sequences shorter than 𝐿 by adding PAD tokens 

𝒙 1 

> (𝑖 )

𝒙 𝟐  

> (𝑖 )

𝒙 𝟑  

> (𝑖 )

𝒙 𝟒  

> (𝑖 )

𝒙 𝟓  

> (𝑖 )

𝒙 𝟔  

> (𝑖 )

𝒙 𝟕  

> (𝑖 )

𝒙 𝟖 

> (𝑖 )

Narwhals  are  generated  by  AI  PAD  PAD  PAD 

Watch  out  , the  narwhals  are  coming  !

How  many  sequences  contain  “ narwhals  are  ”

Narwhals  are  way  cooler  than  axolotls  PAD  PAD 

Of  the  large  aquatic  mammals  , narwhals  are 

Who  knows  what  the  narwhals  are  hiding  ? How do we generate new sequences using an RNN 

language model? 

 Exactly the same way we did for an 𝑛 -gram language 

model, by sampling from some learned probability 

distributions over next words! 

## Recall: 

## Language 

## Model 

## Generation 

> 9/4/24

Narwhals 

ℎ1

are 

ℎ2

way 

ℎ3

cooler 

ℎ4

than 

ℎ5ℎ0

Inputs 

Hidden 

Units 

Outputs 

> 52

 How do we generate new sequences using a transformer 

language model? 

 Exactly the same way we did for an RNN language 

model, by sampling from some learned probability 

distributions over next words! 

## Recall: 

## Language 

## Model 

## Generation 

> 9/4/24

Narwhals  are  way  cooler  than Inputs 

Outputs 

> 53

Transformer Layer  How do we generate new sequences using a transformer 

language model? 

 Exactly the same way we did for an RNN language 

model, by sampling from some learned probability 

distributions over next words! 

## Is this the 

## only thing we 

## could do? 

> 9/4/24

Narwhals  are  way  cooler  than Inputs 

Outputs 

> 54

Transformer Layer Background: 

## Greedy Search  

> 55
> Start
> State
> End
> States
> 2
> 4
> 3
> 17
> 3
> 3
> 5
> 4
> 1
> 2
> 2
> 3
> 5
> 6
> 4
> 7
> 8
> 9
> 8

• Goal : find the lowest (total) weight path from the Start State 

to any End State  • Greedy Search :

• At each node, select 

the edge with 

lowest weight 

• Heuristic : does not 

necessarily find the 

lowest weight path 

> 9/4/24

## Background: 

## Greedy Search  

> 56
> Start
> State
> End
> States
> 2
> 4
> 3
> 17
> 3
> 3
> 5
> 4
> 1
> 2
> 2
> 3
> 5
> 6
> 4
> 7
> 8
> 9
> 8

• Greedy Search :

• At each node, select 

the edge with 

lowest weight 

• Heuristic : does not 

necessarily find the 

lowest weight path 

• Goal : find the lowest (total) weight path from the Start State 

to any End State 

> 9
> 9
> 1
> 9
> 9/4/24

## Background: 

## Greedy Search  

> 57
> Start
> State
> End
> States
> 2
> 4
> 3
> 17
> 3
> 3
> 5
> 4
> 1
> 2
> 2
> 3
> 5
> 6
> 4
> 7
> 8
> 9
> 8

• Goal : find the lowest (total) weight path from the Start State 

to any End State 

> 9
> 9
> 1
> 9
> 7
> 1
> 3
> 5
> 2
> 1
> 2
> 2
> 5
> 3
> 1
> 5

• Greedy Search :

• At each node, select 

the edge with 

lowest weight 

• Heuristic : does not 

necessarily find the 

lowest weight path 

• Computation time is 

linear in max path 

length 

> 9/4/24

• Goal : find the highest probability sequence of tokens 

• Nodes are tokens and weights are (negative) log probabilities 

• At each node, select 

the edge with 

lowest negative log 

probability 

• Heuristic : does not 

necessarily find the 

highest probability 

output 

• Computation time 

is linear in the 

maximum path 

length 

## Greedy 

## Decoding for 

## Language 

## Models 

> 58
> T
> Start
> State
> End
> States
> A
> E
> R
> 2
> 4
> 3
> 1
> I
> A
> Y
> 7
> 3
> 3
> 5
> C
> N
> D
> M
> 4
> 1
> 2
> 2
> S
> K
> Q
> 3
> 5
> 6
> 4
> F
> D
> C
> I
> 7
> 8
> 9
> 8
> Y
> E
> S
> 9
> 9
> 1
> 9
> C
> G
> R
> N
> E
> 7
> 1
> 3
> 5
> C
> N
> Q
> T
> 2
> 1
> 2
> 2
> E
> S
> H
> A
> 5
> 3
> 1
> 5
> O
> 9/4/24

• Goal : find the highest probability sequence of tokens 

• Nodes are tokens and weights are (negative) log probabilities 

• At each node, 

sample an edge 

with probability 

proportional to the 

negative exp’ed 

weights 

• Exact method of 

sampling 

• Computation time 

is linear in the 

maximum path 

length 

## Ancestral 

## Sampling for 

## Language 

## Models