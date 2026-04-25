# Source: https://cs231n.stanford.edu/slides/2025/lecture_8.pdf
# Author: Stanford CS231n
# Author Slug: stanford-cs231n
# Title: [PDF] Lecture 8: Attention and Transformers - CS231n
# Fetched via: jina
# Date: 2026-04-11

Title: lecture_8.pdf



Number of Pages: 122

Stanford CS231n 10 th Anniversary  April 24, 2025 Lecture 8 - 1

# Lecture 8: 

# Attention and Transformers Stanford CS231n 10 th Anniversary  April 24, 2025 Lecture 8 -

# Administrative 

● Assignment 2 released yesterday (4/23) 

● Project proposals are due tomorrow (4/25) 

2Stanford CS231n 10 th Anniversary  April 24, 2025 Lecture 8 -

# Last Time: Recurrent Neural Networks 

3Stanford CS231n 10 th Anniversary  April 24, 2025 Lecture 8 -

# Today: Attention + Transformers 

4

Attention : A new primitive that 

operates on sets of vectors 

Transformer : A neural 

network architecture that 

uses attention everywhere Stanford CS231n 10 th Anniversary  April 24, 2025 Lecture 8 -

# Today: Attention + Transformers 

5

Attention : A new primitive that 

operates on sets of vectors 

Transformers are used 

everywhere today! 

But they developed as 

an offshoot of RNNs 

so let’s start there 

Transformer : A neural 

network architecture that 

uses attention everywhere Stanford CS231n 10 th Anniversary  April 24, 2025 Lecture 8 -

x1 x2 x3

h1 h2 h3

x4

h4

Input : Sequence x 1, … x T

Output : Sequence y 1, …, y T’ 

> Sutskever et al, “Sequence to sequence learning with neural networks”, NeurIPS 2014

Encoder: ht = f W(x t, h t-1)

## Sequence to Sequence with RNNs: Encoder - Decoder 

6

A motivating example for today’s discussion –

machine translation! English → Italian 

we  see  the  sky Stanford CS231n 10 th Anniversary  April 24, 2025 Lecture 8 -

x1 x2 x3

h1 h2 h3 s0

x4

h4

c

Input : Sequence x 1, … x T

Output : Sequence y 1, …, y T’ 

> Sutskever et al, “Sequence to sequence learning with neural networks”, NeurIPS 2014

Encoder: ht = f W(x t, h t-1)

From final hidden state predict: 

Initial decoder state s0

Context vector c (often c=h T)

## Sequence to Sequence with RNNs 

7

we  see  the  sky Stanford CS231n 10 th Anniversary  April 24, 2025 Lecture 8 -

s1

x1 x2 x3

h1 h2 h3 s0

[START] 

y0

y1

x4

h4

vediamo 

c

Input : Sequence x 1, … x T

Output : Sequence y 1, …, y T’ 

> Sutskever et al, “Sequence to sequence learning with neural networks”, NeurIPS 2014

Encoder: ht = f W(x t, h t-1)

Decoder: st = g U(y t-1, s t-1, c) 

From final hidden state predict: 

Initial decoder state s0

Context vector c (often c=h T)

## Sequence to Sequence with RNNs 

8

we  see  the  sky Stanford CS231n 10 th Anniversary  April 24, 2025 Lecture 8 -

s1

x1

we  see  the 

x2 x3

h1 h2 h3 s0 s2

[START] 

y0 y1

y1 y2

sky 

x4

h4

vediamo 

vediamo 

c

Input : Sequence x 1, … x T

Output : Sequence y 1, …, y T’ 

> Sutskever et al, “Sequence to sequence learning with neural networks”, NeurIPS 2014

Encoder: ht = f W(x t, h t-1)

Decoder: st = g U(y t-1, s t-1, c) 

From final hidden state predict: 

Initial decoder state s0

Context vector c (often c=h T)

## Sequence to Sequence with RNNs 

9

il Stanford CS231n 10 th Anniversary  April 24, 2025 Lecture 8 -

s1

x1 x2 x3

h1 h2 h3 s0 s2

[START] 

y0 y1

y1 y2

x4

h4

vediamo  il 

cielo 

y2 y3

vediamo  il 

s3 s4

y3 y4

cielo  [STOP] 

c

Input : Sequence x 1, … x T

Output : Sequence y 1, …, y T’ 

> Sutskever et al, “Sequence to sequence learning with neural networks”, NeurIPS 2014

Encoder: ht = f W(x t, h t-1)

Decoder: st = g U(y t-1, s t-1, c) 

From final hidden state predict: 

Initial decoder state s0

Context vector c (often c=h T)

## Sequence to Sequence with RNNs 

10 

we  see  the  sky Stanford CS231n 10 th Anniversary  April 24, 2025 Lecture 8 -

s1

x1 x2 x3

h1 h2 h3 s0 s2

[START] 

y0 y1

y1 y2

x4

h4

y2 y3

s3 s4

y3 y4

[STOP] 

c

Input : Sequence x 1, … x T

Output : Sequence y 1, …, y T’ 

> Sutskever et al, “Sequence to sequence learning with neural networks”, NeurIPS 2014

Encoder: ht = f W(x t, h t-1)

Decoder: st = g U(y t-1, s t-1, c) 

From final hidden state predict: 

Initial decoder state s0

Context vector c (often c=h T)

## Sequence to Sequence with RNNs 

11 

Problem: Input sequence 

bottlenecks through fixed 

sized c. What if T=1000? 

we  see  the  sky  cielo vediamo  il 

vediamo  il  cielo Stanford CS231n 10 th Anniversary  April 24, 2025 Lecture 8 -

s1

x1 x2 x3

h1 h2 h3 s0 s2

[START] 

y0 y1

y1 y2

x4

h4

y2 y3

s3 s4

y3 y4

[STOP] 

c

Input : Sequence x 1, … x T

Output : Sequence y 1, …, y T’ 

> Sutskever et al, “Sequence to sequence learning with neural networks”, NeurIPS 2014

Encoder: ht = f W(x t, h t-1)

Decoder: st = g U(y t-1, s t-1, c) 

From final hidden state predict: 

Initial decoder state s0

Context vector c (often c=h T)

## Sequence to Sequence with RNNs 

12 

Solution : Look back at the 

whole input sequence on 

each step of the output 

we  see  the  sky  cielo vediamo  il 

vediamo  il  cielo Stanford CS231n 10 th Anniversary  April 24, 2025 Lecture 8 -

x1 x2 x3

h1 h2 h3 s0

x4

h4

> Bahdanau et al, “Neural machine translation by jointly learning to align and translate”, ICLR 2015

Input : Sequence x 1, … x T

Output : Sequence y 1, …, y T’ 

Encoder: ht = f W(x t, h t-1) From final hidden state: 

Initial decoder state s0

## Sequence to Sequence with RNNs and Attention 

13 

we  see  the  sky Stanford CS231n 10 th Anniversary  April 24, 2025 Lecture 8 -

x1 x2 x3

h1 h2 h3 s0

x4

h4

e11  e12  e13  e14 

Bahdanau et al, “Neural machine translation by jointly learning to align and translate”, ICLR 2015 

Compute (scalar) alignment scores 

et,i = f att (s t-1, h i) (f att is a Linear Layer) 

## Sequence to Sequence with RNNs and Attention 

From final hidden state: 

Initial decoder state s0

14 

we  see  the  sky Stanford CS231n 10 th Anniversary  April 24, 2025 Lecture 8 -

x1 x2 x3

h1 h2 h3 s0

x4

h4

e11  e12  e13  e14 

softmax 

a11  a12  a13  a14 

Normalize alignment scores 

to get attention weights 

0 < a t,i < 1 ∑iat,i = 1 

> Bahdanau et al, “Neural machine translation by jointly learning to align and translate”, ICLR 2015

## Sequence to Sequence with RNNs and Attention 

15 

Compute (scalar) alignment scores 

et,i = f att (s t-1, h i) (f att is a Linear Layer) 

From final hidden state: 

Initial decoder state s0

we  see  the  sky Stanford CS231n 10 th Anniversary  April 24, 2025 Lecture 8 -

x1 x2 x3

h1 h2 h3 s0

x4

h4

e11  e12  e13  e14 

softmax 

a11  a12  a13  a14 

c1

+

vediamo 

Compute context vector as 

weighted sum of hidden 


ct = ∑ iat,i hi

> Bahdanau et al, “Neural machine translation by jointly learning to align and translate”, ICLR 2015

## Sequence to Sequence with RNNs and Attention 

From final hidden state: 

Initial decoder state s0

16 

Compute (scalar) alignment scores 

et,i = f att (s t-1, h i) (f att is a Linear Layer) 

Normalize alignment scores 

to get attention weights 

0 < a t,i < 1 ∑iat,i = 1 

we  see  the  sky Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

x1 x2 x3

h1 h2 h3 s0

x4

h4

e11  e12  e13  e14 

softmax 

a11  a12  a13  a14 

c1

+ s1

y0

y1

Compute context vector as 

weighted sum of hidden 


ct = ∑iat,i hi

Use context vector in 

decoder: s t = g U(y t-1, s t-1, c t)  

> Bahdanau et al, “Neural machine translation by jointly learning to align and translate ”, ICLR 2015

[START] 

## Sequence to Sequence with RNNs and Attention 

From final hidden state: 

Initial decoder state s0

17 

Normalize alignment scores 

to get attention weights 

0 < a t,i < 1 ∑iat,i = 1

Compute (scalar) alignment scores 

et,i = f att (s t-1, h i) (f att is a Linear Layer) 

we  see  the  sky 

vediamo 

gU is an RNN unit 

(e.g. LSTM, GRU) Stanford CS 231 n 10 th Anniversary  April 24, 2025 Lecture 8 -        

> x1x2x3
> h1h2h3s0
> x4
> h4
> e11 e12 e13 e14

softmax    

> a11 a12 a13 a14
> c1

+ s1

> y0
> y1

Compute context vector as 

weighted sum of hidden 


ct = ∑iat,i hi

Use context vector in 

decoder: s t = g U(y t-1, s t-1, c t)  

> Bahdanau et al, “Neural machine translation by jointly learning to align and translate ”, ICLR 2015

[START] 

## Sequence to Sequence with RNNs and Attention 

