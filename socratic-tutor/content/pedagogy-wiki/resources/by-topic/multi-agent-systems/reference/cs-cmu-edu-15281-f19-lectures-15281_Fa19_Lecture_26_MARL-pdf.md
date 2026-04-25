# Source: https://www.cs.cmu.edu/~./15281-f19/lectures/15281_Fa19_Lecture_26_MARL.pdf
# Title: CMU 15-281 Lecture 26: Multi-Agent Reinforcement Learning / Markov Games (Michael L. Littman)
# Fetched via: jina
# Date: 2026-04-09

Title: PowerPoint Presentation



Number of Pages: 52

Warm up  

> 

Pick an agent among {Pacman, Blue Ghost, Red 

Ghost}. Design an algorithm to control your agent. 

Assume they can see each others’ location but can’t 

talk. Assume they move simultaneously in each step. 

> 1

Announcement  

> 

Assignments  

> 

HW12 (written) due 12/4 Wed, 10 pm  

> 

Final exam  

> 

12/12 Thu, 1pm -4pm  

> 

Piazza post for in -class questions 

Due 12/6 Fri, 10 pm 

> 2

AI: Representation and Problem Solving 

Multi -Agent Reinforcement Learning 

Instructors: Fei Fang & Pat Virtue 

Slide credits: CMU AI and http://ai.berkeley.edu Learning objectives  

> 

Compare single -agent RL with multi -agent RL  

> 

Describe the definition of Markov games  

> 

Describe and implement  

> 

Minimax -Q algorithm  

> 

Fictitious play  

> 

Explain at a high level how fictitious play and double -oracle 

framework can be combined with single -agent RL algorithms 

for multi -agent RL 

> 4

Single -Agent → Multi -Agent  

> 

Many real -world scenarios have more than one agent!  

> Autonomous driving
> 5

Single -Agent → Multi -Agent  

> 

Many real -world scenarios have more than one agent!  

> 

Autonomous driving  

> 

Humanitarian Assistance / Disaster Response 

> 6

Single -Agent → Multi -Agent  

> 

Many real -world scenarios have more than one agent!  

> 

Autonomous driving  

> 

Humanitarian Assistance / Disaster Response  

> 

Entertainment 

> 7

Single -Agent → Multi -Agent  

> 

Many real -world scenarios have more than one agent!  

> 

Autonomous driving  

> 

Humanitarian Assistance / Disaster Response  

> 

Entertainment  

> 

Infrastructure security / green security / cyber security 

> 8

Single -Agent → Multi -Agent  

> 

Many real -world scenarios have more than one agent!  

> 

Autonomous driving  

> 

Humanitarian Assistance / Disaster Response  

> 

Entertainment  

> 

Infrastructure security / green security / cyber security  

> 

Ridesharing 

> 9

Recall: Normal -Form/Extensive -Form games  

> 

Games are specified by  

> 

Set of players  

> 

Set of actions for each player (at each decision point)  

> 

Payoffs for all possible game outcomes  

> 

(Possibly imperfect) information each player has about the 

other player's moves when they make a decision  

> 

Solution concepts  

> 

Nash equilibrium, dominant strategy equilibrium, 

Minimax/ Maximin strategy, Stackelberg equilibrium  

> 

Approaches to solve the game  

> 

Iterative removal, Solving linear systems, Linear programming 

> 10

Single -Agent → Multi -Agent  

> 

Can we use these approaches to previous problems?  

> 

Limitations of classic approaches in game theory  

> 

Scalability: Can hardly handle complex problems  

> 

Need to specify payoff for all outcomes  

> 

Often need domain knowledge for improvement (e.g., 

abstraction)      

> 11
> Football Concert
> Football 2, 10, 0
> Concert 0, 01, 2
> Berry
> Alex

Recall: Reinforcement learning  

> 

Assume a Markov decision process (MDP):  

> 

A set of states s  S 

> 

A set of actions (per state) A  

> 

A model T( s,a,s ’)  

> 

A reward function R( s,a,s ’)  

> 

