# Source: http://proceedings.mlr.press/v115/wang20b/wang20b-supp.pdf
# Title: Truly Proximal Policy Optimization (supplementary)
# Fetched via: jina
# Date: 2026-04-09

Title: wang20b-supp.pdf



Number of Pages: 11

# Truly Proximal Policy Optimization 

Yuhui Wang *, Hao He *, Xiaoyang Tan College of Computer Science and Technology, Nanjing University of Aeronautics and Astronautics, China MIIT Key Laboratory of Pattern Analysis and Machine Intelligence, China Collaborative Innovation Center of Novel Software Technology and Industrialization, China 

{y.wang, hugo, x.tan }@nuaa.edu.cn 

# Abstract 

Proximal policy optimization (PPO) is one of the most successful deep reinforcement learn-ing methods, achieving state-of-the-art per-formance across a wide range of challenging tasks. However, its optimization behavior is still far from being fully understood. In this paper, we show that PPO could neither strictly restrict the probability ratio as it attempts to do nor enforce a well-defined trust region con-straint, which means that it may still suffer from the risk of performance instability. To ad-dress this issue, we present an enhanced PPO method, named Trust Region-based PPO with Rollback (TR-PPO-RB). Two critical improve-ments are made in our method: 1) it adopts a new clipping function to support a rollback behavior to restrict the ratio between the new policy and the old one; 2) the triggering condi-tion for clipping is replaced with a trust region-based one, which is theoretically justified ac-cording to the trust region theorem. It seems, by adhering more truly to the “proximal” prop-erty − restricting the policy within the trust re-gion, the new algorithm improves the original PPO on both stability and sample efficiency. 

# 1 INTRODUCTION 

Deep model-free reinforcement learning has achieved great successes in recent years, notably in video games (Mnih et al., 2015), board games (Silver et al., 2017), robotics (Levine et al., 2016), and challenging control tasks (Schulman et al., 2016; Duan et al., 2016). Pol-icy gradient (PG) methods are useful model-free policy 

> *Authors contributed equally.

search algorithms, updating the policy with an estimator of the gradient of the expected return (Peters & Schaal, 2008). One major challenge of PG-based methods is to estimate the right step size for the policy updating, and an improper step size may result in severe policy degra-dation due to the fact that the input data strongly depends on the current policy (Kakade & Langford, 2002; Schul-man et al., 2015). For this reason, the trade-off between learning stability and learning speed is an essential issue to be considered for a PG method. The well-known trust region policy optimization (TRPO) method addressed this problem by imposing onto the ob-jective function a trust region constraint so as to control the KL divergence between the old policy and the new one (Schulman et al., 2015). This can be theoretically justified by showing that optimizing the policy within the trust region leads to guaranteed monotonic perfor-mance improvement. However, the complicated second-order optimization involved in TRPO makes it compu-tationally inefficient and difficult to scale up for large scale problems when extending to complex network ar-chitectures. Proximal Policy Optimization (PPO) signif-icantly reduces the complexity by adopting a clipping mechanism so as to avoid imposing the hard constraint completely, allowing it to use a first-order optimizer like the Gradient Descent method to optimize the objective (Schulman et al., 2017). As for the mechanism for deal-ing with the learning stability issue, in contrast with the trust region method of TRPO, PPO tries to remove the incentive for pushing the policy away from the old one when the probability ratio between them is out of a clip-ping range. PPO is proven to be very effective in dealing with a wide range of challenging tasks, while being sim-ple to implement and tune. However, despite its success, the actual optimization be-havior of PPO is less studied, highlighting the need to study the proximal property of PPO. Some researchers have raised concerns about whether PPO could restrict the probability ratio as it attempts to do (Wang et al., 2019; Ilyas et al., 2018), and since there exists an obvi-ous gap between the heuristic probability ratio constraint and the theoretically-justified trust region constraint, it is natural to ask whether PPO enforces a trust region-like constraint as well to ensure its stability in learning? In this paper, we formally address both the above ques-tions and give negative answers to both of them. In par-ticular, we found that PPO could neither strictly restrict the probability ratio nor enforce a trust region constraint. The former issue is mainly caused by the fact that PPO could not entirely remove the incentive for pushing the policy away, while the latter is mainly due to the inherent difference between the two types of constraints adopted by PPO and TRPO respectively. Inspired by the insights above, we propose an enhanced PPO method, named Trust Region-based PPO with Roll-back (TR-PPO-RB). In particular, we apply a nega-tive incentive to prevent the policy from being pushed away during training, which we called a rollback op-eration. Furthermore, we replace the triggering condi-tion for clipping with a trust region-based one, which is theoretically justified according to the trust region theorem that optimizing the policy within the trust re-gion lead to guaranteed monotonic improvement (Schul-man et al., 2015). TR-PPO-RB actually combines the strengths of TRPO and PPO − it is theoretically jus-tified and is simple to implement with first-order opti-mization. Extensive results on several benchmark tasks show that the proposed methods significantly improve both the policy performance and the sample efficiency. Source code is available at https://github.com/ wangyuhuix/TrulyPPO .

# 2 RELATED WORK 

