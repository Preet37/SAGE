# Source: https://www.ri.cmu.edu/pub_files/2011/4/Ross-AISTATS11-NoRegret.pdf
# Title: A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning (DAgger)
# Fetched via: jina
# Date: 2026-04-09

Title: Ross-AISTATS11-NoRegret.pdf



Number of Pages: 9

# A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning 

Stéphane Ross Geoffrey J. Gordon J. Andrew Bagnell 

Robotics Institute Carnegie Mellon University Pittsburgh, PA 15213, USA stephaneross@cmu.edu Machine Learning Department Carnegie Mellon University Pittsburgh, PA 15213, USA ggordon@cs.cmu.edu Robotics Institute Carnegie Mellon University Pittsburgh, PA 15213, USA dbagnell@ri.cmu.edu 

## Abstract 

Sequential prediction problems such as imitation learning, where future observations depend on previous predictions (actions), violate the com-mon i.i.d. assumptions made in statistical learn-ing. This leads to poor performance in theory and often in practice. Some recent approaches (Daumé III et al., 2009; Ross and Bagnell, 2010) provide stronger guarantees in this setting, but re-main somewhat unsatisfactory as they train either non-stationary or stochastic policies and require a large number of iterations. In this paper, we propose a new iterative algorithm, which trains a stationary deterministic policy, that can be seen as a no regret algorithm in an online learning set-ting. We show that any such no regret algorithm, combined with additional reduction assumptions, must find a policy with good performance under the distribution of observations it induces in such sequential settings. We demonstrate that this new approach outperforms previous approaches on two challenging imitation learning problems and a benchmark sequence labeling problem. 

## 1 INTRODUCTION 

Sequence Prediction problems arise commonly in practice. For instance, most robotic systems must be able to pre-dict/make a sequence of actions given a sequence of obser-vations revealed to them over time. In complex robotic sys-tems where standard control methods fail, we must often resort to learning a controller that can make such predic-tions. Imitation learning techniques, where expert demon-    

> Appearing in Proceedings of the 14 th International Conference on Artificial Intelligence and Statistics (AISTATS) 2011, Fort Laud-erdale, FL, USA. Volume 15 of JMLR: W&CP 15. Copyright 2011 by the authors.

strations of good behavior are used to learn a controller, have proven very useful in practice and have led to state-of-the art performance in a variety of applications (Schaal, 1999; Abbeel and Ng, 2004; Ratliff et al., 2006; Silver et al., 2008; Argall et al., 2009; Chernova and Veloso, 2009; Ross and Bagnell, 2010). A typical approach to imitation learning is to train a classifier or regressor to predict an ex-pert’s behavior given training data of the encountered ob-servations (input) and actions (output) performed by the ex-pert. However since the learner’s prediction affects future input observations/states during execution of the learned policy, this violate the crucial i.i.d. assumption made by most statistical learning approaches. Ignoring this issue leads to poor performance both in the-ory and practice (Ross and Bagnell, 2010). In particular, a classifier that makes a mistake with probability  under the distribution of states/observations encountered by the expert can make as many as T 2 mistakes in expectation over T -steps under the distribution of states the classifier itself induces (Ross and Bagnell, 2010). Intuitively this is because as soon as the learner makes a mistake, it may en-counter completely different observations than those under expert demonstration, leading to a compounding of errors. Recent approaches (Ross and Bagnell, 2010) can guarantee an expected number of mistakes linear (or nearly so) in the task horizon T and error  by training over several itera-tions and allowing the learner to influence the input states where expert demonstration is provided (through execution of its own controls in the system). One approach (Ross and Bagnell, 2010) learns a non-stationary policy by training a different policy for each time step in sequence, starting from the first step. Unfortunately this is impractical when 

T is large or ill-defined. Another approach called SMILe (Ross and Bagnell, 2010), similar to SEARN (Daumé III et al., 2009) and CPI (Kakade and Langford, 2002), trains a stationary stochastic policy (a finite mixture of policies) by adding a new policy to the mixture at each iteration of training. However this may be unsatisfactory for practical applications as some policies in the mixture are worse than A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning 

others and the learned controller may be unstable. We propose a new meta-algorithm for imitation learning which learns a stationary deterministic policy guaranteed to perform well under its induced distribution of states (number of mistakes/costs that grows linearly in T and classification cost ). We take a reduction-based approach (Beygelzimer et al., 2005) that enables reusing existing su-pervised learning algorithms. Our approach is simple to implement, has no free parameters except the supervised learning algorithm sub-routine, and requires a number of iterations that scales nearly linearly with the effective hori-zon of the problem. It naturally handles continuous as well as discrete predictions. Our approach is closely related to no regret online learning algorithms (Cesa-Bianchi et al., 2004; Hazan et al., 2006; Kakade and Shalev-Shwartz, 2008) (in particular Follow-The-Leader ) but better lever-ages the expert in our setting. Additionally, we show that any no-regret learner can be used in a particular fashion to learn a policy that achieves similar guarantees. We begin by establishing our notation and setting, discuss related work, and then present the DA GGER (Dataset Ag-gregation) method. We analyze this approach using a no-regret and a reduction approach (Beygelzimer et al., 2005). Beyond the reduction analysis, we consider the sample complexity of our approach using online-to-batch (Cesa-Bianchi et al., 2004) techniques. We demonstrate DA GGER 

