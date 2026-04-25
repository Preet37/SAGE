# Source: https://www.letta.com/blog/anatomy-of-a-context-window
# Title: Anatomy of a Context Window: A Guide to Context Engineering (Letta)
# Fetched via: search
# Date: 2026-04-10

Company

# Anatomy of a Context Window: A Guide to Context Engineering

July 3, 2025

Context engineering – the practice of designing how an agent's context window is structured and dynamically modified – is becoming increasingly important as agents become long-running and stateful, rather than just simple workflows.

Context is a valuable resource, and requires careful context engineering to design how the context window is managed over time. But to engineer context, we first need to break down the actual components (or “anatomy”) of a context window, and how these components are managed over time.

## Breaking down an agent’s context window

An agent’s context window consists of the following components:
- **System prompt**: Defines the agent's architecture and control flow, providing high-level behavioral instructions and explaining core concepts like memory, blocks, and files.
- **Tool schemas**: Specifications that define available tools and their interfaces, enabling the agent to understand what actions it can perform.
- **System metadata:** Stores statistics and metadata about the agent’s state (e.g. the size of the full message history) .
- **Memory blocks**: Persistent units of context (e.g. for long term memory or working context), managed by the agent itself or other background agents.
- **Files & Artifacts**: Files (PDFs, source code, etc.) that the agent can access and manipulate.
- **Message buffer**: The message stream containing messages (user, assistant, and system, and tool calls and tool returns).
Context management refers to both how this context window is *designed* (through configuration of files, blocks, tools, and prompts), as well as how this context window *evolves* over time. The context window can be controlled directly by the underlying system (the “LLM OS” or “AI OS”) or with agentic tool calling (which is executed by the OS).
For example, external context can be pulled into the context window via tools, such as with MCP (Model Context Protocol) or built-in tools for conversational or file search:

Tool calls can also be used to modify specific parts of the context window, such as memory blocks or file blocks:

Designing these mechanisms for context arrangement and evolution over time is what we refer to as “context engineering”, and is what defines the long-term behavior of your agents.

## The LLM Operating System: Automated Context Engineering

To understand context engineering, it's helpful to think of frameworks like Letta as an LLM OS — an operating system for language models. Just as traditional operating systems manage hardware resources (CPUs, GPUs, I/O devices) and provide abstractions for applications to use the underlying hardware, an LLM OS manages context windows and provides abstractions for context engineering the underlying LLM.
In a traditional operating system, resources are scoped into multiple layers:

Like resources in traditional operating systems, in an LLM OS, *context* is scoped to the application layer (i.e. user space) and the system layer (i.e. kernel space):
- **Kernel Context** - Managed context that can be modified through APIs and tool calling (like kernel memory). This represents the underlying agent configuration (the system prompt and tools), as well as managed context such as memory blocks and files.
- **User Context** - The message buffer containing conversations and external context (like user processes), as well as system calls (tools) to modify the kernel context.

## Kernel Context: System-Managed Context

Kernel context represents the managed, mutable state of an agent—analogous to kernel memory in an operating system. This layer enables agents to maintain memory and work with persistent data structures that evolve over time. Crucially, the kernel context is rendered into the context window where the LLM can observe it, but modifications happen through controlled interfaces.

### The System Call Interface

Just as operating systems provide system calls for user processes to interact with kernel space, the LLM OS provides built-in tools that act as the system call interface:

- **Memory operations**: Tools like memory_replace, memory_rethink, and memory_append allow controlled modification of memory blocks
- **File operations**: Tools like open, close, and grep manage file state in kernel space
- **Custom operations**: Custom tools can call APIs to modify underlying state
Combining these tools allows for management of agent context windows via the LLM. These tools can be used both by the agent itself to manage its own memory and context, or by other specialized agents (e.g. sleep-time agents which process information in the background).

### Memory Blocks

Introduced by MemGPT, memory blocks are reserved portions of the context window designed for persistent memory. Each memory block has several key properties:

- **Size limits**: Hard constraints preventing overflow
- **Labels and descriptions**: Metadata that guides what information should be stored
- **Access patterns**: Including read-only flags for protected memory
Memory blocks enable agents to maintain state across conversations, learn from interactions, and build up knowledge over time, and can also be used as “working memory” to achieve complex tasks like deep research. Memory blocks can also be shared across multiple agents.

