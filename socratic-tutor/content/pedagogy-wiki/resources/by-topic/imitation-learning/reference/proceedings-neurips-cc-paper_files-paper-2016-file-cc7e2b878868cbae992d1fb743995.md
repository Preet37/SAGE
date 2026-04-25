# Source: https://proceedings.neurips.cc/paper_files/paper/2016/file/cc7e2b878868cbae992d1fb743995d8f-Paper.pdf
# Title: Generative Adversarial Imitation Learning
# Fetched via: jina
# Date: 2026-04-09

Title: cc7e2b878868cbae992d1fb743995d8f-Paper.pdf


Number of Pages: 9

# Generative Adversarial Imitation Learning 

Jonathan Ho 

OpenAI 

hoj@openai.com 

Stefano Ermon 

Stanford University 

ermon@cs.stanford.edu 

## Abstract 

Consider learning a policy from example expert behavior, without interaction with the expert or access to a reinforcement signal. One approach is to recover the expert’s cost function with inverse reinforcement learning, then extract a policy from that cost function with reinforcement learning. This approach is indirect and can be slow. We propose a new general framework for directly extracting a policy from data as if it were obtained by reinforcement learning following inverse reinforcement learning. We show that a certain instantiation of our framework draws an analogy between imitation learning and generative adversarial networks, from which we derive a model-free imitation learning algorithm that obtains signif-icant performance gains over existing model-free methods in imitating complex behaviors in large, high-dimensional environments. 

## 1 Introduction 

We are interested in a specific setting of imitation learning—the problem of learning to perform a task from expert demonstrations—in which the learner is given only samples of trajectories from the expert, is not allowed to query the expert for more data while training, and is not provided a reinforcement signal of any kind. There are two main approaches suitable for this setting: behavioral cloning [ 18 ], which learns a policy as a supervised learning problem over state-action pairs from expert trajectories; and inverse reinforcement learning [ 23 , 16 ], which finds a cost function under which the expert is uniquely optimal. Behavioral cloning, while appealingly simple, only tends to succeed with large amounts of data, due to compounding error caused by covariate shift [ 21 , 22 ]. Inverse reinforcement learning (IRL), on the other hand, learns a cost function that prioritizes entire trajectories over others, so compounding error, a problem for methods that fit single-timestep decisions, is not an issue. Accordingly, IRL has succeeded in a wide range of problems, from predicting behaviors of taxi drivers [ 29 ] to planning footsteps for quadruped robots [20]. Unfortunately, many IRL algorithms are extremely expensive to run, requiring reinforcement learning in an inner loop. Scaling IRL methods to large environments has thus been the focus of much recent work [ 6, 13 ]. Fundamentally, however, IRL learns a cost function, which explains expert behavior but does not directly tell the learner how to act. Given that the learner’s true goal often is to take actions imitating the expert—indeed, many IRL algorithms are evaluated on the quality of the optimal actions of the costs they learn—why, then, must we learn a cost function, if doing so possibly incurs significant computational expense yet fails to directly yield actions? We desire an algorithm that tells us explicitly how to act by directly learning a policy. To develop such an algorithm, we begin in Section 3, where we characterize the policy given by running reinforcement learning on a cost function learned by maximum causal entropy IRL [ 29 , 30 ]. Our characterization introduces a framework for directly learning policies from data, bypassing any intermediate IRL step. Then, we instantiate our framework in Sections 4 and 5 with a new model-free imitation learning algorithm. We show that our resulting algorithm is intimately connected to generative adversarial 

> 30th Conference on Neural Information Processing Systems (NIPS 2016), Barcelona, Spain.

networks [ 8], a technique from the deep learning community that has led to recent successes in modeling distributions of natural images: our algorithm harnesses generative adversarial training to fit distributions of states and actions defining expert behavior. We test our algorithm in Section 6, where we find that it outperforms competing methods by a wide margin in training policies for complex, high-dimensional physics-based control tasks over various amounts of expert data. 

## 2 Background 

Preliminaries R will denote the extended real numbers R ∪ {∞} . Section 3 will work with finite state and action spaces S and A, but our algorithms and experiments later in the paper will run in high-dimensional continuous environments. Π is the set of all stationary stochastic policies that take actions in A given states in S; successor states are drawn from the dynamics model 

P (s′|s, a ). We work in the γ-discounted infinite horizon setting, and we will use an expectation with respect a policy π ∈ Π to denote an expectation with respect to the trajectory it generates: 

Eπ [c(s, a )] , E [∑∞ 

> t=0

γtc(st, a t)] , where s0 ∼ p0, at ∼ π(·| st), and st+1 ∼ P (·| st, a t) for t ≥ 0.We will use ˆEτ to denote an empirical expectation with respect to trajectory samples τ , and we will always use πE to refer to the expert policy. 

