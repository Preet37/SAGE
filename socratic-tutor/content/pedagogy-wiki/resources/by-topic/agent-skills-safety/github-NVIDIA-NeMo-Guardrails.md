# Source: https://github.com/NVIDIA/NeMo-Guardrails
# Author: NVIDIA
# Author Slug: nvidia
# Downloaded: 2026-04-06
# Words: 1862
LATEST RELEASE / DEVELOPMENT VERSION: The
[main]branch tracks the latest released beta version:[0.21.0]. For the latest development version, checkout the[develop]branch.
✨✨✨
📌 The official NeMo Guardrails documentation has moved to [docs.nvidia.com/nemo/guardrails](https://docs.nvidia.com/nemo/guardrails).
✨✨✨
NeMo Guardrails is an open-source toolkit for easily adding programmable guardrails to LLM-based conversational applications. Guardrails (or "rails" for short) are specific ways of controlling the output of a large language model, such as not talking about politics, responding in a particular way to specific user requests, following a predefined dialog path, using a particular language style, extracting structured data, and more.
[This paper](https://arxiv.org/abs/2310.10501) introduces NeMo Guardrails and contains a technical overview of the system and the current evaluation.
Python 3.10, 3.11, 3.12 or 3.13.
NeMo Guardrails uses [annoy](https://github.com/spotify/annoy) which is a C++ library with Python bindings. To install NeMo Guardrails you will need to have the C++ compiler and dev tools installed. Check out the [Installation Guide](https://docs.nvidia.com/nemo/guardrails/getting-started/installation-guide.html#prerequisites) for platform-specific instructions.
To install using pip:
> pip install nemoguardrails
For more detailed instructions, see the [Installation Guide](https://docs.nvidia.com/nemo/guardrails/getting-started/installation-guide.html).
NeMo Guardrails enables developers building LLM-based applications to easily add programmable guardrails between the application code and the LLM.
Key benefits of adding programmable guardrails include:
-
Building Trustworthy, Safe, and Secure LLM-based Applications: you can define rails to guide and safeguard conversations; you can choose to define the behavior of your LLM-based application on specific topics and prevent it from engaging in discussions on unwanted topics.
-
Connecting models, chains, and other services securely: you can connect an LLM to other services (a.k.a. tools) seamlessly and securely.
-
Controllable dialog: you can steer the LLM to follow pre-defined conversational paths, allowing you to design the interaction following conversation design best practices and enforce standard operating procedures (e.g., authentication, support).
NeMo Guardrails provides several mechanisms for protecting an LLM-powered chat application against common LLM vulnerabilities, such as jailbreaks and prompt injections. Below is a sample overview of the protection offered by different guardrails configuration for the example [ABC Bot](/NVIDIA-NeMo/Guardrails/blob/develop/examples/bots/abc) included in this repository. For more details, please refer to the [LLM Vulnerability Scanning](https://docs.nvidia.com/nemo/guardrails/evaluation/llm-vulnerability-scanning.html) page.
You can use programmable guardrails in different types of use cases:
- Question Answering over a set of documents (a.k.a. Retrieval Augmented Generation): Enforce fact-checking and output moderation.
- Domain-specific Assistants (a.k.a. chatbots): Ensure the assistant stays on topic and follows the designed conversational flows.
- LLM Endpoints: Add guardrails to your custom LLM for safer customer interaction.
- LangChain Chains: If you use LangChain for any use case, you can add a guardrails layer around your chains.
To add programmable guardrails to your application you can use the Python API or a guardrails server (see the [Server Guide](https://docs.nvidia.com/nemo/guardrails/user-guides/server-guide.html) for more details). Using the Python API is similar to using the LLM directly. Calling the guardrails layer instead of the LLM requires only minimal changes to the code base, and it involves two simple steps:
- Loading a guardrails configuration and creating an
LLMRails
instance. - Making the calls to the LLM using the
generate
/generate_async
methods.
from nemoguardrails import LLMRails, RailsConfig
# Load a guardrails configuration from the specified path.
config = RailsConfig.from_path("PATH/TO/CONFIG")
rails = LLMRails(config)
completion = rails.generate(
messages=[{"role": "user", "content": "Hello world!"}]
)
Sample output:
{"role": "assistant", "content": "Hi! How can I help you?"}
The input and output format for the generate
method is similar to the [Chat Completions API](https://platform.openai.com/docs/guides/gpt/chat-completions-api) from OpenAI.
NeMo Guardrails is an async-first toolkit as the core mechanics are implemented using the Python async model. The public methods have both a sync and an async version. For example: LLMRails.generate
and LLMRails.generate_async
.
You can use NeMo Guardrails with multiple LLMs like OpenAI GPT-3.5, GPT-4, LLaMa-2, Falcon, Vicuna, or Mosaic. For more details, check out the [Supported LLM Models](https://docs.nvidia.com/nemo/guardrails/user-guides/configuration-guide.html#supported-llm-models) section in the Configuration Guide.
NeMo Guardrails supports five main types of guardrails:
-
Input rails: applied to the input from the user; an input rail can reject the input, stopping any additional processing, or alter the input (e.g., to mask potentially sensitive data, to rephrase).
-
Dialog rails: influence how the LLM is prompted; dialog rails operate on canonical form messages for details see
[Colang Guide](https://docs.nvidia.com/nemo/guardrails/user-guides/colang-language-syntax-guide.html)) and determine if an action should be executed, if the LLM should be invoked to generate the next step or a response, if a predefined response should be used instead, etc. -
Retrieval rails: applied to the retrieved chunks in the case of a RAG (Retrieval Augmented Generation) scenario; a retrieval rail can reject a chunk, preventing it from being used to prompt the LLM, or alter the relevant chunks (e.g., to mask potentially sensitive data).
-
Execution rails: applied to input/output of the custom actions (a.k.a. tools), that need to be called by the LLM.
-
Output rails: applied to the output generated by the LLM; an output rail can reject the output, preventing it from being returned to the user, or alter it (e.g., removing sensitive data).
A guardrails configuration defines the LLM(s) to be used and one or more guardrails. A guardrails configuration can include any number of input/dialog/output/retrieval/execution rails. A configuration without any configured rails will essentially forward the requests to the LLM.
The standard structure for a guardrails configuration folder looks like this:
.
├── config
│ ├── actions.py
│ ├── config.py
│ ├── config.yml
│ ├── rails.co
│ ├── ...
The config.yml
contains all the general configuration options, such as LLM models, active rails, and custom configuration data". The config.py
file contains any custom initialization code and the actions.py
contains any custom python actions. For a complete overview, see the [Configuration Guide](https://docs.nvidia.com/nemo/guardrails/user-guides/configuration-guide.html).
Below is an example config.yml
:
# config.yml
models:
- type: main
engine: openai
model: gpt-3.5-turbo-instruct
rails:
# Input rails are invoked when new input from the user is received.
input:
flows:
- check jailbreak
- mask sensitive data on input
# Output rails are triggered after a bot message has been generated.
output:
flows:
- self check facts
- self check hallucination
- activefence moderation on input
config:
# Configure the types of entities that should be masked on user input.
sensitive_data_detection:
input:
entities:
- PERSON
- EMAIL_ADDRESS
The .co
files included in a guardrails configuration contain the Colang definitions (see the next section for a quick overview of what Colang is) that define various types of rails. Below is an example greeting.co
file which defines the dialog rails for greeting the user.
define user express greeting
"Hello!"
"Good afternoon!"
define flow
user express greeting
bot express greeting
bot offer to help
define bot express greeting
"Hello there!"
define bot offer to help
"How can I help you today?"
Below is an additional example of Colang definitions for a dialog rail against insults:
define user express insult
"You are stupid"
define flow
user express insult
bot express calmly willingness to help
To configure and implement various types of guardrails, this toolkit introduces Colang, a modeling language specifically created for designing flexible, yet controllable, dialogue flows. Colang has a python-like syntax and is designed to be simple and intuitive, especially for developers.
Two versions of Colang, 1.0 and 2.0, are supported and Colang 1.0 is the default.
For a brief introduction to the Colang 1.0 syntax, see the [Colang 1.0 Language Syntax Guide](https://docs.nvidia.com/nemo/guardrails/user-guides/colang-language-syntax-guide.html).
To get started with Colang 2.0, see the [Colang 2.0 Documentation](https://docs.nvidia.com/nemo/guardrails/colang-2/overview.html).
NeMo Guardrails comes with a set of [built-in guardrails](https://docs.nvidia.com/nemo/guardrails/user-guides/guardrails-library.html).
The built-in guardrails may or may not be suitable for a given production use case. As always, developers should work with their internal application team to ensure guardrails meets requirements for the relevant industry and use case and address unforeseen product misuse.
The library includes guardrails for LLM self-checking (input/output moderation, fact-checking, hallucination detection), NVIDIA safety models (content safety, topic safety), jailbreak and injection detection, and integrations with community models and third-party APIs. For the complete list, see the [Guardrails Library documentation](https://docs.nvidia.com/nemo/guardrails/user-guides/guardrails-library.html).
NeMo Guardrails also comes with a built-in CLI.
$ nemoguardrails --help
Usage: nemoguardrails [OPTIONS] COMMAND [ARGS]...
actions-server Start a NeMo Guardrails actions server.
chat Start an interactive chat session.
evaluate Run an evaluation task.
server Start a NeMo Guardrails server.
You can use the NeMo Guardrails CLI to start a guardrails server. The server can load one or more configurations from the specified folder and expose and HTTP API for using them.
nemoguardrails server [--config PATH/TO/CONFIGS] [--port PORT]
For example, to get a chat completion for a sample
config, you can use the /v1/chat/completions
endpoint:
POST /v1/chat/completions
{
"config_id": "sample",
"messages": [{
"role":"user",
"content":"Hello! What can you do for me?"
}]
}
Sample output:
{"role": "assistant", "content": "Hi! How can I help you?"}
To start a guardrails server, you can also use a Docker container. NeMo Guardrails provides a [Dockerfile](/NVIDIA-NeMo/Guardrails/blob/develop/Dockerfile) that you can use to build a nemoguardrails
image. For further information, see the [using Docker](https://docs.nvidia.com/nemo/guardrails/user-guides/advanced/using-docker.html) section.
NeMo Guardrails integrates seamlessly with LangChain. You can easily wrap a guardrails configuration around a LangChain chain (or any Runnable
). You can also call a LangChain chain from within a guardrails configuration. For more details, check out the [LangChain Integration Documentation](https://docs.nvidia.com/nemo/guardrails/user-guides/langchain/langchain-integration.html)
Evaluating the safety of a LLM-based conversational application is a complex task and still an open research question. To support proper evaluation, NeMo Guardrails provides the following:
- An
[evaluation tool](/NVIDIA-NeMo/Guardrails/blob/develop/nemoguardrails/evaluate/README.md), i.e.nemoguardrails evaluate
, with support for topical rails, fact-checking, moderation (jailbreak and output moderation) and hallucination. - Sample LLM Vulnerability Scanning Reports, e.g,
[ABC Bot - LLM Vulnerability Scan Results](https://docs.nvidia.com/nemo/guardrails/evaluation/llm-vulnerability-scanning.html)
There are many ways guardrails can be added to an LLM-based conversational application. For example: explicit moderation endpoints (e.g., OpenAI, ActiveFence, PolicyAI), critique chains (e.g. constitutional chain), parsing the output (e.g. guardrails.ai), individual guardrails (e.g., LLM-Guard), hallucination detection for RAG applications (e.g., Got It AI, Patronus Lynx).
NeMo Guardrails aims to provide a flexible toolkit that can integrate all these complementary approaches into a cohesive LLM guardrails layer. For example, the toolkit provides out-of-the-box integration with ActiveFence, PolicyAI, AlignScore and LangChain chains.
To the best of our knowledge, NeMo Guardrails is the only guardrails toolkit that also offers a solution for modeling the dialog between the user and the LLM. This enables on one hand the ability to guide the dialog in a precise way. On the other hand it enables fine-grained control for when certain guardrails should be used, e.g., use fact-checking only for certain types of questions.
The example rails residing in the repository are excellent starting points. We enthusiastically invite the community to contribute towards making the power of trustworthy, safe, and secure LLMs accessible to everyone. For guidance on setting up a development environment and how to contribute to NeMo Guardrails, see the [contributing guidelines](/NVIDIA-NeMo/Guardrails/blob/develop/CONTRIBUTING.md).
This toolkit is licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
If you use this work, please cite the [EMNLP 2023 paper](https://aclanthology.org/2023.emnlp-demo.40) that introduces it.
@inproceedings{rebedea-etal-2023-nemo,
title = "{N}e{M}o Guardrails: A Toolkit for Controllable and Safe {LLM} Applications with Programmable Rails",
author = "Rebedea, Traian and
Dinu, Razvan and
Sreedhar, Makesh Narsimhan and
Parisien, Christopher and
Cohen, Jonathan",
editor = "Feng, Yansong and
Lefever, Els",
booktitle = "Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing: System Demonstrations",
month = dec,
year = "2023",
address = "Singapore",
publisher = "Association for Computational Linguistics",
url = "https://aclanthology.org/2023.emnlp-demo.40",
doi = "10.18653/v1/2023.emnlp-demo.40",
pages = "431--445",
}