### Files

Files provide a familiar abstraction for data management within the context window. The file metaphor is particularly powerful because many LLMs are post-trained on coding tasks, making them naturally adept at file operations. Files can be "open" (loaded into context) or "closed" (stored with metadata only), and also searched with common operations like vector search or grep, which translates well to agent capabilities
**Artifacts** represent a special category of editable files (often with extra dependencies or file groupings). These allow agents to iteratively modify content—whether code, documentation, or creative writing—through successive refinements.

## User Context: The Message Buffer

The user context, or message buffer, represents the "user space" of our LLM OS. Like processes in a traditional OS, this is where the actual work happens—conversations unfold, tools are called, and the agent interacts with the outside world. Tools in the user-space can be used to pull in external context (e.g. via MCP) or modify context in the kernel space.
The buffer contains several message types:

- **User messages**: Direct input from users
- **Assistant messages**: The agent's responses
- **System messages**: Framework or system-generated notifications (like system logs)
- **Tool calls and responses**: The log of both system calls and other tools, as well as their results

### Tool Categories: System Calls vs User Programs

In our OS analogy, tools fall into two distinct categories: 

**System Tools** (Built-in system calls) are provided by the LLM OS itself and have privileged access to modify agent state internals reflected in the compiled kernel context (blocks & files).

**Custom Tools** (User programs) are defined by developers and run in user space with limited privileges. They serve as the primary mechanism for dynamically pulling in external context, such as through:
- Search tools for real-time information or accessible external data
- Model Context Protocol (MCP) for standardized context retrieval

These custom tools act as the agent's gateway to the outside world, pulling relevant external information into the context window while maintaining the integrity of the kernel state through proper system call interfaces.

## Context Engineering & Agent Memory

Proper context management and engineering allows you to build agents that actually have long term memory and the ability to use their memory to solve more complex tasks and learn over time. Context and memory management make it possible to build agents that improve, rather than derailing and degrading.

## Conclusion

You can get started with building agents with proper context engineering with Letta. The Agent Development Environment (ADE) makes it easy to visualize your context window so you can engineer your agent’s context to access long-term memory, large data sources and files, and external tools via MCP.

Get started today with the Letta API and Letta Code.

…

## Company

Company announcements, partnerships

Mar 16, 2026

Letta's next phase

Letta builds agents that learn. Agents with persistent memory, real computer access, and the infrastructure to improve from their own lived experience and work. Letta Code is the runtime that brings these together: git-backed memory, skills, subagents, and deployment that works across every model provider.

…

Introducing Letta Code, a memory-first coding agent. Letta Code is the #1 model-agnostic open source agent on the leading AI coding benchmark Terminal-Bench.

Dec 1, 2025

Programmatic Tool Calling with any LLM

The Letta API now supports programmatic tool calling for any LLM model, enabling agents to generate their own workflows.

…

Introducing Letta's new agent architecture, optimized for frontier reasoning models.

Sep 30, 2025

Introducing Claude Sonnet 4.5 and the memory omni-tool in Letta

Letta agents can now take full advantage of Sonnet 4.5’s advanced memory tool capabilities to dynamically manage their own memory blocks.

…

Letta v0.5.2 adds tool rules, which allows you to constrain the behavior of your Letta agents similar to graphs.

Oct 23, 2024

Letta v0.5.1 release

Letta v0.5.1 adds support for auto-loading entire external tool libraries into your Letta server.
Oct 14, 2024

Letta v0.5 release

Letta v0.5 adds dynamic model (LLM) listings across multiple providers.

Oct 3, 2024

Letta v0.4.1 release

Letta v0.4.1 adds support for Composio, LangChain, and CrewAI tools.

## Research

Sleep-time compute, anatomy of a context window

Apr 2, 2026

Context Constitution

Today we are releasing the Context Constitution: a set of principles governing how AI agents manage context to learn from experience.

Feb 12, 2026

Introducing Context Repositories: Git-based Memory for Coding Agents

We're introducing Context Repositories, a rebuild of how memory works in Letta Code based on programmatic context management and git-based versioning.

