# Source: http://proceedings.mlr.press/v54/fruit17a/fruit17a-supp.pdf
# Author: Stephane Ross,&nbsp;Geoffrey Gordon,&nbsp;Drew Bagnell
# Author Slug: stephane-ross-nbsp-geoffrey-gordon-nbsp-drew-bagnell
# Title: Exploration–Exploitation in MDPs with Options (supplement)
# Fetched via: jina
# Date: 2026-04-10

Title: fruit17a-supp.pdf



Number of Pages: 34

# Exploration–Exploitation in MDPs with Options 

Ronan Fruit Alessandro Lazaric 

Inria Lille - SequeL Team Inria Lille - SequeL Team 

## Abstract 

While a large body of empirical results show that temporally-extended actions and op-tions may significantly affect the learning per-formance of an agent, the theoretical under-standing of how and when options can be beneficial in online reinforcement learning is relatively limited. In this paper, we derive an upper and lower bound on the regret of a variant of UCRL using options. While we first analyze the algorithm in the general case of semi-Markov decision processes (SMDPs), we show how these results can be translated to the specific case of MDPs with options and we illustrate simple scenarios in which the re-gret of learning with options can be provably 

much smaller than the regret suffered when learning with primitive actions. 

## 1 Introduction 

The option framework [Sutton et al., 1999] is a simple yet powerful model to introduce temporally-extended actions and hierarchical structures in reinforcement learning (RL) [Sutton and Barto, 1998]. An important feature of this framework is that Markov decision pro-cess (MDP) planning and learning algorithms can be easily extended to accommodate options, thus obtain-ing algorithms such as option value iteration and Q-learning [Sutton et al., 1999], LSTD [Sorg and Singh, 2010], and actor-critic [Bacon and Precup, 2015]. Temporally extended actions are particularly useful in high dimensional problems that naturally decom-pose into a hierarchy of subtasks. For instance, Tessler et al. [2016] recently obtained promising re-sults by combining options and deep learning for life-long learning in the challenging domain of Minecraft. A large body of the literature has then focused on   

> Appearing in Proceedings of the 20 th International Con-ference on Artificial Intelligence and Statistics (AISTATS) 2017, Fort Lauderdale, Florida, USA. JMLR: W&CP vol-ume 54. Copyright 2017 by the authors.

how to automatically construct options that are bene-ficial to the learning process within a single task or across similar tasks (see e.g., [McGovern and Barto, 2001, Menache et al., 2002, Şimşek and Barto, 2004, Castro and Precup, 2012, Levy and Shimkin, 2011]). An alternative approach is to design an initial set of op-tions and optimize it during the learning process itself (see e.g., interrupting options Mann et al. 2014 and op-tions with exceptions Sairamesh and Ravindran 2012). Despite the empirical evidence of the effectiveness of most of these methods, it is well known that options may as well worsen the performance w.r.t. learning with primitive actions [Jong et al., 2008]. Moreover, most of the proposed methods are heuristic in nature and the theoretical understanding of the actual im-pact of options on the learning performance is still fairly limited. Notable exceptions are the recent re-sults of Mann and Mannor [2014] and Brunskill and Li [2014]. Nonetheless, Mann and Mannor [2014] rather focus on a batch setting and they derive a sample complexity analysis of approximate value iteration with options. Furthermore, the PAC-SMDP analysis of Brunskill and Li [2014] describes the performance in SMDPs but it cannot be immediately translated into a sample complexity of learning with options in MDPs. In this paper, we consider the case where a fixed set of options is provided and we study their impact on the learning performance w.r.t. learning without op-tions. In particular, we derive the first regret analy-sis of learning with options. Relying on the fact that using options in an MDP induces a semi-Markov deci-sion process (SMDP), we first introduce a variant of the UCRL algorithm [Jaksch et al., 2010] for SMDPs and we upper- and lower-bound its regret (sections 3 and 4). While this result is of independent interest for learning in SMDPs, its most interesting aspect is that it can be translated into a regret bound for learn-ing with options in MDPs and it provides a first un-derstanding on the conditions sufficient for a set of options to reduce the regret w.r.t. learning with prim-itive actions (Sect. 5). Finally, we provide an illustra-tive example where the empirical results support the theoretical findings (Sect. 6). Exploration–Exploitation in MDPs with Options 

## 2 Preliminaries 

MDPs and options. A finite MDP is a tuple 

M = {S, A, p, r } where S is a finite set of states, A

is a finite set of actions, p(s′|s, a ) is the probability of transitioning from state s to state s′ when action a is taken, r(s, a, s ′) is a distribution over rewards obtained when action a is taken in state s and the next state is s′. A stationary deterministic policy π : S → A 

maps states to actions. A (Markov) option is a tu-ple o = {Io, β o, π o

} where Io ⊂ S is the set of states where the option can be initiated, βo : S → [0 , 1] is the probability distribution that the option ends in a given state, and πo : S → A is the policy followed until the option ends. Whenever the set of primitive actions 

A is replaced by a set of options O, the resulting deci-sion process is no longer an MDP but it belongs to the family of semi-Markov decision processes (SMDP). 

Proposition 1. [Sutton et al. 1999] For any MDP M

and a set of options O, the resulting decision process is an SMDP MO = {SO , O, p O, r O , τ O

}, where SO ⊆ S 

is the set of states where options can start and end, 

SO =

(

∪o∈O Io

) ⋃ ( 

∪o∈O {s : βo(s) > 0}

)

,

O is the set of available actions, pO (s, o, s ′) is the prob-ability of transition from s to s′ by taking the policy πo

associated to option o, i.e., 

pO (s, o, s ′) = 

> ∞

∑

> k=1

p(sk = s′|s, π o)βo(s′),

where p(sk = s′|s, π o) is the probability of reach-ing state s′ after exactly k steps following policy πo,

rO (s, o, s ′) is the distribution of the cumulative reward obtained by executing option o from state s until inter-ruption at s′, and τO(s, o, s ′) is the distribution of the holding time (i.e., number of primitive steps executed to go from s to s′ by following πo). 

Throughout the rest of the paper, we only consider an “admissible” set of options O such that all options ter-minate in finite time with probability 1 and in all possi-ble terminal states there exists at least one option that can start, i.e., ∪o∈O {s : βo(s) > 0} ⊆ ∪ o∈O Io. This also implies that the resulting SMDP MO is communi-cating whenever the original MDP M is communicat-ing. Finally, we notice that a stationary deterministic policy constructed on a set of options O may result into a non-stationary policy on the set of actions A.

Learning in SMDPs. Relying on this mapping, we first study the exploration-exploitation trade-off in a generic SMDP. A thorough discussion on the impli-cations of the analysis of learning in SMDPs for the case of learning with options in MDPs is reported in Sect. 5. For any SMDP M = {S, A, p, r, τ },we denote by τ (s, a, s ′) (resp. r(s, a, s ′)) the ex-pectation of τ (s, a, s ′) (resp. r(s, a, s ′)) and by 

τ (s, a ) = ∑  

> s′∈S

τ (s, a, s ′)p(s′|s, a ) (resp. r(s, a ) = ∑ 

> s′∈S

r(s, a, s ′)p(s′|s, a )) the expected holding time (resp. cumulative reward) of action a from state s.In the next proposition we define the average-reward performance criterion and we recall the properties of the optimal policy in SMDPs. 

Proposition 2. Denote N (t) = sup {n ∈

N, ∑ni=1 τi ≤ t} the number of decision steps that occurred before time t. For any policy π and s ∈ S :

ρπ (s) def 

= lim sup 

> t→+∞

Eπ

[ ∑ N (t) 

> i=1

ri

t

∣∣∣∣s0 = s

]

ρπ (s) def 

= lim inf  

> t→+∞

Eπ

[ ∑ N (t) 

> i=1

ri

t

∣∣∣∣s0 = s

]

.

(1) 

If M is communicating and the expected holding times and reward are finite, there exists a stationary deter-ministic optimal policy π∗ such that for all states s and policies π, ρπ∗

(s) ≥ ρπ (s) and ρπ∗

(s) = ρπ∗

(s) = ρ∗.

Finally, we recall the average reward optimality equa-tion for a communicating SMDP 

u∗(s) = max 

> a∈A

{

r(s, a ) − ρ∗τ (s, a ) (2) 

+ ∑ 

> s′∈S

p(s′|s, a )u∗(s′)

}

,

where u∗ and ρ∗ are the bias (up to a constant) and the gain of the optimal policy π∗.We are now ready to consider the learning problem. For any i ∈ N∗, ai denotes the action taken by the agent at the i-th decision step 1 and si denotes the state reached after ai is taken, with s0 being the initial state. We denote by (ri(s, a, s ′)) i∈N∗ (resp. 

(τi(s, a, s ′)) i∈N∗ ) a sequence of i.i.d. realizations from distribution r(s, a, s ′) (resp. τ (s, a, s ′)). When the learner explores the SMDP, it observes the sequence 

(s0, . . . , s i, a i+1 , r i+1 (si, a i+1 , s i+1 ), τ i+1 (si, a i+1 , s i+1 ),. . . ). The performance of a learning algorithm is mea-sured in terms of its cumulative regret .

Definition 1. For any SMDP M , any starting state 

s ∈ S , and any number of decision steps n ≥ 1, let 

{τi}ni=1 be the random holding times observed along the trajectory generated by a learning algorithm A. Then the total regret of A is defined as 

∆( M, A, s, n ) = 

( n∑

> i=1

τi

)

ρ∗(M ) −

> n

∑

> i=1

ri. (3)   

> 1Notice that decision steps are discrete points in time in which an action is started, while the (possibly continuous) holding time is determined by the distribution τ.

Ronan Fruit, Alessandro Lazaric 

We first notice that this definition reduces to the stan-dard regret in MDPs for τi = 1 (i.e., primitive actions always terminate in one step). The regret measures the difference in cumulative reward obtained by the optimal policy and the learning algorithm. While the performance of the optimal policy is measured by its asymptotic average reward ρ∗, the total duration after 

n decision steps may vary depending on the policy. As a result, when comparing the performance of π∗ after 

n decision steps, we multiply it by the length of the tra-jectory executed by the algorithm A. More formally, from the definition of ρ∗ (Eq. 1) and Prop. 2 we have 2

Eπ∗

[ N (t)

∑

> i=1

ri

∣∣∣s0 = s

]

∼ 

> t→+∞

ρ∗t + o(t).

By introducing the total duration N (t) of A we have 

ρ∗t + o(t) = ρ∗

( N (t)

∑

> i=1

τi

)

+ ρ∗

(

t − 

> N(t)

∑

> i=1

τi

)

+ o(t).

We observe that (t − ∑N (t) 

> i=1

τi

) = o(t) almost surely since (t − ∑N (t) 

> i=1

τi

) ≤ τN (t)+1 and τN (t)+1 is bounded by an almost surely finite (a.s.) random variable since the expected holding time for all state-action pairs is bounded by assumption. So τN (t)+1 /t → 

> t→+∞

0 a.s. and 

Eπ∗

[ N (t)

∑

> i=1

ri

∣∣∣s0 = s

]

∼ 

> t→+∞

ρ∗

( N (t)

∑

> i=1

τi

)

+ o(t),

which justifies the definition of the regret. 

## 3 SMDP-UCRL 

In this section we introduce UCRL-SMDP (Fig. 1), a variant of UCRL [Jaksch et al., 2010]. At each episode 

k, the set of plausible SMDPs Mk is defined by the current estimates of the SMDP parameters and a set of constraints on the rewards, the holding times and the transition probabilities derived from the confidence in-tervals. Given Mk, extended value iteration (EVI) finds an SMDP ˜Mk ∈ M k that maximizes ρ∗( ˜Mk)

and the corresponding optimal policy ˜π∗ 

> k

is computed. To solve this problem, we note that it can be equiv-alently formulated as finding the optimal policy of an extended 3 SMDP ˜M + 

> k

obtained by combining all SMDPs in Mk: ˜M + 

> k

has the same state space and an extended continuous action space ˜A+ 

> k

. Choosing an action a+ ∈ ˜A+ 

> k

amounts to choosing an action 

> 2

In this expectation, N (t) is a r.v. depending on π∗.

> 3

In the MDP literature, the term Bounded Parameter MDPs (BPMDPs) [Tewari and Bartlett, 2007] is often used for "extended" MDPs built using confidence intervals on rewards and transition probabilities. 

