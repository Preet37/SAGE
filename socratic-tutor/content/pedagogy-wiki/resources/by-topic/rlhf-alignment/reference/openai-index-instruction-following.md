# Source: https://openai.com/index/instruction-following/
# Author: OpenAI
# Author Slug: openai
# Title: Aligning language models to follow instructions
# Fetched via: jina
# Date: 2026-04-09

Title: Aligning language models to follow instructions


# Aligning language models to follow instructions | OpenAI


[](https://openai.com/)

*   [Research](https://openai.com/research/index/)
*   Products
*   [Business](https://openai.com/business/)
*   [Developers](https://openai.com/api/)
*   [Company](https://openai.com/about/)
*   [Foundation(opens in a new window)](https://openaifoundation.org/)

Log in[Try ChatGPT(opens in a new window)](https://chatgpt.com/)

*   Research
*   Products
*   Business
*   Developers
*   Company
*   [Foundation(opens in a new window)](https://openaifoundation.org/)

[Try ChatGPT(opens in a new window)](https://chatgpt.com/)Login

OpenAI

Table of contents

*   [Results](https://openai.com/index/instruction-following/#results)
*   [Methods](https://openai.com/index/instruction-following/#methods)
*   [Generalizing to broader preferences](https://openai.com/index/instruction-following/#generalizing-to-broader-preferences)
*   [Limitations](https://openai.com/index/instruction-following/#limitations)
*   [Next steps](https://openai.com/index/instruction-following/#next-steps)

January 27, 2022

[Publication](https://openai.com/research/index/publication/)

# Aligning language models to follow instructions

[Read paper(opens in a new window)](https://arxiv.org/abs/2203.02155)[View model card(opens in a new window)](https://github.com/openai/following-instructions-human-feedback)

Loading…

Share

We’ve trained language models that are much better at following user intentions than GPT‑3 while also making them more truthful and less toxic, using techniques developed through our alignment research. These _InstructGPT_ models, which are trained with humans in the loop, are now deployed as the default language models on our API.


The[OpenAI API is powered by GPT‑3 language models⁠](https://openai.com/index/gpt-3-apps/)which can be coaxed to perform natural language tasks using carefully engineered text prompts. But these models can also generate outputs that are untruthful, toxic, or reflect harmful sentiments. This is in part because GPT‑3 is trained to predict the next word on a large dataset of Internet text, rather than to safely perform the language task that the user wants. In other words, these models aren’t _aligned_ with their users.

To make our models safer, more helpful, and more aligned, we use an existing technique called[reinforcement learning from human feedback (RLHF)⁠](https://openai.com/index/learning-from-human-preferences/). On prompts submitted by our customers to the API,[A](https://openai.com/index/instruction-following/#citation-bottom-A)our labelers provide demonstrations of the desired model behavior, and rank several outputs from our models. We then use this data to fine-tune GPT‑3.

The resulting InstructGPT models are much better at following instructions than GPT‑3. They also make up facts less often, and show small decreases in toxic output generation. Our labelers prefer outputs from our 1.3B InstructGPT model over outputs from a 175B GPT‑3 model, despite having more than 100x fewer parameters. At the same time, we show that we don’t have to compromise on GPT‑3’s capabilities, as measured by our model’s performance on academic NLP evaluations.

These InstructGPT models, which have been in beta on the API for more than a year, are now the default language models accessible on our API.[B](https://openai.com/index/instruction-following/#citation-bottom-B)We believe that fine-tuning language models with humans in the loop is a powerful tool for improving their safety and reliability, and we will continue to push in this direction.

This is the first time our alignment research, which we’ve been[pursuing⁠](https://openai.com/index/deep-reinforcement-learning-from-human-preferences/)for[several⁠](https://openai.com/index/fine-tuning-gpt-2/)[years⁠](https://openai.com/index/learning-to-summarize-with-human-feedback/),[1](https://openai.com/index/instruction-following/#citation-bottom-1), [2](https://openai.com/index/instruction-following/#citation-bottom-2), [3](https://openai.com/index/instruction-following/#citation-bottom-3)has been applied to our product. Our work is also related to recent research that fine-tunes language models to follow instructions using academic NLP datasets, notably FLAN[4](https://openai.com/index/instruction-following/#citation-bottom-4)and T0.[5](https://openai.com/index/instruction-following/#citation-bottom-5)A key motivation for our work is to increase helpfulness and truthfulness while mitigating the harms and biases of language models.[6](https://openai.com/index/instruction-following/#citation-bottom-6), [7](https://openai.com/index/instruction-following/#citation-bottom-7), [8](https://openai.com/index/instruction-following/#citation-bottom-8), [9](https://openai.com/index/instruction-following/#citation-bottom-9), [10](https://openai.com/index/instruction-following/#citation-bottom-10)Some of[our previous research⁠](https://openai.com/index/improving-language-model-behavior/)in this direction found that we can reduce harmful outputs by fine-tuning on a small curated dataset of human demonstrations.[11](https://openai.com/index/instruction-following/#citation-bottom-11)Other research has focused on filtering the pre-training dataset,[12](https://openai.com/index/instruction-following/#citation-bottom-12)safety-specific control tokens,[13](https://openai.com/index/instruction-following/#citation-bottom-13), [14](https://openai.com/index/instruction-following/#citation-bottom-14)or steering model generations.[15](https://openai.com/index/instruction-following/#citation-bottom-15), [16](https://openai.com/index/instruction-following/#citation-bottom-16)We are exploring these ideas and others in our ongoing alignment research.

## Results

We first evaluate how well outputs from InstructGPT follow user instructions, by having labelers compare its outputs to those from GPT‑3. We find that InstructGPT models are significantly preferred on prompts submitted to both the InstructGPT and GPT‑3 models on the API. This holds true when we add a prefix to the GPT‑3 prompt so that it enters an “instruction-following mode.”


To measure the safety of our models, we primarily use a suite of existing metrics on publicly available datasets. Compared to GPT‑3, InstructGPT produces fewer imitative falsehoods (according to TruthfulQA[17](https://openai.com/index/instruction-following/#citation-bottom-17)) and are less toxic (according to RealToxicityPrompts[18](https://openai.com/index/instruction-following/#citation-bottom-18)). We also conduct human evaluations on our API prompt distribution, and find that InstructGPT makes up facts (“hallucinates”) less often, and generates more appropriate outputs.[C](https://openai.com/index/instruction-following/#citation-bottom-C)


Finally, we find that InstructGPT outputs are preferred to those from FLAN[4](https://openai.com/index/instruction-following/#citation-bottom-4)and T0[5](https://openai.com/index/instruction-following/#citation-bottom-5)on our customer distribution. This indicates that the data used to train FLAN and T0, mostly academic NLP tasks, is not fully representative of how deployed language models are used in practice.

## Methods


To train InstructGPT models, our core technique is[reinforcement learning from human feedback(RLHF)⁠](https://openai.com/index/deep-reinforcement-learning-from-human-preferences/), a method we helped pioneer in our earlier alignment research. This technique uses human preferences as a reward signal to fine-tune our models, which is important as the safety and alignment problems we are aiming to solve are complex and subjective, and aren’t fully captured by simple automatic metrics.

We first collect a dataset of human-written demonstrations on prompts submitted to our API, and use this to train our supervised learning baselines. Next, we collect a dataset of human-labeled comparisons between two model outputs on a larger set of API prompts. We then train a reward model (RM) on this dataset to predict which output our labelers would prefer. Finally, we use this RM as a reward function and fine-tune our GPT‑3 policy to maximize this reward using the[PPO algorithm⁠](https://openai.com/index/openai-baselines-ppo/).

One way of thinking about this process is that it “unlocks” capabilities that GPT‑3 already had, but were difficult to elicit through prompt engineering alone: this is because our training procedure has a limited ability to teach the model new capabilities relative to what is learned during pretraining, since it uses less than 2% of the compute and data relative to model pretraining.

A limitation of this approach is that it introduces an “alignment tax”: aligning the models only on customer tasks can make their performance worse on some other academic NLP tasks. This is undesirable since, if our alignment techniques make models worse on tasks that people care about, they’re less likely to be adopted in practice. We’ve found a simple algorithmic change that minimizes this alignment tax: during RL fine-tuning we mix in a small fraction of the original data used to train GPT‑3, and train on this data using the normal log likelihood maximization.[D](https://openai.com/index/instruction-following/#citation-bottom-D)This roughly maintains performance on safety and human preferences, while mitigating performance decreases on academic tasks, and in several cases even surpassing the GPT‑3 baseline.

## Generalizing to broader preferences

Our procedure aligns our models’ behavior with the preferences of our labelers, who directly produce the data used to train our models, and us researchers, who provide guidance to labelers through written instructions, direct feedback on specific examples, and informal conversations. It is also influenced by our customers and the preferences implicit in our API policies. We selected labelers who performed well on a screening test for aptitude in identifying and responding to sensitive prompts. However, these different sources of influence on the data do not guarantee our models are aligned to the preferences of any broader group.

We conducted two experiments to investigate this. First, we evaluate GPT‑3 and InstructGPT using held-out labelers[E](https://openai.com/index/instruction-following/#citation-bottom-E)who did not produce any of the training data, and found that these labelers prefer outputs from the InstructGPT models at about the same rate as our training labelers. Second, we train reward models on data from a subset of our labelers, and find that they generalize well to predicting the preferences of a different subset of labelers. This suggests that our models haven’t solely overfit to the preferences of our training labelers. However, more work is needed to study how these models perform on broader groups of users, and how they perform on inputs where humans disagree about the desired behavior.

## Limitations

Despite making significant progress, our InstructGPT models are far from fully aligned or fully safe; they still generate toxic or biased outputs, make up facts, and generate sexual and violent content without explicit prompting. But the safety of a machine learning system depends not only on the behavior of the underlying models, but also on how these models are deployed. To support the safety of our API, we will continue to[review potential applications⁠(opens in a new window)](https://beta.openai.com/docs/usage-guidelines/use-case-guidelines)before they go live, provide content filters for detecting unsafe completions, and monitor for misuse.

A byproduct of training our models to follow user instructions is that they may become more susceptible to misuse if instructed to produce unsafe outputs. Solving this requires our models to refuse certain instructions; doing this reliably is an important open research problem that we are excited to tackle.

Further, in many cases aligning to the average labeler preference may not be desirable. For example, when generating text that disproportionately affects a minority group, the preferences of that group should be weighted more heavily. Right now, InstructGPT is trained to follow instructions in English; thus, it is biased towards the cultural values of English-speaking people. We are conducting research into understanding the differences and disagreements between labelers’ preferences so we can condition our models on the values of more specific populations. More generally, aligning model outputs to the values of specific humans introduces difficult choices with societal implications, and ultimately we must establish responsible, inclusive processes for making these decisions.

## Next steps

This is the first application of our alignment research to our product. Our results show that these techniques are effective at significantly improving the alignment of general-purpose AI systems with human intentions. However, this is just the beginning: we will keep pushing these techniques to improve the alignment of our current and future models towards language tools that are safe and helpful to humans.

_If you’re interested in these research directions,_[_we’re hiring_⁠(opens in a new window)](https://boards.greenhouse.io/openai/jobs/4050138004)_!_

*   [GPT](https://openai.com/research/index/?tags=gpt)
*   [Language](https://openai.com/research/index/?tags=language)

## Footnotes

1.   A
We only use prompts submitted through the Playground to an earlier version of the InstructGPT models that was deployed in January 2021. Our human annotators remove personal identifiable information from all prompts before adding it to the training set.

2.   B
The InstructGPT models deployed in the API are updated versions trained using the same human feedback data. They use a similar but slightly different training method that we will describe in a forthcoming publication.

3.   C
We also measure several other dimensions of potentially harmful outputs on our API distribution: whether the outputs contain sexual or violent content, denigrate a protected class, or encourage abuse. We find that InstructGPT doesn’t improve significantly over GPT-3 on these metrics; the incidence rate is equally low for both models.

4.   D
We found this approach more effective than simply increasing the KL coefficient.

5.   E
These labelers are sourced from Scale AI and Upwork, similarly to our training labelers, but do not undergo a screening test.

## References

1.   1
Christiano, P., Leike, J., Brown, T.B., Martic, M., Legg, S. and Amodei, D., 2017. Deep reinforcement learning from human preferences. arXiv preprint arXiv:1706.03741.

2.   2
Stiennon, N., Ouyang, L., Wu, J., Ziegler, D.M., Lowe, R., Voss, C., Radford, A., Amodei, D. and Christiano, P.,2020.

3.   3
Wu, J., Ouyang, L., Ziegler, D.M., Stiennon, N., Lowe, R., Leike, J. and Christiano, P., 2021. Recursively summarizing books with human feedback. arXiv preprint arXiv:2109.10862.

4.   4
Wei, J., Bosma, M., Zhao, V.Y., Guu, K., Yu, A.W., Lester, B., Du, N., Dai, A.M. and Le, Q.V., 2021. Finetuned language models are zero-shot learners. arXiv preprint arXiv:2109.01652.

5.   5
Sanh, V., Webson, A., Raffel, C., Bach, S.H., Sutawika, L., Alyafeai, Z., Chaffin, A., Stiegler, A., Scao, T.L., Raja, A. and Dey, M., 2021. Multitask prompted training enables zero-shot task generalization. arXiv preprint arXiv:2110.08207.

6.   6
Bender, E.M., Gebru, T., McMillan-Major, A. and Shmitchell, S., 2021, March. On the Dangers of Stochastic Parrots: Can Language Models Be Too Big?🦜. In Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency (pp.610-623).

7.   7
Bommasani, R., Hudson, D.A., Adeli, E., Altman, R., Arora, S., von Arx, S., Bernstein, M.S., Bohg, J., Bosselut, A., Brunskill, E. and Brynjolfsson, E., 2021. On the opportunities and risks of foundation models. arXiv preprint arXiv:2108.07258.

8.   8
Kenton, Z., Everitt, T., Weidinger, L., Gabriel, I., Mikulik, V. and Irving, G., 2021. Alignment of Language Agents. arXiv preprint arXiv:2103.14659.

9.   9
Weidinger, L., Mellor, J., Rauh, M., Griffin, C., Uesato, J., Huang, P.S., Cheng, M., Glaese, M., Balle, B., Kasirzadeh, A. and Kenton, Z., 2021. Ethical and social risks of harm from Language Models. arXiv preprint arXiv:2112.04359.

10.   10
Tamkin, A., Brundage, M., Clark, J. and Ganguli, D., 2021. Understanding the Capabilities, Limitations, and Societal Impact of Large Language Models. arXiv preprint arXiv:2102.02503.

11.   11
Solaiman, I. and Dennison, C., 2021. Process for Adapting Language Models to Society (PALMS) with Values-Targeted Datasets. arXiv preprint arXiv:2106.10328.

12.   12
Ngo, H., Raterink, C., Araújo, J.G., Zhang, I., Chen, C., Morisot, A. and Frosst, N., 2021. Mitigating harm in language models with conditional-likelihood filtration. arXiv preprint arXiv:2108.07790.

13.   13
Xu, J., Ju, D., Li, M., Boureau, Y.L., Weston, J. and Dinan, E., 2020. Recipes for safety in open-domain chatbots. arXiv preprint arXiv:2010.07079.

14.   14
Keskar, N.S., McCann, B., Varshney, L.R., Xiong, C. and Socher, R., 2019. Ctrl: A conditional transformer language model for controllable generation. arXiv preprint arXiv:1909.05858.

15.   15
Krause, B., Gotmare, A.D., McCann, B., Keskar, N.S., Joty, S., Socher, R. and Rajani, N.F., 2020. Gedi: Generative discriminator guided sequence generation. arXiv preprint arXiv:2009.06367.

16.   16
Dathathri, S., Madotto, A., Lan, J., Hung, J., Frank, E., Molino, P., Yosinski, J. and Liu, R., 2019. Plug and play language models: A simple approach to controlled text generation. arXiv preprint arXiv:1912.02164.

17.   17
Lin, S., Hilton, J. and Evans, O., 2021. TruthfulQA: Measuring how models mimic human falsehoods. arXiv preprint arXiv:2109.07958.

18.   18
Gehman, S., Gururangan, S., Sap, M., Choi, Y. and Smith, N.A., 2020. RealToxicityPrompts: Evaluating neural toxic degeneration in language models. arXiv preprint arXiv:2009.11462.

19.   19
Rudinger, R., Naradowsky, J., Leonard, B. and Van Durme, B., 2018. Gender bias in coreference resolution. arXiv preprint arXiv:1804.09301.

20.   20
Nangia, N., Vania, C., Bhalerao, R. and Bowman, S.R., 2020. CrowS-pairs: A challenge dataset for measuring social biases in masked language models. arXiv preprint arXiv:2010.00133.

## Authors

Ryan Lowe, Jan Leike

## Acknowledgments

We’d like to thank our paper co-authors: Long Ouyang, Jeff Wu, Roger Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, and Paul Christiano, along with everyone who provided feedback on the paper and blog post. We’d also like to thank the Comms team for their guidance and assistance, including Steve Dowling, Hannah Wong, Elie Georges, Alper Ercetin, Jared Salzano, Allan Diego, and Justin Jay Wang. Finally, we’d like to thank our labelers, without whom this project would not have been possible.

## Related articles

[View all](https://openai.com/news/)


[Disrupting malicious uses of AI by state-affiliated threat actors Security Feb 14, 2024](https://openai.com/index/disrupting-malicious-uses-of-ai-by-state-affiliated-threat-actors/)

![Image 3](https://images.ctfassets.net/kftzwdyauwt9/ec66425e-99ca-4314-d04b087f8727/de7341b6a5281c2a220b93a737ce19b0/building-an-early-warning-system-for-llm-aided-biological-threat-creation.jpg?w=3840&q=90&fm=webp)

[Building an early warning system for LLM-aided biological threat creation Publication Jan 31, 2024](https://openai.com/index/building-an-early-warning-system-for-llm-aided-biological-threat-creation/)


[Democratic inputs to AI grant program: lessons learned and implementation plans Safety Jan 16, 2024](https://openai.com/index/democratic-inputs-to-ai-grant-program-update/)

Our Research
*   [Research Index](https://openai.com/research/index/)
*   [Research Overview](https://openai.com/research/)
*   [Research Residency](https://openai.com/residency/)
*   [OpenAI for Science](https://openai.com/science/)
*   [Economic Research](https://openai.com/signals/)

Latest Advancements
*   [GPT-5.3 Instant](https://openai.com/index/gpt-5-3-instant/)
*   [GPT-5.3-Codex](https://openai.com/index/introducing-gpt-5-3-codex/)
*   [GPT-5](https://openai.com/gpt-5/)
*   [Codex](https://openai.com/index/introducing-gpt-5-3-codex/)

Safety
*   [Safety Approach](https://openai.com/safety/)
*   [Security & Privacy](https://openai.com/security-and-privacy/)
*   [Trust & Transparency](https://openai.com/trust-and-transparency/)

ChatGPT
*   [Explore ChatGPT(opens in a new window)](https://chatgpt.com/overview)
*   [Business](https://chatgpt.com/business/business-plan)
*   [Enterprise](https://chatgpt.com/business/enterprise)
*   [Education](https://chatgpt.com/business/education)
*   [Pricing(opens in a new window)](https://chatgpt.com/pricing)
*   [Download(opens in a new window)](https://chatgpt.com/download)

Sora
*   [Sora Overview](https://openai.com/sora/)
*   [Features](https://openai.com/sora/#features)
*   [Pricing](https://openai.com/sora/#pricing)
*   [Sora log in(opens in a new window)](https://sora.com/)

API Platform
*   [Platform Overview](https://openai.com/api/)
*   [Pricing](https://openai.com/api/pricing/)
*   [API log in(opens in a new window)](https://platform.openai.com/login)
*   [Documentation(opens in a new window)](https://developers.openai.com/api/docs)
*   [Developer Forum(opens in a new window)](https://community.openai.com/)

For Business
*   [Business Overview](https://openai.com/business/)
*   [Solutions](https://openai.com/solutions/)
*   [Contact Sales](https://openai.com/contact-sales/)

Company
*   [About Us](https://openai.com/about/)
*   [Our Charter](https://openai.com/charter/)
*   [Foundation(opens in a new window)](https://openaifoundation.org/)
*   [Careers](https://openai.com/careers/)
*   [Brand](https://openai.com/brand/)

Support
*   [Help Center(opens in a new window)](https://help.openai.com/)

More
*   [News](https://openai.com/news/)
*   [Stories](https://openai.com/stories/)
*   [Livestreams](https://openai.com/live/)
*   [Podcast](https://openai.com/podcast/)
*   [RSS](https://openai.com/news/rss.xml)

Terms & Policies
*   [Terms of Use](https://openai.com/policies/terms-of-use/)
*   [Other Policies](https://openai.com/policies/)

[(opens in a new window)](https://x.com/OpenAI)[(opens in a new window)](https://www.youtube.com/OpenAI)[(opens in a new window)](https://www.linkedin.com/company/openai)[(opens in a new window)](https://github.com/openai)[(opens in a new window)](https://www.instagram.com/openai/)[(opens in a new window)](https://www.tiktok.com/@openai)[(opens in a new window)](https://discord.gg/openai)

OpenAI © 2015–2026 Manage Cookies

English United States