Many researchers have extensively studied different ap-proach to constrain policy updating in recent years. The natural policy gradient (NPG) (Kakade, 2001) improves REINFORCE by computing an ascent direction that ap-proximately ensures a small change in the policy dis-tribution. Relative entropy policy search (REPS) (Pe-ters et al., 2010) constrains the state-action marginals, limits the loss of information per iteration and aims to ensure a smooth learning progress. While this algo-rithm requires a costly nonlinear optimization in the in-ner loop, which is computationally expansive. TRPO is derived from the conservative policy iteration (Kakade & Langford, 2002), in which the performance improvement lower bound has been first introduced. There has been a focus on the problem of constraining policy update, and attention is being paid to TRPO and PPO in recent years. Wu et al. (2017) proposed an actor critic method which uses Kronecker-factor trust regions (ACKTR). Hmlinen et al. (2018) proposed a method to improve exploration behavior with evolution strategies. Chen et al. (2018) presented a method adaptively adjusts the scale of policy gradient according to the significance of state-action. Several studies focus on investigating the clipping mech-anism of PPO. Wang et al. (2019) found that the ratio-based clipping of PPO could lead to limited sample effi-ciency when the policy is initialized from a bad solution. To address this problem, the clipping ranges are adap-tively adjusted guided by a trust region criterion. This paper also works on a trust region criterion, but it is used as a triggering condition for clipping, which is much simpler to implement. Ilyas et al. (2018) performed a fine-grained examination and found that the PPO’s per-formance depends heavily on optimization tricks but not the core clipping mechanism. However, as we found, al-though the clipping mechanism could not strictly restrict the policy, it does exert an important effect in restrict-ing the policy and maintain stability. We provide detail discussion in our experiments. 

# 3 PRELIMINARIES 

A Markov Decision Processes (MDP) is described by the tuple (S, A, T , c, ρ 1, γ ). S and A are the state space and action space; T : S × A × S → R is the transition probability distribution; c : S × A → R is the reward function; ρ1 is the distribution of the initial state s1, and 

γ ∈ (0 , 1) is the discount factor. The performance of a policy π is defined as η(π) = Es∼ρπ ,a ∼π [c(s, a )] where 

ρπ (s) = (1 −γ) ∑∞ 

> t=1

γt−1ρπt (s), ρπt is the density func-tion of state at time t.Policy gradients methods (Sutton et al., 1999) update the policy by the following surrogate performance objective, 

Lπold (π) = Es,a [rπ (s, a )Aπold (s, a )] + η(πold ) (1) where π(a|s)/π old (a|s) is the probability ratio between the new policy π and the old policy πold , Aπold (s, a ) = 

E[Rγt |st = s, a t = a; πold ] − E[Rγt |st = s; πold ] is the advantage value function of the old policy πold . Schul-man et al. (2015) derived the following performance bound: 

Theorem 1. Let 

C = max  

> s,a

|Aπold (s, a )| 4γ/ (1 − γ)2, Ds 

> KL

(πold , π ) ,

DKL (πold (·| s)|| π(·| s)) , Mπold (π) = Lπold (π) −

C max s∈S DsKL (πold , π ) . We have 

η(π) ≥ Mπold (π), η (πold ) = Mπold (πold ). (2) This theorem implies that maximizing Mπold (π) guaran-tee non-decreasing of the performance of the new policy 

π. TRPO imposed a constraint on the KL divergence: 

max  

> π

Lπold (π)

s.t. max  

> s∈S

DsKL (πold , π ) ≤ δ

(3a) (3b) Constraint (3b) is called the trust region-based con-straint , which is a constraint on the KL divergence be-tween the old policy and the new one. To faithfully investigate how the algorithms work in practice, we consider a parametrized policy. In practical Deep RL algorithms, the policy are usually parametrized by Deep Neural Networks (DNNs). For discrete action space tasks where |A| = D, the policy is parametrized by πθ (st) = f pθ (st). where f pθ is the DNN outputting a vector which represents a D-dimensional discrete dis-tribution. For continuous action space tasks, it is stan-dard to represent the policy by a Gaussian policy, i.e., 

πθ (a|st) = N (a|f μθ (st), f Σ 

> θ

(st)) (Williams, 1992; Mnih et al., 2016), where f μθ and f Σ 

> θ

are the DNNs which output the mean and covariance matrix of the Gaussian distribution. For simplicity, we will use the notation of 

θ rather than π in the our paper, e.g., Ds

> KL

(θold , θ ) ,

Ds

> KL

(πθold , π θ ).

# 4 ANALYSIS OF THE “PROXI-MAL” PROPERTY OF PPO 

In this section, we will first give a brief review of PPO and then investigate the “proximal” property of PPO. We refer to “proximal” property as whether the algorithm could restrict the policy difference, regarding the proba-bility ratio or the KL divergence between the new policy and the old one. PPO employs a clipped surrogate objective to prevent the new policy from straying away from the old one. The clipped objective function of state-action (st, a t) is 

LCLIP  

> t

(θ)= min (rt(θ, θ old )At, FCLIP (rt(θ, θ old ),  ) At

) (4) where θ and θold are the parameters of the new policy and the old one respectively; rt(θ, θ old ) ,

πθ (at|st)/π θold (at|st) is the probability ratio, we will omit writing the parameter of the old policy θold ex-plicitly; st ∼ ρπθold , a t ∼ πθold (·| st) are the sampled states and actions; At is the estimated advantage value of 

Aπθold (st, a t); The clipping function FCLIP is defined as 

