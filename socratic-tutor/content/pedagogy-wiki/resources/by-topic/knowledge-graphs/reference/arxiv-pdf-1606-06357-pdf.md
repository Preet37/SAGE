# Source: https://arxiv.org/pdf/1606.06357.pdf
# Author: Théo Trouillon et al.
# Title: Complex Embeddings for Simple Link Prediction
# Fetched via: jina
# Date: 2026-04-09

Title: Complex Embeddings for Simple Link Prediction



Number of Pages: 12

# Complex Embeddings for Simple Link Prediction 

Th´ eo Trouillon 1,2 THEO .TROUILLON @XRCE .XEROX .COM 

Johannes Welbl 3 J.WELBL @CS .UCL .AC .UK 

Sebastian Riedel 3 S.RIEDEL @CS .UCL .AC .UK 

´Eric Gaussier 2 ERIC .GAUSSIER @IMAG .FR 

Guillaume Bouchard 3 G.BOUCHARD @CS .UCL .AC .UK  

> 1

Xerox Research Centre Europe, 6 chemin de Maupertuis, 38240 Meylan, FRANCE  

> 2

Universit´ e Grenoble Alpes, 621 avenue Centrale, 38400 Saint Martin d’H` eres, FRANCE  

> 3

University College London, Gower St, London WC1E 6BT, UNITED KINGDOM 

# Abstract 

In statistical relational learning, the link predic-tion problem is key to automatically understand the structure of large knowledge bases. As in pre-vious studies, we propose to solve this problem through latent factorization. However, here we make use of complex valued embeddings. The composition of complex embeddings can handle a large variety of binary relations, among them symmetric and antisymmetric relations. Com-pared to state-of-the-art models such as Neural Tensor Network and Holographic Embeddings, our approach based on complex embeddings is arguably simpler , as it only uses the Hermitian dot product, the complex counterpart of the stan-dard dot product between real vectors. Our ap-proach is scalable to large datasets as it remains linear in both space and time, while consistently outperforming alternative approaches on stan-dard link prediction benchmarks. 1

# 1. Introduction 

Web-scale knowledge bases (KBs) provide a structured representation of world knowledge, with projects such as DBPedia (Auer et al., 2007), Freebase (Bollacker et al., 2008) or the Google Knowledge Vault (Dong et al., 2014). They enable a wide range of applications such as recom-mender systems, question answering or automated personal agents. The incompleteness of these KBs has stimulated 

> 1

Code is available at: https://github.com/ ttrouill/complex 

Proceedings of the 33 rd International Conference on Machine Learning , New York, NY, USA, 2016. JMLR: W&CP volume 48. Copyright 2016 by the author(s). 

research into predicting missing entries, a task known as link prediction that is one of the main problems in Statisti-cal Relational Learning (SRL, Getoor & Taskar, 2007). KBs express data as a directed graph with labeled edges (relations) between nodes (entities). Natural redundan-cies among the recorded relations often make it possi-ble to fill in the missing entries of a KB. As an exam-ple, the relation CountryOfBirth is not recorded for all entities, but it can easily be inferred if the relation 

CityOfBirth is known. The goal of link prediction is the automatic discovery of such regularities. How-ever, many relations are non-deterministic: the combina-tion of the two facts IsBornIn(John,Athens) and 

IsLocatedIn(Athens,Greece) does not always imply the fact HasNationality(John,Greece) .Hence, it is required to handle other facts involving these relations or entities in a probabilistic fashion. To do so, an increasingly popular method is to state the link prediction task as a 3D binary tensor completion prob-lem, where each slice is the adjacency matrix of one re-lation type in the knowledge graph. Completion based on low-rank factorization or embeddings has been popularized with the Netflix challenge (Koren et al., 2009). A partially observed matrix or tensor is decomposed into a product of embedding matrices with much smaller rank, resulting in fixed-dimensional vector representations for each entity and relation in the database. For a given fact r(s,o) in which subject s is linked to object o through relation r, the score can then be recovered as a multi-linear product between the embedding vectors of s, r and o (Nickel et al., 2016a). Binary relations in KBs exhibit various types of pat-terns: hierarchies and compositions like FatherOf ,

OlderThan or IsPartOf —with partial/total, strict/non-strict orders—and equivalence relations like IsSimilarTo . As described in Bordes et al. (2013a), a relational model should (a) be able to learn 

> arXiv:1606.06357v1 [cs.AI] 20 Jun 2016 Complex Embeddings for Simple Link Prediction

all combinations of these properties, namely reflexiv-ity/irreflexivity, symmetry/antisymmetry and transitivity, and (b) be linear in both time and memory in order to scale to the size of present day KBs, and keep up with their growth. Dot products of embeddings scale well and can naturally handle both symmetry and (ir-)reflexivity of relations; us-ing an appropriate loss function even enables transitiv-ity (Bouchard et al., 2015). However, dealing with anti-symmetric relations has so far almost always implied an explosion of the number of parameters (Nickel et al., 2011; Socher et al., 2013) (see Table 1), making models prone to overfitting. Finding the best ratio between expressive-ness and parameter space size is the keystone of embedding models. In this work we argue that the standard dot product between embeddings can be a very effective composition function, provided that one uses the right representation . Instead of using embeddings containing real numbers we discuss and demonstrate the capabilities of complex embeddings. When using complex vectors, i.e. vectors with entries in C,the dot product is often called the Hermitian (or sesquilin-ear) dot product, as it involves the conjugate-transpose of one of the two vectors. As a consequence, the dot product is not symmetric any more, and facts about antisymmetric relations can receive different scores depending on the or-dering of the entities involved. Thus complex vectors can effectively capture antisymmetric relations while retaining the efficiency benefits of the dot product, that is linearity in both space and time complexity. The remainder of the paper is organized as follows. We first justify the intuition of using complex embeddings in the square matrix case in which there is only a single rela-tion between entities. The formulation is then extended to a stacked set of square matrices in a third-order tensor to represent multiple relations. We then describe experiments on large scale public benchmark KBs in which we empiri-cally show that this representation leads not only to simpler and faster algorithms, but also gives a systematic accuracy improvement over current state-of-the-art alternatives. To give a clear comparison with respect to existing ap-proaches using only real numbers, we also present an equivalent reformulation of our model that involves only real embeddings. This should help practitioners when im-plementing our method, without requiring the use of com-plex numbers in their software implementation. 

# 2. Relations as Real Part of Low-Rank Normal Matrices 

In this section we discuss the use of complex embed-dings for low-rank matrix factorization and illustrate this by considering a simplified link prediction task with merely a single relation type. Understanding the factorization in complex space leads to a better theoretical understanding of the class of matrices that can actually be approximated by dot products of embed-dings. These are the so-called normal matrices for which the left and right embeddings share the same unitary basis. 

2.1. Modelling Relations 

Let E be a set of entities with |E| = n. A relation between two entities is represented as a binary value Yso ∈ {− 1, 1},where s ∈ E is the subject of the relation and o ∈ E its object. Its probability is given by the logistic inverse link function: 

P (Yso = 1) = σ(Xso ) (1) where X ∈ Rn×n is a latent matrix of scores, and Y the partially observed sign matrix. Our goal is to find a generic structure for X that leads to a flexible approximation of common relations in real world KBs. Standard matrix factorization approximates X by a matrix product U V T , where U and V are two functionally independent n × K matrices, K being the rank of the ma-trix. Within this formulation it is assumed that entities ap-pearing as subjects are different from entities appearing as objects. This means that the same entity will have two dif-ferent embedding vectors, depending on whether it appears as the subject or the object of a relation. This extensively studied type of model is closely related to the singular value decomposition (SVD) and fits well to the case where the matrix X is rectangular. However, in many link prediction problems, the same entity can appear as both subject and 

object. It then seems natural to learn joint embeddings of the entities, which entails sharing the embeddings of the left and right factors, as proposed by several authors to solve the link prediction problem (Nickel et al., 2011; Bor-des et al., 2013b; Yang et al., 2015). In order to use the same embedding for subjects and ob-jects, researchers have generalised the notion of dot prod-ucts to scoring functions , also known as composition func-tions , that combine embeddings in specific ways. We briefly recall several examples of scoring functions in Ta-ble 1, as well as the extension proposed in this paper. Using the same embeddings for right and left factors boils down to Eigenvalue decomposition: 

X = EW E −1 . (2) It is often used to approximate real symmetric matrices such as covariance matrices, kernel functions and distance or similarity matrices. In these cases all eigenvalues and eigenvectors live in the real space and E is orthogonal: Complex Embeddings for Simple Link Prediction 

Model Scoring Function Relation parameters Otime Ospace 

RESCAL (Nickel et al., 2011) eTs Wr eo Wr ∈ RK2

O(K2) O(K2)

TransE (Bordes et al., 2013b) || (es + wr ) − eo|| p wr ∈ RK O(K) O(K)

NTN (Socher et al., 2013) uTr f (esW [1 ..D ] 

> r

eo + Vr

[es

eo

]

+ br ) Wr ∈ RK2D , b r ∈ RK

Vr ∈ R2KD , u r ∈ RK O(K2D) O(K2D)

DistMult (Yang et al., 2015) < w r , e s, e o > wr ∈ RK O(K) O(K)

HolE (Nickel et al., 2016b) wTr (F−1[F[es] F[eo]])) wr ∈ RK O(K log K) O(K)

ComplEx Re( < w r , e s, ¯eo >) wr ∈ CK O(K) O(K)                       

> Table 1. Scoring functions of state-of-the-art latent factor models for a given fact r(s, o ), along with their relation parameters, time and space (memory) complexity. The embeddings esand eoof subject sand object oare in RKfor each model, except for our model (ComplEx) where es, e o∈CK.Dis an additional latent dimension of the NTN model. Fand F−1denote respectively the Fourier transform and its inverse, and is the element-wise product between two vectors.

ET = E−1. We are in this work however explicitly inter-ested in problems where matrices — and thus the relations they represent — can also be antisymmetric. In that case eigenvalue decomposition is not possible in the real space; there only exists a decomposition in the complex space where embeddings x ∈ CK are composed of a real vec-tor component Re( x) and an imaginary vector component 

Im( x). With complex numbers, the dot product, also called the Hermitian product, or sesquilinear form, is defined as: 

〈u, v 〉 := ¯ uT v (3) where u and v are complex-valued vectors, i.e. u =Re( u) + iIm( u) with Re( u) ∈ RK and Im( u) ∈ RK cor-responding to the real and imaginary parts of the vector 

u ∈ CK , and i denoting the square root of −1. We see here that one crucial operation is to take the conjugate of the first vector: ¯u = Re( u) − iIm( u). A simple way to justify the Hermitian product for composing complex vectors is that it provides a valid topological norm in the induced vectorial space. For example, ¯xT x = 0 implies x = 0 while this is not the case for the bilinear form xT x as there are many complex vectors for which xT x = 0 .Even with complex eigenvectors E ∈ Cn×n, the inversion of E in the eigendecomposition of Equation (2) leads to computational issues. Fortunately, mathematicians defined an appropriate class of matrices that prevents us from in-verting the eigenvector matrix: we consider the space of 

normal matrices , i.e. the complex n × n matrices X, such that X ¯XT = ¯XT X. The spectral theorem for normal ma-trices states that a matrix X is normal if and only if it is unitarily diagonalizable: 

X = EW ¯ET (4) where W ∈ Cn×n is the diagonal matrix of eigenvalues (with decreasing modulus) and E ∈ Cn×n is a unitary ma-trix of eigenvectors, with ¯E representing its complex con-jugate. The set of purely real normal matrices includes all sym-metric and antisymmetric sign matrices (useful to model hierarchical relations such as IsOlder ), as well as all orthogonal matrices (including permutation matrices), and many other matrices that are useful to represent binary rela-tions, such as assignment matrices which represent bipar-tite graphs. However, far from all matrices expressed as 

EW ¯ET are purely real, and equation 1 requires the scores 

X to be purely real. So we simply keep only the real part of the decomposition: 

X = Re( EW ¯ET ) . (5) In fact, performing this projection on the real subspace al-lows the exact decomposition of any real square matrix X

and not only normal ones, as shown by Trouillon et al. (2016). Compared to the singular value decomposition, the eigen-value decomposition has two key differences: 

• The eigenvalues are not necessarily positive or real; 

• The factorization (5) is useful as the rows of E can be used as vectorial representations of the entities corre-sponding to rows and columns of the relation matrix 

X. Indeed, for a given entity, its subject embedding vector is the complex conjugate of its object embed-ding vector. 

2.2. Low-Rank Decomposition 

In a link prediction problem, the relation matrix is unknown and the goal is to recover it entirely from noisy observa-tions. To enable the model to be learnable , i.e. to gener-alize to unobserved links, some regularity assumptions are needed. Since we deal with binary relations, we assume that they have low sign-rank . The sign-rank of a sign ma-trix is the smallest rank of a real matrix that has the same sign-pattern as Y :

rank ±(Y ) = min 

> A∈Rm×n

{rank( A)|sign( A) = Y } . (6) Complex Embeddings for Simple Link Prediction 

This is theoretically justified by the fact that the sign-rank is a natural complexity measure of sign matrices (Linial et al., 2007) and is linked to learnability (Alon et al., 2015), and empirically confirmed by the wide success of factorization models (Nickel et al., 2016a). If the observation matrix Y is low-sign-rank, then our model can decompose it with a rank at most the double of the sign-rank of Y . That is, for any Y ∈ {− 1, 1}n×n, there always exists a matrix X = Re( EW ¯ET ) with the same sign pattern sign( X) = Y , where the rank of EW ¯ET is at most twice the sign-rank of Y (Trouillon et al., 2016). Although twice sounds bad, this is actually a good upper bound. Indeed, the sign-rank is often much lower than the rank of Y . For example, the rank of the n × n identity matrix I is n, but rank ±(I) = 3 (Alon et al., 2015). By permutation of the columns 2j and 2j + 1 , the I matrix corresponds to the relation marriedTo , a relation known to be hard to factorize (Nickel et al., 2014). Yet our model can express it in rank 6, for any n.By imposing a low-rank K 
 n on EW ¯ET , only the first 

K values of diag (W ) are non-zero. So we can directly have 

E ∈ Cn×K and W ∈ CK×K . Individual relation scores 

Xso between entities s and o can be predicted through the following product of their embeddings es, e o ∈ CK :

Xso = Re( eTs W ¯eo) . (7) We summarize the above discussion in three points: 1. Our factorization encompasses all possible binary re-lations. 2. By construction, it accurately describes both symmet-ric and antisymmetric relations. 3. Learnable relations can be efficiently approximated by a simple low-rank factorization, using complex num-bers to represent the latent factors. 

# 3. Application to Binary Multi-Relational Data 

The previous section focused on modeling a single type of relation; we now extend this model to multiple types of relations. We do so by allocating an embedding wr to each relation r, and by sharing the entity embeddings across all relations. Let R and E be the set of relations and entities present in the KB. We want to recover the matrices of scores Xr for all the relations r ∈ R . Given two entities s and o ∈ E , the log-odd of the probability that the fact r(s,o) is true is: 

P (Yrso = 1) = σ(φ(r, s, o ; Θ)) (8) where φ is a scoring function that is typically based on a factorization of the observed relations and Θ denotes the parameters of the corresponding model. While X as a whole is unknown, we assume that we observe a set of true and false facts {Yrso }r(s,o )∈Ω ∈ {− 1, 1}|Ω|, corre-sponding to the partially observed adjacency matrices of different relations, where Ω ⊂ R ⊗ E ⊗ E is the set of ob-served triples. The goal is to find the probabilities of entries 

Yr′s′o′ being true or false for a set of targeted unobserved triples r′(s′, o ′) /∈ Ω.Depending on the scoring function φ(s, r, o ; Θ) used to predict the entries of the tensor X, we obtain different mod-els. Examples of scoring functions are given in Table 1. Our model scoring function is: 

φ(r, s, o ; Θ) = Re( < w r , e s, ¯eo >) (9) 

= Re( 

> K

∑

> k=1

wrk esk ¯eok ) (10) 

= 〈Re( wr ), Re( es), Re( eo)〉

+ 〈Re( wr ), Im( es), Im( eo)〉

+ 〈Im( wr ), Re( es), Im( eo)〉− 〈 Im( wr ), Im( es), Re( eo)〉 (11) where wr ∈ CK is a complex vector . These equations provide two interesting views of the model: 

• Changing the representation : Equation (10) would correspond to DistMult with real embeddings, but handles asymmetry thanks to the complex conjugate of one of the embeddings 2.

• Changing the scoring function : Equation (11) only in-volves real vectors corresponding to the real and imag-inary parts of the embeddings and relations. One can easily check that this function is antisymmetric when wr is purely imaginary (i.e. its real part is zero), and symmetric when wr is real. Interestingly, by separating the real and imaginary part of the relation embedding wr , we obtain a decomposition of the relation matrix Xr as the sum of a symmetric matrix Re( E diag (Re( wr )) ¯ET ) and a antisymmetric matrix Im( E diag (−Im( wr )) ¯ET ). Re-lation embeddings naturally act as weights on each la-tent dimension: Re( wr ) over the symmetric, real part of 

〈eo, e s〉, and Im( w) over the antisymmetric, imaginary part of 〈eo, e s〉. Indeed, one has 〈eo, e s〉 = 〈es, e o〉, meaning that Re( 〈eo, e s〉) is symmetric, while Im( 〈eo, e s〉) is an-tisymmetric. This enables us to accurately describe both       

> 2Note that in Equation (10) we used the standard componen-twise multi-linear dot product < a, b, c > := ∑
> kakbkck. This is not the Hermitian extension as it is not properly defined in the linear algebra literature. Complex Embeddings for Simple Link Prediction

symmetric and antisymmetric relations between pairs of entities, while still using joint representations of entities, whether they appear as subject or object of relations. Geometrically, each relation embedding wr is an anisotropic scaling of the basis defined by the entity embed-dings E, followed by a projection onto the real subspace. 

# 4. Experiments 

In order to evaluate our proposal, we conducted experi-ments on both synthetic and real datasets. The synthetic dataset is based on relations that are either symmetric or antisymmetric, whereas the real datasets comprise differ-ent types of relations found in different, standard KBs. We refer to our model as ComplEx, for Complex Embeddings. 

4.1. Synthetic Task 

To assess the ability of our proposal to accurately model symmetry and antisymmetry, we randomly generated a KB of two relations and 30 entities. One relation is entirely symmetric, while the other is completely antisymmetric. This dataset corresponds to a 2 × 30 × 30 tensor. Figure 2 shows a part of this randomly generated tensor, with a symmetric slice and an antisymmetric slice, decomposed into training, validation and test sets. The diagonal is un-observed as it is not relevant in this experiment. The train set contains 1392 observed triples, whereas the validation and test sets contain 174 triples each. Figure 1 shows the best cross-validated Average Precision (area under Precision-Recall curve) for different factorization models of ranks ranging up to 50. Models were trained using Stochastic Gradient Descent with mini-batches and AdaGrad for tuning the learning rate (Duchi et al., 2011), by minimizing the negative log-likelihood of the logistic model with L2 regularization on the parameters Θ of the considered model: 

min 

> Θ

∑

> r(s,o )∈Ω

log(1 + exp( −Yrso φ(s, r, o ; Θ))) + λ|| Θ|| 22 .

(12) In our model, Θ corresponds to the embeddings 

es, w r , e o ∈ CK . We describe the full algorithm in Ap-pendix A. 

λ is validated in {0.1, 0.03 , 0.01 , 0.003 , 0.001 , 0.0003 ,

0.00001 , 0.0}. As expected, DistMult (Yang et al., 2015) is not able to model antisymmetry and only predicts the symmetric relations correctly. Although TransE (Bor-des et al., 2013b) is not a symmetric model, it performs poorly in practice, particularly on the antisymmetric rela-tion. RESCAL (Nickel et al., 2011), with its large number of parameters, quickly overfits as the rank grows. Canon-ical Polyadic (CP) decomposition (Hitchcock, 1927) fails  

> Figure 2. Parts of the training, validation and test sets of the gener-ated experiment with one symmetric and one antisymmetric rela-tion. Red pixels are positive triples, blue are negatives, and green missing ones. Top: Plots of the symmetric slice (relation) for the 10 first entities. Bottom: Plots of the antisymmetric slice for the 10 first entities.

on both relations as it has to push symmetric and antisym-metric patterns through the entity embeddings. Surpris-ingly, only our model succeeds on such simple data. 

4.2. Datasets: FB15K and WN18 

Dataset |E| |R| #triples in Train/Valid/Test WN18 40,943 18 141,442 / 5,000 / 5,000 FB15K 14,951 1,345 483,142 / 50,000 / 59,071  

> Table 3. Number of entities, relations, and observed triples in each split for the FB15K and WN18 datasets.

We next evaluate the performance of our model on the FB15K and WN18 datasets. FB15K is a subset of Free-base , a curated KB of general facts, whereas WN18 is a subset of Wordnet , a database featuring lexical relations be-tween words. We use original training, validation and test set splits as provided by Bordes et al. (2013b). Table 3 summarizes the metadata of the two datasets. Both datasets contain only positive triples. As in Bor-des et al. (2013b), we generated negatives using the local closed world assumption . That is, for a triple, we randomly change either the subject or the object at random, to form a negative example. This negative sampling is performed at runtime for each batch of training positive examples. For evaluation, we measure the quality of the ranking of each test triple among all possible subject and object sub-stitutions : r(s′, o ) and r(s, o ′), ∀s′, ∀o′ ∈ E . Mean Recip-rocal Rank (MRR) and Hits at m are the standard evalua-tion measures for these datasets and come in two flavours: raw and filtered (Bordes et al., 2013b). The filtered metrics Complex Embeddings for Simple Link Prediction  

> Figure 1. Average Precision (AP) for each factorization rank ranging from 1 to 50 for different state of the art models on the combined symmetry and antisymmetry experiment. Top-left: AP for the symmetric relation only. Top-right: AP for the antisymmetric relation only. Bottom: Overall AP.

are computed after removing all the other positive observed triples that appear in either training, validation or test set from the ranking, whereas the raw metrics do not remove these. Since ranking measures are used, previous studies gener-ally preferred a pairwise ranking loss for the task (Bordes et al., 2013b; Nickel et al., 2016b). We chose to use the neg-ative log-likelihood of the logistic model, as it is a continu-ous surrogate of the sign-rank, and has been shown to learn compact representations for several important relations, es-pecially for transitive relations (Bouchard et al., 2015). In preliminary work, we tried both losses, and indeed the log-likelihood yielded better results than the ranking loss (ex-cept with TransE), especially on FB15K. We report both filtered and raw MRR, and filtered Hits at 1, 3 and 10 in Table 2 for the evaluated models. Furthermore, we chose TransE, DistMult and HolE as baselines since they are the best performing models on those datasets to the best of our knowledge (Nickel et al., 2016b; Yang et al., 2015). We also compare with the CP model to emphasize empirically the importance of learning unique embeddings for entities. For experimental fairness, we reimplemented these methods within the same framework as the ComplEx model, using theano (Bergstra et al., 2010). However, due to time constraints and the complexity of an efficient imple-mentation of HolE, we record the original results for HolE as reported in Nickel et al. (2016b). 

4.3. Results 

WN18 describes lexical and semantic hierarchies between concepts and contains many antisymmetric relations such as hypernymy, hyponymy, or being ”part of”. Indeed, the DistMult and TransE models are outperformed here by ComplEx and HolE, which are on par with respective fil-tered MRR scores of 0.941 and 0.938. Table 4 shows the filtered test set MRR for the models considered and each relation of WN18, confirming the advantage of our model on antisymmetric relations while losing nothing on the oth-ers. 2D projections of the relation embeddings provided in Appendix B visually corroborate the results. On FB15K, the gap is much more pronounced and the ComplEx model largely outperforms HolE, with a filtered MRR of 0.692 and 59.9% of Hits at 1, compared to 0.524 and 40.2% for HolE. We attribute this to the simplicity of our model and the different loss function. This is supported by the relatively small gap in MRR compared to DistMult (0.654); our model can in fact be interpreted as a complex number version of DistMult. On both datasets, TransE Complex Embeddings for Simple Link Prediction 

WN18 FB15K 

MRR Hits at MRR Hits at Model Filter Raw 1 3 10 Filter Raw 1 3 10 CP 0.075 0.058 0.049 0.080 0.125 0.326 0.152 0.219 0.376 0.532 TransE 0.454 0.335 0.089 0.823 0.934 0.380 0.221 0.231 0.472 0.641 DistMult 0.822 0.532 0.728 0.914 0.936 0.654 0.242 0.546 0.733 0.824 HolE* 0.938 0.616 0.93 0.945 0.949 0.524 0.232 0.402 0.613 0.739 ComplEx 0.941 0.587 0.936 0.945 0.947 0.692 0.242 0.599 0.759 0.840  

> Table 2. Filtered and Raw Mean Reciprocal Rank (MRR) for the models tested on the FB15K and WN18 datasets. Hits@m metrics are filtered. *Results reported from (Nickel et al., 2016b) for HolE model.

Relation name ComplEx DistMult TransE hypernym 0.953 0.791 0.446 hyponym 0.946 0.710 0.361 member meronym 0.921 0.704 0.418 member holonym 0.946 0.740 0.465 instance hypernym 0.965 0.943 0.961 instance hyponym 0.945 0.940 0.745 has part 0.933 0.753 0.426 part of 0.940 0.867 0.455 member of domain topic 0.924 0.914 0.861 synset domain topic of 0.930 0.919 0.917 member of domain usage 0.917 0.917 0.875 synset domain usage of 1.000 1.000 1.000 

member of domain region 0.865 0.635 0.865 

synset domain region of 0.919 0.888 0.986 

derivationally related form 0.946 0.940 0.384 similar to 1.000 1.000 0.244 verb group 0.936 0.897 0.323 also see 0.603 0.607 0.279  

> Table 4. Filtered Mean Reciprocal Rank (MRR) for the models tested on each relation of the Wordnet dataset (WN18).

and CP are largely left behind. This illustrates the power of the simple dot product in the first case, and the impor-tance of learning unique entity embeddings in the second. CP performs poorly on WN18 due to the small number of relations, which magnifies this subject/object difference. Reported results are given for the best set of hyper-parameters evaluated on the validation set for each model, after grid search on the fol-lowing values: K ∈ {10 , 20 , 50 , 100 , 150 , 200 },

λ ∈ {0.1, 0.03 , 0.01 , 0.003 , 0.001 , 0.0003 , 0.0},

α0 ∈ { 1.0, 0.5, 0.2, 0.1, 0.05 , 0.02 , 0.01 }, η ∈ { 1, 2, 5, 10 }

with λ the L2 regularization parameter, α0 the initial learning rate (then tuned at runtime with AdaGrad), and 

η the number of negatives generated per positive training triple. We also tried varying the batch size but this had no impact and we settled with 100 batches per epoch. Best ranks were generally 150 or 200, in both cases scores were always very close for all models. The number of negative samples per positive sample also had a large influence on the filtered MRR on FB15K (up to +0.08 improvement from 1 to 10 negatives), but not much on WN18. On both datasets regularization was important (up to +0.05 on filtered MRR between λ = 0 and optimal one). We found the initial learning rate to be very important on FB15K, while not so much on WN18. We think this may also explain the large gap of improvement our model provides on this dataset compared to previously published results – as DistMult results are also better than those previously reported (Yang et al., 2015) – along with the use of the log-likelihood objective. It seems that in general AdaGrad is relatively insensitive to the initial learning rate, perhaps causing some overconfidence in its ability to tune the step size online and consequently leading to less efforts when selecting the initial step size. Training was stopped using early stopping on the valida-tion set filtered MRR, computed every 50 epochs with a maximum of 1000 epochs. 

4.4. Influence of Negative Samples 

We further investigated the influence of the number of neg-atives generated per positive training sample. In the pre-vious experiment, due to computational limitations, the number of negatives per training sample, η, was validated among the possible numbers {1, 2, 5, 10 }. We want to ex-plore here whether increasing these numbers could lead to better results. To do so, we focused on FB15K, with the best validated λ, K, α 0, obtained from the previous experi-ment. We then let η vary in {1, 2, 5, 10 , 20 , 50 , 100 , 200 }.Figure 3 shows the influence of the number of generated negatives per positive training triple on the performance of our model on FB15K. Generating more negatives clearly improves the results, with a filtered MRR of 0.737 with 100 negative triples (and 64.8% of Hits@1), before decreas-ing again with 200 negatives. The model also converges with fewer epochs, which compensates partially for the ad-ditional training time per epoch, up to 50 negatives. It then grows linearly as the number of negatives increases, mak-ing 50 a good trade-off between accuracy and training time. Complex Embeddings for Simple Link Prediction         

> Figure 3. Influence of the number of negative triples generated per positive training example on the filtered test MRR and on train-ing time to convergence on FB15K for the ComplEx model with
> K= 200 ,λ= 0 .01 and α0= 0 .5. Times are given relative to the training time with one negative triple generated per positive training sample ( = 1 on time scale).

# 5. Related Work 

In the early age of spectral theory in linear algebra, com-plex numbers were not used for matrix factorization and mathematicians mostly focused on bi-linear forms (Bel-trami, 1873). The eigen-decomposition in the complex do-main as taught today in linear algebra courses came 40 years later (Autonne, 1915). Similarly, most of the exist-ing approaches for tensor factorization were based on de-compositions in the real domain, such as the Canonical Polyadic (CP) decomposition (Hitchcock, 1927). These methods are very effective in many applications that use different modes of the tensor for different types of entities. But in the link prediction problem, antisymmetry of rela-tions was quickly seen as a problem and asymmetric ex-tensions of tensors were studied, mostly by either consider-ing independent embeddings (Sutskever, 2009) or consider-ing relations as matrices instead of vectors in the RESCAL model (Nickel et al., 2011). Direct extensions were based on uni-,bi- and trigram latent factors for triple data, as well as a low-rank relation matrix (Jenatton et al., 2012). Pairwise interaction models were also considered to im-prove prediction performances. For example, the Universal Schema approach (Riedel et al., 2013) factorizes a 2D un-folding of the tensor (a matrix of entity pairs vs. relations) while Welbl et al. (2016) extend this also to other pairs. In the Neural Tensor Network (NTN) model, Socher et al. (2013) combine linear transformations and multiple bilin-ear forms of subject and object embeddings to jointly feed them into a nonlinear neural layer. Its non-linearity and multiple ways of including interactions between embed-dings gives it an advantage in expressiveness over models with simpler scoring function like DistMult or RESCAL. As a downside, its very large number of parameters can make the NTN model harder to train and overfit more eas-ily. The original multi-linear DistMult model is symmetric in subject and object for every relation (Yang et al., 2015) and achieves good performance, presumably due to its simplic-ity. The TransE model from Bordes et al. (2013b) also em-beds entities and relations in the same space and imposes a geometrical structural bias into the model: the subject en-tity vector should be close to the object entity vector once translated by the relation vector. A recent novel way to handle antisymmetry is via the Holographic Embeddings (HolE) model by (Nickel et al., 2016b). In HolE the circular correlation is used for combin-ing entity embeddings, measuring the covariance between embeddings at different dimension shifts. This generally suggests that other composition functions than the classi-cal tensor product can be helpful as they allow for a richer interaction of embeddings. However, the asymmetry in the composition function in HolE stems from the asymmetry of circular correlation, an O(nlog (n)) operation, whereas ours is inherited from the complex inner product, in O(n).

# 6. Conclusion 

We described a simple approach to matrix and tensor fac-torization for link prediction data that uses vectors with complex values and retains the mathematical definition of the dot product. The class of normal matrices is a natural fit for binary relations, and using the real part allows for ef-ficient approximation of any learnable relation. Results on standard benchmarks show that no more modifications are needed to improve over the state-of-the-art. There are several directions in which this work can be ex-tended. An obvious one is to merge our approach with known extensions to tensor factorization in order to fur-ther improve predictive performance. For example, the use of pairwise embeddings together with complex numbers might lead to improved results in many situations that in-volve non-compositionality. Another direction would be to develop a more intelligent negative sampling procedure, to generate more informative negatives with respect to the positive sample from which they have been sampled. It would reduce the number of negatives required to reach good performance, thus accelerating training time. Also, if we were to use complex embeddings every time a model includes a dot product, e.g. in deep neural networks, would it lead to a similar systematic improvement? Complex Embeddings for Simple Link Prediction 

# Acknowledgements 

This work was supported in part by the Paul Allen Founda-tion through an Allen Distinguished Investigator grant and in part by a Google Focused Research Award. 

# References 

Alon, Noga, Moran, Shay, and Yehudayoff, Amir. Sign rank versus vc dimension. arXiv preprint arXiv:1503.07648 , 2015. Auer, Sren, Bizer, Christian, Kobilarov, Georgi, Lehmann, Jens, and Ives, Zachary. Dbpedia: A nucleus for a web of open data. In In 6th Intl Semantic Web Conference, Busan, Korea , pp. 11–15. Springer, 2007. Autonne, L. Sur les matrices hypohermitiennes et sur les matrices unitaires. Ann. Univ. Lyons, Nouvelle Srie I , 38: 1–77, 1915. Beltrami, Eugenio. Sulle funzioni bilineari. Giornale di Matematiche ad Uso degli Studenti Delle Universita , 11 (2):98–106, 1873. Bergstra, James, Breuleux, Olivier, Bastien, Fr´ ed´ eric, Lamblin, Pascal, Pascanu, Razvan, Desjardins, Guil-laume, Turian, Joseph, Warde-Farley, David, and Ben-gio, Yoshua. Theano: a CPU and GPU math expression compiler. In Proceedings of the Python for Scientific Computing Conference (SciPy) , June 2010. Oral Pre-sentation. Bollacker, Kurt, Evans, Colin, Paritosh, Praveen, Sturge, Tim, and Taylor, Jamie. Freebase: a collaboratively cre-ated graph database for structuring human knowledge. In SIGMOD 08 Proceedings of the 2008 ACM SIGMOD international conference on Management of data , pp. 1247–1250, 2008. Bordes, Antoine, Usunier, Nicolas, Garcia-Duran, Alberto, Weston, Jason, and Yakhnenko, Oksana. Irreflexive and Hierarchical Relations as Translations. In CoRR , 2013a. Bordes, Antoine, Usunier, Nicolas, Garcia-Duran, Alberto, Weston, Jason, and Yakhnenko, Oksana. Translating embeddings for modeling multi-relational data. In Ad-vances in Neural Information Processing Systems , pp. 2787–2795, 2013b. Bouchard, Guillaume, Singh, Sameer, and Trouillon, Th´ eo. On approximate reasoning capabilities of low-rank vec-tor spaces. In AAAI Spring Syposium on Knowledge Rep-resentation and Reasoning (KRR): Integrating Symbolic and Neural Approaches , 2015. Dong, Xin, Gabrilovich, Evgeniy, Heitz, Geremy, Horn, Wilko, Lao, Ni, Murphy, Kevin, Strohmann, Thomas, Sun, Shaohua, and Zhang, Wei. Knowledge vault: A web-scale approach to probabilistic knowledge fusion. In Proceedings of the 20th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining ,KDD ’14, pp. 601–610, 2014. Duchi, John, Hazan, Elad, and Singer, Yoram. Adaptive subgradient methods for online learning and stochastic optimization. The Journal of Machine Learning Re-search , 12:2121–2159, 2011. Getoor, Lise and Taskar, Ben. Introduction to Statis-tical Relational Learning (Adaptive Computation and Machine Learning) . The MIT Press, 2007. ISBN 0262072882. Hitchcock, F. L. The expression of a tensor or a polyadic as a sum of products. J. Math. Phys , 6(1):164–189, 1927. Jenatton, Rodolphe, Bordes, Antoine, Le Roux, Nicolas, and Obozinski, Guillaume. A Latent Factor Model for Highly Multi-relational Data. In Advances in Neural In-formation Processing Systems 25 , pp. 3167–3175, 2012. Koren, Yehuda, Bell, Robert, and Volinsky, Chris. Ma-trix factorization techniques for recommender systems. 

Computer , 42(8):30–37, 2009. Linial, Nati, Mendelson, Shahar, Schechtman, Gideon, and Shraibman, Adi. Complexity measures of sign matrices. 

Combinatorica , 27(4):439–463, 2007. Nickel, Maximilian, Tresp, Volker, and Kriegel, Hans-Peter. A Three-Way Model for Collective Learning on Multi-Relational Data. In 28th International Conference on Machine Learning , pp. 809—-816, 2011. Nickel, Maximilian, Jiang, Xueyan, and Tresp, Volker. Re-ducing the rank in relational factorization models by in-cluding observable patterns. In Advances in Neural In-formation Processing Systems , pp. 1179–1187, 2014. Nickel, Maximilian, Murphy, Kevin, Tresp, Volker, and Gabrilovich, Evgeniy. A review of relational machine learning for knowledge graphs. Proceedings of the IEEE ,104(1):11–33, 2016a. Nickel, Maximilian, Rosasco, Lorenzo, and Poggio, Tomaso A. Holographic embeddings of knowledge graphs. In Proceedings of the Thirtieth AAAI Conference on Artificial Intelligence , pp. 1955–1961, 2016b. Riedel, Sebastian, Yao, Limin, McCallum, Andrew, and Marlin, Benjamin M. Relation extraction with matrix factorization and universal schemas. In Human Lan-guage Technologies: Conference of the North American Chapter of the Association of Computational Linguis-tics, Proceedings , pp. 74–84, 2013. Complex Embeddings for Simple Link Prediction 

Socher, Richard, Chen, Danqi, Manning, Christopher D, and Ng, Andrew. Reasoning with neural tensor networks for knowledge base completion. In Advances in Neural Information Processing Systems , pp. 926–934, 2013. Sutskever, Ilya. Modelling Relational Data using Bayesian Clustered Tensor Factorization. In Advances in Neural Information Processing Systems , volume 22, pp. 1–8, 2009. Trouillon, Th´ eo, Dance, Christopher R., Gaussier, ´ Eric, and Bouchard, Guillaume. Decomposing real square ma-trices via unitary diagonalization. arXiv:1605.07103 ,2016. Welbl, Johannes, Bouchard, Guillaume, and Riedel, Se-bastian. A factorization machine framework for test-ing bigram embeddings in knowledgebase completion. 

arXiv:1604.05878 , 2016. Yang, Bishan, Yih, Wen-tau, He, Xiaodong, Gao, Jianfeng, and Deng, Li. Embedding entities and relations for learn-ing and inference in knowledge bases. In International Conference on Learning Representations , 2015. Complex Embeddings for Simple Link Prediction 

# A. SGD algorithm 

We describe the algorithm to learn the ComplEx model with Stochastic Gradient Descent using only real-valued vectors. Let us rewrite equation 11, by denoting the real part of embeddings with primes and the imaginary part with double primes: e′ 

> i

= Re( ei), e′′  

> i

= Im( ei), w′ 

> r

=Re( wr ), w′′  

> r

= Im( wr ). The set of parameters is Θ = 

{e′

> i

, e ′′  

> i

, w ′ 

> r

, w ′′  

> r

; ∀i ∈ E , ∀r ∈ R} , and the scoring function involves only real vectors: 

φ(r, s, o ; Θ) = 〈w′ 

> r

, e ′

> s

, e ′

> o

〉 + 〈w′ 

> r

, e ′′  

> s

, e ′′  

> o

〉

+ 〈w′′  

> r

, e ′

> s

, e ′′  

> o

〉 − 〈 w′′  

> r

, e ′′  

> s

, e ′

> o

〉

where each entity and each relation has two real embed-dings. Gradients are now easy to write: 

∇e′ 

> s

φ(r, s, o ; Θ) = (w′ 

> r

e′

> o

) + ( w′′  

> r

e′′  

> o

)

∇e′′  

> s

φ(r, s, o ; Θ) = (w′ 

> r

e′′  

> o

) − (w′′  

> r

e′

> o

)

∇e′ 

> o

φ(r, s, o ; Θ) = (w′ 

> r

e′

> s

) − (w′′  

> r

e′′  

> s

)

∇e′′  

> o

φ(r, s, o ; Θ) = (w′ 

> r

e′′  

> s

) + ( w′′  

> r

e′

> s

)

∇w′ 

> r

φ(r, s, o ; Θ) = (e′ 

> s

e′

> o

) + ( e′′  

> s

e′′  

> o

)

∇w′′  

> r

φ(r, s, o ; Θ) = (e′ 

> s

e′′  

> o

) − (e′′  

> s

e′

> o

)

where is the element-wise (Hadamard) product. As stated in equation 8 we use the sigmoid link function, and minimize the L2-regularized negative log-likelihood: 

γ(Ω; Θ) = ∑

> r(s,o )∈Ω

log(1 + exp( −Yrso φ(s, r, o ; Θ))) +λ|| Θ|| 22 .

To handle regularization, note that the squared L2-norm of a complex vector v = v′ + iv ′′ is the sum of the squared modulus of each entry: 

|| v|| 22 = ∑

> j

√

v′2 

> j

+ v′′ 2

> j
> 2

= ∑

> j

v′2 

> j

+ ∑

> j

v′′ 2

> j

= || v′|| 22 + || v′′ || 22

which is actually the sum of the L2-norms of the vectors of the real and imaginary parts. 

Algorithm 1 SGD for the ComplEx model 

input Training set Ω, Validation set Ωv , learning rate α,embedding dim. k, regularization factor λ, negative ratio 

η, batch size b, max iter m, early stopping s.

e′ 

> i

← randn( k), e′′  

> i

← randn( k) for each i ∈ E 

w′ 

> i

← randn( k), w′′  

> i

← randn( k) for each i ∈ R 

for i = 1 , · · · , m do for j = 1 .. |Ω|/b do 

Ωb ← sample (Ω , b, η )

Update embeddings w.r.t.: ∑ 

> r(s,o )∈Ωb

∇γ({r(s, o )}; Θ) 

Update learning rate α using Adagrad 

end for if i mod s = 0 then break if filteredMRR or AP on Ωv decreased 

end if end for 

We can finally write the gradient of γ with respect to a real 

embedding v for one triple r(s, o ):

∇v γ({r(s, o )}; Θ) = −Yrso φ(s, r, o ; Θ) σ(∇v φ(r, s, o ; Θ)) +2 λv 

where σ(x) = 11+e −x is the sigmoid function. Algorithm 1 describes SGD for this formulation of the scor-ing function. When Ω contains only positive triples, we generate η negatives per positive train triple, by corrupt-ing either the subject or the object of the positive triple, as described in Bordes et al. (2013b). 

# B. WN18 embeddings visualization 

We used principal component analysis (PCA) to visual-ize embeddings of the relations of the wordnet dataset (WN18). We plotted the four first components of the best DistMult and ComplEx model’s embeddings in Figure 4. For the ComplEx model, we simply concatenated the real and imaginary parts of each embedding. Most of WN18 relations describe hierarchies, and are thus antisymmetric. Each of these hierarchic relations has its inverse relation in the dataset. For example: hypernym / hyponym , part of 

/ has part , synset domain topic of /

member of domain topic . Since DistMult is unable to model antisymmetry, it will correctly represent the na-ture of each pair of opposite relations, but not the direction of the relations. Loosely speaking, in the hypernym /

hyponym pair the nature is sharing semantics, and the direction is that one entity generalizes the semantics of the other. This makes DistMult reprensenting the opposite Complex Embeddings for Simple Link Prediction 

Figure 4. Plots of the first and second (Top), third and fourth (Bottom) components of the WN18 relations embeddings using PCA. Left: DistMult embeddings. Right: ComplEx embeddings. Opposite relations are clustered together by DistMult while correctly separated by ComplEx. 

relations with very close embeddings, as Figure 4 shows. It is especially striking for the third and fourth principal component (bottom-left). Conversely, ComplEx manages to oppose spatially the opposite relations.