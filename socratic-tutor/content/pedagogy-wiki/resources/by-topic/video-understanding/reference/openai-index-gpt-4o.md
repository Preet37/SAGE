# Source: https://openai.com/index/gpt-4o/
# Author: OpenAI
# Author Slug: openai
# Title: GPT-4o (OpenAI model overview)
# Fetched via: search
# Date: 2026-04-09

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

GPT-4o placed first in four out of the six tests, coming second to Claude 3 Opus in MGSM and to GPT-4 Turbo in Discrete Reasoning Over Paragraphs (DROP), which tests a model’s ability to reason across several paragraphs. 

Overall, GPT-4o did not demonstrate a significant boost in performance over GPT-4 Turbo. Its comparative advancements lie chiefly with its multimodal capabilities and increased speed.

## How can people access GPT-4o?

OpenAI is making GPT-4o available for both free and premium users in various locations and products: 

- ChatGPT Plus, Team and Enterprise
- ChatGPT Free
- Desktop and mobile app
- AI applications
- Microsoft Azure OpenAI Studio

### ChatGPT Plus, Team and Enterprise

Subscribers to OpenAI’s premium ChatGPT services have varying levels of access to GPT-4o. ChatGPT Plus users can send up to 80 messages every 3 hours on GPT-4o, with Team users getting more access. Enterprise users have unlimited access to GPT-4o.

…

### AI applications

ChatGPT Plus, Teams and Enterprise users can build custom GPTs through which they and others can use specialized versions of GPT-4o tailored to specific use cases. Developers can also connect to GPT-4o through APIs to create other AI tools.

### Microsoft Azure OpenAI Studio

GPT-4o and GPT-4o mini are both available in Microsoft’s Azure OpenAI Studio, part of Microsoft’s Azure enterprise AI platform. As of publishing, Copilot continues to offer GPT-4 Turbo, though Microsoft announced in May 2024^4^ that its AI service would soon receive GPT-4o support.

…

- **Intellectual property violations:** OpenAI trains its models on data available online, including copyrighted material such as news articles. Models can inadvertently generate copyrighted content as part of a response.

OpenAI classified GPT-4o as a medium-risk model on their internal scale. Models are evaluated on four threat metrics—cybersecurity, CBRN (chemical, biological, radiological and nuclear threats), persuasion and model autonomy. OpenAI assesses models according to the degree to which they can be used to advance developments in each threat field.