Input: Confidence δ ∈]0 , 1[ , S, A, b r , σ r ,

bτ , σ τ , R max , τ max and τmin .

Initialization: Set i = 1 , and observe initial state s0.

For episodes k = 1 , 2, ... do 

Initialize episode k:1. Set the start step of episode k, ik := i

2. For all (s, a ) initialize the counter for episode k,

νk (s, a ) := 0 and set counter prior to episode k,

Nk (s, a ) = # {ι < i k : sι = s, a ι = a}

3. For s, s ′, a set the accumulated rewards, duration and transition counts prior to episode k,

Rk (s, a ) = 

> ik−1

∑

> ι=1

rι1sι=s,a ι=a, T k (s, a ) = 

> ik−1

∑

> ι=1

τι1sι=s,a ι=a

Pk (s, a, s ′) = # {ι < i k : sι = s, a ι = a, s ι+1 = s′}

Compute estimates ˆpk(s′ | s, a ) := Pk (s,a,s ′)  

> max {1,N k(s,a )}

and 

ˆτk (s, a ) := Tk (s,a )  

> Nk(s,a )

and ˆrk (s, a ) := Rk (s,a ) 

> Nk(s,a )

Compute policy ˜πk :4. Let Mk be the set of all SMDPs with states and actions as in M , and with transition probabilities ˜p, rewards 

˜r, and holding time ˜τ such that for any (s, a )

|˜r − ˆrk | ≤ βrk and Rmax τmax ≥ ˜r(s, a ) ≥ 0

|˜τ − ˆτk | ≤ βτk and τmax ≥ ˜τ (s, a ) ≥ ˜r(s, a )/R max , τ min 

‖˜p(·) − ˆpk (·)‖1 ≤ βpk and ∑

> s′∈S

˜p(s′ | s, a ) = 1 

5. Use extended value iteration (EVI) to find a policy ˜πk

and an optimistic SMDP ˜Mk ∈ M k such that: 

˜ρk := min  

> s

ρ( ˜Mk, ˜πk , s ) ≥ max    

> M′∈M k,π,s

ρ(M ′, π, s )− Rmax 

√ik

Execute policy ˜πk :6. While νk (si, ˜πk (si)) < max {1, N k (si, ˜πk (si)} do 

(a) Choose action ai = ˜πk (si), obtain reward ri, and observe next state si+1 

(b) Update νk (si, a i) := νk (si, a i)+1 and set i = i+1 

Figure 1: UCRL-SMDP 

a ∈ A , a reward ˜rk(s, a ), a holding time ˜τk(s, a ) and a transition probability ˜pk(· | s, a ) in the confidence in-tervals. When a+ is executed in ˜M + 

> k

, the probability, the expected reward and the expected holding time of the transition are respectively ˜pk(· | s, a ), ˜rk (s, a ) and 

˜τk(s, a ). Finally, ˜π∗ 

> k

is executed until the number of samples for a state-action pair is doubled. Since the structure is similar to UCRL ’s, we focus on the ele-ments that need to be rederived for the specific SMDP case: the confidence intervals construction and the ex-tended value iteration algorithm. 

Confidence intervals. Unlike in MDPs, we consider Exploration–Exploitation in MDPs with Options 

a slightly more general scenario where cumulative re-wards and holding times are not bounded but are sub-exponential r.v. (see Lem. 3). As a result, the con-fidence intervals used at step 4 are defined as follows. For any state action pair (s, a ) and for rewards, tran-sition probabilities, and holding times we define 

βrk (s, a ) = 

{

σr

√ 14 log(2 SAi k /δ )  

> max {1,N k(s,a )}

, if Nk (s, a ) ≥ 2b2

> r
> σ2
> r

log ( 240 SAi 7

> k
> δ

)

14 br log(2 SAi k /δ )  

> max {1,N k(s,a )}

, otherwise 

βpk (s, a ) = 

√

14 S log(2 Ai k /δ )

max {1, N k (s, a )} ,βτk (s, a ) = 

{

στ

√ 14 log(2 SAi k /δ )  

> max {1,N k(s,a )}

, if Nk (s, a ) ≥ 2b2

> τ
> σ2
> τ

log ( 240 SAi 7

> k
> δ

)

14 bτ log(2 SAi k /δ )  

> max {1,N k(s,a )}

, otherwise 

where σr , br , στ , br are suitable constants character-izing the sub-exponential distributions of rewards and holding times. As a result, the empirical estimates ˆrk,

ˆτk, and ˆpk are ±βrk(s, a ), β τk (s, a ), β pk (s, a ) away from the true values. 

Extended value iteration (EVI). We rely on a data-transformation (also called “uniformization”) that turns an SMDP M into an “equivalent” MDP Meq ={S, A, p eq , r eq 

} with same state and action spaces and such that ∀s, s ′ ∈ S , ∀a ∈ A :

req (s, a ) = r(s, a )

τ (s, a )

peq (s′|s, a ) = τ

τ (s, a )

(p(s′|s, a ) − δs,s ′

) + δs,s ′

(4) where δs,s ′ = 0 if s 6 = s′ and δs,s ′ = 1 otherwise, and 

τ is an arbitrary non-negative real such that τ < τ min .

Meq enjoys the following equivalence property. 

Proposition 3 ([Federgruen et al., 1983], Lemma 2) .

If (v∗, g ∗) is an optimal pair of bias and gain in Meq 

then (τ −1v∗, g ∗) is a solution to Eq. 2, i.e., it is an optimal pair of bias/gain for the original SMDP M .

As a consequence of the equivalence stated in Prop. 3, computing the optimal policy of an SMDP amounts to computing the optimal policy of the MDP obtained after data transformation (see App. A for more de-tails). Thus, EVI is obtained by applying a value it-eration scheme to an MDP ˜M + 

> k,eq

equivalent to the extended SMDP ˜M + 

> k

. We denote the state values of the j-th iteration by uj (s). We also use the vector notation uj = ( uj (s)) s∈S . Similarly, we denote by 

˜p(· | s, a ) = ( ˜p(s′ | s, a )) s′ ∈S the transition probabil-ity vector of state-action pair (s, a ). The optimistic reward at episode k is fixed through the EVI itera-tions and it is obtained as ˜rj+1 (s, a ) = min {ˆrk(s, a ) + 

βrk(s, a ); Rmax τmax 

}, i.e., by taking the largest possible value compatible with the confidence intervals. At iter-ation j, the optimistic transition model is obtained as 

˜pj+1 (· | s, a ) ∈ Arg max p(·)∈P k (s,a ) {p⊺uj } and Pk(s, a )

is the set of probability distributions included in the confidence interval defined by βpk (s, a ). This optimiza-tion problem can be solved in O(S) operations using the same algorithm as in UCRL . Finally, the optimistic holding time depends on uj and the optimistic transi-tion model ˜pj+1 as 

˜τj+1 (s, a ) = min 

{

τmax ; max {τmin ; ˆ τk(s, a )

−sgn [˜rj+1 (s, a )+ τ (˜pj+1 (·| s, a )⊺uj − uj (s))] βτk (s, a )}}

,

The min and max insure that ˜τj+1 ranges between τmin 

and τmax . When the term ˜rj+1 (s, a )+ (˜pj+1 (·| s, a )⊺uj−

uj (s)) is positive (resp. negative), ˜τj+1 (s, a ) is set to the minimum (resp. largest) possible value compati-ble with its confidence intervals so as to maximize the right-hand side of Eq. 5 below. As a result, for any 

τ ∈ ]0 , τ min [, EVI is applied to an MDP equivalent to the extended SMDP ˜M + 

> k

generated over iterations as 

uj+1 (s) = max 

> a∈A

{ ˜rj+1 (s, a )

˜τj+1 (s, a ) (5) 

+ τ

˜τj+1 (s, a )

(˜pj+1 (· | s, a )⊺uj − uj (s)

)}

+ uj (s)

with arbitrary u0. Finally, the stopping condition is 

max  

> s∈S

{ui+1 (s)−ui(s)}− min  

> s∈S

{ui+1 (s)−ui(s)} < ǫ. (6) We prove the following. 

Lemma 1. If the stopping condition holds at iteration 

i of EVI, then the greedy policy w.r.t. ui is ǫ-optimal w.r.t. extended SMDP ˜M + 

> k

. The stopping condition is always reached in a finite number of steps. 

As a result, we can conclude that running EVI at each episode k with an accuracy parameter ǫ =

Rmax /√ik guarantees that ˜πk is Rmax /√ik-optimal w.r.t. max M′ ∈M k ρ∗(M ′).

## 4 Regret Analysis 

In this section we report upper and lower bounds on the regret of UCRL-SMDP . We first extend the notion of diameter to the case of SMDP as follows. 

Definition 2. For any SMDP M , we define the diam-eter D(M ) by 

D(M ) = max  

> s,s ′∈S

{

min 

> π

{

Eπ [T (s′)|s0 = s]}}

(7) 

where T (s′) is the first time in which s′ is encountered, i.e., T (s′) = inf { ∑ ni=1 τi : n ∈ N, s n = s′}.

Note that the diameter of an SMDP corresponds to an average actual duration and not an average number of Ronan Fruit, Alessandro Lazaric 

decision steps. However, if the SMDP is an MDP the two definitions of diameter coincides. Before reporting the main theoretical results about UCRL-SMDP , we introduce a set of technical assumptions. 

Assumption 1. For all s ∈ S and a ∈ A, we assume that τmax ≥ τ (s, a ) ≥ τmin > 0 and 

max s∈S ,a ∈A 

{ r(s,a ) 

> τ(s,a )

}

≤ Rmax with τmin , τmax , and 

Rmax known to the learning algorithm. Furthermore, we assume that the random variables (r(s, a, s ′)) s,a,s ′

and (τ (s, a, s ′)) s,a,s ′ are either 1) sub-Exponential with constants (σr , b r ) and (στ , b τ ), or 2) bounded in 

[0 , R max Tmax ] and [Tmin , T max ], with Tmin > 0. We also assume that the constants characterizing the dis-tributions are known to the learning agent. 

We are now ready to introduce our main result. 

Theorem 1. With probability of at least 1 − δ, it holds that for any initial state s ∈ S and any n > 1, the regret of UCRL-SMDP ∆( M, A, s, n ) is bounded by: 

O

((

D√S + C(M, n, δ )

)

Rmax 

√

SAn log 

( n

δ

))

, (8) 

where C(M, n, δ ) depends on which case of Asm. 1 is considered 4

1) sub-Exponential 

C(M, n, δ ) = τmax +

( σr ∨ br

Rmax 

+ στ ∨ bτ

)√

log 

( n

δ

)

,

2) bounded 

C(M, n, δ ) = Tmax + ( Tmax − Tmin ).

Proof. The proof (App. B) follows similar steps as in [Jaksch et al., 2010]. Apart from adapting the con-centration inequalities to sub-exponential r.v. and de-riving the guarantees about EVI applied to the equiv-alent MDP Meq (Lem. 1), one of the key aspects of the proof is to show that the learning complex-ity is actually determined by the diameter D(M ) in Eq. 2. As for the analysis of EVI, we rely on the data-transformation and we show that the span of uj

(Eq. 5) can be bounded by the diameter of Meq , which is related to the diameter of the original SMDP as 

D(Meq ) = D(M )/τ (Lem. 6 in App. B). 

The bound. The upper bound is a direct generalization of the result derived by Jaksch et al. [2010] for UCRL 

in MDPs. In fact, whenever the SMDP reduces to an MDP (i.e., each action takes exactly one step to exe-cute), then n = T and the regret, the diameter, and the bounds are the same as for UCRL . If we consider 

Rmax = 1 and bounded holding times, the regret scales as ˜O(DS √An + Tmax 

√SAn ). The most interesting as-pect of this bound is that the extra cost of having      

> 4We denote max {a, b }=a∨b.

actions with random duration is only partially addi-tive rather than multiplicative (as it happens e.g., with the per-step reward Rmax ). This shows that errors in estimating the holding times do not get amplified by the diameter D and number of states S as much as it happens for errors in reward and dynamics. This is confirmed in the following lower bound. 

Theorem 2. For any algorithm A, any inte-gers S, A ≥ 10 , any reals Tmax ≥ 3Tmin ≥ 3,

Rmax > 0, D > max {20 Tmin log A(S), 12 Tmin }, and for 

n ≥ max {D, T max }SA , there is an SMDP M with at most S states, A actions, and diameter D, with holding times in [Tmin , T max ] and rewards in [0, 1 

> 2

Rmax Tmax 

]

satisfying ∀s ∈ S , ∀a ∈ A s, r(s, a ) ≤ Rmax τ (s, a ),such that for any initial state s ∈ S the expected regret of A after n decision steps is lower-bounded by: 

E [∆( M, A, s, n )] = Ω 

((√D + √Tmax 

)Rmax 

√SAn 

)

Proof. Similar to the upper bound, the proof (App. C) is based on [Jaksch et al., 2010] but it requires to per-turb transition probabilities and rewards at the same time to create a family of SMDPs with different opti-mal policies that are difficult to discriminate. The con-tributions of the two perturbations can be made inde-pendent. More precisely, the lower bound is obtained by designing SMDPs where learning to distinguish be-tween “good” and “bad” transition probabilities and learning to distinguish between “good” and “bad” re-wards are two independent problems, leading to two additive terms √D and √Tmax in the lower bound. 

The bound. Similar to UCRL , this lower bound reveals a gap of √DS on the first term and √Tmax . While closing this gap remains a challenging open question, it is a problem beyond the scope of this paper. In the next section, we discuss how these results can be used to bound the regret of options in MDPs and what are the conditions that make the regret smaller than using UCRL on primitive actions. 

## 5 Regret in MDPs with Options 

Let M be an MDP and O a set of options and let MO

be the corresponding SMDP obtained from Prop. 1. We index time steps (i.e., time at primitive action level) by t and decision steps (i.e., time at option level) by 

i. We denote by N (t) the total number of decision steps that occurred before time t. Given n decision steps, we denote by Tn = ∑ni=1 τi the number of time steps elapsed after the execution of the n first options so that N (Tn) = n. Any SMDP-learning algorithm 

AO applied to MO can be interpreted as a learning algorithm A on M so that at each time step t, A selects an action of M based on the policy associated to the Exploration–Exploitation in MDPs with Options 

option started at decision step N (t). We can thus compare the performance of UCRL and UCRL-SMDP 

when learning in M . We first need to relate the notion of average reward and regret used in the analysis of  

> UCRL-SMDP

to the original counterparts in MDPs. 

Lemma 2. Let M be an MDP, O a set of options and MO the corresponding SMDP. Let πO be any sta-tionary policy on MO and π the equivalent policy on 

M (not necessarily stationary). For any state s ∈ S O ,any learning algorithm A, and any number of decision steps n we have ρπO (MO, s ) = ρπ (M, s ) and 

∆( M, A, T n) = ∆( MO ,A, n ) + Tn (ρ∗(M ) − ρ∗(MO)) .

The linear regret term is due to the fact that the intro-duction of options amounts to constraining the space of policies that can be expressed in M . As a result, in general we have ρ∗(M ) ≥ ρ∗(MO) = max πO ρπO (MO),where πO is a stationary deterministic policy on MO.Thm. 2 also guarantees that the optimal policy com-puted in the SMDP MO (i.e., the policy maximizing 

ρπO (MO, s )) is indeed the best in the subset of policies that can be expressed in M by using the set of options 

O. In order to use the regret analysis of Thm. 1, we still need to show that Asm. 1 is verified. 

Lemma 3. An MDP provided with a set of op-tions is an SMDP where the holding times and re-wards τ (s, o, s ′) and r(s, o, s ′) are distributed as sub-exponential random variables. Moreover, the holding time of an option is sub-Gaussian if and only if it is almost surely bounded. 

This result is based on the fact that once an option is executed, we obtain a Markov chain with absorb-ing states corresponding to the states with non-zero termination probability βo(s) and the holding time is the number of visited states before reaching a termi-nal state. While in general this corresponds to a sub-exponential distribution, whenever the option has a zero probability to reach the same state twice before terminating (i.e., there is no cycle), then the holding times become bounded. Finally, we notice that no in-termediate case between sub-exponential and bounded distributions is admissible (e.g., sub-Gaussian). Since these are the two cases considered in Thm. 1, we can directly apply it and obtain the following corollary. 

Corollary 1. For any MDP M = {S , A, p, r } with 

r(s, a, s ′) ∈ [0 , R max ] and a set of options O, con-sider the resulting SMDP MO = {S O, AO , p O, r O , τ O }.Then with probability of at least 1 − δ, it holds that for any initial state s ∈ S and any n > 1, the regret of  

> UCRL-SMDP

in the original MDP is bounded as 

O

((DO

√SO + C(MO, n, δ ))RO

> max

√

SO On log 

( n

δ

)) 

+ Tn (ρ∗(M ) − ρ∗(MO)) ,

where O is the number of options. 

We can also show that the lower bound holds for MDPs with options as well. More precisely, it is possible to create an MDP and a set of options such that the lower bound is slightly smaller than that of Thm. 2. 

Corollary 2. Under the same assumptions as in The-orem 2, there exists an MDP with options such that the regret of any algorithm is lower-bounded as 

Ω

((√ DO + √Tmax − Tmin 

)

RO

> max

√SOOn 

)

+ Tn (ρ∗(M ) − ρ∗(MO )) .

This shows that MDPs with options are slightly eas-ier to learn than SMDPs. This is due to the fact that in SMDPs resulting from MDPs with options re-wards and holding times are strictly correlated (i.e., 

r(s, o, s ′) ≤ Rmax τ (s, o, s ′) a.s. and not just in expec-tation for all (s, o, s ′)). We are now ready to proceed with the comparison of the bounds on the regret of learning with options and primitive actions. We recall that for UCRL 

∆( M, UCRL , s, T n) = ˜O(DSR max 

√AT n). We first no-tice that 5 RO 

> max

≤ Rmax and since SO ⊆ S we have that SO ≤ S. Furthermore, we introduce the following simplifying conditions: 1) ρ∗(M ) = ρ∗(MO ) (i.e., the options do not prevent from learning the optimal pol-icy), 2) O ≤ A (i.e., the number of options is not larger than the number of primitive actions), 3) options have bounded holding time (case 2 in Asm. 1). While in gen-eral comparing upper bounds is potentially loose, we notice that both upper-bounds are derived using simi-lar techniques and thus they would be “similarly” loose and they both have almost matching worst-case lower bounds. Let R(M, n, δ ) be the ratio between the re-gret upper bounds of UCRL-SMDP using options O

and UCRL , then we have (up to numerical constants) 

R(M, n ) ≤

(DO

√SO + Tmax 

)√ SOOn log( n/δ )

DS √AT n log( Tn/δ )

≤ DO

√S + Tmax 

D√S

√ n

Tn

,

where we used n ≤ Tn to simplify the logarithmic terms. Since lim inf  

> n→+∞
> Tn
> n

≥ τmin , then the previous ex-pression gives an (asymptotic) sufficient condition for reducing the regret when using options, that is 

DO

√S + Tmax 

D√Sτ min 

≤ 1. (9) In order to have a better grasp on the cases covered by this condition, let DO = αD , with α ≥ 1. This cor-responds to the case when navigating through some     

> 5The largest per-step reward in the SMDP is defined as
> RO
> max ≥max s∈S ,a ∈A
> {r(s,a )
> τ(s,a )
> }.Ronan Fruit, Alessandro Lazaric

Figure 2: Navigation problem. 


τmin > (1 + α)2, then it is easy to see that the condi-tion in Eq. 9 is satisfied. This shows that even when the introduction of options partially disrupt the struc-ture of the original MDP (i.e., DO ≥ D), it is enough to choose options which are long enough (but not too much) to guarantee an improvement in the regret. No-tice that while conditions 1) and 2) are indeed in favor of UCRL-SMDP , SO, O, and Tmax are in general much smaller than S, A, D√S (S and D are large in most of interesting applications). Furthermore, τmin is a very loose upper-bound on lim inf n→+∞ Tn 

> n

and in practice the ratio Tn 

> n

can take much larger values if τmax is large and many options have a high expected holding time. As a result, the set of MDPs and options on which the regret comparison is in favor of UCRL-SMDP is much wider than the one defined in Eq. 9. Nonetheless, as illustrated in Lem. 3, the case of options with bounded holding times is quite restrictive since it requires the absence of self-loops during the execution of an option. If we reproduce the same comparison in the general case of sub-exponential holding times, then the ratio between the regret upper bounds becomes 

R(M, n ) ≤ DO

√S + C(M, n, δ )

D√S

√ n

Tn

,

where C(M, n, δ ) = O(√log( n/δ )) . As a result, as 

n increases, the ratio is always greater than 1, thus showing that in this case the regret of UCRL-SMDP 

is asymptotically worse than UCRL . Whether this is an artefact of the proof or it is an intrinsic weakness of options, it remains an open question. 

## 6 Illustrative Experiment 

We consider the navigation problem in Fig. 2. In any of the d2 states of the grid except the target, the four cardinal actions are available, each of them being suc-cessful with probability 1. If the agent hits a wall then it stays in its current position with probability 1.When the target state is reached, the state is reset to any other state with uniform probability. The reward of any transition is 0 except when the agent leaves the target in which case it equals Rmax . The optimal pol-icy simply takes the shortest path from any state to the target state. The diameter of the MDP is the longest shortest path in the grid, that is D = 2 d − 2. Let m

be any non-negative integer smaller than d and in ev-ery state but the target we define four macro-actions: 

LEFT , RIGHT , UP and DOWN (blue arrows in the figure). When LEFT is taken, primitive action left is applied up to m times (similar for the other three op-tions). For any state s′ which is k ≤ m steps on the left of the starting state s, we set βo(s′) = 1 /(m−k+1) 

so that the probability of the option to be interrupted after any k ≤ m steps is 1/m . If the starting state s is 

l steps close to the left border with l < m then we set 

βo(s′) = 1 /(l − k + 1) for any state s′ which is k ≤ l

steps on the left. As a result, for all options started m

