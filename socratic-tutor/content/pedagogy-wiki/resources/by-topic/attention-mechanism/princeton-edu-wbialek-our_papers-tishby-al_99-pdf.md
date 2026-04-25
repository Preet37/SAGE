# Source: https://www.princeton.edu/~wbialek/our_papers/tishby+al_99.pdf
# Title: The Information Bottleneck Method (Tishby, Pereira, Bialek, 1999)
# Fetched via: jina
# Date: 2026-04-11

Title: arXiv:physics/0004057 v1   24 Apr 2000



Number of Pages: 16

> arXiv:physics/0004057 v1  24 Apr 2000

# The information bottleneck method 

# Naftali Tishby, 1,2 Fernando C. Pereira, 3 and William Bialek 1

> 1

NEC Research Institute, 4 Independence Way Princeton, New Jersey 08540 

> 2

Institute for Computer Science, and Center for Neural Computation Hebrew University Jerusalem 91904, Israel 

> 3

AT&T Shannon Laboratory 180 Park Avenue Florham Park, New Jersey 07932 30 September 1999 

We define the relevant information in a signal x ∈ X as being the in-formation that this signal provides about another signal y ∈ Y . Examples include the information that face images provide about the names of the peo-ple portrayed, or the information that speech sounds provide about the words spoken. Understanding the signal x requires more than just predicting y, it also requires specifying which features of X play a role in the prediction. We formalize this problem as that of finding a short code for X that preserves the maximum information about Y . That is, we squeeze the information that X

provides about Y through a ‘bottleneck’ formed by a limited set of codewords ˜X. This constrained optimization problem can be seen as a generalization of rate distortion theory in which the distortion measure d(x, ˜x) emerges from the joint statistics of X and Y . This approach yields an exact set of self consistent equations for the coding rules X → ˜X and ˜X → Y . Solutions to these equations can be found by a convergent re–estimation method that generalizes the Blahut–Arimoto algorithm. Our variational principle pro-vides a surprisingly rich framework for discussing a variety of problems in signal processing and learning, as will be described in detail elsewhere. 11 Introduction 

A fundamental problem in formalizing our intuitive ideas about information is to provide a quantitative notion of “meaningful” or “relevant” information. These issues were intentionally left out of information theory in its original formulation by Shannon, who focused attention on the problem of transmit-ting information rather than judging its value to the recipient. Correspond-ingly, information theory has often been viewed as being strictly a theory of communication, and this view has become so accepted that many people consider statistical and information theoretic principles as almost irrelevant for the question of meaning. In contrast, we argue here that information the-ory, in particular lossy source compression, provides a natural quantitative approach to the question of “relevant information.” Specifically, we formu-late a variational principle for the extraction or efficient representation of relevant information. In related work [1] we argue that this single informa-tion theoretic principle contains as special cases a wide variety of problems, including prediction, filtering, and learning in its various forms. The problem of extracting a relevant summary of data, a compressed description that captures only the relevant or meaningful information, is not well posed without a suitable definition of relevance. A typical example is that of speech compression. One can consider lossless compression, but in any compression beyond the entropy of speech some components of the signal cannot be reconstructed. On the other hand, a transcript of the spoken words has much lower entropy (by orders of magnitude) than the acoustic waveform, which means that it is possible to compress (much) further without losing any information about the words and their meaning. The standard analysis of lossy source compression is “rate distortion the-ory,” which characterizes the tradeoff between the rate, or signal represen-tation size, and the average distortion of the reconstructed signal. Rate distortion theory determines the level of inevitable expected distortion, D,given the desired information rate, R, in terms of the rate distortion function 