Intuition : Context 

vector attends  to the 

relevant part of the 

input sequence 

“vediamo ” = “we see ”

so maybe a 11 =a 12 =0.45 ,

a13 =a 14 =0.05 

From final hidden state: 

Initial decoder state s0

18 

Normalize alignment scores 

to get attention weights 

0 < a t,i < 1 ∑iat,i = 1 

Compute (scalar) alignment scores 

et,i = f att (s t-1, h i) (f att is a Linear Layer) 

we  see  the  sky 

vediamo Stanford CS 231 n 10 th Anniversary  April 24, 2025 Lecture 8 -        

> x1x2x3
> h1h2h3s0
> x4
> h4
> e11 e12 e13 e14

softmax    

> a11 a12 a13 a14
> c1

+ s1

> y0
> y1

Compute context vector as 

weighted sum of hidden 


ct = ∑iat,i hi

Use context vector in 

decoder: s t = g U(y t-1, s t-1, c t)  

> Bahdanau et al, “Neural machine translation by jointly learning to align and translate ”, ICLR 2015

[START] 

## Sequence to Sequence with RNNs and Attention 

Intuition : Context 

vector attends  to the 

relevant part of the 

input sequence 

“vediamo ” = “we see ”

so maybe a 11 =a 12 =0.45 ,

a13 =a 14 =0.05 

From final hidden state: 

Initial decoder state s0

19 

Normalize alignment scores 

to get attention weights 

0 < a t,i < 1 ∑iat,i = 1 

Compute (scalar) alignment scores 

et,i = f att (s t-1, h i) (f att is a Linear Layer) 

we  see  the  sky 

vediamo 

All differentiable! No 

supervision on attention 

weights. Backprop 

through everything Stanford CS231n 10 th Anniversary  April 24 , 2025 Lecture 8 -

x1 x2 x3

h1 h2 h3 s0

x4

h4 s1

[START] 

y0

y1

c1 c2

e21  e22  e23  e24 

softmax 

a21  a22  a23  a24 

+

Repeat: Use s 1 to compute 

new context vector c 2

Bahdanau et al, “Neural machine translation by jointly learning to align and translate ”, ICLR 2015 

## Sequence to Sequence with RNNs and Attention 

20 

Compute new alignment 

scores e 2,i and attention 

weights a 2,i

we  see  the  sky 

vediamo Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

x1 x2 x3

h1 h2 h3 s0

x4

h4 s1

[START] 

y0

y1

c1 c2

e21  e22  e23  e24 

softmax 

a21  a22  a23  a24 

+

Repeat: Use s 1 to compute 

new context vector c 2

Bahdanau et al, “Neural machine translation by jointly learning to align and translate ”, ICLR 2015 

## Sequence to Sequence with RNNs and Attention 

21 

s2

y2

il 

y1

Use context vector 

in decoder: s t =

gU(y t-1, s t-1, c t)

we  see  the  sky 

vediamo 

vediamo Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

x1 x2 x3

h1 h2 h3 s0

x4

h4 s1

[START] 

y0

y1

c1 c2

e21  e22  e23  e24 

softmax 

a21  a22  a23  a24 

+

Repeat: Use s 1 to compute 

new context vector c 2  

> Bahdanau et al, “Neural machine translation by jointly learning to align and translate ”, ICLR 2015

## Sequence to Sequence with RNNs and Attention 

22 

s2

y2

y1

Use context vector 

in decoder: s t =

gU(y t-1, s t-1, c t)

Intuition : Context vector 

attends  to the relevant 

part of the input sequence 

“il ” = “the ”

so maybe a 21 =a 22 =0.05 ,

a24 =0.1 , a 23 =0.8 

we  see  the  sky 

il vediamo 

vediamo Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

x1 x2 x3

h1 h2 h3 s0

x4

h4 s1 s2

[START] 

y0

y1 y2

s3 s4

y3 y4

[STOP] 

c1 y1c2 y2c3 y3c4  

> Bahdanau et al, “Neural machine translation by jointly learning to align and translate ”, ICLR 2015

Use a different context vector in each timestep of decoder 

- Input sequence not bottlenecked through single vector 

- At each timestep of decoder, context vector “looks at ”

different parts of the input sequence 

## Sequence to Sequence with RNNs and Attention 

23 

we  see  the  sky 

cielo vediamo  il 

vediamo  il  cielo Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Bahdanau et al, “Neural machine translation by jointly learning to align and translate ”, ICLR 2015 

Example : English to 

French translation  Visualize attention weights a t,i 

## Sequence to Sequence with RNNs and Attention 

24 

x1 x2 x3

h1 h2 h3

x4

h4

e21  e22  e23  e24 

softmax 

a21  a22  a23  a24 

we  see  the  sky Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -  

> Bahdanau et al, “Neural machine translation by jointly learning to align and translate ”, ICLR 2015

Example : English to 

French translation  Visualize attention weights a t,i 

## Sequence to Sequence with RNNs and Attention 

25 

Input : “The agreement on the 

European Economic Area was 

signed in August 1992 .”

Output : “L’accord sur la zone 

économique européenne a été 

signé en août 1992 .”Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -  

> Bahdanau et al, “Neural machine translation by jointly learning to align and translate ”, ICLR 2015

Visualize attention weights a t,i 

## Sequence to Sequence with RNNs and Attention 

26 

Input : “The agreement on the 

European Economic Area was 

signed in August 1992 .”

Output : “L’accord sur la zone 

économique européenne a été 

signé en août 1992 .”

Example : English to 

French translation 

Diagonal attention 

means words 

correspond in order 

Diagonal attention 

means words 

correspond in order Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -  

> Bahdanau et al, “Neural machine translation by jointly learning to align and translate ”, ICLR 2015

Visualize attention weights a t,i 

Diagonal attention 

means words 

correspond in order 

## Sequence to Sequence with RNNs and Attention 

27 

Input : “The agreement on the 

European Economic Area was 

signed in August 1992 .”

Output : “L’accord sur la zone 

économique européenne a été 

signé en août 1992 .”

Example : English to 

French translation 

Attention figures 

out other word 

orders 

Diagonal attention 

means words 

correspond in order Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 28 

x1 x2 x3

h1 h2 h3 s0

x4

h4 s1 s2

[START] 

y0

y1 y2

s3 s4

y3 y4

[STOP] 

c1 y1c2 y2c3 y3c4

we  see  the  sky 

cielo vediamo  il 

vediamo  il  cielo 

## Sequence to Sequence with RNNs and Attention 

e21  e22  e23  e24 

softmax 

a21  a22  a23  a24 

+

There ’s a general 

operator hiding here: Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 29                    

> x1x2x3
> h1h2h3s0
> x4
> h4s1s2
> [START]
> y0
> y1y2
> s3s4
> y3y4
> [STOP]
> c1y1c2y2c3y3c4
> we see the sky
> cielo vediamo il
> vediamo il cielo

## Sequence to Sequence with RNNs and Attention 

Query vectors (decoder RNN states) and 

data vectors (encoder RNN states) 

get transformed to 

output vectors (Context states). 

Each query attends to all data vectors and 

gives one output vector 

There ’s a general 

operator hiding here: Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 30 

## Attention Layer 

Inputs :

Query vector : q [D Q]Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 31 

## Attention Layer 

Inputs :

Query vector : q [D Q]

Data vectors : X [N X x D X]Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 32 

## Attention Layer 

Inputs :

Query vector : q [D Q]

Data vectors : X [N X x D X]

Computation :

Similarities : e [N X] ei = fatt (q, Xi)Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 33 

## Attention Layer 

Inputs :

Query vector : q [D Q]

Data vectors : X [N X x D X]

Computation :

Similarities : e [N X] ei = fatt (q, Xi)

Attention weights : a = softmax (e) [N X]Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 34 

## Attention Layer 

Inputs :

Query vector : q [D Q]

Data vectors : X [N X x D X]

Computation :

Similarities : e [N X] ei = fatt (q, Xi)

Attention weights : a = softmax (e) [N X]

Output vector : y = ∑iaiXi [D X]Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 35 

## Attention Layer 

Inputs :

Query vector : q [D Q]

Data vectors : X [N X x D X]

Computation :

Similarities : e [N X] ei = fatt (q, Xi)

Attention weights : a = softmax (e) [N X]

Output vector : y = ∑iaiXi [D X] Let ’s generalize this! Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 36 

## Attention Layer 

Inputs :

Query vector : q [D X]

Data vectors : X [N X x D X]

Computation :

Similarities : e [N X] ei = q · Xi

Attention weights : a = softmax (e) [N X]

Output vector : y = ∑iaiXi [D X]

Changes 

- Use dot product for similarity Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 37 

## Attention Layer 

Inputs :

Query vector : q [D X]

Data vectors : X [N X x D X]

Computation :

Similarities : e [N X] ei = q · Xi / 𝐷 𝑋 

Attention weights : a = softmax (e) [N X]

Output vector : y = ∑iaiXi [D X]

Changes 

- Use scaled dot product for similarity Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 38 

## Attention Layer 

Inputs :

Query vector : q [D X]

Data vectors : X [N X x D X]

Computation :

Similarities : e [N X] ei = q · Xi / 𝐷 𝑋 

Attention weights : a = softmax (e) [N X]

Output vector : y = ∑iaiXi [D X]

Changes 

- Use scaled dot product for similarity 

Large similarities will cause softmax to 

saturate and give vanishing gradients 

Recall a · b = |a||b| cos(angle) 

Suppose that a and b are constant 

vectors of dimension D 

Then |a| = ( ∑ia2)1/2 = a 𝐷 Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 39 

## Attention Layer 

Inputs :

Query vector : Q [N Q x D X]

Data vectors : X [N X x D X]

Computation :

Similarities : E = QXT / 𝐷 𝑋 [N Q x N X]

Eij = Qi·Xj / 𝐷 𝑋 

Attention weights : A = softmax (E, dim= 1) [N Q x N X]

Output vector : Y = A X [N Q x D X]

Yi = ∑jAij Xj

Changes 

- Use scaled dot product for similarity 

- Multiple query vectors Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 40 

## Attention Layer 

Inputs :

Query vector : Q [N Q x D Q]

Data vectors : X [N X x D X]

Key matrix : WK [D X x D Q]

