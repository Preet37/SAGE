# Source: https://huggingface.co/docs/evaluate/index
# Author: Hugging Face
# Author Slug: hugging-face
# Downloaded: 2026-04-06
# Words: 533
Evaluate documentation
Evaluate on the Hub
Evaluate on the Hub
You can evaluate AI models on the Hub in multiple ways and this page will guide you through the different options:
- Community Leaderboards bring together the best models for a given task or domain and make them accessible to everyone by ranking them.
- Model Cards provide a comprehensive overview of a model’s capabilities from the author’s perspective.
- Libraries and Packages give you the tools to evaluate your models on the Hub.
Community Leaderboards
Community leaderboards show how a model performs on a given task or domain. For example, there are leaderboards for question answering, reasoning, classification, vision, and audio. If you’re tackling a new task, you can use a leaderboard to see how a model performs on it.
Here are some examples of community leaderboards:
| Leaderboard | Model Type | Description |
|---|---|---|
|
[GAIA](https://huggingface.co/spaces/gaia-benchmark/leaderboard)[the paper](https://arxiv.org/abs/2311.12983)for more details.)[OpenVLM Leaderboard](https://huggingface.co/spaces/opencompass/open_vlm_leaderboard)[Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard)[LLM-Perf Leaderboard](https://huggingface.co/spaces/llm-perf/leaderboard)There are many more leaderboards on the Hub. Check out all the leaderboards via this [search](https://huggingface.co/spaces?category=model-benchmarking) or use this [dedicated Space](https://huggingface.co/spaces/OpenEvals/find-a-leaderboard) to find a leaderboard for your task.
Model Cards
Model cards provide an overview of a model’s capabilities evaluated by the community or the model’s author. They are a great way to understand a model’s capabilities and limitations.
Unlike leaderboards, model card evaluation scores are often created by the author, rather than by the community.
For information on reporting results, see details on [the Model Card Evaluation Results metadata](https://huggingface.co/docs/hub/en/model-cards#evaluation-results).
Libraries and packages
There are a number of open-source libraries and packages that you can use to evaluate your models on the Hub. These are useful if you want to evaluate a custom model or performance on a custom evaluation task.
LightEval
LightEval is a library for evaluating LLMs. It is designed to be comprehensive and customizable. Visit the LightEval [repository](https://github.com/huggingface/lighteval) for more information.
For more recent evaluation approaches that are popular on the Hugging Face Hub that are currently more actively maintained, check out [LightEval](https://github.com/huggingface/lighteval).
🤗 Evaluate
A library for easily evaluating machine learning models and datasets.
With a single line of code, you get access to dozens of evaluation methods for different domains (NLP, Computer Vision, Reinforcement Learning, and more!). Be it on your local machine or in a distributed training setup, you can evaluate your models in a consistent and reproducible way!
Visit the 🤗 Evaluate [organization](https://huggingface.co/evaluate-metric) for a full list of available metrics. Each metric has a dedicated Space with an interactive demo for how to use the metric, and a documentation card detailing the metrics limitations and usage.
[Tutorials ](./installation)
Learn the basics and become familiar with loading, computing, and saving with 🤗 Evaluate. Start here if you are using 🤗 Evaluate for the first time!
[How-to guides ](./choosing_a_metric)
Practical guides to help you achieve a specific goal. Take a look at these guides to learn how to use 🤗 Evaluate to solve real-world problems.
[Conceptual guides ](./types_of_evaluations)
High-level explanations for building a better understanding of important topics such as considerations going into evaluating a model or dataset and the difference between metrics, measurements, and comparisons.
[Reference ](./package_reference/main_classes)
Technical descriptions of how 🤗 Evaluate classes and methods work.
[< > Update on GitHub](https://github.com/huggingface/evaluate/blob/main/docs/source/index.mdx)