steps far from any wall, Tmax = m and the expected duration is τ := τ (s, o ) = ( m + 1) /2, which reduces to Tmax = l and τ = ( l + 1) /2 for an option started 

l < m step from the wall and moving towards it. More precisely, all options have an expected duration of τ (s, o ) = τ in all but in md states, which is small compared to the total number of d2 states. The SMDP formed with this set of options preserves the number of state-action pairs SO = S = d2 and A′ = A = 4 and the optimal average reward ρ∗(M ) = ρ∗(M ′), while it slightly perturbs the diameter DO ≤ D+m(m+1) (see App. F for further details). Thus, the two problems seem to be as hard to learn. However the (asymptotic) ratio between the regret upper bounds becomes 

lim 

> n→∞

R(M, n ) ≤ (2 d − 2 + m2 + m)d + m

(2 d − 2) d

(

lim 

> n→∞

√ n

Tn

)

≤

(

1 + 2 m2

d

) ( 

lim 

> n→∞

√ n

Tn

)

,

where we assume m, d ≥ 2. While a rigorous analy-sis of the ratio between the number of option decision steps n and number of primitive actions Tn is difficult, we notice that as d increases w.r.t. m, the chance of ex-ecuting options close to a wall decreases, since for any option only md out of d2 states will lead to a duration smaller than τ and thus we can conclude that n/T n

tends to 1/τ = 2 /(m + 1) as n and d grow. As a re-sult, the ratio would reduce to (1+2 m2/d )√2/(m + 1) 

that is smaller than 1 for a wide range of values for m

and d. Finally, the ratio is (asymptotically in d) min-imized by m ≈ √d, which gives R(M, n ) = O(d−1/4),thus showing that as d increases there is always an appropriate choice of m for which learning with op-tions becomes significantly better than learning with primitive actions. In Fig. 3a we empirically validate Exploration–Exploitation in MDPs with Options        

> 12345678

Maximal duration of options Tmax 

> 0.75 0.80 0.85 0.90 0.95 1.00 1.05 1.10
> Ratio of regrets  R 20x20 Grid 25x25 Grid 30x30 Grid

(a)                   

> 1.41.61.82.02.22.42.62.83.0
> Duration Tn×10 7
> 0.70 0.75 0.80 0.85 0.90 0.95 1.00
> Cumulative Regret  ∆( Tn)
> ×10 7
> Tmax = 1
> Tmax = 2
> Tmax = 3
> Tmax = 4
> Tmax = 5
> Tmax = 6
> Tmax = 7
> Tmax = 8

(b)            

> 0.00.51.01.52.02.53.0
> Duration Tn×10 7
> 1.01.52.02.53.03.54.0
> Duration per decision step  Tn/n
> Tmax = 8
> Tmax = 4
> Tmax = 2

(c) 

Figure 3: (a) Ratio of the regrets with and without options for different values of Tmax ; (b) Regret as a function of Tn for a 20x20 grid; (c) Evolution of Tn/n for a 20x20 grid. this finding by studying the ratio between the actual regrets (and not their upper-bounds) as d and m (i.e., 

Tmax ) vary, and with a fixed value of Tn that is cho-sen big enough for every d. As expected, for a fixed value of d, the ratio R first decreases as m increases, reaches a minimum and starts increasing to eventually exceed 1. As d increases, the value of the minimum de-creases, while the optimal choice of m increases. This behaviour matches the theory, which suggests that the optimal choice for m increases as O(√d). In Fig. 3b we report the cumulative regret and we observe that high values of Tmax worsen the learning performances w.r.t. learning without options ( Tmax = 1 , plotted in black). Finally, Fig. 3c shows that, as n tends to infinity, Tn/n 

tends to converge to (m + 1) /2 when m ≪ d, whereas it converges to slightly smaller values when m is close to d because of the truncations operated by walls. 

Discussion. Despite its simplicity, the most interest-ing aspect of this example is that the improvement on the regret is not obtained by trivially reducing the number of state-action pairs, but it is intrinsic in the way options change the dynamics of the exploration process. The two key elements in designing a success-ful set of options O is to preserve the average reward of the optimal policy and the diameter. The former is often a weaker condition than the latter. In this exam-ple, we achieved both conditions by designing a set O

where the termination conditions allow any option to end after only one step. This preserves the diameter of the original MDP (up to an additive constant), since the agent can still navigate at the level of granular-ity of primitive actions. Consider a slightly different set of options O′, where each option moves exactly by m steps (no intermediate interruption). The num-ber of steps to the target remains unchanged from any state and thus we can achieve the optimal performance. Nonetheless, having π∗ in the set of policies that can be represented with O′ does not guarantee that the 

UCRL-SMDP would be as efficient in learning the op-timal policy as UCRL . In fact, the expected number of steps needed to go from a state s to an adjacent state 

s′ may significantly increase. Despite being only one primitive action apart, there may be no sequence of options that allows to reach s′ from s without relying on the random restart triggered by the target state. A careful analysis of this case shows that the diameter is as large as DO′ = D(1 + m2) and there exists no value of m that satisfies Eq. 9 (see App. F). 

## 7 Conclusions 

We derived upper and lower bounds on the regret of learning in SMDPs and we showed how these results apply to learning with options in MDPs. Comparing the regret bounds of UCRL-SMDP with UCRL , we provided sufficient conditions on the set of options and the MDP (i.e., similar diameter and average reward) to reduce the regret w.r.t. learning with primitive actions. To the best of our knowledge, this is the first attempt of explaining when and how options affect the learning performance. Nonetheless, we believe that this result leaves space for improvements. In fact, Prop. 1 implies that the class of SMDPs is a strict superset of MDPs with options. This suggests that a more effective anal-ysis could be done by leveraging the specific structure of MDPs with options rather than moving to the more general model of SMDPs. This may actually remove the additional √log( n/δ ) factor appearing because of sub-exponential distributions in the UCRL-SMDP re-gret. An interesting direction of research is to use this theoretical result to provide a more explicit and quan-titative objective function for option discovery, in the line of what is done in [Brunskill and Li, 2014]. Finally, it would be interesting to extend the current analysis to more sophisticated hierarchical approaches to RL such as MAXQ [Dietterich, 2000]. Ronan Fruit, Alessandro Lazaric 

## References 

Applied Probability Models with Optimization Applications ,chapter 7: Semi Markov Decision Processes. Dover Pub-lications, INC., New York, 1970. 

A First Course in Stochastic Models , chapter 7: Semi Markov Decision Processes. Wiley, 2003. Pierre-Luc Bacon and Doina Precup. The option-critic ar-chitecture. In NIPS’15 Deep Reinforcement Learning Workshop , 2015. Emma Brunskill and Lihong Li. PAC-inspired Option Dis-covery in Lifelong Reinforcement Learning. In Proceed-ings of the 31st International Conference on Machine Learning , volume 32 of JMLR Proceedings , pages 316– 324. JMLR.org, 2014. Pablo Samuel Castro and Doina Precup. Automatic con-struction of temporally extended actions for mdps using bisimulation metrics. In Proceedings of the 9th Euro-pean Conference on Recent Advances in Reinforcement Learning , EWRL’11, pages 140–152, Berlin, Heidelberg, 2012. Springer-Verlag. ISBN 978-3-642-29945-2. doi: 10.1007/978-3-642-29946-9_16. Özgür Şimşek and Andrew G. Barto. Using relative nov-elty to identify useful temporal abstractions in reinforce-ment learning. In Proceedings of the Twenty-first In-ternational Conference on Machine Learning , ICML ’04, 2004. Thomas G. Dietterich. Hierarchical reinforcement learning with the maxq value function decomposition. Journal of Artificial Intelligence Research , 13:227–303, 2000. A. Federgruen, P.J. Schweitzer, and H.C. Tijms. Denu-merable undiscounted semi-markov decision processes with unbounded rewards. Mathematics of Operations Research , 1983. Thomas Jaksch, Ronald Ortner, and Peter Auer. Near-optimal regret bounds for reinforcement learning. J. Mach. Learn. Res. , 11:1563–1600, August 2010. Nicholas K. Jong, Todd Hester, and Peter Stone. The utility of temporal abstraction in reinforcement learn-ing. In The Seventh International Joint Conference on Autonomous Agents and Multiagent Systems , May 2008. Arie Leizarowitz. Decision and Control in Management Science: Essays in Honor of Alain Haurie , chapter 5: On Optimal Policies of Multichain Finite State Compact Action Markov Decision Processes. Springer Science and Business Media, 2013. Kfir Y. Levy and Nahum Shimkin. Unified inter and intra options learning using policy gradient methods. In Scott Sanner and Marcus Hutter, editors, EWRL , volume 7188 of Lecture Notes in Computer Science , pages 153–164. Springer, 2011. ISBN 978-3-642-29945-2. Kfir Y. Levy and Nahum Shimkin. Recent Advances in Re-inforcement Learning: 9th European Workshop, EWRL 2011 , chapter Unified Inter and Intra Options Learning Using Policy Gradient Methods, pages 153–164. Springer Berlin Heidelberg, 2012. Jianyong Liu and Xiaobo Zhao. On average reward semi-markov decision processes with a general multichain structure. Math. Oper. Res. , 29(2):339–352, 2004. Timothy A. Mann and Shie Mannor. Scaling up approxi-mate value iteration with options: Better policies with fewer iterations. In Proceedings of the 31st International Conference on Machine Learning , 2014. Timothy Arthur Mann, Daniel J. Mankowitz, and Shie Mannor. Time-regularized interrupting options (TRIO). In Proceedings of the 31th International Conference on Machine Learning, ICML 2014, Beijing, China, 21-26 June 2014 , pages 1350–1358, 2014. Amy McGovern and Andrew G. Barto. Automatic discov-ery of subgoals in reinforcement learning using diverse density. In Proceedings of the Eighteenth International Conference on Machine Learning , pages 361–368, 2001. Ishai Menache, Shie Mannor, and Nahum Shimkin. Q-cut - dynamic discovery of sub-goals in reinforcement learn-ing. In Proceedings of the 13th European Conference on Machine Learning , 2002. Iryna Felko Peter Buchholz, Jan Kriege. Input Modeling with Phase-Type Distributions and Markov Models , chap-ter Phase-Type Distributions. Springer, 2014. Martin L. Puterman. Markov Decision Processes: Dis-crete Stochastic Dynamic Programming . John Wiley & Sons, Inc., New York, NY, USA, 1st edition, 1994. ISBN 0471619779. Munu Sairamesh and Balaraman Ravindran. Options with exceptions. In Proceedings of the 9th European Con-ference on Recent Advances in Reinforcement Learn-ing , EWRL’11, pages 165–176, Berlin, Heidelberg, 2012. Springer-Verlag. ISBN 978-3-642-29945-2. doi: 10.1007/ 978-3-642-29946-9_18. M. Schäl. On the second optimality equation for semi-markov decision models. Mathematics of Operations Re-search , 1992. Jonathan Sorg and Satinder P. Singh. Linear Options. In 

AAMAS , pages 31–38, 2010. Richard S. Sutton and Andrew G. Barto. Introduction to Reinforcement Learning . MIT Press, Cambridge, MA, USA, 1st edition, 1998. ISBN 0262193981. Richard S. Sutton, Doina Precup, and Satinder Singh. Be-tween mdps and semi-mdps: A framework for temporal abstraction in reinforcement learning. Artificial Intelli-gence , 112(1):181 – 211, 1999. Chen Tessler, Shahar Givony, Tom Zahavy, Daniel J. Mankowitz, and Shie Mannor. A deep hierarchical approach to lifelong learning in minecraft. CoRR ,abs/1604.07255, 2016. Ambuj Tewari and Peter L. Bartlett. Bounded Param-eter Markov Decision Processes with Average Reward Criterion , pages 263–277. Springer Berlin Heidelberg, Berlin, Heidelberg, 2007. ISBN 978-3-540-72927-3. doi: 10.1007/978-3-540-72927-3_20. Vladimir Vovk, Alex Gammerman, and Glenn Shafer. Al-gorithmic Learning in a Random World . Springer-Verlag New York, Inc., Secaucus, NJ, USA, 2005. ISBN 0387001522. Martin Wainwright. Course on Mathematical Statistics ,chapter 2: Basic tail and concentration bounds. Univer-sity of California at Berkeley, Department of Statistics, 2015. Exploration–Exploitation in MDPs with Options 

## A Optimal average reward in discrete and continuous SMDPs: existence and computation 

In this section we prove Proposition 2 and Lemma 1. Since extended value iteration is run on SMDP ˜M + 

> k

with continuous actions (the choice of the transition probability), in the following we consider both the continuous and discrete case at the same time. In order to have a more rigorous treatment of SMDPs, we introduce further notations from [Puterman, 1994]. A decision rule is a function d : H → ∆( A) where H is the set of possible histories and ∆( A) is the set of probability distributions over A. For an SMDP M , we will denote by DHR M the set of history-dependent randomized decision rules and DMD M the subset of Markovian deterministic decision rules ( DMD M ⊂ DHR M ). Ahistory-dependent randomized policy is a sequence of elements of DHR M indexed by the decision steps, i.e., π =(d1, d 2, ... ) ∈ (DHR M )N, while a stationary deterministic policy is a constant sequence of elements of DMD M : π =(d, d, ... ) = d∞. The set of history-dependent randomized policies will be denoted ΠHR M and the subset of stationary deterministic policies will be denoted ΠSD M : ΠSD M ⊂ ΠHR M . We also consider the more general case where the set of available actions may depend on the state, i.e., there exists a set As for each s ∈ S .

A.1 Optimality criterion 

We start by defining the optimality criterion in SMDPs. Unlike for MDPs, where the average reward of a fixed policy is uniquely defined, in SMDPs there are three different definitions that are usually encountered in the literature (see Schäl 1992, Federgruen et al. 1983, and Ros 1970). 6

Definition 3. Denote N (t) = sup 

{

n : n ∈ N, ∑ni=1 τi ≤ t

}

the number of decision steps that occured before time t. For any π ∈ ΠHR M and s ∈ S , we define: 

ρ1π (s) = lim sup 

> t→+∞

Eπ

[ ∑ N (t) 

> i=1

ri

t

∣∣∣∣s0 = s

]

, ρ1π (s) = lim inf  

> t→+∞

Eπ

[ ∑ N (t) 

> i=1

ri

t

∣∣∣∣s0 = s

]

(10) 

ρ2π (s) = lim sup 

> n→+∞

Eπ [ ∑ ni=1 ri

∣∣s0 = s]

Eπ[ ∑ ni=1 τi

∣∣s0 = s] , ρ2π (s) = lim inf 

> n→+∞

Eπ [ ∑ ni=1 ri

∣∣s0 = s]

Eπ[ ∑ ni=1 τi

∣∣s0 = s] (11) 

and for any d∞ ∈ ΠSD M and s ∈ S we define: 

ρd∞ 

> 3

(s) = 

> ν(d)

∑

> α=1

pd(α|s)gd(α), with gd(α) = 

∑ 

> s∈Rdα

μdα(s)r(s, d (s)) 

∑

> s∈Rdα

μdα(s)τ (s, d (s)) (12) 

where ν(d) is the number of positive recurrent classes under d∞, pd(α|s) is the probability of entering positive recurrent class α starting from s and following policy d∞, Rdα is the set of states of class α and μdα is the stationary probability distribution of class α.

A.2 Proof of Proposition 2 

We say that (d∗)∞ is (3)-average-optimal if for all states s ∈ S and decision rules d ∈ DMD M , ρ(d∗)∞ 

> 3

(s) ≥

ρd∞ 

> 3

(s). We say that π∗ is (1)-average-optimal (respectively (2)-average-optimal) if for all states s ∈ S and all 

π ∈ ΠHR M , ρ1π∗

(s) ≥ ρ1π (s) (respectively ρ2π∗

(s) ≥ ρ2π (s)). We prove a slightly more general formulation than Proposition 2. 

Proposition 4. If M is communicating and the expected holding times and rewards are finite, then 

• There exists a stationary policy π∗ = ( d∗)∞ which is (1,2,3)-average-optimal. 

• All optimal values are equal and constant and we will denote this value by ρ∗:

∀s ∈ S , ρ1(d∗)∞

(s) = ρ1(d∗)∞

(s) = ρ2(d∗ )∞

(s) = ρ2(d∗)∞

(s) = ρ(d∗)∞ 

> 3

(s) = ρ∗.

> 6

Notice that the definition we provide in Eq. 1 of Prop. 2 is ρ1.Ronan Fruit, Alessandro Lazaric 

Proof. Step 1: Optimality equation of a communicating SMDP. We first recall the average reward optimality equations for a communicating SMDP (Eq. 2) 

∀s ∈ S , u ∗(s) = max 

> a∈A s

{

r(s, a ) − ρ∗τ (s, a ) + ∑ 

> s′∈S

p(s′|s, a )u∗(s′)

}

(13) where u∗ and ρ∗ are the bias (up to additive constant) and average reward respectively. Since we need to analyse both the case where As is finite and the case where As is continuous, we verify that it is appropriate to consider the max instead of sup in the previous expression. For the original SMDP M , As is finite and the maximum is well-defined. For the extended SMDPs ˜M + 

> k

