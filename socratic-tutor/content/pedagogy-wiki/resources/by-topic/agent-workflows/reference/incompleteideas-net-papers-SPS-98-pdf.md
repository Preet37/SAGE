# Source: http://incompleteideas.net/papers/SPS-98.pdf
# Author: Richard Sutton
# Author Slug: richard-sutton
# Title: Between MDPs and Semi-MDPs: Learning, Planning, and Representing Knowledge at Multiple Temporal Scales
# Fetched via: jina
# Date: 2026-04-10

Title: SPS-98.pdf



Number of Pages: 40

> Technical !Report !98-74, !Dept. !of !Computer !Science, !University !of !Massachusetts, !Amherst, !MA !01003. !! April, !1998.

# Between MDPs and Semi-MDPs: Learning, Planning, and Representing Knowledge at Multiple Temporal Scales 

Richard S. Sutton rich@cs.umass.edu 

Doina Precup dprecup@cs.umass.edu 

University of Massachusetts, Amherst, MA 01003 USA 

Satinder Singh baveja@cs.colorado.edu 

University of Colorado, Boulder, CO 80309 USA 

Abstract 

Learning, planning, and representing knowledge at multiple levels of temporal abstrac-tion are key challenges for AI. In this paper we develop an approach to these problems based on the mathematical framework of reinforcement learning and Markov decision pro-cesses (MDPs). We extend the usual notion of action to include options —whole courses of behavior that may be temporally extended, stochastic, and contingent on events. Ex-amples of options include picking up an object, going to lunch, and traveling to a distant city, as well as primitive actions such as muscle twitches and joint torques. Options may be given a priori, learned by experience, or both. They may be used interchangeably with actions in a variety of planning and learning methods. The theory of semi-Markov decision processes (SMDPs) can be applied to model the consequences of options and as a basis for planning and learning methods using them. In this paper we develop these connections, building on prior work by Bradtke and Du ff (1995), Parr (in prep.) and others. Our main novel results concern the interface between the MDP and SMDP levels of analysis. We show how a set of options can be altered by changing only their termination conditions to improve over SMDP methods with no additional cost. We also introduce intra-option 

temporal-di ff erence methods that are able to learn from fragments of an option’s execution. Finally, we propose a notion of subgoal which can be used to improve the options them-selves. Overall, we argue that options and their models provide hitherto missing aspects of a powerful, clear, and expressive framework for representing and organizing knowledge. 

1. Temporal Abstraction 

To make everyday decisions, people must foresee the consequences of their possible courses of action at multiple levels of temporal abstraction. Consider a traveler deciding to undertake a journey to a distant city. To decide whether or not to go, the benefits of the trip must be weighed against the expense. Having decided to go, choices must be made at each leg, e.g., whether to fly or to drive, whether to take a taxi or to arrange a ride. Each of these steps involves foresight and decision, all the way down to the smallest of actions. For example, just to call a taxi may involve finding a telephone, dialing each digit, and the individual muscle contractions to lift the receiver to the ear. Human decision making routinely involves Sutton, Precup, & Singh 

planning and foresight—choice among temporally-extended options—over a broad range of time scales. In this paper we examine the nature of the knowledge needed to plan and learn at multiple levels of temporal abstraction. The principal knowledge needed is the ability to predict the consequences of di ff erent courses of action. This may seem straightforward, but it is not. It is not at all clear what we mean either by a “course of action” or, particularly, by “its consequences”. One problem is that most courses of action have many consequences, with the immediate consequences di ff erent from the longer-term ones. For example, the course of action go-to-the-library may have the near-term consequence of being outdoors and walking, and the long-term consequence of being indoors and reading. In addition, we usually only consider courses of action for a limited but indefinite time period. An action like wash-the-car is most usefully executed up until the car is clean, but without specifying a particular time at which it is to stop. We seek a way of representing predictive knowledge that is: 

Expressive The representation must be able to include basic kinds of commonsense knowl-edge such as the examples we have mentioned. In particular, it should be able to pre-dict consequences that are temporally extended and uncertain. This criterion rules out many conventional engineering representations, such as di ff erential equations and transition probabilities. The representation should also be able to predict the con-sequences of courses of action that are stochastic and contingent on subsequent ob-servations. This rules out simple sequences of action with a deterministically known outcome, such as conventional macro-operators. 

Clear The representation should be clear, explicit, and grounded in primitive observations and actions. Ideally it would be expressed in a formal mathematical language. Any predictions made should be testable simply by comparing them against data: no human interpretation should be necessary. This criterion rules out conventional AI representations with ungrounded symbols. For example, “Tweety is a bird” relies on people to understand “Tweety,” “Bird,” and “is-a”; none of these has a clear interpretation in terms of observables. A related criterion is that the representation should be learnable. Only a representation that is clear and directly testable from observables is likely to be learnable. A clear representation need not be unambiguous. For example, it could predict that one of two events will occur at a particular time, but not specify which of them will occur. 

Suitable for Planning A representation of knowledge must be suitable for how it will be used as part of planning and decision-making. In particular, the representation should enable interrelating and intermixing knowledge at di ff erent levels of temporal abstraction. It should be clear that we are addressing a fundamental question of AI: how should an intelligent agent represent its knowledge of the world? We are interested here in the underlying semantics of the knowledge, not with its surface form. In particular, we are not concerned with the data structures of the knowledge representation, e.g., whether the 2Between MDPs and Semi-MDPs 

knowledge is represented by neural networks or symbolic rules. Whatever data structures are used to generate the predictions, our concern is with their meaning , i.e., with the interpretation that we or that other parts of the system can make of the predictions. Is the meaning clear and grounded enough to be tested and learned? Do the representable meanings include the commonsense predictions we seem to use in everyday planning? Are these meanings su ffi cient to support e ff ective planning? Planning with temporally extended actions has been extensively explored in several fields. Early AI research focused on it from the point of view of abstraction in planning (e.g., Fikes, Hart, and Nilsson, 1972; Newell and Simon, 1972; Nilsson, 1973; Sacerdoti, 1974). More recently, macro-operators, qualitative modeling, and other ways of chunking action selections into units have been extensively developed (e.g., Kuipers, 1979; de Kleer and Brown, 1984; Korf, 1985, 1987; Laird, Rosenbloom and Newell, 1986; Minton, 1988; Iba, 1989; Drescher, 1991; Ruby and Kibler, 1992; Dejong, 1994; Levinson and Fuchs, 1994; Nilsson, 1994; Say and Selahattin, 1996; Brafman and Moshe, 1997; Haigh, Shewchuk, and Veloso, 1997). Roboticists and control engineers have long considered methodologies for combining and switching between independently designed controllers (e.g., Brooks, 1986; Maes, 1991; Koza and Rice, 1992; Brockett, 1993; Grossman et al., 1993; Mill´ an, 1994; Araujo and Grupen, 1996; Colombetti, Dorigo, and Borghi, 1996; Dorigo and Colombetti, 1994; T´ oth, Kov´ acs, and L¨ orincz, 1995; Sastry, 1997; Rosenstein and Cohen, 1998). More recently, the topic has been taken up within the framework of MDPs and reinforcement learning (Watkins, 1989; Ring, 1991; Wixson, 1991; Schmidhuber, 1991; Mahadevan and Connell, 1992; Tenenberg, Karlsson, and Whitehead, 1992; Lin, 1993; Dayan and Hinton, 1993; Dayan, 1993; Kaelbling, 1993; Singh et al., 1994; Chrisman, 1994; Hansen, 1994; Uchibe, Asada and Hosada, 1996; Asada et al., 1996; Thrun and Schwartz, 1995; Kalm´ ar, Szepesv´ ari, and L¨ orincz, 1997, in prep.; Dietterich, 1997; Matari´ c, 1997; Huber and Gru-pen, 1997; Wiering and Schmidhuber, 1997; Parr and Russell, 1998; Drummond, 1998; Hauskrecht et al., in prep.; Meuleau, in prep.), within which we also work here. Our re-cent work in this area (Precup and Sutton, 1997, 1998; Precup, Sutton, and Singh, 1997, 1998; see also McGovern, Sutton, and Fagg, 1997; McGovern and Sutton, in prep.) can be viewed as a combination and generalization of Singh’s hierarchical Dyna (1992a,b,c,d) and Sutton’s mixture models (1995; Sutton and Pinette, 1985). In the current paper we simplify our treatment of the ideas by linking temporal abstraction to the theory of Semi-MDPs, as in Parr (in prep.), and as we discuss next. 

2. Between MDPs and SMDPs 

In this paper we explore the extent to which Markov decision processes (MDPs) can provide a mathematical foundation for the study of temporal abstraction and temporally extended action. MDPs have been widely used in AI in recent years to study planning and learning in stochastic environments (e.g., Barto, Bradtke, and Singh, 1995; Dean et al., 1995; Boutilier, Brafman, and Gelb, 1997; Simmons and Koenig, 1995; Ge ff ner and Bonet, in prep.). They provide a simple formulation of the AI problem including sensation, action, stochastic cause-and-e ff ect, and general goals formulated as reward signals. E ff ective learning and planning methods for MDPs have been proven in a number of significant applications (e.g., Mahade-3Sutton, Precup, & Singh 

MDP SMDP Options over MDP State Time 

Figure 1: The state trajectory of an MDP is made up of small, discrete-time transitions, whereas that of an SMDP comprises larger, continuous-time transitions. Options enable an MDP trajectory to be analyzed at either level. van et al., 1997; Marbach et al., 1998; Nie and Haykin, to appear; Singh and Bertsekas, 1997; Tesauro, 1995; Crites and Barto, 1996). However, conventional MDPs include only a single temporal scale of action. They are based on a discrete time step: the unitary action taken at time t aff ects the state and reward at time t + 1. There is no notion of a course of action persisting over a variable period of time. As a consequence, MDP methods are unable to take advantage of the simplicities and e ffi ciencies sometimes available at higher levels of temporal abstraction. An alternative is to use semi-Markov decision processes (SMDPs), a special kind of MDP appropriate for modeling continuous-time discrete-event systems (e.g., see Puterman, 1994; Mahadevan et al., 1997). The actions in SMDPs are permitted to take variable amounts of time and are intended to model temporally-extended courses of action. The existing theory of SMDPs also specifies how to model the results of these actions and how to plan with them. However, existing SMDP work is limited because the temporally extended actions are treated as indivisible and unknown units. There is no attempt in SMDP theory to look inside the temporally extended actions, to examine or modify how they are comprised of lower-level actions. As we have tried to suggest above, this is the essence of analyzing temporally abstract actions in AI applications: goal directed behavior involves multiple overlapping scales at which decisions are made and modified. In this paper we explore what might be viewed as a middle ground between MDPs and SMDPs. The base problem we consider is that of a conventional discrete-time MDP, but we also consider courses of action within the MDP whose results are state transitions of extended and variable duration. We use the term options for these courses of action, which include primitive actions as a special case. A fixed set of options defines a new discrete-time SMDP embedded within the original MDP, as suggested by Figure 1. The top panel shows 4Between MDPs and Semi-MDPs 

