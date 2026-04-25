# Source: https://academic.oup.com/imajna/article/41/4/2311/5893596
# Author: Blanchard, Pierre, Higham, Desmond J, Higham, Nicholas J
# Author Slug: blanchard-pierre-higham-desmond-j-higham-nicholas-j
# Title: Accurately computing the log-sum-exp and softmax functions
# Fetched via: browser
# Date: 2026-04-08

Abstract

Evaluating the log-sum-exp function or the softmax function is a key step in many modern data science algorithms, notably in inference and classification. Because of the exponentials that these functions contain, the evaluation is prone to overflow and underflow, especially in low-precision arithmetic. Software implementations commonly use alternative formulas that avoid overflow and reduce the chance of harmful underflow, employing a shift or another rewriting. Although mathematically equivalent, these variants behave differently in floating-point arithmetic and shifting can introduce subtractive cancellation. We give rounding error analyses of different evaluation algorithms and interpret the error bounds using condition numbers for the functions. We conclude, based on the analysis and numerical experiments, that the shifted formulas are of similar accuracy to the unshifted ones, so can safely be used, but that a division-free variant of softmax can suffer from loss of accuracy.

log-sum-exp, softmax, floating-point arithmetic, rounding error analysis, overflow, underflow, condition number
Issue Section: Article
Collection: IMA Journals
1. Introduction
In many applications, especially in a wide range of machine learning classifiers such as multinomial linear regression and naive Bayes classifiers (Williams & Barber, 1998; Murphy, 2012; Calafiore et al., 2019), one needs to compute an expression of the form


𝑦
=
𝑓
(
𝑥
)
=
log
⁡
∑
𝑖
=
1
𝑛
𝑒
𝑥
𝑖
,
(1.1)
where 
𝑥
=
[
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
]
T
∈
𝑅
𝑛
 and 
log
 is the natural logarithm. The function 
𝑓
:
𝑅
𝑛
→
𝑅
 is often referred to as log-sum-exp or LSE. Its gradient 
𝑔
:
𝑅
𝑛
→
𝑅
𝑛
⁠, given by
𝑔
𝑗
(
𝑥
)
=
𝜕
𝜕
𝑥
𝑗
𝑓
(
𝑥
)
=
𝑒
𝑥
𝑗
∑
𝑖
=
1
𝑛
𝑒
𝑥
𝑖
,
𝑗
=
1
:
𝑛
,
(1.2)
is called softmax and is also a key function in classification algorithms (Efron & Hastie, 2016, p. 355; Goodfellow et al., 2016, p. 78; Higham & Higham, 2019). It is often the case that log-sum-exp and softmax are required simultaneously.

The most obvious danger in evaluating (1.1) and (1.2) is overflow. We are interested in IEEE arithmetic in the precisions half (fp16), single (fp32) and double (fp64) (IEEE, 2019), as well as the bfloat16 half-precision format (Intel Corporation, 2018). Table 1 shows the key parameters of interest for these precisions: the unit roundoff 
𝑢
⁠, the largest finite number 
𝑟
max
 and the smallest positive normalized and subnormal floating-point numbers. If some 
𝑥
𝑖
 exceeds the relevant 
log
⁡
𝑟
max
 value in Table 2 then overflow will occur in evaluating 
𝑒
𝑥
𝑖
⁠. Clearly, overflow is possible even for quite modestly sized 
𝑥
⁠, especially for half and single precision.

TABLE 1
Open in new tab

Parameters for bfloat16 and IEEE fp16, fp32 and fp64 arithmetics, to three significant figures: unit roundoff 
𝑢
⁠, smallest positive (subnormal) number 
𝑟
min
(
𝑠
)
⁠, smallest positive normalized number 
𝑟
min
 and largest finite number 
𝑟
max
⁠. In Intel’s bfloat16 specification subnormal numbers are not supported, so 
𝑟
min
(
𝑠
)
=
𝑟
min
 (Intel Corporation, 2018)

	
𝑢
	
𝑟
min
(
𝑠
)
	
𝑟
min
	
𝑟
max

bfloat16	
3.91
×
10
−
3
	
9.18
×
10
−
41
	
1.18
×
10
−
38
	
3.39
×
10
38

fp16	
4.88
×
10
−
4
	
5.96
×
10
−
8
	
6.10
×
10
−
5
	
6.55
×
10
4

fp32	
5.96
×
10
−
8
	
1.40
×
10
−
45
	
1.18
×
10
−
38
	
3.40
×
10
38

fp64	
1.11
×
10
−
16
	
4.94
×
10
−
324
	
2.22
×
10
−
308
	
1.80
×
10
308
TABLE 2
Open in new tab

Logarithms of key parameters in Table 1, to three significant figures

	
log
⁡
𝑟
min
(
𝑠
)
	
log
⁡
𝑟
min
	
log
⁡
𝑟
max

bfloat16	
−
92.2
	
−
87.3
	
88.7

fp16	
−
16.6
	
−
9.70
	
11.0

fp32	
−
103
	
−
87.3
	
88.7

fp64	
−
744
	
−
708
	
710

Underflow is also possible. For example, for 
𝑛
=
1
⁠, if 
𝑥
1
 is a finite floating-point number with 
𝑥
1
<
log
⁡
𝑟
min
(
𝑠
)
/
2
 then1
f
l
(
𝑓
(
𝑥
1
)
)
=
f
l
(
log
⁡
(
f
l
(
𝑒
𝑥
1
)
)
)
=
f
l
(
log
⁡
0
)
=
−
∞
 with round to nearest, whereas 
𝑓
(
𝑥
1
)
=
𝑥
1
⁠. For 
𝑛
>
1
⁠, underflow is damaging when all the 
𝑥
𝑖
 are less than 
log
⁡
𝑟
min
(
𝑠
)
⁠. As well as avoiding harmful underflow it is desirable to avoid generating subnormal numbers, which incur a performance penalty if handled in software;2 see Higham (2002) or Muller et al. (2018) for details of subnormal numbers.

A way to avoid overflow, and to attempt to avoid harmful underflow and subnormal numbers, in evaluating log-sum-exp is to rewrite
	






𝑦
	
=
log
⁡
∑
𝑖
=
1
𝑛
𝑒
𝑥
𝑖
=
log
⁡
∑
𝑖
=
1
𝑛
𝑒
𝑎
𝑒
𝑥
𝑖
−
𝑎
=
log
⁡
(
𝑒
𝑎
∑
𝑖
=
1
𝑛
𝑒
𝑥
𝑖
−
𝑎
)
.
Hence


𝑦
=
𝑎
+
log
⁡
∑
𝑖
=
1
𝑛
𝑒
𝑥
𝑖
−
𝑎
.
(1.3)
We note that (1.3) remains valid for complex 
𝑥
𝑖
 with 
log
 the principal logarithm (the one whose imaginary part lies in 
(
−
𝜋
,
𝜋
]
⁠), provided that 
𝑎
∈
𝑅
 (Aprahamian & Higham, 2014, Lem. 2.5). The softmax function can be expressed in a related form:
𝑔
𝑗
=
𝑒
𝑥
𝑗
−
𝑎
∑
𝑖
=
1
𝑛
𝑒
𝑥
𝑖
−
𝑎
,
𝑗
=
1
:
𝑛
.
(1.4)
This shifting, typically with 
𝑎
=
max
𝑖
𝑥
𝑖
⁠, is a well-known way to attempt to avoid overflow and underflow in the evaluation of 
𝑓
 and 
𝑔
⁠, described in many places, including on Wikipedia,3 in blog posts4 and even in a YouTube video.5 The functions logsumexp in SciPy 1.3.1 (Jones et al., 2001) and LogSumExp in R (R Core Team) both implement (1.3) with 
𝑎
=
max
𝑖
𝑥
𝑖
⁠. The function softmax in the MATLAB Deep Learning Toolbox (R2019b) (Deep Learning Toolbox) uses (1.4) with 
𝑎
=
max
𝑖
𝑥
𝑖
⁠.
An alternative to (1.4), which removes the denominator of (1.2) by rewriting it as 
𝑒
𝑦
 and moving it into the numerator, is


