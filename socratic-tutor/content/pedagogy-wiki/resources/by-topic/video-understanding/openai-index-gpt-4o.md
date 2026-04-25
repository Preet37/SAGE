# Source: https://openai.com/index/gpt-4o/
# Fetched via: search fallback (Perplexity)
# Downloaded: 2026-04-09
# Words: 2415
# Author: OpenAI
# Author Slug: openai
May 13, 2024
Milestone
…
GPT‑4o (“o” for “omni”) is a step towards much more natural human-computer interaction—it accepts as input any combination of text, audio, image, and video and generates any combination of text, audio, and image outputs.
It can respond to audio inputs in as little as 232 milliseconds, with an average of 320 milliseconds, which is similar to human response time⁠(opens in a new window) in a conversation.
It matches GPT‑4 Turbo performance on text in English and code, with significant improvement on text in non-English languages, while also being much faster and 50% cheaper in the API.
GPT‑4o is especially better at vision and audio understanding compared to existing models.
## Model capabilities
Two GPT‑4os interacting and singing.
Interview prep.
Rock Paper Scissors.
Sarcasm.
Math with Sal and Imran Khan.
Two GPT‑4os harmonizing.
Point and learn Spanish.
Meeting AI.
Real-time translation.
Lullaby.
Talking faster.
Happy Birthday.
Dog.
Dad jokes.
…
Prior to GPT‑4o, you could use Voice Mode⁠ to talk to ChatGPT with latencies of 2.8 seconds (GPT‑3.5) and 5.4 seconds (GPT‑4) on average.
To achieve this, Voice Mode is a pipeline of three separate models: one simple model transcribes audio to text, GPT‑3.5 or GPT‑4 takes in text and outputs text, and a third simple model converts that text back to audio.
This process means that the main source of intelligence, GPT‑4, loses a lot of information—it can’t directly observe tone, multiple speakers, or background noises, and it can’t output laughter, singing, or express emotion.
With GPT‑4o, we trained a single new model end-to-end across text, vision, and audio, meaning that all inputs and outputs are processed by the same neural network.
Because GPT‑4o is our first model combining all of these modalities, we are still just scratching the surface of exploring what the model can do and its limitations.
Select sample:
1
Input
A first person view of a robot typewriting the following journal entries:
1. yo, so like, i can see now??
...
As measured on traditional benchmarks, GPT‑4o achieves GPT‑4 Turbo-level performance on text, reasoning, and coding intelligence, while setting new high watermarks on multilingual, audio, and vision capabilities.
…
|Gujarati 4.4x fewer tokens (from 145 to 33)|હેલો, મારું નામ જીપીટી-4o છે.
...
GPT‑4o has safety built-in by design across modalities, through techniques such as filtering training data and refining the model’s behavior through post-training.
We have also created new safety systems to provide guardrails on voice outputs.
We’ve evaluated GPT‑4o according to our Preparedness Framework⁠ and in line with our voluntary commitments⁠.
Our evaluations of cybersecurity, CBRN, persuasion, and model autonomy show that GPT‑4o does not score above Medium risk in any of these categories.
This assessment involved running a suite of automated and human evaluations throughout the model training process.
...
GPT‑4o is our latest step in pushing the boundaries of deep learning, this time in the direction of practical usability.
We spent a lot of effort over the last two years working on efficiency improvements at every layer of the stack.
As a first fruit of this research, we’re able to make a GPT‑4 level model available much more broadly.
GPT‑4o’s capabilities will be rolled out iteratively (with extended red team access starting today).
GPT‑4o’s text and image capabilities are starting to roll out today in ChatGPT.
We are making GPT‑4o available in the free tier, and to Plus users with up to 5x higher message limits.
We'll roll out a new version of Voice Mode with GPT‑4o in alpha within ChatGPT Plus in the coming weeks.
Developers can also now access GPT‑4o in the API as a text and vision model.
GPT‑4o is 2x faster, half the price, and has 5x higher rate limits compared to GPT‑4 Turbo.
We plan to launch support for GPT‑4o's new audio and video capabilities to a small group of trusted partners in the API in the coming weeks.