considered while computing the optimistic SMDP, ˜A+

> k,s

is compact and r(s, a ), τ (s, a ) and p(· | s, a ) are continuous in ˜A+ 

> k,s

by the very definition of ˜M + 

> k

. The function 

r(s, a ) − ρ∗τ (s, a ) + ∑  

> s′∈S

p(s′|s, a )u∗(s′) is thus continuous on ˜A+ 

> k,s

compact and by Weierstrass theorem, we know that the maximum is reached (i.e., there exists a maximizer). As a result, Eq. 13 is well-defined and we can study the existence and properties of its solutions. 

Step 2: Data-transformation (uniformization) of an SMDP. The structure of EVI is based on a data-transformation (also called "uniformization") which turns the initial SMDP M into an “equivalent” MDP Meq ={S, A, p eq , r eq 

} defined as in Eq. 4. As a result, we can just apply standard MDP theory to the equivalent MDP. The average optimality equation of Meq is [Puterman, 1994] 

∀s ∈ S , v ∗(s) = max 

> a∈A s

{

r(s, a )

τ (s, a ) − g∗ + τ

τ (s, a )

∑ 

> s′∈S

p(s′|s, a )v∗(s′) + 

(

1 − τ

τ (s, a )

)

v∗(s)

}

(14) Since τ < τ min , every Markov Chain induced by a stationary deterministic policy on Meq is necessarily aperiodic (for any action, the probability of any state to loop on itself is strictly positive). Moreover, since M is assumed to be communicating, Meq is also communicating. The same holds for ˜M + 

> k, eq

(i.e., the MDP obtained from the extended SMDP ˜M + 

> k

after data transformation). Under these conditions, Eq. 14 has a solution (v∗, g ∗) where 

g∗ is the optimal average reward of Meq (respectively ˜M +

> k, eq

) and the (stationary deterministic) greedy policy w.r.t. v∗ is average-optimal. Moreover, standard value iteration is guaranteed to converge and it can be applied with the stopping condition in Eq. 6 to obtain an ǫ-optimal policy in finitely many steps. This holds for both finite and compact As with continuous req (s, a ) and peq (s′|s, a ) (see for example Puterman 1994 and Leizarowitz 2013). It is easy to show that EVI in Eq. 5 is exactly value iteration applied to ˜M +

> k, eq

. Finally, Lemma 2 of [Federgruen et al., 1983] (Prop. 3) shows the “equivalence” between M and Meq (respectively ˜M + 

> k

and ˜M +

> k, eq

): if (v∗, g ∗) is a solution to Eq. 14, then (τ −1 v∗, g ∗) is a solution to Eq. 13 and conversely. As a result, there exists a solution (u∗, ρ ∗) to Eq. 13 for both M and ˜M + 

> k

.

Step 3: Existence of deterministic stationary optimal policy. We are now ready to prove the existence of a deterministic stationary policy that is (1,2,3)-optimal and that the corresponding optimal value is constant and equal in all three cases. We consider the case of finite and continuous As separately. 

Step 3a: For M (finite As). Since conditions (L), (F) and (R) of [Schäl, 1992] hold, we can apply their main theorem and obtain that 1. Any greedy policy (d∗)∞ w.r.t. u∗ is such that ρ1(d∗)∞

(s) ≥ ρ1π (s) for any π ∈ ΠHR M and any s ∈ S ,2. ∀s ∈ S , ρ1(d∗)∞

(s) = ρ∗,where (u∗, ρ ∗) is a solution of Eq. 13. Furthermore, from renewal theory (see e.g., Tij 2003 and [Ros, 1970]) we have that ∀d∞ ∈ ΠSD M , ρ1d∞

= ρ1d∞

= ρd∞ 

> 1

(i.e., the limit exists for deterministic stationary policies), thus we can conclude that (d∗)∞ is (1)-optimal. Furthermore, by Lemma 2.7 of [Schäl, 1992]: ∀d∞ ∈ ΠSD M , ∀s ∈S, ρ1d∞

(s) = ρd∞ 

> 3

(s) so d∗ is also necessarily (3)-optimal. Finally, by Theorem 7.6 of [Ros, 1970], since (u∗, ρ ∗)

is a solution of Eq. 13: 1. Any greedy policy (d∗)∞ w.r.t. u∗ is such that ρ2(d∗)∞

(s) ≥ ρ2π (s) for any π ∈ ΠHR M and any s ∈ S ,2. ∀s ∈ S , ρ2(d∗)∞

(s) = ρ∗.Exploration–Exploitation in MDPs with Options 

By Theorem 11.4.1 of [Puterman, 1994] we have ∀d∞ ∈ ΠSD M , ρ2 = ρ2 = ρd∞ 

> 2

and thus d∗ is also (2)-optimal. This concludes the proof for the finite case, which proves the statement of Prop. 2. 

Step 3b: For ˜M + 

> k

(compact ˜A+ 

> k,s

with continuous rewards, holding times and transition probabili-ties). The proof is almost the same as with discrete action spaces. The only difference is that we can’t apply the Theorem of [Schäl, 1992] because conditions (R) and (C*) do not hold in general. However, we can use Propositions 5.4 and 5.5 of [Schäl, 1992] and we have the same result as in the discrete case (assumptions (L), (C), (P) and (I) hold in our case and we know that the optimality equation 13 admits a solution (u∗, ρ ∗), see above). Since the state space is finite, the rest of the proof is rigorously the same (the Theorems and Lemmas still applies). This guarantees the same statement as Prop. 2 but for the optimistic SMDP ˜M + 

> k

.

A.3 Proof of Lemma 1 

Proof. From the proof of Prop. 2, we already have that EVI converges towards the optimal average reward of 

˜M +

> k, eq

, which is also the optimal average reward of ˜M + 

> k

. We also know that the stopping criterion is met in a finite number of steps and that the greedy policy when the stopping criterion holds is ǫ-optimal in the equivalent 

˜M +

> k, eq

. Then, in order to prove Lemma 1, we only need to prove that this policy is also ǫ-optimal in the optimistic SMDP ˜M + 

> k

. Tij [2003] shows that for any stationary deterministic policy d∞ ∈ ΠSD 

> ˜M+
> k

, the (1)-average reward is the same in the SMDP and the MDP obtained by uniformization, that is 

∀s ∈ S , ρ d∞ 

> 1

( ˜M + 

> k

) = ρd∞

( ˜M +

> k, eq

).

Then it immediately follows that the policy returned by EVI is (1)-ǫ-optimal in ˜M + 

> k

and since ∀d∞ ∈ ΠSD M , ρ d∞ 

> 1

=

ρd∞ 

> 3

, it is also (3)-ǫ-optimal. Note that for any deterministic stationary policy d ∈ ΠSD 

> ˜M+
> k

defining a unichain Markov chain in ˜M + 

> k, eq

(or equivalently in ˜M + 

> k

), we have: ∀s ∈ S , ρ d∞ 

> 1

(s) = ρd∞ 

> 2

(s) and this value is constant across states (see for example chapter 11 of [Puterman, 1994], Theorem 7.5 of [Ros, 1970] or [Liu and Zhao, 2004]). However, in the general case, this equality does not hold (see Example 2.1 of [Liu and Zhao, 2004]). Nevertheless, by Theorem 3.1 of [Liu and Zhao, 2004] we have 

∀d∞ ∈ ΠSD 

> ˜M+
> k

, ∀s ∈ S , ∣∣ρd∞ 

> 2

( ˜M + 

> k

, s ) − ρd∞

( ˜M +

> k, eq

, s )∣∣ ≤ ρd∞

> max

( ˜M +

> k, eq

) − ρd∞

> min

( ˜M +

> k, eq

)

where ρd∞

> max

( ˜M +

> k, eq

) = max  

> s∈S

ρd∞

( ˜M +

> k, eq

, s ) and ρd∞

> min

( ˜M +

> k, eq

) = min  

> s∈S

ρd∞

( ˜M +

> k, eq

, s ). (15) If we denote by d the policy returned by EVI and ρ∗ the optimal gain of ˜M + 

> k, eq

and ˜M + 

> k

we obtain 

∀s ∈ S , ρ∗ − ρd∞ 

> 2

( ˜M + 

> k

, s ) = ρd∞

( ˜M +

> k, eq

, s ) − ρd∞ 

> 2

( ˜M + 

> k

, s ) + ρ∗ − ρd∞

( ˜M +

> k, eq

, s )

≤ ρd∞

> max

( ˜M +

> k, eq

) − ρd∞

> min

( ˜M +

> k, eq

) + ǫ

= ρd∞

> max

( ˜M +

> k, eq

) − ρ∗ + ρ∗ − ρd∞

> min

( ˜M +

> k, eq

) + ǫ ≤ 2ǫ. 

For the first inequality we used Eq. 15 and the fact that d is ǫ-optimal in ˜M +

> k, eq

. For the second inequality, we used again that d is ǫ-optimal in ˜M + 

> k, eq

and we also used the fact that ρd∞

> max

( ˜M +

> k, eq

) ≤ ρ∗. In conclusion, the policy returned by EVI is (2)-2ǫ-optimal. The remaining part of Theorem 1 is thus proved for all optimality criteria. 

By Theorem 8.3.2 of [Puterman, 1994], we know that there exists an optimal policy ˜d∗ of MDP ˜M + 

> k, eq

that yields a unichain Markov Chain (i.e., a Markov Chain with a single positive recurrent class). The Markov Chain induced by ˜d∗ in ˜M + 

> k

is thus also unichain and moreover: ρ( ˜d∗)∞ 

> 1

( ˜M + 

> k

) = ρ( ˜d∗)∞

( ˜M +

> k, eq

) = ρ∗( ˜M +

> k, eq

) = ρ∗( ˜M + 

> k

).We have seen that for any policy d ∈ ΠSD 

> ˜M+
> k

yielding a unichain Markov Chain ρd∞ 

> 1

( ˜M + 

> k

) = ρd∞ 

> 2

( ˜M + 

> k

) and so in particular, it is true for ˜d∗. Therefore, there exists a policy of ˜M + 

> k

which yields a unichain Markov Chain and which is (1)-optimal, (2)-optimal and (3)-optimal. This explains why the optimal gain is the same for criteria (1) and (2) but EVI must be run with a different accuracy to insure ǫ-accuracy (the Markov Chain induced by the policy returned by EVI is not necessarily unichain). Ronan Fruit, Alessandro Lazaric 

## B Analysis of SMDP-UCRL (proof of Theorem 1) 

The proof follows the same steps as in [Jaksch et al., 2010]. Therefore, in the following we only emphasize the differences between SMDPs and MDPs and we refer to [Jaksch et al., 2010] for the parts of the proof which are similar. 

B.1 Splitting into Episodes 

We first recall the definition of sub-exponential random variables. 

Definition 4 (Wainwright [2015]) . A random variable X with mean μ < +∞ is said to be sub-exponential, if one of the following equivalent conditions is satisfied: 1. (Laplace transform condition) There exists (σ, b ) ∈ R+ × R+∗ such that: 

E[eλ(X−μ)] ≤ e σ2 λ2 

> 2

for all |λ| < 1

b . (16) 

In this case, we say that X is sub-exponential of parameters σ, b and we denote it by X ∈ subExp( σ, b ).2. There exists c0 > 0 such that E[eλ(X−μ)] < +∞ for all |λ| ≤ c0.

In order to define the confidence intervals, we use the Bernstein concentration inequality for sub-exponential random variables. 

Proposition 5 (Bernstein inequality, [Wainwright, 2015]) . Let (Xi)1≤i≤n be a collection of independent sub-Exponential random variables s.t. ∀i ∈ { 1, ..., n }, X i ∈ subExp( σi, b i) and E[Xi] = μi. We have the following concentration inequalities: 

∀t ≥ 0, P

( n∑

> i=1

Xi −

> n

∑

> i=1

μi ≥ t

)

≤