Looking for a policy (s) without knowing T or R  

> 

Learn the policy through experience in the environment 

> 12

Single -Agent → Multi -Agent  

> 

Can we apply single -agent RL to previous problems? How?  

> 

Simultaneously independent single -agent RL, i.e., let every 

agent 𝑖 use Q -learning to learn 𝑄 (𝑠 , 𝑎 𝑖 ) at the same time  

> 

Effective only in some problems (limited agent interactions)  

> 

Limitations of single -agent RL in multi -agent setting  

> 

Instability and adapatability : Agents are co -evolving 

> 13

If treat other agents as part of 

environment, this environment 

is changing over time! Single -Agent → Multi -Agent  

> 

Multi -Agent Reinforcement Learning  

> 

Let the agents learn through interacting with the 

environment and with each other  

> 

Simplest approach: Simultaneously independent single -agent 

RL (suffer from instability and adapatability ) 

> 

Need better approaches 

> 14

Multi -Agent Reinforcement Learning  

> 

Assume a Markov game:  

> 

A set of 𝑁 agents  

> 

A set of states 𝑆  

> 

Describing the possible configurations for all agents  

> 

A set of actions for each agent 𝐴 1, … , 𝐴 𝑁  

> 

A transition function 𝑇 𝑠 , 𝑎 1, 𝑎 2, … , 𝑎 𝑛 , 𝑠 ′ 

> 

Probability of arriving at state 𝑠′ after all the agents taking 

actions 𝑎 1, 𝑎 2, … , 𝑎 𝑛 respectively  

> 

A reward function for each agent 𝑅 𝑖 (𝑠 , 𝑎 1, 𝑎 2, … , 𝑎 𝑛 )

> 15

Piazza Poll 1  

> 

You know that the state at time 𝑡 is 𝑠 𝑡 and the 

actions taken by the players at time 𝑡 is 𝑎 𝑡 ,1, … , 𝑎 𝑡 ,𝑁 .

The reward for agent 𝑖 at time 𝑡 + 1 is dependent on 

which factors?  

> 

A: 𝑠 𝑡  

> 

B: 𝑎 𝑡 ,𝑖  

> 

C: 𝑎 𝑡 ,−𝑖 ≜ 𝑎 𝑡 ,1, … , 𝑎 𝑡 ,𝑖 −1, 𝑎 𝑡 ,𝑖 +1, … , 𝑎 𝑡 ,𝑁  

> 

D: None  

> 

E: I don’t know 

> 16

Multi -Agent Reinforcement Learning  

> 

Assume a Markov game  

> 

Looking for a set of policies {𝜋 𝑖 }, one for each agent, 

without knowing 𝑇 , 𝑅 𝑖 , ∀𝑖         

> 𝜋 𝑖 𝑠 ,𝑎 is the probability of choosing action 𝑎 at state 𝑠
> 

Each agent’s total expected return is 𝑡 𝛾 𝑡 𝑟 𝑖 𝑡 where 

𝛾 is the discount factor  

> 

Learn the policies through experience in the 

environment and interact with each other 

> 17

Multi -Agent Reinforcement Learning  

> 

Descriptive  

> 

What would happen if agents learn in a certain way?  

> 

Propose a model of learning that mimics learning in real life  

> 

Analyze the emergent behavior with this learning model 

(expecting them to agree with the behavior in real life)  

> 

Identify interesting properties of the learning model 

> 18

Multi -Agent Reinforcement Learning  

> 

Prescriptive (our main focus today)  

> 

How agents should learn?  

> 

Not necessary to show a match with real -world phenomena  

> 

Design a learning algorithm to get a “good” policy 

(e.g., high total reward against a broad class of other agents) 

> 19

DeepMind's AlphaStar beats 99.8% of human Recall: Value Iteration and Bellman Equation  

> 20
> 

Value iteration  

> 

With reward function 𝑅 (𝑠 , 𝑎 ) 

> 

When converges (Bellman Equation) 

𝑉 𝑘 +1 𝑠 = max  

> 𝑎 𝑠′

