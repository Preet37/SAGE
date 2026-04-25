# Source: https://github.com/mem0ai/mem0
# Downloaded: 2026-04-06
# Words: 563
# Author: Mem0 AI
# Author Slug: mem0-ai
[Learn more](https://mem0.ai)
·
[Join Discord](https://mem0.dev/DiG)
·
[Demo](https://mem0.dev/demo)
[📄 Building Production-Ready AI Agents with Scalable Long-Term Memory →](https://mem0.ai/research)
⚡ +26% Accuracy vs. OpenAI Memory • 🚀 91% Faster • 💰 90% Fewer Tokens
🎉 mem0ai v1.0.0 is now available! This major release includes API modernization, improved vector store support, and enhanced GCP integration.
[See migration guide →]
- +26% Accuracy over OpenAI Memory on the LOCOMO benchmark
- 91% Faster Responses than full-context, ensuring low-latency at scale
- 90% Lower Token Usage than full-context, cutting costs without compromise
[Read the full paper](https://mem0.ai/research)
[Mem0](https://mem0.ai) ("mem-zero") enhances AI assistants and agents with an intelligent memory layer, enabling personalized AI interactions. It remembers user preferences, adapts to individual needs, and continuously learns over time—ideal for customer support chatbots, AI assistants, and autonomous systems.
Core Capabilities:
- Multi-Level Memory: Seamlessly retains User, Session, and Agent state with adaptive personalization
- Developer-Friendly: Intuitive API, cross-platform SDKs, and a fully managed service option
Applications:
- AI Assistants: Consistent, context-rich conversations
- Customer Support: Recall past tickets and user history for tailored help
- Healthcare: Track patient preferences and history for personalized care
- Productivity & Gaming: Adaptive workflows and environments based on user behavior
Choose between our hosted platform or self-hosted package:
Get up and running in minutes with automatic updates, analytics, and enterprise security.
- Sign up on
[Mem0 Platform](https://app.mem0.ai) - Embed the memory layer via SDK or API keys
Install the sdk via pip:
pip install mem0ai
Install sdk via npm:
npm install mem0ai
Manage memories from your terminal:
npm install -g @mem0/cli # or: pip install mem0-cli
mem0 init
mem0 add "Prefers dark mode and vim keybindings" --user-id alice
mem0 search "What does Alice prefer?" --user-id alice
See the [CLI documentation](https://docs.mem0.ai/platform/cli) for the full command reference.
Mem0 requires an LLM to function, with `gpt-4.1-nano-2025-04-14 from OpenAI as the default. However, it supports a variety of LLMs; for details, refer to our [Supported LLMs documentation](https://docs.mem0.ai/components/llms/overview).
First step is to instantiate the memory:
from openai import OpenAI
from mem0 import Memory
openai_client = OpenAI()
memory = Memory()
def chat_with_memories(message: str, user_id: str = "default_user") -> str:
# Retrieve relevant memories
relevant_memories = memory.search(query=message, user_id=user_id, limit=3)
memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])
# Generate Assistant response
system_prompt = f"You are a helpful AI. Answer the question based on query and memories.\nUser Memories:\n{memories_str}"
messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}]
response = openai_client.chat.completions.create(model="gpt-4.1-nano-2025-04-14", messages=messages)
assistant_response = response.choices[0].message.content
# Create new memories from the conversation
messages.append({"role": "assistant", "content": assistant_response})
memory.add(messages, user_id=user_id)
return assistant_response
def main():
print("Chat with AI (type 'exit' to quit)")
while True:
user_input = input("You: ").strip()
if user_input.lower() == 'exit':
print("Goodbye!")
break
print(f"AI: {chat_with_memories(user_input)}")
if __name__ == "__main__":
main()
For detailed integration steps, see the [Quickstart](https://docs.mem0.ai/quickstart) and [API Reference](https://docs.mem0.ai/api-reference).
- ChatGPT with Memory: Personalized chat powered by Mem0 (
[Live Demo](https://mem0.dev/demo)) - Browser Extension: Store memories across ChatGPT, Perplexity, and Claude (
[Chrome Extension](https://chromewebstore.google.com/detail/onihkkbipkfeijkadecaafbgagkhglop?utm_source=item-share-cb)) - Langgraph Support: Build a customer bot with Langgraph + Mem0 (
[Guide](https://docs.mem0.ai/integrations/langgraph)) - CrewAI Integration: Tailor CrewAI outputs with Mem0 (
[Example](https://docs.mem0.ai/integrations/crewai))
- Full docs:
[https://docs.mem0.ai](https://docs.mem0.ai) - Community:
[Discord](https://mem0.dev/DiG)·[X (formerly Twitter)](https://x.com/mem0ai) - Contact:
[founders@mem0.ai](mailto:founders@mem0.ai)
We now have a paper you can cite:
@article{mem0,
title={Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory},
author={Chhikara, Prateek and Khant, Dev and Aryan, Saket and Singh, Taranjeet and Yadav, Deshraj},
journal={arXiv preprint arXiv:2504.19413},
year={2025}
}
Apache 2.0 — see the [LICENSE](https://github.com/mem0ai/mem0/blob/main/LICENSE) file for details.