Value matrix : WV [D X x D V]

Computation :

Keys : K = XWK [N X x D Q]

Values : V = XWV [N X x D V]

Similarities : E = QKT / 𝐷 𝑄 [N Q x N X]

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N Q x N X]

Output vector : Y = A V [N Q x D V]

Yi = ∑jAij Vj

Changes 

- Use scaled dot product for similarity 

- Multiple query vectors 

- Separate key and value Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 41 

## Attention Layer 

Inputs :

Query vector : Q [N Q x D Q]

Data vectors : X [N X x D X]

Key matrix : WK [D X x D Q]

Value matrix : WV [D X x D V]

Computation :

Keys : K = XWK [N X x D Q]

Values : V = XWV [N X x D V]

Similarities : E = QKT / 𝐷 𝑄 [N Q x N X]

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N Q x N X]

Output vector : Y = A V [N Q x D V]

Yi = ∑jAij Vj Q1

X1

X2

X3

Q2 Q3 Q4Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 42 

## Attention Layer 

Inputs :

Query vector : Q [N Q x D Q]

Data vectors : X [N X x D X]

Key matrix : WK [D X x D Q]

Value matrix : WV [D X x D V]

Computation :

Keys : K = XWK [N X x D Q]

Values : V = XWV [N X x D V]

Similarities : E = QKT / 𝐷 𝑄 [N Q x N X]

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N Q x N X]

Output vector : Y = A V [N Q x D V]

Yi = ∑jAij Vj Q1

X1

X2

X3

K1

K2

K3

V1

V2

V3

Q2 Q3 Q4Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 43 

## Attention Layer 

Inputs :

Query vector : Q [N Q x D Q]

Data vectors : X [N X x D X]

Key matrix : WK [D X x D Q]

Value matrix : WV [D X x D V]

Computation :

Keys : K = XWK [N X x D Q]

Values : V = XWV [N X x D V]

Similarities : E = QKT / 𝐷 𝑄 [N Q x N X]

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N Q x N X]

Output vector : Y = A V [N Q x D V]

Yi = ∑jAij Vj Q1

X1

X2

X3

K1

K2

K3  

> E1,1 E2,1
> E1,2
> E1,3
> E2,2
> E2,3 E3,3
> E3,2
> E3,1
> E4,3
> E4,2
> E4,1

V1

V2

V3

Q2 Q3 Q4Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 44 

## Attention Layer 

Inputs :

Query vector : Q [N Q x D Q]

Data vectors : X [N X x D X]

Key matrix : WK [D X x D Q]

Value matrix : WV [D X x D V]

Computation :

Keys : K = XWK [N X x D Q]

Values : V = XWV [N X x D V]

Similarities : E = QKT / 𝐷 𝑄 [N Q x N X]

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N Q x N X]

Output vector : Y = A V [N Q x D V]

Yi = ∑jAij Vj

Softmax ( )

Q1

X1

X2

X3

K1

K2

K3    

> E1,1 E2,1
> E1,2
> E1,3
> E2,2
> E2,3 E3,3
> E3,2
> E3,1
> E4,3
> E4,2
> E4,1
> A1,1 A2,1
> A1,2
> A1,3
> A2,2
> A2,3 A3,3
> A3,2
> A3,1
> A4,3
> A4,2
> A4,1

V1

V2

V3

Q2 Q3 Q4

Softmax normalizes each 

column: each query predicts 

a distribution over the keys Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 45 

## Attention Layer 

Inputs :

Query vector : Q [N Q x D Q]

Data vectors : X [N X x D X]

Key matrix : WK [D X x D Q]

Value matrix : WV [D X x D V]

Computation :

Keys : K = XWK [N X x D Q]

Values : V = XWV [N X x D V]

Similarities : E = QKT / 𝐷 𝑄 [N Q x N X]

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N Q x N X]

Output vector : Y = A V [N Q x D V]

Yi = ∑jAij Vj

Softmax ( )

Q1

X1

X2

X3

K1

K2

K3    

> E1,1 E2,1
> E1,2
> E1,3
> E2,2
> E2,3 E3,3
> E3,2
> E3,1
> E4,3
> E4,2
> E4,1
> A1,1 A2,1
> A1,2
> A1,3
> A2,2
> A2,3 A3,3
> A3,2
> A3,1
> A4,3
> A4,2
> A4,1

V1

V2

V3

Product( ), Sum( )

Q2 Q3 Q4

Y1 Y2 Y3 Y4Each output is a linear 

combination of all values ,

weighted by attention weights Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 46 

## Cross -Attention Layer 

Inputs :

Query vector : Q [N Q x D Q]

Data vectors : X [N X x D X]

Key matrix : WK [D X x D Q]

Value matrix : WV [D X x D V]

Computation :

Keys : K = XWK [N X x D Q]

Values : V = XWV [N X x D V]

Similarities : E = QKT / 𝐷 𝑄 [N Q x N X]

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N Q x N X]

Output vector : Y = A V [N Q x D V]

Yi = ∑jAij Vj

Softmax ( )

Q1

X1

X2

X3

K1

K2

K3    

> E1,1 E2,1
> E1,2
> E1,3
> E2,2
> E2,3 E3,3
> E3,2
> E3,1
> E4,3
> E4,2
> E4,1
> A1,1 A2,1
> A1,2
> A1,3
> A2,2
> A2,3 A3,3
> A3,2
> A3,1
> A4,3
> A4,2
> A4,1

V1

V2

V3

Product( ), Sum( )

Q2 Q3 Q4

Y1 Y2 Y3 Y4

Each query produces 

one output , which is a 

mix of information in 

the data vectors Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D in ]

Key matrix : WK [D in x Dout ]

Value matrix : WV [D in x Dout ]

Query matrix : WQ [D in x Dout ]

Computation :

Queries : Q = XWQ [N x Dout ]

Keys : K = XWK [N x Dout ]

Values : V = XWV [N x Dout ]

Similarities : E = QKT / 𝐷 𝑄 [N x N] 

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N x N] 

Output vector : Y = A V [N x Dout ]

Yi = ∑jAij Vj

47 

## Self -Attention Layer 

Each input produces 

one output , which is 

a mix of information 

from all inputs 

Softmax ( )

K1

K2

K3    

> E1,1 E2,1
> E1,2
> E1,3
> E2,2
> E2,3 E3,3
> E3,2
> E3,1
> A1,1 A2,1
> A1,2
> A1,3
> A2,2
> A2,3 A3,3
> A3,2
> A3,1

V1

V2

V3

Product( ), Sum( )

Y1 Y2 Y3

Q1 Q2 Q3

X1 X2 X3

Shapes get a little simpler: 

- N input vectors, each D in 

- Almost always D Q = D V = Dout Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D in ]

Key matrix : WK [D in x Dout ]

Value matrix : WV [D in x Dout ]

Query matrix : WQ [D in x Dout ]

Computation :

Queries : Q = XWQ [N x Dout ]

Keys : K = XWK [N x Dout ]

Values : V = XWV [N x Dout ]

Similarities : E = QKT / 𝐷 𝑄 [N x N] 

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N x N] 

Output vector : Y = A V [N x Dout ]

Yi = ∑jAij Vj

48 

## Self -Attention Layer 

Each input produces 

one output , which is 

a mix of information 

from all inputs 

K1

K2

K3

V1

V2

V3

Q1 Q2 Q3

X1 X2 X3

From each input :

compute a query ,

key , and value vector 

Often fused to one matmul :

[Q K V] = X[WQ WK WV]   

> [N x 3Dout] = [N x Din] [Din x 3Dout]

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D in ]

Key matrix : WK [D in x Dout ]

Value matrix : WV [D in x Dout ]

Query matrix : WQ [D in x Dout ]

Computation :

Queries : Q = XWQ [N x Dout ]

Keys : K = XWK [N x Dout ]

Values : V = XWV [N x Dout ]

Similarities : E = QKT / 𝐷 𝑄 [N x N] 

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N x N] 

Output vector : Y = A V [N x Dout ]

Yi = ∑jAij Vj

49 

## Self -Attention Layer 

Each input produces 

one output , which is 

a mix of information 

from all inputs 

K1

K2

K3  

> E1,1 E2,1
> E1,2
> E1,3
> E2,2
> E2,3 E3,3
> E3,2
> E3,1

V1

V2

V3

Q1 Q2 Q3

X1 X2 X3

Compute similarity 

between each query 

and each key Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D in ]

Key matrix : WK [D in x Dout ]

Value matrix : WV [D in x Dout ]

Query matrix : WQ [D in x Dout ]

Computation :

Queries : Q = XWQ [N x Dout ]

Keys : K = XWK [N x Dout ]

Values : V = XWV [N x Dout ]

Similarities : E = QKT / 𝐷 𝑄 [N x N] 

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N x N] 

Output vector : Y = A V [N x Dout ]

Yi = ∑jAij Vj

50 

## Self -Attention Layer 

Each input produces 

one output , which is 

a mix of information 

from all inputs 

Softmax ( )

K1

K2

K3    

> E1,1 E2,1
> E1,2
> E1,3
> E2,2
> E2,3 E3,3
> E3,2
> E3,1
> A1,1 A2,1
> A1,2
> A1,3
> A2,2
> A2,3 A3,3
> A3,2
> A3,1

V1

V2

V3

Q1 Q2 Q3

X1 X2 X3

Normalize over each column: 

each query computes a 

distribution over keys Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D in ]

Key matrix : WK [D in x Dout ]

Value matrix : WV [D in x Dout ]

Query matrix : WQ [D in x Dout ]

Computation :

Queries : Q = XWQ [N x Dout ]

Keys : K = XWK [N x Dout ]

Values : V = XWV [N x Dout ]

Similarities : E = QKT / 𝐷 𝑄 [N x N] 

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N x N] 

Output vector : Y = A V [N x Dout ]

Yi = ∑jAij Vj

51 

## Self -Attention Layer 

Each input produces 

one output , which is 

a mix of information 

from all inputs 

Softmax ( )

K1

K2

K3    

> E1,1 E2,1
> E1,2
> E1,3
> E2,2
> E2,3 E3,3
> E3,2
> E3,1
> A1,1 A2,1
> A1,2
> A1,3
> A2,2
> A2,3 A3,3
> A3,2
> A3,1

