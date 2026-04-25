# Source: https://openai.com/research/learning-to-summarize-with-human-feedback
# Fetched via: search fallback (Perplexity)
# Downloaded: 2026-04-09
# Words: 2376
# Author: OpenAI
# Author Slug: openai
September 4, 2020

Publication

# Learning to summarize with human feedback

We’ve applied reinforcement learning from human feedback to train language models that are better at summarization.

Listen to article

## Why it matters

Our models generate summaries that are better than summaries from 10x larger models trained only with supervised learning. Even though we train our models on the Reddit TL;DR dataset, the same models transfer to generate good summaries of CNN/DailyMail news articles without any further fine-tuning. Our techniques are not specific to summarization; in the long run, our goal is to make aligning AI systems with human preferences a central component of AI research and deployment in many domains.
Large-scale language models are becoming increasingly capable on NLP tasks. These models are usually trained with the objective of next word prediction on a dataset of human-written text. But this objective doesn’t capture exactly what we want; usually, we don’t want our models to imitate humans, we want them to give high-quality answers.
This mismatch is clear when a model is trained to imitate low-quality human-written text, but it can also happen in more subtle ways. For example, a model trained to predict what a human would say might make up facts when it is unsure, or generate sentences reflecting harmful social bias, both failure modes that have been well-documented.^3, 4, 5, 6^
As part of our work on safety, we want to develop techniques that align our models’ objectives with the end behavior we really care about. As our models become more powerful, we believe aligning them with our goals will be very important to ensure they are beneficial for humans. In the short term, we wanted to test if human feedback techniques could help our models improve performance on useful tasks.
We focused on English text summarization, as it’s a challenging problem where the notion of what makes a “good summary” is difficult to capture without human input. We apply our method primarily to an existing dataset^1^ of posts submitted to the social network Reddit^B^ together with human-written “TL;DRs,” which are short summaries written by the original poster.
We first train a reward model via supervised learning to predict which summaries humans will prefer.^A^ We then fine-tune a language model with reinforcement learning (RL) to produce summaries that score highly according to that reward model. We find that this significantly improves the quality of the summaries, as evaluated by humans, even on datasets very different from the one used for fine-tuning.
Our approach follows directly from our previous work⁠ on learning from human feedback.^7^ There has also been other work on using human feedback to train summarization models.^8^ We push the technique further by scaling to larger models, collecting more feedback data, closely monitoring researcher-labeler agreement, and providing frequent feedback to labelers.
Human feedback has also been used to train models in several other domains, such as dialogue,^9, 10, 11^ semantic parsing,^12^ translation,^13, 14^ story^15^ and review^16^ generation, evidence extraction,^17^ and more traditional RL tasks.^18, 19^

…

Pre-trained 6B model

What does the debt ceiling really mean?

We evaluated several different summarization models—some pre-trained on a broad distribution of text from the internet, some fine-tuned via supervised learning to predict TL;DRs, and some fine-tuned using human feedback.^D^ To evaluate each model, we had it summarize posts from the validation set and asked humans to compare their summaries to the human-written TL;DR. The results are shown in Figure 1⁠.
We found that RL fine-tuning with human feedback had a very large effect on quality compared to both supervised fine-tuning and scaling up model size. In particular, our 1.3 billion parameter (1.3B) model trained with human feedback outperforms our 12B model trained only with supervised learning. Summaries from both our 1.3B and 6.7B human feedback models are preferred by our labelers to the original human-written TL;DRs in the dataset.^E^
People make different trade-offs when writing summaries, including between conciseness and coverage of the original text; depending on the purpose of the summary, different summary lengths might be preferred. Our labelers tended to prefer longer summaries, so our models adapted to that preference and converged to the longest allowable length. Controlling for length reduced human preferences for our 6.7B model’s summaries from 70% to 65%, explaining a minority of our gains.^F^

# Human feedback models trained on Reddit transfer to generate excellent summaries of CNN/DM news articles without further training

- Raw scores
- Length-controlled

…