R(D). The main problem with rate distortion theory is in the need to specify the distortion function first, which in turn determines the relevant features of the signal. Those features, however, are often not explicitly known and 2an arbitrary choice of the distortion function is in fact an arbitrary feature selection. In the speech example, we have at best very partial knowledge of what precise components of the signal are perceived by our (neural) speech recog-nition system. Those relevant components depend not only on the complex structure of the auditory nervous system, but also on the sounds and utter-ances to which we are exposed during our early life. It therefore is virtually impossible to come up with the “correct” distortion function for acoustic signals. The same type of difficulty exists in many similar problems, such as natural language processing, bioinformatics (for example, what features of protein sequences determine their structure) or neural coding (what informa-tion is encoded by spike trains and how). This is the fundamental problem of feature selection in pattern recognition. Rate distortion theory does not provide a full answer to this problem since the choice of the distortion func-tion, which determines the relevant features, is not part of the theory. It is, however, a step in the right direction. A possible solution comes from the fact that in many interesting cases we have access to an additional variable that determines what is relevant. In the speech case it might be the transcription of the signal, if we are interested in the speech recognition problem, or it might be the speaker’s identity if speaker identification is our goal. For natural language processing, it might be the part of speech labels for words in grammar checking, but the dictionary senses of ambiguous words in information retrieval. Similarly, for the protein folding problem we have a joint database of sequences and three dimensional structures, and for neural coding a simultaneous recording of sensory stimuli and neural responses defines implicitly the relevant variables in each domain. All of these problems have the same formal underlying structure: extract the information from one variable that is relevant for the prediction of another one. The choice of additional variable determines the relevant components or features of the signal in each case. In this short paper we formalize this intuitive idea using an informa-tion theoretic approach which extends elements of rate distortion theory. We derive self consistent equations and an iterative algorithm for finding representations of the signal that capture its relevant structure, and prove 3convergence of this algorithm. 

# 2 Relevant quantization 

Let X denote the signal (message) space with a fixed probability measure 

p(x), and let ˜X denote its quantized codebook or compressed representation. For ease of exposition we assume here that both of these sets are finite, that is, a continuous space should first be quantized. For each value x ∈ X we seek a possibly stochastic mapping to a repre-sentative, or codeword in a codebook, ˜ x ∈ ˜X, characterized by a conditional p.d.f. p(˜ x|x). The mapping p(˜ x|x) induces a soft partitioning of X in which each block is associated with one of the codebook elements ˜ x ∈ ˜X, with probability given by 

p(˜ x) = ∑

> x

p(x)p(˜ x|x) . (1) The average volume of the elements of X that are mapped to the same codeword is 2 H(X| ˜X), where 

H(X| ˜X) = − ∑

> x∈X

p(x) ∑ 

> ˜x∈˜X

p(˜ x|x) log p(˜ x|x) (2) is the conditional entropy of X given ˜X.What determines the quality of a quantization? The first factor is of course the rate, or the average number of bits per message needed to specify an element in the codebook without confusion. This number per element of 

X is bounded from below by the mutual information 

I(X; ˜ X) = ∑ 

> x∈X
> ∑
> ˜x∈˜X

p(x, ˜x) log  

> [

p(˜ x|x)

p(˜ x)

> ]

, (3) since the average cardinality of the partitioning of X is given by the ratio of the volume of X to that of the mean partition, 2 H(X)/2H(X| ˜X) = 2 I(X; ˜X), via the standard asymptotic arguments. Notice that this quantity is different from the entropy of the codebook, H( ˜X), and this entropy normally is not what we want to minimize. 4However, information rate alone is not enough to characterize good quan-tization since the rate can always be reduced by throwing away details of the original signal x. We need therefore some additional constraints. 

# 2.1 Relevance through distortion: Rate distortion theory 

In rate distortion theory such a constraint is provided through a distortion function, d : X × ˜X → R +, which is presumed to be small for good represen-tations. Thus the distortion function specifies implicitly what are the most relevant aspects of values in X.The partitioning of X induced by the mapping p(˜ x|x) has an expected distortion 

〈d(x, ˜x)〉p(x, ˜x) = ∑ 