is scalable and outperforms previous approaches in practice on two challenging imitation learning problems: 1) learn-ing to steer a car in a 3D racing game ( Super Tux Kart ) and 2) and learning to play Super Mario Bros. , given input im-age features and corresponding actions by a human expert and near-optimal planner respectively. Following Daumé III et al. (2009) in treating structured prediction as a de-generate imitation learning problem, we apply DA GGER to the OCR (Taskar et al., 2003) benchmark prediction prob-lem achieving results competitive with the state-of-the-art (Taskar et al., 2003; Ratliff et al., 2007; Daumé III et al., 2009) using only single-pass, greedy prediction. 

## 2 PRELIMINARIES 

We begin by introducing notation relevant to our setting. We denote by Π the class of policies the learner is consid-ering and T the task horizon. For any policy π, we let dtπ

denote the distribution of states at time t if the learner exe-cuted policy π from time step 1 to t − 1. Furthermore, we denote dπ = 1

> T

∑Tt=1 dtπ the average distribution of states if we follow policy π for T steps. Given a state s, we de-note C(s, a ) the expected immediate cost of performing ac-tion a in state s for the task we are considering and denote 

Cπ (s) = Ea∼π(s)[C(s, a )] the expected immediate cost of 

π in s. We assume C is bounded in [0 , 1] . The total cost of executing policy π for T -steps ( i.e. , the cost-to-go) is denoted J(π) = ∑Tt=1 Es∼dtπ [Cπ (s)] = T Es∼dπ [Cπ (s)] .In imitation learning, we may not necessarily know or ob-serve true costs C(s, a ) for the particular task. Instead, we observe expert demonstrations and seek to bound J(π)

for any cost function C based on how well π mimics the expert’s policy π∗. Denote ` the observed surrogate loss function we minimize instead of C. For instance `(s, π )

may be the expected 0-1 loss of π with respect to π∗ in state s, or a squared/hinge loss of π with respect to π∗ in s.Importantly, in many instances, C and ` may be the same function– for instance, if we are interested in optimizing the learner’s ability to predict the actions chosen by an expert. Our goal is to find a policy ˆπ which minimizes the observed surrogate loss under its induced distribution of states, i.e.: 

ˆπ = arg min 

> π∈Π

Es∼dπ [`(s, π )] (1) As system dynamics are assumed both unknown and com-plex, we cannot compute dπ and can only sample it by exe-cuting π in the system. Hence this is a non-i.i.d. supervised learning problem due to the dependence of the input distri-bution on the policy π itself. The interaction between pol-icy and the resulting distribution makes optimization diffi-cult as it results in a non-convex objective even if the loss 

`(s, ·) is convex in π for all states s. We now briefly review previous approaches and their guarantees. 

2.1 Supervised Approach to Imitation 

The traditional approach to imitation learning ignores the change in distribution and simply trains a policy π that per-forms well under the distribution of states encountered by the expert dπ∗ . This can be achieved using any standard supervised learning algorithm. It finds the policy ˆπsup :

ˆπsup = arg min 

> π∈Π

Es∼dπ∗ [`(s, π )] (2) Assuming `(s, π ) is the 0-1 loss (or upper bound on the 0-1 loss) implies the following performance guarantee with respect to any task cost function C bounded in [0 , 1] :

Theorem 2.1. (Ross and Bagnell, 2010) Let 

Es∼dπ∗ [`(s, π )] = , then J(π) ≤ J(π∗) + T 2.Proof. Follows from result in Ross and Bagnell (2010) since  is an upper bound on the 0-1 loss of π in dπ∗ .Note that this bound is tight, i.e. there exist problems such that a policy π with  0-1 loss on dπ∗ can incur ex-tra cost that grows quadratically in T . Kääriäinen (2006) demonstrated this in a sequence prediction setting 1 and                   

> 1In their example, an error rate of  > 0when trained to predict the next output in sequence with the previous correct output as input can lead to an expected number of mistakes of
> T
> 2−1−(1 −2)T+1
> 4+12over sequences of length Tat test time. This is bounded by T2and behaves as Θ( T2)for small .Stéphane Ross, Geoffrey J. Gordon, J. Andrew Bagnell

Ross and Bagnell (2010) provided an imitation learning ex-ample where J(ˆ πsup ) = (1 − T )J(π∗) + T 2. Hence the traditional supervised learning approach has poor perfor-mance guarantees due to the quadratic growth in T . Instead we would prefer approaches that can guarantee growth lin-ear or near-linear in T and . The following two approaches from Ross and Bagnell (2010) achieve this on some classes of imitation learning problems, including all those where surrogate loss ` upper bounds C.

2.2 Forward Training 

The forward training algorithm introduced by Ross and Bagnell (2010) trains a non-stationary policy (one policy 

πt for each time step t) iteratively over T iterations, where at iteration t, πt is trained to mimic π∗ on the distribution of states at time t induced by the previously trained poli-cies π1, π 2, . . . , π t−1. By doing so, πt is trained on the actual distribution of states it will encounter during exe-cution of the learned policy. Hence the forward algorithm guarantees that the expected loss under the distribution of states induced by the learned policy matches the average loss during training, and hence improves performance. We here provide a theorem slightly more general than the one provided by Ross and Bagnell (2010) that applies to any policy π that can guarantee  surrogate loss under its own distribution of states. This will be useful to bound the performance of our new approach presented in Section 3. Let Qπ′ 

> t

(s, π ) denote the t-step cost of executing π in initial state s and then following policy π′ and assume `(s, π ) is the 0-1 loss (or an upper bound on the 0-1 loss), then we have the following performance guarantee with respect to any task cost function C bounded in [0 , 1] :