We are launching our newest flagship model and making more capabilities available for free in ChatGPT.
...
In line with our mission, we are focused on advancing AI technology and ensuring it is accessible and beneficial to everyone.
Today we are introducing our newest model, GPT‑4o, and will be rolling out more intelligence and advanced tools to ChatGPT for free.
## Introducing GPT-4o
GPT‑4o⁠ is our newest flagship model that provides GPT‑4-level intelligence but is much faster and improves on its capabilities across text, voice, and vision.
Today, GPT‑4o is much better than any existing model at understanding and discussing the images you share.
For example, you can now take a picture of a menu in a different language and talk to GPT‑4o to translate it, learn about the food's history and significance, and get recommendations.
In the future, improvements will allow for more natural, real-time voice conversation and the ability to converse with ChatGPT via real-time video.
For example, you could show ChatGPT a live sports game and ask it to explain the rules to you.
We plan to launch a new Voice Mode with these new capabilities in an alpha in the coming weeks, with early access for Plus users as we roll out more broadly.
To make advanced AI more accessible and useful worldwide, GPT‑4o's language capabilities are improved across quality and speed.
ChatGPT also now supports more than 50 languages⁠(opens in a new window) across sign-up and login, user settings, and more.
We are beginning to roll out GPT‑4o to ChatGPT Plus and Team users, with availability for Enterprise users coming soon.
We are also starting to roll out to ChatGPT Free with usage limits today.
Plus users will have a message limit that is up to 5x greater than free users, and Team and Enterprise users will have even higher limits.
## Bringing more intelligence and advanced tools for free
...
When using GPT‑4o, ChatGPT Free users will now have access to features such as:
- Experience GPT‑4⁠ level intelligence
- Get responses⁠(opens in a new window) from both the model and the web
- Analyze data⁠(opens in a new window) and create charts
- Chat about photos⁠ you take
- Upload files⁠(opens in a new window) for assistance summarizing, writing or analyzing
- Discover and use GPTs⁠ and the GPT Store⁠
- Build a more helpful experience with Memory⁠
There will be a limit on the number of messages that free users can send with GPT‑4o depending on usage and demand.
When the limit is reached, ChatGPT will automatically switch to GPT‑3.5 so users can continue their conversations.
### Streamlining your workflow in the new desktop app
For both free and paid users, we're also launching a new ChatGPT desktop app for macOS that is designed to integrate seamlessly into anything you’re doing on your computer.
With a simple keyboard shortcut (Option + Space), you can instantly ask ChatGPT a question.
You can also take and discuss screenshots directly in the app.
You can now have voice conversations with ChatGPT directly from your computer, starting with Voice Mode that has been available in ChatGPT at launch, with GPT‑4o’s new audio and video capabilities coming in the future.
Whether you want to brainstorm a new idea for your company, prepare for an interview or have a topic you’d like to discuss, tap the headphone icon in the bottom right corner of the desktop app to start a voice conversation.
We're rolling out the macOS app to Plus users starting today, and we will make it more broadly available in the coming weeks.
We also plan to launch a Windows version later this year.

## What is GPT-4o?

GPT-4o is a multimodal and multilingual generative pretrained transformer model released in May 2024 by artificial intelligence (AI) developer OpenAI. It is the flagship large language model (LLM) in the GPT-4 family of AI models, which also includes GPT-4o mini, GPT-4 Turbo and the original GPT-4.
The “o” in GPT-4o stands for omni and highlights that GPT-4o is a multimodal AI model with sound and vision capabilities. This means it can accept prompt datasets as a mixture of text, audio, image and video input. GPT-4o is also capable of image generation. GPT-4o brings multimedia input and output capabilities to the same transformer-powered GPT-4 intelligence fueling the other models in its line.
Revealed in May 2024 as part of OpenAI’s Spring Updates, ChatGPT’s new model appeared to translate spoken language in real time, adapt audio responses to include emotional content and engage in lifelike conversations. 

Both GPT-4o and GPT-4o mini support fine-tuning, enabling developers to apply these models toward specific use cases.

### What is GPT-4o mini?

GPT-4o mini is a smaller, cost-effective GPT-4o model and the fastest generative AI model in the OpenAI product family. Unlike bigger large language models (LLMs) with tens or hundreds of billions of parameters, GPT-4o mini is a small and lean model. Despite its compact size, it outperforms GPT-3.5 Turbo with similar speed and at approximately 60% of the cost.
Like its larger sibling, GPT-4o mini has multimodal capabilities, supports languages other than English and can handle typical AI tasks such as reasoning, math and coding. As of publishing, GPT-4o mini can process text and image inputs. OpenAI claims that support for audio and video content is pending. 

Developers can access GPT-4o mini through application programming interfaces (APIs) at a cost of USD 0.15 per million input tokens and USD 0.60 cents per million output tokens.

## How is GPT-4o different from GPT-4 Turbo?