This time we evaluated our models by asking our labelers to rate them on a scale from 1–7.^G^ We discovered that our human feedback models transfer to generate excellent short summaries of news articles without any training. When controlling for summary length, our 6.7B human feedback model generates summaries that are rated higher than the CNN/DM reference summaries written by humans. This suggests that our human feedback models have learned something more general about how to summarize text, and are not specific to Reddit posts.
A diagram of our method, which is similar to the one used in our previous work⁠(opens in a new window).

Our core method consists of four steps: training an initial summarization model, assembling a dataset of human comparisons between summaries, training a reward model to predict the human-preferred summary, and then fine-tuning our summarization models with RL to get a high reward.
We trained several supervised baselines by starting from GPT‑style transformer models trained on text from the Internet,20⁠ and fine-tuning them to predict the human-written TL;DR via supervised learning. We mainly use models with 1.3 and 6.7 billion parameters. As a sanity check, we confirmed that this training procedure led to competitive results^H^ on the CNN/DM dataset.
We then collected a dataset of human quality judgments. For each judgment, a human compares two summaries of a given post and picks the one they think is better.^I^ We use this data to train a reward model that maps a *(post, summary)* pair to a reward *r*. The reward model is trained to predict which summary a human will prefer, using the rewards as logits.
Finally, we optimize the policy against the reward model using RL. We use PPO⁠ with 1 million episodes in total, where each episode consists of the policy summarizing a single article and then receiving a reward *r*. We include a KL penalty that incentivizes the policy to remain close to the supervised initialization.

Any training procedure that uses human feedback is directly influenced by the actual humans labeling the data. In our previous work on fine-tuning language models from human preferences,7⁠ our labelers often gave high ratings to summaries we thought were average, which was reflected in the quality of our trained models.

…

Optimizing against our reward model is supposed to make our policy align with human preferences. But the reward model is only a proxy for human preferences, as it only sees a small amount of comparison data from a narrow distribution of summaries. While the reward model performs well on the kinds of summaries it was trained on, we wanted to know how much we could optimize against it until it started giving useless evaluations.
We trained policies at different “optimization strengths” against the reward model, and asked our labelers to evaluate the summaries from these models. We did this by varying the KL coefficient, which trades off the incentive to get a higher reward against the incentive to remain close to the initial supervised policy. We found the best samples had roughly the same predicted reward as the 99th percentile of reference summaries from the dataset. Eventually optimizing the reward model actually makes things worse.
If we have a well-defined notion of the desired behavior for a model, our method of training from human feedback allows us to optimize for this behavior. However, this is not a method for determining what the desired model behavior *should be*. Deciding what makes a good summary is fairly straightforward, but doing this for tasks with more complex objectives, where different humans might disagree on the correct model behavior, will require significant care.

…

We trained on the Reddit TL;DR dataset1⁠ because the summarization task is significantly more challenging than on CNN/DM. However, since the dataset consists of user-submitted posts with minimal moderation, they sometimes contain content that is offensive or reflects harmful social biases. This means our models can generate biased or offensive summaries, as they have been trained to summarize such content.
Part of our success involves scaling up our reward model and policy size. This requires a large amount of compute, which is not available to all researchers: notably, fine-tuning our 6.7B model with RL required about 320 GPU-days. However, since smaller models trained with human feedback can exceed the performance of much larger models, our procedure is more cost-effective than simply scaling up for training high-quality models on specific tasks.
Though we outperform the human-written reference summaries on TL;DR, our models have likely not reached human-level performance, as the reference summary baselines for TL;DR and CNN/DM are not the highest possible quality. When evaluating our model’s TL;DR summaries on a 7-point scale along several axes of quality (*accuracy*, *coverage*, *coherence*, and *overall*), labelers find our models can still generate inaccurate summaries, and give a perfect *overall* score 45% of the time.

…

