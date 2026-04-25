# Source: https://discuss.huggingface.co/t/how-can-i-use-evaluates-perplexity-metric-on-a-model-thats-already-loaded/48564
# Title: How can I use evaluate's perplexity metric on a model that's already loaded?
# Fetched via: jina
# Date: 2026-04-09

Title: How can I use evaluate's perplexity metric on a model that's already loaded? - Intermediate - Hugging Face Forums



# How can I use evaluate's perplexity metric on a model that's already loaded? - Intermediate - Hugging Face Forums



Log In
*    ​ 

*   [Topics](https://discuss.huggingface.co/latest "All topics")
*    More 

 Categories 

*   [Beginners](https://discuss.huggingface.co/c/beginners/5 "Use this category for any basic question you have on any of the Hugging Face  library. Don’t moderate yourself, everyone has to begin somewhere and everyone on this forum is here to help!")
*   [Intermediate](https://discuss.huggingface.co/c/intermediate/6 "Use this category for any advanced question you have on any of the Hugging Face  library or to share/coordinate with other users your projects using them.")
*   [Course](https://discuss.huggingface.co/c/course/20 "Use this category to ask any question related to the course or organize study groups.")
*   [Research](https://discuss.huggingface.co/c/research/7 "Use this category for any research question or to coordinate on a project with other users.")
*   [Models](https://discuss.huggingface.co/c/models/13 "Use this category for any question specific to a given model: questions not really related to the library per se and more research-like such as tips to fine-tune/train, where to use/not to use etc.")
*   [All categories](https://discuss.huggingface.co/categories)

 ​ 

 ​ 

You can login using your [huggingface.co](https://huggingface.co/) credentials.

This forum is powered by [Discourse](https://www.discourse.org/) and relies on a [trust-level system](https://blog.discourse.org/2018/06/understanding-discourse-trust-levels/). As a new user, you’re temporarily limited in the number of topics and posts you can create. To lift those restrictions, just spend time reading other posts (to be precise, enter 5 topics, read through 30 posts and spend a total of 10 minutes reading).

Start with reading [this post](https://discuss.huggingface.co/t/how-to-ask-questions-on-the-forum/54). Then maybe someone already had that error that is bugging you check with a quick [search](https://discuss.huggingface.co/search). Or you can read the latest [awesome paper](http://discuss.huggingface.co/c/research/awesome-paper/) the team discussed.

# [How can I use evaluate’s perplexity metric on a model that’s already loaded?](https://discuss.huggingface.co/t/how-can-i-use-evaluates-perplexity-metric-on-a-model-thats-already-loaded/48564)

[Intermediate](https://discuss.huggingface.co/c/intermediate/6)

You have selected **0** posts.

[select all](https://discuss.huggingface.co/t/how-can-i-use-evaluates-perplexity-metric-on-a-model-thats-already-loaded/48564)

[cancel selecting](https://discuss.huggingface.co/t/how-can-i-use-evaluates-perplexity-metric-on-a-model-thats-already-loaded/48564)

## post by Imnimo on Jul 28, 2023

[![Image 3](https://avatars.discourse-cdn.com/v4/letter/i/ecb155/48.png)](https://discuss.huggingface.co/u/imnimo)

[Imnimo](https://discuss.huggingface.co/u/imnimo)

[Jul 2023](https://discuss.huggingface.co/t/how-can-i-use-evaluates-perplexity-metric-on-a-model-thats-already-loaded/48564 "Post date")

Following the example [here](https://huggingface.co/spaces/evaluate-metric/perplexity), I can create compute perplexity for a model I have previously saved like this:

```ini
perplexity = load("perplexity", module_type="metric")
results = perplexity.compute(predictions=dataset,model_id='my-saved-model')
```

But this only lets me specify a model_id, which is then loaded. I can’t do something like this:

```ini
model = AutoModelForCausalLM.from_pretrained('my-saved-model')
perplexity = load("perplexity", module_type="metric")
results = perplexity.compute(predictions=dataset,model_id=model)
```

Is there an alternative way to use evaluate’s perplexity metric that doesn’t require me to point to a saved model on disk?

For larger context, I’m trying to follow the quantization pipeline [here](https://huggingface.co/docs/optimum/intel/optimization_inc) and want to use perplexity as my criterion. But this requires computing perplexity on the model as it’s being updated in memory. If evaluate’s perplexity metric is not the correct tool for this job, is there something else I should be using?


+1

 1 

 ​ 

 ​ 

1.7k views 2 links 

Reply

### Related topics

Topic list, column headers with buttons are sortable.| Topic | Replies | Views | Activity |
| --- | --- | --- | --- |
| [Calculating Perplexity for Quantized Llama 3 8B & Mistral 7B Models: Evaluate Library vs. Custom Code?](https://discuss.huggingface.co/t/calculating-perplexity-for-quantized-llama-3-8b-mistral-7b-models-evaluate-library-vs-custom-code/145919) [Beginners](https://discuss.huggingface.co/c/beginners/5) | [3](https://discuss.huggingface.co/t/calculating-perplexity-for-quantized-llama-3-8b-mistral-7b-models-evaluate-library-vs-custom-code/145919/1) | 411 | [Mar 2025](https://discuss.huggingface.co/t/calculating-perplexity-for-quantized-llama-3-8b-mistral-7b-models-evaluate-library-vs-custom-code/145919/4) |
| [Useful compute_metrics functions for perplexity](https://discuss.huggingface.co/t/useful-compute-metrics-functions-for-perplexity/23805) [🤗Transformers](https://discuss.huggingface.co/c/transformers/9) | [0](https://discuss.huggingface.co/t/useful-compute-metrics-functions-for-perplexity/23805/1) | 682 | [Sep 2022](https://discuss.huggingface.co/t/useful-compute-metrics-functions-for-perplexity/23805/1) |
| [Using perplexity as metric during training](https://discuss.huggingface.co/t/using-perplexity-as-metric-during-training/42354) [Beginners](https://discuss.huggingface.co/c/beginners/5) | [0](https://discuss.huggingface.co/t/using-perplexity-as-metric-during-training/42354/1) | 1.7k | [Jun 2023](https://discuss.huggingface.co/t/using-perplexity-as-metric-during-training/42354/1) |
| [Log Perplexity using Trainer](https://discuss.huggingface.co/t/log-perplexity-using-trainer/4947) [🤗Transformers](https://discuss.huggingface.co/c/transformers/9) | [2](https://discuss.huggingface.co/t/log-perplexity-using-trainer/4947/1) | 2.1k | [Oct 2021](https://discuss.huggingface.co/t/log-perplexity-using-trainer/4947/3) |
| [Trainer.evaluate()](https://discuss.huggingface.co/t/trainer-evaluate/6107) [🤗Transformers](https://discuss.huggingface.co/c/transformers/9) | [3](https://discuss.huggingface.co/t/trainer-evaluate/6107/1) | 6.9k | [May 2021](https://discuss.huggingface.co/t/trainer-evaluate/6107/4) |

 Invalid date  Invalid date