V1

V2

V3

Product( ), Sum( )

Y1 Y2 Y3

Q1 Q2 Q3

X1 X2 X3

Compute output 

vectors as linear 

combinations of 

value vectors Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D in ]

Key matrix : WK [D in x Dout ]

Value matrix : WV [D in x Dout ]

Query matrix : WQ [D in x Dout ]

Computation :

Queries : Q = XWQ [N x Dout ]

Keys : K = XWK [N x Dout ]

Values : V = XWV [N x Dout ]

Similarities : E = QKT / 𝐷 𝑄 [N x N] 

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N x N] 

Output vector : Y = A V [N x Dout ]

Yi = ∑jAij Vj

52 

## Self -Attention Layer    

> Softmax ()
> Product( ), Sum( )

X3 X1 X2

Consider permuting inputs :Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D in ]

Key matrix : WK [D in x Dout ]

Value matrix : WV [D in x Dout ]

Query matrix : WQ [D in x Dout ]

Computation :

Queries : Q = XWQ [N x Dout ]

Keys : K = XWK [N x Dout ]

Values : V = XWV [N x Dout ]

Similarities : E = QKT / 𝐷 𝑄 [N x N] 

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N x N] 

Output vector : Y = A V [N x Dout ]

Yi = ∑jAij Vj

53 

## Self -Attention Layer  

> Softmax ()

K3

K1

K2

V3

V1

V2  

> Product( ), Sum( )

Q3 Q1 Q2

X3 X1 X2

Consider permuting inputs :

Queries , keys , and values 

will be the same but permuted Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D in ]

Key matrix : WK [D in x Dout ]

Value matrix : WV [D in x Dout ]

Query matrix : WQ [D in x Dout ]

Computation :

Queries : Q = XWQ [N x Dout ]

Keys : K = XWK [N x Dout ]

Values : V = XWV [N x Dout ]

Similarities : E = QKT / 𝐷 𝑄 [N x N] 

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N x N] 

Output vector : Y = A V [N x Dout ]

Yi = ∑jAij Vj

54 

## Self -Attention Layer 

Softmax ( )

K3

K1

K2  

> E3,3 E1,3
> E3,1
> E3,2
> E1,1
> E1,2 E2,2
> E2,1
> E2,3

V3

V1

V2

Product( ), Sum( )

Q3 Q1 Q2

X3 X1 X2

Consider permuting inputs :

Queries , keys , and values 

will be the same but permuted 

Similarities are the same but 

permuted Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D in ]

Key matrix : WK [D in x Dout ]

Value matrix : WV [D in x Dout ]

Query matrix : WQ [D in x Dout ]

Computation :

Queries : Q = XWQ [N x Dout ]

Keys : K = XWK [N x Dout ]

Values : V = XWV [N x Dout ]

Similarities : E = QKT / 𝐷 𝑄 [N x N] 

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N x N] 

Output vector : Y = A V [N x Dout ]

Yi = ∑jAij Vj

55 

## Self -Attention Layer 

Softmax ( )

K3

K1

K2    

> E3,3 E1,3
> E3,1
> E3,2
> E1,1
> E1,2 E2,2
> E2,1
> E2,3
> A3,3 A1,3
> A3,1
> A3,2
> A1,1
> A1,2 A2,2
> A2,1
> A2,3

V3

V1

V2

Product( ), Sum( )

Q3 Q1 Q2

X3 X1 X2

Consider permuting inputs :

Queries , keys , and values 

will be the same but permuted 

Similarities are the same but 

permuted 

Attention weights are the 

same but permuted Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D in ]

Key matrix : WK [D in x Dout ]

Value matrix : WV [D in x Dout ]

Query matrix : WQ [D in x Dout ]

Computation :

Queries : Q = XWQ [N x Dout ]

Keys : K = XWK [N x Dout ]

Values : V = XWV [N x Dout ]

Similarities : E = QKT / 𝐷 𝑄 [N x N] 

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N x N] 

Output vector : Y = A V [N x Dout ]

Yi = ∑jAij Vj

56 

## Self -Attention Layer 

Softmax ( )

K3

K1

K2    

> E3,3 E1,3
> E3,1
> E3,2
> E1,1
> E1,2 E2,2
> E2,1
> E2,3
> A3,3 A1,3
> A3,1
> A3,2
> A1,1
> A1,2 A2,2
> A2,1
> A2,3

V3

V1

V2

Product( ), Sum( )

Y3 Y1 Y2

Q3 Q1 Q2

X3 X1 X2

Consider permuting inputs :

Queries , keys , and values 

will be the same but permuted 

Similarities are the same but 

permuted 

Attention weights are the 

same but permuted 

Outputs are the same but 

permuted Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D in ]

Key matrix : WK [D in x Dout ]

Value matrix : WV [D in x Dout ]

Query matrix : WQ [D in x Dout ]

Computation :

Queries : Q = XWQ [N x Dout ]

Keys : K = XWK [N x Dout ]

Values : V = XWV [N x Dout ]

Similarities : E = QKT / 𝐷 𝑄 [N x N] 

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N x N] 

Output vector : Y = A V [N x Dout ]

Yi = ∑jAij Vj

57 

## Self -Attention Layer 

Softmax ( )

K3

K1

K2    

> E3,3 E1,3
> E3,1
> E3,2
> E1,1
> E1,2 E2,2
> E2,1
> E2,3
> A3,3 A1,3
> A3,1
> A3,2
> A1,1
> A1,2 A2,2
> A2,1
> A2,3

V3

V1

V2

Product( ), Sum( )

Y3 Y1 Y2

Q3 Q1 Q2

X3 X1 X2

Self -Attention is 

permutation equivariant :

F( σ(X)) =  σ(F(X)) 

This means that Self -Attention 

works on sets of vectors Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D in ]

Key matrix : WK [D in x Dout ]

Value matrix : WV [D in x Dout ]

Query matrix : WQ [D in x Dout ]

Computation :

Queries : Q = XWQ [N x Dout ]

Keys : K = XWK [N x Dout ]

Values : V = XWV [N x Dout ]

Similarities : E = QKT / 𝐷 𝑄 [N x N] 

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N x N] 

Output vector : Y = A V [N x Dout ]

Yi = ∑jAij Vj

58 

## Self -Attention Layer 

Softmax ( )

K1

K2

K3    

> E1,1 E2,1
> E1,2
> E1,3
> E2,2
> E2,3 E3,3
> E3,2
> E3,1
> A1,1 A2,1
> A1,2
> A1,3
> A2,2
> A2,3 A3,3
> A3,2
> A3,1

V1

V2

V3

Product( ), Sum( )

Y1 Y2 Y3

Q1 Q2 Q3

X1 X2 X3

Problem : Self -Attention 

does not know the order of 

the sequence Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D in ]

Key matrix : WK [D in x Dout ]

Value matrix : WV [D in x Dout ]

Query matrix : WQ [D in x Dout ]

Computation :

Queries : Q = XWQ [N x Dout ]

Keys : K = XWK [N x Dout ]

Values : V = XWV [N x Dout ]

Similarities : E = QKT / 𝐷 𝑄 [N x N] 

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N x N] 

Output vector : Y = A V [N x Dout ]

Yi = ∑jAij Vj

59 

## Self -Attention Layer 

Problem : Self -Attention 

does not know the order of 

the sequence 

Solution : Add positional 

encoding to each input; this 

is a vector that is a fixed 

function of the index 

Softmax ( )

K1

K2

K3    

> E1,1 E2,1
> E1,2
> E1,3
> E2,2
> E2,3 E3,3
> E3,2
> E3,1
> A1,1 A2,1
> A1,2
> A1,3
> A2,2
> A2,3 A3,3
> A3,2
> A3,1

V1

V2

V3

Product( ), Sum( )

Y1 Y2 Y3

Q1 Q2 Q3

X1 X2 X3  

> E( 1)E( 2)E( 3)

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D in ]

Key matrix : WK [D in x Dout ]

Value matrix : WV [D in x Dout ]

Query matrix : WQ [D in x Dout ]

Computation :

Queries : Q = XWQ [N x Dout ]

Keys : K = XWK [N x Dout ]

Values : V = XWV [N x Dout ]

Similarities : E = QKT / 𝐷 𝑄 [N x N] 

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N x N] 

Output vector : Y = A V [N x Dout ]

Yi = ∑jAij Vj

60 

## Masked Self -Attention Layer 

Override similarities with -inf; 

this controls which inputs each 

vector is allowed to look at. 

Softmax ( )

K1

K2

K3 

> E1,1 E2,1

-∞

-∞

> E2,2

-∞ E3,3   

> E3,2
> E3,1
> A1,1 A2,1
> 0
> 0
> A2,2
> 0A3,3
> A3,2
> A3,1

V1

V2

V3

Product( ), Sum( )

Q1 Q2 Q3

Don ’t let vectors “look ahead ” in the sequence 

Y1 Y2 Y3

X1 X2 X3Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D in ]

Key matrix : WK [D in x Dout ]

Value matrix : WV [D in x Dout ]

Query matrix : WQ [D in x Dout ]

Computation :

Queries : Q = XWQ [N x Dout ]

Keys : K = XWK [N x Dout ]

Values : V = XWV [N x Dout ]

Similarities : E = QKT / 𝐷 𝑄 [N x N] 

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N x N] 

Output vector : Y = A V [N x Dout ]

Yi = ∑jAij Vj

61 

## Masked Self -Attention Layer 

Override similarities with -inf; 

this controls which inputs each 

vector is allowed to look at. 

Used for language modeling 

where you want to predict the 

next word 

Softmax ( )

K1

K2

K3

V1

V2

V3

Product( ), Sum( )

Q1 Q2 Q3

Don ’t let vectors “look ahead ” in the sequence 

Attention  is  very 

is  very  cool    

> A1,1 A2,1
> 0
> 0
> A2,2
> 0A3,3
> A3,2
> A3,1
> E1,1 E2,1

-∞

-∞

> E2,2

-∞ E3,3 

> E3,2
> E3,1

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D in ]

Key matrix : WK [D in x Dout ]

Value matrix : WV [D in x Dout ]

Query matrix : WQ [D in x Dout ]

Computation :

Queries : Q = XWQ [N x Dout ]

Keys : K = XWK [N x Dout ]