Inverse reinforcement learning Suppose we are given an expert policy πE that we wish to ratio-nalize with IRL. For the remainder of this paper, we will adopt and assume the existence of solutions of maximum causal entropy IRL [ 29 , 30 ], which fits a cost function from a family of functions C with the optimization problem 

maximize 

> c∈C

(

min  

> π∈Π

−H(π) + Eπ [c(s, a )] 

)

− EπE [c(s, a )] (1) where H(π) , Eπ [− log π(a|s)] is the γ-discounted causal entropy [ 3] of the policy π. In practice, 

πE will only be provided as a set of trajectories sampled by executing πE in the environment, so the expected cost of πE in Eq. (1) is estimated using these samples. Maximum causal entropy IRL looks for a cost function c ∈ C that assigns low cost to the expert policy and high cost to other policies, thereby allowing the expert policy to be found via a certain reinforcement learning procedure: 

RL( c) = arg min 

> π∈Π

−H(π) + Eπ [c(s, a )] (2) which maps a cost function to high-entropy policies that minimize the expected cumulative cost. 

## 3 Characterizing the induced optimal policy 

To begin our search for an imitation learning algorithm that both bypasses an intermediate IRL step and is suitable for large environments, we will study policies found by reinforcement learning on costs learned by IRL on the largest possible set of cost functions C in Eq. (1): all functions 

RS×A = {c : S × A → R}. Using expressive cost function classes, like Gaussian processes [ 14 ]and neural networks [ 6], is crucial to properly explain complex expert behavior without meticulously hand-crafted features. Here, we investigate the best IRL can do with respect to expressiveness by examining its capabilities with C = RS×A .Of course, with such a large C, IRL can easily overfit when provided a finite dataset. Therefore, we will incorporate a (closed, proper) convex cost function regularizer ψ : RS×A → R into our study. Note that convexity is a not particularly restrictive requirement: ψ must be convex as a function defined on all of RS×A , not as a function defined on a small parameter space; indeed, the cost regularizers of Finn et al. [6] , effective for a range of robotic manipulation tasks, satisfy this requirement. Interestingly, ψ will play a central role in our discussion and will not serve as a nuisance in our analysis. Let us define an IRL primitive procedure, which finds a cost function such that the expert performs better than all other policies, with the cost regularized by ψ:

IRL ψ (πE ) = arg max 

> c∈RS×A

−ψ(c) + 

(

min  

> π∈Π

−H(π) + Eπ [c(s, a )] 

)

− EπE [c(s, a )] (3) 2Let ˜c ∈ IRL ψ (πE ). We are interested in a policy given by RL(˜ c)—this is the policy given by running reinforcement learning on the output of IRL. To characterize RL(˜ c), let us first define for a policy π ∈ Π its occupancy measure ρπ : S × A → R as ρπ (s, a ) = π(a|s) ∑∞ 

> t=0

γtP (st = s|π).The occupancy measure can be interpreted as the unnormalized distribution of state-action pairs that an agent encounters when navigating the environment with the policy π, and it allows us to write Eπ [c(s, a )] = ∑ 

> s,a

ρπ (s, a )c(s, a ) for any cost function c. We will also need the concept of a convex conjugate: for a function f : RS×A → R, its convex conjugate f ∗ : RS×A → R is given by 

f ∗(x) = sup y∈RS×A xT y − f (y).Now, we are prepared to characterize RL(˜ c), the policy learned by RL on the cost recovered by IRL: 

Proposition 3.1. RL ◦ IRL ψ (πE ) = arg min π∈Π −H(π) + ψ∗(ρπ − ρπE ) (4) 

The proof of Proposition 3.1 can be found in Appendix A.1. It relies on the observation that the optimal cost function and policy form a saddle point of a certain function. IRL finds one coordinate of this saddle point, and running RL on the output of IRL reveals the other coordinate. Proposition 3.1 tells us that ψ-regularized inverse reinforcement learning, implicitly, seeks a policy whose occupancy measure is close to the expert’s, as measured by ψ∗. Enticingly, this suggests that various settings of ψ lead to various imitation learning algorithms that directly solve the optimization problem given by Proposition 3.1. We explore such algorithms in Sections 4 and 5, where we show that certain settings of ψ lead to both existing algorithms and a novel one. The special case when ψ is a constant function is particularly illuminating, so we state and show it directly using concepts from convex optimization. 

Proposition 3.2. Suppose ρπE > 0. If ψ is a constant function, ˜c ∈ IRL ψ (πE ), and ˜π ∈ RL(˜ c),then ρ˜π = ρπE .

