# Source: https://react-lm.github.io
# Title: ReAct: Synergizing Reasoning and Acting in Language Models
# Fetched via: jina
# Date: 2026-04-10

Title: ReAct: Synergizing Reasoning and Acting in Language Models



# ReAct: Synergizing Reasoning and Acting in Language Models

# ReAct: Synergizing Reasoning and Acting in Language Models

[Shunyu Yao](https://ysymyth.github.io/), [Jeffrey Zhao](http://descrip.github.io/), [Dian Yu](https://diandyu.github.io/), [Nan Du](https://research.google/people/104844/), [Izhak Shafran](https://research.google/people/IzhakShafran/), [Karthik Narasimhan](https://www.cs.princeton.edu/~karthikn/), [Yuan Cao](https://research.google/people/YuanCao/)

[**[Paper]**](https://arxiv.org/abs/2210.03629)[**[Code]**](https://github.com/ysymyth/ReAct)[**[Blogpost]**](https://ai.googleblog.com/2022/11/react-synergizing-reasoning-and-acting.html)[**[BibTex]**](https://react-lm.github.io/files/bib.txt)


Language models are getting better at reasoning (e.g. chain-of-thought prompting) and acting (e.g. WebGPT, SayCan, ACT-1), but these two directions have remained separate. 

**ReAct asks, what if these two fundamental capabilities are combined?**

## Abstract

While large language models (LLMs) have demonstrated impressive capabilities across tasks in language understanding and interactive decision making, their abilities for reasoning (e.g. chain-of-thought prompting) and acting (e.g. action plan generation) have primarily been studied as separate topics. In this paper, we explore the use of LLMs to generate both reasoning traces and task-specific actions in an interleaved manner, allowing for greater synergy between the two: reasoning traces help the model induce, track, and update action plans as well as handle exceptions, while actions allow it to interface with external sources, such as knowledge bases or environments, to gather additional information. We apply our approach, named ReAct, to a diverse set of language and decision making tasks and demonstrate its effectiveness over state-of-the-art baselines, as well as improved human interpretability and trustworthiness over methods without reasoning or acting components. Concretely, on question answering (HotpotQA) and fact verification (Fever), ReAct overcomes issues of hallucination and error propagation prevalent in chain-of-thought reasoning by interacting with a simple Wikipedia API, and generates human-like task-solving trajectories that are more interpretable than baselines without reasoning traces. On two interactive decision making benchmarks (ALFWorld and WebShop), ReAct outperforms imitation and reinforcement learning methods by an absolute success rate of 34% and 10% respectively, while being prompted with only one or two in-context examples.

## ReAct Prompting

A ReAct prompt consists of few-shot task-solving trajectories, with human-written text reasoning traces and actions, as well as environment observations in response to actions (see examples in paper appendix!) 

 ReAct prompting is intuitive and flexible to design, and achieves state-of-the-art few-shot performances across a variety of tasks, from question answering to online shopping!


#### HotpotQA Example

The reason-only baseline (i.e. chain-of-thought) suffers from misinformation (in red) as it is not grounded to external environments to obtain and update knowledge, and has to rely on limited internal knowledge. 

 The act-only baseline suffers from the lack of reasoning, unable to synthesize the final answer despite having the same actions and observation as ReAct in this case. 

 In contrast, ReAct solves the task with a interpretable and factual trajectory.


#### ALFWorld Example

For decision making tasks, we design human trajectories with sparse reasoning traces, letting the LM decide when to think vs. act. 

 ReAct isn't perfect --- below is a failure example on ALFWorld. However, ReAct format allows easy human inspection and behavior correction by changing a couple of model thoughts, an exciting novel approach to human alignment!


## ReAct Finetuning: Initial Results

Prompting has limited context window and learning support. Initial finetuning results on HotpotQA using ReAct prompting trajectories suggest: (1) ReAct is the best fintuning format across model sizes; (2) ReAct finetuned smaller models outperform prompted larger models!