𝑃 𝑠 ′ 𝑠 , 𝑎 𝑅 𝑠 , 𝑎 , 𝑠 ′ + 𝛾 𝑉 𝑘 𝑠 ′ , ∀𝑠 

𝑉 𝑘 +1 𝑠 = max  

> 𝑎

𝑅 𝑠 , 𝑎 + 𝛾 

> 𝑠′

𝑃 𝑠 ′ 𝑠 , 𝑎 𝑉 𝑘 𝑠 ′ , ∀𝑠 

𝑉 ∗ 𝑠 = max  

> 𝑎

𝑄 ∗(𝑠 , 𝑎 ) , ∀𝑠 

𝑄 ∗ 𝑠 , 𝑎 = 𝑅 𝑠 , 𝑎 + 𝛾 

> 𝑠 ′

𝑃 𝑠 ′ 𝑠 , 𝑎 𝑉 ∗ 𝑠 ′ , ∀𝑎 , 𝑠 Value Iteration in Markov Games  

> 

In two -player zero -sum Markov game  

> 

Let 𝑉 ∗(𝑠 ) be state value for player 1 ( −𝑉 ∗(𝑠 ) for player 2)  

> 

Let 𝑄 ∗(𝑠 , 𝑎 1, 𝑎 2) be action -state value for player 1 when 

player 1 chooses 𝑎 1 and player 2 chooses 𝑎 2 in state 𝑠 

> 21

𝑄 ∗ 𝑠 , 𝑎 1, 𝑎 2 =

𝑉 ∗ 𝑠 =

𝑉 ∗ 𝑠 = max  

> 𝑎

𝑄 ∗(𝑠 , 𝑎 ) , ∀𝑠 

𝑄 ∗ 𝑠 , 𝑎 = 𝑅 𝑠 , 𝑎 + 𝛾 

> 𝑠 ′

𝑃 𝑠 ′ 𝑠 , 𝑎 𝑉 ∗ 𝑠 ′ , ∀𝑎 , 𝑠 Minimax -Q Algorithm  

> 

Value iteration requires knowing 𝑇 , 𝑅 𝑖  

> 

Minimax -Q [Littman94]  

> 

Extension of Q -learning  

> 

For two -player zero -sum Markov games  

> 

Provably converges to Nash equilibria in self play 

> 23

A learning agent learns through interacting 

with another learning agent using the same 

learning algorithm Minimax -Q Algorithm 

Initialize 𝑄 𝑠 , 𝑎 1, 𝑎 2 ← 1, 𝑉 𝑠 ← 1, 𝜋 1 𝑠 , 𝑎 1 ← 1

> |𝐴 1|

, 𝛼 ← 1

Take actions : At state 𝑠 , w ith prob. 𝜖 choose a random action, and 

with prob. 1 − 𝜖 choose action ac cording to 𝜋 1 𝑠 , 𝑎 

Learn : after receiving 𝑟 1 for moving from 𝑠 to 𝑠 ′ via 𝑎 1, 𝑎 2

Update 𝛼 

> 24

𝑉 𝑠 ← min  

> 𝑎 2∈𝐴 2𝑎 1∈𝐴 1

𝜋 1 𝑠 , 𝑎 1 𝑄 𝑠 , 𝑎 1, 𝑎 2

𝑄 𝑠 , 𝑎 1, 𝑎 2 ← 1 − 𝛼 𝑄 𝑠 , 𝑎 1, 𝑎 2 + 𝛼 𝑟 1 + 𝛾𝑉 𝑠 ′

𝜋 1 𝑠 ,⋅ ← argmax  

> 𝜋 1
> ′(𝑠 ,⋅)∈Δ(𝐴 1)

min  

> 𝑎 2∈𝐴 2𝑎 1∈𝐴 1

𝜋 1 

> ′

𝑠 , 𝑎 1 𝑄 𝑠 , 𝑎 1, 𝑎 2Minimax -Q Algorithm 

 How to solve the maximin problem? 

> 26

Linear Programming:  max 

𝜋 1 

> ′