𝑔
𝑗
=
exp
⁡
(
𝑥
𝑗
−
log
⁡
∑
𝑖
=
1
𝑛
𝑒
𝑥
𝑖
)
.
(1.5)
The conciseness of this division-free formula makes it attractive for implementing softmax when a log-sum-exp function is available. This formula is used in the SciPy 1.4.1 function softmax, in a MATLAB toolbox (Matlab Code for Machine Learning Algorithms in Book PRML) associated with the book Bishop (2006), in the internal function softmax in the MATLAB Statistics and Machine Learning Toolbox (R2019b) (Statistics and Machine Learning Toolbox) and in Wang et al. (2018); in each case the log-sum-exp term is computed by (1.3) with 
𝑎
=
max
𝑖
𝑥
𝑖
⁠. Formula (1.5) can also be found in codes posted in online communities such as Stack Exchange.

Because of the importance of the log-sum-exp and softmax functions, great efforts are made to optimize their implementations in software (Czaja et al., 2019) and hardware (Wang et al., 2018). Yet we are not aware of any investigation of the accuracy of the different formulas in floating-point arithmetic, and indeed the accuracy properties are not clear. In particular, when 
𝑎
=
max
𝑖
𝑥
𝑖
<
0
⁠, 
𝑦
 in (1.3) is computed as the sum of two terms of opposite sign, so there could potentially be damaging subtractive cancellation that appears not to be present in (1.1). We note that Guo et al. (2020, sec. 4.3) limit the size of 
𝑎
 in (1.4), stating that the shift causes loss of accuracy by up to a factor 
𝑒
𝑎
⁠.

In this work we carry out a rounding error analysis of the unshifted and shifted formulas and (1.5) in order to determine which choices of formulas give the best accuracy and reliability. We relate the error bounds to the conditioning of 
𝑓
 and 
𝑔
⁠. We show that the shifted formulas have broadly similar error bounds to the unshifted ones and so are entirely appropriate for practical use. We find, however, that the alternative softmax formula (1.5) has a less favorable error bound than the shifted formula and tends to produce larger errors in practice.

We begin, in the next section, by investigating the conditioning of the log-sum-exp and softmax functions. In Section 3 we give detailed rounding error analyses of the basic formulas. In Section 4 we analyze the shifted formulas and (1.5) and compare their error bounds with those for unshifted formulas. Numerical experiments are given in Section 5 to test the accuracy of the evaluations and also to examine how the sum of the computed softmax vector entries compares with the exact value 
1
⁠. Conclusions are given in Section 6.

From now on we write



𝑥
max
=
max
𝑖
𝑥
𝑖
,
𝑥
min
=
min
𝑖
𝑥
𝑖
.
(1.6)
We will use the standard model of floating-point arithmetic (Higham, 2002, sec. 2.2)
f
l
(
𝑎
op
𝑏
)
=
(
𝑎
op
𝑏
)
(
1
+
𝛿
)
,
|
𝛿
|
⩽
𝑢
,
op
∈
{
+
,
−
,
×
,
/
}
.
(1.7)
2. Condition numbers and forward stability

Before considering algorithms for computing log-sum-exp and softmax we investigate the conditioning of these functions, that is, the sensitivity of 
𝑓
(
𝑥
)
 and 
𝑔
(
𝑥
)
 in (1.1) and (1.2) to small perturbations in 
𝑥
⁠.

We define the condition number of 
𝑓
 in the usual way (see, e.g., Higham, 2008, chap. 3), by



cond
(
𝑓
,
𝑥
)
:=
lim
𝜖
→
0
sup
‖
𝛥
𝑥
‖
⩽
𝜖
‖
𝑥
‖
|
𝑓
(
𝑥
+
𝛥
𝑥
)
−
𝑓
(
𝑥
)
|
𝜖
|
𝑓
(
𝑥
)
|
.
This definition implies that
|
𝑓
(
𝑥
+
𝛥
𝑥
)
−
𝑓
(
𝑥
)
|
|
𝑓
(
𝑥
)
|
⩽
cond
(
𝑓
,
𝑥
)
‖
𝛥
𝑥
‖
‖
𝑥
‖
+
𝑜
(
‖
𝛥
𝑥
‖
)
,
(2.1)
so that 
cond
(
𝑓
,
𝑥
)
 measures the worst-case relative change in 
𝑓
 corresponding to a small relative change in 
𝑥
⁠. It is easy to show that for the 
∞
-norm,
cond
∞
(
𝑓
,
𝑥
)
=
‖
∇
𝑓
(
𝑥
)
‖
1
‖
𝑥
‖
∞
|
𝑓
(
𝑥
)
|
=
‖
𝑥
‖
∞
|
𝑓
(
𝑥
)
|
=
max
𝑖
|
𝑥
𝑖
|
|
log
⁡
∑
𝑖
𝑒
𝑥
𝑖
|
,
(2.2)
since 
‖
∇
𝑓
(
𝑥
)
‖
1
=
1
 by (1.2).

We identify two extreme cases. First, the condition number is infinite when 
𝑥
𝑖
=
−
log
⁡
𝑛
 for all 
𝑖
⁠, because 
𝑓
(
𝑥
)
=
0
⁠. Hence when 
𝑥
𝑖
≈
−
log
⁡
𝑛
 for all 
𝑖
 the condition number must be large. Secondly, 
|
𝑓
(
𝑥
)
|
≥
max
𝑖
𝑥
𝑖
⁠, so if 
max
𝑖
𝑥
𝑖
=
max
𝑖
|
𝑥
𝑖
|
 then 
cond
∞
(
𝑓
,
𝑥
)
⩽
1
 and the problem is perfectly conditioned.

A forward stable algorithm for computing log-sum-exp is one for which the relative error of the computed result is bounded by 
𝑝
(
𝑛
)
cond
(
𝑓
,
𝑥
)
𝑢
⁠, for some low-degree polynomial 
𝑝
⁠. Ideally, we would like the algorithm that we use to be forward stable. To see whether it is reasonable to expect forward stability consider the case 
𝑛
=
1
⁠. Then 
𝑦
=
𝑓
(
𝑥
)
=
log
⁡
𝑒
𝑥
=
𝑥
⁠, so 
cond
(
𝑓
,
𝑥
)
=
1
⁠: the problem is perfectly conditioned. When we compute 
𝑓
 using standard library functions we can expect to obtain relative errors in the computed exponential and logarithm bounded by 
𝑢
 (de Dinechin et al., 2007; Muller, 2016; Muller et al., 2018, Chap. 10), that is,
𝑦
^
=
f
l
(
𝑓
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
(
1
+
𝛿
1
)
)
(
1
+
𝛿
2
)
,
|
𝛿
1
|
,
|
𝛿
2
|
⩽
𝑢
.
(2.3)
The term 
1
+
𝛿
2
 causes just a small relative perturbation of 
𝑦
^
⁠, so we have
	
𝑦
^
≈
log
⁡
(
𝑒
𝑥
(
1
+
𝛿
1
)
)
	
=
𝑥
+
log
⁡
(
1
+
𝛿
1
)
=
𝑥
+
𝛿
1
+
𝑂
(
𝛿
1
2
)
.
Hence, since 
𝑦
=
𝑥
⁠,
|
𝑦
−
𝑦
^
|
|
𝑦
|
≲
𝑢
|
𝑥
|
+
𝑂
(
𝑢
2
)
.
(2.4)
This relative error bound is much larger than 
𝑢
 for 
|
𝑥
|
≪
1
⁠, even though the problem is perfectly conditioned. So it is not reasonable to expect an algorithm to be unconditionally forward stable in floating-point arithmetic. For this trivial computation, backward error and forward error are the same, so we also conclude that we cannot expect to obtain an algorithm that is unconditionally backward stable.
The softmax function has condition number



cond
(
𝑔
,
𝑥
)
:=
lim
𝜖
→
0
sup
‖
Δ
𝑥
‖
⩽
𝜖
‖
𝑥
‖
‖
𝑔
(
𝑥
+
Δ
𝑥
)
−
𝑔
(
𝑥
)
‖
𝜖
‖
𝑔
(
𝑥
)
‖
,
which is given explicitly by
cond
(
𝑔
,
𝑥
)
=
‖
𝐺
(
𝑥
)
‖
‖
𝑥
‖
‖
𝑔
(
𝑥
)
‖
.
Here the 
𝑛
×
𝑛
 matrix 