Values : V = XWV [N x Dout ]

Similarities : E = QKT / 𝐷 𝑄 [N x N] 

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N x N] 

Output vector : Y = AX [N x Dout ]

Yi = ∑jAij Vj

62 

## Multiheaded Self -Attention Layer 

Run H copies of Self -Attention in parallel 

X1 X2 X3Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D in ]

Key matrix : WK [D in x Dout ]

Value matrix : WV [D in x Dout ]

Query matrix : WQ [D in x Dout ]

Computation :

Queries : Q = XWQ [N x Dout ]

Keys : K = XWK [N x Dout ]

Values : V = XWV [N x Dout ]

Similarities : E = QKT / 𝐷 𝑄 [N x N] 

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N x N] 

Output vector : Y = AX [N x Dout ]

Yi = ∑jAij Vj

63 

## Multiheaded Self -Attention Layer 

Run H copies of Self -Attention in parallel 

X1 X2 X3

H = 3 independent 

self -attention layers 

(called heads), each 

with their own weights Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D in ]

Key matrix : WK [D in x Dout ]

Value matrix : WV [D in x Dout ]

Query matrix : WQ [D in x Dout ]

Computation :

Queries : Q = XWQ [N x Dout ]

Keys : K = XWK [N x Dout ]

Values : V = XWV [N x Dout ]

Similarities : E = QKT / 𝐷 𝑄 [N x N] 

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N x N] 

Output vector : Y = AX [N x Dout ]

Yi = ∑jAij Vj

64 

## Multiheaded Self -Attention Layer 

Run H copies of Self -Attention in parallel 

X1 X2 X3

> Y1,1
> Y1,2
> Y1,3
> Y2,1
> Y2,2
> Y2,3
> Y3,1
> Y3,2
> Y3,3

H = 3 independent 

self -attention layers 

(called heads), each 

with their own weights 

Stack up the H 

independent outputs 

for each input X Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D in ]

Key matrix : WK [D in x Dout ]

Value matrix : WV [D in x Dout ]

Query matrix : WQ [D in x Dout ]

Computation :

Queries : Q = XWQ [N x Dout ]

Keys : K = XWK [N x Dout ]

Values : V = XWV [N x Dout ]

Similarities : E = QKT / 𝐷 𝑄 [N x N] 

Eij = Qi·Kj / 𝐷 𝑄 

Attention weights : A = softmax (E, dim= 1) [N x N] 

Output vector : Y = AX [N x Dout ]

Yi = ∑jAij Vj

65 

## Multiheaded Self -Attention Layer 

Run H copies of Self -Attention in parallel 

X1 X2 X3  

> Y1,1
> Y1,2
> Y1,3
> Y2,1
> Y2,2
> Y2,3
> Y3,1
> Y3,2
> Y3,3
> O1O2O3

H = 3 independent 

self -attention layers 

(called heads), each 

with their own weights 

Stack up the H 

independent outputs 

for each input X 

Output projection fuses 

data from each head Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D] 

Key matrix : WK [D x HD H]

Value matrix : WV [D x HD H]

Query matrix : WQ [D x HD H]

Output matrix : WO [HD H x D] 

Computation :

Queries : Q = XWQ [H x N x D H]

Keys : K = XWK [H x N x D H]

Values : V = XWV [H x N x D H]

Similarities : E = QKT / 𝐷 𝑄 [H x N x N] 

Attention weights : A = softmax (E, dim= 2) [H x N x N] 

Head outputs : Y = A V [H x N x D H] => [N x HD H]

Outputs : O = YWO [N x D] 

66 

## Multiheaded Self -Attention Layer 

Run H copies of Self -Attention in parallel 

X1 X2 X3  

> Y1,1
> Y1,2
> Y1,3
> Y2,1
> Y2,2
> Y2,3
> Y3,1
> Y3,2
> Y3,3
> O1O2O3

Each of the H parallel 

layers use a qkv dim of 

DH = “head dim ”

Usually D H = D / H, so 

inputs and outputs have 

the same dimension Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D] 

Key matrix : WK [D x HD H]

Value matrix : WV [D x HD H]

Query matrix : WQ [D x HD H]

Output matrix : WO [HD H x D] 

Computation :

Queries : Q = XWQ [H x N x D H]

Keys : K = XWK [H x N x D H]

Values : V = XWV [H x N x D H]

Similarities : E = QKT / 𝐷 𝑄 [H x N x N] 

Attention weights : A = softmax (E, dim= 2) [H x N x N] 

Head outputs : Y = A V [H x N x D H] => [N x HD H]

Outputs : O = YWO [N x D] 

67 

## Multiheaded Self -Attention Layer 

Run H copies of Self -Attention in parallel 

X1 X2 X3  

> Y1,1
> Y1,2
> Y1,3
> Y2,1
> Y2,2
> Y2,3
> Y3,1
> Y3,2
> Y3,3
> O1O2O3

In practice, compute 

all H heads in parallel 

using batched matrix 

multiply operations. 

Used everywhere in 

practice. Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D] 

Key matrix : WK [D x HD H]

Value matrix : WV [D x HD H]

Query matrix : WQ [D x HD H]

Output matrix : WO [HD H x D] 

Computation :

Queries : Q = XWQ [H x N x D H]

Keys : K = XWK [H x N x D H]

Values : V = XWV [H x N x D H]

Similarities : E = QKT / 𝐷 𝑄 [H x N x N] 

Attention weights : A = softmax (E, dim= 2) [H x N x N] 

Head outputs : Y = AV [H x N x D H] => [N x HD H]

Outputs : O = YWO [N x D] 

68 

## Self -Attention is Four Matrix Multiplies! Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D] 

Key matrix : WK [D x HD H]

Value matrix : WV [D x HD H]

Query matrix : WQ [D x HD H]

Output matrix : WO [HD H x D] 

Computation :

Queries : Q = XWQ [H x N x D H]

Keys : K = XWK [H x N x D H]

Values : V = XWV [H x N x D H]

Similarities : E = QKT / 𝐷 𝑄 [H x N x N] 

Attention weights : A = softmax (E, dim= 2) [H x N x N] 

Head outputs : Y = AV [H x N x D H] => [N x HD H]

Outputs : O = YWO [N x D] 

69 

## Self -Attention is Four Matrix Multiplies! 

1.  QKV Projection 

[N x D] [D x 3HD H] => [N x 3HD H]

Split and reshape to get Q, K, V each of 

shape [H x N x D H]Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D] 

Key matrix : WK [D x HD H]

Value matrix : WV [D x HD H]

Query matrix : WQ [D x HD H]

Output matrix : WO [HD H x D] 

Computation :

Queries : Q = XWQ [H x N x D H]

Keys : K = XWK [H x N x D H]

Values : V = XWV [H x N x D H]

Similarities : E = QKT / 𝐷 𝑄 [H x N x N] 

Attention weights : A = softmax (E, dim= 2) [H x N x N] 

Head outputs : Y = AV [H x N x D H] => [N x HD H]

Outputs : O = YWO [N x D] 

70 

## Self -Attention is Four Matrix Multiplies! 

1.  QKV Projection 

[N x D] [D x 3HD H] => [N x 3HD H]

Split and reshape to get Q, K, V each of 

shape [H x N x D H]

2.  QK Similarity 

[H x N x D H] [H x D H x N] => [H x N x N] Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D] 

Key matrix : WK [D x HD H]

Value matrix : WV [D x HD H]

Query matrix : WQ [D x HD H]

Output matrix : WO [HD H x D] 

Computation :

Queries : Q = XWQ [H x N x D H]

Keys : K = XWK [H x N x D H]

Values : V = XWV [H x N x D H]

Similarities : E = QKT / 𝐷 𝑄 [H x N x N] 

Attention weights : A = softmax (E, dim= 2) [H x N x N] 

Head outputs : Y = AV [H x N x D H] => [N x HD H]

Outputs : O = YWO [N x D] 

71 

## Self -Attention is Four Matrix Multiplies! 

1.  QKV Projection 

[N x D] [D x 3HD H] => [N x 3HD H]

Split and reshape to get Q, K, V each of 

shape [H x N x D H]

2.  QK Similarity 

[H x N x D H] [H x D H x N] => [H x N x N] 

3.  V-Weighting 

[H x N x N] [H x N x D H] => [H x N x D H]

Reshape to [N x HD H]Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D] 

Key matrix : WK [D x HD H]

Value matrix : WV [D x HD H]

Query matrix : WQ [D x HD H]

Output matrix : WO [HD H x D] 

Computation :

Queries : Q = XWQ [H x N x D H]

Keys : K = XWK [H x N x D H]

Values : V = XWV [H x N x D H]

Similarities : E = QKT / 𝐷 𝑄 [H x N x N] 

Attention weights : A = softmax (E, dim= 2) [H x N x N] 

Head outputs : Y = AV [H x N x D H] => [N x HD H]

Outputs : O = YWO [N x D] 

72 

## Self -Attention is Four Matrix Multiplies! 

1.  QKV Projection 

[N x D] [D x 3HD H] => [N x 3HD H]

Split and reshape to get Q, K, V each of 

shape [H x N x D H]

2.  QK Similarity 

[H x N x D H] [H x D H x N] => [H x N x N] 

3.  V-Weighting 

[H x N x N] [H x N x D H] => [H x N x D H]

Reshape to [N x HD H]

4.  Output Projection 

[N x HD H] [HD H x D] => [N x D] Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D] 

Key matrix : WK [D x HD H]

Value matrix : WV [D x HD H]

Query matrix : WQ [D x HD H]

Output matrix : WO [HD H x D] 

Computation :

Queries : Q = XWQ [H x N x D H]

Keys : K = XWK [H x N x D H]

Values : V = XWV [H x N x D H]

Similarities : E = QKT / 𝐷 𝑄 [H x N x N] 

Attention weights : A = softmax (E, dim= 2) [H x N x N] 

Head outputs : Y = AV [H x N x D H] => [N x HD H]

Outputs : O = YWO [N x D] 

73 

## Self -Attention is Four Matrix Multiplies! 

1.  QKV Projection 

[N x D] [D x 3HD H] => [N x 3HD H]

Split and reshape to get Q, K, V each of 

shape [H x N x D H]

2.  QK Similarity 

