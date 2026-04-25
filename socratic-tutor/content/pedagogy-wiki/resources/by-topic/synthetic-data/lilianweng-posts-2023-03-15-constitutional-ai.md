# Source: https://lilianweng.github.io/posts/2023-03-15-constitutional-ai/
# Fetched via: search fallback (Perplexity)
# Downloaded: 2026-04-09
# Words: 2350
# Author: Lilian Weng
# Author Slug: lilian-weng
[Submitted on 15 Dec 2022]
…
Abstract:As AI systems become more capable, we would like to enlist their help to supervise other AIs.
We experiment with methods for training a harmless AI assistant through self-improvement, without any human labels identifying harmful outputs.
The only human oversight is provided through a list of rules or principles, and so we refer to the method as 'Constitutional AI'.
The process involves both a supervised learning and a reinforcement learning phase.
In the supervised phase we sample from an initial model, then generate self-critiques and revisions, and then finetune the original model on revised responses.
In the RL phase, we sample from the finetuned model, use a model to evaluate which of the two samples is better, and then train a preference model from this dataset of AI preferences.
We then train with RL using the preference model as the reward signal, i.e. we use 'RL from AI Feedback' (RLAIF).
As a result we are able to train a harmless but non-evasive AI assistant that engages with harmful queries by explaining its objections to them.
Both the SL and RL methods can leverage chain-of-thought style reasoning to improve the human-judged performance and transparency of AI decision making.
…
|Subjects:|Computation and Language (cs.CL); Artificial Intelligence (cs.AI)|
...
| |https://doi.org/10.48550/arXiv.2212.08073 arXiv-issued DOI via DataCite|