Discover the capabilities of OpenAI's GPT-4o, including processing text, images, and audio with improved accuracy and ethical guardrails for AI interactions.
GPT-4o is OpenAI's latest and most advanced multimodal large language model.
It can process and generate text, images, and audio, enabling seamless human-computer interaction across various modalities.
GPT-4o boasts improved capabilities over its predecessors in language understanding, image processing, and audio generation.
…
- **Multimodal Inputs & Outputs:** Accepts text, audio, and image inputs; generates text, audio, and image outputs
- **Natural Language Processing:** Engages in human-like conversations, answers complex questions, generates high-quality content
- **Vision Capabilities:** Analyzes images, charts, and diagrams; describes visual elements; generates new images
- **Audio Capabilities:** Speech recognition, text-to-speech conversion, audio analysis and generation
- **Real-time Conversation:** Enables real-time, back-and-forth conversations across multiple modalities
- **Multilingual Support:** Understands and generates content in over 50 languages
- **Contextual Awareness:** Provides relevant and coherent responses based on user intent, background knowledge, and conversational history
- **Ethical Guardrails:** Ensures responsible, unbiased, and factually accurate outputs
**Accessing GPT-4o:**
|User Type|Access Method|
|--|--|
|Current ChatGPT Plus/Team Users|Upgrade within the ChatGPT interface|
|Developers|Access via the GPT-4o API with higher rate limits and reduced costs|
…
Upcoming enhancements include expanded multimodal capabilities, improved accuracy, and increased efficiency.
GPT-4o is expected to have a significant impact on the AI market, enabling new applications and transforming industries.
## Related video from YouTube
...
GPT-4o is a powerful multimodal model that combines text, audio, and visual inputs and outputs.
It can understand and generate human-like language, process and generate images, and comprehend and produce audio with high accuracy and speed.
**Text Capabilities**
GPT-4o can engage in natural conversations, answer complex questions, and generate high-quality content across various domains.
Its language understanding and generation are on par with human-level proficiency, making interactions feel effortless and intuitive.
**Vision Capabilities**
GPT-4o can analyze and interpret images, charts, and diagrams with precision.
It can describe visual elements in detail, identify objects and patterns, and even generate new images based on textual prompts.
**Audio Capabilities**
GPT-4o can process and generate audio data, including speech recognition, text-to-speech conversion, and audio analysis.
This feature facilitates natural voice interactions, making it ideal for virtual assistants, audio content creation, and accessibility applications.
### New Features in GPT-4o
GPT-4o introduces several innovative features that enhance the user experience and expand its potential applications:
|Feature|Description|
|--|--|
|Real-time Conversation|Engage in real-time, back-and-forth conversations across multiple modalities|
|Improved Multilingual Support|Understand and generate content in over 50 languages|
|Multimodal Generation|Generate outputs that combine text, images, and audio|
|Contextual Awareness|Provide more relevant and coherent responses based on user intent, background knowledge, and conversational history|
|Enhanced Safety and Ethical Guardrails|Ensure responsible, unbiased, and factually accurate outputs|
With its remarkable capabilities and innovative features, GPT-4o represents a significant leap forward in the field of artificial intelligence, paving the way for more natural and intuitive human-machine interactions across a wide range of applications.
## Accessing GPT-4o
GPT-4o is easy to access, with options for different user tiers and needs.
### Upgrading to GPT-4o for Current Users
If you're already a ChatGPT Plus or Team subscriber, you can upgrade to GPT-4o to take advantage of its enhanced capabilities.
To do so, follow these steps:
1. Click on the dropdown menu at the top of the page.
2. Select GPT-4o from the list of available models.
…
### GPT-4o API for Developers
Developers can access GPT-4o through the API, which offers several benefits:
|Feature|Description|
|--|--|
|Revised rate limits|5x higher rate limits compared to GPT-4 Turbo|
|Cost-efficiency|50% reduction in costs compared to GPT-4 Turbo|
|Enhanced capabilities|Advanced multimodal capabilities, including text, voice, and vision inputs and outputs|
To get started with the GPT-4o API:
1. Sign up for an OpenAI account.
2. Obtain an API key.
3. Follow the API documentation to integrate GPT-4o into your projects.
## Using GPT-4o in Practice
GPT-4o offers a wide range of applications in professional settings, from data analysis and decision support to content creation and language tasks.
In this section, we'll explore the numerous ways GPT-4o can be used in practice, providing examples pertinent to the development and networking context.
...
- GPT-4o can process text, images, and voice inputs, enabling various applications across industries.
- Upcoming enhancements will further improve the model's capabilities.
- GPT-4o has the potential to transform industries and revolutionize how we interact with technology.
…
|Recommendation|Description|
...
### What can GPT-4o do?
GPT-4o is a powerful language model that can process and generate human-like text, images, and audio.
It can solve written problems, generate original content, and even create art.
### What are the features of GPT-4o?
GPT-4o has several features that make it more advanced than its predecessors.
These include:
|Feature|Description|
|--|--|
|Multimodal capabilities|Accepts text, images, and audio inputs and generates outputs in various formats|
|Long-form content creation|Can generate content up to 25,000 words, making it suitable for long-form writing and document analysis|
|Image analysis|Can analyze and generate captions for images|