GPT-4o is an “all-in-one” flagship model capable of processing multimodal inputs and outputs on its own as a single neural network. With previous models such as GPT-4 Turbo and GPT-3.5, users would need OpenAI APIs and other supporting models to input and generate varied content types. While GPT-4 Turbo can process image prompts, it is not capable of processing audio without API assistance.
The multimodal nature of GPT-4o is the single biggest breakthrough as compared to GPT-4 Turbo and underpins many of its advancements: 

- Real-time audio conversations
- Tone of voice capabilities
- Built-in video processing
- Image generation
- Greater token efficiency

### Real-time audio conversations

GPT-4o’s faster speed and multimodal capabilities allow it to engage conversationally and translate languages at a more humanlike pace than GPT-4 Turbo. In a video demo as part of its release announcement^1^, ChatGPT-4o was shown translating in real time between English and Spanish speakers. GPT-4o brings chatbot voice support in over 50 languages.
Because it can process audio inputs by itself, GPT-4o has lower latency—the time taken to produce output from the moment an input is received—than previous models. It responds to audio input in 320 milliseconds, comparable to the typical human response time of 210 milliseconds.
Previous iterations of GPT-4 required multiple models assembled in a pipeline to provide a similar service, increasing its latency to 5.4 seconds. Before GPT-4o, OpenAI’s Whisper API converted audio prompts to text, fed them to GPT-4 Turbo, then text-to-speech (TTS) services converted GPT’s responses back to audio.

…

### Tone of voice capabilities

The previous Whisper–GPT–TTS pipeline meant that when fielding audio inputs, GPT-4 Turbo was receiving only a text transcription of what was being said. The transcription isolates the content spoken by the user while filtering out background noise, speaker identities and tone of voice, depriving GPT of substantial contextual data. 

As a multimodal model, GPT-4o can process the entirety of an audio input and respond appropriately to this additional context. Its improved natural language processing (NLP) enables it to include sentiment, tone and emotional content into its output generation when used in voice mode.

### Built-in video processing

GPT-4o handles image and video input in addition to text and audio. GPT-4o can connect to a live camera feed or record a user’s screen, then describe what it sees and answer questions. Users can turn on their smartphone cameras and speak with ChatGPT-4o the same way they would to a friend or colleague.

…

### Image generation

According to OpenAI’s release statement, GPT-4o offers self-contained image generation abilities. GPT-4 Turbo was only able to generate images by connecting to OpenAI’s DALL-E 3 model. GPT-4 Turbo would field a text-based user prompt, then DALL-E would create the image.

### Greater token efficiency

OpenAI improved GPT-4’s tokenization abilities with GPT-4o. Tokenization is the process by which LLMs convert words into data. Each token represents either a whole word or part of one and punctuation. AI models convert words into tokens, then apply complex mathematics to analyze that data.

GPT-4o converts non-Roman languages, such as Chinese, Hindi and Arabic, into tokens much more efficiently than its predecessors. Because OpenAI charges API users per input or output token, GPT-4o’s improved efficiency in non-Roman scripts makes it more cost-effective for use cases in those languages.

## What else can GPT-4o do?

In addition to its new multimodal capabilities, GPT-4o brings many of the same functions as seen in prior iterations: 

- Question-answering
- Document analysis and summarization
- Sentiment analysis
- Data analysis
- Coding

### Question-answering

With a knowledge cutoff of October 2023, GPT-4o is OpenAI’s most current model in terms of its knowledge base. A knowledge cutoff is the point in time at which a model’s training data concludes. Users can ask GPT-4o questions and receive answers, though at the risk of hallucinations.

### Document analysis and summarization

Users can upload files and have ChatGPT analyze and summarize them. GPT-4o’s context window of 128,000 tokens allows it to process large input datasets, though that is not quite as large as that of Claude 3.  

The context window of an LLM represents the maximum number of tokens that it can field while maintaining contextual awareness over the entire input sequence. A larger context window permits AI models to intake more complex prompts and include more information from users when generating responses.
GPT-4 has already demonstrated a real-world ability to read documents via optical character recognition (OCR) by using the GPT-4 Vision API.

…

### Data analysis

GPT-4o can process complex datasets and distill actionable insights, as seen with self-service analytics platforms. It can also represent data as charts and graphs.

### Coding

GPT-4o isn’t the first LLM to have coding abilities, but its multimodal nature can simplify workflows for programmers. Rather than copy and paste code into the user interface, users can share their screens and allow GPT-4o to analyze their code, provide feedback and generate code snippets.

…

GPT-4o placed first in four out of the six tests, coming second to Claude 3 Opus in MGSM and to GPT-4 Turbo in Discrete Reasoning Over P