# Constitutional AI: Harmlessness from AI Feedback
...
Based on my review of the paper, it does not appear to have a clearly stated central research question or hypothesis.
The paper seems to focus on presenting a new method called "Constitutional AI" for training AI systems to be helpful, harmless, and honest without relying on large amounts of human feedback.
The key elements of the Constitutional AI method include:
- Using an initial "helpful" RLHF model to generate responses to prompts
- Asking the model to critique its own harmful responses according to principles/rules (the "constitution")
- Revising the responses to remove harm
- Finetuning a model on the revised responses
- Using the finetuned model to generate responses and have another model evaluate/compare them
- Distilling the model evaluations into a preference model
- Doing RL using the preference model as the reward signal
So in summary, the paper is presenting and evaluating this new Constitutional AI training technique, rather than testing a specific hypothesis.
The motivating goals seem to be finding ways to train AI systems that are helpful, harmless, and honest with minimal human oversight.
Does this help summarize the key focus and contributions of the paper?
...
This paper introduces Constitutional AI (CAI), a method for training AI systems to be helpful, honest and harmless using simple principles rather than extensive human feedback data.
The key contributions are:
…
- Using model-generated preferences between responses as a reward signal for RL, eliminating the need for human harmfulness labels.
Models trained this way are less harmful and non-evasive.
- Establishing that constitutional AI can train models to be helpful and harmless using only around 10 simple human-written principles as supervision, rather than extensive human feedback.
Overall, the main contribution is showing that constitutional AI can greatly reduce the amount of human involvement needed for training helpful, honest and harmless AI systems.
This makes it possible to control model behavior more precisely with far less human effort.
## What is the TL;DR (Too Long, Didn't Read) version of the paper?
If you had to summarize it in one sentence, what would that be?
Based on skimming the paper, I would summarize it as:
"The authors propose Constitutional AI - a method to train AI systems to be helpful and harmless using critiques, revisions, and reinforcement learning guided by simple principles, with minimal human oversight."
In more detail:
The paper introduces a method called "Constitutional AI" to train AI assistants to be helpful and harmless without requiring large amounts of human feedback.
The key ideas are:
…
## Summarize the paper in one paragraph.
Here is a one paragraph summary of the paper:
The paper presents a method for training helpful and harmless AI assistants using constitutional principles rather than direct human supervision.
The method has two main stages - a supervised learning stage and a reinforcement learning stage.
In the supervised stage, an initial helpful AI assistant is asked to critique and revise its own potentially harmful responses according to constitutional principles that encourage harmlessness.
…
The paper presents a method called Constitutional AI (CAI) to train AI systems to be helpful, honest, and harmless without relying on human labels identifying harmful outputs.
CAI has two main stages - a supervised learning stage and a reinforcement learning stage.
In the supervised stage, an initial AI assistant is asked to critique and revise its own potentially harmful responses according to principles in a 'constitution.'
…
## What problem or question is the paper addressing?
The paper titled "Constitutional AI: Harmlessness from AI Feedback" addresses the challenge of training AI systems to be helpful, honest, and harmless without relying extensively on human oversight.
Specifically, it investigates methods for an AI system to supervise and improve itself in order to reduce harmful behaviors, with minimal human involvement beyond specifying a simple set of principles or "constitution" to govern the AI's conduct.
…
The paper seems to focus on using constitutional principles and model critiques/revisions to train AI assistants to be helpful, harmless, and honest, with minimal direct human oversight.
Key methods discussed include critiquing and revising model responses using constitutional principles, distilling these revisions into preference models, and using the preference models for reinforcement learning.
The goal is to develop transparent and robust AI systems using scaling supervision and self-supervision, with human oversight focused on high-level principles rather than direct feedback.
Let me know if any other key terms come to mind based on your reading!
…
## Summarize the paper in two paragraphs.
Here is a two paragraph summary of the paper:
The paper presents a method called Constitutional AI (CAI) to train AI systems to be helpful, harmless, and honest.
CAI involves two main stages - a supervised learning (SL) stage and a reinforcement learning (RL) stage.
In the SL stage, the authors start with a helpful AI assistant and have it critique and revise its own potentially harmful responses according to a set of principles called a "constitution."
…
This paper introduces Constitutional AI (CAI), a new technique for training AI systems to behave in helpful, honest, and harmless ways using only simple principles rather than large amounts of human feedback data.
The authors first show that large language models can effectively identify harmful behaviors at levels approaching human accuracy.
They then detail a CAI training process with two main stages: (1) In the supervised learning stage, an initial model generates self-critiques and revisions to reduce harmfulness based on constitutional principles.
…
## Summarize the paper in one sentence.
This paper introduces Constitutional AI, a method to train helpful and harmless AI assistants by having them generate self-critiques and revisions according to principles in a "constitution", without requiring human feedback on harmfulness.
## Summarize the paper in one paragraphs.
This paper proposes Constitutional AI (CAI), a method for training AI systems to be helpful, honest, and harmless using only a small set of principles rather than a large dataset of human feedback labels.
The approach has two main phases:
1. Supervised Learning CAI: An initial AI assistant is used to generate responses to prompts.
It then critiques its own responses according to principles in a "constitution", and revises the responses to remove harmful content.
The initial AI is finetuned on these revised responses.
2. Reinforcement Learning CAI: The finetuned AI generates pairs of responses to harmful prompts.
Another AI acts as a "feedback model" and selects the less harmful response based on the constitution.
This generates a dataset of AI preferences for harmlessness.
RL trains a final AI on human preferences for helpfulness mixed with AI preferences for harmlessness.
…
## Design 10 in-depth questions about the method proposed in this paper and avoid simple questions.

oversight is provided through a list of rules or principles, and so we refer to the method as
‘Constitutional AI’. The process involves both a supervised learning and a reinforcement
learning phase. In the supervised phase we sample from an initial model, then generate
self-critiques and revisions, and then finetune the original model on revised responses. In
the RL phase, we sample from the finetuned model, use a model to evaluate which of the
two samples is better, and then train a preference model from this dataset of AI prefer-
ences. We then train with RL using the preference model as the reward signal, i.e. we
use ‘RL from AI Feedback’ (RLAIF). As a result we are able to train a harmless but non-
evasive AI assistant that engages with harmful queries by explaining its objections to them.
Both the SL and RL methods can leverage chain-of-thought style reasoning to improve the
human-judged performance and transparency of AI decision making. These methods make
it possible to control AI behavior more precisely and with far fewer human labels.
∗Correspondence to: {yuntao,jared}@anthropic.com
Author contributions are detailed in 7.
arXiv:2212.08073v1  [cs.CL]  15 Dec 2022
Generate Responses
to “Red Teaming”
Prompts Eliciting Harmful
Samples
Generate Responses
to “Red Teaming”
Prompts Eliciting 
Harmful Samples
 RLAIF