FCLIP (rt(θ),  ) = 



1 −  rt(θ) ≤ 1 − 

1 +  rt(θ) ≥ 1 + rt(θ) else 

(5) where (1 −, 1+ ) is called the clipping range , 0 <  < 1

is the parameter. The overall objective function is 

LCLIP (θ) = 1

T

> T

∑

> t=1

LCLIP  

> t

(θ) (6) To faithfully analyse how PPO works in practice, we as-sume that si 6 = sj for all i 6 = j (1 ≤ i, j ≤ T ), since we could hardly meet exactly the same states in finite tri-als in large or continuous state space. This assumption means that only one action is sampled on each sampled states. PPO restricts the policy by clipping the probability ratio between the new policy and the old one. Recently, re-searchers have raised concerns about whether this clip-ping mechanism can really restrict the policy (Wang et al., 2019; Ilyas et al., 2018). We investigate the fol-lowing questions of PPO. The first one is that whether PPO could bound the probability ratio as it attempts to do. The second one is that whether PPO could enforce a well-defined trust region constraint, which is primar-ily concerned since that it is a theoretical indicator on the performance guarantee (see eq. (2)) (Schulman et al., 2015). We give an elaborate analysis of PPO to answer these two questions. 

Question 1. Could PPO bound the probability ratio within the clipping range as it attempts to do? 

In general, PPO could generate an effect of preventing the probability ratio from exceeding the clipping range too much, but it could not strictly bound the probability ratio. To see this, LCLIP  

> t

(θ) in eq. (4) can be rewritten as: 

LCLIP  

> t

(θ) = 



(1 − )At

rt(θ) ≤ 1 − 

and At < 0(1 + )At rt(θ) ≥ 1 + 

and At > 0

rt(θ)At otherwise (7a) (7b) The case (7a) and (7b) are called the clipping condition .As the equation implies, once rt(θ) is out of the clipping range (with a certain condition of At), the gradient of 

LCLIP  

> t

(θ) w.r.t. θ will be zero. As a result, the incentive, deriving from LCLIP  

> t

(θ), for driving rt(θ) to go farther beyond the clipping range is removed. However, in practice the probability ratios are known to be not bounded within the clipping range (Ilyas et al., 2018). The probability ratios on some tasks could even reach a value of 40, which is much larger than the upper clipping range 1.2 (  = 0 .2, see our empirical results in Section 6). One main factor for this problem is that the clipping mechanism could not entirely remove incentive deriving from the overall objective LCLIP (θ), which pos-sibly push these out-of-the-range rt(θ) to go farther be-yond the clipping range. We formally describe this claim in following. 

Theorem 2. Given θ0 that rt(θ0) satisfies the clipping condition (either 7a or 7b). Let ∇LCLIP (θ0) denote the gradient of LCLIP at θ0, and similarly ∇rt(θ0). Let θ1 =

θ0 + β∇LCLIP (θ0), where β is the step size. If 

〈∇ LCLIP (θ0), ∇rt(θ0)〉At > 0 (8) 

then there exists some ¯β > 0 such that for any β ∈ (0 , ¯β),we have 

|rt(θ1) − 1| > |rt(θ0) − 1| > . (9) We provide the proof in Appendix A. As this theorem implies, even the probability ratio rt(θ0) is already out of the clipping range, it could be driven to go farther be-yond the range (see eq. (9)). The condition (8) requires the gradient of the overall objective LCLIP (θ0) to be sim-ilar in direction to that of rt(θ0)At. This condition possi-bly happens due to the similar gradients of different sam-ples or optimization tricks. For example, the Momentum optimization methods preserve the gradients attained be-fore, which could possibly make this situation happen. Such condition occurs quite often in practice. We made statistics over 1 million samples on benchmark tasks in Section 6, and the condition occurs at a percentage from 25% to 45% across different tasks. 

Question 2. Could PPO enforce a trust region con-straint? 

PPO does not explicitly attempt to impose a trust region constraint, i.e., the KL divergence between the old pol-icy and the new one. Nevertheless, Wang et al. (2019) revealed that a different scale of the clipping range can affect the scale of the KL divergence. As they stated, under state-action (st, a t), if the probability ratio rt(θ)

is not bounded, then neither could the corresponding KL divergence Dst

> KL

(θold , θ ) be bounded. Thus, together with the previous conclusion in Question 1, we can know that PPO could not bound KL divergence. In fact, even the probability ratio rt(θ) is bounded, the corresponding KL divergence Dst

> KL

(θold , θ ) is not necessarily bounded. Formally, we have the following theorem. 

Theorem 3. Assume that for discrete action space tasks where |A|≥ 3 and the policy is πθ (s) =

f pθ (s), we have {f pθ (st)|θ ∈ R} = {p|p ∈

R+D , ∑Dd p(d) = 1 }; for continuous action space tasks where the policy is πθ (a|s) = N (a|f μθ (s), f Σ 

> θ

(s)) ,we have {(f μθ (st), f Σ 

> θ

(st)) |θ ∈ R} = {(μ, Σ) |μ ∈

RD , Σ is a symmetric semidefinite D × D matrix }. Let 

Θ = {θ|1 −  ≤ rt(θ) ≤ 1 + }. We have 

sup θ∈Θ Dst

> KL

(θold , θ ) = + ∞ for both discrete and con-tinuous action space tasks. 