# Context window viewer
See exactly what your agent sees including system instructions, tools, and memory.
The context simualtor is a powerful feature in the ADE that allows you to observe and understand what your agent “sees” in real-time.
It provides a transparent view into the agent’s thought process by displaying all the information currently available to the LLM.
…
### System Instructions
Section titled “System Instructions”
The system instructions contain the top-level system prompt that guides the behavior of your agent.
This includes:
- Base instructions about how the agent should behave
- Formatting requirements for responses
- Guidelines for tool usage
While the default system instructions often work well for many use cases, you can customize them to better fit your specific application.
Access and edit these instructions in the Settings tab.
### Function (Tool) Definitions
Section titled “Function (Tool) Definitions”
This section displays the JSON schema definitions of all tools available to your agent.
Each definition includes:
- The tool’s name and description
- Required and optional parameters
- Parameter data types
These definitions are what your agent uses to understand how to call the tools correctly.
When you add or modify tools, this section automatically updates.
### Core Memory Blocks
Section titled “Core Memory Blocks”
Core memory blocks represent the agent’s persistent, in-context memory.
In many of the example starter kits, this includes:
- **Human memory block**: Contains information about the user (preferences, past interactions, etc.)
- **Persona memory block**: Defines the agent’s personality, skills, and self-perception
However, you can structure memory blocks however you want.
For example, by deleting the human and persona blocks, and adding your own.
Memory blocks in core memory are “read-write”: the agent can read and update these blocks during conversations, making them ideal for storing important information that should always be accessible but also should be updated over time.
### External Memory Statistics
Section titled “External Memory Statistics”
This section provides statistics about the agent’s archival memory that exists outside the immediate context window, including:
- Total number of stored memories
- Most recent archival entries
This helps you understand the scope of information your agent can access via retrieval tools.
### Recursive Summary
Section titled “Recursive Summary”
As conversations grow longer, Letta automatically creates and updates a recursive summary of the event history.
This summary:
- Condenses past conversations into key points
- Updates when the context window needs to be truncated
- Preserves important information when older messages get pushed out of context
This mechanism ensures your agent maintains coherence and continuity across long interactions.
### Message History
Section titled “Message History”
The message or “event” queue displays the chronological list of all messages that the agent has processed, including:
- User messages
- Agent responses
- System notifications
- Tool calls and their results
This provides a complete audit trail of the agent’s interaction history.
When the message history exceeds the maximum context window size, Letta intelligently manages content by recreating the summary, and evicting old messages.
Old messages can still be retrieved via tools (similar to how you might use a search tool within a chat application).
…
### Adjusting Maximum Context Length
Section titled “Adjusting Maximum Context Length”
You can configure the maximum context window length in the Advanced section of your agent’s settings.
For example:
- If you’re using Claude 3.5 Sonnet but want to limit context to 16k tokens for performance or cost reasons, set the max context window to 16k instead of using the full 200k capacity.
- When conversations reach this limit, Letta intelligently manages content by:
- Creating summaries of older content
- Moving older messages to archival memory
- Preserving critical information in core memory blocks
### Best Practices
Section titled “Best Practices” - **Regular monitoring**: Check the context window viewer during testing to ensure your agent has access to necessary information
- **Optimizing memory blocks**: Keep core memory blocks concise and relevant
- **Managing context length**: Find the right balance between context size and performance for your use case
- **Using persistent memory**: For information that must be retained, utilize core memory blocks rather than relying on conversation history