Training
with 
PM + SL-CAI 
Models
Constitutional AI Feedback
for Self-Improvement
Helpful RLHF 
Model
Generate Responses
to “Red Teaming”
Prompts Eliciting Harmful
Samples
Generate Responses
to “Red Teaming”
Prompts Eliciting 
Pairs of Samples
Finetuned
Preference
Model (PM)
Finetuned
SL-CAI
Model
Final
RL-CAI
Model
Response
Critique
Revision
Figure 1
We show the basic steps of our Constitutional AI (CAI) process, which consists of both a super-
vised learning (SL) stage, consisting of the steps at the top, and a Reinforcement Learning (RL) stage, shown
as the sequence of steps at the bottom of the figure. Both the critiques and the AI feedback are steered by
a small set of principles drawn from a ‘constitution’. The supervised stage significantly improves the initial
model, and gives some control over the initial behavior at the start of the RL phase, addressing potential
exploration problems. The RL stage significantly improves performance and reliability.
1
Introduction
We would like to train AI systems that remain helpful, honest, and harmless, even as some AI capabilities
reach or exceed human-level performance. This suggests that we will need to develop techniques that do not
rely on humans to supervise all aspects of AI behavior, and that can be used to automatically test and enhance
robustness to harmful behaviors. We also aim to develop methods that encode desirable AI behavior in a
simple and transparent form, and that make it easier to understand and evaluate AI decision making.
In this paper we develop a method we refer to as Constitutional AI (CAI), depicted in Figure 1, and use it
to train a non-evasive and relatively harmless AI assistant, without any human feedback labels for harms.
The method therefore improves upon, and partially replaces reinforcement learning from human feedback
[Christiano et al., 2017]. The new assistant ‘RL-CAI’ is preferred by crowdworkers over those trained with
previously collected [Bai et al., 2022, Ganguli et al., 2022] human feedback labels for harmfulness. We chose
the term ‘constitutional’ because we are able to train less harmful systems entirely through the specification
of a short list of principles or instructions, i.e. a constitution. But we are also employing this terminology to
emphasize that when developing and deploying a general AI system, we cannot avoid choosing some set of
principles to govern it, even if they remain hidden or implicit.
Our motivations for developing this technique were: (1) to study simple possibilities for using AI systems to
help supervise other AIs, and thus scale supervision, (2) to improve on our prior work training a harmless AI
assistant by eliminating evasive responses, reducing tension1 [Bai et al., 2022, Glaese et al., 2022] between
helpfulness and harmlessness and encouraging the AI to explain its objections to harmful requests, (3) to
make the principles governing AI behavior, and their implementation, more transparent, and (4) to reduce
iteration time by obviating the need to collect new human feedback labels when altering the objective. Let us

…

Pretrained
Base
Constitutional RL
(Pareto Improvement)
With Chain
of Thought
Standard
RLHF
Constitutional SL
Helpful-Only
Helpful
+ Harmless
Figure 2
We show harmlessness versus helpfulness Elo scores (higher is better, only differences are mean-
ingful) computed from crowdworkers’ model comparisons for all 52B RL runs. Points further to the right
are later steps in RL training.
The Helpful and HH models were trained with human feedback as in
[Bai et al., 2022], and exhibit a tradeoff between helpfulness and harmlessness. The RL-CAI models trained

…

(and quite possibly obscuring) decision making. As we discuss below, our constitutional approach leverages
chain-of-thought reasoning [Nye et al., 2021, Wei et al., 2022] to make decision making more legible.
In a certain sense,
work on reinforcement learning from human feedback [Stiennon et al., 2020,

…

Here, we will test methods that reduce human input to an extreme, in order to study their viability. We will
finetune AI models to be harmless using only of order ten2 simple principles, stated in natural language.
2These principles were chosen in a fairly ad hoc and iterative way for research purposes. In the future, we believe

…

1010
5 1010
Parameters
250
200
150
100
50
0
50
100
150
Helpfulness Elo
SL-CAI
Helpful RLHF
HH RLHF
RL-CAI
RL-CAI w/ CoT
1010
5 1010

…

and helpful & harmless (HH) RLHF are similar to prior work [Bai et al., 2022]. SL-CAI, RL-CAI, and RL-
CAI w/ CoT models are trained with our new constitutional method.
Although here we largely eliminate direct human supervision for harmlessness, rather than removing human

…

1.2
The Constitutional AI Approach
We will be experimenting with an extreme form of scaled supervision, which we refer to as Constitutional
AI (CAI). The idea is that human supervision will come entirely from a set of principles that should govern
AI behavior, along with a small number of examples used for few-shot prompting. Together thes