𝑠 ,⋅ ,𝑣 𝑣 

Get optimal solution 𝜋 1

′∗ 𝑠 ,⋅ , 𝑣 ∗, update 𝜋 1 𝑠 ,⋅ ← 𝜋 1

′∗ 𝑠 ,⋅ , 𝑉 𝑠 ← 𝑣 ∗

𝑉 𝑠 ← min  

> 𝑎 2∈𝐴 2𝑎 1∈𝐴 1

𝜋 1 𝑠 , 𝑎 1 𝑄 𝑠 , 𝑎 1, 𝑎 2

𝜋 1 𝑠 ,⋅ ← argmax  

> 𝜋 1
> ′(𝑠 ,⋅)∈Δ(𝐴 1)

min  

> 𝑎 2∈𝐴 2𝑎 1∈𝐴 1

𝜋 1 

> ′

𝑠 , 𝑎 1 𝑄 𝑠 , 𝑎 1, 𝑎 2Minimax -Q Algorithm  

> 

How does player 2 chooses action 𝑎 2? 

> 

If player 2 is also using the minimax -Q algorithm  

> 

Self -play  

> 

Proved to converge to NE  

> 

If player 2 chooses actions uniformly randomly, the algorithm 

still leads to a good policy empirically in some games 

> 28

Minimax -Q for Matching Pennies  

> 

A simple Markov game: Repeated Matching Pennies  

> 

Let state to be dummy: Player’s strategy is not 

dependent on past actions. Just play a mixed strategy 

as in the one -shot game  

> 

Discount factor 𝛾 = 0.9     

> 29
> Heads Tails
> Heads 1, -1-1, 1
> Tails -1, 11, -1
> Player 2
> Player  1

Minimax -Q for Matching Pennies 

Simplified version for this games with only one state 

Initialize 𝑄 𝑎 1, 𝑎 2 ← 1, 𝑉 ← 1, 𝜋 1 𝑎 1 ← 0.5, 𝛼 ← 1

Take actions : With prob. 𝜖 choose a random action, and with 

prob. 1 − 𝜖 choose action ac cording to 𝜋 1 𝑎 

Learn : after receiving 𝑟 1 with actions 𝑎 1, 𝑎 2

> 30

𝑄 𝑎 1, 𝑎 2 ← 1 − 𝛼 𝑄 𝑎 1, 𝑎 2 + 𝛼 𝑟 1 + 𝛾𝑉 

𝜋 1 ⋅ ← argmax  

> 𝜋 1
> ′(⋅)∈Δ2

min  

> 𝑎 2∈𝐴 2𝑎 1∈𝐴 1

𝜋 1 

> ′

𝑎 1 𝑄 𝑎 1, 𝑎 2

𝑉 ← min  

> 𝑎 2∈𝐴 2𝑎 1∈𝐴 1

𝜋 1 𝑎 1 𝑄 𝑎 1, 𝑎 2     

> Heads Tails
> Heads 1, -1-1, 1
> Tails -1, 11, -1

Update 𝛼 = 1/ #times 𝑎 1, 𝑎 2 visited Minimax -Q for Matching Pennies 

31 

Heads  Tails 

Heads  1, -1 -1, 1

Tails  -1, 1 1, -1

𝑄 𝑎 1, 𝑎 2 ← 1 − 𝛼 𝑄 𝑎 1, 𝑎 2 + 𝛼 𝑟 1 + 𝛾𝑉 

max    

> 𝜋 1
> ′𝑠 ,⋅,𝑣

𝑣 

𝑣 ≤

> 𝑎 1∈𝐴 1

𝜋 1 

> ′

𝑠 , 𝑎 1 𝑄 𝑠 , 𝑎 1, 𝑎 2 , ∀𝑎 2

> 𝑎 1∈𝐴 1

𝜋 1 

> ′

𝑠 , 𝑎 1 = 1

𝜋 1 

> ′

𝑠 , 𝑎 1 ≥ 0, ∀𝑎 1Piazza Poll 2  

> 

If the actions are (H,T) in round 1 with a reward of -1