Theorem 2.2. Let π be such that Es∼dπ [`(s, π )] = , and 

Qπ∗ 

> T−t+1

(s, a ) − Qπ∗ 

> T−t+1

(s, π ∗) ≤ u for all action a, t ∈{1, 2, . . . , T }, dtπ (s) > 0, then J(π) ≤ J(π∗) + uT  .Proof. We here follow a similar proof to Ross and Bagnell (2010). Given our policy π, consider the policy π1: t, which executes π in the first t-steps and then execute the expert 

π∗. Then 

J(π)= J(π∗) + ∑T −1 

> t=0

[J(π1: T −t) − J(π1: T −t−1)] = J(π∗) + ∑Tt=1 Es∼dtπ [Qπ∗ 

> T−t+1

(s, π ) − Qπ∗ 

> T−t+1

(s, π ∗)] 

≤ J(π∗) + u ∑Tt=1 Es∼dtπ [`(s, π )] = J(π∗) + uT  

The inequality follows from the fact that `(s, π ) upper bounds the 0-1 loss, and hence the probability π and π∗

pick different actions in s; when they pick different actions, the increase in cost-to-go ≤ u.In the worst case, u could be O(T ) and the forward al-gorithm wouldn’t provide any improvement over the tra-ditional supervised learning approach. However, in many cases u is O(1) or sub-linear in T and the forward algo-rithm leads to improved performance. For instance if C is the 0-1 loss with respect to the expert, then u ≤ 1. Addi-tionally if π∗ is able to recover from mistakes made by π, in the sense that within a few steps, π∗ is back in a distribution of states that is close to what π∗ would be in if π∗ had been executed initially instead of π, then u will be O(1) . 2 Adrawback of the forward algorithm is that it is impractical when T is large (or undefined) as we must train T different policies sequentially and cannot stop the algorithm before we complete all T iterations. Hence it can not be applied to most real-world applications. 

2.3 Stochastic Mixing Iterative Learning 

SMILe, proposed by Ross and Bagnell (2010), alleviates this problem and can be applied in practice when T is large or undefined by adopting an approach similar to SEARN (Daumé III et al., 2009) where a stochastic sta-tionary policy is trained over several iterations. Initially SMILe starts with a policy π0 which always queries and executes the expert’s action choice. At iteration n, a pol-icy ˆπn is trained to mimic the expert under the distribu-tion of trajectories πn−1 induces and then updates πn =

πn−1 + α(1 − α)n−1(ˆ πn − π0). This update is interpreted as adding probability α(1 − α)n−1 to executing policy ˆπn

at any step and removing probability α(1 − α)n−1 of ex-ecuting the queried expert’s action. At iteration n, πn is a mixture of n policies and the probability of using the queried expert’s action is (1 − α)n. We can stop the al-gorithm at any iteration N by returning the re-normalized policy ˜πN = πN −(1 −α)N π0 

> 1−(1 −α)N

which doesn’t query the expert anymore. Ross and Bagnell (2010) showed that choosing 

α in O( 1  

> T2

) and N in O(T 2 log T ) guarantees near-linear regret in T and  for some class of problems. 

## 3 DATASET AGGREGATION 

We now present DA GGER (Dataset Aggregation), an it-erative algorithm that trains a deterministic policy that achieves good performance guarantees under its induced distribution of states. In its simplest form, the algorithm proceeds as follows. At the first iteration, it uses the expert’s policy to gather a dataset of trajectories D and train a policy ˆπ2 that best mimics the expert on those trajectories. Then at iteration 

n, it uses ˆπn to collect more trajectories and adds those trajectories to the dataset D. The next policy ˆπn+1 is the policy that best mimics the expert on the whole dataset D.          

> 2This is the case for instance in Markov Desision Processes (MDPs) when the Markov Chain defined by the system dynamics and policy π∗is rapidly mixing. In particular, if it is α-mixing with exponential decay rate δthen uis O(11−exp( −δ)).A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning

Initialize D ← ∅ .Initialize ˆπ1 to any policy in Π.

for i = 1 to N do 

Let πi = βiπ∗ + (1 − βi)ˆ πi.Sample T -step trajectories using πi.Get dataset Di = {(s, π ∗(s)) } of visited states by πi

and actions given by expert. Aggregate datasets: D ← D ⋃ Di.Train classifier ˆπi+1 on D.

end for Return best ˆπi on validation. 

Algorithm 3.1: DA GGER Algorithm. In other words, DA GGER proceeds by collecting a dataset at each iteration under the current policy and trains the next policy under the aggregate of all collected datasets. The in-tuition behind this algorithm is that over the iterations, we are building up the set of inputs that the learned policy is likely to encounter during its execution based on previous experience (training iterations). This algorithm can be in-terpreted as a Follow-The-Leader algorithm in that at itera-tion n we pick the best policy ˆπn+1 in hindsight, i.e. under all trajectories seen so far over the iterations. To better leverage the presence of the expert in our imita-tion learning setting, we optionally allow the algorithm to use a modified policy πi = βiπ∗ + (1 − βi)ˆ πi at iteration 

i that queries the expert to choose controls a fraction of the time while collecting the next dataset. This is often desir-able in practice as the first few policies, with relatively few datapoints, may make many more mistakes and visit states that are irrelevant as the policy improves. We will typically use β1 = 1 so that we do not have to spec-ify an initial policy ˆπ1 before getting data from the expert’s behavior. Then we could choose βi = pi−1 to have a prob-ability of using the expert that decays exponentially as in SMILe and SEARN. We show below the only requirement is that {βi} be a sequence such that βN = 1

> N

∑Ni=1 βi → 0

as N → ∞ . The simple, parameter-free version of the al-gorithm described above is the special case βi = I(i = 1) 

for I the indicator function, which often performs best in practice (see Section 5). The general DA GGER algorithm is detailed in Algorithm 3.1. The main result of our analysis in the next section is the following guarantee for DA GGER .Let π1: N denote the sequence of policies π1, π 2, . . . , π N .Assume ` is strongly convex and bounded over Π. Suppose 