{

e− t2 

> 2nσ 2

, if 0 ≤ t ≤ σ2

> b

e− t 

> 2b

, if t > σ2

> b

P

( n∑

> i=1

Xi +

> n

∑

> i=1

μi ≤ t

)

≤

{

e− t2 

> 2nσ 2

, if 0 ≤ t ≤ σ2

> b

e− t 

> 2b

, if t > σ2

> b

(17) 

where σ =

√ ∑ni=1 σ2 

> i
> n

and b = max 1≤i≤n{bi}.

Denoting by N (s, a ) the state-action counts we have 

> n

∑

> i=1

ri(si−1, a i−1) = ∑

> s∈S

∑ 

> a∈A s
> N(s,a )

∑

> j=1

rkj (s, a ).

Conditionally on knowing (N (s, a )) s,a , the previous sum is equal (in distribution) to a sum of independent random variables with mean ∑

> s∈S

∑ 

> a∈A s

N (s, a )r(s, a ) and from Prop. 5 we have 

P

( n∑

> i=1

ri ≤ ∑

> s∈S

∑

> a∈A s

N (s, a )r(s, a ) − σr

√

5

2 n log 

( 13 n

δ

)∣∣∣∣∣ (N (s, a )) s,a 

)

≤

( δ

13 n

)5/4

≤ δ

24 n5/4 ,

if n ≥ 5b2

> r

2σ2

> r

log 

( 13 n

δ

)

P

( n∑

> i=1

ri ≤ ∑

> s∈S

∑

> a∈A s

N (s, a )r(s, a ) − 5

2 br log 

( 13 n

δ

) ∣∣∣∣∣ (N (s, a )) s,a 

)

≤

( δ

13 n

)5/4

≤ δ

24 n5/4 ,

if n ≤ 5b2

> r

2σ2

> r

log 

( 13 n

δ

)Exploration–Exploitation in MDPs with Options 

Similarly, the total holding time satisfies 

P

( n∑

> i=1

τi ≥ ∑

> s∈S

∑

> a∈A s

N (s, a )τ (s, a ) + στ

√

5

2 n log 

( 13 n

δ

)∣∣∣∣∣ (N (s, a )) s,a 

)

≤

( δ

13 n

)5/4

≤ δ

24 n5/4 ,

if n ≥ 5b2

> τ

2σ2

> τ

log 

( 13 n

δ

)

P

( n∑

> i=1

τi ≥ ∑

> s∈S

∑

> a∈A s

N (s, a )τ (s, a ) + 5

2 bτ log 

( 13 n

δ

) ∣∣∣∣∣ (N (s, a )) s,a 

)

≤

( δ

13 n

)5/4

≤ δ

24 n5/4 ,

if n ≤ 5b2

> τ

2σ2

> τ

log 

( 13 n

δ

)

Lemma 4. The optimal average reward can be bounded as follows: 

ρ∗(M ) ≤ max 

> s∈S ,a ∈A s

{ r(s, a )

τ (s, a )

}

≤ Rmax .

Proof. In App. A we prove that ρ∗(M ) = ρ∗(Meq ) where ρ∗(Meq ) is the optimal average reward of an MDP 

Meq with same state and action spaces as SMDP M and with average rewards of the form r(s,a )  

> τ(s,a )

. All the rewards of Meq are thus bounded by Rmax and so ρ∗(Meq ) is necessarily bounded by Rmax as well and thus: 

ρ∗(M ) ≤ Rmax .

We are now ready to split the regret over episodes. We define the per-episode regret as 

∆k = ∑

> s∈S

∑

> a∈A s

νk(s, a ) ( τ (s, a )ρ∗ − r(s, a )) .

Setting γr = max 

{ 5 

> 2

br,

√ 5 

> 2

σr

}

and γτ = max 

{ 5 

> 2

bτ ,

√ 5 

> 2

στ

}

, and using a union bound on the previous inequali-ties we have that with probability at least 1 − δ

> 12 n5/4

∆( M, A, s, n ) ≤

> n

∑

> k=1

∆k + ( γr + γτ Rmax ) log 

( 13 n

δ

) √n

B.2 Dealing with Failing Confidence Regions Lemma 5. For any episode k ≥ 1, the probability that the true SMDP M is not contained in the set of plausible MDPs Mk at step i is at most δ

> 15 i6
> k

, that is: 

∀k ≥ 1, P (M 6 ∈ M k) < δ

15 i6

> k

(18) 

Proof. This lemma is the SMDP-analogue of Lemma 17 in [Jaksch et al., 2010] and the proof is similar. Using an ℓ1-concentration inequality for discrete probability distributions we obtain 

P

(∥∥p(·| s, a ) − ˆpk(·| s, a )∥∥1 ≥ βpk (s, a )

)

= P

(∥∥p(·| s, a ) − ˆpk(·| s, a )∥∥1 ≥

√

14 S

n log 

( 2Ai k

δ

))

≤ P

(∥∥p(·| s, a ) − ˆpk(·| s, a )∥∥1 ≥

√

2

n log 

( 2S 20 SAi 7

> k

δ

))

≤ 2S exp 

(

− n

2 × 2

n log 

( 2S 20 SAi 7

> k

δ

)) 

= δ

20 i7

> k

SA Ronan Fruit, Alessandro Lazaric 

In the inequalities above, it is implicitly assumed that the value Nk(s, a ) = n is fixed. To be more rigorous, we are bounding the probability of the intersection of event {∥∥˜p(·| s, a ) − ˆpk(·| s, a )∥∥1 ≥ βpk (s, a )} with event 

{Nk(s, a ) = n} but we omitted the latter to simplify notations, and we will also omit it in the next inequalities. Using Bernstein inequality (Prop. 5) and noting that 240 ≤ 27 ( SA 

> δ

)6 for S, A ≥ 2 and δ ≤ 1, we have: 

• If n ≥ 2b2

> r
> σ2
> r

log 

( 240 SAi 7

> k
> δ

)

:

P

(

|r(s, a ) − ˆrk (s, a )| ≥ βrk(s, a )

)

= P

(

|r(s, a ) − ˆrk(s, a )| ≥ σr

√

14 

n log 

( 2SAi k

δ

))

≤ P

(

|r(s, a ) − ˆrk(s, a )| ≥ σr

√

2

n log 

( 240 SAi 7

> k

δ

))

≤ 2 exp 

(

− n

2σ2

> r

× 2

n σ2 

> r

log 

( 240 SAi 7

> k

δ

)) 

= δ

120 i7

> k

SA 

• If n < 2b2

> r
> σ2
> r

log 

( 240 SAi 7

> k
> δ

)

:

P

(

|r(s, a ) − ˆrk(s, a )| ≥ βrk(s, a )

)

= P

(

|r(s, a ) − ˆrk(s, a )| ≥ 14 br

n log 

( 2SAi k

δ

)) 

≤ P

(

|r(s, a ) − ˆrk(s, a )| ≥ 2br

n log 

( 240 SAi 7

> k

δ

)) 

≤ 2 exp 

(

− n

2br

× 2

n br log 

( 240 SAi 7

> k

δ

)) 

= δ

120 i7

> k

SA 

Similarly for holding times we have: 

P

(

|τ (s, a ) − ˆτk(s, a )| ≥ βτk (s, a )

)

≤ δ

120 i7

> k

SA 

Note that when there hasn’t been any observation, the confidence intervals trivially hold with probability 1.Moreover, Nk(s, a ) < i k by the stopping condition of an episode. Taking a union bound over all possible values of Nk(s, a ) yields: 

P

(

|τ (s, a ) − ˆτk(s, a )| ≥ βτk (s, a )

)

≤ δ

120 i6

> k

SA 

P

(

|r(s, a ) − ˆrk(s, a )| ≥ βrk(s, a )

)

≤ δ

120 i6

> k

SA 

P

(∥∥p(·| s, a ) − ˆpk(·| s, a )∥∥1 ≥ βpk (s, a )

)

≤ δ

20 i6

> k

SA 

Summing over all state-action pairs: P (M 6 ∈ M k) < δ

> 15 i6
> k

.

We now consider the regret of episodes in which the set of plausible SMDPs Mk does not contain the true SMDP M : ∑mk=1 ∆k1M6 ∈M k . By the stopping criterion for episode k (except for episodes where νk(s, a ) = 1 

and Nk(s, a ) = 0 for which ∑

> s∈S

∑ 

> a∈A s

νk(s, a ) = 1 ≤ ik): 

∑

> s∈S

∑

> a∈A s

νk(s, a ) ≤ ∑

> s∈S

∑

> a∈A s

Nk(s, a ) = ik − 1 (19) Exploration–Exploitation in MDPs with Options 

We can thus bound this part of the regret: 

> m

∑

> k=1

∆k1M6 ∈M k ≤

> m

∑

> k=1

∑

> s∈S

∑

> a∈A s

νk(s, a )τ (s, a )ρ∗1M6 ∈M k

≤ τmax ρ∗

> m

∑

> k=1

ik1M6 ∈M k = τmax ρ∗

> n

∑

> i=1

i

> m

∑

> k=1

1i=ik ,M 6 ∈M k

≤ τmax ρ∗

 

> ⌊n1/4⌋

∑

> i=1

i +

> n

∑ 

> i=⌊n1/4⌋+1

i

> m

∑

> k=1

1i=ik ,M 6 ∈M k



≤ τmax ρ∗

√n +

> n

∑ 

> i=⌊n1/4⌋+1

i

> m

∑

> k=1

1i=ik ,M 6 ∈M k



where we defined: τmax = max s,a τ (s, a ) < +∞.By Lemma 5, the probability that the second term in the right hand side of the above inequality is non-zero is bounded by 

> n

∑ 

> i=⌊n1/4⌋

δ

15 i6 ≤ δ

15 n6/4 +

∫ +∞

> n1/4

δ

15 x6 dx ≤ δ

12 n5/4 .

In other words, with probability at least 1 − δ 

> 12 n5/4

:

> m

∑

> k=1

∆k1M6 ∈M k ≤ τmax Rmax 

√n. 

B.3 Episodes with M ∈ M k

Now we assume that M ∈ M k and we start by analysing the regret of a single episode k. By construction, 

Rmax ≥ ˜ρk ≥ ρ∗ − Rmax √ik

hence: 

∆k = ∑

> s∈S

∑

> a∈A s

νk(s, a ) ( τ (s, a )ρ∗ − r(s, a )) ≤ ∑

> s∈S

∑

> a∈A s

νk(s, a ) ( τ (s, a )˜ρk − r(s, a )) + Rmax 

∑

> s∈S

∑

> a∈A s

νk(s, a )

√ik

τ (s, a )=⇒ ∆k ≤ ∑

> s∈S

∑

> a∈A s

νk(s, a ) ( ˜τk(s, a )˜ρk − r(s, a )) + Rmax 

∑

> s∈S

∑

> a∈A s

νk(s, a ) ( τ (s, a ) − ˜τk(s, a )) + Rmax τmax 

∑

> s∈S

∑

> a∈A s

νk(s, a )

√ik

We now need two results about the extended value iteration algorithm. 

Lemma 6. At any iteration i ≥ 0 of EVI (extended value iteration), the range of the state values is bounded as follows, 

∀i ≥ 0, max  

> s∈S

ui(s) − min  

> s∈S

ui(s) ≤ Rmax D(M )

τ , (20) 

where Rmax is an upper-bound on the per-step reward r(s, a )/τ (s, a ), τ is the parameter used in the uniformization of the SMDP M and D(M ) is its diameter (Def. 2). Proof. In Appendix A we show that EVI is value iteration applied to the equivalent MDP ˜M + 

> k, eq

obtained by “uniformizing” the extended SMDP ˜M + 

> k

. Thus, we focus on any SMDP M and its equivalent MDP Meq . Using the same argument as in section 4.3.1 of [Jaksch et al., 2010], we have that: ∀i ≥ 0, max s∈S ui(s)−min s∈S ui(s) ≤Ronan Fruit, Alessandro Lazaric 

Rmax D(Meq ) since all rewards of Meq are bounded by Rmax whenever the average reward in M is bounded by 

Rmax . Thus we need to find a relationship between D(M ) and D(Meq ). Let T (s′) denote the first time at which state s′ is reached in M or Meq , that is In SMDP M : T (s′) = inf 

{ n∑

> i=1

τi : n ∈ N, s n = s′

}

In MDP Meq : T (s′) = inf 

{

n : n ∈ N, s n = s′

}

.

We prove that ∀s, s ′ ∈ S , ∀π ∈ ΠSD M = Π SD M′ , EπM

[T (s′)|s0 = s] = τ EπM′

[T (s′)|s0 = s]. We consider two cases: 1. If PπM

(T (s′) = + ∞| s0 = s) > 0 then necessarily EπM

[T (s′)|s0 = s] = + ∞.Moreover: PπM

(T (s′) = + ∞| s0 = s) > 0 = ⇒ PπMeq 

(T (s′) = + ∞| s0 = s) > 0 and so EπMeq 

[T (s′)|s0 = s] =+∞ = 1 

> τ

EπM

[T (s′)|s0 = s].2. Conversely: PπM

(T (s′) = + ∞| s0 = s) = 0 =⇒ PπMeq 

(T (s′) = + ∞| s0 = s) = 0 in which case both expectations are finite. To prove they are equal up to factor τ , we see the holding time as a “reward” (the true rewards are ignored here). Note that any policy π induces Markov chains with different dynamics on 

M and Meq (different transition probabilities). We call these Markov chains M C and M C eq respectively. Suppose we modify M C as follows: all states that are not reachable from s are ignored, all other states are unchanged except s′ that is assumed to be absorbing (i.e., π(s′) is an action that loops on s′ with probability 1). Furthermore, we build a Markov reward process M R with the same dynamics as M C and such that all transitions (s, π (s)) have an expected reward equal to τ (s, π (s)) except (s′, π (s′)) which has a reward of zero. The total expected reward of this Markov reward process (MRP denoted M R ) starting from s trivially equals EπM

[T (s′)|s0 = s]. Since we assumed that EπM

[T (s′)|s0 = s] is finite, and because all states of M R are reachable from s (the other states were ignored), s′ is reached with probability 1 no matter which starting state s of M R is chosen (or in other words, even though we ignored some states, the transition matrix of M R is stochastic −and not sub-stochastic − and has a single recurrent class consisting of the absorbing state s′). By [Puterman, 1994], the vector (T (s)) 

> s∈S

= (EπM

[T (s′)|s0 = s])  

> s∈S

is the unique solution to the system of equations 

∀s, T (s) = τ (s, d (s)) + ∑

> ˜s

p(˜s|s, d (s)) T (˜s).

Applying the same transformation to M C eq and assigning a reward of 1 to all transitions but (s′, π (s′)) (which has reward 0) in order to build M R eq , we deduce that the vector (T eq (s)) 

> s∈S

= (EπMeq 

[T (s′)|s0 = s])  

> s∈S

is the unique solution to the system of equations 

∀s, T eq (s) = 1 + τ

τ (s, d (s)) 

∑

> ˜s

p(˜s|s, d (s)) T eq (˜s) + 

(

1 − τ

τ (s, d (s)) 

)

T eq (s)

⇐⇒ ∀ s, (τ T eq (s)) = τ (s, d (s)) + ∑

> ˜s

p(˜s|s, d (s)) (τ T eq (˜s)) .

By uniqueness of the solution: τ T eq = T =⇒ τ D (Meq ) = D(M ).

Lemma 7. If the convergence criterion of EVI hold at iteration i, then: 

∀s ∈ S , ∣∣ui+1 (s) − ui(s) − ˜ρk

∣∣ ≤ 1

√ik

(21) 

Proof. We introduce the following quantities 

Mi = max  

> s∈S

{ui+1 (s) − ui(s)}, mi = min  

> s∈S

{ui+1 (s) − ui(s)}, ǫ = 1

√ik

.Exploration–Exploitation in MDPs with Options 

Since EVI is just value iteration applied to MDP M ′

> k

, Theorem 8.5.6 of [Puterman, 1994] hold and we have: 

1

2 (Mi + mi) ≥ ˜ρk − ǫ

2 ⇐⇒ mi ≥ ˜ρk − ǫ

2 − 1

2 (Mi − mi) = ⇒ mi ≥ ˜ρk − ǫ

1

2 (Mi + mi) − ˜ρk ≤ ǫ

2 ⇐⇒ Mi ≤ ˜ρk + ǫ

2 + 1

2 (Mi − mi) = ⇒ Mi ≤ ˜ρk + ǫ. 

In conclusion: 

∀s ∈ S , −1

√ik

≤ ui+1 (s) − ui(s) − ˜ρk ≤ 1

√ik

.

Based on Lemma 7, Eq. 21, and optimiality equation Eq. 14, we have: 

∀s ∈ S ,

∣∣∣∣∣(˜ρk − ˜rk(s, ˜πk (s)) 

˜τk(s, ˜πk(s)) 

)

−

( ∑

> s′∈S

˜pk(s′|s, ˜πk(s)) ui(s′) − ui(s)

)

τ

˜τk(s, ˜πk(s)) 

∣∣∣∣∣ ≤ 1

√ik

(22) Setting rk = (˜rk(s, ˜πk(s)) ) 

> s∈S

to be the column vector of rewards under policy ˜πk, ˜Pk = (˜pk(s′|s, ˜πk(s)) ) 

> s,s ′∈S

the transition matrix and vk = (νk(s, ˜πk(s)) ) 

> s∈S

the row vector of visit counts for each state and the corresponding action chosen by ˜πk. We will use the fact that a 6 = ˜πk(s) = ⇒ νk(s, a ) = 0 .

∆k ≤ ∑

> s,a

νk(s, a ) ( ˜τk(s, a )˜ρk − r(s, a )) + Rmax 

∑

> s,a

νk(s, a ) ( τ (s, a ) − ˜τk(s, a )) + Rmax τmax 

∑

> s,a

νk(s, a )

√ik

= ∑

> s,a

νk(s, a ) ( ˜τk(s, a )˜ρk − ˜rk(s, a )) + ∑

> s,a

νk(s, a ) ( ˜rk(s, a ) − r(s, a )) + Rmax τmax 

∑

> s,a

νk(s, a )

√ik

+ Rmax 

∑

> s,a

νk(s, a ) ( τ (s, a ) − ˜τk(s, a )) 

We will now upper-bound the four terms of the right-hand side of the above inequality. Setting cr =max {14 br, √14 σr } and cτ = max {14 bτ , √14 στ } we have: 

˜rk(s, a ) − r(s, a ) ≤ ∣∣˜rk(s, a ) − ˆrk(s, a )∣∣ + ∣∣ˆrk(s, a ) − r(s, a )∣∣ ≤ 2βrk(s, a ) ≤ 2cr

log(2 SAi k/δ )

√max {1, N k(s, a )}

τ (s, a ) − ˜τk(s, a ) ≤ ∣∣˜τk(s, a ) − ˆτk(s, a )∣∣ + ∣∣ˆτk(s, a ) − τ (s, a )∣∣ ≤ 2βτk (s, a ) ≤ 2cτ

log(2 SAi k/δ )

√max {1, N k(s, a )}

Finally, using 22 and noting that ˜τk(s, a ) ≤ τmax (by construction) we obtain: 

˜τk (s, a )˜ρk − ˜rk(s, a ) ≤ Rmax τmax 

√ik

+ τ

( ∑

> s′∈S

˜pk(s′|s, ˜πk(s)) ui(s′) − ui(s)

)

, if a = ˜πk(s)=⇒ ∑

> s,a

νk(s, a ) ( ˜τk(s, a )˜ρk − ˜rk (s, a )) ≤ Rmax τmax 

∑

> s,a

νk(s, a )

√ik

+ τ

(

vk

( ˜Pk − I)ui

)

where i is the iteration at which the stopping condition of EVI holds. Defining the column vector wk by: 

wk(s) = ui(s) − min s∈S ui(s) + max s∈S ui(s)

2Ronan Fruit, Alessandro Lazaric 

and since the rows of ˜Pk sum to one, we have: vk

( ˜Pk − I)ui = vk

( ˜Pk − I)wk. Moreover, by Lemma 6: ‖wk‖∞ ≤  

> Rmax D
> 2τ

. Noting that max {1, N k(s, a )} ≤ ik ≤ n we get: 

∆k ≤ τ

(

vk

( ˜Pk − I)wk

)

+ 2 

(

Rmax τmax + ( cr + Rmax cτ ) log 

( 2SAn 

δ

)) ∑

> s,a

νk(s, a )

√max {1, N k(s, a )}

Using exactly the same arguments as in Jaksch et al. [2010], it is trivial to prove that with probability at least 

1 − δ 

> 12 n5/4

:

> m

∑

> k=1

vk

( ˜Pk − I)wk1M∈M k ≤ Rmax D

τ

[√ 

14 S log 

( 2An 

δ

) m∑

> k=1

∑

> s,a

νk(s, a )

√max {1, N k(s, a )} +

√

5

2 n log 

( 8n

δ

)

+SA log 2

( 8n

SA 

) ]

Lemma 8. Consider a sequence of positive reals (zk)k and define: ∀k, Z k = max {1, ∑ki=1 zi}. Assuming that 

0 ≤ zk ≤ Zk−1 we have: 

∀n ≥ 1,

> n

∑

> k=1

zk

√Zk−1

≤ (√2 + 1 )√ Zn

Proof. See Appendix C.3 of [Jaksch et al., 2010]. 

Using Lemma 8 we get: 

> m

∑

> k=1

∑

> s,a

νk(s, a )

√max {1, N k(s, a )} ≤ (√2 + 1 ) ∑ 

> s,a

√N (s, a )

By Jensen’s inequality we thus have: 

> m

∑

> k=1

∑

> s,a

νk(s, a )

√max {1, N k(s, a )} ≤ (√2 + 1 )√SAn 

In conclusion, when M ∈ M k, with probability at least 1 − δ 

> 12 n5/4

:

> m

∑

> k=1

∆k1M∈M k ≤ Rmax D

√

5

2 n log 

( 8n

δ

)

+ Rmax DSA log 2

( 8n

SA 

)

+ ( √2 + 1) 

[

2Rmax τmax 

+2( cr + Rmax cτ ) log 

( 2SAn 

δ

)

+ Rmax D

√

14 S log 

( 2An 

δ

)]√SAn 

B.4 Computing the final bound 

Gathering all previous inequalities, we have that with probability at least 1 − 3δ 

> 12 n5/4

= 1 − δ 

> 4n5/4

:

∆( M, A, s, n ) ≤ (γr + γτ Rmax ) log 

( 13 n

δ

) √n + τmax Rmax 

√n + Rmax D

√

5

2 n log 

( 8n

δ

)

+ ( √2 + 1) 

[

2τmax + 2( cr + Rmax cτ ) log 

( 2SAn 

δ

)

+ Rmax D

√

14 S log 

( 2An 

δ

)]√SAn 

+ Rmax DSA log 2

( 8n

SA 

)Exploration–Exploitation in MDPs with Options 

In [Jaksch et al., 2010] (see Appendix C.4), it is shown that when n > 34 A log ( n

> δ

):

DSA log 2

( 8n

SA 

)

< 2

34 DS 

√

An log 

( n

δ

)

, and log 

( 2An 

δ

)

≤ 2 log 

( n

δ

)

and moreover if n > S log ( n

> δ

) and A ≥ 2 (if A = 1 the regret is zero): 

n2

δ2 ≥ nS log ( n

> δ

)

δ ≥ nS 

δ =⇒ n2A2

δ2 ≥ 2SAn 

δ =⇒ 4 log 

( n

δ

)

≥ 2 log 

( An 

δ

)

≥ log 

( 2SAn 

δ

)

=⇒ ∆( M, A, s, n ) = O

(( 

D√S + τmax +

( Cr

Rmax 

+ Cτ

) √ 

log 

( n

δ

))

Rmax 

√

SAn log 

( n

δ

))

where Cr = max {br, σ r } and Cτ = max {bτ , σ τ }.Note that if n ≤ 34 A log ( n

> δ

) then we trivially have: 

> m

∑

> k=1

∆k ≤ τmax Rmax n = τmax Rmax (√n)2 ≤ 34 τmax Rmax 

√

An log 

( n

δ

)

and if n ≤ S log ( n

> δ

):

> m

∑

> k=1

∆k ≤ τmax Rmax n = τmax Rmax (√n)2 ≤ τmax Rmax 

√

Sn log 

( n

δ

)

and thus the previous bound on the whole regret still holds. Taking a union bound over all possible values of 

n ≥ 1 we have that with probability at least 1 − δ:

∀n ≥ 1, ∆( M, A, s, n ) = O

(( 

D√S + τmax +

( Cr

Rmax 

+ Cτ

) √ 

log 

( n

δ

))

Rmax 

√

SAn log 

( n

δ

))

.

The derivation for the case of bounded holding times is exactly the same with different concentration inequalities applied to estimates ̂ τ (s, a ). Note that all the terms in the upper bound are very similar to those appearing in the derivation of the upper bound for MDPs, thus the constants in the big O are very close. This justifies the analysis of the ratio between the two upper bounds in Sect. 5. 

## C The Lower Bound (Theorem 2) 

C.1 Lower Bound for SMDPs 

We will derive the lower bound by applying the same techniques as in the proof of the lower bound for MDPs (section 6 of [Jaksch et al., 2010]). We first consider the two-state SMDP M ′ depicted in Fig. 4. Since by assumption D 

> 12

> T min and Tmax  

> 3

> T min , let τ ∈ ]Tmin , min { D 

> 12

, Tmax 

> 3

}] . Define p = τ 