To attain an intuition on how this theorem holds, we plot the sublevel sets of rt(θ) and the level sets of 

Dst

> KL

(θold , θ ) for the continuous and discrete action space tasks respectively. As Fig. 1 illustrates, the KL divergences (solid lines) within the sublevel sets of prob-ability ratio (grey area) could go to infinity. It can be concluded that there is an obvious gap between 

> (a) Case of a Continuous Action Space Task
> (b) Case of a Discrete Action Space Task

Figure 1: The grey area shows the sublevel sets of rt(θ), i.e., Θ = {θ|1 −  ≤ rt(θ) ≤ 1 + }. The solid lines are the level sets of the KL divergence, i.e., {θ|Dst

> KL

(θold , θ ) = δ}. (a) The case of a continuous action space case, where dim (A) = 1 . The action distribution under state st is πθ (st) = N (μt, Σt), where μt = f μθ (st), Σt = f Σ 

> θ

(st).(b) The case of a discrete action space task, where |A| = 3 . The policy under state st is parametrized by πθ (st) = (p(1)  

> t

, p (2)  

> t

, p (3)  

> t

). Note that the level sets are plotted on the hyperplane ∑3 

> d=1

p(d) 

> t

= 1 and the figure is showed from the view of elevation = 45 ◦ and azimuth = 45 ◦.bounding the probability ratio and bounding the KL di-vergence. Approaches which manage to bound the prob-ability ratio could not necessarily bound KL divergence theoretically. 

# 5 METHOD 

In the previous section, we have shown that PPO could neither strictly restrict the probability ratio nor enforce a trust region constraint. We address these problems in the scheme of PPO with a general form 

Lt(θ) = min ( rt(θ)At, F (rt(θ), ·) At) (10) where F is a clipping function which attempts to restrict the policy, “ ·” in F means any hyperparameters of it. For example, in PPO, F is a ratio-based clipping function 

FCLIP (rt(θ),  ) (see eq. (5)). We modify this function to promote the ability in bounding the probability ratio and the KL divergence. We now detail how to achieve this goal in the following sections. 

# 5.1 PPO WITH ROLLBACK (PPO-RB) 

As discussed in Question 1, PPO could not strictly re-strict the probability ratio within the clipping range: the clipping mechanism could not entirely remove the incen-tive for driving rt(θ) to go beyond the clipping range, even rt(θ) has already exceeded the clipping range. We address this issue by substituting the clipping function with a rollback function , which is defined as 

FRB (rt(θ), , α )=



−αr t(θ)+(1 + α)(1 − ) rt(θ) ≤ 1 − 

−αr t(θ)+(1 + α)(1 + ) rt(θ) ≥ 1 + rt(θ) otherwise (11) where α > 0 is a hyperparameter to decide the force of the rollback. The corresponding objective function at timestep t is denoted as LRB  

> t

(θ) and the overall objective function is LRB (θ). The rollback function 

FRB (rt(θ), , α ) generates a negative incentive when 

rt(θ) is outside of the clipping range. Thus it could somewhat neutralize the incentive deriving from the overall objective LFB (θ). Fig. 2 plots LRB  

> t

and LCLIP 

> t

as functions of the probability ratio rt(θ). As the figure depicted, when rt(θ) is over the clipping range, the slope of LRB  

> t

is reversed, while that of LCLIP  

> t

is zero. The rollback operation could more forcefully prevent the probability ratio from being pushed away compared to the original clipping function. Formally, we have the fol-lowing theorem.        

> (a) At>0(b) At<0

Figure 2: Plots showing LRB  

> t

and LCLIP  

> t

as functions of the probability ratio rt(θ), for positive advantages (left) and negative advantages (right). The red circle on each plot shows the starting point for the optimization, i.e., 

rt(θ) = 1 . When rt(θ) crosses the clipping range, the slope of LRB  

> t

is reversed, while that of LCLIP  

> t

is zero. 

Theorem 4. Let θCLIP 1 = θ0 + β∇LCLIP (θ0), θRB 1 =

θ0 + β∇LRB (θ0). The indexes of the samples which sat-isfy the clipping condition is denoted as Ω = {t|1 ≤

t ≤ T, (At > 0 and rt(θ0) ≥ 1 + ) or (At <

0 and rt(θ0) ≤ 1 − )}. If t ∈ Ω and rt(θ0) satisfies ∑ 

> t′∈Ω

〈∇ rt(θ0), ∇rt′ (θ0)〉AtAt′ > 0, then there exists some ¯β > 0 such that for any β ∈ (0 , ¯β), we have 

∣∣rt(θRB 1 ) − 1∣∣ < ∣∣rt(θCLIP 1 ) − 1∣∣ . (12) This theorem implies that the rollback function can im-prove its ability in preventing the out-of-the-range ratios from going farther beyond the range. 

# 5.2 TRUST REGION-BASED PPO (TR-PPO) 

As discussed in Question 2, there is a gap between the ratio-based constraint and the trust region-based one: bounding the probability ratio is not sufficient to bound the KL divergence. However, bounding the KL diver-gence is what we primarily concern about, since it is a theoretical indicator on the performance guarantee (see eq. (2)). Therefore, new mechanism incorporating the KL divergence should be taken into account. The original clipping function uses the probability ratio as the element of the trigger condition for clipping (see eq. (5)). Inspired by the thinking above, we substitute the ratio-based clipping with a trust region-based one. Formally, the probability ratio is clipped when the policy πθ is out of the trust region, 