to player 1, what would be the updated value of 

𝑄 (𝐻 , 𝑇 ) with 𝛾 = 0.9? 

> 

A: 0.9  

> 

B: 0.1  

> 

C: -0.1  

> 

D: 1.9  

> 

E: I don’t know 

> 33

Minimax -Q for Matching Pennies 

> 34

Heads  Tails 

Heads  1, -1 -1, 1

Tails  -1, 1 1, -1How to Evaluate a MARL algorithm (prescriptive)?  

> 

Brainstorming: how to evaluate minimiax -Q?  

> 

Recall: Design a learning algorithm 𝐴𝑙𝑔 to get a “good” 

policy (e.g., high total expected return against a broad class 

of other agents) 

> 35

How to Evaluate a MARL algorithm (prescriptive)?  

> 

Training: Find a policy for agent 1 through minimax -Q 

> 

Let an agent 1 learn with minimax -Q while agent 2 is  

> 

Also learning with minimax -Q (Self -play)  

> 

Using a heuristic strategy, e.g., random  

> 

Learning using a different learning algorithm, e.g., vanilla Q -

learning or a variant of minimax -Q 

> 

Exemplary resulting policy:  

> 

𝜋 1

> 𝑀𝑀

(Minimax -Q-trained -against -selfplay ) 

> 

𝜋 1

> 𝑀 𝑅

(Minimax -Q-trained -against -Random)  

> 

𝜋 1

> 𝑀 𝑄

(Minimax -Q-trained -against -Q) 

> 36

Co -evolving! How to Evaluate a MARL algorithm (prescriptive)?  

> 

Testing: Fix agent 1’s strategy 𝜋 1, no more change  

> 

Test again an agent 2’s strategy 𝜋 2, which can be  

> 

A heuristic strategy, e.g., random  

> 

Trained using a different learning algorithm, e.g., vanilla Q -

learning or a variant of minimax -Q 

> 

Need to specify agent 1’s behavior during training agent 2 

(random? Minimax -Q? Q -learning?), can be different from 

𝜋 1 or even co -evolving  

> 

Best response to player 1’s strategy 𝜋 1 

> 

Worst case for player 1  

> 

Fix 𝜋 1, treat player 1 as part of the environment, find the 

optimal policy for player 2 through single -agent RL 

> 37

How to Evaluate a MARL algorithm (prescriptive)?  

> 

Testing: Fix agent 1’s strategy 𝜋 1, no more change  

> 

Test again an agent 2’s strategy 𝜋 2, which can be  

> 

Exemplary policy for agent 2:  

> 

𝜋 2

> 𝑀𝑀

(Minimax -Q-trained -against -selfplay ) 

> 

𝜋 2

> 𝑀𝑅

(Minimax -Q-trained -against -Random)  

> 

𝜋 2

> 𝑅

(Random)  

> 

𝜋 2 

> 𝐵𝑅

= 𝐵𝑅 (𝜋 1) (Best response to 𝜋 1)

> 38

Piazza Poll 3  

> 

Only consider strategies resulting from minimax -Q algorithm 

and random strategy. How many different tests can we run? An 

example test can be:  

> 

A: 1  

> 

B: 2  

> 

C: 4  

> 

D: 9  

> 

E: Other  

> 

F: I don’t know 

> 39

𝜋 1

> 𝑀𝑀

(Minimax -Q-trained -against -selfplay ) vs 𝜋 2

> 𝑅

(Random) Piazza Poll 3  

> 

Only consider strategies resulting from minimax -Q algorithm 

and random strategy. How many different tests can we run?  

> 

𝜋 1 can be  

> 

𝜋 1

> 𝑀𝑀

(Minimax -Q-trained -against -selfplay ) 

> 

𝜋 1

> 𝑀𝑅

(Minimax -Q-trained -against -Random)  

> 

𝜋 1

> 𝑅

(Random)  

> 

𝜋 2 can be  

> 

𝜋 2

> 𝑀𝑀

(Minimax -Q-trained -against -selfplay ) 