the state trajectory over discrete time of an MDP, the middle panel shows the larger state changes over continuous time of an SMDP, and the last panel shows how these two levels of analysis can be superimposed through the use of options. In this case the underlying base system is an MDP, with regular, single-step transitions, while the options define larger transitions, like those of an SMDP, that last for a number of discrete steps. All the usual SMDP theory applies to the superimposed SMDP defined by the options but, in addition, we have an explicit interpretation of them in terms of the underlying MDP. The SMDP actions (the options) are no longer black boxes, but policies in the base MDP which can be examined, changed, learned, and planned in their own right. This is what we see as the essential insight of the current work, as the key that enables new results of relevance to AI. The first part of this paper (Sections 3-5) develops the formal machinery for options as temporally extended actions equivalent to SMDP actions within a base MDP. We define new value functions and Bellman equations for this case, but most of the results are simple applications of existing SMDP theory or of existing reinforcement learning methods for SMDPs. The primary appeal of our formalization is that it enables multi-step options to be treated identically to primitive actions in existing planning and learning methods. In particular, the consequences of multi-step options can be modeled just as SMDP actions are modeled, and the models can be used in existing MDP planning methods interchangeably with models of primitive MDP actions. The second part of the paper introduces several ways of going beyond an SMDP analysis of options to change or learn their internal structure in terms of the MDP. The first issue we consider is that of e ff ectively combining a given set of policies into a single overall policy. For example, a robot may have pre-designed controllers for servoing joints to positions, picking up objects, and visual search, but still face a di ffi cult problem of how to coordinate and switch between these behaviors (e.g., Mahadevan and Connell, 1992; Matari´ c, 1997; Uchibe et al., 1996; Sastry, 1997; Maes and Brooks, 1990; Koza and Rice, 1992; Dorigo and Colombetti, 1994; Kalm´ ar et al., 1997, in prep). The second issue we consider is that of intra-option learning —looking inside options to learn simultaneously about all options consistent with each fragment of experience. Finally, we define a notion of subgoal that can be used to shape options and create new ones. 

3. Reinforcement Learning (MDP) Framework 

In this section we briefly describe the conventional reinforcement learning framework of discrete-time, finite Markov decision processes , or MDPs , which forms the basis for our extensions to temporally extended courses of action. In this framework, a learning agent 

interacts with an environment at some discrete, lowest-level time scale t = 0 , 1, 2, . . . . On each time step the agent perceives the state of the environment, s t ∈ S, and on that basis chooses a primitive action, at ∈ A s t . In response to each action, at , the environment produces one step later a numerical reward, rt+1 , and a next state, s t+1 . It is notationaly convenient to suppress the di ff erences in available actions across states whenever possible; we let A = ⋃ 

> s∈S

A s denote the union of the action sets. If S and A, are finite, then the 5Sutton, Precup, & Singh 

environment’s transition dynamics are modeled by one-step state-transition probabilities, 

p ass ′ = Pr {

s t+1 = s ′ | s t = s, a t = a

> }

,

and one-step expected rewards, 

r as = E{rt+1 | s t = s, a t = a},

for all s, s ′ ∈ S and a ∈ A (it is understood here that p ass ′ = 0 for a " ∈ A s ). These two sets of quantities together constitute the one-step model of the environment. The agent’s objective is to learn an optimal Markov policy , a mapping from states to probabilities of taking each available primitive action, π : S × A $ → [0 , 1], that maximizes the expected discounted future reward from each state s:

V π (s) = E

> {

rt+1 + γrt+1 + γ 2 rt+1 + · · ·  

> ∣∣∣

s t = s, π

> }

(1) = E

> {

rt+1 + γV π (s t+1 ) 

> ∣∣∣

s t = s, π

> }

= ∑

> a∈As

π(s, a )

> [

r as + γ ∑ 

> s′

p ass ′ V π (s ′ )

> ]

, (2) where π(s, a ) is the probability with which the policy π chooses action a ∈ A s in state s,and γ ∈ [0 , 1] is a discount-rate parameter. This quantity, V π (s), is called the value of state 

s under policy π, and V π is called the state-value function for π. The optimal state-value function gives the value of a state under an optimal policy: 

V ∗ (s) = max  

> π

V π (s) (3) = max 

> a∈As

E

> {

rt+1 + γV ∗ (s t+1 ) 

> ∣∣∣

s t = s, a t = a

> }

= max 

> a∈As
> [

r as + γ ∑ 

> s′

p ass ′ V ∗ (s ′ )

> ]

. (4) Any policy that achieves the maximum in (3) is by definition an optimal policy. Thus, given V ∗ , an optimal policy is easily formed by choosing in each state s any action that achieves the maximum in (4). Planning in reinforcement learning refers to the use of models of the environment to compute value functions and thereby to optimize or improve policies. Particularly useful in this regard are Bellman equations, such as (2) and (4), which recursively relate value functions to themselves. If we treat the values, V π (s) or V ∗ (s), as unknowns, then a set of Bellman equations, for all s ∈ S, forms a system of equations whose unique solution is in fact V π or V ∗ as given by (1) or (3). This fact is key to the way in which all temporal-di ff erence and dynamic programming methods estimate value functions. Particularly important for learning methods is a parallel set of value functions and Bellman equations for state–action pairs rather than for states. The value of taking action 

a in state s under policy π, denoted Qπ (s, a ), is the expected discounted future reward starting in s, taking a, and henceforth following π:

Qπ (s, a ) = E

> {

rt+1 + γrt+1 + γ 2 rt+1 + · · ·  

> ∣∣∣

s t = s, a t = a, π

> }
> 6Between MDPs and Semi-MDPs

= r as + γ ∑ 

> s′

p ass ′ V π (s ′ )= r as + γ ∑ 

> s′

p ass ′

> ∑
> a′

π(s, a ′ )Qπ (s ′ , a ′ ).

This is known as the action-value function for policy π. The optimal action-value function is 

Q∗ (s, a ) = max  

> π

Qπ (s, a )= r as + γ ∑ 

> s′

p ass ′ max  

> a′

Q∗ (s ′ , a ′ ).

Finally, many tasks are episodic in nature, involving repeated trials, or episodes , each ending with a reset to a standard state or state distribution. In these episodic tasks , we include a single special terminal state , arrival in which terminates the current episode. The set of regular states plus the terminal state (if there is one) is denoted S + . Thus, the s ′ in 

p ass ′ in general ranges over the set S + rather than just S as stated earlier. In an episodic task, values are defined by the expected cumulative reward up until termination rather than over the infinite future (or, equivalently, we can consider the terminal state to transition to itself forever with a reward of zero). 

4. Options 

We use the term options for our generalization of primitive actions to include temporally extended courses of action. Options consist of three components: a policy π : S ×A $ → [0 , 1], a termination condition β : S + $ → [0 , 1], and an input set I ⊆ S. An option 〈I, π, β〉 is available in state s if and only if s ∈ I. If the option is taken, then actions are selected according to π until the option terminates stochastically according to β. In particular, if the option taken in state s t is Markov , then the next action at is selected according to the prob-ability distribution π(s, ·). The environment then makes a transition to state s t+1 , where the option either terminates, with probability β(s t+1 ), or else continues, determining at+1 

according to π(s t+1 , ·), possibly terminating in s t+2 according to β(s t+2 ), and so on. 1 When the option terminates, then the agent has the opportunity to select another option. For example, an option named open-the-door might consist of a policy for reaching, grasping and turning the door knob, a termination condition for recognizing that the door has been opened, and an input set restricting consideration of open-the-door to states in which a door is present. In episodic tasks, termination of an episode also terminates the current option (i.e., β maps the terminal state to 1 in all options). The input set and termination condition of an option together restrict its range of application in a potentially useful way. In particular, they limit the range over which the option’s policy need be defined. For example, a handcrafted policy π for a mobile robot to dock with its battery charger might be defined only for states I in which the battery charger         

> 1. The termination condition βplays a role similar to the βin β-models (Sutton, 1995), but with an opposite sense. That is, β(s) in this paper corresponds to 1 −β(s) in that earlier paper.
> 7Sutton, Precup, & Singh

is within sight. The termination condition β could be defined to be 1 outside of I and when the robot is successfully docked. A subpolicy for servoing a robot arm to a particular joint configuration could similarly have a set of allowed starting states, a controller to be applied to them, and a termination condition indicating that either the target configuration had been reached within some tolerance or that some unexpected event had taken the subpolicy outside its domain of application. For Markov options it is natural to assume that all states where an option might continue are also states where the option might be taken (i.e., that 

{s : β(s) < 1} ⊆I ). In this case, π need only be defined over I rather than over all of S.Sometimes it is useful for options to “timeout,” to terminate after some period of time has elapsed even if they have failed to reach any particular state. Unfortunately, this is not possible with Markov options because their termination decisions are made solely on the basis of the current state, not on how long the option has been executing. To handle this and other cases of interest we consider a generalization to semi-Markov options, in which policies and termination conditions may make their choices dependent on all prior events since the option was initiated. In general, an option is initiated at some time, say 

t, determines the actions selected for some number of steps, say k, and then terminates in s t+k . At each intermediate time T , t ≤ T < t + k, the decisions of a Markov option may depend only on s T , whereas the decisions of a semi-Markov option may depend on the entire sequence s t , a t , r t+1 , s t+1 , a t+1 , . . . , r T , s T , but not on events prior to s t (or after s T ). We call this sequence the history from t to T and denote it by htT . We denote the set of all histories by Ω. In semi-Markov options, the policy and termination condition are functions of possible histories, that is, they are π : Ω×A $ → [0 , 1] and β : Ω $ → [0 , 1]. The semi-Markov case is also useful for cases in which options use a more detailed state representation than is available to the policy that selects the options. Given a set of options, their input sets implicitly define a set of available options Os

for each state s ∈ S. These Os are much like the sets of available actions, A s . We can unify these two kinds of sets by noting that actions can be considered a special case of options. Each action a corresponds to an option that is available whenever a is available (I = {s : a ∈ A s }), that always lasts exactly one step ( β(s) = 1 , ∀s ∈ S), and that selects 

a everywhere ( π(s, a ) = 1 , ∀s ∈ I). Thus, we can consider the agent’s choice at each time to be entirely among options, some of which persist for a single time step, others which are more temporally extended. The former we refer to as one-step or primitive options and the latter as multi-step options. Just as in the case of actions, it is convenient to notationaly suppress the di ff erences in available options across states. We let O = ⋃ 

> s∈S

Os denote the set of all available options. Our definition of options is crafted to make them as much like actions as possible, except temporally extended. Because options terminate in a well defined way, we can consider sequences of them in much the same way as we consider sequences of actions. We can consider policies that select options instead of primitive actions, and we can model the consequences of selecting an option much as we model the results of an action. Let us consider each of these in turn. Given any two options a and b, we can consider taking them in sequence, that is, we can consider first taking a until it terminates, and then b until it terminates (or omitting b

> 8

Between MDPs and Semi-MDPs 

altogether if a terminates in a state outside of b’s input set). We say that the two options are composed to yield a new option, denoted ab , corresponding to this way of behaving. The composition of two Markov options will in general be semi-Markov, not Markov, because actions are chosen di ff erently before and after the first option terminates. The composi-tion of two semi-Markov options is always another semi-Markov option. Because actions are special cases of options, we can also compose them, producing a deterministic action sequence, in other words, a classical macro-operator. More interesting are policies over options . When initiated in a state s t , the Markov policy over options μ : S × O $ → [0 , 1] selects an option o ∈ Os according to probability distribution μ(s t , ·). The option o is then taken in s t , determining actions until it terminates in s t+k , at which point a new option is selected, according to μ(s t+k , ·), and so on. In this way a policy over options, μ, determines a conventional policy over actions, or flat policy ,

π = f lat (μ). Henceforth we use the unqualified term policy for policies over options, which include flat policies as a special case. Note that even if a policy is Markov and all of the options it selects are Markov, the corresponding flat policy is unlikely to be Markov if any of the options are multi-step (temporally extended). The action selected by the flat policy in state s T depends not just on s T but on the option being followed at that time, and this depends stochastically on the entire history htT since the policy was initiated at time t.By analogy to semi-Markov options, we call policies that depend on histories in this way 

semi-Markov policies. 2

Our definitions of state values and action values can be generalized to apply to general policies and options. First we define the value of a state s ∈ S under a semi-Markov flat policy π as the expected return if the policy is started in s:

V π (s) def 

= E

{

rt+1 + γrt+2 + γ 2 rt+3 + · · · 

∣∣∣ E(π, s, t )

}

,

where E(π, s, t ) denotes the event of π being initiated in s at time t. The value of a state under a general policy μ can then be defined as the value of the state under the corresponding flat policy: V μ (s) def 

= V f lat (μ) (s), for all s ∈ S.It is natural to generalize action-value functions to option -value functions. We define 

Qμ (s, o ), the value of taking option o in state s ∈ I under policy μ, as 

Qμ (s, o ) def 

= E

{

rt+1 + γrt+2 + γ 2 rt+3 + · · · 

∣∣∣ E(oμ, s, t )

}

,

where oμ , the composition of o and μ, denotes the semi-Markov policy that first follows o

until it terminates and then initiates μ in the resultant state. 

5. SMDP (Option-to-Option) Methods 

Options are closely related to the actions in a special kind of decision problem known as a 

semi-Markov decision process , or SMDP (e.g., see Puterman, 1994). In fact, any MDP with   

> 2. This and other similarities suggest that the concepts of policy and option can be unified. In such a unification, options would select other options, and thus arbitrary hierarchical structures would be permitted. Although this appears straightforward, for simplicity we restrict ourselves in this paper to just two levels: policies that select options, and options that select actions.

9Sutton, Precup, & Singh 

a fixed set of options is an SMDP, as we state formally below. This theorem is not really a result, but a simple observation that follows more or less immediately from definitions. We present it as a theorem to highlight it and state explicitly its conditions and consequences: 

Theorem 1 (MDP + Options = SMDP) For any MDP, and any set of options de-fined on that MDP, the decision process that selects among those options, executing each to termination, is an SMDP. 

Proof: (Sketch) An SMDP consists of 1) a set of states, 2) a set of actions, 3) for each pair of state and action, an expected cumulative discounted reward, and 4) a well-defined joint distribution of the next state and transit time. In our case, the set of states is S, and the set of actions is just the set of options. The expected reward and the next-state and transit-time distributions are defined for each state and option by the MDP and by the option’s policy and termination condition, π and β. These expectations and distributions are well defined because the MDP is Markov and the options are semi-Markov; thus the next state, reward, and time are dependent only on the option and the state in which it was initiated. The transit times of options are always discrete, but this is simply a special case of the arbitrary real intervals permitted in SMDPs. +

