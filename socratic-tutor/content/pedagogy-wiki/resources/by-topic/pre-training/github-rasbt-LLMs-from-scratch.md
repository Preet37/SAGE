# Source: https://github.com/rasbt/LLMs-from-scratch
# Author: Sebastian Raschka
# Author Slug: sebastian-raschka
# Downloaded: 2026-04-06
# Words: 1083
This repository contains the code for developing, pretraining, and finetuning a GPT-like LLM and is the official code repository for the book [Build a Large Language Model (From Scratch)](https://amzn.to/4fqvn0D).
In [Build a Large Language Model (From Scratch)](http://mng.bz/orYv), you'll learn and understand how large language models (LLMs) work from the inside out by coding them from the ground up, step by step. In this book, I'll guide you through creating your own LLM, explaining each stage with clear text, diagrams, and examples.
The method described in this book for training and developing your own small-but-functional model for educational purposes mirrors the approach used in creating large-scale foundational models such as those behind ChatGPT. In addition, this book includes code for loading the weights of larger pretrained models for finetuning.
- Link to the official
[source code repository](https://github.com/rasbt/LLMs-from-scratch) [Link to the book at Manning (the publisher's website)](http://mng.bz/orYv)[Link to the book page on Amazon.com](https://www.amazon.com/gp/product/1633437167)- ISBN 9781633437166
To download a copy of this repository, click on the [Download ZIP](https://github.com/rasbt/LLMs-from-scratch/archive/refs/heads/main.zip) button or execute the following command in your terminal:
git clone --depth 1 https://github.com/rasbt/LLMs-from-scratch.git
(If you downloaded the code bundle from the Manning website, please consider visiting the official code repository on GitHub at [https://github.com/rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) for the latest updates.)
Please note that this README.md
file is a Markdown (.md
) file. If you have downloaded this code bundle from the Manning website and are viewing it on your local computer, I recommend using a Markdown editor or previewer for proper viewing. If you haven't installed a Markdown editor yet, [Ghostwriter](https://ghostwriter.kde.org) is a good free option.
You can alternatively view this and other files on GitHub at [https://github.com/rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) in your browser, which renders Markdown automatically.
Tip: If you're seeking guidance on installing Python and Python packages and setting up your code environment, I suggest reading the
[README.md]file located in the[setup]directory.
| Chapter Title | Main Code (for Quick Access) | All Code + Supplementary |
|---|---|---|
|
[ch02.ipynb](/rasbt/LLMs-from-scratch/blob/main/ch02/01_main-chapter-code/ch02.ipynb)-
[dataloader.ipynb](/rasbt/LLMs-from-scratch/blob/main/ch02/01_main-chapter-code/dataloader.ipynb)(summary)-
[exercise-solutions.ipynb](/rasbt/LLMs-from-scratch/blob/main/ch02/01_main-chapter-code/exercise-solutions.ipynb)[./ch02](/rasbt/LLMs-from-scratch/blob/main/ch02)[ch03.ipynb](/rasbt/LLMs-from-scratch/blob/main/ch03/01_main-chapter-code/ch03.ipynb)-
[multihead-attention.ipynb](/rasbt/LLMs-from-scratch/blob/main/ch03/01_main-chapter-code/multihead-attention.ipynb)(summary)-
[exercise-solutions.ipynb](/rasbt/LLMs-from-scratch/blob/main/ch03/01_main-chapter-code/exercise-solutions.ipynb)[./ch03](/rasbt/LLMs-from-scratch/blob/main/ch03)[ch04.ipynb](/rasbt/LLMs-from-scratch/blob/main/ch04/01_main-chapter-code/ch04.ipynb)-
[gpt.py](/rasbt/LLMs-from-scratch/blob/main/ch04/01_main-chapter-code/gpt.py)(summary)-
[exercise-solutions.ipynb](/rasbt/LLMs-from-scratch/blob/main/ch04/01_main-chapter-code/exercise-solutions.ipynb)[./ch04](/rasbt/LLMs-from-scratch/blob/main/ch04)[ch05.ipynb](/rasbt/LLMs-from-scratch/blob/main/ch05/01_main-chapter-code/ch05.ipynb)-
[gpt_train.py](/rasbt/LLMs-from-scratch/blob/main/ch05/01_main-chapter-code/gpt_train.py)(summary)-
[gpt_generate.py](/rasbt/LLMs-from-scratch/blob/main/ch05/01_main-chapter-code/gpt_generate.py)(summary)-
[exercise-solutions.ipynb](/rasbt/LLMs-from-scratch/blob/main/ch05/01_main-chapter-code/exercise-solutions.ipynb)[./ch05](/rasbt/LLMs-from-scratch/blob/main/ch05)[ch06.ipynb](/rasbt/LLMs-from-scratch/blob/main/ch06/01_main-chapter-code/ch06.ipynb)-
[gpt_class_finetune.py](/rasbt/LLMs-from-scratch/blob/main/ch06/01_main-chapter-code/gpt_class_finetune.py)-
[exercise-solutions.ipynb](/rasbt/LLMs-from-scratch/blob/main/ch06/01_main-chapter-code/exercise-solutions.ipynb)[./ch06](/rasbt/LLMs-from-scratch/blob/main/ch06)[ch07.ipynb](/rasbt/LLMs-from-scratch/blob/main/ch07/01_main-chapter-code/ch07.ipynb)-
[gpt_instruction_finetuning.py](/rasbt/LLMs-from-scratch/blob/main/ch07/01_main-chapter-code/gpt_instruction_finetuning.py)(summary)-
[ollama_evaluate.py](/rasbt/LLMs-from-scratch/blob/main/ch07/01_main-chapter-code/ollama_evaluate.py)(summary)-
[exercise-solutions.ipynb](/rasbt/LLMs-from-scratch/blob/main/ch07/01_main-chapter-code/exercise-solutions.ipynb)[./ch07](/rasbt/LLMs-from-scratch/blob/main/ch07)[code-part1.ipynb](/rasbt/LLMs-from-scratch/blob/main/appendix-A/01_main-chapter-code/code-part1.ipynb)-
[code-part2.ipynb](/rasbt/LLMs-from-scratch/blob/main/appendix-A/01_main-chapter-code/code-part2.ipynb)-
[DDP-script.py](/rasbt/LLMs-from-scratch/blob/main/appendix-A/01_main-chapter-code/DDP-script.py)-
[exercise-solutions.ipynb](/rasbt/LLMs-from-scratch/blob/main/appendix-A/01_main-chapter-code/exercise-solutions.ipynb)[./appendix-A](/rasbt/LLMs-from-scratch/blob/main/appendix-A)[./appendix-B](/rasbt/LLMs-from-scratch/blob/main/appendix-B)[list of exercise solutions](/rasbt/LLMs-from-scratch/blob/main/appendix-C)[./appendix-C](/rasbt/LLMs-from-scratch/blob/main/appendix-C)[appendix-D.ipynb](/rasbt/LLMs-from-scratch/blob/main/appendix-D/01_main-chapter-code/appendix-D.ipynb)[./appendix-D](/rasbt/LLMs-from-scratch/blob/main/appendix-D)[appendix-E.ipynb](/rasbt/LLMs-from-scratch/blob/main/appendix-E/01_main-chapter-code/appendix-E.ipynb)[./appendix-E](/rasbt/LLMs-from-scratch/blob/main/appendix-E)The mental model below summarizes the contents covered in this book.
The most important prerequisite is a strong foundation in Python programming. With this knowledge, you will be well prepared to explore the fascinating world of LLMs and understand the concepts and code examples presented in this book.
If you have some experience with deep neural networks, you may find certain concepts more familiar, as LLMs are built upon these architectures.
This book uses PyTorch to implement the code from scratch without using any external LLM libraries. While proficiency in PyTorch is not a prerequisite, familiarity with PyTorch basics is certainly useful. If you are new to PyTorch, Appendix A provides a concise introduction to PyTorch. Alternatively, you may find my book, [PyTorch in One Hour: From Tensors to Training Neural Networks on Multiple GPUs](https://sebastianraschka.com/teaching/pytorch-1h/), helpful for learning about the essentials.
The code in the main chapters of this book is designed to run on conventional laptops within a reasonable timeframe and does not require specialized hardware. This approach ensures that a wide audience can engage with the material. Additionally, the code automatically utilizes GPUs if they are available. (Please see the [setup](https://github.com/rasbt/LLMs-from-scratch/blob/main/setup/README.md) doc for additional recommendations.)
[A 17-hour and 15-minute companion video course](https://www.manning.com/livevideo/master-and-build-large-language-models) where I code through each chapter of the book. The course is organized into chapters and sections that mirror the book's structure so that it can be used as a standalone alternative to the book or complementary code-along resource.
[Build A Reasoning Model (From Scratch)](https://mng.bz/lZ5B), while a standalone book, can be considered as a sequel to Build A Large Language Model (From Scratch).
It starts with a pretrained model and implements different reasoning approaches, including inference-time scaling, reinforcement learning, and distillation, to improve the model's reasoning capabilities.
Similar to Build A Large Language Model (From Scratch), [Build A Reasoning Model (From Scratch)](https://mng.bz/lZ5B) takes a hands-on approach implementing these methods from scratch.
- Amazon link (TBD)
[Manning link](https://mng.bz/lZ5B)[GitHub repository](https://github.com/rasbt/reasoning-from-scratch)
Each chapter of the book includes several exercises. The solutions are summarized in Appendix C, and the corresponding code notebooks are available in the main chapter folders of this repository (for example, [./ch02/01_main-chapter-code/exercise-solutions.ipynb](/rasbt/LLMs-from-scratch/blob/main/ch02/01_main-chapter-code/exercise-solutions.ipynb).
In addition to the code exercises, you can download a free 170-page PDF titled [Test Yourself On Build a Large Language Model (From Scratch)](https://www.manning.com/books/test-yourself-on-build-a-large-language-model-from-scratch) from the Manning website. It contains approximately 30 quiz questions and solutions per chapter to help you test your understanding.
Several folders contain optional materials as a bonus for interested readers:
-
Setup
-
Chapter 2: Working With Text Data
-
Chapter 3: Coding Attention Mechanisms
-
Chapter 4: Implementing a GPT Model From Scratch
-
Chapter 5: Pretraining on Unlabeled Data
[Alternative Weight Loading Methods](/rasbt/LLMs-from-scratch/blob/main/ch05/02_alternative_weight_loading)[Pretraining GPT on the Project Gutenberg Dataset](/rasbt/LLMs-from-scratch/blob/main/ch05/03_bonus_pretraining_on_gutenberg)[Adding Bells and Whistles to the Training Loop](/rasbt/LLMs-from-scratch/blob/main/ch05/04_learning_rate_schedulers)[Optimizing Hyperparameters for Pretraining](/rasbt/LLMs-from-scratch/blob/main/ch05/05_bonus_hparam_tuning)[Building a User Interface to Interact With the Pretrained LLM](/rasbt/LLMs-from-scratch/blob/main/ch05/06_user_interface)[Converting GPT to Llama](/rasbt/LLMs-from-scratch/blob/main/ch05/07_gpt_to_llama)[Memory-efficient Model Weight Loading](/rasbt/LLMs-from-scratch/blob/main/ch05/08_memory_efficient_weight_loading/memory-efficient-state-dict.ipynb)[Extending the Tiktoken BPE Tokenizer with New Tokens](/rasbt/LLMs-from-scratch/blob/main/ch05/09_extending-tokenizers/extend-tiktoken.ipynb)[PyTorch Performance Tips for Faster LLM Training](/rasbt/LLMs-from-scratch/blob/main/ch05/10_llm-training-speed)[LLM Architectures](/rasbt/LLMs-from-scratch/blob/main/ch05/#llm-architectures-from-scratch)[Chapter 5 with other LLMs as Drop-In Replacement (e.g., Llama 3, Qwen 3)](/rasbt/LLMs-from-scratch/blob/main/ch05/14_ch05_with_other_llms)
-
Chapter 6: Finetuning for classification
-
Chapter 7: Finetuning to follow instructions
[Dataset Utilities for Finding Near Duplicates and Creating Passive Voice Entries](/rasbt/LLMs-from-scratch/blob/main/ch07/02_dataset-utilities)[Evaluating Instruction Responses Using the OpenAI API and Ollama](/rasbt/LLMs-from-scratch/blob/main/ch07/03_model-evaluation)[Generating a Dataset for Instruction Finetuning](/rasbt/LLMs-from-scratch/blob/main/ch07/05_dataset-generation/llama3-ollama.ipynb)[Improving a Dataset for Instruction Finetuning](/rasbt/LLMs-from-scratch/blob/main/ch07/05_dataset-generation/reflection-gpt4.ipynb)[Generating a Preference Dataset With Llama 3.1 70B and Ollama](/rasbt/LLMs-from-scratch/blob/main/ch07/04_preference-tuning-with-dpo/create-preference-data-ollama.ipynb)[Direct Preference Optimization (DPO) for LLM Alignment](/rasbt/LLMs-from-scratch/blob/main/ch07/04_preference-tuning-with-dpo/dpo-from-scratch.ipynb)[Building a User Interface to Interact With the Instruction-Finetuned GPT Model](/rasbt/LLMs-from-scratch/blob/main/ch07/06_user_interface)
More bonus material from the [Reasoning From Scratch](https://github.com/rasbt/reasoning-from-scratch) repository:
-
Qwen3 (From Scratch) Basics
-
Evaluation
-
Inference Scaling
-
Reinforcement Learning (RL)
I welcome all sorts of feedback, best shared via the [Manning Forum](https://livebook.manning.com/forum?product=raschka&page=1) or [GitHub Discussions](https://github.com/rasbt/LLMs-from-scratch/discussions). Likewise, if you have any questions or just want to bounce ideas off others, please don't hesitate to post these in the forum as well.
Please note that since this repository contains the code corresponding to a print book, I currently cannot accept contributions that would extend the contents of the main chapter code, as it would introduce deviations from the physical book. Keeping it consistent helps ensure a smooth experience for everyone.
If you find this book or code useful for your research, please consider citing it.
Chicago-style citation:
Raschka, Sebastian. Build A Large Language Model (From Scratch). Manning, 2024. ISBN: 978-1633437166.
BibTeX entry:
@book{build-llms-from-scratch-book,
author = {Sebastian Raschka},
title = {Build A Large Language Model (From Scratch)},
publisher = {Manning},
year = {2024},
isbn = {978-1633437166},
url = {https://www.manning.com/books/build-a-large-language-model-from-scratch},
github = {https://github.com/rasbt/LLMs-from-scratch}
}