> 

𝜋 2

> 𝑀𝑅

(Minimax -Q-trained -against -Random)  

> 

𝜋 2

> 𝑅

(Random)  

> 

So 3*3=9 

> 40

Fictitious Play  

> 

A simple learning rule  

> 

An iterative approach for computing NE in two -player zero -

sum games  

> 

Learner explicitly maintain belief about opponent’s strategy  

> 

In each iteration, learner  

> 

Best responds to current belief about opponent  

> 

Observe the opponent’s actual play  

> 

Update belief accordingly  

> 

Simplest way of forming the belief: empirical frequency! 

> 41

Fictitious Play 

 One -shot matching pennies 

> 42

Heads  Tails 

Heads  1, -1 -1, 1

Tails  -1, 1 1, -1

Player 2 

> Player  1

Let 𝑤 (𝑎 )= #times opponent play 𝑎 

Agent believes opponent’s strategy is 

choosing 𝑎 with prob. 𝑤 𝑎   

> 𝑎 ′𝑤 𝑎 ′

Round  1’s action  2’s action  1’s belief 

in 𝑤 (𝑎 )

2’s belief 

in 𝑤 (𝑎 )

0 (1.5,2)  (2,1.5) 

1 T T (1.5, 3) (2, 2.5 )

2

3

4Fictitious Play  

> 

How would actions change from iteration 𝑡 to 𝑡 + 1? 

> 

Steady state: whenever a pure strategy profile 𝐚 = (𝑎 1, 𝑎 2)

is played in 𝑡 , it will be played in 𝑡 + 1 

> 

If 𝐚 = (𝑎 1, 𝑎 2) is a strict NE (deviation leads to lower 

utility), then it is a steady state of FP  

> 

If 𝐚 = (𝑎 1, 𝑎 2) is a steady state of FP, then it is a (possibly 

weak) NE in the game 

> 44

Fictitious Play  

> 

Will this process converge?  

> 

Assume agents use empirical frequency to form the briefs  

> 

Empirical frequencies of play converge to NE if the game is  

> 

Two -player zero -sum  

> 

Solvable by iterative removal  

> 

Some other cases 

> 45

Fictitious Play with Reinforcement Learning  

> 

In each iteration, best responds to opponents’ 

historical average strategy  

> 

Find best response through single -agent RL 

> 46

Basic implementation: Perform 

a complete RL process until 

convergence for each agent in 

each iteration 

Time consuming (Optional) MARL with Partial Observation  

> 

Assume a Markov game with partial observation (imperfect 

information) : 

> 

A set of 𝑁 agents  

> 

A set of states 𝑆  

> 

Describing the possible configurations for all agents  

> 

A set of actions for each agent 𝐴 1, … , 𝐴 𝑁  

> 

A transition function 𝑇 𝑠 , 𝑎 1, 𝑎 2, … , 𝑎 𝑛 , 𝑠 ′ 

> 

Probability of arriving at state 𝑠′ after all the agents taking 

actions 𝑎 1, 𝑎 2, … , 𝑎 𝑛 respectively  

> 

A reward function for each agent 𝑅 𝑖 (𝑠 , 𝑎 1, 𝑎 2, … , 𝑎 𝑛 ) 

> 

A set of observations for each agent 𝑂 1, … , 𝑂 𝑁  

> 

A observation function for each agent  Ω𝑖 (𝑠 )

> 47

(Optional) MARL with Partial Observation  

> 

Assume a Markov game with partial observation  

> 

Looking for a set of policies {𝜋 𝑖 𝑜 𝑖 }, one for each 

agent, without knowing 𝑇 , 𝑅 𝑖 or  Ω𝑖  

> 

Learn the policies through experience in the 

environment and interact with each other  

> 

Many algorithm can be applied, e.g., use a simple 

variant of Minimax -Q

> 48

Patrol with Real -Time Information 

 Sequential interaction 

 Players make flexible decisions instead of sticking to a plan 

 Players may leave traces as they take actions 

 Example domain: Wildlife protection 