This story outlines five essential concepts that explain how large language models process input within a context window.
Using clear examples and practical insights, it covers foundational ideas like tokenization, sequence length, and attention.
The goal is to help readers better understand how context affects model behavior in AI applications.
We also present results from an analytical model used to estimate system behavior, to show how scaling input and output sequence lengths impacts response time.
The results highlight how decoding longer outputs takes significantly more time, pointing to the importance of fast memory systems like HBM in supporting efficient inference at scale.
These concepts are useful for anyone working with or designing prompts for generative AI systems.
...
When working with large language models, it’s important to understand the difference between concepts like context window, context length, and sequence length.
These terms are often used interchangeably, which can lead to confusion.
In this blog, we will define and refer to them as distinct concepts.
The context window is the model’s maximum capacity: the total number of tokens it can process at once, including both your input and the model’s output.
As a simple example, let’s define the rectangle size below as equivalent to a 100,000 token context window.
The context length, on the other hand, is how much you’ve put into that space, which is the actual number of tokens—input tokens (blue) and output tokens (green)—currently in use during a conversation.
For example, if a model has a 100,000-token context window and your input uses 75,000 tokens, only 25,000 tokens remain for the model’s response before it reaches the upper limit of the window.
Sequence length typically refers to the length of a single input or output sequence within that window.
It’s a more granular measure used in model training and inference to track the length of each segment of text.
The context window sets the limit for how much information a model can process, but it does not directly reflect intelligence.
A larger window allows more input, yet the quality of the output often depends on how well that input is structured and used.
Once the window is full, the model may lose coherence, leading to unwanted outcomes (for example, hallucinations).
**Tokens aren’t words**
If the context window is defined by an upper limit (say 100,000), tokens are the units that measure what fits inside, and it’s important to understand that tokens are not words.
The words you type into a prompt are fed to a “tokenizer,” which breaks down text into tokens.
A single word may be split into several tokens.
For example, “strawberry” becomes three tokens and “trifle” becomes two.
In other cases, a word may consist of just one token, like “cake”.
…
...
The model pays attention to all tokens in the context window, but it gives more weight to some than to others.
And that’s why attention in large language models is often described as “weighted”, meaning that not all tokens are treated equally.
This uneven distribution is key to understanding how models might prioritize information and why they sometimes appear to lose focus.
**More context may or may not mean better answers**
A model can scan all tokens within the context window, but it doesn’t consider each token with equal interest.
As the window fills (say, up to 100,000 tokens), the model’s attention becomes more diffuse.
In its attempt to keep track of everything, clarity may diminish.
…
To explore this further, we used a first-order analytical model to estimate end-to-end latency during LLM inference.

Context windows are one of the most important concepts to understand when working with large language models.
This guide explains what they are, why they matter, and how to maximize their effectiveness in your applications.
## What Is a Context Window?
A
**context window** is the amount of text (measured in tokens) that a language model can "see" and consider at any given time.
It represents the model's working memory—all the information it can access when generating a response.
Think of it like a sliding window of text that moves through a conversation or document.
The model can only "see" what's inside this window when generating its next output.
…
## Why Context Windows Matter
The size of a context window determines:
**How much information**the model can consider at once **How long**conversations can be before earlier messages are forgotten **How much documentation**or reference material can be included **The complexity**of tasks the model can handle
Larger context windows enable more sophisticated applications, but they also come with higher costs and potential inefficiencies if not used properly.
…
...
They're also crucial for:
- Document analysis and summarization
- Code generation with extensive references
- Complex reasoning tasks that require multiple steps
- Retrieval-augmented generation (RAG) applications
### Context Window Visualization
Context window breakdown:
- • System prompt: 150 tokens
- • Conversation history: 4,850 tokens
- • Current user query: 1,000 tokens
- • Retrieved documents: 6,000 tokens
## Strategies for Optimizing Context Window Usage
...
Instead of keeping the entire conversation history in the context window, periodically summarize previous exchanges.
This technique is sometimes called "context compression."
#### ❌ Inefficient
...
Instead of loading entire documents into the context window, use RAG to:
- Store documents in a vector database
- Retrieve only the most relevant sections based on the current query
- Include only those sections in the context window
### 3.
Implement Context Management
Develop a system to manage what goes into the context window:
- Prioritize recent and relevant information
- Remove redundant or outdated content
- Maintain a "memory" outside the context window that can be selectively included
// Pseudocode for context window management function manageContextWindow(conversation, maxTokens = 8000) { // Calculate current token usage const currentTokenCount = countTokens(conversation); if (currentTokenCount <= maxTokens) { return conversation; // No management needed } // If we exceed the limit, compress older messages const compressedHistory = summarizeOlderMessages(conversation); // Keep the most recent messages intact const recentMessages = getRecentMessages(conversation, 5); return [...compressedHistory, ...recentMessages]; }
### 4.
Use Chunking for Long-Form Content
When working with long documents:
- Split the document into logical chunks (paragraphs, sections, etc.)
- Process each chunk separately
- Combine the results afterward
### 5.
Be Strategic About System Prompts
System prompts consume tokens from your context window.
Make them concise while still providing necessary instructions.
Consider:
- Moving detailed examples to user messages where they can be removed later
- Using shorthand instructions that the model can understand
- Focusing on the most important guidelines
## Measuring and Monitoring Context Usage
To effectively manage your context window:
- Track token usage for each component (system prompt, user messages, etc.)
- Set up alerts when approaching context limits
- Regularly audit your prompts for optimization opportunities
- Use a token counter (like ours!) to measure token usage before sending to the API
### Need to measure your token usage?
Use our free token counter to see exactly how many tokens your text uses and how close you are to your context window limits.
## Conclusion