GPT-4o is the latest advancement from OpenAI, bringing the most updated multimodal AI capabilities to platforms like ChatGPT.
This guide will explain what GPT-4o is, how it operates, and the various ways it can enhance interactions and productivity across different applications.
**Table of contents**
...
GPT-4o (the “o” stands for *omni*) is an advanced AI model developed by OpenAI, designed to power generative AI platforms such as ChatGPT.
Unlike its predecessors, GPT-4o is the first version in the GPT series capable of processing text, audio, and images simultaneously.
This multimodal capability enables the model to understand and generate responses across different formats much more quickly, making interactions more seamless and natural.
The introduction of GPT-4o marks a significant evolution from earlier GPT models, which primarily focused on text processing.
With its ability to handle multiple input types, GPT-4o supports a broader range of applications, from creating and analyzing images to transcribing and translating audio.
This versatility allows for more dynamic and engaging user experiences, whether in creative, educational, or practical contexts.
GPT-4o opens up new possibilities for innovative AI-driven solutions by integrating these diverse capabilities into a single model.
## How does GPT-4o work?
GPT-4o is a type of multimodal language model, which is an evolution of large language models (LLMs).
LLMs are highly advanced machine learning models capable of identifying patterns in large amounts of text.
Multimodal models can process text, images, and audio and return any of these as outputs.
The GPT series (and all generative AI) work by predicting the correct response to a user’s prompt.
The predictions are based on the patterns that the model learns during training.
The model recognizes these patterns because of an element called a transformer.
The transformer, which is what the “T” in GPT stands for, can process large amounts of information without the need for humans to label each piece of data.
Instead, it identifies patterns and connections between bits of information.
This is how it learns the structure and meaning of language, audio, and images.
This process is called pre-training.
After the initial training stages, the model is then optimized to follow human input.
At this stage, humans rate the responses so the model can learn which ones are most preferable.
They also help teach the model how to avoid biased prompts and responses.
With the combination of the transformer, the training process, and reinforcement learning from human feedback, GPT-4o can interpret natural language and images and respond in kind.
…
### More capabilities
One of the biggest differences between GPT-4o and previous models is the ability to understand and generate text, audio, and images at a remarkable speed.
GPT-4 and GPT-4 Turbo can process text and image prompts, but they’re only capable of generating text responses by themselves.
...
GPT-4o, on the other hand, can process multiple media formats on its own, leading to a more coherent and faster output.
According to OpenAI, this provides a better experience because the model can process all information directly, allowing it to better capture nuances like tone and background noise.
...
Individual users can access GPT-4 and GPT-4o through ChatGPT.
GPT-4o is available to free users, while GPT-4 requires a paid account.
These models can also be accessed through the OpenAI API and the Azure OpenAI Service, which allow developers to integrate AI into their websites, mobile apps, and software.
### Speed
GPT-4o is several times faster than GPT-4 Turbo, especially with respect to audio processing speed.
With the previous models, the average response time for an audio prompt was 5.4 seconds since it combined the output of three separate models.
The average response time for audio prompts with GPT-4o is 320 milliseconds.
…
### Is GPT-4o free?
You can access GPT-4o for free through ChatGPT, but there are usage limits.
OpenAI doesn’t specify what those limits are, but it does say that users with ChatGPT Plus have a message limit that is up to five times higher than free users.
If you use GPT-4o through a Team or Enterprise-level subscription, the message limit is even higher.
### Cost
GPT-4o, through the OpenAI API, costs half of what GPT-4 Turbo does, at $5 per 1 million input tokens and $15 per 1 million output tokens.
A token is a unit used to measure an AI model’s prompts and responses.
Each word, image, and piece of audio is broken down into chunks, and each chunk is a single token.
An input of 750 words is approximately 1,000 tokens.
...
Currently, GPT-4o costs $0.15 per 1 million input tokens and $0.60 per 1 million output tokens.
…
### Generate original content
With GPT-4o, you can generate original text-based content, such as emails, code, and reports.
The model can be used at every stage of the creation process, from brainstorming to repurposing.
...
Using its image analysis capabilities, you can ask it to describe a chart or photograph.
GPT-4o can also turn an image of text, like a handwritten note, into text or speech.
...
With GPT-4o, you can transcribe audio from meetings, videos, or one-on-one conversations in real time and translate audio from one language to another.
...
For example, you can upload a long data report and ask for an overview of the key points that would appeal to a particular audience.
The overview can be in the form of written text, audio, charts, or a combination of all three.
...
GPT-4o is available for free through ChatGPT (albeit in a limited capacity), meaning that everyday users can access the capabilities of OpenAI’s most advanced model right away.
This is especially beneficial to those who use it for assistive purposes since it removes barriers to access.