𝐺
(
𝑥
)
=
(
𝜕
𝑔
𝑖
/
𝜕
𝑥
𝑗
)
 is the Jacobian of 
𝑔
 and 
‖
⋅
‖
 denotes any vector norm and the corresponding subordinate matrix norm. We note in passing that 
𝐺
 is the Hessian of 
𝑓
 and can be shown to be symmetric positive semidefinite for all 
𝑥
 (Boyd & Vandenberghe, 2004, p. 74). Now
	

	
𝜕
𝑔
𝑖
𝜕
𝑥
𝑗
=
{
−
𝑒
𝑥
𝑖
𝑒
𝑥
𝑗
(
∑
𝑘
=
1
𝑛
𝑒
𝑥
𝑘
)
2
,
	
𝑖
≠
𝑗
,


𝑒
𝑥
𝑖
∑
𝑘
=
1
𝑛
𝑒
𝑥
𝑘
−
𝑒
2
𝑥
𝑖
(
∑
𝑘
=
1
𝑛
𝑒
𝑥
𝑘
)
2
,
	
𝑖
=
𝑗
.
We have, for each 
𝑖
⁠,






∑
𝑗
=
1
𝑛
|
𝜕
𝑔
𝑖
𝜕
𝑥
𝑗
|
=
2
𝑒
𝑥
𝑖
∑
𝑗
=
1
𝑗
≠
𝑖
𝑛
𝑒
𝑥
𝑗
(
∑
𝑘
=
1
𝑛
𝑒
𝑥
𝑘
)
2
⩽
1
,
(2.5)
that is, 
‖
𝐺
(
𝑥
)
‖
∞
⩽
1
⁠. Hence
cond
∞
(
𝑔
,
𝑥
)
⩽
‖
𝑥
‖
∞
‖
𝑔
(
𝑥
)
‖
∞
⩽
𝑛
‖
𝑥
‖
∞
because 
‖
𝑔
‖
∞
≥
𝑛
−
1
‖
𝑔
‖
1
=
𝑛
−
1
⁠.

We note that if 
𝑥
𝑖
≡
𝜉
 for all 
𝑖
 then 
‖
𝑔
(
𝑥
)
‖
∞
=
𝑛
−
1
 and 
‖
𝐺
‖
∞
=
2
(
𝑛
−
1
)
/
𝑛
2
 by (2.5), so 
cond
∞
(
𝑔
,
𝑥
)
=
(
2
(
𝑛
−
1
)
/
𝑛
)
‖
𝑥
‖
∞
⁠. Hence 
cond
∞
(
𝑔
,
𝑥
)
 can be arbitrarily large.

We also note that shifting, as in (1.3) and (1.4), does not change the functions so does not change their condition numbers; likewise for (1.5). These reformulations may, of course, affect the accuracy of the floating-point evaluation.

3. Basic algorithms and error analysis

Algorithm 3.1 gives a naive implementation of (1.1) and (1.2).

 

ALGORITHM 3.1 Given 
𝑥
∈
𝑅
𝑛
 this algorithm computes 
𝑓
(
𝑥
)
=
log
⁡
∑
𝑖
=
1
𝑛
𝑒
𝑥
𝑖
 and the gradient 
𝑔
(
𝑥
)
=
∇
𝑓
(
𝑥
)
⁠.

 

1 
𝑠
=
0

2 for 
𝑖
=
1
:
𝑛

3 
𝑤
𝑖
=
exp
⁡
(
𝑥
𝑖
)

4 
𝑠
=
𝑠
+
𝑤
𝑖

5 end

6 
𝑓
=
log
⁡
(
𝑠
)

7 for 
𝑖
=
1
:
𝑛

8 
𝑔
𝑖
=
𝑤
𝑖
/
𝑠

9 end

What can be said about the accuracy of this algorithm when it is implemented in floating-point arithmetic? To answer this question we carry out a rounding error analysis. Throughout this section we assume that there is no overflow or underflow.

First we consider the error in evaluating the sum of positive terms




𝑠
=
∑
𝑖
=
1
𝑛
𝑒
𝑥
𝑖
≡
∑
𝑖
=
1
𝑛
𝑤
𝑖
.
Evaluating 
𝑤
𝑖
=
𝑒
𝑥
𝑖
 yields a computed result satisfying
𝑤
^
𝑖
=
𝑒
𝑥
𝑖
(
1
+
𝛿
1
)
,
(3.1)
where, as noted in Section 2, we can expect the relative error from the exponential evaluation to satisfy 
|
𝛿
1
|
⩽
𝑢
⁠. Therefore
|
𝑤
^
𝑖
−
𝑤
𝑖
|
⩽
𝑤
𝑖
𝑢
.
Write the (exact) sum of computed quantities as


𝑠
~
=
∑
𝑖
=
1
𝑛
𝑤
^
𝑖
.
The rounding error analysis in Higham (1993) and Higham (2002, sec. 4.2) shows that the computed sum 
𝑠
^
 satisfies6


|
𝑠
~
−
𝑠
^
|
⩽
𝑢
∑
𝑖
=
1
𝑛
−
1
|
𝑡
𝑖
|
+
𝑂
(
𝑢
2
)
,
where 
𝑡
𝑖
=
∑
𝑗
=
1
𝑖
+
1
𝑤
^
𝑗
⁠, so that, since 
𝑤
^
𝑖
≥
0
⁠,


|
𝑠
~
−
𝑠
^
|
⩽
𝑢
(
𝑛
−
1
)
(
𝑤
^
1
+
𝑤
^
2
)
+
𝑢
∑
𝑖
=
3
𝑛
(
𝑛
+
1
−
𝑖
)
𝑤
^
𝑖
+
𝑂
(
𝑢
2
)
.
Here and throughout this paper, the 
𝑂
(
𝑢
2
)
 term is innocuous in that it becomes significant only when the corresponding first-order term is already so large that it provides no useful information; see Blanchard et al. (2020, sec. 2.1.2) for details of these terms for summation. Writing 
𝑠
−
𝑠
^
=
𝑠
−
𝑠
~
+
𝑠
~
−
𝑠
^
 we obtain
	



	





	


|
𝑠
−
𝑠
^
|
	
⩽
∑
𝑖
=
1
𝑛
|
𝑤
^
𝑖
−
𝑤
𝑖
|
+
|
𝑠
~
−
𝑠
^
|

	
⩽
𝑢
∑
𝑖
=
1
𝑛
𝑤
𝑖
+
𝑢
∑
𝑖
=
1
𝑛
(
𝑛
+
1
−
𝑖
)
𝑤
^
𝑖
+
𝑂
(
𝑢
2
)

	
=
∑
𝑖
=
1
𝑛
(
𝑛
+
2
−
𝑖
)
𝑤
𝑖
+
𝑂
(
𝑢
2
)
,
(3.2)
since 
𝑤
^
𝑖
=
𝑤
𝑖
+
𝑂
(
𝑢
)
⁠. Hence
𝑠
^
=
𝑠
+
𝛥
𝑠
,
|
𝛥
𝑠
|
⩽
(
𝑛
+
1
)
𝑢
𝑠
+
𝑂
(
𝑢
2
)
.
(3.3)
Then the computed log-sum-exp is
	

	
	

	
𝑦
^
	
=
f
l
(
log
⁡
𝑠
^
)
=
log
⁡
(
𝑠
^
)
(
1
+
𝜖
)
,
|
𝜖
|
⩽
𝑢
,

	
=
log
⁡
(
𝑠
+
𝛥
𝑠
)
(
1
+
𝜖
)

	
=
(
log
⁡
𝑠
+
𝛥
𝑠
𝑠
+
𝑂
(
𝑢
2
)
)
(
1
+
𝜖
)

	
=
𝑦
(
1
+
𝜖
)
+
𝛥
𝑠
𝑠
+
𝑂
(
𝑢
2
)
.
(3.4)
Using (3.3) we obtain
|
𝑦
−
𝑦
^
|
⩽
𝑢
|
𝑦
|
+
(
𝑛
+
1
)
𝑢
+
𝑂
(
𝑢
2
)
,
which gives the following result.

 

THEOREM 3.2
(Basic log-sum-exp algorithm).
In the absence of overflow and underflow the computed log-sum-exp 
𝑦
^
 from Algorithm 3.1 satisfies
|
𝑦
−
𝑦
^
𝑦
|
⩽
(
1
+
𝑛
+
1
|
𝑦
|
)
𝑢
+
𝑂
(
𝑢
2
)
.
(3.5)

This bound is a factor 
(
|
𝑦
|
+
𝑛
+
1
)
/
‖
𝑥
‖
∞
 larger than 
cond
∞
(
𝑓
,
𝑥
)
𝑢
 in (2.2). But 
|
𝑦
|
⩽
|
𝑥
max
|
+
log
⁡
𝑛
 from (1.1) (or see (4.2) below), so this factor is bounded by 
1
+
(
𝑛
+
1
+
log
⁡
𝑛
)
/
‖
𝑥
‖
∞
⁠. Hence we have forward stability as long as 
‖
𝑥
‖
∞
≳
1
⁠, but for 
‖
𝑥
‖
∞
≪
1
 the bound does not guarantee forward stability. This is consistent with the bound (2.4) for the case 
𝑛
=
1
⁠.

Turning to the evaluation of the softmax function 
𝑔
 from its definition (1.2), by (3.1) we have
𝑔
^
𝑗
=
𝑒
𝑥
𝑗
(
1
+
𝛿
1
)
𝑠
^
(
1
+
𝛿
2
)
,
|
𝛿
2
|
⩽
𝑢
,
where 
𝛿
2
 accounts for the division, and so by (3.3),
𝑔
^
𝑗
=
𝑒
𝑥
𝑗
𝑠
(
1
+
𝜂
)
(
1
+
𝛿
1
)
(
1
+
𝛿
2
)
,
|
𝜂
|
⩽
(
𝑛
+
1
)
𝑢
+
𝑂
(
𝑢
2
)
.
Therefore
	
𝑔
^
𝑗
	
=
𝑔
𝑗
(
1
+
𝜏
𝑗
)
,
|
𝜏
𝑗
|
⩽
(
𝑛
+
3
)
𝑢
+
𝑂
(
𝑢
2
)
.
This bound guarantees a relative error of order at most 
𝑛
𝑢
 in every component of 
𝑔
⁠. We weaken the bound into a normwise bound for the next theorem.

 

THEOREM 3.3
(Basic softmax algorithm).
In the absence of overflow and underflow the computed softmax 
𝑔
^
 from Algorithm 3.1 satisfies
‖
𝑔
−
𝑔
^
‖
∞
‖
𝑔
‖
∞
⩽
(
𝑛
+
3
)
𝑢
+
𝑂
(
𝑢
2
)
.
(3.6)

While the error bounds of Theorems 3.2 and 3.3 have a very satisfactory form, they provide no useful information when 
𝑛
≳
1
/
𝑢
⁠, and for fp16 this happens for 
𝑛
 as small as 
2048
⁠. We note, however, that the 
𝑛
 terms, which come from the summation, are pessimistic. It is shown by Higham & Mary (2019, Thm. 3.1) and Higham & Mary (2020, Thm. 2.5) that, under probabilistic models of rounding errors, 
𝑛
 in the error bound for summation can be replaced by a small constant multiple of 
𝑛
 with high probability, and the same holds for the bounds of Theorems 3.2 and 3.3.

Next consider the alternative formula (1.5), which we rewrite here:


𝑔
𝑗
=
exp
⁡
(
𝑥
𝑗
−
log
⁡
∑
𝑖
=
1
𝑛
𝑒
𝑥
𝑖
)
=
exp
⁡
(
𝑥
𝑗
−
𝑦
)
.
(3.7)
With 
𝑦
=
𝑓
(
𝑥
)
 evaluated in floating-point arithmetic by Algorithm 3.1, we obtain
	

	
𝑔
^
𝑗
	
=
(
1
+
𝛿
)
exp
⁡
[
(
𝑥
𝑗
−
𝑦
^
)
(
1
+
𝜖
)
]
,
|
𝛿
|
,
|
𝜖
|
⩽
𝑢
,

	
=
(
1
+
𝛿
)
exp
⁡
[
(
𝑥
𝑗
−
𝑦
+
(
𝑦
−
𝑦
^
)
)
(
1
+
𝜖
)
]
(3.8)
	
	
=
(
1
+
𝛿
)
𝑔
𝑗
exp
⁡
[
(
𝑥
𝑗
−
𝑦
)
𝜖
+
(
𝑦
−
𝑦
^
)
(
1
+
𝜖
)
]
(3.9)
	

	
	
=
(
1
+
𝛿
)
𝑔
𝑗
[
1
+
(
𝑥
𝑗
−
𝑦
)
𝜖
+
(
𝑦
−
𝑦
^
)
(
1
+
𝜖
)
+
𝑂
(
𝑢
2
)
]

	
=
(
1
+
𝜏
𝑗
)
𝑔
𝑗
,
(3.10)
where, using Theorem 3.2,
|
𝜏
𝑗
|
⩽
(
|
𝑦
|
+
|
𝑥
𝑗
−
𝑦
|
+
𝑛
+
2
)
𝑢
+
𝑂
(
𝑢
2
)
.
We summarize this result as follows.

 

THEOREM 3.4
(Alternative softmax algorithm).
In the absence of overflow and underflow the computed 
𝑔
^
 from (3.7) with the log-sum-exp computed by Algorithm 3.1 satisfies


‖
𝑔
−
𝑔
^
‖
∞
‖
𝑔
‖
∞
⩽
(
|
𝑦
|
+
max
𝑗
|
𝑥
𝑗
−
𝑦
|
+
𝑛
+
2
)
𝑢
+
𝑂
(
𝑢
2
)
.
(3.11)

From (4.2) and (4.3) below, using the notation (1.6), we have


|
𝑦
|
+
max
𝑗
|
𝑥
𝑗
−
𝑦
|
⩽
|
𝑥
max
|
+
|
𝑥
max
−
𝑥
min
|
+
2
log
⁡
𝑛
.
Hence (3.11) is less favorable than (3.6) when 
𝑥
max
−
𝑥
min
≫
𝑛
 or 
|
𝑥
max
|
≫
𝑛
⁠. The analysis therefore suggests that (1.2) should be preferred to (1.5).

To give an intuitive explanation for the potential inaccuracy in (3.7) we refer to the steps leading to (3.10). A large absolute error in the argument of the exp in (3.9) may lead to a large relative error in the result. This effect can be traced back to the appearance of 
𝑥
𝑗
−
𝑦
 in (3.8).

4. Algorithms with shifting

Now we consider the use of shifts in the log-sum-exp and softmax evaluations in order to avoid overflow and reduce the chance of harmful underflow. We are particularly interested to see whether the potential cancellation caused by the shift can lead to numerical instability.

Recall definition (1.6) of 
𝑥
max
 and 
𝑥
min
⁠. Overflow in the exponential evaluations in (1.3) is certainly avoided if we take 
𝑎
=
𝑥
max
⁠, as we then have 
𝑥
𝑖
−
𝑎
⩽
0
 and hence 
0
⩽
𝑒
𝑥
𝑖
−
𝑎
⩽
1
 for all 
𝑖
⁠. We can rewrite (1.3) as


𝑦
=
𝑥
max
+
log
⁡
(
1
+
∑
𝑖
=
1
𝑖
≠
𝑘
𝑛
𝑒
𝑥
𝑖
−
𝑥
max
)
,
(4.1)
where 
𝑥
𝑘
=
𝑥
max
 (if there is more than one such 
𝑘
⁠, we can take any of them). From this expression we see that
𝑥
max
⩽
𝑦
⩽
𝑥
max
+
log
⁡
𝑛
.
(4.2)
It follows that when 
𝑥
max
≥
0
 the sum ‘
𝑥
max
+
log
⁡
(
⋅
)
’ that produces 
𝑦
 in (4.1) cannot suffer cancellation.

Note that for 
𝑛
=
1
⁠, (4.1) trivially provides the exact result 
𝑦
=
𝑥
max
⁠, in contrast to the basic formula (1.1).

For later use we note that (4.2) implies that, for any 
𝑗
⁠,
|
𝑦
−
𝑥
𝑗
|
⩽
|
𝑥
max
−
𝑥
𝑗
|
+
log
⁡
𝑛
⩽
|
𝑥
max
−
𝑥
min
|
+
log
⁡
𝑛
.
(4.3)

The 
log
 term in (4.1) has the form 
log
⁡
(
1
+
𝑠
)
⁠, where 
𝑠
≥
0
⁠. If 
𝑠
 is very small then 
1
+
𝑠
 will round to 
1
 and the logarithm will evaluate as zero, even though 
log
⁡
(
1
+
𝑠
)
≈
𝑠
≠
0
⁠. To avoid this loss of information we will use the function 
log
1
p
(
𝑠
)
=
log
⁡
(
1
+
𝑠
)
 provided in, for example, C, MATLAB and NumPy. These functions guarantee an accurate result for small 
𝑠
 (which can be achieved with a simple formula based on 
log
⁠; Hewlett-Packard, 1982; Higham, 2002, Prob. 1.5). The improved accuracy brought by 
log
1
p
(
𝑠
)
 for small 
𝑠
 is likely to benefit 
𝑦
 when 
𝑥
max
≈
−
𝑠
⁠.

These considerations lead to Algorithm 4.1.

Note that while it is important to avoid forming 
1
+
𝑠
 for the 
𝑓
-evaluation, for 
𝑔
 we can safely form 
1
+
𝑠
 because if 
𝑠
 is small it has little influence on 
𝑔
⁠.

Algorithm 4.1 avoids overflow. If underflow occurs in the exponential then it is in a term in the sum added to 
1
 in (4.1), so that term is negligible and the underflow is harmless. Note, in particular, that if 
𝑥
𝑖
≈
𝑥
<
log
⁡
𝑟
min
(
𝑠
)
/
2
 for all 
𝑖
 then, whereas Algorithm 3.1 returns 
𝑓
=
−
∞
⁠, Algorithm 4.1 suffers no underflow and returns 
𝑓
≳
𝑥
max
⁠.

The main question is how shifting affects the accuracy of the evaluations. We give a rounding error analysis to assess this question. The analysis is a generalization of that in the previous section for the unshifted algorithm.

 

Algorithm 4.1 (log-sum-exp and softmax with shift)

This algorithm computes 
𝑓
(
𝑥
)
=
log
⁡
∑
𝑖
=
1
𝑛
𝑒
𝑥
𝑖
 and the gradient 
𝑔
(
𝑥
)
=
∇
𝑓
(
𝑥
)
 for 
𝑥
∈
𝑅
𝑛
⁠.

1 
[
𝑎
,
𝑘
]
=
max
𝑖
𝑥
𝑖
 % 
𝑎
=
𝑥
𝑘
=
max
𝑖
𝑥
𝑖

2 
𝑠
=
0

3 for 
𝑖
=
1
:
𝑛

4 
𝑤
𝑖
=
exp
⁡
(
𝑥
𝑖
−
𝑎
)

5 if 
𝑖
≠
𝑘
⁠, 
𝑠
=
𝑠
+
𝑤
𝑖
⁠, end

6 end

7 
𝑓
=
𝑎
+
log
1
p
(
𝑠
)

8 for 
𝑖
−
1
:
𝑛

9 
𝑔
𝑖
=
𝑤
𝑖
/
(
1
+
𝑠
)

10 end

We first examine the error in evaluating the sum of non-negative terms




𝑠
=
∑
𝑖
=
1
𝑖
≠
𝑘
𝑛
𝑒
𝑥
𝑖
−
𝑎
=:
∑
𝑖
=
1
𝑖
≠
𝑘
𝑛
𝑤
𝑖
.
(4.4)
Evaluating 
𝑤
𝑖
=
𝑒
𝑥
𝑖
−
𝑎
 yields a computed result satisfying
𝑤
^
𝑖
=
𝑒
(
𝑥
𝑖
−
𝑎
)
(
1
+
𝛿
1
)
(
1
+
𝛿
2
)
,
|
𝛿
1
|
⩽
u
,
|
𝛿
2
|
⩽
u
.
Therefore
𝑤
^
𝑖
=
𝑒
𝑥
𝑖
−
𝑎
𝑒
(
𝑥
𝑖
−
𝑎
)
𝛿
1
(
1
+
𝛿
2
)
=
𝑒
𝑥
𝑖
−
𝑎
(
1
+
(
𝑥
𝑖
−
𝑎
)
𝛿
1
+
𝑂
(
𝛿
1
2
)
)
(
1
+
𝛿
2
)
and hence
|
𝑤
^
𝑖
−
𝑤
𝑖
|
⩽
(
(
1
+
𝑎
−
𝑥
𝑖
)
𝑢
+
𝑂
(
𝑢
2
)
)
𝑤
𝑖
.
Assuming for notational simplicity that 
𝑘
=
𝑛
 we can write the (exact) sum of computed quantities as


𝑠
~
=
∑
𝑖
=
1
𝑛
−
1
𝑤
^
𝑖
.
The rounding error analysis in Higham (1993) and Higham (2002, sec. 4.2) shows that the computed sum 
𝑠
^
 satisfies


|
𝑠
~
−
𝑠
^
|
⩽
𝑢
∑
𝑖
=
1
𝑛
−
2
|
𝑡
𝑖
|
+
𝑂
(
𝑢
2
)
,
where 
𝑡
𝑖
=
∑
𝑗
=
1
𝑖
+
1
𝑤
^
𝑗
⁠, so that, since 
𝑤
^
𝑖
≥
0
⁠,


|
𝑠
~
−
𝑠
^
|
⩽
𝑢
∑
𝑖
=
1
𝑛
−
1
(
𝑛
−
𝑖
)
𝑤
^
𝑖
+
𝑂
(
𝑢
2
)
.
Hence
	



	





	


|
𝑠
−
𝑠
^
|
	
⩽
∑
𝑖
=
1
𝑛
−
1
|
𝑤
^
𝑖
−
𝑤
𝑖
|
+
|
𝑠
^
−
𝑠
~
|

	
⩽
𝑢
∑
𝑖
=
1
𝑛
−
1
(
1
+
𝑎
−
𝑥
𝑖
)
𝑤
𝑖
+
𝑢
∑
𝑖
=
1
𝑛
−
1
(
𝑛
−
𝑖
)
𝑤
^
𝑖
+
𝑂
(
𝑢
2
)

	
=
𝑢
∑
𝑖
=
1
𝑛
−
1
(
1
+
𝑎
−
𝑥
𝑖
+
𝑛
−
𝑖
)
𝑤
𝑖
+
𝑂
(
𝑢
2
)
,
(4.5)
since 
𝑤
^
𝑖
=
𝑤
𝑖
+
𝑂
(
𝑢
)
⁠. Hence
|
𝑠
^
−
𝑠
𝑠
|
⩽
(
𝑛
+
𝑥
max
−
𝑥
min
)
𝑢
+
𝑂
(
𝑢
2
)
,
(4.6)
which guarantees an accurate computed sum as long as 
𝑛
+
𝑥
max
−
𝑥
min
 is not too large.
The final stage of the computation is to evaluate 
𝑦
=
𝑥
max
+
log
⁡
(
1
+
𝑠
)
 using the computed 
𝑠
^
⁠, for which we have
𝑦
^
=
(
𝑥
max
+
log
⁡
(
1
+
𝑠
^
)
(
1
+
𝛿
3
)
)
(
1
+
𝛿
4
)
,
|
𝛿
3
|
,
|
𝛿
4
|
⩽
𝑢
.
Here we are assuming that the 
log
1
p
 function has the property
f
l
(
log
1
p
(
𝑠
)
)
=
log
1
p
(
𝑠
)
(
1
+
𝛿
)
,
|
𝛿
|
⩽
𝑢
.
Ignoring the innocuous 
𝛿
4
 term and writing, by (4.6),
𝑠
^
=
𝑠
(
1
+
𝜂
)
,
|
𝜂
|
⩽
(
𝑛
+
𝑥
max
−
𝑥
min
)
𝑢
+
𝑂
(
𝑢
2
)
,
(4.7)
we have
	
	
	
𝑦
^
	
=
𝑥
max
+
log
⁡
(
1
+
𝑠
(
1
+
𝜂
)
(
1
+
𝛿
3
)

	
=
𝑥
max
+
log
⁡
(
1
+
𝑠
+
𝑠
𝜂
)
(
1
+
𝛿
3
)

	
=
𝑥
max
+
(
log
⁡
(
1
+
𝑠
)
+
𝑠
𝜂
1
+
𝑠
+
𝑂
(
𝑢
2
)
)
(
1
+
𝛿
3
)
,
using a Taylor series expansion about 
1
+
𝑠
 of the logarithm. Hence
𝑦
^
−
𝑦
=
log
⁡
(
1
+
𝑠
)
𝛿
3
+
𝑠
𝜂
1
+
𝑠
(
1
+
𝛿
3
)
+
𝑂
(
𝑢
2
)
.
Bounding 
𝜂
 using (4.7) gives
|
𝑦
−
𝑦
^
|
⩽
log
⁡
(
1
+
𝑠
)
𝑢
+
𝑠
1
+
𝑠
(
𝑛
+
𝑥
max
−
𝑥
min
)
𝑢
+
𝑂
(
𝑢
2
)
(4.8)
or, as a relative error bound, since 
𝑠
≥
0
⁠,
|
𝑦
−
𝑦
^
𝑦
|
⩽
(
log
⁡
(
1
+
𝑠
)
+
𝑛
+
𝑥
max
−
𝑥
min
|
𝑦
|
)
𝑢
+
𝑂
(
𝑢
2
)
.
(4.9)
Simplifying the bound gives the next result.

 

THEOREM 4.2
(Shifted log-sum-exp algorithm).
The computed log-sum-exp 
𝑦
^
 from Algorithm 4.1 satisfies
|
𝑦
−
𝑦
^
𝑦
|
≤
|
𝑦
+
𝑛
−
𝑥
min
𝑦
|
𝑢
+
𝑂
(
𝑢
2
)
.
(4.10)

The main question is how this result compares with Theorem 3.2 for the unshifted algorithm. The only difference in the bounds is that 
|
𝑦
|
+
𝑛
+
1
 in (3.5) is replaced by 
|
𝑦
+
𝑛
−
𝑥
min
|
 here. Now 
|
𝑦
+
𝑛
−
𝑥
min
|
≫
|
𝑦
|
+
𝑛
 is possible only if 
𝑥
min
≪
0
 and 
𝑥
min
≪
𝑥
max
⁠, so let us assume that these two inequalities hold. The term 
|
𝑦
+
𝑛
−
𝑥
min
|
 comes from bounding the terms 
(
1
+
𝑎
−
𝑥
𝑖
+
𝑛
−
𝑖
)
𝑤
𝑖
 in (4.5), where 
𝑤
𝑖
 is defined in (4.4) and 
𝑥
𝑖
=
𝑥
min
⁠, and if 
𝑥
min
≪
0
 then 
𝑤
𝑖
=
𝑒
𝑥
𝑖
−
𝑎
=
𝑒
𝑥
min
−
𝑥
max
≪
1
⁠. Hence the potentially large constant is mitigated by the 
𝑤
𝑖
 term that it multiplies—something that is lost in the manipulations to achieve a readable bound. We conclude that shifting should have little effect on the accuracy.

We note that (4.10) is weaker than necessary when 
𝑠
≪
1
 (recall that 
𝑠
≥
0
⁠), which happens when 
𝑥
𝑖
≪
𝑥
max
 for all 
𝑖
≠
𝑘
⁠, since we bounded 
𝑠
/
(
1
+
𝑠
)
 by 
1
 in going from (4.8) to (4.9). If 
𝑠
≪
1
 then (4.8) becomes
|
𝑦
−
𝑦
^
|
≲
𝑠
(
1
+
𝑛
+
𝑥
max
−
𝑥
min
)
𝑢
+
𝑂
(
𝑢
2
)
.
Since 
𝑠
≪
1
 also implies 
𝑥
𝑖
≪
𝑥
max
 for 
𝑖
≠
𝑘
 and hence 
𝑦
≈
𝑥
max
 we then have
|
𝑦
−
𝑦
^
|
|
𝑦
|
≲
𝑠
|
1
+
𝑛
+
𝑦
−
𝑥
min
|
|
𝑦
|
𝑢
+
𝑂
(
𝑢
2
)
,
which is a factor 
𝑠
 smaller than (4.10).
Turning to the evaluation of the softmax function 
𝑔
 from the shifted formula (1.4) we have, using (4.6),
𝑔
^
𝑗
=
exp
⁡
(
(
𝑥
𝑗
−
𝑎
)
(
1
+
𝛿
1
)
)
(
1
+
𝛿
2
)
(
1
+
𝛿
3
)
1
+
𝑠
(
1
+
𝜂
)
,
where 
𝛿
2
 corresponds to the exponential evaluation and 
𝛿
3
 to the division, and
|
𝛿
𝑖
|
⩽
u
,
𝑖
=
1
:
3
,
|
𝜂
|
⩽
(
𝑛
+
𝑥
max
−
𝑥
min
)
𝑢
+
𝑂
(
𝑢
2
)
.
Therefore
	

	
𝑔
^
𝑗
	
=
𝑔
𝑗
exp
⁡
(
(
𝑥
𝑗
−
𝑎
)
𝛿
1
)
(
1
+
𝛿
2
)
(
1
+
𝛿
3
)
1
+
𝑠
𝜂
/
(
1
+
𝑠
)

	
=
𝑔
𝑗
(
1
+
𝜃
)
,
|
𝜃
|
⩽
(
𝑛
+
2
+
2
(
𝑥
max
−
𝑥
min
)
)
𝑢
+
𝑂
(
𝑢
2
)
.

Hence we have obtained the following result.

 

THEOREM 4.3
(Shifted softmax algorithm).
The computed 
𝑔
^
 from Algorithm 4.1 satisfies
‖
𝑔
−
𝑔
^
‖
∞
‖
𝑔
‖
∞
⩽
(
𝑛
+
2
+
2
(
𝑥
max
−
𝑥
min
)
)
𝑢
+
𝑂
(
𝑢
2
)
.
(4.11)

Again, this is broadly commensurate with Theorem 3.3 for the unshifted evaluation, bearing in mind the comments following Theorem 4.2.

Finally we consider (1.5) with the log-sum-exp computed by Algorithm 4.1. In floating-point arithmetic we have the same equation (3.8) as for the unshifted algorithm but now, using (4.10), with 
𝜃
 bounded by
|
𝜃
|
⩽
(
1
+
|
𝑥
𝑗
−
𝑦
|
+
|
𝑦
+
𝑛
−
𝑥
min
|
)
𝑢
+
𝑂
(
𝑢
2
)
.
We have obtained the following result.

 

THEOREM 4.4
(Alternative shifted softmax algorithm).
The computed 
𝑔
^
 from (1.5) with the log-sum-exp computed by Algorithm 4.1 satisfies


‖
𝑔
−
𝑔
^
‖
∞
‖
𝑔
‖
∞
⩽
(
1
+
max
𝑗
|
𝑥
𝑗
−
𝑦
|
+
|
𝑦
+
𝑛
−
𝑥
min
|
)
𝑢
+
𝑂
(
𝑢
2
)
.
(4.12)

This is broadly similar to Theorem 3.4 for the unshifted alternative softmax algorithm.

5. Computational experiments

We now perform some experiments in a realistic setting, using MATLAB R2020a. The codes and data used for the experiments are available online.7

Our aims are to examine the sharpness of the rounding error bounds and to give a pairwise comparison of the accuracy of the algorithms in floating-point arithmetic. Our data come from a deep learning application. To generate the data we first set up and trained an artificial neural network, using the MATLAB Deep Learning Toolbox (Deep Learning Toolbox). More precisely, we trained a network to classify handwritten digit data from the widely used MNIST data set (LeCun et al.). Here each data point is a grayscale 
28
×
28
 pixel image and there are 10 categories: 
0
⁠, 
1
⁠,…, 
9
⁠. We used a network whose architecture has the following general form:

Image Input 
28
×
28
×
1
 with normalization.

Convolution 8 
3
×
3
×
1
 stride [1 1] padding ‘same’.

Batch Normalization 8 channels.

ReLU.

Max Pool 
2
×
2
 stride [2 2] padding [0 0 0 0].

Convolution 16 
3
×
3
×
8
 stride [1 1] padding ‘same’.

Batch Normalization 16 channels.

ReLU.

Max Pool 
2
×
2
 stride [2 2] padding [0 0 0 0].

Convolution 32 
3
×
3
×
16
 stride [1 1] padding ‘same’.

Batch Normalization 32 channels.

ReLU.

Fully Connected 10 layer.

Softmax.

Classification Output crossentropy.

This is the default architecture from the Deep Learning Toolbox, where further details may be found.

The network was trained on 7500 images (750 from each of the ten categories), with 2500 further images (250 from each of the ten categories) used for validation.

The network takes as input a 
28
×
28
 matrix corresponding to the pixels in the image and returns a non-negative 
10
×
1
 vector whose 
𝑖
th component may be interpreted as the probability that the image came from category 
𝑖
⁠. If we categorize according to the highest probability from the output then the trained network misclassifed 27 of the 2500 validation images, corresponding to a 98.9% success rate.

The network uses single precision arithmetic, fp32. In our experiments we are concerned only with floating-point arithmetic issues, and we treat the trained network as a means to produce a realistic data set. To do this we extracted the 2500 single precision vectors from the validation set that were passed into the softmax layer and converted them to fp16 or bfloat16. We then used this data in our implementation of the softmax and log-sum-exp algorithms that we have studied in the previous sections.

To record errors in computed results we applied the basic algorithm, Algorithm 3.1, in single precision to provide a reference solution and used the chop function of Higham & Pranesh (2019) to simulate half-precision arithmetic, in both the fp16 format and the bfloat16 format.

We first describe experiments in fp16. The components in the 2500 test vectors 
𝑥
∈
𝑅
10
 vary between about 
−
19
 and 
+
20
⁠. As indicated in Table 2, 
𝑒
𝑥
 overflows in fp16 for 
𝑥
≳
11
⁠. Hence, in these tests, overflow is an issue for the basic log-sum-exp implementation in Algorithm 3.1: it generated an Inf for 475 of the 2500 test vectors. The shifted version of log-sum-exp in Algorithm 4.1 did not overflow. In the plots below we do not include results for the cases where Algorithm 3.1 produced overflow.

First we look at the log-sum-exp algorithms. In the upper-left plot of Fig. 1 we used the basic implementation of log-sum-exp, Algorithm 3.1. We scatter plot over the 2025 vectors where no overflow occurred. For each such vector the horizontal coordinate is the leading term in the error bound of Theorem 3.2, scaled by 
𝑢
⁠, that is, 
1
+
(
𝑛
+
1
)
/
|
𝑦
|
⁠. Here, as shown in Table 1, 
𝑢
=
4.88
×
10
−
4
 for fp16. The vertical coordinate is the actual scaled relative error 
|
𝑦
^
−
𝑦
|
/
(
𝑢
|
𝑦
|
)
⁠. The plot also gives a reference line of slope 
1
 from the origin. We see that the bound is always satisfied and is reasonably sharp in many cases.

FIG. 1.

Scatter plots of errors and error bounds, scaled by unit roundoff, over 
2025
 vectors in 
𝑅
10
 for log-sum-exp algorithms in fp16. See the text for a description of the axes. Upper left: basic implementation of log-sum-exp from Algorithm 3.1. According to the error analysis all points should lie below the reference line 
𝑦
=
𝑥
 (shown in red). Upper right: corresponding results for the shifted implementation of log-sum-exp in Algorithm 4.1. Lower: scaled error from Algorithm 3.1 versus scaled error from Algorithm 4.1.

Open in new tabDownload slide

In the upper-right plot of Fig. 1 we show corresponding results for the shifted log-sum-exp implementation in Algorithm 4.1, using the bound from Theorem 4.2.

In the lower part of Fig. 1 we scatter plot the floating-point errors for the basic and shifted algorithms. Here, for 1863 of the 2025 cases (92%), the two errors were identical to all digits in the half-precision computation. In more detail, over all the data points the ratio of the error in the basic log-sum-exp (horizontal axis) divided by the error in the shifted version (vertical axis) varied between 0.19 and 59, with a mean of 1.07 and a standard error of 0.03. This indicates that the two versions perform similarly, with the shift producing slightly better results.

We now move on to the four softmax implementations. In Fig. 2 we use the shifted softmax implementation from Algorithm 4.1, analysed in Theorem 4.3, as the basis for comparison. The upper left plot has the scaled error 
‖
𝑔
^
−
𝑔
‖
∞
/
(
𝑢
‖
𝑔
‖
∞
)
 from Algorithm 4.1 on the horizontal axis and the scaled error from the basic softmax in Algorithm 3.1 on the vertical axis. The upper-right plot compares the shifted softmax against the alternative algorithm using (3.7) and the unshifted log-sum-exp analyzed in Theorem 3.4. Similarly, the lower plot compares the alternative shifted softmax algorithm that uses (3.9) with the shifted log-sum-exp, which is analyzed in Theorem 4.4. We see that the softmax values obtained from Algorithm 4.1 are generally slightly more accurate than those from Algorithm 3.1, whereas the alternative softmax versions based on the rewrite in (1.5) are mostly less accurate than those from Algorithm 4.1.

FIG. 2.

Scatter plots of errors, scaled by unit roundoff, for softmax algorithms in fp16. See the text for a description of the axes. Reference line is 
𝑦
=
𝑥
⁠.

Open in new tabDownload slide

Overall, the results in Figs 1 and 2 are consistent with our floating-point error analysis.

A further test is to compute the sum of each softmax vector, which should equal 
1
⁠. In Fig. 3 we compare the softmax sums for the basic algorithm (Algorithm 3.1, red circles) analyzed in Theorem 3.3 and the alternative version (blue crosses) analyzed in Theorem 3.4. Similarly, Fig. 4 compares the shifted softmax algorithm analyzed in Theorem 4.3 and its alternative analyzed in Theorem 4.4. The order along the 
𝑥
-axis is arbitrary; it corresponds to the order in which the data vectors were generated. These figures provide further evidence that the alternative softmax algorithms are less accurate than the basic or shifted algorithms.

FIG. 3.

Sum of entries of computed softmax vector for Algorithm 3.1 (red circles), analyzed in Theorem 3.3, and the alternative (blue crosses) analyzed in Theorem 3.4.

Open in new tabDownload slide
FIG. 4.

Sum of entries of computed softmax vector for Algorithm 4.1 (red circles), analyzed in Theorem 4.3, and the alternative (blue crosses) analyzed in Theorem 4.4.

Open in new tabDownload slide

We also conducted the corresponding experiments in simulated bfloat16 arithmetic. Here, as indicated in Tables 1 and 2, the number range is increased at the expense of reduced precision. In this case there was no overflow in any of the algorithms. The results were very similar to those for fp16, so they are not shown here.

6. Conclusions

The log-sum-exp and softmax functions both feature in many computational pipelines, so it is important to compute them accurately and to avoid generating infs or NaNs because of overflow or underflow. To this end a shift is usually incorporated into the defining formulas, yielding (1.3) and (1.4). It is important to understand the effect of the shift on the accuracy of the computed result, especially when computations are carried out in a low-precision arithmetic such as bfloat16 or fp16, which have the equivalent of only three or four decimal digits of precision.

Our rounding error analysis shows that shifting by the largest element of the input vector does not lessen the accuracy of the computed log-sum-exp and softmax, so the shifted formulas can be safely used. Underlying this pleasing fact is the phenomenon that any large error constants caused by shifting are cancelled by multiplication with small exponentials.

We obtained an explicit formula for the condition number of log-sum-exp and bounds for the condition number of softmax, and we were able to identify situations in which the log-sum-exp algorithms are guaranteed to be forward stable.

For the alternative and widely used softmax formula that avoids division, (1.5), we obtained larger error bounds than for the shifted formula (1.4). Since our numerical experiments confirm that larger errors are typically obtained in practice we recommend using (1.4) instead of (1.5) to evaluate softmax.

In summary, Algorithm 4.1 is our recommendation for computing log-sum-exp and softmax. It avoids overflow, reduces the chance of harmful underflow and generally produces results as accurate as those from the unshifted formulas.

Acknowledgements

We thank the referees for their helpful comments. The opinions and views expressed in this publication are those of the authors and not necessarily those of the funding bodies.

Funding

Engineering and Physical Sciences Research Council (EP/P020720/1); The MathWorks; Royal Society.

Footnotes
1	

log
⁡
0
=
−
∞
 is the value recommended by the IEEE standard (IEEE Computer Society, 2019, sec. 9.2.1).

2	

https://devblogs.nvidia.com/cuda-pro-tip-flush-denormals-confidence/, https://en.wikipedia.org/wiki/Denormal_number.

3	

https://en.wikipedia.org/wiki/LogSumExp.

4	

For example, http://bayesjumping.net/log-sum-exp-trick/, and https://jblevins.org/log/log-sum-exp. And similarly for the softmax: https://timvieira.github.io/blog/post/2014/02/11/exp-normalize-trick/.

5	

https://youtu.be/-RVM21Voo7Q.

6	

We note that more refined error bounds for summation are available under additional assumptions on the floating-point arithmetic (Rump, 2012; Lange & Rump, 2019).

7	

https://github.com/higham/logsumexp-softmax-tests.

References

Aprahamian, M. & Higham, N. J. (2014) The matrix unwinding function, with an application to computing the matrix exponential. SIAM J. Matrix Anal. Appl., 35, 88–109.

Google Scholar

Crossref

WorldCat

 

Bishop, C. M. (2006) Pattern Recognition and Machine Learning. New York: Springer.

Google Scholar

Google Preview

WorldCat

COPAC 

Blanchard, P., Higham, N. J. & Mary, T. (2020) A class of fast and accurate summation algorithms. SIAM J. Sci. Comput., 42, A1541–A1557.

Google Scholar

Crossref

WorldCat

 

Boyd, S. & Vandenberghe, L. (2004) Convex Optimization. Cambridge, UK: Cambridge University Press.

Google Scholar

Crossref

Google Preview

WorldCat

COPAC 

Calafiore, G. C., Gaubert, S. & Possieri, C. (2020) Log-sum-exp neural networks and posynomial models for convex and log-log-convex data. IEEE Trans. Neural Networks and Learning Systems, 31, 1–12 .

Google Scholar

WorldCat

 

Czaja, J., Gallus, M., Patejko, T. & Tang, J. (2019) Softmax optimizations for Intel Xeon processor-based platforms. arXiv: 1904.12380.

De Dinechin, F., Lauter, C. & Muller, J.-M. (2007) Fast and correctly rounded logarithms in double-precision. RAIRO-Inf. Theor. Appl., 41, 85–102.

Google Scholar

Crossref

WorldCat

 

Deep Learning Toolbox. Natick, MA: The MathWorks, Inc. Available at http://www.mathworks.co.uk/products/deep-learning/.

Efron, B. & Hastie, T. (2016) Computer Age Statistical Inference. Algorithms, Evidence, and Data Science. Cambridge, UK: Cambridge University Press.

Google Scholar

Crossref

Google Preview

WorldCat

COPAC 

Goodfellow, I., Bengio, Y. & Courville, A. (2016) Deep Learning. Cambridge, MA: MIT Press.

Google Scholar

Google Preview

WorldCat

COPAC 

Guo, C., Hannun, A., Knott, B., van der Maaten, L., Tygert, M. & Zhu, R. (2020) Secure multiparty computations in floating-point arithmetic. arXiv: 2001.03192.

Hewlett-Packard (1982) HP-15C Advanced Functions Handbook. Portable Computer Division. Corvallis, OR: Hewlett-Packard. Part number 00015-90011 Rev. C.

Google Scholar

Google Preview

WorldCat

COPAC 

Higham, C. F. & Higham, D. J. (2019) Deep learning: an introduction for applied mathematicians. SIAM Rev., 61, 860–891.

Google Scholar

Crossref

WorldCat

 

Higham, N. J. (1993) The accuracy of floating point summation. SIAM J. Sci. Comput., 14, 783–799.

Google Scholar

Crossref

WorldCat

 

Higham, N. J. (2002) Accuracy and Stability of Numerical Algorithms, 2nd edn. Philadelphia, PA: Society for Industrial and Applied Mathematics.

Google Scholar

Crossref

Google Preview

WorldCat

COPAC 

Higham, N. J. (2008) Functions of Matrices: Theory and Computation. Philadelphia, PA: Society for Industrial and Applied Mathematics.

Google Scholar

Crossref

Google Preview

WorldCat

COPAC 

Higham, N. J. & Mary, T. (2019) A new approach to probabilistic rounding error analysis. SIAM J. Sci. Comput., 41, A2815–A2835.

Google Scholar

Crossref

WorldCat

 

Higham, N. J., & Mary, T. (2020) Sharper Probabilistic Backward Error Analysis for Basic Linear Algebra Kernels with Random Data. MIMS EPrint 2020.4. UK: Manchester Institute for Mathematical Sciences, The University of Manchester.

Google Scholar

Google Preview

WorldCat

COPAC 

Higham, N. J. & Pranesh, S. (2019) Simulating low precision floating-point arithmetic. SIAM J. Sci. Comput., 41, C585–C602.

Google Scholar

Crossref

WorldCat

 

IEEE (2019) IEEE Standard for Floating-Point Arithmetic, IEEE Std 754-2019 (Revision of IEEE 754-2008). New York: Institute of Electrical and Electronics Engineers.

Google Scholar

Google Preview

WorldCat

COPAC 

Intel Corporation (2018) BFLOAT16—Hardware Numerics Definition. White paper. Document number 338302-001US.

Jones, E., Oliphant, T., Peterson, P., et al. (2001) SciPy: Open Source Scientific Tools for Python. Available at http://www.scipy.org/.

 

Lange, M. & Rump, S. M. (2019) Sharp estimates for perturbation errors in summations. Math. Comp., 88, 349–368.

Google Scholar

Crossref

WorldCat

 

LeCun, Y., Cortes, C. & Burges, C. J. C. The MNIST Database of Handwritten Digits. Available at http://yann.lecun.com/exdb/mnist/.

 

Matlab Code for Machine Learning Algorithms in Book PRML. Available at https://github.com/PRML/PRMLT.

Muller, J.-M. (2016) Elementary Functions: Algorithms and Implementation, 3rd edn. Boston, MA: Birkhäuser.

Google Scholar

Crossref

Google Preview

WorldCat

COPAC 

Muller, J.-M., Brunie, N., de Dinechin, F., Jeannerod, C.-P., Joldes, M., Lefèvre, V., Melquiond, G., Revol, N. & Torres, S. (2018) Handbook of Floating-Point Arithmetic, 2nd edn. Boston, MA: Birkhäuser.

Google Scholar

Crossref

Google Preview

WorldCat

COPAC 

Murphy, K. P. (2012) Machine Learning: A Probabilistic Approach. Cambridge, UK: Cambridge University Press.

Google Scholar

Google Preview

WorldCat

COPAC 

Rump, S. M. (2012) Error estimation of floating-point summation and dot product. BIT, 52, 201–220.

Google Scholar

Crossref

WorldCat

 

Statistics and Machine Learning Toolbox Natick, MA: MathWorks, Inc. Available at https://uk.mathworks.com/products/statistics.html.

R Core Team R: A Language and Environment for Statistical Computing. Vienna, Austria: R Foundation for Statistical Computing.

Google Scholar

Google Preview

WorldCat

COPAC 

Wang, M., Lu, S., Zhu, D., Lin, J., & Wang, Z. (2018) A high-speed and low-complexity architecture for softmax function in deep learning. 2018 IEEE Asia Pacific Conference on Circuits and Systems (APCCAS). Chengdu, China: IEEE. 223–226.

Williams, C. K. I. & Barber, D. (1998) Bayesian classification with Gaussian processes. IEEE Trans. Pattern Analysis and Machine Intelligence, 20, 1342–1351.

Google Scholar

Crossref

WorldCat

 
© The Author(s) 2020. Published by Oxford University Press on behalf of the Institute of Mathematics and its Applications. All rights reserved.
This is an Open Access article distributed under the terms of the Creative Commons Attribution License (http://creativecommons.org/licenses/by/4.0/), which permits unrestricted reuse, distribution, and reproduction in any medium, provided the original work is properly cited.