FTR (rt(θ), δ ) = 

{

rt(θold ) Dst

> KL

(θold , θ ) ≥ δrt(θ) otherwise (13) where δ is the parameter, rt(θold ) = 1 is a constant. The incentive for updating policy is removed when the pol-icy πθ is out of the trust region, i.e., Dst

> KL

(θold , θ ) ≥ δ.Although the clipped value rt(θold ) may make the surro-gate objective discontinuous, this discontinuity does not affect the optimization of the parameter θ at all, since the value of the constant does not affect the gradient. In general, TR-PPO could combine both the strengths of TRPO and PPO: it is somewhat theoretically-justified (by the trust region constraint) while is simple to imple-ment and only requires first-order optimization. Com-pared to TRPO, TR-PPO doesn’t need to optimize θ

through the KL divergence term Dst

> KL

(θold , θ ). The KL divergence is just calculated to decide whether to clip rt(θ) or not. Compared to PPO, TR-PPO uses a different metric of policy difference to restrict the policy. PPO applies a ratio-based metric, i.e., 

π(at|st)/π old (at|st), which imposes an element-wise constraint on the sampled action point. While TR-PPO uses a trust region-based one, i.e., the KL divergence ∑ 

> a

πold (a|st) log( πold (a|st)/π (a|st)) , which imposes a summation constraint over the action space. The ratio-based constraint could impose a relatively strict con-straint on actions which are not preferred by the old pol-icy (i.e., πold (at|st) is small), which may lead to limited sample efficiency when the policy is initialized from a bad solution (Wang et al., 2019). While the trust region-based one has no such bias and tends to perform more sample efficient in practice. Finally, we should note the importance of the min( ·, ·)

operation for all variants of PPO. Take TR-PPO as an example, the objective function incorporating the extra 

min( ·, ·) operation is 

LTR  

> t

(θ) = min (rt(θ)At, FTR (rt(θ), δ ) At

) (14) Schulman et al. (2017) stated that this extra min( ·, ·)

operation makes LTR  

> t

(θ) be a lower bound on the un-clipped objective rt(θ)At. It should also be noted that such operation is important for optimization. As eq. (13) implies, the objective without min (·, ·) operation, i.e., 

FTR (rt(θ), δ )At, would stop updating once the policy violates the trust region, even the objective value is worse than the initial one, i.e., rt(θ)At < r t(θold )At. The 

min (·, ·) operation actually provides a remedy for this issue. To see this, eq. (14) is rewritten as 

LTR  

> t

(θ) = 



rt(θold )At

Dst

> KL

(θold , θ ) ≥ δ and 

rt(θ)At ≥ rt(θold )At

rt(θ)At otherwise (15) As can be seen, the ratio is clipped only if the objective value is improved (and the policy violates the constraint). We also experimented with the direct-clipping method, i.e., FTR (rt(θ), δ )At, and found it performs extremely bad in practice. 

# 5.3 COMBINATION OF TR-PPO AND PPO-RB (TR-PPO-RB) 

The trust region-based clipping still possibly suffers from the unbounded probability ratio problem, since we do not provide any negative incentive when the policy is out of the trust region. Thus we integrate the trust region-based clipping with the rollback mechanism. 

FTR −RB (rt(θ), δ, α )=

{

−αr t(θ) Dst

> KL

(θold , θ ) ≥ δrt(θ) otherwise (16) As the equation implies, FTR −RB (rt(θ), δ, α ) generates a negative incentive when πθ is out of the trust region. 

# 6 EXPERIMENT 

We conducted experiments to investigate whether the proposed methods could improve ability in restricting the policy and accordingly benefit the learning. To measure the behavior and the performance of the al-gorithm, we evaluate the probability ratio, the KL diver-gence, and the episode reward during the training pro-cess. The probability ratio and the KL divergence are measured between the new policy and the old one at each epoch. We refer one epoch as: 1) sample state-actions from a behavior policy πθold ; 2) optimize the policy πθ

with the surrogate function and obtain a new policy. We evaluate the following algorithms. (a) PPO : the orig-inal PPO algorithm. We used  = 0 .2, which is recom-mended by (Schulman et al., 2017). We also tested PPO with  = 0 .6, denoted as PPO-0.6 . (b) PPO-RB : PPO with the extra rollback trick. The rollback coefficient is set to be α = 0 .3 for all tasks (except for the Humanoid task we use α = 0 .1). (c) TR-PPO : trust region-based PPO. The trust region coefficient is set to be δ = 0 .025 

for all tasks (except for the Humanoid and HalfCheetah task we use δ = 0 .03 ). (d) TR-PPO-RB : trust region-based PPO with rollback. The coefficients are set to be 

δ = 0 .03 and α = 0 .05 (except for the Humanoid and HalfCheetah task we use α = 0 .1). The δ of TR-PPO-RB is set to be slightly larger than that of TR-PPO due to the existence of the rollback mechanism. (e) TR-PPO-simple : A vanilla version of TR-PPO, which does not include the min( ·, ·) operation. The δ is same as TR-PPO. (f) A2C : a classic policy gradient method. A2C has the exactly same implementations and hyperparameters as PPO except the clipping mechanism is removed. (g) 