The relationship between MDPs, options, and SMDPs provides a basis for the theory of planning and learning methods with options. In later sections we discuss the limitations of this theory due to its treatment of options as indivisible units without internal structure, but in this section we focus on establishing the benefits and assurances that it provides. We establish theoretical foundations and then survey SMDP methods for planning and learning with options. Although our formalism is slightly di ff erent, these results are in essence taken or adapted from prior work (including classical SMDP work and Singh, 1992a,b,c,d; Bradtke and Du ff , 1995; Sutton, 1995; Precup and Sutton, 1997, 1998; Precup, Sutton, and Singh, 1997, 1998; Parr and Russell, 1998; McGovern, Sutton, and Fagg, 1997; Parr, in prep.). A result very similar to Theorem 1 was proved in detail by Parr (in prep.). In the sections following this one we present new methods that improve over SMDP methods. Planning with options requires a model of their consequences. Fortunately, the appro-priate form of model for options, analogous to the r as and p ass ′ defined earlier for actions, is known from existing SMDP theory. For each state in which an option may be started, this kind of model predicts the state in which the option will terminate and the total reward received along the way. These quantities are discounted in a particular way. For any option 

o, let E(o, s, t ) denote the event of o being initiated in state s at time t. Then the reward part of the model of o for any state s ∈ S is 

r os = E

> {

rt+1 + γrt+2 + · · · + γ k−1 rt+k 

> ∣∣∣

E(o, s, t )

> }

, (5) where t + k is the random time at which o terminates. The state-prediction part of the model of o for state s is 

p oss ′ =

> ∞∑
> j=1

γ j Pr { s t+k = s ′ , k = j | E (o, s, t )

> }

= E

> {

γ k δs ′ s t+k | E (o, s, t )

> }

, (6) 10 Between MDPs and Semi-MDPs 

for all s ′ ∈ S, under the same conditions, where δss ′ is an identity indicator, equal to 1 if 

s = s ′ , and equal to 0 otherwise. Thus, p oss ′ is a combination of the likelihood that s ′ is the state in which o terminates together with a measure of how delayed that outcome is relative to γ. We call this kind of model a multi-time model (Precup and Sutton, 1997, 1998) because it describes the outcome of an option not at a single time but at potentially many di ff erent times, appropriately combined. 3

Using multi-time models we can write Bellman equations for general policies and options. For any Markov policy μ, the state-value function can be written 

V μ (s) = E

{

rt+1 + · · · + γ k−1 rt+k + γ k V μ (s t+k )

∣∣∣ E(μ, s, t )

}

,

where k is the duration of the first option selected by μ,= ∑

> o∈Os

μ(s, o )

[

r os + ∑ 

> s′

p oss ′ V μ (s ′ )

]

, (7) which is a Bellman equation analogous to (2). The corresponding Bellman equation for the value of an option o in state s ∈ I is 

Qμ (s, o ) = E

{

rt+1 + · · · + γ k−1 rt+k + γ k V μ (s t+k )

∣∣∣ E(o, s, t )

}

= E

{

rt+1 + · · · + γ k−1 rt+k + γ k ∑ 

> o′∈Os

μ(s t+k , o ′ )Qμ (s t+k , o ′ )

∣∣∣ E(o, s, t )

}

= r os + ∑ 

> s′

p oss ′

∑ 

> o′∈Os

μ(s ′ , o ′ )Qμ (s ′ , o ′ ). (8) Note that all these equations specialize to those given earlier in the special case in which μ

is a conventional policy and o is a conventional action. Also note that Qμ (s, o ) = V oμ (s). Finally, there are generalizations of optimal value functions and optimal Bellman equa-tions to options and to policies over options. Of course the conventional optimal value functions V ∗ and Q∗ are not a ff ected by the introduction of options; one can ultimately do just as well with primitive actions as one can with options. Nevertheless, it is interesting to know how well one can do with a restricted set of options that does not include all the actions. For example, in planning one might first consider only high-level options in order to find an approximate plan quickly. Let us denote the restricted set of options by O and the set of all policies selecting only from options in O by Π(O). Then the optimal value function given that we can select only from O is 

V ∗ 

> O

(s) def 

= max  

> μ∈Π(O)

V μ (s)= max 

> o∈Os

E

{

rt+1 + · · · + γ k−1 rt+k + γ k V ∗ 

> O

(s t+k )

∣∣∣ E(o, s, t )

}

,

where k is the duration of o when taken in s t ,         

> 3. Note that the definition of state predictions in multi-time models di ff ers slightly from that given earlier for primitive actions. Under the new definition, the model of transition from state sto s′for primitive action ais not simply the corresponding transition probability, but the transition probability times γ.Henceforth we use the new definition given by (6).

11 Sutton, Precup, & Singh 

= max 

> o∈Os

[

r os + ∑ 

> s′

p oss ′ V ∗ 

> O

(s ′ )

]

(9) = max 

> o∈Os

E

{

r + γ k V ∗ 

> O

(s ′ )

∣∣∣ E(o, s )

}

, (10) where E(o, s ) denotes option o being initiated in state s. Conditional on this event are the usual random variables: s ′ is the state in which o terminates, r is the cumulative discounted reward along the way, and k is the number of time steps elapsing between s and s ′ . The value functions and Bellman equations for optimal option values are 

Q∗ 

> O

(s, o ) def 

= max  

> μ∈Π(O)

Qμ (s, o )= E

{

rt+1 + · · · + γ k−1 rt+k + γ k V ∗ 

> O

(s t+k )

∣∣∣ E(o, s, t )

}

,

where k is the duration of o from s t ,= E

{

rt+1 + · · · + γ k−1 rt+k + γ k max  

> o′∈Ost+k

Q∗ 

> O

(s t+k , o ′ )

∣∣∣ E(o, s, t )

}

,

= r os + ∑ 

> s′

p oss ′ max  

> o′∈Ost+k

Q∗ 

> O

(s ′ , o ′ ) (11) = E

{

r + γ k max  

> o′∈Ost+k

Q∗ 

> O

(s ′ , o ′ )

∣∣∣ E(o, s )

}

,

where r, k, and s ′ are again the reward, number of steps, and next state due to taking 

o ∈ Os .Given a set of options, O, a corresponding optimal policy , denoted μ ∗ 

> O

, is any policy that achieves V ∗ 

> O

, i.e., for which V μ∗ 

> O

(s) = V ∗ 

> O

(s) in all states s ∈ S. If V ∗ 

> O

and models of the options are known, then optimal policies can be formed by choosing in any proportion among the maximizing options in (9) or (10). Or, if Q∗ 

> O

is known, then optimal policies can be found without a model by choosing in each state s in any proportion among the options 

o for which Q∗ 

> O

(s, o ) = max o′ Q∗ 

> O

(s, o ′ ). In this way, computing approximations to V ∗ 

> O

or 

Q∗ 

> O

become key goals of planning and learning methods with options. 

5.1 SMDP Planning 

With these definitions, an MDP together with the set of options O formally comprises an SMDP, and standard SMDP methods and results apply. Each of the Bellman equations for options, (7), (8), (9), and (11), defines a system of equations whose unique solution is the corresponding value function. These Bellman equations can be used as update rules in dynamic-programming-like planning methods for finding the value functions. Typically, solution methods for this problem maintain an approximation of V ∗ 

> O

(s) or Q∗ 

> O

(s, o ) for all states s ∈ S and all options o ∈ Os . For example, synchronous value iteration (SVI) with options initializes an approximate value function V0 (s) arbitrarily and then updates it by 

Vk+1 (s) ← max 

> o∈Os

r os + ∑   

> s′∈S+

p oss ′ Vk (s ′ )

 (12) 12 Between MDPs and Semi-MDPs 

> o
> HALLWAYS
> o

8 multi-step options up down right left (to each room’s 2 hallways) 

> G

4 stochastic primitive actions Fail 33% of the time 

> G

Figure 2: The rooms example is a gridworld environment with stochastic cell-to-cell actions and room-to-room hallway options. Two of the hallway options are suggested by the arrows labeled o1 and o2 . The labels G1 and G2 indicate two locations used as goals in experiments described in the text. for all s ∈ S. The action-value form of SVI initializes Q0 (s, o ) arbitrarily and then updates it by 

Qk+1 (s, o ) ← r os + ∑   

> s′∈S+

p oss ′ max  

> o′∈Os′

Qk (s ′ , o ′ )for all s ∈ S and o ∈ Os . Note that these algorithms reduce to the conventional value iteration algorithms in the special case that O = A. Standard results from SMDP theory guarantee that these processes converge for general semi-Markov options: lim k→∞ Vk (s) = 

V ∗ 

> O

(s) and lim k→∞ Qk (s, o ) = Q∗ 

> O

(s, o ) for all s ∈ S, o ∈ O, and for all sets of options O.The plans (policies) found using temporally abstract options are approximate in the sense that they achieve only V ∗ 

> O

, which is less than the maximum possible, V ∗ . On the other hand, if the models used to find them are correct, then they are guaranteed to achieve 

V ∗ 

> O

. We call this the value achievement property of planning with options. This contrasts with planning methods that abstract over state space, which generally cannot be guaranteed to achieve their planned values even if their models are correct (e.g., Dean and Lin, 1995). As a simple illustration of planning with options, consider the rooms example , a grid-world environment of four rooms shown in Figure 2. The cells of the grid correspond to the states of the environment. From any state the agent can perform one of four actions, 

up , down , left or right , which have a stochastic e ff ect. With probability 2/3, the actions cause the agent to move one cell in the corresponding direction, and with probability 1/3, the agent moves instead in one of the other three directions, each with 1/9 probability. In either case, if the movement would take the agent into a wall then the agent remains in the same cell. For now we consider a case in which rewards are zero on all state transitions. 13 Sutton, Precup, & Singh 

Target Hallway 

Figure 3: The policy underlying one of the eight hallway options. 

# Iteration #1 Initial Values Iteration #2 

# O = A

Primitive options 

# O = H

Hallway options 