> x∈X
> ∑
> ˜x∈˜X

p(x, ˜x)d(x, ˜x) . (4) There is a monotonic tradeoff between the rate of the quantization and the expected distortion: the larger the rate, the smaller is the achievable distor-tion. The celebrated rate distortion theorem of Shannon and Kolmogorov (see, for example Ref. [2]) characterizes this tradeoff through the rate distortion function, R(D), defined as the minimal achievable rate under a given con-straint on the expected distortion: 

R(D) ≡ min  

> {p(˜ x|x): 〈d(x, ˜x)〉≤ D}

I(X; ˜X) . (5) Finding the rate distortion function is a variational problem that can be solved by introducing a Lagrange multiplier, β, for the constrained expected distortion. One then needs to minimize the functional 

F[p(˜ x|x)] = I(X; ˜ X) + β〈d(x, ˜x)〉p(x, ˜x) (6) over all normalized distributions p(˜ x|x). This variational formulation has the following well known consequences: 5Theorem 1 The solution of the variational problem, 

δF

δp (˜ x|x) = 0 , (7) 

for normalized distributions p(˜ x|x), is given by the exponential form 

p(˜ x|x) = p(˜ x)

Z(x, β ) exp [ −βd (x, ˜x)] , (8) 

where Z(x, β ) is a normalization (partition) function. Moreover, the La-grange multiplier β, determined by the value of the expected distortion, D, is positive and satisfies 

δR 

δD = −β . (9) 

Proof. Taking the derivative w.r.t. p(˜ x|x), for given x and ˜ x, one obtains 

δF

δp (˜ x|x) = p(x)

> [

log p(˜ x|x)

p(˜ x) + 1 

− 1

p(˜ x)

> ∑
> x′

p(x′)p(˜ x|x′) + βd (x, ˜x) + λ(x)

p(x)

> ]

, (10) since the marginal distribution satisfies p(˜ x) = ∑ 

> x′

p(x′)p(˜ x|x′). λ(x) are the normalization Lagrange multipliers for each x. Setting the derivatives to zero and writing log Z(x, β ) = λ(x)/p (x), we obtain Eq. (8). When varying the normalized p(˜ x|x), the variations δI (X; ˜ X) and δ〈d(x, ˜x)〉p(x, ˜x) are linked through 

δF = δI (X; ˜ X) + βδ 〈d(x, ˜x)〉p(x, ˜x) = 0 , (11) from which Eq. (9) follows. The positivity of β is then a consequence of the concavity of the rate distortion function (see, for example, Chapter 13 of Ref. [2]). 

62.2 The Blahut–Arimoto algorithm 

An important practical consequence of the above variational formulation is that it provides a converging iterative algorithm for self consistent determi-nation of the distributions p(˜ x|x) and p(˜ x). Equations (8) and (1) must be satisfied simultaneously for consistent probability assignment. A natural approach to solve these equations is to alternately iterate between them until reaching convergence. The following lemma, due to Csisz´ ar and Tusn´ ady [3], assures global convergence in this case. 

Lemma 2 Let p(x, y ) = p(x)p(y|x) be a given joint distribution. Then the distribution q(y) that minimizes the relative entropy or Kullback–Leibler di-vergence, DKL [p(x, y )|p(x)q(y)] , is the marginal distribution 

p(y) = ∑

> x

p(x)p(y|x).

Namely, 

I(X; Y ) = DKL [p(x, y )|p(x)p(y)] = min  

> q(y)

DKL [p(x, y )|p(x)q(y)] .

Equivalently, the distribution q(y) which minimizes the expected relative en-tropy, ∑

> x

p(x)DKL [p(y|x)|q(y)] ,

is also the marginal distribution p(y) = ∑ 

> x

p(x)p(y|x).

The proof follows directly from the non–negativity of the relative entropy. This lemma guarantees the marginal condition Eq. (1) through the same variational principle that leads to Eq. (8): 