Tree marking Lighters  Poacher camp Footprints      

> Deep Reinforcement Learning for Green Security Games with Real -Time Information Yufei Wang, Zheyuan
> Ryan Shi, Lantao Yu, Yi Wu, Rohit Singh, Lucas Joppa, Fei Fang In AAAI -19

49 Patrol with Real -Time Information 

Defender’s view 

Footprints of defender 

Destructive tools 

Footprints of attacker 

Attacker' view 

Features 

> STRAT
> POINT
> 50

Recall: Approximate Q -Learning  

> 51
> 

Features are functions from q -state (s, a) to real numbers, e.g.,  

> 

𝑓 1(𝑠 , 𝑎 )=Distance to closest ghost  

> 

𝑓 2(𝑠 , 𝑎 )=Distance to closest food  

> 

𝑓 3(𝑠 , 𝑎 )=Whether action leads to closer distance to food  

> 

Aim to learn the q -value for any ( s,a ) 

> 

Assume the q -value can be approximated 

by a parameterized Q -function 

𝑄 𝑠 , 𝑎 ≈ 𝑄 𝑤 𝑠 , 𝑎 

𝑄 𝒘 (𝑠 , 𝑎 ) = 𝑤 1𝑓 1(𝑠 , 𝑎 ) + … + 𝑤 𝑛 𝑓 𝑛 (𝑠 , 𝑎 )

If 𝑄 𝑤 (𝑠 , 𝑎 ) is a linear function of features: Recall: Approximate Q -Learning 

Update Rule for Approximate Q -Learning with Q -Value Function: 

> 52

𝑤 𝑖 ← 𝑤 𝑖 + 𝛼 𝑟  + 𝛾  max  

> 𝑎 ′

𝑄 𝑤  𝑠 ′, 𝑎 ′ − 𝑄 𝑤  𝑠 , 𝑎  𝜕 𝑄 𝑤  𝑠 , 𝑎 

𝜕 𝑤 𝑖 

If latest sample higher than previous estimate: 

adjust weights to increase the estimated Q -value 

Previous estimate Latest sample 

Need to learn parameters 𝑤 through interacting with the environment (Optional) Train Defender Against Heuristic Attacker  

> 

Through single -agent RL  

> 

Use neural network to represent a parameterized Q function 

𝑄 (𝑜 𝑖 , 𝑎 𝑖 ) where 𝑜 is the observation 

Up  Down  Left  Right  Still 

> 53

(Optional) Train Defender Against Heuristic Attacker 

Defender 

Snares 

Attacker 

Patrol Post 

> 54

Compute Equilibrium: RL + Double Oracle 

Compute 𝜎 𝑑 , 𝜎 𝑎 =

𝑁𝑎𝑠ℎ (𝐺 𝑑 , 𝐺 𝑎 ) Train 𝑓 𝑑 = 𝑅𝐿 (𝜎 𝑎 )

Find Best Response to 

defender’s strategy 

Compute Nash/Minimax 

Train 𝑓 𝑎 = 𝑅𝐿 (𝜎 𝑎 )

Find Best Response 

to attacker’s strategy 

Add 𝑓 𝑑 ,𝑓 𝑎 to 

𝐺 𝑑 , 𝐺 𝑎 

Update bags of strategies 

> 55

(Optional) Other Domains: Patrol in Continuous Area 

OptGradFP: CNN + Fictitious Play 

DeepFP : Generative network + Fictitious Play 

Policy Learning for Continuous Space Security Games using 

Neural Networks. Nitin Kamra , Umang Gupta, Fei Fang, 

Yan Liu, Milind Tambe . In AAAI -18 

DeepFP for Finding Nash Equilibrium in Continuous 

Action Spaces. Nitin Kamra , Umang Gupta, Kai Wang, Fei 

Fang, Yan Liu, Milind Tambe . In GameSec -19 

56 AI Has Great Potential for Social Good 

Artificial 

Intelligence 

Machine Learning 

Computational 

Game Theory 

Security & Safety 

Environmental 

Sustainability  Mobility 

Societal Challenges