βi ≤ (1 − α)i−1 for all i for some constant α independent of T . Let N = min π∈Π 1

> N

∑Ni=1 Es∼dπi [`(s, π )] be the true loss of the best policy in hindsight. Then the following holds in the infinite sample case (infinite number of sample trajectories at each iteration): 

Theorem 3.1. For DA GGER , if N is ˜O(T ) there exists a policy ˆπ ∈ ˆπ1: N s.t. Es∼dˆπ [`(s, ˆπ)] ≤ N + O(1 /T )

In particular, this holds for the policy ˆπ =arg min π∈ˆπ1: N Es∼dπ [`(s, π )] . 3 If the task cost function C corresponds to (or is upper bounded by) the surrogate loss ` then this bound tells us directly that 

J(ˆ π) ≤ T  N + O(1) . For arbitrary task cost function C,then if ` is an upper bound on the 0-1 loss with respect to 

π∗, combining this result with Theorem 2.2 yields that: 

Theorem 3.2. For DA GGER , if N is ˜O(uT ) there exists a policy ˆπ ∈ ˆπ1: N s.t. J(ˆ π) ≤ J(π∗) + uT  N + O(1) .

Finite Sample Results In the finite sample case, sup-pose we sample m trajectories with πi at each it-eration i, and denote this dataset Di. Let ˆN =min π∈Π 1

> N

∑Ni=1 Es∼Di [`(s, π )] be the training loss of the best policy on the sampled trajectories, then using Azuma-Hoeffding’s inequality leads to the following guarantee: 

Theorem 3.3. For DA GGER , if N is O(T 2 log(1 /δ )) and 

m is O(1) then with probability at least 1 − δ there exists a policy ˆπ ∈ ˆπ1: N s.t. Es∼dˆπ [`(s, ˆπ)] ≤ ˆN + O(1 /T )

A more refined analysis taking advantage of the strong con-vexity of the loss function (Kakade and Tewari, 2009) may lead to tighter generalization bounds that require N only of order ˜O(T log(1 /δ )) . Similarly: 

Theorem 3.4. For DA GGER , if N is O(u2T 2 log(1 /δ )) 

and m is O(1) then with probability at least 1 − δ there exists a policy ˆπ ∈ ˆπ1: N s.t. J(ˆ π) ≤ J(π∗)+ uT ˆN +O(1) .

## 4 THEORETICAL ANALYSIS 

The theoretical analysis of DA GGER only relies on the no-regret property of the underlying Follow-The-Leader algo-rithm on strongly convex losses (Kakade and Tewari, 2009) which picks the sequence of policies ˆπ1: N . Hence the pre-sented results also hold for any other no regret online learn-ing algorithm we would apply to our imitation learning set-ting. In particular, we can consider the results here a re-duction of imitation learning to no-regret online learning where we treat mini-batches of trajectories under a single policy as a single online-learning example. We first briefly review concepts of online learning and no regret that will be used for this analysis. 

4.1 Online Learning 

In online learning, an algorithm must provide a policy πn at iteration n which incurs a loss `n(πn). After observing this loss, the algorithm can provide a different policy πn+1 for the next iteration which will incur loss `n+1 (πn+1 ). The     

> 3It is not necessary to find the best policy in the sequence that minimizes the loss under its distribution; the same guarantee holds for the policy which uniformly randomly picks one policy in the sequence ˆπ1: Nand executes that policy for Tsteps.

Stéphane Ross, Geoffrey J. Gordon, J. Andrew Bagnell 

loss functions `n+1 may vary in an unknown or even adver-sarial fashion over time. A no-regret algorithm is an algo-rithm that produces a sequence of policies π1, π 2, . . . , π N

such that the average regret with respect to the best policy in hindsight goes to 0 as N goes to ∞:

1

N

> N

∑

> i=1

`i(πi) − min 

> π∈Π

1

N

> N

∑

> i=1

`i(π) ≤ γN (3) for lim N →∞ γN = 0 . Many no-regret algorithms guar-antee that γN is ˜O( 1 

> N

) (e.g. when ` is strongly convex) (Hazan et al., 2006; Kakade and Shalev-Shwartz, 2008; Kakade and Tewari, 2009). 

4.2 No Regret Algorithms Guarantees 

Now we show that no-regret algorithms can be used to find a policy which has good performance guarantees under its own distribution of states in our imitation learning setting. To do so, we must choose the loss functions to be the loss under the distribution of states of the current policy chosen by the online algorithm: `i(π) = Es∼dπi [`(s, π )] .For our analysis of DA GGER , we need to bound the to-tal variation distance between the distribution of states en-countered by ˆπi and πi, which continues to call the expert. The following lemma is useful: 

Lemma 4.1. || dπi − dˆπi || 1 ≤ 2T β i.Proof. Let d the distribution of states over T steps condi-tioned on πi picking π∗ at least once over T steps. Since πi

always executes ˆπi over T steps with probability (1 − βi)T

we have dπi = (1 − βi)T dˆπi + (1 − (1 − βi)T )d. Thus 

|| dπi − dˆπi || 1

= (1 − (1 − βi)T )|| d − dˆπi || 1

≤ 2(1 − (1 − βi)T )

≤ 2T β i

The last inequality follows from the fact that (1 − β)T ≥

1 − βT for any β ∈ [0 , 1] .This is only better than the trivial bound || dπi − dˆπi || 1 ≤ 2

for βi ≤ 1 

> T

. Assume βi is non-increasing and define 

nβ the largest n ≤ N such that βn > 1 

> T

. Let N =min π∈Π 1

> N

∑Ni=1 Es∼dπi [`(s, π )] the loss of the best pol-icy in hindsight after N iterations and let `max be an upper bound on the loss, i.e. `i(s, ˆπi) ≤ `max for all policies ˆπi,and state s such that dˆπi (s) > 0. We have the following: 

Theorem 4.1. For DA GGER , there exists a policy ˆπ ∈

ˆπ1: N s.t. Es∼dˆπ [`(s, ˆπ)] ≤ N + γN + 2`max  

> N

[nβ +

T ∑Ni=nβ +1 βi], for γN the average regret of ˆπ1: N .Proof. The last lemma implies Es∼dˆπi (`i(s, ˆπi)) ≤