Theorem 3 Equations (1) and (8) are satisfied simultaneously at the mini-mum of the functional, 

F = −〈 log Z(x, β )〉p(x) = I(X; ˜X) + β〈d(x, ˜x)〉p(x, ˜x) , (12) 

where the minimization is done independently over the convex sets of the normalized distributions, {p(˜ x)} and {p(˜ x|x)},

min  

> p(˜ x)

min  

> p(˜ x|x)

F [p(˜ x); p(˜ x|x)] .

7These independent conditions correspond precisely to alternating iterations of Eq. (1) and Eq. (8). Denoting by t the iteration step,  

> {

pt+1 (˜ x) = ∑ 

> x

p(x)pt(˜ x|x)

pt(˜ x|x) = pt(˜ x) 

> Zt(x,β )

exp( −βd (x, ˜x)) (13) 

where the normalization function Zt(x, β ) is evaluated for every t in Eq. (13). Furthermore, these iterations converge to a unique minimum of F in the convex sets of the two distributions. 

For the proof, see references [2, 4]. This alternating iteration is the well known Blauht-Arimoto (BA) algorithm for calculation of the rate distortion function. It is important to notice that the BA algorithm deals only with the op-timal partitioning of the set X given the set of representatives ˜X, and not with an optimal choice of the representation ˜X. In practice, for finite data, it is also important to find the optimal representatives which minimize the expected distortion, given the partitioning. This joint optimization is similar to the EM procedure in statistical estimation and does not in general have a unique solution. 

# 3 Relevance through another variable: The Information Bottleneck 

Since the “right” distortion measure is rarely available, the problem of rel-evant quantization has to be addressed directly, by preserving the relevant information about another variable. The relevance variable, denoted here by 

Y , must not be independent from the original signal X, namely they have positive mutual information I(X; Y ). It is assumed here that we have access to the joint distribution p(x, y ), which is part of the setup of the problem, similarly to p(x) in the rate distortion case. 1

> 1The problem of actually obtaining a good enough sample of this distribution is an interesting issue in learning theory, but is beyond the scope of this paper. For a start on this problem see Ref. [1].

83.1 A new variational principle 

As before, we would like our relevant quantization ˜X to compress X as much as possible. In contrast to the rate distortion problem, however, we now want this quantization to capture as much of the information about Y as possible. The amount of information about Y in ˜X is given by 

I( ˜ X; Y ) = ∑

> y
> ∑
> ˜x

p(y, ˜x) log p(y, ˜x)

p(y)p(˜ x) ≤ I(X; Y ). (14) Obviously lossy compression cannot convey more information than the orig-inal data. As with rate and distortion, there is a tradeoff between compress-ing the representation and preserving meaningful information, and there is no single right solution for the tradeoff. The assignment we are looking for is the one that keeps a fixed amount of meaningful information about the rel-evant signal Y while minimizing the number of bits from the original signal 

X (maximizing the compression). 2 In effect we pass the information that X

provides about Y through a “bottleneck” formed by the compact summaries in ˜X.We can find the optimal assignment by minimizing the functional 

L[p(˜ x|x)] = I( ˜ X; X) − βI ( ˜ X; Y ), (15) where β is the Lagrange multiplier attached to the constrained meaningful information, while maintaining the normalization of the mapping p(˜ x|x) for every x. At β = 0 our quantization is the most sketchy possible—everything is assigned to a single point—while as β → ∞ we are pushed toward arbitrar-ily detailed quantization. By varying the (only) parameter β one can explore the tradeoff between the preserved meaningful information and compression at various resolutions. As we show elsewhere [1, 5], for interesting special cases (where there exist sufficient statistics) it is possible to preserve almost all the meaningful information at finite β with a significant compression of the original data. 

> 2It is completely equivalent to maximize the meaningful information for a fixed com-pression of the original variable.

93.2 Self-consistent equations 

Unlike the case of rate distortion theory, here the constraint on the meaning-ful information is nonlinear in the desired mapping p(˜ x|x) and this is a much harder variational problem. Perhaps surprisingly, this general problem of extracting the meaningful information—minimizing the functional L[p(˜ x|x)] in Eq. (15)—can be given an exact formal solution. 

Theorem 4 The optimal assignment, that minimizes Eq. (15), satisfies the equation 

p(˜ x|x) = p(˜ x)

Z(x, β ) exp 

> [

−β ∑

> y

p(y|x) log p(y|x)

p(y|˜x)

> ]

, (16) 

where the distribution p(y|˜x) in the exponent is given via Bayes’ rule and the Markov chain condition ˜X ← X ← Y , as, 

p(y|˜x) = 1

p(˜ x)

> ∑
> x

p(y|x)p(˜ x|x)p(x). (17) This solution has a number of interesting features, but we must emphasize that it is a formal solution since p(y|˜x) in the exponential is defined implicitly in terms of the assignment mapping p(˜ x|x). Just as before, the marginal distribution p(˜ x) must satisfy the marginal condition Eq. (1) for consistency. 

Proof. First we note that the conditional distribution of y on ˜ xp(y|˜x) = ∑

> x∈X

p(y|x)p(x|˜x) , (18) follows from the Markov chain condition Y ← X ← ˜X.3 The only varia-tional variables in this scheme are the conditional distributions, p(˜ x|x), since other unknown distributions are determined from it through Bayes’ rule and consistency. Thus we have 

p(˜ x) = ∑

> x

p(˜ x|x)p(x) , (19)        

> 3It is important to notice that this not a modeling assumption and the quantization ˜ X
> is not used as a hidden variable in a model of the data. In the latter, the Markov condition would have been different: Y←˜X←X.

10 and 

p(˜ x|y) = ∑

> x

p(˜ x|x)p(x|y) . (20) The above equations imply the following derivatives w.r.t. p(˜ x|x), 

δp (˜ x)

δp (˜ x|x) = p(x) (21) and 

δp (˜ x|y)

δp (˜ x|x) = p(x|y) . (22) Introducing Lagrange multipliers, β for the information constraint and λ(x)for the normalization of the conditional distributions p(˜ x|x) at each x, the Lagrangian, Eq. (15), becomes 

L = I(X, ˜X) − βI ( ˜X, Y ) − ∑

> x, ˜x

λ(x)p(˜ x|x) (23) = ∑

> x, ˜x

p(˜ x|x)p(x) log  

> [

p(˜ x|x)

p(˜ x)

> ]

− β ∑

> ˜x,y

p(˜ x, y ) log  

> [

p(˜ x|y)

p(˜ x)

> ]

− ∑

> x, ˜x

λ(x)p(˜ x|x) . (24) Taking derivatives with respect to p(˜ x|x) for given x and ˜ x, one obtains 

δL

δp (˜ x|x) = p(x) [1 + log p(˜ x|x)] − δp (˜ x)

δp (˜ x|x) [1 + log p(˜ x)] 

−β ∑

> y

δp (˜ x|y)

δp (˜ x|x) p(y) [1 + log p(˜ x|y)] 

−β δp (˜ x)

δp (˜ x|x) [1 + log p(˜ x)] − λ(x) . (25) Substituting the derivatives from Eq’s. (21) and (22) and rearranging, 

δL

δp (˜ x|x) = p(x)

> {

log  

> [

p(˜ x|x)

p(˜ x)

> ]

− β ∑

> y

p(y|x) log  

> [

p(y|˜x)

p(y)

> ]

− λ(x)

p(x)

> }

.(26) 11 Notice that ∑ 

> y

p(y|x) log p(y|x) 

> p(y)

= I(x, Y ) is a function of x only (independent of ˜ x) and thus can be absorbed into the multiplier λ(x). Introducing ˜λ(x) = λ(x)

p(x) − β ∑

> y

p(y|x) log  

> [

p(y|x)

p(y)

> ]

,

we finally obtain the variational condition: 

δL

δp (˜ x|x) = p(x)

> [

log p(˜ x|x)

p(˜ x) + β ∑

> y

p(y|x) log p(y|x)

p(y|˜x) − ˜λ(x)

> ]

= 0 , (27) which is equivalent to equation (16) for p(˜ x|x), 

p(˜ x|x) = p(˜ x)

Z(x, β ) exp ( −βD KL [p(y|x)|p(y|˜x)]) , (28) with 

Z(x, β ) = exp[ β ˜λ(x)] = ∑

> ˜x

p(˜ x) exp ( −βD KL [p(y|x)|p(y|˜x)]) ,

the normalization (partition) function. 

Comments: 

1. The Kullback–Leibler divergence, DKL [p(y|x)|p(y|˜x)], emerged as the relevant “effective distortion measure” from our variational principle but is not assumed otherwise anywhere! It is therefore natural to con-sider it as the “correct” distortion d(x, ˜x) = DKL [p(y|x)|p(y|˜x)] for quantization in the information bottleneck setting. 2. Equation (28), together with equations (18) and (19), determine self consistently the desired conditional distributions p(˜ x|x) and p(˜ x). The crucial quantization is here performed through the conditional distri-butions p(y|˜x), and the self consistent equations include also the opti-mization over the representatives, in contrast to rate distortion theory, where the selection of representatives is a separate problem. 12 3.3 The information bottleneck iterative algorithm 

As for the BA algorithm, the self consistent equations (16) and (17) suggest a natural method for finding the unknown distributions, at every value of β.Indeed, these equations can be turned into converging, alternating iterations among the three convex distribution sets, {p(˜ x|x)}, {p(˜ x)}, and {p(y|˜x)}, as stated in the following theorem. 

Theorem 5 The self consistent equations (18), (19), and (28), are satisfied simultaneously at the minima of the functional, 

F [p(˜ x|x); p(˜ x); p(y|˜x)] = −〈 log Z(x, β )〉p(x) (29) = I(X; ˜X) + β〈DKL [p(y|x)|p(y|˜x)] 〉p(x, ˜x) ,(30) 

where the minimization is done independently over the convex sets of the normalized distributions, {p(˜ x)} and {p(˜ x|x)} and {p(y|˜x)}. Namely, 

min  

> p(y|˜x)

min  

> p(˜ x)

min  

> p(˜ x|x)

F [p(˜ x|x); p(˜ x); p(y|˜x)] .

This minimization is performed by the converging alternating iterations. De-noting by t the iteration step, 

> 

pt(˜ x|x) = pt(˜ x) 

> Zt(x,β )

exp( −βd (x, ˜x)) 

pt+1 (˜ x) = ∑ 

> x

p(x)pt(˜ x|x)

pt+1 (y|˜x) = ∑ 

> y

p(y|x)pt(x|˜x)(31) 

and the normalization (partition function) Zt(β, ˜x) is evaluated for every t

in Eq. (31). 

Proof. For lack of space we can only outline the proof. First we show that the equations indeed are satisfied at the minima of the functional F (known for physicists as the “free energy”). This follows from lemma (2) when applied to I(X; ˜X) with the convex sets of p(˜ x) and p(˜ x|x), as for the BA algorithm. Then the second part of the lemma is applied to 〈DKL [p(y|x)|p(y|˜x)] 〉p(x, ˜x)

which is an expected relative entropy. Equation (28) minimizes the expected relative entropy w.r.t. to variations in the convex set of the normalized 13 {p(y|˜x)}. Denoting by d(x, ˜x) = DKL [p(y|x)|p(y|˜x)] and by λ(˜ x) the normal-ization Lagrange multipliers, we obtain 

δd (x, ˜x) = δ

> (

− ∑

> y

p(y|x) log p(y|˜x) + λ(˜ x)( ∑

> y

p(y|˜x) − 1) 

> )

(32) = ∑

> y
> (

−p(y|x)

p(y|˜x) + λ(˜ x)

> )

δp (y|˜x) . (33) The expected relative entropy becomes, 

> ∑
> x
> ∑
> y
> (

−p(y|x)p(x|˜x)

p(y|˜x) + λ(˜ x)

> )

δp (y|˜x) = 0 , (34) which gives Eq. (28), since δp (y|˜x) are independent for each ˜ x. Equation (28) also have the interpretation of a weighted average of the data conditional distributions that contribute to the representative ˜ x.To prove the convergence of the iterations it is enough to verify that each of the iteration steps minimizes the same functional, independently, and that this functional is bounded from below as a sum of two non–negative terms. The only point to notice is that when p(y|˜x) is fixed we are back to the rate distortion case with fixed distortion matrix d(x, ˜x). The argument in [3] for the BA algorithm applies here as well. On the other hand we have just shown that the third equation minimizes the expected relative entropy without affecting the mutual information I(X; ˜ X). This proves the convergence of the alternating iterations. However, the situation here is similar to the EM algorithm and the functional F [p(˜ x|x); p(˜ x); p(y|˜x)] is convex in each of the distribution independently but not in the product space of these distributions. Thus our convergence proof does not imply uniqueness of the solution. 

# 3.4 The structure of the solutions 

The formal solution of the self consistent equations, described above, still requires a specification of the structure and cardinality of ˜X, as in rate distortion theory. For every value of the Lagrange multiplier β there are corresponding values of the mutual information IX ≡ I(X, ˜X), and IY ≡

14 I( ˜X, Y ) for every choice of the cardinality of ˜X. The variational principle implies that 

δI ( ˜X, Y )

δI (X, ˜X) = β−1 > 0 , (35) which suggests a deterministic annealing approach. By increasing the value of β one can move along convex curves in the “information plane” ( IX , I Y ). These curves, analogous to the rate distortion curves, exists for every choice of the cardinality of ˜X. The solutions of the self consistent equations thus correspond to a family of such annealing curves, all starting from the (trivial) point (0 , 0) in the information plane with infinite slope and parameterized by 

β. Interestingly, every two curves in this family separate (bifurcate) at some finite (critical) β through a second order phase transition. These transitions form a hierarchy of relevant quantizations for different cardinalities of ˜X, as described in [1, 5, 6]. 

# Further work 

The most fascinating aspect of the information bottleneck principle is that it provides a unified framework for different information processing problems, including prediction, filtering and learning [1]. There are already several successful applications of this method to various “real” problems, such as semantic clustering of English words [6], document classification [5], neural coding, and spectral analysis. 

Acknowledgements 

Helpful discussions and insights on rate distortion theory with Joachim Buh-mann and Shai Fine are greatly appreciated. Our collaboration was facili-tated in part by a grant from the US–Israel Binational Science Foundation (BSF). 

# References 

[1] W. Bialek and N. Tishby, “Extracting relevant information,” in prepara-tion. 15 [2] T. M. Cover and J. A. Thomas, Elements of Information Theory (Wiley, New York, 1991). [3] I. Csisz´ ar and G. Tusn´ ady, “Information geometry and alternating mini-mization procedures,” Statistics and Decisions Suppl. 1, 205–237 (1984). [4] R. E. Blahut, “Computation of channel capacity and rate distortion func-tion,” IEEE Trans. Inform. Theory IT-18, 460–473 (1972). [5] N. Slonim and N. Tishby, “Agglomerative information bottleneck,” To appear in Advances in Neural Information Processing systems (NIPS-12) 

1999. [6] F. C. Pereira, N. Tishby, and L. Lee, “Distributional clustering of En-glish words,” in 30th Annual Mtg. of the Association for Computational Linguistics , pp. 183–190 (1993). 16