[H x N x D H] [H x D H x N] => [H x N x N] 

3.  V-Weighting 

[H x N x N] [H x N x D H] => [H x N x D H]

Reshape to [N x HD H]

4.  Output Projection 

[N x HD H] [HD H x D] => [N x D] 

Q: How much compute  does this take 

as the number of vectors N increases? Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D] 

Key matrix : WK [D x HD H]

Value matrix : WV [D x HD H]

Query matrix : WQ [D x HD H]

Output matrix : WO [HD H x D] 

Computation :

Queries : Q = XWQ [H x N x D H]

Keys : K = XWK [H x N x D H]

Values : V = XWV [H x N x D H]

Similarities : E = QKT / 𝐷 𝑄 [H x N x N] 

Attention weights : A = softmax (E, dim= 2) [H x N x N] 

Head outputs : Y = AV [H x N x D H] => [N x HD H]

Outputs : O = YWO [N x D] 

74 

## Self -Attention is Four Matrix Multiplies! 

1.  QKV Projection 

[N x D] [D x 3HD H] => [N x 3HD H]

Split and reshape to get Q, K, V each of 

shape [H x N x D H]

2.  QK Similarity 

[H x N x D H] [H x D H x N] => [H x N x N] 

3.  V-Weighting 

[H x N x N] [H x N x D H] => [H x N x D H]

Reshape to [N x HD H]

4.  Output Projection 

[N x HD H] [HD H x D] => [N x D] 

Q: How much compute  does this take 

as the number of vectors N increases? 

A: O(N 2)Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D] 

Key matrix : WK [D x HD H]

Value matrix : WV [D x HD H]

Query matrix : WQ [D x HD H]

Output matrix : WO [HD H x D] 

Computation :

Queries : Q = XWQ [H x N x D H]

Keys : K = XWK [H x N x D H]

Values : V = XWV [H x N x D H]

Similarities : E = QKT / 𝐷 𝑄 [H x N x N] 

Attention weights : A = softmax (E, dim= 2) [H x N x N] 

Head outputs : Y = AV [H x N x D H] => [N x HD H]

Outputs : O = YWO [N x D] 

75 

## Self -Attention is Four Matrix Multiplies! 

1.  QKV Projection 

[N x D] [D x 3HD H] => [N x 3HD H]

Split and reshape to get Q, K, V each of 

shape [H x N x D H]

2.  QK Similarity 

[H x N x D H] [H x D H x N] => [H x N x N] 

3.  V-Weighting 

[H x N x N] [H x N x D H] => [H x N x D H]

Reshape to [N x HD H]

4.  Output Projection 

[N x HD H] [HD H x D] => [N x D] 

Q: How much memory  does this take 

as the number of vectors N increases? Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D] 

Key matrix : WK [D x HD H]

Value matrix : WV [D x HD H]

Query matrix : WQ [D x HD H]

Output matrix : WO [HD H x D] 

Computation :

Queries : Q = XWQ [H x N x D H]

Keys : K = XWK [H x N x D H]

Values : V = XWV [H x N x D H]

Similarities : E = QKT / 𝐷 𝑄 [H x N x N] 

Attention weights : A = softmax (E, dim= 2) [H x N x N] 

Head outputs : Y = AV [H x N x D H] => [N x HD H]

Outputs : O = YWO [N x D] 

76 

## Self -Attention is Four Matrix Multiplies! 

1.  QKV Projection 

[N x D] [D x 3HD H] => [N x 3HD H]

Split and reshape to get Q, K, V each of 

shape [H x N x D H]

2.  QK Similarity 

[H x N x D H] [H x D H x N] => [H x N x N] 

3.  V-Weighting 

[H x N x N] [H x N x D H] => [H x N x D H]

Reshape to [N x HD H]

4.  Output Projection 

[N x HD H] [HD H x D] => [N x D] 

Q: How much memory  does this take 

as the number of vectors N increases? 

A: O(N 2)Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D] 

Key matrix : WK [D x HD H]

Value matrix : WV [D x HD H]

Query matrix : WQ [D x HD H]

Output matrix : WO [HD H x D] 

Computation :

Queries : Q = XWQ [H x N x D H]

Keys : K = XWK [H x N x D H]

Values : V = XWV [H x N x D H]

Similarities : E = QKT / 𝐷 𝑄 [H x N x N] 

Attention weights : A = softmax (E, dim= 2) [H x N x N] 

Head outputs : Y = AV [H x N x D H] => [N x HD H]

Outputs : O = YWO [N x D] 

77 

## Self -Attention is Four Matrix Multiplies! 

1.  QKV Projection 

[N x D] [D x 3HD H] => [N x 3HD H]

Split and reshape to get Q, K, V each of 

shape [H x N x D H]

2.  QK Similarity 

[H x N x D H] [H x D H x N] => [H x N x N] 

3.  V-Weighting 

[H x N x N] [H x N x D H] => [H x N x D H]

Reshape to [N x HD H]

4.  Output Projection 

[N x HD H] [HD H x D] => [N x D] 

Q: How much memory  does this take 

as the number of vectors N increases? 

A: O(N 2)

If N= 100 K, H= 64 then 

HxNxN attention weights 

take 1.192 TB! GPUs don ’t

have that much memory …Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

Inputs :

Input vectors : X [N x D] 

Key matrix : WK [D x HD H]

Value matrix : WV [D x HD H]

Query matrix : WQ [D x HD H]

Output matrix : WO [HD H x D] 

Computation :

Queries : Q = XWQ [H x N x D H]

Keys : K = XWK [H x N x D H]

Values : V = XWV [H x N x D H]

Similarities : E = QKT / 𝐷 𝑄 [H x N x N] 

Attention weights : A = softmax (E, dim= 2) [H x N x N] 

Head outputs : Y = AV [H x N x D H] => [N x HD H]

Outputs : O = YWO [N x D] 

78 

## Self -Attention is Four Matrix Multiplies! 

1.  QKV Projection 

[N x D] [D x 3HD H] => [N x 3HD H]

Split and reshape to get Q, K, V each of 

shape [H x N x D H]

2.  QK Similarity 

[H x N x D H] [H x D H x N] => [H x N x N] 

3.  V-Weighting 

[H x N x N] [H x N x D H] => [H x N x D H]

Reshape to [N x HD H]

4.  Output Projection 

[N x HD H] [HD H x D] => [N x D] 

Q: How much memory  does this take 

as the number of vectors N increases? 

A: O(N) with Flash Attention 

If N= 100 K, H= 64 then 

HxNxN attention weights 

take 1.192 TB! GPUs don ’t

have that much memory …  

> Dao et al, “FlashAtten tion : Fast an d Memor y -Efficien t Exact Atte ntio n with IO -Awaren ess ”,202 2

Flash Attention 

algorithm computes 

2+3 at the same time 

without storing the 

full attention matrix! 

Makes large N 

possible Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 79 

## Three Ways of Processing Sequences Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 80 

## Three Ways of Processing Sequences 

y1 y2 y3 y4

x1 x2 x3 x4

Recurrent Neural Network 

Works on 1D ordered sequences 

(+) Theoretically good at long 

sequences: O(N) compute and 

memory for a sequence of length N 

(-) Not parallelizable. Need to 

compute hidden states sequentially Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 81 

## Three Ways of Processing Sequences 

y1 y2 y3 y4

x1 x2 x3 x4

y1 y2 y3 y4

x1 x2 x3 x4

Recurrent Neural Network  Convolution 

Works on 1D ordered sequences 

(+) Theoretically good at long 

sequences: O(N) compute and 

memory for a sequence of length N 

(-) Not parallelizable. Need to 

compute hidden states sequentially 

Works on N-dimensional grids 

(-) Bad for long sequences: need to 

stack many layers to build up large 

receptive fields 

(+) Parallelizable, outputs can be 

computed in parallel Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 82 

## Three Ways of Processing Sequences 

y1 y2 y3 y4

x1 x2 x3 x4

y1 y2 y3 y4

x1 x2 x3 x4Q1 Q2 Q3     

> K3
> K2
> K1
> E1,3
> E1,2
> E1,1
> E2,3
> E2,2
> E2,1
> E3,3
> E3,2
> E3,1
> A1,3
> A1,2
> A1,1
> A2,3
> A2,2
> A2,1
> A3,3
> A3,2
> A3,1
> V3
> V2
> V1
> Product( →), Sum( ↑)Softmax( ↑)
> Y1Y2Y3
> X1X2X3

Recurrent Neural Network  Convolution  Self -Attention 

Works on 1D ordered sequences 

(+) Theoretically good at long 

sequences: O(N) compute and 

memory for a sequence of length N 

(-) Not parallelizable. Need to 

compute hidden states sequentially 

Works on N-dimensional grids 

(-) Bad for long sequences: need to 

stack many layers to build up large 

receptive fields 

(+) Parallelizable, outputs can be 

computed in parallel 

Works on sets of vectors 

(+) Great for long sequences; each 

output depends directly on all inputs 

(+) Highly parallel, it ’s just 4 matmuls 

(-) Expensive: O(N 2) compute, O(N) 

memory for sequence of length N Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 83 

## Three Ways of Processing Sequences 

y1 y2 y3 y4

x1 x2 x3 x4

y1 y2 y3 y4

x1 x2 x3 x4Q1 Q2 Q3     

> K3
> K2
> K1
> E1,3
> E1,2
> E1,1
> E2,3
> E2,2
> E2,1
> E3,3
> E3,2
> E3,1
> A1,3
> A1,2
> A1,1
> A2,3
> A2,2
> A2,1
> A3,3
> A3,2
> A3,1
> V3
> V2
> V1
> Product( →), Sum( ↑)Softmax( ↑)
> Y1Y2Y3
> X1X2X3

Recurrent Neural Network  Convolution  Self -Attention 

Works on 1D ordered sequences 

(+) Theoretically good at long 

sequences: O(N) compute and 

memory for a sequence of length N 

(-) Not parallelizable. Need to 

compute hidden states sequentially 

Works on N-dimensional grids 

(-) Bad for long sequences: need to 

stack many layers to build up large 

receptive fields 

(+) Parallelizable, outputs can be 

computed in parallel 

Works on sets of vectors 

(+) Great for long sequences; each 

output depends directly on all inputs 