> Tmax

and δ = 4τ 

> D

. By definition of τ we have: p, δ ≤ 1 

> 3

. There are A′ = ⌊ A−1 

> 2

⌋ actions available in each state of M ′. We assume that 

∀(s, a, s ′) ∈ S × A s × S and ∀i ≥ 0, ri(s, a, s ′) and τi(s, a, s ′) are independent. We also assume that ∀i ≥ 0,

τi(si−1, a i, s i) and ri(si−1, a i, s i) are independent of the next state si and we write: τi(si−1, a i) and ri(si−1, a i).For each action a in As0 , r(s0, a ) = 0 and τ (s, a ) ∼ τ where τ is a r.v. defined in Table 1. Moreover, for all actions a but a specific action a∗

> 0

, p(s1|s0, a ) = δ whereas p(s1|s0, a ∗

> 0

) = δ + ǫ for some 0 < ǫ < δ specified later in the proof. For all actions a in As1 , p(s0|s1, a ) = δ and τ (s1, a ) ∼ τ . Finally, r(s1, a ) ∼ r for all actions a except 

a∗ 

> 1

for which r(s1, a ∗

> 1

) ∼ r∗, where r and r∗ are r.v. defined in Table 1 where 0 < η < p will be defined later in the proof. Note that since η < τ 

> Tmax

, we have: r ≤ τ R max and r∗ ≤ τ R max which satisfies the definition of Rmax 

given in assumption 1. We denote E[·| s] the expectation conditionally on starting in state s.Let’s define T (s1) = inf {t : st = s1} the first time in which s1 is encountered. ∀d∞ ∈ ΠSD M′ such that d(s0) 6 = a∗

> 0

Ronan Fruit, Alessandro Lazaric 

s0 s1

1 − δ, τ, 0

δ, τ, r 

δ, τ, 0

1 − δ, τ, r 

δ + ǫ, τ, 0

δ, τ, r ∗

1 − δ − ǫ, τ, 0

1 − δ, τ, r ∗

Figure 4: The two-state SMDP M ′ for the lower-bound on SMDPs. The two special actions a∗ 

> 0

and a∗ 

> 1

are shown as dashed lines. we have: 

Ed∞

[T (s1)|s0] = Ed∞



> +∞

∑

> n=1

( n∑

> i=1

τi(si−1, a i, s i)

) 

> n−1

∏

> j=0

1sj =s0

 1sn =s1

∣∣∣∣∣s0



=

> +∞

∑

> n=1

Ed∞

( n∑

> i=1

τi(s0, d (s0)) 

) 

> n−1

∏

> j=0

1sj =s0

 1sn =s1

∣∣∣∣∣s0



=

> +∞

∑

> n=1

Ed∞

[ n∑

> i=1

τi(s0, d (s0)) 

∣∣∣∣∣s0

]

Ed∞



> n−1

∏

> j=0

1sj =s0

 1sn =s1

∣∣∣∣∣s0



=

> +∞

∑

> n=1

nτ × δ(1 − δ)n−1 = τ

δ

We used the fact that τi is independent of the next state si and that τ = E[τ ]. We can compute Ed∞

[T (s1)|s0]

with d(s0) = a∗ 

> 0

and Ed∞

[T (s0)|s1] (for both d(s0) 6 = a∗ 

> 0

and d(s0) = a∗

> 0

) similarly. The diameter of SMDP M ′

is thus: 

D′ = max 

{

min 

{ τ

δ , τ

δ + ǫ

}

, min 

{ τ

δ , τ

δ

}} 

= max 

{ τ

δ + ǫ , τ

δ

}

= τ

δ

Any policy d∞ ∈ ΠSD M′ induces a recurrent Markov Chain on M ′. Let’s denote by P ∗ 

> d

the limiting matrix of this Markov Chain. We know (see [Puterman, 1994]) that P ∗ 

> d

= eμ ⊺ 

> d

where μd = (1 − pd, p d)⊺ is the stationary distribution of the recurrent Markov Chain. The probability pd can take only two different values: pd = 1 

> 2

if and only if d(s0) 6 = a∗

> 0

, and pd = δ+ǫ 

> 2δ+ǫ

if and only if d(s0) = a∗

> 0

. Using criterion 3 of Definition 3, the gain yielded by 

d∞ has the form: 

ρd = pdX

(1 − pd)τ + pdτ = pdX

τ

where X = r if and only if d(s1) 6 = a∗

> 1

, and X = r∗ if and only if d(s1) = a∗

> 1

. Since r∗ > r, the optimal decision rule d∗ must satisfy: d∗(s1) = a∗

> 1

. Similarly, since δ+ǫ 

> 2δ+ǫ

> 1 

> 2

we must have: d∗(s0) = a∗

> 0

. The optimal gain is thus: 

ρ∗ = Rmax 

2 × (δ + ǫ) ( τ + ηT max )

(2 δ + ǫ) τ

The actual SMDP M that we will use to prove the lower bound is built by considering k = ⌊ S 

> 2

⌋ copies of the two-state SMDP M ′, where only one of the copies has such "good" actions a∗ 

> 0

and a∗ 

> 1

(all the other copies have the exact same number of actions as M ′, but all actions are identical). A′ + 1 additional actions with deterministic transitions are introduced in every s0-state. The reward for each of those actions is zero and the Exploration–Exploitation in MDPs with Options 

R.v. X Xmin Xmax P(X = Xmin ) P(X = Xmax ) E[X]

τ Tmin Tmax > 0 > 0 τ

r 0 1 

> 2

Rmax Tmax 1 − p p 1 

> 2

τ R max 

r∗ 0 1 

> 2

Rmax Tmax 1 − p − η p + η 1 

> 2

(τ R max + ηT max Rmax )

Table 1: Definition of random variables τ , r and r∗.holding time is Tmin . These actions connect the s0-states of the k copies in a A′-ary tree structure on the s0


> 4

+ Tmin ⌈log A′ k⌉) ≤ D. All holding times of M are in [Tmin , T max ], and all rewards are in [0 , 1 

> 2

Rmax Tmax ]. For all (s, a ) ∈ S × A s we have: r(s, a ) ≤ τ (s, a )Rmax . Moreover, M has at most S states and A actions per state. For the analysis, we will study the simpler-to-learn SMDP M ′′ where all s0-states are merged together as well as all s1-states. The "merged" s0-state is set to be the initial state. M ′′ is thus equivalent to the two-state SMDP 

M ′ with kA ′ available actions in both s0 and s1. Let’s assume that the learning algorithm A used is fixed. The probability distribution of the stochastic process (s0, a 0, τ 0, r 0, s 1, ... ) is denoted: 

• Pa0 ,a 1 when (a0, a 1) are the best actions in respectively s0 and s1,

• P∗ when the pair (a0, a 1) identifying the best actions is first chosen uniformly at random from {1, ..., kA ′} × {1, ..., kA ′} before algorithm A starts, 

• Punif 0,a 1 when the pair a1 is the best action in s1 and ǫ = 0 (no-optimal actions in s0), 

• Pa0,unif 1 when the pair a0 is the best action in s0 and η = 0 (no-optimal actions in s1). By construction, it is trivial to see that: E∗[∆( M, A, s, n )] ≥ E∗[∆( M ′′ , A, s, n )] (M ′′ is easier to learn). We will show that E∗[∆( M ′′ , A, s 0, n )] = Ω 

(( √D′ + √Tmax 

)

Rmax 

√kA ′n

)

and the same result can be proved with initial state s1 using similar arguments. This will necessarily imply that there exists at least one choice of pair 

(a0, a 1) for which, for all states s we have: Ea0,a 1 [∆( M, A, s, n )] = Ω 

(( √D + √Tmax 

)

Rmax 

√SAn 

)

.As already argued by [Jaksch et al., 2010], for the analysis it is sufficient to consider algorithms with deterministic strategies for choosing actions. We assume algorithm A is run for n decision steps, which means that n + 1 states are visited in total (including the last state in which no action is taken). Let’s denote by N0 and N1 the number of visits in states s0 and s1

respectively, last state excluded. For any (a, a) ∈ A s0 × A s1 , let’s denote by N a 

> 0

and N a 

> 1

the respective number of times actions a and a are taken. Finally, let’s denote by N ∗ 

> 0

and N ∗ 

> 1

the respective number of times best actions in s0 and s1 are taken. The SMDP M ′′ has the same transition probabilities as the MDP considered by [Jaksch et al., 2010] and we can use their proof to show that for any choice of best actions (a0, a 1):

Eunif 0,a 1 [N1] ≥ n

2 − 1

2δ = n

2 − D′

2τ

Ea0,a 1 [N1] ≤ n

2 + Ea0,a 1 [N ∗ 

> 0

]ǫ

δ + 1

2δ = n

2 + Ea0,a 1 [N a0 

> 0

]ǫD ′

2τ + D′

2τ

The regret is defined as: 

E∗[∆( M ′′ , A, s 0, n )] = E∗

[ n∑

> i=1

τi(si−1, a i, s i)

]

ρ∗ − E∗

[ n∑

> i=1

ri(si−1, a i, s i)

]

where the total duration is simply: 

E∗

[ n∑

> i=1

τi(si−1, a i, s i)

]

=

> n

∑

> i=1

E∗ [τi(si−1, a i)] = nτRonan Fruit, Alessandro Lazaric 

and the cumulated reward is given by: 

E∗

[ n∑

> i=1

ri(si−1, a i, s i)

]

=

> n

∑

> i=1

E∗

[ri(s1, a ∗

> 1

)1si−1 =s1 ,a i=a∗ 

> 1

+ ri(s1, a i 6 = a∗

> 1

)1si−1 =s1 ,a i6 =a∗

> 1

]

= E∗

[

r∗

(n−1∑

> i=0

1si=s1 ,a i+1 =a∗

> 1

)

+ r

(n−1∑

> i=0

1si =s1 ,a i+1 6 =a∗

> 1

)] 

= E∗ [r (N1 − N ∗ 

> 1

) + r∗N ∗ 

> 1

]= E∗ [rN 1 + ( r∗ − r)N ∗ 

> 1

]= Rmax 

2 τ E∗ [N1] + η Rmax 

2 Tmax E∗[N ∗ 

> 1

]

hence the formula: 

E∗[∆( M ′′ , A, s 0, n )] = τ

(

nρ ∗ − Rmax 

2 E∗[N1]

)

− η Rmax 

2 Tmax E∗[N ∗ 

> 1

] (23) 

Lemma 9. Let f : {s0, s 1}n+1 × { Tmin , T max }n × { 0, 1 

> 2

Rmax Tmax }n → [0 , M ] be any function defined on state/reward sequence (sn+1 , τ n, rn) ∈ { s0, s 1}n+1 × { Tmin , T max }n × { 0, 1 

> 2

Rmax Tmax }n observed in the SMDP 

M ′′ . Then for any n ≥ 1, any 0 ≤ δ ≤ 1 

> 2

, any 0 ≤ ǫ ≤ 1 − 2δ, any 0 ≤ p ≤ 1 

> 2

, any 0 ≤ η ≤ 1 − 2p, and any 

(a0, a 1) ∈ { 1, ..., kA ′} × { 1, ..., kA ′}:

∣∣∣∣Ea0,a 1

[f (sn+1 , τ n, rn)] − Eunif 0,a 1

[f (sn+1 , τ n, rn)] ∣∣∣∣ ≤ M

2

ǫ

√δ

√

2Eunif 0,a 1 [N a0 

> 0

]

∣∣∣∣Ea0,a 1

[f (sn+1 , τ n, rn)] − Ea0 ,unif 1

[f (sn+1 , τ n, rn)] ∣∣∣∣ ≤ M

2

η

√p

√

2Ea0,unif 1 [N a1 

> 1

]

Proof. We refer the reader to Appendix E of [Jaksch et al., 2010] where a similar Lemma is proved for the MDP-analogue of SMDP M ′′ . In the following, we will only stress the main difference with the proof in [Jaksch et al., 2010]. We know from information theory that: 

∣∣∣∣Ea0,a 1

[f (sn+1 , τ n, rn)] − Eunif 0,a 1

[f (sn+1 , τ n, rn)] ∣∣∣∣ ≤ M

2

√

2 log(2) KL (Punif 0,a 1 ‖Pa0,a 1 )

∣∣∣∣Ea0,a 1

[f (sn+1 , τ n, rn)] − Ea0,unif 1

[f (sn+1 , τ n, rn)] ∣∣∣∣ ≤ M

2

√

2 log(2) KL (Pa0 ,unif 1‖Pa0,a 1 )

By the chain rule of Kullback–Leibler divergences, it holds that: 

KL (Pa0 ,unif 1‖Pa0,a 1 ) = 

> n

∑

> i=1

KL (Pa0 ,unif 1(si, τ i, r i|si−1, τ i−1, ri−1)‖Pa0,a 1 (si, τ i, r i|si−1, τ i−1, ri−1))

where KL (P(si, τ i, r i|si−1, τ i−1, ri−1)‖Q(si, τ i, r i|si−1, τ i−1, ri−1)) =

∑     

> si∈S i,τi∈T ,ri∈R i

P(si, τ i−1, ri) log 2

( P(si, τ i, r i|si−1, τ i−1, ri−1)

Q(si, τ i, r i|si−1, τ i−1, ri−1)

)

with S = {s0, s 1}, T = {Tmin , T max } and R = {0, 1 

> 2

Rmax Tmax }. The same holds for Punif 0,a 1 .Similarly to [Jaksch et al., 2010] and using the independence between si, τi and ri, we obtain: 

KL (Punif 0,a 1 (si, τ i, r i|si−1, τ i−1, ri−1)‖Pa0,a 1 (si, τ i, r i|si−1, τ i−1, ri−1))

= Punif 0,a 1 (si−1 = s0, a i = a0) ∑   

> s′∈S ,τ ′∈T ,r ′∈R

Punif 0,a 1 (s′, τ ′, r ′|s0, a 0) log 2

( Punif 0,a 1 (s′, τ ′, r ′|s0, a 0)

Pa0 ,a 1 (s′, τ ′, r ′|s0, a 0)

)

= Punif 0,a 1 (si−1 = s0, a i = a0) ∑ 

> s′∈S

