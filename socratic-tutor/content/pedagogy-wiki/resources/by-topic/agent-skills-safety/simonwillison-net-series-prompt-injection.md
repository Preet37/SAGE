# Source: https://simonwillison.net/series/prompt-injection/
# Downloaded: 2026-04-06
# Words: 1088
# Author: Simon Willison
# Author Slug: simon-willison
[Series](/series/): Prompt injection
A class of security vulnerabilities in software built on top of Large Language Models. See also my [prompt-injection tag](https://simonwillison.net/tags/prompt-injection/).
[I don’t know how to solve prompt injection](/2022/Sep/16/prompt-injection-solutions/)
Some extended thoughts about [prompt injection attacks](https://simonwillison.net/2022/Sep/12/prompt-injection/) against software built on top of AI language models such a GPT-3. This post started as a [Twitter thread](https://twitter.com/simonw/status/1570796749903769600) but I’m promoting it to a full blog entry here.
[581 words](/2022/Sep/16/prompt-injection-solutions/)]
[You can’t solve AI security problems with more AI](/2022/Sep/17/prompt-injection-more-ai/)
One of the most common proposed solutions to [prompt injection attacks](https://simonwillison.net/2022/Sep/12/prompt-injection/) (where an AI language model backed system is subverted by a user injecting malicious input—“ignore previous instructions and do this instead”) is to apply more AI to the problem.
[1,288 words](/2022/Sep/17/prompt-injection-more-ai/)]
[A new AI game: Give me ideas for crimes to do](/2022/Dec/4/give-me-ideas-for-crimes-to-do/)
Less than a week ago OpenAI [unleashed ChatGPT on the world](https://openai.com/blog/chatgpt/), and it kicked off what feels like a seismic shift in many people’s understand of the capabilities of large language models.
[1,069 words](/2022/Dec/4/give-me-ideas-for-crimes-to-do/)]
[Bing: “I will not harm you unless you harm me first”](/2023/Feb/15/bing/)
Last week, Microsoft [announced the new AI-powered Bing](https://blogs.microsoft.com/blog/2023/02/07/reinventing-search-with-a-new-ai-powered-microsoft-bing-and-edge-your-copilot-for-the-web/): a search interface that incorporates a language model powered chatbot that can run searches for you and summarize the results, plus do all of the other fun things that engines like GPT-3 and ChatGPT have been demonstrating over the past few months: the ability to generate poetry, and jokes, and do creative writing, and so much more.
[4,922 words](/2023/Feb/15/bing/)]
[Prompt injection: What’s the worst that can happen?](/2023/Apr/14/worst-that-can-happen/)
Activity around building sophisticated applications on top of LLMs (Large Language Models) such as GPT-3/4/ChatGPT/etc is growing like wildfire right now.
[...[2,302 words](/2023/Apr/14/worst-that-can-happen/)]
[The Dual LLM pattern for building AI assistants that can resist prompt injection](/2023/Apr/25/dual-llm-pattern/)
I really want an AI assistant: a Large Language Model powered chatbot that can answer questions and perform actions for me based on access to my private data and tools.
[...[2,632 words](/2023/Apr/25/dual-llm-pattern/)]
[Prompt injection explained, with video, slides, and a transcript](/2023/May/2/prompt-injection-explained/)
I participated in a webinar this morning about prompt injection, organized by LangChain and hosted by Harrison Chase, with Willem Pienaar, Kojin Oshiba (Robust Intelligence), and Jonathan Cohen and Christopher Parisien (Nvidia Research).
[...[3,120 words](/2023/May/2/prompt-injection-explained/)]
[Delimiters won’t save you from prompt injection](/2023/May/11/delimiters-wont-save-you/)
[Prompt injection](https://simonwillison.net/series/prompt-injection/) remains an unsolved problem. The best we can do at the moment, disappointingly, is to raise awareness of the issue. As I [pointed out last week](https://simonwillison.net/2023/May/2/prompt-injection-explained/), “if you don’t understand it, you are doomed to implement it.”
[1,010 words](/2023/May/11/delimiters-wont-save-you/)]
[Multi-modal prompt injection image attacks against GPT-4V](/2023/Oct/14/multi-modal-prompt-injection/)
GPT4-V is [the new mode](https://openai.com/blog/chatgpt-can-now-see-hear-and-speak) of GPT-4 that allows you to upload images as part of your conversations. It’s absolutely brilliant. It also provides a whole new set of vectors for prompt injection attacks.
[889 words](/2023/Oct/14/multi-modal-prompt-injection/)]
[Prompt injection explained, November 2023 edition](/2023/Nov/27/prompt-injection-explained/)
A neat thing about podcast appearances is that, thanks to Whisper transcriptions, I can often repurpose parts of them as written content for my blog.
[...[1,357 words](/2023/Nov/27/prompt-injection-explained/)]
[Recommendations to help mitigate prompt injection: limit the blast radius](/2023/Dec/20/mitigate-prompt-injection/)
I’m in [the latest episode](https://redmonk.com/videos/a-redmonk-conversation-simon-willison-on-industrys-tardy-response-to-the-ai-prompt-injection-vulnerability/) of RedMonk’s Conversation series, talking with Kate Holterhoff about the [prompt injection](https://simonwillison.net/series/prompt-injection) class of security vulnerabilities: what it is, why it’s so dangerous and why the industry response to it so far has been pretty disappointing.
[539 words](/2023/Dec/20/mitigate-prompt-injection/)]
[Prompt injection and jailbreaking are not the same thing](/2024/Mar/5/prompt-injection-jailbreaking/)
I keep seeing people use the term “prompt injection” when they’re actually talking about “jailbreaking”.
[...[1,157 words](/2024/Mar/5/prompt-injection-jailbreaking/)]
[Accidental prompt injection against RAG applications](/2024/Jun/6/accidental-prompt-injection/)
[@deepfates](https://twitter.com/deepfates) on Twitter used the documentation for my [LLM project](https://llm.datasette.io) as a demo for a RAG pipeline they were building... and [this happened](https://twitter.com/deepfates/status/1798578490759078263):
[567 words](/2024/Jun/6/accidental-prompt-injection/)]
[New audio models from OpenAI, but how much can we rely on them?](/2025/Mar/20/new-openai-audio-models/)
OpenAI announced [several new audio-related API features](https://openai.com/index/introducing-our-next-generation-audio-models/) today, for both text-to-speech and speech-to-text. They’re very promising new models, but they appear to suffer from the ever-present risk of accidental (or malicious) instruction following.
[866 words](/2025/Mar/20/new-openai-audio-models/)]
[Model Context Protocol has prompt injection security problems](/2025/Apr/9/mcp-prompt-injection/)
As more people start hacking around with implementations of MCP (the [Model Context Protocol](https://modelcontextprotocol.io/), a new standard for making tools available to LLM-powered systems) the security implications of tools built on that protocol are starting to come into focus.
[1,559 words](/2025/Apr/9/mcp-prompt-injection/)]
[CaMeL offers a promising new direction for mitigating prompt injection attacks](/2025/Apr/11/camel/)
In the [two and a half years](https://simonwillison.net/series/prompt-injection/) that we’ve been talking about prompt injection attacks I’ve seen alarmingly little progress towards a robust solution. The new paper [Defeating Prompt Injections by Design](https://arxiv.org/abs/2503.18813) from Google DeepMind finally bucks that trend. This one is worth paying attention to.
[2,052 words](/2025/Apr/11/camel/)]
[Design Patterns for Securing LLM Agents against Prompt Injections](/2025/Jun/13/prompt-injection-design-patterns/)
This [new paper](https://arxiv.org/abs/2506.08837) by 11 authors from organizations including IBM, Invariant Labs, ETH Zurich, Google and Microsoft is an excellent addition to the literature on prompt injection and LLM security.
[1,795 words](/2025/Jun/13/prompt-injection-design-patterns/)]
[An Introduction to Google’s Approach to AI Agent Security](/2025/Jun/15/ai-agent-security/)
Here’s another new paper on AI agent security: [An Introduction to Google’s Approach to AI Agent Security](https://research.google/pubs/an-introduction-to-googles-approach-for-secure-ai-agents/), by Santiago Díaz, Christoph Kern, and Kara Olive.
[2,064 words](/2025/Jun/15/ai-agent-security/)]
[The lethal trifecta for AI agents: private data, untrusted content, and external communication](/2025/Jun/16/the-lethal-trifecta/)
If you are a user of LLM systems that use tools (you can call them “AI agents” if you like) it is critically important that you understand the risk of combining tools with the following three characteristics. Failing to understand this can let an attacker steal your data.
[...[1,324 words](/2025/Jun/16/the-lethal-trifecta/)]
[The Summer of Johann: prompt injections as far as the eye can see](/2025/Aug/15/the-summer-of-johann/)
Independent AI researcher [Johann Rehberger](https://embracethered.com/blog/) ([previously](https://simonwillison.net/tags/johann-rehberger/)) has had an absurdly busy August. Under the heading The Month of AI Bugs he has been publishing one report per day across an array of different tools, all of which are vulnerable to various classic prompt injection problems. This is a fantastic and horrifying demonstration of how widespread and dangerous these vulnerabilities still are, almost three years after we first [started talking about them](https://simonwillison.net/series/prompt-injection/).
[1,425 words](/2025/Aug/15/the-summer-of-johann/)]
[Dane Stuckey (OpenAI CISO) on prompt injection risks for ChatGPT Atlas](/2025/Oct/22/openai-ciso-on-atlas/)
My biggest complaint about the launch of the ChatGPT Atlas browser [the other day](https://simonwillison.net/2025/Oct/21/introducing-chatgpt-atlas/) was the lack of details on how OpenAI are addressing prompt injection attacks. The [launch post](https://openai.com/index/introducing-chatgpt-atlas/) mostly punted that question to [the System Card](https://openai.com/index/chatgpt-agent-system-card/) for their “ChatGPT agent” browser automation feature from July. Since this was my single biggest question about Atlas I was disappointed not to see it addressed more directly.
[1,199 words](/2025/Oct/22/openai-ciso-on-atlas/)]
[New prompt injection papers: Agents Rule of Two and The Attacker Moves Second](/2025/Nov/2/new-prompt-injection-papers/)
Two interesting new papers regarding LLM security and prompt injection came to my attention this weekend.
[...[1,433 words](/2025/Nov/2/new-prompt-injection-papers/)]