(+) Highly parallel, it ’s just 4 matmuls 

(-) Expensive: O(N 2) compute, O(N) 

memory for sequence of length N 

# Attention is All You Need 

Vaswani et al, NeurIPS 2017 Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 84 

x1 x2 x3 x4

## The Transformer 

Transformer Block 

Input : Set of vectors x    

> Vaswani et al, “Attention is all you need, ”NeurIPS 2017

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 85 

x1 x2 x3 x4

Self -Attention 

## The Transformer 

Transformer Block 

Input : Set of vectors x 

All vectors interact through 

(multiheaded) Self -Attention    

> Vaswani et al, “Attention is all you need, ”NeurIPS 2017

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 86 

## The Transformer 

Transformer Block 

Input : Set of vectors x 

Residual connection 

x1 x2 x3 x4

Self -Attention 

+

All vectors interact through 

(multiheaded) Self -Attention    

> Vaswani et al, “Attention is all you need, ”NeurIPS 2017

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 87 

## The Transformer 

Transformer Block 

Input : Set of vectors x 

Layer normalization 

normalizes all vectors 

x1 x2 x3 x4

Self -Attention 

Layer Normalization 

+

Recall Layer Normalization :

Given h 1, …, hN (Shape: D) 

scale: 𝛾 (Shape: D) 

shift: 𝛽 (Shape: D) 

𝜇 i = ( ∑j hi,j )/D (scalar) 

𝜎 i = ( ∑j (hi,j - 𝜇 i)2/D) 1/2 (scalar) 

zi = (h i - 𝜇 i) / 𝜎 i

yi = 𝛾 * z i + 𝛽 

Ba et al, 2016 

Residual connection 

All vectors interact through 

(multiheaded) Self -Attention    

> Vaswani et al, “Attention is all you need, ”NeurIPS 2017

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 88 

## The Transformer 

Transformer Block 

Input : Set of vectors x 

x1 x2 x3 x4

MLP  MLP  MLP  MLP 

Self -Attention 

Layer Normalization 

+

Layer normalization 

normalizes all vectors 

Residual connection 

All vectors interact through 

(multiheaded) Self -Attention 

MLP independently 

on each vector 

Usually a two -layer MLP; 

classic setup is 

D => 4D => D 

Also sometimes called FFN 

(Feed -Forward Network)    

> Vaswani et al, “Attention is all you need, ”NeurIPS 2017

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 89 

## The Transformer 

Transformer Block 

Input : Set of vectors x 

Layer normalization 

normalizes all vectors 

Residual connection 

All vectors interact through 

(multiheaded) Self -Attention 

x1 x2 x3 x4

MLP  MLP  MLP  MLP 

Self -Attention 

Layer Normalization 

+

+

MLP independently 

on each vector 

Residual connection    

> Vaswani et al, “Attention is all you need, ”NeurIPS 2017

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 90 

## The Transformer 

Transformer Block 

Input : Set of vectors x 

Layer normalization 

normalizes all vectors 

Residual connection 

All vectors interact through 

(multiheaded) Self -Attention 

MLP independently 

on each vector 

Residual connection 

x1 x2 x3 x4

y1 y2 y3 y4

MLP  MLP  MLP  MLP 

Self -Attention 

Layer Normalization 

+

Layer Normalization 

+

Another Layer Norm    

> Vaswani et al, “Attention is all you need, ”NeurIPS 2017

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 91 

x1 x2 x3 x4

y1 y2 y3 y4

MLP  MLP  MLP  MLP 

Self -Attention 

Layer Normalization 

+

Layer Normalization 

+

## The Transformer 

Transformer Block 

Input : Set of vectors x 

Output : Set of vectors y 

Self -Attention is the only 

interaction between vectors 

LayerNorm and MLP work on 

each vector independently 

Highly scalable and 

parallelizable, most of the 

compute is just 6 matmuls :

4 from Self -Attention 

2 from MLP    

> Vaswani et al, “Attention is all you need, ”NeurIPS 2017

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 92 

## The Transformer 

Transformer Block 

Input : Set of vectors x 

Output : Set of vectors y 

Self -Attention is the only 

interaction between vectors 

LayerNorm and MLP work on 

each vector independently 

Highly scalable and 

parallelizable, most of the 

compute is just 6 matmuls :

4 from Self -Attention 

2 from MLP    

> Vaswani et al, “Attention is all you need, ”NeurIPS 2017

A Transformer is just a stack of 

identical Transformer blocks! 

They have not changed much since 

2017 … but have gotten a lot bigger Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 93 

## The Transformer 

Transformer Block 

Input : Set of vectors x 

Output : Set of vectors y 

Self -Attention is the only 

interaction between vectors 

LayerNorm and MLP work on 

each vector independently 

Highly scalable and 

parallelizable, most of the 

compute is just 6 matmuls :

4 from Self -Attention 

2 from MLP    

> Vaswani et al, “Attention is all you need, ”NeurIPS 2017

A Transformer is just a stack of 

identical Transformer blocks! 

They have not changed much since 

2017 … but have gotten a lot bigger 

Original : [Vaswani et al, 2017 ]

12 blocks, D= 1024 , H= 16 , N= 512 

213 M params Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 94 

## The Transformer 

Transformer Block 

Input : Set of vectors x 

Output : Set of vectors y 

Self -Attention is the only 

interaction between vectors 

LayerNorm and MLP work on 

each vector independently 

Highly scalable and 

parallelizable, most of the 

compute is just 6 matmuls :

4 from Self -Attention 

2 from MLP    

> Vaswani et al, “Attention is all you need, ”NeurIPS 2017

A Transformer is just a stack of 

identical Transformer blocks! 

They have not changed much since 

2017 … but have gotten a lot bigger 

Original : [Vaswani et al, 2017 ]

12 blocks, D= 1024 , H= 16 , N= 512 

213 M params 

GPT -2: [Radford et al, 2019 ]

48 blocks, D= 1600 , H= 25 , N= 1024 

1.5 B params Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 95 

## The Transformer 

Transformer Block 

Input : Set of vectors x 

Output : Set of vectors y 

Self -Attention is the only 

interaction between vectors 

LayerNorm and MLP work on 

each vector independently 

Highly scalable and 

parallelizable, most of the 

compute is just 6 matmuls :

4 from Self -Attention 

2 from MLP    

> Vaswani et al, “Attention is all you need, ”NeurIPS 2017

A Transformer is just a stack of 

identical Transformer blocks! 

They have not changed much since 

2017 … but have gotten a lot bigger 

Original : [Vaswani et al, 2017 ]

12 blocks, D= 1024 , H= 16 , N= 512 

213 M params 

GPT -2: [Radford et al, 2019 ]

48 blocks, D= 1600 , H= 25 , N= 1024 

1.5 B params 

GPT -3: [Brown et al, 2020 ]

96 blocks, D= 12288 , H= 96 , N= 2048 

175 B params Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 96 

## Transformers for Language Modeling (LLM)    

> Attention is all you
> Embedding Matrix
> [V x D]

Learn an embedding matrix  at the start of 

the model to convert words into vectors. 

Given vocab size V and model dimension 

D, it ’s a lookup table of shape [V x D] Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 97 

## Transformers for Language Modeling (LLM)    

> Attention is all you
> Embedding Matrix
> [V x D]

Learn an embedding matrix  at the start of 

the model to convert words into vectors. 

Given vocab size V and model dimension 

D, it ’s a lookup table of shape [V x D] 

Use masked attention inside each 

transformer block so each token can only 

see the ones before it Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 98 

## Transformers for Language Modeling (LLM)    

> Attention is all you
> Embedding Matrix
> [V x D]

Learn an embedding matrix  at the start of 

the model to convert words into vectors. 

Given vocab size V and model dimension 

D, it ’s a lookup table of shape [V x D] 

Use masked attention inside each 

transformer block so each token can only 

see the ones before it 

At the end, learn a projection matrix  of 

shape [D x V] to project each D -dim 

vector to a V -dim vector of scores for 

each element of the vocabulary.    

> Projection Matrix
> [D x V]
> is all you need

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 99 

## Transformers for Language Modeling (LLM)    

> Attention is all you
> Embedding Matrix
> [V x D]

Learn an embedding matrix  at the start of 

the model to convert words into vectors. 

Given vocab size V and model dimension 

D, it ’s a lookup table of shape [V x D] 

Use masked attention inside each 

transformer block so each token can only 

see the ones before it 

At the end, learn a projection matrix  of 

shape [D x V] to project each D -dim 

vector to a V -dim vector of scores for 

each element of the vocabulary. 

Train to predict next token using softmax 

+ cross -entropy loss    

> Projection Matrix
> [D x V]
> is all you need

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 100 

## Vision Transformers ( ViT )

Input image :

e.g. 224 x224 x3

Dosovitskiy et al, “An Image is Worth 

16 x16 Words: Tran sformers fo r Image 

Recognition at Scale ”, ICLR 202 1 Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 101 

## Vision Transformers ( ViT )

Input image :

e.g. 224 x224 x3

Break into patches 

e.g. 16 x16 x3

Dosovitskiy et al, “An Image is Worth 

16 x16 Words: Tran sformers fo r Image 

Recognition at Scale ”, ICLR 202 1 Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 102 

## Vision Transformers ( ViT )

Input image :

e.g. 224 x224 x3

Break into patches 

e.g. 16 x16 x3

Flatten and apply a linear 

transform 768 => D     

> Dosovitskiy et al, “An Image is Worth
> 16 x16 Words: Tran sformers fo r Image
> Recognition at Scale ”, ICLR 202 1

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 103 

## Vision Transformers ( ViT )

Input image :

e.g. 224 x224 x3

Break into patches 

e.g. 16 x16 x3

Flatten and apply a linear 

transform 768 => D     

> Dosovitskiy et al, “An Image is Worth
> 16 x16 Words: Tran sformers fo r Image
> Recognition at Scale ”, ICLR 202 1

Q: Any other way to 

describe this operation? Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 104 

## Vision Transformers ( ViT )

Input image :

e.g. 224 x224 x3

Break into patches 

e.g. 16 x16 x3

Flatten and apply a linear 

transform 768 => D     

> Dosovitskiy et al, “An Image is Worth
> 16 x16 Words: Tran sformers fo r Image
> Recognition at Scale ”, ICLR 202 1