Punif 0,a 1 (s′|s0, a 0) log 2

( Punif 0,a 1 (s′|s0, a 0)

Pa0,a 1 (s′|s0, a 0)

)

= Punif 0,a 1 (si−1 = s0, a i = a0)

(

δ log 2

( δ

δ + ǫ

)

+ (1 − δ) log 2

( 1 − δ

1 − δ − ǫ

)) Exploration–Exploitation in MDPs with Options 

KL (Pa0 ,unif 1(si, τ i, r i|si−1, τ i−1, ri−1)‖Pa0,a 1 (si, τ i, r i|si−1, τ i−1, ri−1))

= Pa0 ,unif 1(si−1 = s1, a i = a1) ∑   

> s′∈S ,τ ′∈T ,r ′∈R

Pa0 ,unif 1(s′, τ ′, r ′|s1, a 1) log 2

( Pa0,unif 1(s′, τ ′, r ′|s1, a 1)

Pa0 ,a 1 (s′, τ ′, r ′|s1, a 1)

)

= Pa0 ,unif 1(si−1 = s1, a i = a1) ∑

> r′∈R

Pa0,unif 1(r′|s1, a 1) log 2

( Pa0 ,unif 1(r′|s1, a 1)

Pa0,a 1 (r′|s1, a 1)

)

= Pa0 ,unif 1(si−1 = s1, a i = a1)

(

p log 2

( p

p + η

)

+ (1 − p) log 2

( 1 − p

1 − p − η

)) 

Using Lemma 20 of [Jaksch et al., 2010] we have that under conditions 0 ≤ δ ≤ 1 

> 2

, 0 ≤ ǫ ≤ 1 − 2δ, 0 ≤ p ≤ 1 

> 2

,and 0 ≤ η ≤ 1 − 2p the following inequalities hold: 

δ log 2

( δ

δ + ǫ

)

+ (1 − δ) log 2

( 1 − δ

1 − δ − ǫ

)

≤ ǫ2

δ log(2) 

and p log 2

( p

p + η

)

+ (1 − p) log 2

( 1 − p

1 − p − η

)

≤ η2

p log(2) 

which concludes the proof. 

Note that by assumption: ǫ ≤ δ ≤ 1 

> 3

≤ 1 − 2δ and η ≤ p ≤ 1 

> 3

≤ 1 − 2p.We can bound E∗ [N1] using Lemma 9 as is done in [Jaksch et al., 2010]. This is because N1 can be written as a function of (sn+1 , τ n, rn). Since the computations are rigorously the same except that δ = τ 

> D′

instead of 1 

> D′

,we give the results without any further details: 

E∗ [N1] ≤ n

2 + D′

2τ + ǫnD ′

2τ kA ′ + ǫD ′2

2τ 2kA ′ + ǫ2nD ′

2τ kA ′

√ D′kA ′n

τ + ǫ2nD ′2

2τ 2kA ′

√kA ′

Taking into account the fact that by assumption n ≥ DSA ≥ 16 D′kA ′ we get: 

E∗ [N1] ≤ n

2 + D′

2τ + ǫnD ′

τ

( 1

2kA ′ + 1

32 τ k 2A′2

)

+ ǫ2nD ′

τ kA ′

√ D′kA ′n

τ

( 1

2 + 1

8√kA ′

)

(24) Given that δ ≥ ǫ ≥ 0 we have the following inequality: 

ρ∗ − Rmax 

4 = Rmax 

2 × ǫτ + ( δ + ǫ)ηT max 

2(2 δ + ǫ)τ ≥ Rmax 

2 ×

( ǫD ′

6τ + ηT max 

6τ

)

(25) Applying Lemma 9 ( N ∗ 

> 1

is a function of (sn+1 , τ n, rn)) and Jensen’s inequality we get ∀a0 ∈ { 1, ..., kA ′}:

E∗ [N ∗ 

> 1

] = 1

kA ′

> kA ′

∑

> a1=1

Ea0,a 1 [N a1 

> 1

] ≤ Ea0,unif 1 [N1]

kA ′ + n

2kA ′ η

√ 2kA ′Tmax 

τ Ea0 ,unif 1 [N1]

We will now derive an upper-bound on Ea0,unif 1 [N1].

Lemma 10. Let (un)n∈N ∈ RN be any real sequence satisfying the following arithmetico-geometric recurrence relation: 

∀n ∈ N, un+1 ≥ qu n + r where (q, r ) ∈ R \ { 1} × R

Then we have that: 

∀n ∈ N, un ≥

(

u0 − r

1 − q

)

αn + r

1 − qRonan Fruit, Alessandro Lazaric 

Proof. Defining sequence vn = un − r 

> 1−q

, we have: 

∀n ∈ N, vn+1 = un+1 − r

1 − q ≥ qu n + r − r

1 − q = q

(

un − r

1 − q

)

= qv n

By trivial induction we get: ∀n ∈ N, vn ≥ v0qn. The result follows by replacing vn by un − r 

> 1−q

.

By the law of total probability and since Pa0 ,unif 1 (si = s0) + Pa0 ,unif 1 (si = s1) = 1 we have: 

∀i ≥ 0, Pa0 ,unif 1 (si+1 = s0) = Pa0,unif 1 (si+1 = s0|si = s0) Pa0 ,unif 1 (si = s0)+ Pa0 ,unif 1 (si+1 = s0|si = s1) Pa0,unif 1 (si = s1)=Pa0,unif 1 (si = s0) (Pa0,unif 1 (si+1 = s0|si = s0)

− Pa0 ,unif 1 (si+1 = s0|si = s1) ) + Pa0 ,unif 1 (si+1 = s0|si = s1)

≥Pa0,unif 1 (si = s0) (1 − 2δ − ǫ) + δ

Since the initial state is s0 and 2δ + ǫ ≤ 3δ we have by Lemma 10: 

∀i ≥ 0, Pa0,unif 1 (si = s0) ≥

(

1 − δ

2δ + ǫ

)

(1 − 2δ − ǫ)i + δ

2δ + ǫ ≥ 1

3=⇒ Ea0,unif 1 [N0] = 

> n

∑

> i=0

Pa0,unif 1 (si = s0) ≥ n

3=⇒ Ea0,unif 1 [N1] ≤ 2n

3=⇒ E∗ [N ∗ 

> 1

] ≤ 2n

3kA ′ + nη 

kA ′

√ Tmax nkA ′

3τ

Hence the bound: 

ηT max E∗ [N ∗ 

> 1

] ≤ 2nηT max 

3kA ′ + nη 2Tmax 

kA ′

√ Tmax nkA ′

3τ (26) By setting ǫ = c

√ kA ′ 

> nD ′

and η = κ

√ kA ′ 

> nT max

and incorporating inequalities 24, 25 and 26 into inequality 23 we obtain: 

E∗[∆( M ′′ , A, s 0, n )] ≥

[ c

6 − c

2kA ′ − c

32 k2A′2τ − c2

2√τ − c2

8√kA ′τ − 1

8kA ′

] Rmax 

2

√D′kA ′n

+

[ κ

6 − 2κ

3kA ′ − κ2

√3τ

] Rmax 

2

√Tmax kA ′n

≥

[ c

6 − c

2kA ′ − c

32 k2A′2 − c2

2 − c2

8√kA ′ − 1

8kA ′

] Rmax 

2

√D′kA ′n

+

[ κ

6 − 2κ

3kA ′ − κ2

√3

] Rmax 

2

√Tmax kA ′n

For the second inequality, we used the fact that τ > T min ≥ 1 (by assumption). If c and κ are sufficiently small, then the conditions of lemma 9 are indeed satisfied and the above polynomials in c and κ are non-negative. For example, if c = κ = 1 

> 5

:

n ≥ DSA ≥ 16 D′kA ′ =⇒ ǫ = 1

5

√ kA ′

nD ′ ≤ δ

20 < δ n ≥ Tmax SA ≥ 4Tmax kA ′ =⇒ η = 1

5

√ kA ′

nT max 

≤ p

10 < p 

and E∗[∆( M ′′ , A, s 0, n )] ≥ 0.0015 ×

(√D′ + √Tmax 

)

Rmax 

√kA ′nExploration–Exploitation in MDPs with Options 

s0 s1

1 − δ, τ, 0

δ, τ, r 

δ, τ, 0

1 − δ, τ, r 

δ + ǫ, τ, 0

δ, τ ∗, r ∗

1 − δ − ǫ, τ, 0

1 − δ, τ ∗, r ∗

Figure 5: The two-state SMDP M ′ for the lower-bound on MDPs with options. The two special actions a∗ 

> 0

and 

a∗ 

> 1

are shown as dashed lines. 

C.2 Lower Bound for MDPs with options 

We first note that SMDP M ′ depicted in Fig. 4 cannot be converted into an MDP with options. This is due to the fact that τi(si−1, a i, s i) and ri(si−1, a i, s i) were assumed to be independent and the fact that P(r∗ = 

> 1
> 2

Rmax Tmax ) > P(τ = Tmax ). However, it is possible to prove a slightly smaller lower bound for a family of SMDPs that can be transformed into an equivalent MDP with options. We will first present the SMDPs and the lower bound and then we will describe how to transform them into an MDP with options. The family of SMDPs is constructed in the same way as previously except that we use a slightly different SMDP 

M ′, represented on Fig. 5 with the random variables given in Table 2. We take: p = 1  

> 2( Tmax −Tmin )

and δ = 4τ 

> D

.By assumption p < 1 

> 3

and δ < 1 

> 2

. As before, we assume that for all i, τi(si−1, a i, s i) and ri(si−1, a i, s i) are independent of the next state si. But the main difference with the previous lower bound is that we assume that 

ri and τi are strongly correlated, namely: ri(si−1, a i, s i) = Rmax 1{si−1 =s1 }τi(si−1, a i). We assume ǫ ≤ δ and 

η ≤ 1 − 2p. The optimal gain of M ′ is reached when a∗ 

> 0

and a∗ 

> 1

are chosen in s0 and s1 respectively and is equal to: 

ρ∗ = Rmax × (δ + ǫ) ( τ + η(Tmax − Tmin )) 

(2 δ + ǫ) τ + ( δ + ǫ) ( Tmax − Tmin )

By adapting the proof of the lower bound for general SMDPs, we can obtain the following result: 

E∗[∆( M ′′ , A, s 0, n )] ≥

[ c

6 − c

2kA ′ − c

32 k2A′2τ − c2

2√τ − c2

8√kA ′τ − 1

8kA ′

]

Rmax 

√D′kA ′n

+

[

κ

6 − 2κ

3kA ′ − κ2

√3/2

]

Rmax 

√(Tmax − Tmin )kA ′n

≥

[ c

6 − c

2kA ′ − c

32 k2A′2 − c2

2 − c2

8√kA ′ − 1

8kA ′

]

Rmax 

√D′kA ′n

+

[

κ

6 − 2κ

3kA ′ − κ2

√3/2

]

Rmax 

√(Tmax − Tmin )kA ′n

by setting ǫ = c

√ kA ′ 

> nD ′

and η = κ

√ kA ′  

> n(Tmax −Tmin )

. It is then possible to tune c and κ so that ǫ and η satisfy the constraints and: 

E∗[∆( M ′′ , A, s 0, n )] = Ω 

(( √D′ + √Tmax − Tmin 

)

Rmax 

√kA ′n

)

SMDPs M ′ and M ′′ can be transformed into equivalent MDPs with options. We illustrate this transformation on Fig. 6 for an action a1 ∈ A s1 different than a∗

> 1

. The same method can be applied for the other actions. The idea consists in adding new states (blank states in Fig. 6) and primitive actions between those states. Note that the states added are just "hidden" states from which no option can be started. Thus, they should not be counted in the number of states for the lower bound. In our example it is sufficient to consider primitive actions with constant (i.e., deterministic) reward. On Fig. 6 we give the probabilities of each primitive action when 

a1 ∈ A s1 \ { a∗

> 1

} is executed. Ronan Fruit, Alessandro Lazaric 

R.v. X Xmin Xmax P(X = Xmin ) P(X = Xmax ) E[X]

τ Tmin Tmax 1 − p p τ = Tmin + p(Tmax − Tmin )

τ ∗ Tmin Tmax 1 − p − η p + η τ + η(Tmax − Tmin )

r Rmax Tmin Rmax Tmax 1 − p p τ R max 

r∗ Rmax Tmin Rmax Tmax 1 − p − η p + η τ R max + ηR max (Tmax − Tmin )

Table 2: Definition of random variables τ , τ ∗, r and r∗.

s0 s1

(1 − p)δ, r = Rmax 

p(1 − δ), r = Rmax 

1, r = Rmax 

1, r = Rmax 

pδ, r = Rmax 

1, r = Rmax 

1, r = Rmax 

(1 − p)(1 − δ), r = Rmax 

Figure 6: Decomposition of an action a1 ∈ A s1 \ { a∗

> 1

} into a set of primitive actions in an MDP. In this example, 

Tmax = 3 and Tmin = 1 .

## D Distribution of the holding time and reward of a finite Markov option (Lem. 3) 

We denote by R+ and R+∗ the set of positive and non-negative reals respectively. For the definition of sub-exponential random variables, we refer to Def. 4, while sub-Gaussian random variables are defined as follows. 

Definition 5 (Wainwright [2015]) . A random variable X with mean μ < +∞ is said to be sub-Gaussian if and only if there exists σ ∈ R+ such that: 

E[eλ(X−μ)] ≤ e σ2 λ2 

> 2

for all λ ∈ R. (27) A finite 7 Markov option can be seen as an absorbing Markov Chain together with a reward process (i.e., a finite Markov option can be seen as an absorbing Markov Reward Process). To see this we add a new state ˜s for every state s for which βo(s) > 0. We then add a transitions from s to ˜s with probability βo(s) > 0 and reward 0, and we add a self-loop on ˜s with probability 1 and reward 0 ( ˜s is an absorbing state). The Markov Reward Process obtained is indeed absorbing since we assumed the option to be a.s. finite, and it is equivalent to the original option (same reward and holding time). Let’s denote by P the transition matrix of the Markov Chain. In canonical form we have: 

P =

[Q R

0 Ir

]

where r is the number of absorbing states, Ir is the identity matrix of dimension r, Q is the transition matrix between non-absorbing states and R the transition matrix from non-absorbing to absorbing states. If the option is a.s. finite then Q is necessarily (strictly) sub-stochastic ( Qe ≤ e where e = (1 , ..., 1) ⊺ and ∃j s.t. (Qe )j < 1) and irreducible (no recurrent class). It is well-known that such a matrix has a spectral radius strictly smaller than 1 (ρ(Q) < 1) and thus I − Q is invertible (where I is the identity matrix). The holding time τ (s, o, s ′) of any option 

o is defined as the first time absorbing state s′ is reached starting from state s: inf {n ≥ 1 : sn = s′ with s0 = s}

where (sn)n is the sequence of states in the absorbing Markov Chain defined by o. It is well-known in the literature [Peter Buchholz, 2014] that this type of stopping times have Discrete Phase-Type distributions, with probability mass function given by: 

∀k ∈ N∗, P(τ (s, a, s ′) = k) = e⊺ 

> s

Qk−1Re s′

> 7

Note that if at least one option is not (almost surely) finite, the learning agent can potentially be stuck executing that option forever and the problem is ill-posed. Exploration–Exploitation in MDPs with Options 

where es = (0 , 0, ... 0, 1, 0, ..., 0) ⊺ is a vector of all zeros except in state s where it equals 1. These distributions generalize the geometric distribution (defined in dimension 1) to higher dimensions. The Laplace transform can be computed as follows (we simplify notations and denote: τ ← τ (s, o, s ′) and τ ← τ (s, o, s ′) = E[τ (s, o, s ′)] ): 

E

[

eλ(τ −τ )]

=

> ∞

∑

> k=1

eλ(k−τ )e⊺ 

> s

Qk−1Re s′ = eλ(1 −τ )e⊺

> s

[ ∞∑

> k=0

(eλQ)k

]

Re s′

The term ∑∞

> k=0

(eλQ)k is finite if and only if eλρ(Q) < 1, in which case we have: 

E

[

eλ(τ −τ )]

= eλ(1 −τ )e⊺

> s

(I − eλQ)−1 Re s′

and otherwise: E [eλ(τ −τ)] = + ∞. Note that eλρ(Q) < 1 if and only if either λ < − log ( ρ(Q)) or ρ(Q) = 0 . We will now analyse the two cases separately: 1. ρ(Q) = 0 if and only if all the eigenvalues of Q in C are 0, if and only if Q is nilpotent ( ∃n > 0 s.t. 

Qn = 0 ). This is because Q can always be triangularized in C: Q = U T U −1 where T is upper-triangular with the eigenvalues of Q on the diagonal that is, only zeros if ρ(Q) = 0 . This implies that ∃n > 0 s.t. 

T n = U −1QnU = 0 = ⇒ Qn = 0 hence Q is nilpotent. The reverse is obviously true: if Q is nilpotent then 