In other words, if there were no cost regularization at all, the recovered policy will exactly match the expert’s occupancy measure. (The condition ρπE > 0, inherited from Ziebart et al. [30] , simplifies our discussion and in fact guarantees the existence of ˜c ∈ IRL ψ (πE ). Elsewhere in the paper, as mentioned in Section 2, we assume the IRL problem has a solution.) To show Proposition 3.2, we need the basic result that the set of valid occupancy measures D , {ρπ : π ∈ Π} can be written as a feasible set of affine constraints [ 19 ]: if p0(s) is the distribution of starting states and P (s′|s, a ) is the dynamics model, then D =

{

ρ : ρ ≥ 0 and ∑ 

> a

ρ(s, a ) = p0(s) + γ ∑ 

> s′,a

P (s|s′, a )ρ(s′, a ) ∀ s ∈ S 

}

.Furthermore, there is a one-to-one correspondence between Π and D:

Lemma 3.1 (Theorem 2 of Syed et al. [27] ). If ρ ∈ D , then ρ is the occupancy measure for 

πρ(a|s) , ρ(s, a )/ ∑ 

> a′

ρ(s, a ′), and πρ is the only policy whose occupancy measure is ρ.

We are therefore justified in writing πρ to denote the unique policy for an occupancy measure ρ. We also need a lemma that lets us speak about causal entropies of occupancy measures: 

Lemma 3.2. Let ¯H(ρ) = − ∑ 

> s,a

ρ(s, a ) log( ρ(s, a )/ ∑ 

> a′

ρ(s, a ′)) . Then, ¯H is strictly concave, and for all π ∈ Π and ρ ∈ D , we have H(π) = ¯H(ρπ ) and ¯H(ρ) = H(πρ).

The proof of this lemma is in Appendix A.1. Lemma 3.1 and Lemma 3.2 together allow us to freely switch between policies and occupancy measures when considering functions involving causal entropy and expected costs, as in the following lemma: 

Lemma 3.3. If L(π, c ) = −H(π) + Eπ [c(s, a )] and ¯L(ρ, c ) = − ¯H(ρ) + ∑ 

> s,a

ρ(s, a )c(s, a ), then, for all cost functions c, L(π, c ) = ¯L(ρπ , c ) for all policies π ∈ Π, and ¯L(ρ, c ) = L(πρ, c ) for all occupancy measures ρ ∈ D .

Now, we are ready to verify Proposition 3.2. 

Proof of Proposition 3.2. Define ¯L(ρ, c ) = − ¯H(ρ) + ∑ 

> s,a

c(s, a )( ρ(s, a ) − ρE (s, a )) . Given that 

ψ is a constant function, we have the following, due to Lemma 3.3: 

˜c ∈ IRL ψ (πE ) = arg max 

> c∈RS×A

min  

> π∈Π

−H(π) + Eπ [c(s, a )] − EπE [c(s, a )] + const . (5) 

= arg max 

> c∈RS×A

min  

> ρ∈D

− ¯H(ρ) + ∑

> s,a

ρ(s, a )c(s, a ) − ∑

> s,a

ρE (s, a )c(s, a ) = arg max 

> c∈RS×A

min 

> ρ∈D

¯L(ρ, c ). (6) 3This is the dual of the optimization problem 

minimize  

> ρ∈D

− ¯H(ρ) subject to ρ(s, a ) = ρE (s, a ) ∀ s ∈ S , a ∈ A (7) with Lagrangian ¯L, for which the costs c(s, a ) serve as dual variables for equality constraints. Thus, 

˜c is a dual optimum for (7). In addition, strong duality holds for (7): D is compact and convex, − ¯H

is convex, and, since ρE > 0, there exists a feasible point in the relative interior of the domain D.Moreover, Lemma 3.2 guarantees that − ¯H is in fact strictly convex, so the primal optimum can be uniquely recovered from the dual optimum [ 4, Section 5.5.5] via ˜ρ = arg min ρ∈D ¯L(ρ, ˜c) = arg min ρ∈D − ¯H(ρ) + ∑ 

> s,a

˜c(s, a )ρ(s, a ) = ρE , where the first equality indicates that ˜ρ is the unique minimizer of ¯L(·, ˜c), and the third follows from the constraints in the primal problem (7). But if ˜π ∈ RL(˜ c), then Lemma 3.3 implies ρ˜π = ˜ ρ = ρE .Let us summarize our conclusions. First, IRL is a dual of an occupancy measure matching problem , and the recovered cost function is the dual optimum. Classic IRL algorithms that solve reinforcement learning repeatedly in an inner loop, such as the algorithm of Ziebart et al. [29] that runs a variant of value iteration in an inner loop, can be interpreted as a form of dual ascent, in which one repeatedly solves the primal problem (reinforcement learning) with fixed dual values (costs). Dual ascent is effective if solving the unconstrained primal is efficient, but in the case of IRL, it amounts to reinforcement learning! Second, the induced optimal policy is the primal optimum. 

