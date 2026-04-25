# Card: Stream only the final node’s output (LangGraph `streamEvents`)
**Source:** https://github.com/langchain-ai/langgraphjs/issues/320  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Event filtering/selection patterns (node-level filtering) for streaming/debugging

## Key Content
- **Problem:** In a multi-node LangGraph (e.g., RAG graph with a query-rewrite node then a generation node), the user wants to **stream tokens only from the last/generation node**, not earlier nodes.
- **Baseline streaming loop (JS):**
  - Create event stream:  
    `const eventStream = await graph.streamEvents(inputs, config);`
  - Consume events:  
    `for await (const { event, data } of eventStream) { ... }`
  - Token streaming event type used in example:  
    `event === "on_chat_model_stream"`
  - Accumulate streamed text when chunk content is a string:  
    `if (typeof data.chunk.content === "string") result += data.chunk.content;`
- **Key filtering mechanism (design rationale):**
  - **Events include metadata** that can identify **which node** produced the event (“metadata containing information about the node that it's within”).
  - A common practice is to use **tagging** to **narrow which events are published/handled**, instead of maintaining a manual `currentNode` state variable.
- **Canonical procedure reference:** Maintainer points to an official how-to demonstrating **streaming outputs from the final node** (Python example):  
  https://langchain-ai.github.io/langgraph/how-tos/streaming-from-final-node/#stream-outputs-from-the-final-node  
  (Use this for the concrete pattern; this issue establishes that node metadata/tags are the intended approach.)

## When to surface
Use when a student asks how to **filter LangGraph streaming events by node** (e.g., “only stream the final/generation node”, “avoid streaming rewrite/retrieval steps”, “how to use metadata/tags with `streamEvents`”).