Tracks
...
In the world of Large Language Models (LLMs), this attention span is defined by the context window.
...
## What Is a Context Window?
The context window of an AI model determines the amount of text it can hold in its working memory while generating a response.
It limits how long a conversation can be carried out without forgetting details from earlier interactions.
You can think of it as a human’s short-term memory.
It stores information from previous conversations temporarily to use for the task at hand.
Context windows affect various aspects, including the quality of reasoning, the depth of conversation, and the model's ability to personalize responses effectively.
It also determines the maximum size of input it can process at once.
When a prompt or conversation context exceeds that limit, the model truncates (cuts off) the earliest parts of the text to make room.
…
## Context Window Concepts
Three core concepts underlie LLMs: tokenization, the attention mechanism, and positional encoding.
### Tokenization
Tokenization is the process of converting raw text into a sequence of smaller units, or tokens, that an LLM can process.
These tokens can represent entire words, individual characters, or even partial syllables.
Collectively, the entire set of unique tokens a model recognizes is referred to as its vocabulary.
For example, the sentence “Hello, world” might be tokenized into
...
During training or inference, each token is turned into a unique integer, and the model reads these numbers instead of the original text.
It analyzes the numerical sequence, learns how tokens relate to one another, and generates new text by predicting the next probable token.
Efficient tokenization plays a big role in the amount of information that fits into a model’s context window.
When a tokenizer can represent text with fewer tokens, more content fits into the same window.
...
The so-called attention mechanism is another foundation of modern LLMs.
It helps a model focus on the most relevant parts of its input when generating an output.
Instead of treating every token equally, the model compares the current representation against all other token representations and assigns a score to each comparison.
This selective weighting lets the model process long sequences and understand context more effectively.
Attention is built around three components: **Queries**, **Keys**, and **Values**.
- **Queries:** The signal sent by the current token to "search" for relevant information in the rest of the sequence.
- **Keys:** The identifier for each token in the sequence that determines how well it matches the search signal.
- **Values:** The actual informational content that is retrieved and used when a match between a Query and a Key is found.
The model computes similarity scores between queries and keys, converts those scores into weights using the softmax activation function, and then produces the final output as a weighted sum of the values.
Self-attention compares the current token to every other token in the sequence.
...
Transformers, which power modern language models, don’t naturally understand the order of tokens.
Instead, they rely on positional encoding to incorporate this information.
Positional encoding adds a small signal to each token that helps the model understand distance and relative arrangement.
The specific method of positional information also defines how far the model can reliably track relationships within a sequence, which determines the size and effectiveness of its context window.
Let’s compare some popular methods:
...
Open-source model families like Llama and Mistral generally land in the 100k to 200k range, offering respectable long-context performance while remaining practical to deploy locally or fine-tune.
Notable exceptions include Llama Maverick, which supports a 1 million token window designed for general-purpose reasoning across long documents.
Meanwhile, Llama Scout pushes the boundary even further with a massive 10 million token capacity, specifically engineered for processing entire codebases or legal archives in a single pass.
…
### Real-world applications
...
Tasks that involve full-document analysis, multi-file reasoning, or long-running conversations benefit from models with windows in the 200k–1M range.
For more focused tasks like summarization, code review, or short-form question answering, models in the 100k–200k range often provide the best balance of speed, cost, and accuracy.