Figure 4: Value functions formed over iterations of planning by synchronous value iteration with primitive actions and with hallway options. The hallway options enabled planning to proceed room-by-room rather than cell-by-cell. The area of the disk in each cell is proportional to the estimated value of the state, where a disk that just fills a cell represents a value of 1.0. 14 Between MDPs and Semi-MDPs 

In each of the four rooms we provide two built-in hallway options designed to take the agent from anywhere within the room to one of the two hallway cells leading out of the room. A hallway option’s policy π follows a shortest path within the room to its target hallway while minimizing the chance of stumbling into the other hallway. For example, the policy for one hallway option is shown in Figure 3. The termination condition β(s) for each hallway option is zero for states s within the room and 1 for states outside the room, including the hallway states. The input set I comprises the states within the room plus the non-target hallway state leading into the room. Note that these options are deterministic and Markov, and that an option’s policy is not defined outside of its input set. We denote the set of eight hallway options by H. For each option o ∈ H, we also provide a priori its accurate model r os and p oss ′ , for all s ∈ I and s ′ ∈ S + , assuming there are no goal states. Note that although the transition models p oss ′ are nominally large (order |I| × |S + |), in fact they are sparse, and relatively little memory (order |I| × 2) is actually needed to hold the nonzero transitions from each state to the two adjacent hallway states. 4

Now consider a sequence of planning tasks for navigating within the grid to a designated goal state, in particular, to the hallway state labeled G1 in Figure 2. Formally, the goal state is a state from which all actions lead to the terminal state with a reward of +1. Throughout this paper we use discounting ( γ = 0 .9) with this task. As a planning method, we used SVI as given by (12), with various sets of options O.The initial value function V0 was 0 everywhere except the goal state, which was initialized to its correct value, V0 (G1 ) = 1, as shown in the leftmost panels of Figure 4. This figure contrasts planning with the original actions ( O = A) and planning with the hallway options and not the original actions ( O = H). The upper part of the figure shows the value function after the first two iterations of SVI using just primitive actions. The region of accurately valued states moved out by one cell on each iteration, but after two iterations most states still had their initial arbitrary value of zero. In the lower part of the figure are shown the corresponding value functions for SVI with the hallway options. In the first iteration all states in the rooms adjacent to the goal state became accurately valued, and in the second iteration all the states become accurately valued. Although the values continued to change by small amounts over subsequent iterations, a complete and optimal policy was known by this time. Rather than planning step-by-step, the hallway options enabled the planning to proceed at a higher level, room-by-room, and thus be much faster. The example above is a particularly favorable case for the use of multi-step options because the goal state is a hallway, the target state of some of the options. Next we consider a case in which there is no such coincidence, in which the goal lies in the middle of a room, in the state labeled G2 in Figure 2. The hallway options and their models were just as in the previous experiment. In this case, planning with (models of) the hallway options alone could never completely solve the task, because these take the agent only to hallways and thus never to the goal state. Figure 5 shows the value functions found over five iterations of SVI using both the hallway options and options corresponding to the primitive actions (i.e., using O = A ∪H ). In the first two iterations, accurate values were 

> 4. The o ff -target hallway states are exceptions in that they have three possible outcomes: the target hallway, themselves, and the neighboring state in the o ff -target room.
> 15 Sutton, Precup, & Singh

Iteration #1 Initial values Iteration #2 Iteration #3 Iteration #4 Iteration #5 

Figure 5: An example in which the goal is di ff erent from the subgoal of the hallway options. Planning here was by SVI with options O = A∪H. Initial progress was due to the models of the primitive actions, but by the third iteration room-to-room planning dominated and greatly accelerated planning. 16 Between MDPs and Semi-MDPs 

propagated from G2 by one cell per iteration by the models corresponding to the primitive actions. After two iterations, however, the first hallway state was reached, and subsequently room-to-room planning using the temporally extended hallway options dominated. Note how the lower-left most state was given a nonzero value during iteration three. This value corresponds to the plan of first going to the hallway state above and then down to the goal; it was overwritten by a larger value corresponding to a more direct route to the goal in the next iteration. Because of the options, a close approximation to the correct value function was found everywhere by the fourth iteration; without them only the states within three steps of the goal would have been given non-zero values by this time. We have used SVI in this example because it is a particularly simple planning method which makes the potential advantage of multi-step options particularly clear. In large problems, SVI is impractical because the number of states is too large to complete many iterations, often not even one. In practice it is often necessary to be very selective about the states updated, the options considered, and even the next states considered. These issues are not resolved by multi-step options, but neither are they greatly aggravated. Options provide a tool for dealing with them more flexibly. Planning with options need be no more complex than planning with actions. In the SVI experiments above there were four primitive options and eight hallway options, but in each state only two hallway options needed to be considered. In addition, the models of the primitive actions generate four possible successors with non-zero probability whereas the multi-step options generate only two. Thus planning with the multi-step options was actually computationally cheaper than conventional SVI in this case. In the second experiment this was not the case, but still the use of multi-step options did not greatly increase the computational costs. 

5.2 SMDP Value Learning 

The problem of finding an optimal policy over a set of options O can also be addressed by learning methods. Because the MDP augmented by the options is an SMDP, we can apply SMDP learning methods as developed by Bradtke and Du ff (1995), Parr and Russell (1998; Parr, in prep.), Mahadevan et al. (1997), or McGovern, Sutton and Fagg (1997). Much as in the planning methods discussed above, each option is viewed as an indivisible, opaque unit. When the execution of option o is started in state s, we next jump to the state 

s ′ in which o terminates. Based on this experience, an approximate option-value function 

Q(s, o ) is updated. For example, the SMDP version of one-step Q-learning (Bradtke and Du ff , 1995), which we call SMDP Q-learning , updates after each option termination by 

Q(s, o ) ← Q(s, o ) + α

> [

r + γ k max  

> a∈O

Q(s ′ , a ) − Q(s, o )

> ]

,

where k denotes the number of time steps elapsing between s and s ′ , r denotes the cumula-tive discounted reward over this time, and it is implicit that the step-size parameter α may depend arbitrarily on the states, option, and time steps. The estimate Q(s, o ) converges to Q∗ 

> O

(s, o ) for all s ∈ S and o ∈ O under conditions similar to those for conventional Q-learning (Parr, in prep.), from which it is easy to determine an optimal policy as described earlier. 17 Sutton, Precup, & Singh 

Episodes Episodes Steps per episode     

> AAAHAUHAUH

# Goal at G 

# Goal at G         

> 110 100 1000 10,000 10 100 1000 110 100 1000 10,000 10 100 1000
> HH

Figure 6: Learning curves for SMDP Q-learning in the rooms example with various goals and sets of options. After 100 episodes, the data points are averages over bins of 10 episodes to make the trends clearer. The step size parameter was optimized to the nearest power of 2 for each goal and set of options. The results shown used α = 1 

> 8

in all cases except that with O = H and G1 (α = 1 

> 16

) and that with 

O = A ∪H and G2 (α = 1 

> 4

). As an illustration, we applied SMDP Q-learning to the rooms example (Figure 2) with the goal at G1 and at G2 . As in the case of planning, we used three di ff erent sets of options, 