The induced optimal policy is obtained by running RL after IRL, which is exactly the act of recovering the primal optimum from the dual optimum; that is, optimizing the Lagrangian with the dual variables fixed at the dual optimum values. Strong duality implies that this induced optimal policy is indeed the primal optimum, and therefore matches occupancy measures with the expert. IRL is traditionally defined as the act of finding a cost function such that the expert policy is uniquely optimal, but we can alternatively view IRL as a procedure that tries to induce a policy that matches the expert’s occupancy measure .

## 4 Practical occupancy measure matching 

We saw in Proposition 3.2 that if ψ is constant, the resulting primal problem (7) simply matches occupancy measures with expert at all states and actions. Such an algorithm is not practically useful. In reality, the expert trajectory distribution will be provided only as a finite set of samples, so in large environments, most of the expert’s occupancy measure values will be small, and exact occupancy measure matching will force the learned policy to rarely visit these unseen state-action pairs simply due to lack of data. Furthermore, in the cases in which we would like to use function approximation to learn parameterized policies πθ , the resulting optimization problem of finding an appropriate θ would have an intractably large number of constraints when the environment is large: as many constraints as points in S × A .Keeping in mind that we wish to eventually develop an imitation learning algorithm suitable for large environments, we would like to relax Eq. (7) into the following form, motivated by Proposition 3.1: 

minimize  

> π

dψ (ρπ , ρ E ) − H(π) (8) by modifying the IRL regularizer ψ so that dψ (ρπ , ρ E ) , ψ∗(ρπ − ρE ) smoothly penalizes violations in difference between the occupancy measures. 

Entropy-regularized apprenticeship learning It turns out that with certain settings of ψ, Eq. (8) takes on the form of regularized variants of existing apprenticeship learning algorithms, which indeed do scale to large environments with parameterized policies [ 10 ]. For a class of cost functions 

C ⊂ RS×A , an apprenticeship learning algorithm finds a policy that performs better than the expert across C, by optimizing the objective 

minimize  

> π

max  

> c∈C

Eπ [c(s, a )] − EπE [c(s, a )] (9) Classic apprenticeship learning algorithms restrict C to convex sets given by linear combinations of basis functions f1, . . . , f d, which give rise a feature vector f (s, a ) = [ f1(s, a ), . . . , f d(s, a )] for each state-action pair. Abbeel and Ng [1] and Syed et al. [27] use, respectively, 