SAC : Soft Actor-Critic, a state-of-the-art off-policy RL algorithm (Haarnoja et al., 2018). We adopt the imple-mentations provided in (Haarnoja et al., 2018). (h) PPO-SAC and TR-PPO-SAC : two variants of SAC which use ratio-based clipping with  = 0 .2 and trust region-based clipping with δ = 0 .02 respectively. All our proposed methods and PPO adopt exactly the same implemen-tations and hyperparameters given in (Dhariwal et al., 2017) except the clipping function. This ensures that the differences are due to the algorithm changes instead of the implementations. The algorithms are evaluated on continuous and discrete control benchmark tasks implemented in OpenAI Gym (Brockman et al., 2016), simulated by MuJoCo (Todorov et al., 2012) and Arcade Learning Environment (Belle-mare et al., 2013). For continuous control tasks, we eval-uate algorithms on 6 benchmark tasks (including a chal-lenging high-dimensional Humanoid locomotion task). All tasks were run with 1 million timesteps except for the Humanoid task was 20 million timesteps. Each algo-rithm was run with 4 random seeds. The experiments on discrete control tasks are detailed in Appendix B. 

Question 1. Does PPO suffer from the issue in bound-ing the probability ratio and KL divergence as we have analysed? 

In general, PPO could not strictly bound the probability ratio within the predefined clipping range. As shown in Fig. 3, a reasonable proportion of the probability ratios of PPO are out of the clipping range on all tasks. Espe-cially on Humanoid-v2, HalfCheetah-v2, and Walker2d-v2, even half of the probability ratios exceed. Moreover, as can be seen in Fig. 4, the maximum probability ratio of PPO can achieve more than 3 on all tasks (the upper clipping range is 1.2). In addition, the maximum KL di-vergence also grows as timestep increases (see Fig. 5). Nevertheless, PPO still exerts an important effect on re-stricting the policy. To show this, we tested two variants of PPO: one uses  = 0 .6, denoted as PPO-0.6 ; another one entirely removes the clipping mechanism, which col-lapses to the vanilla A2C algorithm. As expected, the probability ratios and the KL divergences of these two variants are much larger than that of PPO (we put the results in Appendix B, since the values are too large). Moreover, the performance of these two methods fluctu-ate dramatically during the training process (see Fig. 6). In summary, it could be concluded that although the core 

Figure 3: The proportions of the probability ratios which are out of the clipping range. The proportions are cal-culated over all sampled state-actions at that epoch. We only show the results of PPO and PPO-RB, since only these two methods have the clipping range parameter to judge whether the probability ratio is out of the clipping range. 

Figure 4: The maximum ratio over all sampled sates of each update during the training process. The results of TR-PPO-simple and PPO-0.6 are provided in Appendix. since their value are too large. 

Figure 5: The maximum KL divergence over all sam-pled states of each update during the training process. The results of TR-PPO-simple and PPO-0.6 are plotted in Appendix, since their value are too large. clipping mechanism of PPO could not strictly restrict the probability ratio within the predefined clipping range, it could somewhat generate the effect on restricting the pol-icy and benefit the learning. This conclusion is partly different from that of Ilyas et al. (2018). They drew a conclusion that “PPO’s performance depends heavily Table 1: a) Timesteps to hit thresholds within 1 million timesteps (except Humanoid with 20 million). b) Averaged top 10 episode rewards during training process. These results are averaged over 4 random seeds.                                                                                                    

> (a) Timesteps to hit threshold ( ×10 3)(b) Averaged top 10 episode tewards Threshold PPO PPO-RB TR-PPO TR-PPO-RB SAC PPO-SAC TR-PPO-SAC PPO PPO-RB TR-PPO TR-PPO-RB SAC PPO-SAC TR-PPO-SAC Hopper 3000 273 179 153 130 187 144 136 3612 3604 3788 3653 3453 3376 3439 Walker2d 3000 528 305 345 320 666 519 378 4036 4992 4874 5011 3526 3833 4125 Humanoid 5000 8410 8344 7580 6422 314 //7510 7366 6842 6501 7636 //Reacher -4.5 230 206 211 161 352 367 299 -3.55 -1.61 -1.55 -1.5 -3.81 -3.44 -4.21 Swimmer 70 721 359 221 318 ///101 126 110 112 53 54 56 HalfCheetah 2100 /374 227 266 39 45 36 1623 3536 4672 4048 10674 10826 10969

Figure 6: Episode rewards of the policy during the training process averaged over 4 random seeds. The shaded area depicts the mean ± the standard deviation. on optimization tricks but not the core clipping mecha-nism”. They got this conclusion by examining a variant of PPO which implements only the core clipping mech-anism and removes additional optimization tricks (e.g., clipped value loss, reward scaling). This variant also fails in restricting policy and learning. However, as can be seen in our results, arbitrarily enlarging the clipping range or removing the core clipping mechanism can also result in failure. These results means that the core clip-ping mechanism also plays a critical and indispensable role in learning. 

Question 2. Could the rollback mechanism and the trust region-based clipping improve its ability in bounding the probability ratio or the KL divergence? Could it benefit policy learning? 