Q: Any other way to 

describe this operation? 

A: 16 x16 conv with stride 

16 , 3 input channels, D 

output channels Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 105 

## Vision Transformers ( ViT )

Input image :

e.g. 224 x224 x3

Break into patches 

e.g. 16 x16 x3

Flatten and apply a linear 

transform 768 => D 

D-dim vector per patch 

are the input vectors to 

the Transformer     

> Dosovitskiy et al, “An Image is Worth
> 16 x16 Words: Tran sformers fo r Image
> Recognition at Scale ”, ICLR 202 1

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 106 

## Vision Transformers ( ViT )

Input image :

e.g. 224 x224 x3

Break into patches 

e.g. 16 x16 x3

Flatten and apply a linear 

transform 768 => D 

D-dim vector per patch 

are the input vectors to 

the Transformer 

Use positional 

encoding to tell 

the transformer 

the 2D position 

of each patch     

> Dosovitskiy et al, “An Image is Worth
> 16 x16 Words: Tran sformers fo r Image
> Recognition at Scale ”, ICLR 202 1

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 107 

## Vision Transformers ( ViT )

Input image :

e.g. 224 x224 x3

Break into patches 

e.g. 16 x16 x3

Flatten and apply a linear 

transform 768 => D 

D-dim vector per patch 

are the input vectors to 

the Transformer 

Don ’t use any 

masking; each 

image patch can 

look at all other 

image patches 

Use positional 

encoding to tell 

the transformer 

the 2D position 

of each patch     

> Dosovitskiy et al, “An Image is Worth
> 16 x16 Words: Tran sformers fo r Image
> Recognition at Scale ”, ICLR 202 1

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 108 

## Vision Transformers ( ViT )

Input image :

e.g. 224 x224 x3

Break into patches 

e.g. 16 x16 x3

Flatten and apply a linear 

transform 768 => D 

D-dim vector per patch 

are the input vectors to 

the Transformer 

Don ’t use any 

masking; each 

image patch can 

look at all other 

image patches 

Use positional 

encoding to tell 

the transformer 

the 2D position 

of each patch 

Transformer 

gives an output 

vector per patch     

> Dosovitskiy et al, “An Image is Worth
> 16 x16 Words: Tran sformers fo r Image
> Recognition at Scale ”, ICLR 202 1

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 109 

## Vision Transformers ( ViT )

Input image :

e.g. 224 x224 x3

Break into patches 

e.g. 16 x16 x3

Flatten and apply a linear 

transform 768 => D 

D-dim vector per patch 

are the input vectors to 

the Transformer 

Don ’t use any 

masking; each 

image patch can 

look at all other 

image patches 

Use positional 

encoding to tell 

the transformer 

the 2D position 

of each patch 

Transformer 

gives an output 

vector per patch 

Pooling 

Average pool NxD vectors to 

1xD, apply a linear layer 

D=>C to predict class scores     

> Dosovitskiy et al, “An Image is Worth
> 16 x16 Words: Tran sformers fo r Image
> Recognition at Scale ”, ICLR 202 1

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 110 

## Tweaking Transformers 

x1 x2 x3 x4

y1 y2 y3 y4

MLP  MLP  MLP  MLP 

Self -Attention 

Layer Normalization 

+

Layer Normalization 

+

The Transformer architecture has not 

changed much since 2017 .

But a few changes have become common: Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 111 

x1 x2 x3 x4

y1 y2 y3 y4

MLP  MLP  MLP  MLP 

Self -Attention 

Layer Normalization 

+

Layer Normalization 

+

## Pre -Norm Transformer 

Layer normalization is outside 

the residual connections 

Kind of weird, the model can ’t

actually learn the identify function      

> Baevski &Auli ,“Adaptive Input Representations for Neural Language Modeling ”,arXiv 2018

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 112 

x1 x2 x3 x4

y1 y2 y3 y4

MLP  MLP  MLP  MLP 

Self -Attention 

Layer Normalization 

+

Layer Normalization 

+

## Pre -Norm Transformer 

Layer normalization is outside 

the residual connections 

Kind of weird, the model can ’t

actually learn the identify function 

Solution : Move layer 

normalization before the Self -

Attention and MLP, inside the 

residual connections. Training is 

more stable.      

> Baevski &Auli ,“Adaptive Input Representations for Neural Language Modeling ”,arXiv 2018

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 113 

x1 x2 x3 x4

y1 y2 y3 y4

MLP  MLP  MLP  MLP 

Self -Attention 

RMSNorm 

+

RMSNorm 

+

## RMSNorm 

Replace Layer Normalization 

with Root -Mean -Square 

Normalization ( RMSNorm )

Input : x [shape D] 

Output : y [shape D] 

Weight : 𝛾 [shape D] 

𝑦 𝑖 = 𝑥 𝑖 

𝑅𝑀𝑆 (𝑥 ) ∗ 𝛾 𝑖 

𝑅𝑀𝑆 𝑥 = 𝜀 + 1

𝑁 ෍𝑖 =1

> 𝑁

𝑥 𝑖 

> 2

Training is a bit more stable     

> Zhang and Sennrich ,“Root Mean Square Layer Normalization ”,NeurIPS 2019

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 114 

x1 x2 x3 x4

y1 y2 y3 y4

MLP  MLP  MLP  MLP 

Self -Attention 

RMSNorm 

+

RMSNorm 

+

## SwiGLU MLP 

Classic MLP :

Input : X [N x D] 

Weights : W 1 [D x 4D] 

W2 [4D x D] 

Output : Y =  σ(XW 1)W 2 [N x D]   

> Shazeer ,“GLU Variants Improve Transformers ”,2020

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 115 

x1 x2 x3 x4

y1 y2 y3 y4

MLP  MLP  MLP  MLP 

Self -Attention 

RMSNorm 

+

RMSNorm 

+

## SwiGLU MLP 

Classic MLP :

Input : X [N x D] 

Weights : W 1 [D x 4D] 

W2 [4D x D] 

Output : Y =  σ(XW 1)W 2 [N x D]   

> Shazeer ,“GLU Variants Improve Transformers ”,2020

SwiGLU MLP :

Input : X [N x D] 

Weights : W 1 , W 2 [D x H] 

W3 [H x D] 

Output :

𝑌 = 𝜎 𝑋 𝑊 1 ⊙ 𝑋 𝑊 2 𝑊 3

Setting H = 8D/ 3 keeps 

same total params Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 116 

x1 x2 x3 x4

y1 y2 y3 y4

MLP  MLP  MLP  MLP 

Self -Attention 

RMSNorm 

+

RMSNorm 

+

## SwiGLU MLP 

Classic MLP :

Input : X [N x D] 

Weights : W 1 [D x 4D] 

W2 [4D x D] 

Output : Y =  σ(XW 1)W 2 [N x D]   

> Shazeer ,“GLU Variants Improve Transformers ”,2020

SwiGLU MLP :

Input : X [N x D] 

Weights : W 1 , W 2 [D x H] 

W3 [H x D] 

Output :

𝑌 = 𝜎 𝑋 𝑊 1 ⊙ 𝑋 𝑊 2 𝑊 3

We offer no explanation as 

to why these architectures 

seem to work; we attribute 

their success, as all else, 

to divine benevolence. 

Setting H = 8D/ 3 keeps 

same total params Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 117 

x1 x2 x3 x4

y1 y2 y3 y4

MLP  MLP  MLP  MLP 

Self -Attention 

RMSNorm 

+

RMSNorm 

+

## Mixture of Experts ( MoE )

Learn E separate sets of MLP weights in 

each block; each MLP is an expert 

W1: [D x 4D] => [E x D x 4D] 

W2: [ 4D x D] => [E x 4D x D]    

> Shazeer et al, “Outrageously Large Neural Networks: The Sparsely -Gated Mixture -of -Experts Layer ”,2017

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 118 

x1 x2 x3 x4

y1 y2 y3 y4

MLP  MLP  MLP  MLP 

Self -Attention 

RMSNorm 

+

RMSNorm 

+

## Mixture of Experts ( MoE )

Learn E separate sets of MLP weights in 

each block; each MLP is an expert 

W1: [D x 4D] => [E x D x 4D] 

W2: [ 4D x D] => [E x 4D x D] 

Each token gets routed to A < E of the 

experts. These are the active experts .

Increases params by E, 

But only increases compute by A    

> Shazeer et al, “Outrageously Large Neural Networks: The Sparsely -Gated Mixture -of -Experts Layer ”,2017

Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 119 

x1 x2 x3 x4

y1 y2 y3 y4

MLP  MLP  MLP  MLP 

Self -Attention 

RMSNorm 

+

RMSNorm 

+

## Mixture of Experts ( MoE )

Learn E separate sets of MLP weights in 

each block; each MLP is an expert 

W1: [D x 4D] => [E x D x 4D] 

W2: [ 4D x D] => [E x 4D x D] 

Each token gets routed to A < E of the 

experts. These are the active experts .

Increases params by E, 

But only increases compute by A 

All of the biggest LLMs today (e.g. 

GPT 4o, GPT 4.5 , Claude 3.7 , Gemini 2.5 

Pro, etc ) almost certainly use MoE and 

have > 1T params; but they don ’t publish 

details anymore Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 120 

## Tweaking Transformers 

x1 x2 x3 x4

y1 y2 y3 y4

MLP  MLP  MLP  MLP 

Self -Attention 

RMSNorm 

+

RMSNorm 

+

The Transformer architecture has not 

changed much since 2017 .

But a few changes have become common: 

- Pre -Norm: Move normalization inside 

residual 

- RMSNorm : Different normalization layer 

- SwiGLU : Different MLP architecture 

- Mixture of Experts ( MoE ): Learn E 

different MLPs, use A < E of them per 

token. Massively increase params, 

modest increase to compute cost. Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 -

# Summary: Attention + Transformers 

121 

Attention : A new primitive that 

operates on sets of vectors 

Transformer : A neural 

network architecture that 

uses attention everywhere 

Transformers are the 

backbone of all large 

AI models today! 

Used for language, 

vision, speech, …Stanford CS 231 n 10 th Anniversary  April 24 , 2025 Lecture 8 - 122 

# Next Time: 

# Detection, Segmentation, 

# Visualization