Clinear = {∑

> i

wifi : ‖w‖2 ≤ 1} and Cconvex = {∑

> i

wifi : ∑

> i

wi = 1 , w i ≥ 0 ∀i} . (10) 4Clinear leads to feature expectation matching [ 1], which minimizes `2 distance between expected feature vectors: max c∈C linear Eπ [c(s, a )] −EπE [c(s, a )] = ‖Eπ [f (s, a )] −EπE [f (s, a )] ‖2. Meanwhile, 

Cconvex leads to MWAL [ 26 ] and LPAL [ 27 ], which minimize worst-case excess cost among the individual basis functions, as max c∈C convex Eπ [c(s, a )] − EπE [c(s, a )] = max i∈{ 1,...,d } Eπ [fi(s, a )] −

EπE [fi(s, a )] .We now show how Eq. (9) is a special case of Eq. (8) with a certain setting of ψ. With the indicator function δC : RS×A → R, defined by δC (c) = 0 if c ∈ C and +∞ otherwise, we can write the apprenticeship learning objective (9) as 

max  

> c∈C

Eπ [c(s, a )] −EπE [c(s, a )] = max 

> c∈RS×A

−δC (c) + ∑

> s,a

(ρπ (s, a )−ρπE(s, a )) c(s, a ) = δ∗C (ρπ −ρπE)

Therefore, we see that entropy-regularized apprenticeship learning 

minimize  

> π

−H(π) + max  

> c∈C

Eπ [c(s, a )] − EπE [c(s, a )] (11) is equivalent to performing RL following IRL with cost regularizer ψ = δC , which forces the implicit IRL procedure to recover a cost function lying in C. Note that we can scale the policy’s entropy regularization strength in Eq. (11) by scaling C by a constant α as {αc : c ∈ C} , recovering the original apprenticeship objective (9) by taking α → ∞ .

Cons of apprenticeship learning It is known that apprenticeship learning algorithms generally do not recover expert-like policies if C is too restrictive [ 27 , Section 1]—which is often the case for the linear subspaces used by feature expectation matching, MWAL, and LPAL, unless the basis functions 

f1, . . . , f d are very carefully designed. Intuitively, unless the true expert cost function (assuming it exists) lies in C, there is no guarantee that if π performs better than πE on all of C, then π equals πE .With the aforementioned insight based on Proposition 3.1 that apprenticeship learning is equivalent to RL following IRL, we can understand exactly why apprenticeship learning may fail to imitate: it forces πE to be encoded as an element of C. If C does not include a cost function that explains expert behavior well, then attempting to recover a policy from such an encoding will not succeed. 

Pros of apprenticeship learning While restrictive cost classes C may not lead to exact imitation, apprenticeship learning with such C can scale to large state and action spaces with policy function approximation. Ho et al. [10] rely on the following policy gradient formula for the apprenticeship objective (9) for a parameterized policy πθ :

∇θ max  

> c∈C

Eπθ [c(s, a )] − EπE [c(s, a )] = ∇θ Eπθ [c∗(s, a )] = Eπθ [∇θ log πθ (a|s)Qc∗ (s, a )] 

where c∗ = arg max 

> c∈C

Eπθ [c(s, a )] − EπE [c(s, a )] , Q c∗ (¯ s, ¯a) = Eπθ [c∗(¯ s, ¯a) | s0 = ¯ s, a 0 = ¯ a] (12) Observing that Eq. (12) is the policy gradient for a reinforcement learning objective with cost c∗, Ho et al. propose an algorithm that alternates between two steps: 1. Sample trajectories of the current policy πθi by simulating in the environment, and fit a cost function c∗ 

> i

, as defined in Eq. (12). For the cost classes Clinear and Cconvex (10), this cost fitting amounts to evaluating simple analytical expressions [10]. 2. Form a gradient estimate with Eq. (12) with c∗ 

> i

and the sampled trajectories, and take a trust region policy optimization (TRPO) [24] step to produce πθi+1 .This algorithm relies crucially on the TRPO policy step, which is a natural gradient step constrained to ensure that πθi+1 does not stray too far πθi , as measured by KL divergence between the two policies averaged over the states in the sampled trajectories. This carefully constructed step scheme ensures that the algorithm does not diverge due to high noise in estimating the gradient (12). We refer the reader to Schulman et al. [24] for more details on TRPO. With the TRPO step scheme, Ho et al. were able train large neural network policies for apprentice-ship learning with linear cost function classes (10) in environments with hundreds of observation dimensions. Their use of these linear cost function classes, however, limits their approach to settings in which expert behavior is well-described by such classes. We will draw upon their algorithm to develop an imitation learning method that both scales to large environments and imitates arbitrarily complex expert behavior. To do so, we first turn to proposing a new regularizer ψ that wields more expressive power than the regularizers corresponding to Clinear and Cconvex (10). 55 Generative adversarial imitation learning 

As discussed in Section 4, the constant regularizer leads to an imitation learning algorithm that exactly matches occupancy measures, but is intractable in large environments. The indicator regularizers for the linear cost function classes (10), on the other hand, lead to algorithms incapable of exactly matching occupancy measures without careful tuning, but are tractable in large environments. We propose the following new cost regularizer that combines the best of both worlds, as we will show in the coming sections: 

ψGA (c) ,

{EπE [g(c(s, a ))] if c < 0+∞ otherwise where g(x) = 

{−x − log(1 − ex) if x < 0+∞ otherwise (13) This regularizer places low penalty on cost functions c that assign an amount of negative cost to expert state-action pairs; if c, however, assigns large costs (close to zero, which is the upper bound for costs feasible for ψGA ) to the expert, then ψGA will heavily penalize c. An interesting property of 

ψGA is that it is an average over expert data, and therefore can adjust to arbitrary expert datasets. The indicator regularizers δC , used by the linear apprenticeship learning algorithms described in Section 4, are always fixed, and cannot adapt to data as ψGA can. Perhaps the most important difference between 

ψGA and δC , however, is that δC forces costs to lie in a small subspace spanned by finitely many basis functions, whereas ψGA allows for any cost function, as long as it is negative everywhere. Our choice of ψGA is motivated by the following fact, shown in the appendix (Corollary A.1.1): 

ψ∗

> GA

(ρπ − ρπE ) = sup 

> D∈(0 ,1) S×A

Eπ [log( D(s, a ))] + EπE [log(1 − D(s, a ))] (14) where the supremum ranges over discriminative classifiers D : S × A → (0 , 1) . Equation (14) is pro-portional to the optimal negative log loss of the binary classification problem of distinguishing between state-action pairs of π and πE . It turns out that this optimal loss is, up to a constant shift and scaling, the Jensen-Shannon divergence DJS (¯ ρπ , ¯ρπE ) , DKL (¯ ρπ ‖(¯ ρπ + ¯ ρE )/2) + DKL (¯ ρE ‖(¯ ρπ + ¯ ρE )/2) ,which is a squared metric between the normalized occupancy distributions ¯ρπ = (1 − γ)ρπ and 

¯ρπE = (1 − γ)ρπE [8 , 17 ]. Treating the causal entropy H as a policy regularizer controlled by λ ≥ 0

and dropping the 1 − γ occupancy measure normalization for clarity, we obtain a new imitation learning algorithm: 

minimize  

> π

ψ∗

> GA

(ρπ − ρπE ) − λH (π) = DJS (ρπ , ρ πE ) − λH (π), (15) which finds a policy whose occupancy measure minimizes Jensen-Shannon divergence to the expert’s. Equation (15) minimizes a true metric between occupancy measures, so, unlike linear apprenticeship learning algorithms, it can imitate expert policies exactly. 

Algorithm Equation (15) draws a connection between imitation learning and generative adversarial networks [ 8], which train a generative model G by having it confuse a discriminative classifier 

D. The job of D is to distinguish between the distribution of data generated by G and the true data distribution. When D cannot distinguish data generated by G from the true data, then G has successfully matched the true data. In our setting, the learner’s occupancy measure ρπ is analogous to the data distribution generated by G, and the expert’s occupancy measure ρπE is analogous to the true data distribution. We now present a practical imitation learning algorithm, called generative adversarial imitation learning or GAIL (Algorithm 1), designed to work in large environments. GAIL solves Eq. (15) by finding a saddle point (π, D ) of the expression 

Eπ [log( D(s, a ))] + EπE [log(1 − D(s, a ))] − λH (π) (16) with both π and D represented using function approximators: GAIL fits a parameterized policy 

πθ , with weights θ, and a discriminator network Dw : S × A → (0 , 1) , with weights w. GAIL alternates between an Adam [ 11 ] gradient step on w to increase Eq. (16) with respect to D, and a TRPO step on θ to decrease Eq. (16) with respect to π (we derive an estimator for the causal entropy gradient ∇θ H(πθ ) in Appendix A.2). The TRPO step serves the same purpose as it does with the apprenticeship learning algorithm of Ho et al. [10] : it prevents the policy from changing too much due to noise in the policy gradient. The discriminator network can be interpreted as a local cost function providing learning signal to the policy—specifically, taking a policy step that decreases expected cost with respect to the cost function c(s, a ) = log D(s, a ) will move toward expert-like regions of state-action space, as classified by the discriminator. 6Algorithm 1 Generative adversarial imitation learning  

> 1:

Input: Expert trajectories τE ∼ πE , initial policy and discriminator parameters θ0, w 0 

> 2:

for i = 0 , 1, 2, . . . do  

> 3:

Sample trajectories τi ∼ πθi 

> 4:

Update the discriminator parameters from wi to wi+1 with the gradient 

ˆEτi [∇w log( Dw(s, a ))] + ˆEτE [∇w log(1 − Dw(s, a ))] (17)  

> 5:

Take a policy step from θi to θi+1 , using the TRPO rule with cost function log( Dwi+1 (s, a )) .Specifically, take a KL-constrained natural gradient step with 

ˆEτi [∇θ log πθ (a|s)Q(s, a )] − λ∇θ H(πθ ),

where Q(¯ s, ¯a) = ˆEτi [log( Dwi+1 (s, a )) | s0 = ¯ s, a 0 = ¯ a] (18)  

> 6:

end for 

## 6 Experiments 

We evaluated GAIL against baselines on 9 physics-based control tasks, ranging from low-dimensional control tasks from the classic RL literature—the cartpole [ 2], acrobot [ 7], and mountain car [ 15 ]—to difficult high-dimensional tasks such as a 3D humanoid locomotion, solved only recently by model-free reinforcement learning [ 25 , 24 ]. All environments, other than the classic control tasks, were simulated with MuJoCo [28]. See Appendix B for a complete description of all the tasks. Each task comes with a true cost function, defined in the OpenAI Gym [ 5]. We first generated expert behavior for these tasks by running TRPO [ 24 ] on these true cost functions to create expert policies. Then, to evaluate imitation performance with respect to sample complexity of expert data, we sampled datasets of varying trajectory counts from the expert policies. The trajectories constituting each dataset each consisted of about 50 state-action pairs. We tested GAIL against three baselines: 1. Behavioral cloning: a given dataset of state-action pairs is split into 70% training data and 30% validation data. The policy is trained with supervised learning, using Adam [11] with minibatches of 128 examples, until validation error stops decreasing. 2. Feature expectation matching (FEM): the algorithm of Ho et al. [10] using the cost function class Clinear (10) of Abbeel and Ng [1] 3. Game-theoretic apprenticeship learning (GTAL): the algorithm of Ho et al. [10] using the cost function class Cconvex (10) of Syed and Schapire [26] We used all algorithms to train policies of the same neural network architecture for all tasks: two hidden layers of 100 units each, with tanh nonlinearities in between. The discriminator networks for GAIL also used the same architecture. All networks were always initialized randomly at the start of each trial. For each task, we gave FEM, GTAL, and GAIL exactly the same amount of environment interaction for training. We ran all algorithms 5-7 times over different random seeds in all environments except Humanoid, due to time restrictions. Figure 1 depicts the results, and Appendix B provides exact performance numbers and details of our experiment pipeline, including expert data sampling and algorithm hyperparameters. We found that on the classic control tasks (cartpole, acrobot, and mountain car), behavioral cloning generally suffered in expert data efficiency compared to FEM and GTAL, which for the most part were able produce policies with near-expert performance with a wide range of dataset sizes, albeit with large variance over different random initializations of the policy. On these tasks, GAIL consistently produced policies performing better than behavioral cloning, FEM, and GTAL. However, behavioral cloning performed excellently on the Reacher task, on which it was more sample efficient than GAIL. We were able to slightly improve GAIL’s performance on Reacher using causal entropy regularization—in the 4-trajectory setting, the improvement from λ = 0 to λ = 10 −3 was statistically significant over training reruns, according to a one-sided Wilcoxon rank-sum test with p = .05 . We used no causal entropy regularization for all other tasks. 71 4 7 10 0.0 0.2 0.4 0.6 0.8 1.0                     

> Cartpole
> 14710 0.0 0.2 0.4 0.6 0.8 1.0
> Acrobot
> 14710 0.0 0.2 0.4 0.6 0.8 1.0
> Mountain Car
> 411 18 25 0.0 0.2 0.4 0.6 0.8 1.0
> HalfCheetah
> 411 18 25 0.0 0.2 0.4 0.6 0.8 1.0
> Hopper
> 411 18 25 0.0 0.2 0.4 0.6 0.8 1.0
> Walker
> 411 18 25 −1.0 −0.5 0.0 0.5 1.0
> Ant
> 80 160 240 0.0 0.2 0.4 0.6 0.8 1.0
> Humanoid
> Number of trajectories in dataset Performance (scaled)
> Expert Random Behavioral cloning
> FEM GTAL
> GAIL (ours)

(a) 4 11 18 −0.5 0.0 0.5 1.0 

Reacher     

> Number of trajectories in dataset Performance (scaled)
> Expert Random Behavioral cloning GAIL ( ¸= 0 )
> GAIL ( ¸= 10 ¡3)GAIL ( ¸= 10 ¡2)

(b) 

Figure 1: (a) Performance of learned policies. The y-axis is negative cost, scaled so that the expert achieves 1 and a random policy achieves 0. (b) Causal entropy regularization λ on Reacher. Except for Humanoid, shading indicates standard deviation over 5-7 reruns. On the other MuJoCo environments, GAIL almost always achieved at least 70% of expert performance for all dataset sizes we tested and reached it exactly with the larger datasets, with very little variance among random seeds. The baseline algorithms generally could not reach expert performance even with the largest datasets. FEM and GTAL performed poorly for Ant, producing policies consistently worse than a policy that chooses actions uniformly at random. Behavioral cloning was able to reach satisfactory performance with enough data on HalfCheetah, Hopper, Walker, and Ant, but was unable to achieve more than 60% for Humanoid, on which GAIL achieved exact expert performance for all tested dataset sizes. 

## 7 Discussion and outlook 

As we demonstrated, GAIL is generally quite sample efficient in terms of expert data. However, it is not particularly sample efficient in terms of environment interaction during training. The number of such samples required to estimate the imitation objective gradient (18) was comparable to the number needed for TRPO to train the expert policies from reinforcement signals. We believe that we could significantly improve learning speed for GAIL by initializing policy parameters with behavioral cloning, which requires no environment interaction at all. Fundamentally, our method is model free, so it will generally need more environment interaction than model-based methods. Guided cost learning [ 6], for instance, builds upon guided policy search [ 12 ]and inherits its sample efficiency, but also inherits its requirement that the model is well-approximated by iteratively fitted time-varying linear dynamics. Interestingly, both GAIL and guided cost learning alternate between policy optimization steps and cost fitting (which we called discriminator fitting), even though the two algorithms are derived completely differently. Our approach builds upon a vast line of work on IRL [ 29 , 1 , 27 , 26 ], and hence, just like IRL, our approach does not interact with the expert during training. Our method explores randomly to determine which actions bring a policy’s occupancy measure closer to the expert’s, whereas methods that do interact with the expert, like DAgger [ 22 ], can simply ask the expert for such actions. Ultimately, we believe that a method that combines well-chosen environment models with expert interaction will win in terms of sample complexity of both expert data and environment interaction. 

Acknowledgments 

We thank Jayesh K. Gupta, John Schulman, and the anonymous reviewers for assistance, advice, and critique. This work was supported by the SAIL-Toyota Center for AI Research and by a NSF Graduate Research Fellowship (grant no. DGE-114747). 8References 

[1] P. Abbeel and A. Y. Ng. Apprenticeship learning via inverse reinforcement learning. In Proceedings of the 21st International Conference on Machine Learning , 2004. [2] A. G. Barto, R. S. Sutton, and C. W. Anderson. Neuronlike adaptive elements that can solve difficult learning control problems. Systems, Man and Cybernetics, IEEE Transactions on , (5):834–846, 1983. [3] M. Bloem and N. Bambos. Infinite time horizon maximum causal entropy inverse reinforcement learning. In Decision and Control (CDC), 2014 IEEE 53rd Annual Conference on , pages 4911–4916. IEEE, 2014. [4] S. Boyd and L. Vandenberghe. Convex optimization . Cambridge university press, 2004. [5] G. Brockman, V. Cheung, L. Pettersson, J. Schneider, J. Schulman, J. Tang, and W. Zaremba. OpenAI Gym. arXiv preprint arXiv:1606.01540 , 2016. [6] C. Finn, S. Levine, and P. Abbeel. Guided cost learning: Deep inverse optimal control via policy optimization. In Proceedings of the 33rd International Conference on Machine Learning , 2016. [7] A. Geramifard, C. Dann, R. H. Klein, W. Dabney, and J. P. How. Rlpy: A value-function-based reinforce-ment learning framework for education and research. JMLR , 2015. [8] I. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. Warde-Farley, S. Ozair, A. Courville, and Y. Bengio. Generative adversarial nets. In NIPS , pages 2672–2680, 2014. [9] J.-B. Hiriart-Urruty and C. Lemaréchal. Convex Analysis and Minimization Algorithms , volume 305. Springer, 1996. [10] J. Ho, J. K. Gupta, and S. Ermon. Model-free imitation learning with policy optimization. In Proceedings of the 33rd International Conference on Machine Learning , 2016. [11] D. Kingma and J. Ba. Adam: A method for stochastic optimization. arXiv preprint arXiv:1412.6980 , 2014. [12] S. Levine and P. Abbeel. Learning neural network policies with guided policy search under unknown dynamics. In Advances in Neural Information Processing Systems , pages 1071–1079, 2014. [13] S. Levine and V. Koltun. Continuous inverse optimal control with locally optimal examples. In Proceedings of the 29th International Conference on Machine Learning , pages 41–48, 2012. [14] S. Levine, Z. Popovic, and V. Koltun. Nonlinear inverse reinforcement learning with gaussian processes. In Advances in Neural Information Processing Systems , pages 19–27, 2011. [15] A. W. Moore and T. Hall. Efficient memory-based learning for robot control. 1990. [16] A. Y. Ng and S. Russell. Algorithms for inverse reinforcement learning. In ICML , 2000. [17] X. Nguyen, M. J. Wainwright, and M. I. Jordan. On surrogate loss functions and f-divergences. The Annals of Statistics , pages 876–904, 2009. [18] D. A. Pomerleau. Efficient training of artificial neural networks for autonomous navigation. Neural Computation , 3(1):88–97, 1991. [19] M. L. Puterman. Markov decision processes: discrete stochastic dynamic programming . John Wiley & Sons, 2014. [20] N. D. Ratliff, D. Silver, and J. A. Bagnell. Learning to search: Functional gradient techniques for imitation learning. Autonomous Robots , 27(1):25–53, 2009. [21] S. Ross and D. Bagnell. Efficient reductions for imitation learning. In AISTATS , pages 661–668, 2010. [22] S. Ross, G. J. Gordon, and D. Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In AISTATS , pages 627–635, 2011. [23] S. Russell. Learning agents for uncertain environments. In Proceedings of the Eleventh Annual Conference on Computational Learning Theory , pages 101–103. ACM, 1998. [24] J. Schulman, S. Levine, P. Abbeel, M. Jordan, and P. Moritz. Trust region policy optimization. In 

Proceedings of The 32nd International Conference on Machine Learning , pages 1889–1897, 2015. [25] J. Schulman, P. Moritz, S. Levine, M. Jordan, and P. Abbeel. High-dimensional continuous control using generalized advantage estimation. arXiv preprint arXiv:1506.02438 , 2015. [26] U. Syed and R. E. Schapire. A game-theoretic approach to apprenticeship learning. In Advances in Neural Information Processing Systems , pages 1449–1456, 2007. [27] U. Syed, M. Bowling, and R. E. Schapire. Apprenticeship learning using linear programming. In 

Proceedings of the 25th International Conference on Machine Learning , pages 1032–1039, 2008. [28] E. Todorov, T. Erez, and Y. Tassa. Mujoco: A physics engine for model-based control. In Intelligent Robots and Systems (IROS), 2012 IEEE/RSJ International Conference on , pages 5026–5033. IEEE, 2012. [29] B. D. Ziebart, A. Maas, J. A. Bagnell, and A. K. Dey. Maximum entropy inverse reinforcement learning. In AAAI , AAAI’08, 2008. [30] B. D. Ziebart, J. A. Bagnell, and A. K. Dey. Modeling interaction via the principle of maximum causal entropy. In ICML , pages 1255–1262, 2010. 

9