In general, our new methods could take a significant ef-fect in restricting the policy compared to PPO. As can be seen in Fig. 3, the proportions of out-of-range proba-bility ratios of PPO-RB are much less than those of the original PPO during the training process. The probabil-ity ratios and the KL divergences of PPO-RB are also much smaller than those of PPO (see Fig. 4 and 5). Al-though PPO-RB focuses on restricting the probability ra-tio, it seems that the improved ability of restriction on the probability ratio also leads to better restriction on the KL divergence. For the trust region-based clipping meth-ods (TR-PPO and TR-PPO-RB), the KL divergences are also smaller than those of PPO (see Fig. 5). Especially, TR-PPO possesses the enhanced restriction ability on the KL divergence even it does not incorporate the rollback mechanism. Our new methods could benefit policy learning in both sample efficiency and policy performance. As listed in Table 1 (a), all the three new methods require less sam-ples to hit the threshold on all tasks. Especially, these new methods requires about 3/5 samples of PPO on Hop-per, Walker2d and Swimmer. As Table 1 (b) lists, all the three proposed methods achieve much higher episode re-wards than PPO does on Walker2d, Reacher, Swimmer, HalfCheetah (while performs fairly good as PPO on the remaining tasks). The improvement on policy learning of the newly pro-posed methods may be considered as a success of the “trust region” theorem, which makes the algorithm per-form less greedy to the advantage value of the old policy. To show this, we plot the entropy of the policy during the Figure 7: The policy entropy during the training process, averaged over 4 random seeds. The shaded area depicts the mean ± the standard deviation. training process. As can be seen in Fig. 7, the entropy of the three proposed methods are much larger than that of PPO on almost all tasks, which means the policy per-forms less greedy and explores more sufficiently. 

Question 3. How well do the ratio-based methods per-form compared to trust region-based ones? 

The ratio-based and trust region-based methods restrict the probability ratio and KL divergence respectively. The ratio-based methods include PPO and PPO-RB, while the trust region-based methods include TR-PPO and TR-PPO-RB. We consider two groups of comparisons, that is, PPO vs. TR-PPO and PPO-RB vs. TR-PPO-RB, since the only difference within each group is the the measure-ment of the policies. In general, the trust region-based methods are more sam-ple efficient than the ratio-based ones, and they could ob-tain a better policy on most of the tasks. As listed in Ta-ble 1 (a), both TR-PPO and TR-PPO-RB require much fewer episodes to achieve the threshold than PPO and PPO-RB do on all the tasks. Notably, on Hopper and Swimmer, TR-PPO requires almost half of the episodes of PPO. Besides, as listed in Table 1 (b), the episode re-wards of TR-PPO and TR-PPO-RB are better than those of PPO and PPO-RB on 4 of the 6 tasks except Humanoid and Swimmer. As Fig. 7 plots, the entropies of trust region-based tends to be larger than those of ratio-based on all tasks, and the entropies even increase at the lat-ter stages of training process. On the one hand, larger entropy may make trust region-based methods explore more sufficiently. On the other hand, it may make the policy hardly converge to the optimal policy. 

Comparison with the state-of-art method: We com-pare our methods with soft actor critic (SAC) (Haarnoja et al., 2018). As Table 1 lists, our methods are fairly bet-ter than SAC on 4 of 6 tasks. In addition, the variants of PPO are much more computationally efficient than SAC. Within one million timesteps, the training wall-clock time for all variants of PPO is about 32 min; for SAC, 182 min (see Appendix B.4 for more detail). Fur-thermore, the variants of PPO require relatively less ef-fort on hyperparameter tuning as we use the same hyper-parameter across most of the tasks. Our methods perform worse than SAC on the remaining 2 tasks. This may due to that we adopt an on-policy ap-proach to learn the actor and critic while SAC adopts an off-policy one. We have also evaluated two variants of SAC which incorporate the clipping technique, termed as PPO-SAC and TR-PPO-SAC, which use ratio-based and trust region-based clipping respectively. As Table 1 lists, the introduced clipping mechanism could improve SAC on both sample efficiency and policy performance on 5 of 6 tasks (see Appendix B.2 for more detail). 

# 7 CONCLUSION 

Despite the effectiveness of the well-known PPO, it somehow lacks theoretical justification, and its actual op-timization behaviour is less studied. To our knowledge, this is the first work to reveal the reason why PPO could neither strictly bound the probability ratio nor enforce a well-defined trust region constraint. Based on this obser-vation, we proposed a trust region-based clipping objec-tive function with a rollback operation. The trust region-based clipping is more theoretically justified while the rollback operation could enhance its ability in restrict-ing policy. Both these two techniques significantly im-prove ability in restricting policy and maintaining train-ing stability. Extensive results show the effectiveness of the proposed methods. Deep RL algorithms have been notorious in its tricky im-plementations and require much effort to tune the hyper-parameters (Islam et al., 2017; Henderson et al., 2018). Our three variants of the proposed methods are equally simple to implement and tune as PPO. They may be con-sidered as useful alternatives to PPO. 

Acknowledgements 

This work is partially supported by National Science Foundation of China (61672280, 61373060, 61732006), AI+ Project of NUAA(56XZA18009), Postgraduate Research & Practice Innovation Program of Jiangsu Province (KYCX19 0195). References 