Es∼dπi (`i(s, ˆπi)) + 2`max min(1 , T β i). Then: 

min ˆπ∈ˆπ1: N Es∼dˆπ [`(s, ˆπ)] 

≤ 1

> N

∑Ni=1 Es∼dˆπi (`(s, ˆπi)) 

≤ 1

> N

∑Ni=1 [Es∼dπi (`(s, ˆπi)) + 2 `max min(1 , T β i)] 

≤ γN + 2`max  

> N

[nβ + T ∑Ni=nβ +1 βi] + min π∈Π

∑Ni=1 `i(π)= γN + N + 2`max  

> N

[nβ + T ∑Ni=nβ +1 βi]

Under an error reduction assumption that for any input dis-tribution, there is some policy π ∈ Π that achieves sur-rogate loss of , this implies we are guaranteed to find a policy ˆπ which achieves  surrogate loss under its own state distribution in the limit, provided βN → 0. For in-stance, if we choose βi to be of the form (1 − α)i−1, then  

> 1
> N

[nβ + T ∑Ni=nβ +1 βi] ≤ 1 

> N α

[log T + 1] and this extra penalty becomes negligible for N as ˜O(T ). As we need at least ˜O(T ) iterations to make γN negligible, the num-ber of iterations required by DA GGER is similar to that re-quired by any no-regret algorithm. Note that this is not as strong as the general error or regret reductions consid-ered in (Beygelzimer et al., 2005; Ross and Bagnell, 2010; Daumé III et al., 2009) which require only classification: we require a no-regret method or strongly convex surrogate loss function, a stronger (albeit common) assumption. 

Finite Sample Case: The previous results hold if the on-line learning algorithm observes the infinite sample loss, i.e. the loss on the true distribution of trajectories induced by the current policy πi. In practice however the algorithm would only observe its loss on a small sample of trajecto-ries at each iteration. We wish to bound the true loss under its own distribution of the best policy in the sequence as a function of the regret on the finite sample of trajectories. At each iteration i, we assume the algorithm samples m

trajectories using πi and then observes the loss `i(π) = 

Es∼Di (`(s, π )) , for Di the dataset of those m trajectories. The online learner guarantees 1

> N

∑Ni=1 Es∼Di (`(s, π i)) −

min π∈Π 1

> N

∑Ni=1 Es∼Di (`(s, π )) ≤ γN . Let ˆN =min π∈Π 1

> N

∑Ni=1 Es∼Di [`(s, π )] the training loss of the best policy in hindsight. Following a similar analysis to Cesa-Bianchi et al. (2004), we obtain: 

Theorem 4.2. For DA GGER , with probability at least 1−δ,there exists a policy ˆπ ∈ ˆπ1: N s.t. Es∼dˆπ [`(s, ˆπ)] ≤ ˆN +

γN + 2`max  

> N

[nβ + T ∑Ni=nβ +1 βi] + `max 

√ 2 log(1 /δ ) 

> mN

, for 

γN the average regret of ˆπ1: N .Proof. Let Yij be the difference between the expected per step loss of ˆπi under state distribution dπi and the aver-age per step loss of ˆπi under the jth sample trajectory with πi at iteration i. The random variables Yij over all 

i ∈ {1, 2, . . . , N } and j ∈ {1, 2, . . . , m } are all zero mean, bounded in [−`max , ` max ] and form a martingale (considering the order Y11 , Y 12 , . . . , Y 1m, Y 21 , . . . , Y N m ). By Azuma-Hoeffding’s inequality 1

> mN

∑Ni=1 

∑mj=1 Yij ≤A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning 

`max 

√ 2 log(1 /δ ) 

> mN

with probability at least 1 − δ. Hence, we obtain that with probability at least 1 − δ:

min ˆπ∈ˆπ1: N Es∼dˆπ [`(s, ˆπ)] 

≤ 1

> N

∑Ni=1 Es∼dˆπi [`(s, ˆπi)] 

≤ 1

> N

∑Ni=1 Es∼dπi [`(s, ˆπi)] + 2`max  

> N

[nβ + T ∑Ni=nβ +1 βi]= 1

> N

∑Ni=1 Es∼Di [`(s, ˆπi)] + 1

> mN

∑Ni=1 

∑mj=1 Yij 

+ 2`max  

> N

[nβ + T ∑Ni=nβ +1 βi]

≤ 1

> N

∑Ni=1 Es∼Di [`(s, ˆπi)] + `max 

√ 2 log(1 /δ )

> mN

+ 2`max  

> N

[nβ + T ∑Ni=nβ +1 βi]

≤ ˆN + γN + `max 

√ 2 log(1 /δ ) 

> mN

+ 2`max  

> N

[nβ + T ∑Ni=nβ +1 βi]

The use of Azuma-Hoeffding’s inequality suggests we need 

N m in O(T 2 log(1 /δ )) for the generalization error to be 

O(1 /T ) and negligible over T steps. Leveraging the strong convexity of ` as in (Kakade and Tewari, 2009) may lead to a tighter bound requiring only O(T log( T /δ )) trajectories. 

## 5 EXPERIMENTS 

To demonstrate the efficacy and scalability of DA GGER , we apply it to two challenging imitation learning problems and a sequence labeling task (handwriting recognition). 

5.1 Super Tux Kart 

Super Tux Kart is a 3D racing game similar to the popular Mario Kart. Our goal is to train the computer to steer the kart moving at fixed speed on a particular race track, based on the current game image features as input (see Figure 1). A human expert is used to provide demonstrations of the correct steering (analog joystick value in [-1,1]) for each of the observed game images. For all methods, we use a linear 

Figure 1: Image from Super Tux Kart’s Star Track. controller as the base learner which updates the steering at 5Hz based on the vector of image features 4.

> 4

Features x: LAB color values of each pixel in a 25x19 re-sized image of the 800x600 image; output steering: ˆy = wT x + b

where w, b minimizes ridge regression objective: L(w, b ) =

> 1
> n

Pni=1 (wT xi + b − yi)2 + λ 

> 2

wT w, for regularizer λ = 10 −3.

We compare performance on a race track called Star Track. As this track floats in space, the kart can fall off the track at any point (the kart is repositioned at the center of the track when this occurs). We measure performance in terms of the average number of falls per lap. For SMILe and DA GGER ,we used 1 lap of training per iteration ( ∼1000 data points) and run both methods for 20 iterations. For SMILe we choose parameter α = 0 .1 as in Ross and Bagnell (2010), and for DA GGER the parameter βi = I(i = 1) for I the in-dicator function. Figure 2 shows 95% confidence intervals on the average falls per lap of each method after 1, 5, 10, 15 and 20 iterations as a function of the total number of train-ing data collected. We first observe that with the baseline 0 0.5 1 1.5 2 2.5 x 10 4  

> 0
> 0.5
> 1
> 1.5
> 2
> 2.5
> 3
> 3.5
> 4
> 4.5
> Number of Training Data Average Falls Per Lap
> DAgger ( βi= I(i=1))
> SMILe ( α= 0.1)
> Supervised

Figure 2: Average falls/lap as a function of training data. supervised approach where training always occurs under the expert’s trajectories that performance does not improve as more data is collected. This is because most of the train-ing laps are all very similar and do not help the learner to learn how to recover from mistakes it makes. With SMILe we obtain some improvements but the policy after 20 iter-ations still falls off the track about twice per lap on aver-age. This is in part due to the stochasticity of the policy which sometimes makes bad choices of actions. For DA G-

> GER

, we were able to obtain a policy that never falls off the track after 15 iterations of training. Though even after 5 iterations, the policy we obtain almost never falls off the track and is significantly outperforming both SMILe and the baseline supervised approach. Furthermore, the policy obtained by DA GGER is smoother and looks qualitatively better than the policy obtained with SMILe. A video avail-able on YouTube (Ross, 2010a) shows a qualitative com-parison of the behavior obtained with each method. 

5.2 Super Mario Bros. 

Super Mario Bros. is a platform video game where the character, Mario, must move across each stage by avoid-Stéphane Ross, Geoffrey J. Gordon, J. Andrew Bagnell 

ing being hit by enemies and falling into gaps, and before running out of time. We used the simulator from a recent Mario Bros. AI competition (Togelius and Karakovskiy, 2009) which can randomly generate stages of varying diffi-culty (more difficult gaps and types of enemies). Our goal is to train the computer to play this game based on the cur-rent game image features as input (see Figure 3). Our ex-pert in this scenario is a near-optimal planning algorithm that has full access to the game’s internal state and can simulate exactly the consequence of future actions. An ac-tion consists of 4 binary variables indicating which subset of buttons we should press in {left,right,jump,speed }. For 

Figure 3: Captured image from Super Mario Bros. all methods, we use 4 independent linear SVM as the base learner which update the 4 binary actions at 5Hz based on the vector of image features 5.We compare performance in terms of the average distance travelled by Mario per stage before dying, running out of time or completing the stage, on randomly generated stages of difficulty 1 with a time limit of 60 seconds to complete the stage. The total distance of each stage varies but is around 4200-4300 on average, so performance can vary roughly in [0,4300]. Stages of difficulty 1 are fairly easy for an average human player but contain most types of en-emies and gaps, except with fewer enemies and gaps than stages of harder difficulties. We compare performance of DAgger, SMILe and SEARN 6 to the supervised approach (Sup). With each approach we collect 5000 data points per iteration (each stage is about 150 data points if run to com-pletion) and run the methods for 20 iterations. For SMILe we choose parameter α = 0 .1 (Sm0.1) as in Ross and Bag-

> 5

For the input features x: each image is discretized in a grid of 22x22 cells centered around Mario; 14 binary features de-scribe each cell (types of ground, enemies, blocks and other spe-cial items); a history of those features over the last 4 images is used, in addition to other features describing the last 6 actions and the state of Mario (small,big,fire,touches ground), for a to-tal of 27152 binary features (very sparse). The kth output binary variable ˆyk = I(wTk x + bk > 0) , where wk , b k optimizes the SVM objective with regularizer λ = 10 −4 using stochastic gradi-ent descent (Ratliff et al., 2007; Bottou, 2009). 

> 6

We use the same cost-to-go approximation in Daumé III et al. (2009); in this case SMILe and SEARN differs only in how the weights in the mixture are updated at each iteration. 

nell (2010). For DA GGER we obtain results with differ-ent choice of the parameter βi: 1) βi = I(i = 1) for I

the indicator function (D0); 2) βi = pi−1 for all values of p ∈ { 0.1, 0.2, . . . , 0.9}. We report the best results ob-tained with p = 0 .5 (D0.5). We also report the results with 

p = 0 .9 (D0.9) which shows the slower convergence of using the expert more frequently at later iterations. Simi-larly for SEARN, we obtain results with all choice of α in 

{0.1, 0.2, . . . , 1}. We report the best results obtained with 

α = 0 .4 (Se0.4). We also report results with α = 1 .0

(Se1), which shows the unstability of such a pure policy iteration approach. Figure 4 shows 95% confidence inter-vals on the average distance travelled per stage at each it-eration as a function of the total number of training data collected. Again here we observe that with the supervised 0 1 2 3 4 5 6 7 8 9 10 x 10 4      

> 1000
> 1200
> 1400
> 1600
> 1800
> 2000
> 2200
> 2400
> 2600
> 2800
> 3000
> 3200
> Number of Training Data Average Distance Travelled Per Stage
> D0 D0.5 D0.9 Se1 Se0.4 Sm0.1 Sup

Figure 4: Average distance/stage as a function of data. approach, performance stagnates as we collect more data from the expert demonstrations, as this does not help the particular errors the learned controller makes. In particu-lar, a reason the supervised approach gets such a low score is that under the learned controller, Mario is often stuck at some location against an obstacle instead of jumping over it. Since the expert always jumps over obstacles at a sig-nificant distance away, the controller did not learn how to get unstuck in situations where it is right next to an ob-stacle. On the other hand, all the other iterative methods perform much better as they eventually learn to get unstuck in those situations by encountering them at the later iter-ations. Again in this experiment, DA GGER outperforms SMILe, and also outperforms SEARN for all choice of α

we considered. When using βi = 0 .9i−1, convergence is significantly slower could have benefited from more itera-tions as performance was still improving at the end of the 20 iterations. Choosing 0.5i−1 yields slightly better per-formance (3030) then with the indicator function (2980). This is potentially due to the large number of data gener-ated where mario is stuck at the same location in the early iterations when using the indicator; whereas using the ex-A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning 

pert a small fraction of the time still allows to observe those locations but also unstucks mario and makes it collect a wider variety of useful data. A video available on YouTube (Ross, 2010b) also shows a qualitative comparison of the behavior obtained with each method. 

5.3 Handwriting Recognition 

Finally, we demonstrate the efficacy of our approach on a structured prediction problem involving recognizing hand-written words given the sequence of images of each charac-ter in the word. We follow Daumé III et al. (2009) in adopt-ing a view of structured prediction as a degenerate form of imitation learning where the system dynamics are deter-ministic and trivial in simply passing on earlier predictions made as inputs for future predictions. We use the dataset of Taskar et al. (2003) which has been used extensively in the literature to compare several structured prediction ap-proaches. This dataset contains roughly 6600 words (for a total of over 52000 characters) partitioned in 10 folds. We consider the large dataset experiment which consists of training on 9 folds and testing on 1 fold and repeating this over all folds. Performance is measured in terms of the character accuracy on the test folds. We consider predicting the word by predicting each charac-ter in sequence in a left to right order, using the previously predicted character to help predict the next and a linear SVM 7, following the greedy SEARN approach in Daumé III et al. (2009). Here we compare our method to SMILe, as well as SEARN (using the same approximations used in Daumé III et al. (2009)). We also compare these ap-proaches to two baseline, a non-structured approach which simply predicts each character independently and the su-pervised training approach where training is conducted with the previous character always correctly labeled. Again we try all choice of α ∈ { 0.1, 0.2, . . . , 1} for SEARN, and report results for α = 0 .1, α = 1 (pure policy iteration) and the best α = 0 .8, and run all approaches for 20 itera-tions. Figure 5 shows the performance of each approach on the test folds after each iteration as a function of training data. The baseline result without structure achieves 82% character accuracy by just using an SVM that predicts each character independently. When adding the previous charac-ter feature, but training with always the previous character correctly labeled (supervised approach), performance in-creases up to 83.6%. Using DAgger increases performance further to 85.5%. Surprisingly, we observe SEARN with 

α = 1 , which is a pure policy iteration approach performs very well on this experiment, similarly to the best α = 0 .8

and DAgger. Because there is only a small part of the in-put that is influenced by the current policy (the previous 

> 7

Each character is 8x16 binary pixels (128 input features); 26 binary features are used to encode the previously predicted let-ter in the word. We train the multiclass SVM using the all-pairs reduction to binary classification (Beygelzimer et al., 2005). 0 2 4 6 8 10 12 14 16 18 20 

> 0.81
> 0.815
> 0.82
> 0.825
> 0.83
> 0.835
> 0.84
> 0.845
> 0.85
> 0.855
> 0.86
> Training Iteration Test Folds Character Accuracy
> DAgger ( βi=I(i=1))
> SEARN ( α=1)
> SEARN ( α=0.8)
> SEARN ( α=0.1)
> SMILe ( α=0.1)
> Supervised
> No Structure

Figure 5: Character accuracy as a function of iteration. predicted character feature) this makes this approach not as unstable as in general reinforcement/imitation learning problems (as we saw in the previous experiment). SEARN and SMILe with small α = 0 .1 performs similarly but sig-nificantly worse than DAgger. Note that we chose the sim-plest (greedy, one-pass) decoding to illustrate the benefits of the DAGGER approach with respect to existing reduc-tions. Similar techniques can be applied to multi-pass or beam-search decoding leading to results that are competi-tive with the state-of-the-art. 

## 6 FUTURE WORK 

We show that by batching over iterations of interaction with a system, no-regret methods, including the presented DA GGER approach can provide a learning reduction with strong performance guarantees in both imitation learning and structured prediction. In future work, we will consider more sophisticated strategies than simple greedy forward decoding for structured prediction, as well as using base classifiers that rely on Inverse Optimal Control (Abbeel and Ng, 2004; Ratliff et al., 2006) techniques to learn a cost function for a planner to aid prediction in imitation learn-ing. Further we believe techniques similar to those pre-sented, by leveraging a cost-to-go estimate, may provide an understanding of the success of online methods for rein-forcement learning and suggest a similar data-aggregation method that can guarantee performance in such settings. 

Acknowledgements 

This work is supported by the ONR MURI grant N00014-09-1-1052, Reasoning in Reduced Information Spaces, and by the National Sciences and Engineering Research Coun-cil of Canada (NSERC). Stéphane Ross, Geoffrey J. Gordon, J. Andrew Bagnell 

## References 

P. Abbeel and A. Y. Ng. Apprenticeship learning via in-verse reinforcement learning. In Proceedings of the 21st International Conference on Machine Learning (ICML) ,2004. B. D. Argall, S. Chernova, M. Veloso, and B. Browning. A survey of robot learning from demonstration. Robotics and Autonomous Systems , 2009. A. Beygelzimer, V. Dani, T. Hayes, J. Langford, and B. Zadrozny. Error limiting reductions between classi-fication tasks. In Proceedings of the 22nd International Conference on Machine Learning (ICML) , 2005. L. Bottou. sgd code, 2009. URL http://www.leon. bottou.org/projects/sgd .N. Cesa-Bianchi, A. Conconi, and C. Gentile. On the gen-eralization ability of on-line learning algorithms. 2004. S. Chernova and M. Veloso. Interactive policy learning through confidence-based autonomy. 2009. H. Daumé III, J. Langford, and D. Marcu. Search-based structured prediction. Machine Learning , 2009. E. Hazan, A. Kalai, S. Kale, and A. Agarwal. Logarith-mic regret algorithms for online convex optimization. In 

Proceedings of the 19th annual conference on Computa-tional Learning Theory (COLT) , 2006. M. Kääriäinen. Lower bounds for reductions, 2006. Atomic Learning workshop. S. Kakade and J. Langford. Approximately optimal ap-proximate reinforcement learning. In Proceedings of the 19th International Conference on Machine Learning (ICML) , 2002. S. Kakade and S. Shalev-Shwartz. Mind the duality gap: Logarithmic regret algorithms for online optimization. In Advances in Neural Information Processing Systems (NIPS) , 2008. S. Kakade and A. Tewari. On the generalization abil-ity of online strongly convex programming algorithms. In Advances in Neural Information Processing Systems (NIPS) , 2009. N. Ratliff, D. Bradley, J. A. Bagnell, and J. Chestnutt. Boosting structured prediction for imitation learning. In Advances in Neural Information Processing Systems (NIPS) , 2006. N. Ratliff, J. A. Bagnell, and M. Zinkevich. (Online) sub-gradient methods for structured prediction. In Proceed-ings of the International Conference on Artificial Intelli-gence and Statistics (AISTATS) , 2007. S. Ross. Comparison of imitation learning approaches on Super Tux Kart, 2010a. URL http://www. youtube.com/watch?v=V00npNnWzSU .S. Ross. Comparison of imitation learning approaches on Super Mario Bros, 2010b. URL http://www. youtube.com/watch?v=anOI0xZ3kGM .S. Ross and J. A. Bagnell. Efficient reductions for imita-tion learning. In Proceedings of the 13th International Conference on Artificial Intelligence and Statistics (AIS-TATS) , 2010. S. Schaal. Is imitation learning the route to humanoid robots? In Trends in Cognitive Sciences , 1999. D. Silver, J. A. Bagnell, and A. Stentz. High performance outdoor navigation from overhead data using imitation learning. In Proceedings of Robotics Science and Sys-tems (RSS) , 2008. B. Taskar, C. Guestrin, and D. Koller. Max margin markov networks. In Advances in Neural Information Processing Systems (NIPS) , 2003. J. Togelius and S. Karakovskiy. Mario AI Competition, 2009. URL http://julian.togelius.com/ mariocompetition2009 .