We’re interested in scaling human feedback to tasks where humans can’t easily evaluate the quality of model outputs. For example, we might want our models to answer questions that would take humans a lot of research to verify; getting enough human evaluations to train our models this way would take a long time. One approach to tackle this problem is to give humans tools to help them evaluate more quickly and accurately. If these tools use ML, we can also improve them with human feedback, which could allow humans to accurately evaluate model outputs for increasingly complicated tasks.^23^
In addition to tackling harder problems, we’re also exploring different types of feedback beyond binary comparisons: we can ask humans to provide demonstrations, edit model outputs to make them better, or give explanations as to why one model output is better than another. We’d like to figure out which kinds of feedback are most effective for training models that are aligned with human preferences.

…

## Footnotes

1. 1
   For training, we use the Reddit TL;DR dataset instead of the more popular CNN/DM dataset because simple copying baselines perform better than the human-written reference summaries on CNN/DM, which is not the case for TL;DR (see Appendix D of our paper). We performed a new web crawl to increase the TL;DR dataset size, required summaries to be between 24 and 48 tokens, and performed some other cleaning and filtering
2. B
   We hire human labelers to judge summary quality, and implement quality control to ensure that labeler judgments agree with our own. We describe our human data collection procedure below.
3. C
   Interestingly, we found that human evaluators preferred the Lead-3 baseline (taking the first 3 sentences of the article) to the dataset’s reference summaries, and we confirmed this ourselves.
4. D
   We generate all of our samples at temperature 0, which we found humans preferred most.
5. E
   While we use human-written TL;DRs as our main point of comparison, they don’t always represent optimal human performance; they are sometimes intended to be funny or to summarize only a part of the post, and their grammar and style are all over the map.
6. F
   We control by training a logistic regression model to predict the preferred summary given only the policy ID and the log ratio of the lengths of the summaries. Then, we report the regression coefficients on each policy ID, corresponding to a length ratio of 1 with the reference summaries.
7. G
   We took this approach because it is hard to directly compare our TL;DR-trained models to models trained on CNN/DM; the CNN/DM summaries are much longer and written in bullet-point form.
8. 21
   In terms of ROUGE results on CNN/DM, our 6.7B supervised models are a bit worse than T5 , but a bit better than state-of-the-art models from mid-2019.
9. I
   Our main models are trained on about 65K comparisons, though we achieve good results with as few as 8K comparisons.
10. J
   Specifically, we use Upwork, Scale, and Lionbridge. Our contractors have a range of ages, genders, and educational backgrounds, and are mostly American or Filipino (see Appendix C of our paper for demographic data).
11. K
   Our criteria for hiring contractors were: (1) they were willing to do the task, and (2) they passed a minimum threshold of speed and agreement with researcher labels. We paid all our contractors at least $15/hr.
12. L
   This is impressive relative to the TL;DR reference summaries, which get a perfect *overall* score 23% of the time, but indicates there is still room for improvement.

Nisan Stiennon∗
Long Ouyang∗
Jeff Wu∗
Daniel M. Ziegler∗
Ryan Lowe∗
Chelsea Voss∗
Alec Radford
Dario Amodei
Paul Christiano∗
OpenAI
Abstract
As language models become more powerful, training and evaluation are increas-
ingly bottlenecked by the data and metrics used for a particular task. For example,
summarization models are often trained to predict human reference summaries and
evaluated using ROUGE, but both of these metrics are rough proxies for what we
really care about—summary quality. In this work, we show that it is possible to
significantly improve summary quality by training a model to optimize for human
preferences. We collect a large, high-quality dataset of human comparisons be-
tween summaries, train a model to predict the human-preferred summary, and use
that model as a reward function to fine-tune a summarization policy using reinforce-
ment learning. We apply our method to a version of the TL;DR dataset of Reddit
posts [63] and find that our models significantly outperform both human reference
summaries and much larger models fine-tuned with supervised learning alone. Our
models also transfer to CNN/DM news articles [22], producing summaries nearly
as good as the human reference without any news-specific fine-tuning.2 We con-
duct extensive analyses to understand our human feedback dataset and fine-tuned
models.3 We establish that our reward model generalizes to new datasets, and that
optimizing our reward model results in better summaries than optimizing ROUGE
according to humans. We hope the evidence from o