A, H, and A ∪H . In all cases, options were selected from the set according to an (-greedy 

method. That is, given the current estimates Q(s, o ), let o∗ = arg max o∈Os Q(s, o ) denote the best valued action (with ties broken randomly). Then the policy used to select options was 

μ(s, o ) = 

{ 1 − ( + (  

> |O s|

if o = o∗

(  

> |O s|

otherwise, for all s ∈ S and o ∈ O, where O is one of A, H, or A∪H. The probability of random action, 

(, was set at 0 .1 in all cases. The initial state of each trial was in the upper-left corner. Figure 6 shows learning curves for both goals and all sets of options. In all cases, multi-step options caused the goal to be reached much more quickly, even on the very first trial. With the goal at G1 , these methods maintained an advantage over conventional Q-learning throughout the experiment, presumably because they did less exploration. The results were similar with the goal at G2 , except that the H method performed worse than the others in the long term. This is because the best solution requires several steps of primitive actions (the hallway options alone find the best solution running between hallways that sometimes stumbles upon G2 ). For the same reason, the advantages of the A ∪H method over the A

method were also reduced. 18 Between MDPs and Semi-MDPs 

6. Termination Improvement 

SMDP methods apply to options, but only when they are treated as opaque indivisible units. More interesting and potentially more powerful methods are possible by looking inside options and by altering their internal structure. In this section we take a first step in altering options to make them more useful. This is the area where working simultaneously in terms of MDPs and SMDPs is most relevant. We can analyze options in terms of the SMDP and then use their MDP interpretation to change them and produce a new SMDP. In particular, in this section we consider altering the termination conditions of options. Note that treating options as indivisible units, as SMDP methods do, is limiting in an unnecessary way. Once an option has been selected, such methods require that its policy be followed until the option terminates. Suppose we have determined the option-value function 

Qμ (s, o ) for some policy μ and for all state–options pairs s, o that could be encountered while following μ. This function tells us how well we do while following μ, committing irrevocably to each option, but it can also be used to re-evaluate our commitment on each step. Suppose at time t we are in the midst of executing option o. If o is Markov in s, then we can compare the value of continuing with o, which is Qμ (s t , o ), to the value of terminating o and selecting a new option according to μ, which is V μ (s) = ∑ 

> q

μ(s, q )Qμ (s, q ). If the latter is more highly valued, then why not terminate o and allow the switch? We prove below that this new way of behaving will indeed be better. In the following theorem we characterize the new way of behaving as following a policy 

μ′ that is the same as the original policy, μ, but over a new set of options: μ ′ (s, o ′ ) = μ(s, o ), for all s ∈ S. Each new option o′ is the same as the corresponding old option o except that it terminates whenever termination seems better than continuing according to Qμ . In other words, the termination condition β ′ of o′ is the same as that of o except that β ′ (s) = 1 if 

Qμ (s, o ) < V μ (s). We call such a μ′ a termination improved policy of μ. The theorem below generalizes on the case described above in that termination improvement is optional, not required, at each state where it could be done; this weakens the requirement that Qμ (s, o )be completely known. A more important generalization is that the theorem applies to semi-Markov options rather than just Markov options. This is an important generalization, but can make the result seem less intuitively accessible on first reading. Fortunately, the result can be read as restricted to the Markov case simply by replacing every occurrence of “history” with “state”, set of histories, Ω, with set of states, S, etc. 

Theorem 2 (Termination Improvement) For any MDP, any set of options O, and any Markov policy μ : S × O $ → [0 , 1] , define a new set of options, O ′ , with a one-to-one mapping between the two option sets as follows: for every o = 〈I, π, β〉 ∈ O we define a corresponding o′ = 〈I, π, β ′ 〉 ∈ O ′ , where β ′ = β except that for any history h that ends in state s and in which Qμ (h, o ) < V μ (s), we may choose to set β ′ (h) = 1 . Any histories whose termination conditions are changed in this way are called termination-improved histories .Let policy μ′ be such that for all s ∈ S, and for all o′ ∈ O ′ , μ′ (s, o ′ ) = μ(s, o ), where o is the option in O corresponding to o′ . Then 1. V μ′

(s) ≥ V μ (s) for all s ∈ S.

> 19

Sutton, Precup, & Singh 

2. If from state s ∈ S there is a non-zero probability of encountering a termination-improved history upon initiating μ′ in s, then V μ′

(s) > V μ (s).

Proof: Shortly we show that, for an arbitrary start state s, executing the option given by the termination improved policy μ ′ and then following policy μ thereafter is no worse than always following policy μ. In other words, we show that the following inequality holds: 

∑

> o′

μ′ (s, o ′ )[ r o′ 

> s

+ ∑ 

> s′

p o′  

> ss ′

V μ (s ′ )] ≥ V μ (s) = ∑

> o

μ(s, o )[ r os + ∑ 

> s′

p oss ′ V μ (s ′ )] . (13) If this is true, then we can use it to expand the left-hand side, repeatedly replacing every occurrence of V μ (x) on the left by the corresponding ∑ 

> o′

μ′ (x, o ′ )[ r o′ 

> x

+ ∑  

> x′

p o′  

> xx ′

V μ (x′ )]. In the limit, the left-hand side becomes V μ′

, proving that V μ′

≥ V μ .To prove the inequality in (13), we note that for all s, μ ′ (s, o ′ ) = μ(s, o ), and show that 

r o′ 

> s

+ ∑ 

> s′

p o′  

> ss ′

V μ (s ′ ) ≥ r os + ∑ 

> s′

p oss ′ V μ (s ′ ) (14) as follows. Let Γ denote the set of all termination improved histories: Γ = {h ∈ Ω : β(h) " =

β ′ (h)}. Then, 

r o′ 

> s

+ ∑ 

> s′

p o′  

> ss ′

V μ (s ′ ) = E

{

r + γ k V μ (s ′ )

∣∣∣ E(o′ , s ), h ss ′ " ∈ Γ

}

+E

{

r + γ k V μ (s ′ )

∣∣∣ E(o′ , s ), h ss ′ ∈ Γ

}

,

where s ′ , r, and k are the next state, cumulative reward, and number of elapsed steps following option o from s (hss ′ is the history from s to s ′ ). Trajectories that end because of encountering a history not in Γ never encounter a history in Γ, and therefore also occur with the same probability and expected reward upon executing option o in state s. Therefore, if we continue the trajectories that end because of encountering a history in Γ with option o

until termination and thereafter follow policy μ, we get 

E

{

r + γ k V μ (s ′ )

∣∣∣ E(o′ , s ), h ss ′ " ∈ Γ

}

+ E

{

β(s ′ )[ r + γ k V μ (s ′ )] + (1 − β(s ′ ))[ r + γ k Qμ (hss ′ , o )] 

∣∣∣ E(o′ , s ), h ss ′ ∈ Γ

}

= r os + ∑ 

> s′

p oss ′ V μ (s ′ ),

because option o is semi-Markov. This proves (13) because for all hss ′ ∈ Γ, Qμ 

> O

(hss ′ , o ) ≤

V μ (s ′ ). Note that strict inequality holds in (14) if Qμ 

> O

(hss ′ , o ) < V μ (s ′ ) for at least one history hss ′ ∈ Γ that ends a trajectory generated by o′ with non-zero probability. +

As one application of this result, consider the case in which μ is an optimal policy for some given set of Markov options O. We have already discussed how we can, by planning or learning, determine the optimal value functions V ∗ 

> O

and Q∗ 

> O

and from them the optimal policy μ∗ 

> O

that achieves them. This is indeed the best that can be done without changing O,that is, in the SMDP defined by O, but less than the best possible achievable in the MDP, which is V ∗ = V ∗ 

> A

. But of course we typically do not wish to work directly in the primitive options A because of the computational expense. The termination improvement theorem 20 Between MDPs and Semi-MDPs 

gives us a way of improving over μ ∗ 

> O

with little additional computation by stepping outside 

O. That is, at each step we interrupt the current option and switch to any new option that is valued more highly according to Q∗ 

> O

. Checking for such options can typically be done at vastly less expense per time step than is involved in the combinatorial process of computing 

Q∗ 

> O

. In this sense, termination improvement gives us a nearly free improvement over any SMDP planning or learning method that computes Q∗ 

> O

as an intermediate step. Kaelbling (1993) was the first to demonstrate this e ff ect—improved performance by interrupting a temporally extended substep based on a value function found by planning at a higher level—albeit in a more restricted setting than we consider here. In the extreme case, we might interrupt on every step and switch to the greedy option— the option in that state that is most highly valued according to Q∗ 

> O

. In this case, options are never followed for more than one step, and they might seem superfluous. However, the options still play a role in determining Q∗ 

> O

, the basis on which the greedy switches are made, and recall that multi-step options enable Q∗ 

> O

to be found much more quickly than Q∗

could (Section 5). Thus, even if multi-step options are never actually followed for more than one step, they still provide substantial advantages in computation and in our theoretical understanding. Figure 7 shows a simple example. Here the task is to navigate from a start location to a goal location within a continuous two-dimensional state space. The actions are movements of 0.01 in any direction from the current state. Rather than work with these low-level actions, infinite in number, we introduce seven landmark locations in the space. For each landmark we define a controller that takes us to the landmark in a direct path (cf. Moore, 1994). Each controller is only applicable within a limited range of states, in this case within a certain distance of the corresponding landmark. Each controller then defines an option: the circular region around the controller’s landmark is the option’s input set, the controller itself is the policy, and arrival at the target landmark is the termination condition. We denote the set of seven landmark options by O. Any action within 0.01 of the goal location transitions to the terminal state, the discount rate γ is 1, and the reward is −1 on all transitions, which makes this a minimum-time task. One of the landmarks coincides with the goal, so it is possible to reach the goal while picking only from O. The optimal policy within O runs from landmark to landmark, as shown by the thin line in the upper panel of Figure 7. This is the optimal solution to the SMDP defined by O and is indeed the best that one can do while picking only from these options. But of course one can do better if the options are not followed all the way to each landmark. The trajectory shown by the thick line in Figure 7 cuts the corners and is shorter. This is the termination-improvement policy with respect to the SMDP-optimal policy. The termination improvement policy takes 474 steps from start to goal which, while not as good as the optimal policy in primitive actions (425 steps), is much better, for no additional cost, than the SMDP-optimal policy, which takes 600 steps. The state-value functions, V μ∗ 

> O

and V μ′

for the two policies are shown in the lower part of Figure 7. Figure 8 shows results for an example using controllers/options with dynamics. The task here is to move a mass along one dimension from rest at position 0.0 to rest at position 2.0, again in minimum time. There is no option that takes the system all the way from 21 Sutton, Precup, & Singh 

> SMDP Solution (600 Steps) Termination-Improved Solution (474 Steps) range (input set) of each run-to-landmark controller landmarks

SG0 1 2 30123-600 -500 -400 -300 -200 -100 00 1 2 30123-600 -500 -400 -300 -200 -100 0

## V - SMDP Value Function *

O

μγ

## Landmarks Problem 

## V - Termination Improved 

Figure 7: Termination improvement in navigating with landmark-directed controllers. The task (top) is to navigate from S to G in minimum time using options based on controllers that run each to one of seven landmarks (the black dots). The circles show the region around each landmark within which the controllers operate. The thin line shows the SMDP solution, the optimal behavior that uses only these controllers without interrupting them, and the thick line shows the corresponding termination improved solution, which cuts the corners. The lower two panels show the state-value functions for the SMDP and termination-improved solutions. 22 Between MDPs and Semi-MDPs     

> 00.02 0.04 0.06 00.5 11.5 2

# Position Velocity Termination Improved 121 Steps SMDP Solution 210 Steps 

Figure 8: Phase-space plot of the SMDP and termination improved policies in a simple dynamical task. The system is a mass moving in one dimension: xt+1 = xt + ˙ xt+1 ,˙xt+1 = ˙ xt +at −0.175 ˙ xt where xt is the position, ˙ xt the velocity, 0.175 a coe ffi cient of friction, and the action at an applied force. Two controllers are provided as options, one that drives the position to zero velocity at x∗ = 1 .0 and the other to x∗ = 2 .0. Whichever option is being followed at time t, its target position x∗

determines the action taken, according to at = 0 .01( x∗ − xt ). 23 Sutton, Precup, & Singh 

0.0 to 2.0, but we do have an option that takes it from 0.0 to 1.0 and another option that takes it from any position greater than 0.5 to 2.0. Both options control the system precisely to its target position and to zero velocity, terminating only when both of these are correct to within ( = 0 .0001. Using just these options, the best that can be done is to first move precisely to rest at 1.0, using the first option, then re-accelerate and move to 2.0 using the second option. This SMDP-optimal solution is much slower than the corresponding termination improved policy, as shown in Figure 8. Because of the need to slow down to near-zero velocity at 1.0, it takes over 200 time steps, whereas the improved policy takes only 121 steps. 

7. Intra-Option Model Learning 

The models of an option, r os and p oss ′ , can be learned from experience given knowledge of the option (i.e., of its I, π, and β). For a semi-Markov option, the only general approach is to execute the option to termination many times in each state s, recording in each case the resultant next state s ′ , cumulative discounted reward r, and elapsed time k. These outcomes are then averaged to approximate the expected values for r os and p oss ′ given by (5) and (6). For example, an incremental learning rule for this could update its estimates ˆ r os

and ˆ p osx , for all x ∈ S, after each execution of o in state s, by ˆr os = ˆ r os + α[r − ˆr os ], (15) and ˆp osx = ˆ p osx + α[γ k δxs ′ − ˆp osx ], (16) where the step-size parameter, α, may be constant or may depend on the state, option, and time. For example, if α is 1 divided by the number of times that o has been experienced in s,then these updates maintain the estimates as sample averages of the experienced outcomes. However the averaging is done, we call these SMDP model-learning methods because, like SMDP value-learning methods, they are based on jumping from initiation to termination of each option, ignoring what happens along the way. In the special case in which o is a primitive action, SMDP model-learning methods reduce to those used to learn conventional one-step models of actions. One drawback to SMDP model-learning methods is that they improve the model of an option only when the option terminates. Because of this, they cannot be used for nonterminating options and can only be applied to one option at a time—the one option that is executing at that time. For Markov options, special temporal-di ff erence methods can be used to learn usefully about the model of an option before the option terminates. We call these intra-option methods because they learn from experience within a single option. Intra-option methods can even be used to learn about the model of an option without ever executing the option, as long as some selections are made that are consistent with the option. Intra-option methods are examples of off -policy learning methods (Sutton and Barto, 1998) because they learn about the consequences of one policy while actually behaving according to another, potentially di ff erent policy. Intra-option methods can be used to simultaneously learn models of many di ff erent options from the same experience. 24 Between MDPs and Semi-MDPs 

Intra-option methods were introduced by Sutton (1995), but only for a prediction problem with a single unchanging policy, not the full control case we consider here. Just as there are Bellman equations for value functions, there are also Bellman equations for models of options. Consider the intra-option learning of the model of a Markov option 

o = 〈I, π, β〉. The correct model of o is related to itself by 

r os = ∑

> a∈As

π(s, a )E

{

r + γ(1 − β(s ′ )) r os ′

}

where r and s ′ are the reward and next state given that action a is taken in state s,= ∑

> a∈As

π(s, a )

[

r as + ∑ 

> s′

p ass ′ (1 − β(s ′ )) r os ′

]

,

and 

p osx = ∑

> a∈As

π(s, a )γE

{

(1 − β(s ′ )) p os ′ x + β(s ′ )δs ′ x

}

= ∑

> a∈As

π(s, a ) ∑ 

> s′

p ass ′ (1 − β(s ′ )) p os ′ x + β(s ′ )δs ′ x

for all s, x ∈ S. How can we turn these Bellman-like equations into update rules for learning the model? First consider that action at is taken in s t , and that the way it was selected is consistent with o = 〈I, π, β〉, that is, that at was selected with the distribution π(s t , ·). Then the Bellman equations above suggest the temporal-di ff erence update rules ˆr os t ← ˆr os t + α

[

rt+1 + γ(1 − β(s t+1 ))ˆ r os t+1 − ˆr os t

]

(17) and ˆp os t x ← ˆp os t x + α

[

γ(1 − β(s t+1 ))ˆ p os t+1 x + γβ (s t+1 )δs t+1 x − ˆp os t x

]

, (18) where ˆ p oss ′ and ˆ r os are the estimates of p oss ′ and r os , respectively, and α is a positive step-size parameter. The method we call one-step intra-option model learning applies these updates to every option consistent with every action taken, at . Of course, this is just the simplest intra-option model-learning method. Others may be possible using eligibility traces and standard tricks for o ff -policy learning (as in Sutton, 1995). As an illustration, consider the use of SMDP and intra-option model learning in the rooms example. As before, we assume that the eight hallway options are given, but now we assume that their models are not given and must be learned. In this experiment, the rewards were selected according to a normal probability distribution with a standard deviation of 0.1 and a mean that was di ff erent for each state–action pair. The means were selected randomly at the beginning of each run uniformly from the [ −1, 0] interval. Experience was generated by selecting randomly in each state among the two possible options and four possible actions, with no goal state. In the SMDP model-learning method, equations (15) and (16) were applied whenever an option terminated, whereas, in the intra-option model-learning method, equations (17) and (18) were applied on every step to all options that were consistent with the action taken on that step. In this example, all options are deterministic, 25 Sutton, Precup, & Singh      

> 01234020,000 40,000 60,000 80,000 100,000

Options Executed Options Executed SMDP Intra SMDP 1/t SMDP Intra SMDP 1/t Reward Prediction Error State Prediction Error Max Error Avg. Error 00.1 0.2 0.3 0.4 0.5 0.6 0.7 0 20,000 40,000 60,000 80,000 100,000 SMDP SMDP SMDP 1/t Intra Intra SMDP 1/t Max Error Avg. Error 

Figure 9: Learning curves for model learning by SMDP and intra-option methods. Shown are the average and maximum over I of the absolute errors between the learned and true models, averaged over the eight hallway options and 30 repetitions of the whole experiment. The lines labeled ‘SMDP 1/t’ are for the SMDP method using sample averages; the others all used α = 1 /4. so consistency with the action selected means simply that the option would have selected that action. For each method, we tried a range of values for the step-size parameter, α = 1 

> 2

, 1 

> 4

, 1 

> 8

, and  

> 1
> 16

. Results are shown in Figure 9 for the value that seemed to be best for each method, which happened to be α = 1 

> 4

in all cases. For the SMDP method, we also show results with the step-size parameter set such that the model estimates were sample averages, which should give the best possible performance of this method (these lines are labeled 1 /t ). The figure shows the average and maximum errors over the state–option space for each method, averaged over the eight options and 30 repetitions of the experiment. As expected, the intra-option method was able to learn significantly faster than the SMDP methods. 

8. Intra-Option Value Learning 

We turn now to the intra-option learning of option values and thus of optimal policies over options. If the options are semi-Markov, then again the SMDP methods described in Section 5.2 are probably the only feasible methods; a semi-Markov option must be completed before it can be evaluated in any way. But if the options are Markov and we are willing to look inside them, then we can consider intra-option methods. Just as in the case of model learning, intra-option methods for value learning are potentially more e ffi cient than SMDP methods because they extract more training examples from the same experience. 26 Between MDPs and Semi-MDPs 

For example, suppose we are learning to approximate Q∗ 

> O

(s, o ) and that o is Markov. Based on an execution of o from t to t+k, SMDP methods extract a single training example for Q∗ 

> O

(s, o ). But because o is Markov, it is, in a sense, also initiated at each of the steps between t and t + k. The jumps from each intermediate s i to s t+k are also valid experiences with o, experiences that can be used to improve estimates of Q∗ 

> O

(s i , o ). Or consider an option that is very similar to o and which would have selected the same actions, but which would have terminated one step later, at t + k + 1 rather than at t + k. Formally this is a di ff erent option, and formally it was not executed , yet all this experience could be used for learning relevant to it. In fact, an option can often learn something from experience that is only slightly related (occasionally selecting the same actions) to what would be generated by executing the option. This is the idea of o ff -policy training—to make full use of whatever experience occurs to learn as much as possible about all options irrespective of their role in generating the experience. To make the best use of experience we would like an o ff -policy and intra-option version of Q-learning. It is convenient to introduce new notation for the value of a state–option pair given that the option is Markov and executing upon arrival in the state: 

U ∗ 

> O

(s, o ) = (1 − β(s)) Q∗ 

> O

(s, o ) + β(s) max   

> o′∈O

Q∗ 

> O

(s, o ′ ),

Then we can write Bellman-like equations that relate Q∗ 

> O

(s, o ) to expected values of U ∗ 

> O

(s ′ , o ), where s ′ is the immediate successor to s after initiating Markov option o = 〈I, π, β〉 in s:

Q∗ 

> O

(s, o ) = ∑

> a∈As

π(s, a )E

> {

r + γU ∗ 

> O

(s ′ , o ) 

> ∣∣∣

s, a 

> }

= ∑

> a∈As

π(s, a )

> [

r as + ∑ 

> s′

p ass ′ U ∗ 

> O

(s ′ , o )

> ]

, (19) where r is the immediate reward upon arrival in s ′ . Now consider learning methods based on this Bellman equation. Suppose action at is taken in state s t to produce next state s t+1 

and reward rt+1 , and that at was selected in a way consistent with the Markov policy π

of an option o = 〈I, π, β〉. That is, suppose that at was selected according to the distri-bution π(s t , ·). Then the Bellman equation above suggests applying the o ff -policy one-step temporal-di ff erence update: 

Q(s t , o ) ← Q(s t , o ) + α

> [

(rt+1 + γU (s t+1 , o )) − Q(s t , o )

> ]

, (20) where 

U (s, o ) = (1 − β(s)) Q(s, o ) + β(s) max   

> o′∈O

Q(s, o ′ ).

The method we call one-step intra-option Q-learning applies this update rule to every option 

o consistent with every action taken, at . Note that the algorithm is potentially dependent on the order in which options are updated. 

Theorem 3 (Convergence of intra-option Q-learning) For any set of deterministic Markov options O, one-step intra-option Q-learning converges w.p.1 to the optimal Q-values, Q∗ 

> O

, for every option regardless of what options are executed during learning provided every primitive action gets executed in every state infinitely often. 

> 27 Sutton, Precup, & Singh

Proof: (Sketch) On experiencing the transition, ( s, a, r ′ , s ′ ), for every option o that picks action a in state s, intra-option Q-learning performs the following update: 

Q(s, o ) ← Q(s, o ) + α(s, o )[ r ′ + γU (s ′ , o ) − Q(s, o )] .

Let a be the action selection by deterministic Markov option o = 〈I, π, β〉. Our result follows directly from Theorem 1 of Jaakkola, Jordan, and Singh (1994) and the observation that the expected value of the update operator r ′ + γU (s ′ , o ) yields a contraction, proved below: 

|E{r ′ + γU (s ′ , o )} − Q∗ 

> O

(s, o )| = |r as + ∑ 

> s′

p ass ′ U (s ′ , o ) − Q∗ 

> O

(s, o )|

= |r as + ∑ 

> s′

p ass ′ U (s ′ , o ) − r as − ∑ 

> s′

p ass ′ U ∗ 

> O

(s ′ , o )|

≤ | ∑ 

> s′

p ass ′

> [

(1 − β(s ′ ))( Q(s ′ , o ) − Q∗ 

> O

(s ′ , o )) + β(s ′ )(max   

> o′∈O

Q(s ′ , o ′ ) − max   

> o′∈O

Q∗ 

> O

(s ′ , o ′ )

> ]

|

≤ ∑ 

> s′

p ass ′ max    

> s′′ ,o ′′

|Q(s ′′ , o ′′ ) − Q∗ 

> O

(s ′′ , o ′′ )|

≤ γ max    

> s′′ ,o ′′

|Q(s ′′ , o ′′ ) − Q∗ 

> O

(s ′′ , o ′′ )|

+

As an illustration, we applied this intra-option method to the rooms example, this time with the goal in the rightmost hallway, cell G1 in Figure 2. Actions were selected randomly with equal probability from the four primitives. The update (20) was applied first to the primitive options, then to any of the hallway options that were consistent with the action. The hallway options were updated in clockwise order, starting from any hallways that faced up from the current state. The rewards were the same as in the experiment in the previous section. Figure 10 shows learning curves demonstrating the e ff ective learning of option values without ever selecting the corresponding options. Intra-option versions of other reinforcement learning methods such as Sarsa, TD( λ), and eligibility-trace versions of Sarsa and Q-learning should be straightforward, although there has been no experience with them. The intra-option Bellman equation (19) could also be used for intra-option sample-based planning. 

9. Learning Options 

Perhaps the most important aspect of working between MDPs and SMDPs is that the options making up the SMDP actions may be changed. We have seen one way in which this can be done by changing their termination conditions. Perhaps more fundamental than that is changing their policies , which we consider briefly in this section. It is natural to think of options as achieving subgoals of some kind, and to adapt each option’s policy to better achieve its subgoal. For example, if the option is open-the-door , then it is natural 28 Between MDPs and Semi-MDPs        

> -4 -3 -2 -1 001000 1000 6000 2000 3000 4000 5000 6000

Episodes Episodes Option values for G 

Average value of greedy policy Learned value Learned value Upper hallway option Left hallway option True value True value -4 -3 -2 1 10 100 Value of Optimal Policy 

Figure 10: The learning of option values by intra-option methods without ever selecting the options. Experience was generated by selecting randomly among primitive actions, with the goal at G1 . Shown on the left is the value of the greedy policy, averaged over all states and 30 repetitions of the experiment, as compared with the value of the optimal policy. The right panel shows the learned option values from state G2 approaching their correct values. to adapt its policy over time to make it more e ff ective and e ffi cient in opening the door, which should make it more generally useful. Given subgoals for options, it is relatively straightforward to design o ff -policy intra-option learning methods to adapt the policies to better achieve those subgoals. For example, it may be possible to simply apply Q-learning to learn independently about each subgoal and option (as in Singh, 1992b; Thrun and Schwartz, 1995; Lin, 1993; Dorigo and Colombetti, 1994). On the other hand, it is not clear which of the several possible ways of formulating sub-goals to associate with options is the best, or even what the basis for evaluation should be. One of the important considerations is the extent to which models of options constructed to achieve one subgoal can be transferred to aid in planning the solution to another. We would like a long-lived learning agent to face a continuing series of subtasks that result in its being more and more capable. A full treatment of the transfer across subgoals probably involves developing the ideas of general hierarchical options (options that select other op-tions), which we have avoided in this paper. Nevertheless, in this section we briefly present a simple approach to associating subgoals with options. We do this without going to the full hierarchical case, that is, we continue to consider only options that select only primitive actions. The formalization of subgoals we present here is probably not the best, but it su ffi ces to illustrate some of the possibilities and problems that arise. A larger issue which we do not address is the source of the subgoals. We assume that the subgoals are given and focus on how options can be learned and tuned to achieve them, and on how learning toward di ff erent subgoals can aid each other. 29 Sutton, Precup, & Singh 

A simple way to formulate a subgoal is by assigning a subgoal value , g(s), to each state 

s in a subset of states G ⊆ S. These values indicate how desirable it is to terminate an option in each state in G. For example, to learn a hallway option in the rooms task, the target hallway might be assigned a subgoal value of +1 while the other hallway and all states outside the room might be assigned a subgoal value of 0. Let Og denote the set of options that terminate only and always in the states G in which g is defined (i.e., for which 

β(s) = 0 for s " ∈ G and β(s) = 1 for s ∈ G). Given a subgoal-value function g : G $ → 0 , one can define a new state-value function, denoted V og (s), for options o ∈ Og , as the expected value of the cumulative reward if option o is initiated in state s, plus the subgoal value g(s ′ )of the state s ′ in which it terminates. Similarly, we can define a new action-value function 

Qog (s, a ) = V ao g (s) for actions a ∈ A s and options o ∈ Og .Finally, we can define optimal value functions for any subgoal g: V ∗ 

> g

(s) = max o∈Og V og (s)and Q∗ 

> g

(s, a ) = max o∈Og Qog (s, a ). Finding an option that achieves these maximums (an op-timal option for the subgoal) is then a well defined subtask. For Markov options, this subtask has Bellman equations and methods for learning and planning just as in the orig-inal task. For example, the one-step tabular Q-learning method for updating an estimate 

Qg (s t , a t ) of Q∗ 

> g

(s t , a t ) is 

Qg (s t , a t ) ← Qg (s t , a t ) + α

> [

rt+1 + γ max  

> a

Qg (s t+1 , a t+1 ) − Qg (s t , a t )

> ]

,

if s t+1 " ∈ G, and 

Qg (s t , a t ) ← Qg (s t , a t ) + α [rt+1 + γg(s t+1 ) − Qg (s t , a t )] ,

if s t+1 ∈ G.As a simple example, we applied this method to learn the policies of the eight hallway options in the rooms example. Each option was assigned subgoal values of +1 for the target hallway and 0 for all states outside the option’s room, including the o ff -target hallway. The initial state was that in the upper left corner, actions were selected randomly with equal probability, and there was no goal state. The parameters were γ = 0 .9 and α = 0 .1. All rewards were zero. Figure 11 shows the learned action values Qg (s, a ) for each of the eight subgoals/options reliably approaching their ideal values, Q∗ 

> g

(s, a ). It is interesting to note that, in general, the policies learned to achieve subgoals will depend in detail on the precise values assigned by g to the subgoal states. For example, suppose nonzero expected rewards were introduced into the rooms task, distributed uni-formly between 0 and −1. Then a subgoal value of +10 (at the target hallway) results in an optimal policy that goes directly to the target hallway and away from the other hallway, as shown on the left in Figure 12, whereas a subgoal value of +1 may result in an optimal policy that goes only indirectly to the target hallway, as shown on the right in Figure 12. A roundabout path may be preferable in the latter case to avoid unusually large penalties. In the extreme it may even be optimal to head for the o ff -target hallway, or even to spend an infinite amount of time running into a corner and never reach any subgoal state. This is not a problem, but merely illustrates the flexibility of this subgoal formulation. For example, we may want to have two options for open-the-door , one of which opens the door only if it is easy to do so, for example, if is unlocked, and one which opens the door no matter 30 Between MDPs and Semi-MDPs 

Time steps RMS Error in hallway subtask values 00.1 0.2 0.3 0.4 0.5 0.6 0.7 0 20,000 40,000 Time Steps 60,000 upper hallway task true values learned values lower hallway task 80,000 100,000 Values of G

# for two tasks 00.1 0.2 0.3 0.4 0 20,000 40,000 60,000 80,000 100,000 

# [Qg(s,a) - Qg(s,a)]2*

Figure 11: Learning curves for the action values of each hallway option under random be-havior. Shown on the left is the error between Qg (s, a ) and Q∗ 

> g

(s, a ) averaged over s ∈ I, a ∈ A, and 30 repetitions of the whole experiment. The right panel shows the individual learned values for two options at one state (maximum over the learned action values) approaching their correct values.       

> g= 10 g= 1
> g= 0 g= 0

Figure 12: Two di ff erent optimal policies for options given two di ff erent subgoal values at the target hallway. A subgoal value of +10 (left) results in a more direct policy than a subgoal of +1. what, for example, by breaking it down if need be. If we had only the first option, then we would not be able to break down the door if need be, but if we had only the second, then we would not be able to choose to open the door without committing to breaking it down if it was locked, which would greatly diminish the option’s usefulness. The ability to learn and represent options for di ff erent intensities of subgoals, or di ff erent balances of outcome values, is an important flexibility. Subgoals, options, and models of options enable interesting new possibilities for rein-forcement learning agents. For example, we could present the agent with a series of tasks as subgoals, perhaps graded in di ffi culty. For each, the agent would be directed to find an option that achieves the subgoal and to learn a model of the option. Although the option 31 Sutton, Precup, & Singh 

> 10 !1?

Figure 13: A subgoal to which a hallway option does not transfer. The option for passing from the lower-left room through to the state with subgoal value 10 no longer works because of the state with subgoal value −1. The original model of this option is overpromising with respect to the subgoal. and model are constructed based on the task, note that they can be transferred to any other task. The option just says what to do; if behaving that way is a useful substep on another task, then it will help on that task. Similarly, the model just predicts the consequences of behaving that way; if that way of behaving is a useful substep on another task, then the model will help in planning to use that substep. As long as the model is accurate for its option it may be useful in planning the solution to another task. Singh (1992a,b,c) and Lin (1993) provide some simple examples of learning solutions to subtasks and then transferring them to help solve a new task. On the other hand, assuring that the models of options remain accurate across changes in tasks or subgoals is far from immediate. The most severe problem arises when the new subgoal prevents the successful completion of an option whose model has previously been learned. Figure 13 illustrates the problem in a rooms example. Here we assume the options and models have already been learned, then a new subgoal is considered that assigns a high value, 10 to a state in the lower-right room but a low value, −1, to a state that must be passed through to enter that room from the lower-left room. The −1 subgoal state makes it impossible to pass between the two rooms—the subgoal considers only options that terminate in its subgoal states—and the low value of this state makes it undesirable to try. Yet the prior model indicates that it is still possible to travel from the lower-left room “through” the −1 state to the hallway state and thereby to the 10-valued state. Thus, planning with this model will lead inevitably to a highly-valued but poor policy. Such problems can arise whenever the new subgoal involves states that which may be passed through when an option is executed. On the other hand, such problems can be detected and prevented in a number of ways. One idea is keep track of which states an option passes through and invalidate options and 32 Between MDPs and Semi-MDPs 

models that pass through subgoal states. Another idea is to alter the subgoal formulation such that subgoal states can be passed through: stopping in them and collecting the subgoal value is optional rather than required. Finally, note that we do not require models to be accurate, just non-overpromising —that is, they do not have to predict the correct outcome, just an outcome that is less than or equal to, in expected value, the correct outcome. This finesse may enable important special cases to be handled simply. For example, any new subgoal involving states G that all have the same subgoal value, e.g., any singleton G, can probably be safely transferred to. The sort of problem shown in Figure 13 can never occur in such cases. 

10. Conclusion 

Representing knowledge flexibly at multiple levels of temporal abstraction has the potential to greatly speed planning and learning on large problems. Options and their models o ff er a new set of tools for realizing this potential. They o ff er new capabilities in each of three critical areas that we identified at the beginning of this paper. They are clear enough to be interpreted entirely mechanically, as we have shown by exhibiting simple procedures for executing options, learning models of them, testing the models against real events, modifying options, and creating new options given subgoals. They are more expressive 

than previous methods based on MDPs and SMDPs in that they permit multiple levels of temporal abstraction to simultaneously apply to the same system. Finally, they are explicitly designed to be suitable for planning using methods based on Bellman equations. Compared to conventional MDP and SMDP formulations, options provide a substantial increase in expressiveness with no loss of clarity or suitability for planning. Compared with classical AI representations, they are a substantial increase in clarity and in some aspects of expressiveness. In particular, they apply to stochastic environments, closed-loop policies, and to a more general class of goals. The foundation for the theory of options is provided by the existing theory of Semi-MDPs. The fact that each set of options defines an SMDP provides a rich set of planning and learning methods, convergence theory, and an immediate, natural, and general way of analyzing mixtures of actions at di ff erent time scales. This theory o ff ers a lot, but still the most interesting cases are beyond it because they involve interrupting, constructing, or otherwise decomposing options into their constituent parts. It is the intermediate ground between MDPs and SMDPs that seems richest in possibilities for new algorithms and results. In this paper we have broken this ground and touched on many of the issues, but there is far more left to be done. Key issues such as transfer between subtasks, the source of subgoals, and integration with state abstraction remain open and unclear. The connection between options and SMDPs provides only a foundation for addressing these and other issues. Finally, although this paper has emphasized temporally extended action , it is interesting to note that there may be implications for temporally extended perception as well. It is now common to recognize that action and perception are intimately related. To see the objects in a room is not so much to label or locate them as it is to know what opportunities they aff ord for action: a door to open, a chair to sit on, a book to read, a person to talk to. If the 33 Sutton, Precup, & Singh 

temporally extended actions are modeled as options, then perhaps the model of the option corresponds well to these perceptions. Consider a robot learning to recognize its battery charger. The most useful concept for it is the set of states from which it can successfully dock with the charger. This is exactly the concept that would be produced by the model of a docking option. These kinds of action-oriented concepts are appealing because they can be tested and learned by the robot without external supervision, as we have shown in this paper. 

Acknowledgements 

The authors gratefully acknowledge the substantial help they have received from the col-leagues who have shared their related results and ideas with us over the long period during which this paper was in preparation, especially Amy McGovern, Andy Barto, Ron Parr, Tom Dietterich, Andrew Fagg, and Manfred Huber. We also thank Leo Zelevinsky, Zsolt Kalm´ ar, Csaba Szepesv´ ari, Andr´ as L¨ orincz, Paul Cohen, Robbie Moll, Mance Harmon, Sascha En-gelbrecht, and Ted Perkins. This work was supported by NSF grant ECS-9511805 and grant AFOSR-F49620-96-1-0254, both to Andrew Barto and Richard Sutton. Doina Precup also acknowledges the support of the Fulbright foundation. Satinder Singh was supported by NSF grant IIS-9711753. 

References 

Araujo, E.G., Grupen, R.A. (1996). Learning control composition in a complex environ-ment. Proceedings of the Fourth International Conference on Simulation of Adaptive Behavior , pp. 333-342. Asada, M., Noda, S., Tawaratsumida, S., Hosada, K. (1996). Purposive behavior acquisition for a real robot by vision-based reinforcement learning. Machine Learning 23 :279–303. Barto, A.G., Bradtke, S.J., Singh, S.P. (1995). Learning to act using real-time dynamic programming. Artificial Intelligence 72 :81–138. Boutilier, C., Brafman, R.I., Geib, C. (1997). Prioritized goal Decomposition of Markov decision processes: Toward a synthesis of classical and decision theoretic planning. 

Proceedings of the Fifteenth International Joint Conference on Artificial Intelligence ,pp. 1165–1162. Bradtke, S.J., and Du ff , M.O. (1995). Reinforcement learning methods for continuous-time Markov decision problems. Advances in Neural Information Processing Systems 8:393–400. MIT Press, Cambridge, MA. Brafman, R.I., Moshe, T. (1997). Modeling agents as qualitative decision makers. Artificial Intelligence 94 (1):217-268. Brockett, R.W. (1993). Hybrid models for motion control systems. In Essays in Control: Perspectives in the Theory and and its Applications , pp. 29–53. Birkh¨ auser, Boston. 34 Between MDPs and Semi-MDPs 

Brooks, R. (1986). A robust layered control system for a mobile robot. IEEE journal of Robotics and Automation , 14–23. Chrisman, L. (1994). Reasoning about probabilistic actions at multiple levels of granularity, 

AAAI Spring Symposium: Decision-Theoretic Planning , Stanford University. Colombetti, M., Dorigo, M., Borghi, G. (1996). Behavior analysis and training: A methodol-ogy for behavior engineering. IEEE Transactions on Systems, Man, and Cybernetics-Part B 26 (3):365–380 Crites, R.H., and Barto, A.G. (1996). Improving elevator performance using reinforcement learning. Advances in Neural Information Processing Systems 9 :1017–1023. MIT Press, Cambridge, MA. Dayan, P. (1993). Improving generalization for temporal di ff erence learning: The successor representation. Neural Computation 5 :613–624. Dayan, P., Hinton, G.E. (1993). Feudal reinforcement learning. Advances in Neural Infor-mation Processing Systems 5 :271–278. San Mateo, CA: Morgan Kaufmann. de Kleer, J., Brown, J.S. (1984). A qualitative physics based on confluences. Artificial Intelligence 24 (1–3):7–83. Dean, T., Kaelbling, L.P., Kirman, J., Nicholson, A. (1995). Planning under time con-straints in stochastic domains. Artificial Intelligence 76 (1–2): 35–74. Dean, T., Lin, S.-H. (1995). Decomposition techniques for planning in stochastic domains. 

Proceedings of the Fourteenth International Joint Conference on Artificial Intelli-gence , pp. 1121–1127. Morgan Kaufmann. See also Technical Report CS-95-10, Brown University, Department of Computer Science, 1995. Dejong, G.F. (1994). Learning to plan in continuous domains. Artificial Intelligence 65 :71– 141. Dietterich, T.G. (1997). Hierarchical reinforcement learning with the MAXQ value function decomposition. Technical Report, Department of Computer Science, Oregon State University. Dorigo, M., Colombetti, M. (1994). Robot shaping: Developing autonomous agents through learning. Artificial Intelligence 71 :321–370. Drescher, G.L. (1991). Made Up Minds: A Constructivist Approach to Artificial Intelli-gence . MIT Press. Drummond, C. (1998). Composing functions to speed up reinforcement learning in a chang-ing world. Proceedings of the Tenth European Conference on Machine Learning .Springer-Verlag. Fikes, R.E., Hart, P.E., Nilsson, N.J. (1972). Learning and executing generalized robot plans. Artificial Intelligence 3 :251–288. Ge ff ner, H., Bonet, B. (in preparation). High-level planning and control with incomplete information using POMDPs. 35 Sutton, Precup, & Singh 

Grossman, R.L., Nerode, A., Ravn, A.P., Rischel, H. (1993). Hybrid Systems . Springer-Verlag, New York. Haigh, K.Z., Shewchuk, J., Veloso, M.M. (1997). Exploring geometry in analogical route planning. Journal of Experimental and Theoretical Artificial Intelligence 9 :509–541. Hansen, E. (1994). Cost-e ff ective sensing during plan execution. Proc. AAAI-94 , pp. 1029– 1035. Hauskrecht, M., Meuleau, N., Boutilier, C., Kaelbling, L.P., Dean, T. (in preparation). Hierarchical solution of Markov decision processes using macro-actions. Huber, M., Grupen, R.A. (1997). A feedback control structure for on-line learning tasks. 

Robotics and Autonomous Systems 22 (3-4):303-315. Iba, G.A. (1989). A heuristic approach to the discovery of macro-operators. Machine Learning 3 :285–317. Jaakkola, T., Jordan, M.I., and Singh, S.P. (1994). On the convergence of stochastic itera-tive dynamic programming algorithms. Neural Computation 6 (6):1185–1201. Kaelbling, L.P. (1993). Hierarchical learning in stochastic domains: Preliminary results. 

Proc. of the Tenth Int. Conf. on Machine Learning , pp. 167–173, Morgan Kaufmann. Kalm´ ar, Z., Szepesv´ ari, C., L¨ orincz, A. (1997). Module based reinforcement learning for a real robot. Proceedings of the Sixth European Workshop on Learning Robots ,pp. 22–32. Kalm´ ar, Z., Szepesv´ ari, C., L¨ orincz, A. (in preparation). Module based reinforcement learning: Experiments with a real robot. Korf, R.E. (1985). Learning to Solve Problems by Searching for Macro-Operators . Boston: Pitman Publishers. Korf, R.E. (1987). Planning as search: A quantitative approach. Artificial Intelligence 33 :65–88. Koza, J.R., Rice, J.P. (1992). Automatic programming of robots using genetic program-ming. Proceedings of the Tenth National Conference on Artificial Intelligence , pp. 194– 201. Kuipers, B.J. (1979). Commonsense knowledge of space: Learning from experience. Proc. IJCAI-79 , pp. 499–501. Laird, J.E., Rosenbloom, P.S., Newell, A. (1986). Chunking in SOAR: The anatomy of a general learning mechanism. Machine Learning 1 :11–46. Levinson, R., Fuchs, G. (1994). A pattern-weight formulation of search knowledge. Tech-nical Report UCSC-CRL-94-10, University of California at Santa Cruz. Lin, L.-J. (1993). Reinforcement Learning for Robots Using Neural Networks . PhD thesis, Carnegie Mellon University. Technical Report CMU-CS-93-103. 36 Between MDPs and Semi-MDPs 

Maes, P. (1991). A bottom-up mechanism for behavior selection in an artificial creature. 

Proceedings of the First International Conference on Simulation of Adaptive Behavior .MIT Press. Maes, P., Brooks, R. (1990). Learning to coordinate behaviors. Proceedings of AAAI-90 ,pp. 796–802. Mahadevan, S., Connell, J. (1992). Automatic programming of behavior-based robots using reinforcement learning. Artificial Intelligence 55 (2-3):311–365. Mahadevan, S., Marchalleck, N., Das, T., Gosavi, A. (1997). Self-improving factory simu-lation using continuous-time average-reward reinforcement learning. Proceedings of the 14th International Conference on Machine Learning .Marbach, P., Mihatsch, O., Schulte, M., Tsitsiklis, J.N. (1998). Reinforcement learning for call admission control in routing in integrated service networks. Advances in Neural Information Processing Systems 10 . San Mateo: Morgan Kaufmann. Mataric, M.J. (1997). Behavior-based control: Examples from navigation, learning, and group behavior. Journal of Experimental and Theoretical Artificial Intelligence 9 (2– 3). McGovern, A., Sutton, R.S., Fagg, A.H. (1997). Roles of macro-actions in accelerating reinforcement learning. Proceedings of the 1997 Grace Hopper Celebration of Women in Computing .McGovern, A., Sutton, R.S., (in prep.). Roles of temporally extended actions in accelerating reinforcement learning. Meuleau, N., Hauskrecht, M., Kim, K.-E., Peshkin, L., Kaelbling, L.P., Dean, T., Boutilier, C. (in preparation). Solving very large weakly coupled Markov decision processes. Mill´ an, J. del R. (1994). Learning reactive sequences from basic reflexes. Proceedings of the Third International Conference on Simulation of Adaptive Behavior , pp. 266–274. Minton, S. (1988). Learning Search Control Knowledge: An Explanation-based Approach .Kluwer Academic. Moore, A.W. (1994). The parti-game algorithm for variable resolution reinforcement learn-ing in multidimensional spaces, Advances in Neural Information Processing Systems 7:711–718, MIT Press, Cambridge, MA. Newell, A., Simon, H.A. (1972). Human Problem Solving . Prentice-Hall, Englewood Cli ff s, NJ. Nie, J., and Haykin, S. (to appear). A Q-learning based dynamic channel assignment technique for mobile communication systems. IEEE Transactions on Vehicular Tech-nology .Nilsson, N.J. (1973). Hierarchical robot planning and execution system. SRI AI Center Technical Note 76, SRI International, Inc., Menlo Park, CA. 37 Sutton, Precup, & Singh 

Nilsson, N. (1994). Teleo-reactive programs for agent control. Journal of Artificial Intelli-gence Research, 1 :139–158. Parr, R., Russell, S. (1998). Reinforcement learning with hierarchies of machines. Advances in Neural Information Processing Systems 11 . MIT Press, Cambridge, MA. Parr, R. (in preparation). Hierarchical control and learning for Markov decision processes, chapter 3. Precup, D., Sutton, R.S. (1997). Multi-time models for reinforcement learning. Proceedings of the ICML’97 Workshop on Modelling in Reinforcement Learning .Precup, D., Sutton, R.S. (1998). Multi-time models for temporally abstract planning. 

Advances in Neural Information Processing Systems 11 . MIT Press, Cambridge, MA. Precup, D., Sutton, R.S., Singh, S.P. (1997). Planning with closed-loop macro actions. 

Working notes of the 1997 AAAI Fall Symposium on Model-directed Autonomous Systems .Precup, D., Sutton, R.S., Singh, S.P. (1998). Theoretical results on reinforcement learning with temporally abstract options. Proceedings of the Tenth European Conference on Machine Learning . Springer-Verlag. Puterman, M. L. (1994). Markov Decision Problems . Wiley, New York. Rosenstein, M.T., Cohen, P.R. (1998). Concepts from time series. Proceedings of the Fifteenth National Conference on Artificial Intelligence .Ring, M. (1991). Incremental development of complex behaviors through automatic con-struction of sensory-motor hierarchies. Proceedings of the Eighth International Con-ference on Machine Learning, pp. 343–347, Morgan Kaufmann. Rudy, D., Kibler, D. (1992). Learning episodes for optimization. Proceedings of the Ninth International Conference on Machine Learning , Morgan Kaufmann. Sacerdoti, E.D. (1974). Planning in a hierarchy of abstraction spaces. Artificial Intelligence 5:115–135. Sastry, S. (1997). Algorithms for design of hybrid systems. Proceedings of the International Conference of Information Sciences .Say, A.C.C., Selahattin, K. (1996). Qualitative system identification: Deriving structure from behavior. Artificial Intelligence 83 (1):75–141. Schmidhuber, J. (1991). Neural Sequence Chunkers. Technische Universitat Munchen TR FKI-148-91. Simmons, R., Koenig, S. (1995). Probabilistic robot navigation in partially observable envi-ronments. Proceedings of the Fourteenth International Joint Conference on Artificial Intelligence , pp. 1080–1087. Morgan Kaufmann. 38 Between MDPs and Semi-MDPs 

Singh, S.P. (1992a). Reinforcement learning with a hierarchy of abstract models. Pro-ceedings of the Tenth National Conference on Artificial Intelligence , pp. 202–207. MIT/AAAI Press. Singh, S.P. (1992b). Scaling reinforcement learning by learning variable temporal resolution models. Proceedings of the Ninth International Conference on Machine Learning ,pp. 406–415, Morgan Kaufmann. Singh, S.P. (1992c). Transfer of learning by composing solutions of elemental sequential tasks. Machine Learning 8 (3/4):323–340. Singh, S.P. (1992d). The e ffi cient learning of multiple task sequences. In Advances in Neural Information Processing Systems 4 :251–258, Morgan Kaufmann. Singh S.P., Barto A.G., Grupen R.A., Connolly C.I. (1994). Robust reinforcement learning in motion planning. Advances in Neural Information Processing Systems 6 :655–662, Morgan Kaufmann. Singh, S.P., Bertsekas, D. (1997). Reinforcement learning for dynamic channel allocation in cellular telephone systems. Advances in Neural Information Processing Systems 9:974–980. MIT Press. Sutton, R.S. (1995). TD models: Modeling the world at a mixture of time scales. Pro-ceedings of the Twelfth International Conference on Machine Learning , pp. 531–539, Morgan Kaufmann. Sutton, R.S., Barto, A.G. (1998). Reinforcement Learning: An Introduction . MIT Press, Cambridge, MA. Sutton, R.S., Pinette, B. (1985). The learning of world models by connectionist networks. 

Proc. of the Seventh Annual Conf. of the Cognitive Science Society , pp. 54-64. Tenenberg, J. Karlsson, J., Whitehead, S. (1992). Learning via task decomposition. Proc. Second Int. Conf. on the Simulation of Adaptive Behavior. MIT Press. Tesauro, G.J. (1995). Temporal di ff erence learning and TD-Gammon. Communications of the ACM 38 :58–68. Thrun, T., Schwartz, A. (1995). Finding structure in reinforcement learning. Advances in Neural Information Processing Systems 7 . San Mateo: Morgan Kaufmann. T´ oth, G.J., Kov´ acs, S., L¨ orincz, A. (1995). Genetic algorithm with alphabet optimization. 

Biological Cybernetics 73 :61–68. Uchibe, M., Asada, M., Hosada, K. (1996). Behavior coordination for a mobile robot using modular reinforcement learning. Proceedings of IEEE/RSJ International Conference on Intelligent Robots and Systems , pp. 1329–1336. Watkins, C.J.C.H. (1989). Learning with Delayed Rewards . PhD thesis, Cambridge Uni-versity. Wiering, M., Schmidhuber, J. (1997). HQ-learning. Adaptive Behavior 6 (2). 39 Sutton, Precup, & Singh 

Wixson, L.E. (1991). Scaling reinforcement learning techniques via modularity, Proc. Eighth Int. Conf. on Machine Learning, pp. 368–372, Morgan Kaufmann. 40