Bellemare, M. G., Naddaf, Y., Veness, J., and Bowling, M. The arcade learning environment: An evaluation platform for general agents. Journal of Artificial Intel-ligence Research , 47:253–279, 2013. Brockman, G., Cheung, V., Pettersson, L., Schneider, J., Schulman, J., Tang, J., and Zaremba, W. Openai gym, 2016. Chen, G., Peng, Y., and Zhang, M. An adaptive clipping approach for proximal policy optimization. CoRR ,abs/1804.06461, 2018. Dhariwal, P., Hesse, C., Klimov, O., Nichol, A., Plap-pert, M., Radford, A., Schulman, J., Sidor, S., and Wu, Y. Openai baselines. https://github.com/ openai/baselines , 2017. Duan, Y., Chen, X., Houthooft, R., Schulman, J., and Abbeel, P. Benchmarking deep reinforcement learning for continuous control. In International Conference on Machine Learning , pp. 1329–1338, 2016. Haarnoja, T., Zhou, A., Abbeel, P., and Levine, S. Soft actor-critic: Off-policy maximum entropy deep rein-forcement learning with a stochastic actor. In Inter-national Conference on Machine Learning , pp. 1856– 1865, 2018. Henderson, P., Islam, R., Bachman, P., Pineau, J., Pre-cup, D., and Meger, D. Deep reinforcement learning that matters. In Thirty-Second AAAI Conference on Artificial Intelligence , 2018. Hmlinen, P., Babadi, A., Ma, X., and Lehtinen, J. PPO-CMA: Proximal policy optimization with covariance matrix adaptation. arXiv preprint arXiv:1810.02541 ,2018. Ilyas, A., Engstrom, L., Santurkar, S., Tsipras, D., Janoos, F., Rudolph, L., and Madry, A. Are deep policy gradient algorithms truly policy gradient algo-rithms? arXiv preprint arXiv:1811.02553 , 2018. Islam, R., Henderson, P., Gomrokchi, M., and Precup, D. Reproducibility of benchmarked deep reinforcement learning tasks for continuous control. arXiv preprint arXiv:1708.04133 , 2017. Kakade, S. and Langford, J. Approximately optimal ap-proximate reinforcement learning. In International Conference on Machine Learning (ICML) , volume 2, pp. 267–274, 2002. Kakade, S. M. A natural policy gradient. In Advances in Neural Information Processing Systems 14 , vol-ume 14, pp. 1531–1538, 2001. Levine, S., Finn, C., Darrell, T., and Abbeel, P. End-to-end training of deep visuomotor policies. Journal of Machine Learning Research , 17(1):1334–1373, 2016. Mnih, V., Kavukcuoglu, K., Silver, D., Rusu, A. A., Ve-ness, J., Bellemare, M. G., Graves, A., Riedmiller, M., Fidjeland, A. K., Ostrovski, G., et al. Human-level control through deep reinforcement learning. Nature ,518(7540):529, 2015. Mnih, V., Badia, A. P., Mirza, M., Graves, A., Lillicrap, T., Harley, T., Silver, D., and Kavukcuoglu, K. Asyn-chronous methods for deep reinforcement learning. In 

International Conference on Machine Learning , pp. 1928–1937, 2016. Peters, J. and Schaal, S. Reinforcement learning of motor skills with policy gradients. Neural networks , 21(4): 682–697, 2008. Peters, J., Mlling, K., and Altn, Y. Relative entropy pol-icy search. In AAAI’10 Proceedings of the Twenty-Fourth AAAI Conference on Artificial Intelligence , pp. 1607–1612, 2010. Schulman, J., Levine, S., Abbeel, P., Jordan, M., and Moritz, P. Trust region policy optimization. In Inter-national Conference on Machine Learning , pp. 1889– 1897, 2015. Schulman, J., Moritz, P., Levine, S., Jordan, M. I., and Abbeel, P. High-dimensional continuous control us-ing generalized advantage estimation. International Conference on Learning Representations , 2016. Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and Klimov, O. Proximal policy optimization algorithms. 

arXiv preprint arXiv:1707.06347 , 2017. Silver, D., Hubert, T., Schrittwieser, J., Antonoglou, I., Lai, M., Guez, A., Lanctot, M., Sifre, L., Kumaran, D., Graepel, T., et al. Mastering chess and shogi by self-play with a general reinforcement learning algorithm. 

arXiv preprint arXiv:1712.01815 , 2017. Sutton, R. S., McAllester, D. A., Singh, S. P., and Man-sour, Y. Policy gradient methods for reinforcement learning with function approximation. In Advances in Neural Information Processing Systems 12 , pp. 1057– 1063, 1999. Todorov, E., Erez, T., and Tassa, Y. Mujoco: A physics engine for model-based control. In 2012 IEEE/RSJ In-ternational Conference on Intelligent Robots and Sys-tems , pp. 5026–5033. IEEE, 2012. Wang, Y., He, H., Tan, X., and Gan, Y. Trust region-guided proximal policy optimization. arXiv preprint arXiv:1901.10314 , 2019. Williams, R. J. Simple statistical gradient-following algorithms for connectionist reinforcement learning. 

Machine learning , 8(3-4):229–256, 1992. Wu, Y., Mansimov, E., Grosse, R. B., Liao, S., and Ba, J. Scalable trust-region method for deep reinforcement learning using kronecker-factored approximation. In 

Advances in Neural Information Processing Systems ,pp. 5279–5288, 2017.