ρ(Q) = 0 , (otherwise there would exist λ 6 = 0 , v 6 = 0 and n > 0 s.t. Qn = 0 and Qv = λv =⇒ Qnv =

λnv = 0 , which is absurd). By definition, matrix Q is nilpotent of order n if and only if the Markov Chain reaches an absorbing state in at most n steps (a.s.). In conclusion, ρ(Q) = 0 if and only if the option is almost surely bounded. This happens if and only if there is no cycle in the option (with probability 1, every non-absorbing state is visited at most once). 2. In the case where ρ(Q) > 0: it is clear that E [eλ(τ −τ )] can not be bounded by a function of the form 

λ → e σ2λ2 

> 2

for λ ≥ − log ( ρ(Q)) so τ (s, o, s ′) is not sub-Gaussian (Definition 5). However, since ρ(Q) < 1

we can choose 0 < c 0 < − log ( ρ(Q)) and we have E [eλ(τ −τ )] < +∞ for all |λ| < c 0, which implies that 

τ (s, o, s ′) is sub-exponential (Definition 4). In conclusion, either option o contains inner-loops (some states are visited several times with non-zero probability) in which case the distribution of τ (s, o, s ′) is sub-Exponential but not sub-Gaussian, or o has no inner-loop in which case o is bounded (and thus sub-Gaussian). There is no other alternative. The distribution of rewards r(s, o, s ′) is not as simple: the reward of an option is the sum of all micro-rewards obtained at every time step before the option ends, and every micro-reward earned at each time step can have a different distribution. The only constraint is that all micro-rewards should be (a.s.) bounded between 0 and 

Rmax . As a result, if τ (s, o, s ′) is a.s. bounded (by let’s say Tmax ) then r(s, o, s ′) is also a.s. bounded (by 

Rmax Tmax ). But if τ (s, o, s ′) is unbounded then r(s, o, s ′) may still be bounded if for example, all micro-rewards are 0. If however all micro-rewards are equal to Rmax then r(s, o, s ′) has a discrete phase-type distribution just like τ (s, o, s ′). r(s, o, s ′) can thus be unbounded (and even not sub-Gaussian). However, we will show that 

r(s, o, s ′) is always sub-Exponential. Using the law of total expectations and the fact that P (r ≤ Rmax τ ) = 1 we have: 

∀λ > 0, E

[

eλ(r−r)]

=

> ∞

∑

> k=1

E

[

eλ(r−r)∣∣τ = k

]

P(τ = k) ≤

> ∞

∑

> k=1

E

[

eλ(Rmax τ −r)∣∣τ = k

]

P(τ = k)=

> ∞

∑

> k=1

E

[

eλ(Rmax k−r)∣∣τ = k

]

P(τ = k)=

> ∞

∑

> k=1

eλ(Rmax k−r)P(τ = k)= eλ(Rmax −τ )e⊺

> s

[ ∞∑

> k=0

(eλR max Q)k

]

Re s′

We can now conclude as we did for τ (s, o, s ′): let 0 < c 0 < − log( ρ(Q))  

> Rmax

, for all 0 < λ < c 0 the quantity E [eλ(r−r)]

is finite. Note that for λ ≤ 0: E [eλr ] ≤ 1 so E [eλ(r−r)] < +∞. By Definition 4, r(s, o, s ′) is sub-Exponential. Ronan Fruit, Alessandro Lazaric 

## E Equivalent policies in an MDP with options and the induced SMDP (Lem. 2) 

We consider the original MDP M and the SMDP MO induced by the set of options O. By definition of MO,the reward of an option is equal to the sum of the rewards of all the primitive actions taken until the option terminates (when the option is executed in M ). Therefore ∑ni=1 ri 

> O

= ∑N (Tn) 

> i=1

ri 

> O

= ∑Tn 

> t=1

rt and: 

∆( M, A, s, T n) = Tnρ∗(M ) −

> Tn

∑

> t=1

rt

= Tnρ∗(M ′) + Tn (ρ∗(M ) − ρ∗(MO )) −

> n

∑

> i=1

ri

> O

= ∆( MO, A, s, n ) + Tn (ρ∗(M ) − ρ∗(MO)) 

(28) The second part of Lem. 2 is thus proved. We now define the (finite-time) average reward in the two processes 

∀T ∈ N∗, ρπ (M, s, T ) = EπM

[ ∑Tt=1 rt

T

∣∣∣∣s0 = s

]

∀T ′ ∈ R+∗, ρπO (MO , s, T ′) = EπO

> MO

[ ∑N (T ′) 

> i=1

ri

> O

T ′

∣∣∣∣s0 = s

]

.

The limit lim n→+∞ Tn = + ∞ since the sequence (Tn)n∈N∗ is strictly increasing and unbounded (at least one primitive action is executed before the option ends: ∀n ≥ 1, T n+1 ≥ Tn + 1 ). Moreover, lim T ′ →+∞ ρπO (MO, s, T ′)

exists since πO is stationary and deterministic (see appendix A) and by composition of the limit we have 

lim  

> n→+∞

ρπO (MO , s, T n) = lim    

> T′→+∞

ρπO (MO, s, T ′) = ρπO (MO, s )

The limit lim T →+∞ ρπ (M, s, T ) also exists. To see this, we can build an augmented MDP equivalent to M where the state and actions encountered in two different options are duplicated (see section 3 of [Levy and Shimkin, 2012]). The equivalence between the original and augmented MDPs is in the strong sense: for any optional policy, the corresponding policy in the augmented MDP yields exactly the same reward for any finite horizon. In the augmented MDP, policy π is stationary deterministic and we know from MDP theory [Puterman, 1994] that the corresponding average reward exists. We also have: 

∀n ≥ 1, EπM

[ ∑Tn 

> t=1

rt

Tn

∣∣∣∣s0 = s

]

= EπO

> MO

[ ∑ ni=1 ri

> O

Tn

∣∣∣∣s0 = s

]

=⇒ ρπO (MO, s ) = lim  

> n→+∞

ρπ (M, s, T n) = lim   

> T→+∞

ρπ (M, s, T ) = ρπ (M, s )

The first part of Lem. 2 is thus proved. Finally, we know from the literature [Puterman, 1994] that there exists a stationary deterministic optimal policy in the augmented MDP and thus there also exists a stationary determin-istic optional policy (a policy using only options in O) in the original MDP. As a result, ρ∗(MO) is the maximal average reward achievable in M using only options in O. In conclusion, the linear term Tn (ρ∗(M ) − ρ∗(MO)) 

in equation 28 is the minimal asymptotic regret incurred if the learning agent decides to only use options. This linear loss is unavoidable. 

## F Details of the illustrative experiments 

In this section we will detail the experiments described in section 6. 

Terminating Condition Let’s denote the current state by s0 and for all k ∈ { 1...m }, denote by sk the state which is k steps on the left to s0. Assume option LEFT is taken in s0. By definition, once sk is reached, the probability of ending the option is given by βo(sk) = 1 /(m − k + 1) . Since all transitions in the MDP have probability 1 (except at the target), the probability of ending in exactly k steps can be computed as follows: Exploration–Exploitation in MDPs with Options 

## s′

## s

m-close (up) 

m-close (down) 

m-close (right) m-close (left) 

# ≤ D

Figure 7: Upper bound on the diameter of the SMDP used in the experiments. 

• If k = 1 :

P(τ = 1) = βo(s1) = 1

m

• If k ≥ 1:

P(τ = k) = 

(k−1∏

> i=1

(1 − βo(si)) 

)

× βo(sk)=

(k−1∏

> i=1

(

1 − 1

m − i + 1 

))

× 1

m − k + 1 =

(k−1∏

> i=1

( m − i

m − i + 1 

))

× 1

m − k + 1 = 1

m

By symmetry, the other options ( RIGHT , UP and DOWN ) have the same holding time. 

Expected Holding Time Based on the previous result, we can easily compute the expected holding time: 

E[τ ] = 

> m

∑

> k=1

k · P(τ = k) = 1

m

> m

∑

> k=1

k = m + 1 

2

Diameter Let s and s′ be two distinct states in the grid. With the options defined above, the expected shortest path from s to s′ is obtained if in each visited state on the way to s′, we choose an option that goes in the direction of s′. For example, if s is the state located in the top left corner of the grid and s′ is the target, the expected shortest path is obtained when either RIGHT or DOWN is taken in every state. With this policy, the expected time to get m-close to s′ both horizontally and vertically is trivially bounded by D (red path on Fig. 7). Once we are m-close to s′ (green square on Fig. 7, m = 3 on this example), we will potentially start cycling until we reach s′. On Fig. 8, we give an example (in one dimension) of a possible path before reaching s′ once in an m-close state (the green arrows represent the successive transitions, and m = 3 on this example). Since all Ronan Fruit, Alessandro Lazaric     

> RIGHT LEF T RIGHT RIGHT LEF T LEF T

# s′

m steps m steps 

Figure 8: Behaviour of the agent in m-close states. options end after at most m time steps, once we are m-close to s′, we stay m-close with the chosen policy. The expected time it takes to reach s′ once we are m-close to it is m(m + 1) /2 both horizontally and vertically. To prove this, we need to solve a linear system. For all i ∈ { 1...m − 1}, denote by τi the time it takes to go from s

to the i-th state to the left (respectively right, up or down) when the option chosen is left (respectively right, up or down). The value is the same in all directions by symmetry. We can express the τi as follows: 

τ1 = 1

m + 1

m (2 + τ1) + · · · + 1

m (m + τm−1)

τ2 = 1

m × 2 + 1

m (1 + τ1) + 1

m (3 + τ1) + · · · + 1

m (m + τm−2)

τ3 = 1

m × 3 + 1

m (1 + τ2) + 1

m (2 + τ1) + 1

m (4 + τ1) + · · · + 1

m (m + τm−3)

. . . τi = m + 1 

2 + 1

m

> i−1

∑

> j=1

τj + 1

m

> m−i

∑

> j=1

τj

(29) With probability 1/m , the next state after executing the option is 1 step to the left of s and the value of τ1 is then 1 . With probability 1/m the next state is 2 steps to the left of s and so s′ is now located 1 step to the right of the new state: the value of τ1 is thus 2 + τ1. With probability 1/m the next state is 3 steps to the left of 

s and and so s′ is now located 2 steps to the right of the new state: the value of τ1 is thus 3 + τ2. And so on and so forth. What we used here is basically the law of total expectations where the partition of events is the set of all possible states reached after executing the option only once. The same thing can be done for τ2 . . . τ m−1. It is trivial to verify that the only solution of the linear system in equation 29 is: τi = m(m + 1) /2, ∀i ∈ { 1...m − 1}.This results is rather intuitive: m corresponds to the expected number of times the option needs to be executed to end up in the desired state s′ whereas (m+ 1) /2 is the expected duration at every decision step. The simplicity of this result comes from the symmetry of the problem: every time an option is executed, we stay m-close to s′

and the probability to exactly reach s′ is always 1/m . So in this sense, we have i.i.d. Bernoulli trials where the probability of success is 1/m . The expected time to reach s′ when we start in an m-close state both horizontally and vertically is thus 2 × m(m + 1) /2 = m(m + 1) . Therefore, the expected time to go from s to s′ is always bounded by D + m(m + 1) .On Fig. 9 we illustrate what happens when the options are deterministic i.e., when they terminate after exactly 

m time steps. On this example we chose m = 3 . If we start from state s0, only the green states can be reached without resorting to the restart triggered by the target state, whereas if we start from s1 only the blue states can be reached 8 (and similarly for the white states). Let’s assume that we want to go from a green state to a blue state. The only way to do so is to go to the target and "hope" to end up in one of the blue states after the restart (we recall that the restart state is chosen randomly with equi-probability). The shortest path to go from any state to the target is bounded by D and the probability to restart in a state with the desired colour is 1/m (1/m 2 in dimension 2). We can thus upper bound the diameter of the SMDP MO by the expected time needed to go from s0 to s1 in the SMDP of Fig. 10, that is: DO ≤ D(1 + m2). This bound is tight (up to a                

> 8Here we slightly simplified the problem. In reality, due to the truncation operated by the walls and if we assume s0
> to be the leftmost state, it is possible to go from s1to s0in one time step by executing LEF T . But for m≥3there will always be pairs of states that cannot be reached from each other without a restart. If s0is the leftmost state, this is the case for s1and the white state adjacent to it on Fig. 9. So the proof remains valid.

Exploration–Exploitation in MDPs with Options 

# b

Target Starting State 

# s0 s1

Figure 9: Behaviour of the agent with deterministic options. 

## s0 Target s1

E[τ ] ≤ D

p = 1 

E[τ ] ≤ D

p = 1

> m2

E[τ ] ≤ D

p = 1 − 1

> m2

Figure 10: Upper bound on the diameter of MO for deterministic options. constant factor) since the average time to go from any state chosen at random with equi-probability to the target is exactly D/ 2 in the 2-dimensional grid. 

Optimality Since the target state is located in a corner of the grid, the shortest path to go from any state to the target is equally long in the original MDP and the MDP with options. As a result, the optimal average rewards are also equal (i.e., there exists an optimal policy using only options LEFT RIGHT , UP and DOWN 

which consists in applying only RIGHT or DOWN ). 

Asymptotic behaviour We will now analyse the behaviour of the ratio n 

> Tn

using results on martingales. 

Theorem 3 (Martingale Strong Law of Large Numbers, [Vovk et al., 2005]) . Let X1, ..., X n be a martingale difference sequence w.r.t. a filtration F0, F1, ..., Fn and let A1, ..., A n be an increasing predictable sequence w.r.t. the same filtration with A1 > 0 and lim n→+∞ An = + ∞ almost surely. If: 

> +∞

∑

> i=1

E[X2 

> i

|F i−1]

A2

> i

< +∞ a.s. then: 

1

Ann∑

> i=1

Xi −−−−−→ 

> n→+∞

0 a.s. 

Let’s take Xi = τi − τ i (where τ i = τ i(si−1, a i)) and Fi = σ (s0, a 1, τ 1, r 1, ..., s i, a i+1 ). The sequence (Xi)i≤1 is a martingale difference because E[Xi] < +∞ and E[Xi|F i−1] = 0 . Since (τ (s, a, s ′)) s,a,s ′ are sub-Exponential, all moments are finite and it is well known from the literature that the variance is bounded by the sub-Exponential constant σ2 

> τ

hence: E[X2 

> i

|F i−1] < σ 2 

> τ

. If in addition we take Ai = i then the conditions of Theorem 3 are satisfied and thus: 

Tn

n − Tn

n −−−−−→ 

> n→+∞

0 a.s. where Tn = E[Tn]. By definition: τmax n ≥ Tn ≥ τmin n hence: ∀ǫ > 0, ∃Nǫ > 0 s.t. ∀n ≥ Nǫ :

∣∣∣∣

Tn

n − Tn

n

∣∣∣∣ ≤ ǫ a.s. =⇒ τmin − ǫ ≤ Tn

n − ǫ ≤ Tn

n ≤ ǫ + Tn

n ≤ ǫ + τmax Ronan Fruit, Alessandro Lazaric 

and so: lim inf n→+∞ Tn 

> n

≥ τmin and lim sup n→+∞ Tn 

> n

≤ τmax a.s. Finally: 

log { n 

> δ

}

log { Tn 

> δ

} = log { n 

> δ

}

log { Tn−Tn 

> n

+ Tn 

> n

} + log { n 

> δ

} ≤ log { n 

> δ

}

log { Tn −Tn 

> n

+ τmin } + log { n 

> δ

} −−−−−→ 

> n→+∞

1

In the general case of sub-Exponential rewards and holding times our results provide no theoretical evidence of the advantage of introducing options due to the fact that C(M ′, n, δ ) scales as √log( n):

lim  

> n→+∞

R(M, n, δ ) = + ∞ a.s. but if the rewards and holding times are bounded we have: 

lim sup 

> n→+∞

R(M, n, δ ) ≤ 1

√τmin 

(

1 + Tmax 

D√S

)

a.s. Note that τmin is a very loose upper-bound on lim inf n→+∞ Tn 

> n

and in practice the ratio Tn 

> n

can take much higher values if τmax is big and many options have a high expected holding time. 

Tightness of the upper bounds On Fig. 11a, we plot the expected theoretical values taken by the ratio of the regrets according to our upper bounds (formula given in Sect. 6). On Fig. 11b however, we plot the empirical values of the ratios in our experiments (same graph as on Fig. 3a). We can see that the curves have similar shapes. In particular, they reach their respective minima for the same value of Tmax and the value of these minimum is below 1 (meaning that learning with options is more efficient than with primitive actions in this case). Moreover, the theoretical ratios are upper-bounding the empirical ones for all values of Tmax . We can conclude that the ratio of the upper bounds is a good proxy for the true ratio in this example. Exploration–Exploitation in MDPs with Options        

> 12345678

Maximal duration of options Tmax 

> 0.75 0.80 0.85 0.90 0.95 1.00 1.05 1.10
> Ratio of regrets  ˜R

20x20 Grid 25x25 Grid 30x30 Grid 

(a)        

> 12345678

Maximal duration of options Tmax 

> 0.75 0.80 0.85 0.90 0.95 1.00 1.05 1.10
> Ratio of regrets  R

20x20 Grid 25x25 Grid 30x30 Grid 

(b) 

Figure 11: (a) Theoretical ratios of the regrets with and without options for different values of Tmax ; (b) Empirical ratios of the regrets with and without options for different values of Tmax .