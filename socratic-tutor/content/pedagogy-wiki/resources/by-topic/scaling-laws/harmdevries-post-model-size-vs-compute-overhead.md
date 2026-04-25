# Source: https://www.harmdevries.com/post/model-size-vs-compute-overhead/
# Downloaded: 2026-04-06
# Words: 1785
# Author: Harm de Vries
# Author Slug: harm-de-vries
Go smol or go home
Why we should train smaller LLMs on more tokens
If you have access to a big compute cluster and are planning to train a Large Language Model (LLM), you will need to make a decision on how to allocate your compute budget. This involves selecting the number of model parameters $N$ and the number of training tokens $D$. By applying the [scaling](https://arxiv.org/abs/2001.08361) [laws](https://arxiv.org/abs/2203.15556), you can get guidance on how to reach the best model performance for your given compute budget, and find the optimal distribution of compute $C$ between the parameters $N_{opt}$ and training tokens $D_{opt}$.
However, for most use cases you should not train a compute-optimal LLM but instead spend some extra compute to obtain a smaller model. Smaller models not only make inference faster and cheaper, they are also much easier to use for developers and researchers with limited GPU resources. Although many LLM practitioners train their models on more tokens than the Chinchilla scaling laws suggest, not everyone is aware that scaling laws can assist in determining how much smaller models we can train and how much additional compute is required.
In this blogpost, I’ll show how to derive the trade-off between model size and compute overhead and reveal there is significant room to reduce the compute-optimal model size with minimal compute overhead. However, there comes a point where spending more compute resources leads to diminishing returns because you’ve hit the critical model size. The critical model size is essentially the minimum LLM capacity required to attain a specific loss level, and further reducing the model size beyond this point becomes near-impossible. My analysis suggest that the critical model size is around 30% of the Chinchilla optimal model and leads to a 100% compute overhead. Notably, recent models such as LLaMa-7B, which is trained on 1T tokens, are far from reaching the critical model size, indicating that there is ample room to train “smaller” LLMs for longer.
Recap of Chinchilla scaling laws
In [Chinchilla’s third approach](https://arxiv.org/abs/2203.15556) to estimating the scaling laws, the authors argue that the loss can be modelled as a function of the parameter count and number of seen tokens:
$$L(N, D) = E + \frac{A}{N^{\alpha}} + \frac{B}{D^{\beta}}$$
The authors fitted the parameters on a series of experiments with various model sizes and training tokens and found the following parameter estimates:
$$E=1.69, A=406.4, B=410.7, \alpha=0.32, \beta=0.28.$$
By optimizing this loss function $L$ under the constraint that the compute budget $C = 6ND$, you can show that the compute-optimal number of parameters $N_{opt}$ and compute-optimal number of tokens $D_{opt}$ follow a power law: $$N_{opt}(C) = G\left(\frac{C}{6}\right)^{\frac{\beta}{\alpha+\beta}}, D_{opt}(C) = G^{-1}\left(\frac{C}{6}\right)^{\frac{\alpha}{\alpha+\beta}}, G = \left(\frac{\alpha A}{\beta B}\right)^{\frac{1}{\alpha+\beta}}$$
Model size vs compute overhead
Suppose we reduce the optimal model size $N_{opt}$ by half. How much do we need to increase the training tokens to obtain the same model loss? To keep the same compute budget, we must double the number of training tokens $D_{opt}$ but we should expect some compute overhead and train for longer than that.
We can return to Chinchilla’s parameteric loss function to answer this question. We are looking to scale the parameters by $k_N$ and training tokens by $k_D$ while reaching the same loss as $L(N_{opt}, D_{opt})$. More precisely, we are looking to satisfy the following equation: $$L(N_{opt}, D_{opt}) = L(k_N N_{opt}, k_D D_{opt})$$ $$E + \frac{A}{N_{opt}^{\alpha}} + \frac{B}{D_{opt}^{\beta}} = E + \frac{A}{\left(k_N N_{opt}\right)^{\alpha}} + \frac{B}{\left(k_D D_{opt}\right)^{\beta}}$$
With a few mathematical steps, you find that:
$$k_D= \left(1 - (k_N^{-\alpha} - 1) \frac{A N_{opt}^{-\alpha}}{B D_{opt}^{-\beta}}\right)^{\frac{1}{-\beta}}$$
Once we found the data scaling factor $k_D$, we can determine the new compute budget $$C_{new} = 6 (k_N N_{opt}) (k_D D_{opt})$$ as well as the compute overhead $$C_{overhead} = \frac{C_{new} - C}{C}*100.$$
Interestingly, as I’ll show [below](#invariancetoC), the data scaling factor $k_D$ is independent of the compute budget $C$. The resulting model-size vs compute overhead trade-off is therefore identical across all compute budgets.
Note: Fig 12 in the [original scaling laws paper](https://arxiv.org/abs/2001.08361) shows a similar plot.
The critical model size
As depicted in the graph, there exists a substantial region where you can reduce the optimal model size with minimal compute overhead. For example, the compute overhead for 75% of the optimal model size is only 2.8%, whereas for half of the optimal model size, the overhead rises to 20%. As we move towards smaller models, we observe an asymptotic trend, and at 25% of the compute-optimal model size, the compute overhead increases rapidly to 188%.
Deciding where to position oneself on this curve relies on how often you’re going to run inference. If you never run inference, you should go with Chinchilla. If you run inference occasionally, you should take a slightly smaller model and in the limit (running inference infinitely often), you should take the smallest model possible (i.e. with infinite compute overhead).
However, while the analysis predicts that you can continue to reduce the model size, in practice you’ll likely hit the critical model size. Essentially, the critical model size is the minimal LLM capacity required to reach a particular loss level, and further reducing the model size beyond this point is near-impossible. Based on my analysis, I estimate that the critical model size is around 30% of the Chinchilla optimal model and incurs a 100% overhead. Note that you shouldn’t think of the critical model size as a hard threshold but more like a region where you can expect diminishing returns. If you’re not looking for the smallest possible model, you can always opt to be more conservative and select a model size within 40-60% of the compute-optimal model size and expect a 10-42% compute overhead.
LLaMA-7B and SantaCoder
A number of recent models, such as [LLaMA-7B](https://arxiv.org/abs/2302.13971) and [SantaCoder](https://arxiv.org/abs/2301.03988), are trained for longer than what the Chinchilla scaling laws suggest. How much compute are they trading for a smaller model size?
Let’s look at LLaMA-7B first.
- With 6.9B parameters and 1000B tokens, the total compute budget is 4.14e22 FLOP.
- The compute-optimal model for this compute budget has roughly 12.52B parameters and is trained on 550B tokens.
- We can look which scaling factor $k_N$ gets “close” to LLaMA-7B’s parameters and trainings tokens. We find that $k_N$=0.57 leads to a reasonable fit with $7.13$B parameters and 1088B training tokens.
- Compute overhead is roughly $12$%.
Now consider SantaCoder.
- With 1.1B parameter model and 236B training tokens, the total compute budget is 1.56e21 FLOP.
- The compute-optimal model for this budget has roughly 2.79B parameters and is trained on 93B tokens.
- It’s harder to find a good fit for the SantaCoder, but with $k_N$=0.46 we would train a 1.29B parameter model on 258B tokens.
- Compute overhead is roughly $24$%.
SantaCoder further reduces the model size than LLaMA-7B but, according to the Chinchilla scaling laws, these models can further trade-off compute for a smaller model size.
Training tokens for various $k_N$
To give you a better sense of which model sizes and number of training tokens fall within a reasonable range of the model-size vs compute trade-off, I’ve updated Table A3 of the Chinchilla paper with predictions for $k_N=0.5$ and $k_N=0.3$. I only report the third approach for estimating the Chinchilla compute-optimal models, which is already the one that predicts the smallest model size and largest number of training tokens.
| $k_N=1$ | $k_N=0.5$ | $k_N=0.3$ | ||||
|---|---|---|---|---|---|---|
| C | N | D | N | D | N | D |
| 2.21e+19 | 0.40 B | 9.22 B | 0.20 B | 22.28 B | 0.12 B | 63.20 B |
| 1.62e+20 | 0.99 B | 27.20 B | 0.50 B | 65.70 B | 0.30 B | 186.35 B |
| 2.46e+22 | 9.87 B | 415.53 B | 4.93 B | 1003.77 B | 2.96 B | 2847.27 B |
| 1e+23 | 18.73 B | 889.63 B | 9.37 B | 2149.02 B | 5.62 B | 6095.86 B |
| 1.71e+24 | 68.60 B | 4154.24 B | 34.30 B | 10035.16 B | 20.58 B | 28465.50 B |
- At $k_N=0.5$, it suggest to train a 5B parameter model on 1 trillion tokens and a 9B parameter model on 2.1 trillion tokens.
- At $k_N=0.3$, it suggest to train a 3B parameter model on 2.8 trillion tokens and a 6B parameter model on over 6.1 trillion tokens.
- The authors likely rounded the reported $\alpha$ and $\beta$ parameters in the paper so I slightly changed $\alpha=0.336$ and $\beta=0.283$ to better fit the scaling law predictions with table A3. I kept $A=406.4$, $B=410.7$, $E=1.62$.
- Note that the Chinchilla coefficients depend on the dataset (which is not known to us) and that the results may change for other training data.
Limitations
- Are chinchilla scaling laws accurate? They are sensitive to small changes in the parameter estimates and are not fitted on the small-model-long-training regime.
- Even if smaller models are reaching the same perplexity, it’s unclear whether this leads to the same model capabilities (e.g. zero-shot prompting performance).
- Training smaller models for longer might be harder to efficiently parallelize on HPC clusters.
Conclusion
The Chinchilla scaling laws suggest we haven’t reached the limit of training smaller models on more tokens. With the amazing speed of innovation in the open-source AI community, I expect small and capable LLMs to arrive soon!
If you want to further explore these concepts yourself, please check out this [research notebook](https://github.com/bigcode-project/bigcode-analysis/pull/36).
Acknowledgement
This analysis was the result of discussions in the [BigCode](https://www.bigcode-project.org) training working group. Thanks to everyone who participated in these discussions, especially Raymond Li, Joel Lamy Poirier, Denis Kocetkov, Leandro von Werra, Loubna Ben Allal, Evgenii Zheltonozhskii, Niklas Muennighoff, Dzmitry Bahdanau, and Thomas Wolf. Credit to Leandro for the title suggestion and thanks to Niklas for giving permission to use his explanation for describing the model-size vs compute overhead curve in terms of how often you want run inference.
Citation
If you would like to cite this post in an academic context, you can use this BibTeX entry:
@misc{devries2023chinchilla_analysis,
author = {De Vries, Harm},
title = {Go smol or go home},
url = {https://www.harmdevries.com/post/model-size-vs-compute-overhead/},
year = {2023}
}
Appendix
Scaling factors $k_N$, $k_D$ are invariant to compute budget C
While the data scaling factor $k_D$ is expressed in terms of the compute-optimal parameters $N_{opt}$ and training tokens $D_{opt}$, I’ll show in this section that the solution is invariant to the compute budget $C$. Let’s start from $$k_D= \left(1 - (k_N^{-\alpha} - 1) \frac{A N_{opt}^{-\alpha}}{B D_{opt}^{-\beta}}\right)^{\frac{1}{-\beta}}$$ and zoom in on the part that depends on compute budget $C$: $$\frac{N_{opt}^{-\alpha}}{D_{opt}^{-\beta}}.$$
Let’s plug $N_{opt}=G\left(\frac{C}{6}\right)^{\frac{\beta}{\alpha+\beta}}$ and $D_{opt}(C) = G^{-1}\left(\frac{C}{6}\right)^{\frac{\alpha}{\alpha+\beta}}$ into this formula: $$\frac{\left(G\left(\frac{C}{6}\right)^{\frac{\beta}{\alpha+\beta}}\right)^{-\alpha}}{\left( G^{-1}\left(\frac{C}{6}\right)^{\frac{\alpha}{\alpha+\beta}}\right)^{-\beta}}.$$ By pushing the outer exponents in, we can see $C$ cancels $$\frac{G^{-\alpha}\left(\frac{C}{6}\right)^{\frac{-\alpha\beta}{\alpha+\beta}}}{G^{\beta}\left(\frac{C}{6}\right)^{\frac{-\alpha\beta}{\alpha+\beta}}}$$ and simplifies to $G^{-\alpha} G^{-\beta}$.