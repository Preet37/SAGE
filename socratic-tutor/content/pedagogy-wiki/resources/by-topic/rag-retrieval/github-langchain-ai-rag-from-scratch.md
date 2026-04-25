# Source: https://github.com/langchain-ai/rag-from-scratch
# Author: LangChain
# Author Slug: langchain
# Downloaded: 2026-04-06
# Words: 113
LLMs are trained on a large but fixed corpus of data, limiting their ability to reason about private or recent information. Fine-tuning is one way to mitigate this, but is often [not well-suited for factual recall](https://www.anyscale.com/blog/fine-tuning-is-for-form-not-facts) and [can be costly](https://www.glean.com/blog/how-to-build-an-ai-assistant-for-the-enterprise).
Retrieval augmented generation (RAG) has emerged as a popular and powerful mechanism to expand an LLM's knowledge base, using documents retrieved from an external data source to ground the LLM generation via in-context learning.
These notebooks accompany a [video playlist](https://youtube.com/playlist?list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x&feature=shared) that builds up an understanding of RAG from scratch, starting with the basics of indexing, retrieval, and generation.
langchain-ai/rag-from-scratch
Folders and files
| Name | Name | Last commit date | ||
|---|---|---|---|---|