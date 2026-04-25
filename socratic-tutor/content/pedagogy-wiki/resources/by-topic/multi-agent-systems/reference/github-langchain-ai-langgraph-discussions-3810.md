# Source: https://github.com/langchain-ai/langgraph/discussions/3810
# Author: LangChain
# Author Slug: langchain
# Title: Replace message history atomically (langgraph discussion #3810)
# Fetched via: search
# Date: 2026-04-10

langgraph
...
Design agents that reliably handle complex tasks with LangGraph, an agent runtime and low-level orchestration framework.
### How does LangGraph help?
...
Prevent agents from veering off course with easy-to-add moderation and quality controls.
Add human-in-the-loop checks to steer and approve agent actions.
...
LangGraph’s low-level primitives provide the flexibility needed to create fully customizable agents.
Design diverse control flows — single, multi-agent, hierarchical — all using one framework.
See different agent architectures
...
LangGraph’s built-in memory stores conversation histories and maintains context over time, enabling rich, personalized interactions across sessions.
Learn about agent memory
...
Bridge user expectations and agent capabilities with native token-by-token streaming, showing agent reasoning and actions in real time.
See how to use streaming
...
Learn the basics of LangGraph in this LangChain Academy Course.
You'll learn about how to leverage state, memory, human-in-the-loop, and more for your agents.
Enroll for free
...
Build and ship agents fast with any model provider.
Use high-level abstractions or fine-grained control as needed.
...
LangGraph provides a more expressive framework to handle companies’ unique tasks without restricting users to a single black-box cognitive architecture.
...
LangGraph will not add any overhead to your code and is specifically designed with streaming workflows in mind.
Is LangGraph open source?
Is it free?
Yes.
LangGraph is an MIT-licensed open-source library and is free to use.
### See what your agent is really doing

Trusted by companies shaping the future of agents— including Klarna, Uber, J.P. Morgan, and more— LangGraph is a low-level orchestration framework and runtime for building, managing, and deploying long-running, stateful agents.
LangGraph is very low-level, and focused entirely on agent **orchestration**.
Before using LangGraph, we recommend you familiarize yourself with some of the components used to build agents, starting with models and tools.
...
LangGraph is focused on the underlying capabilities important for agent orchestration: durable execution, streaming, human-in-the-loop, and more.
## ​ Install
```
pip install -U langgraph
```
Then, create a simple hello world example:
```
from langgraph.graph import StateGraph, MessagesState, START, END
def mock_llm(state: MessagesState):
return {"messages": [{"role": "ai", "content": "hello world"}]}
graph = StateGraph(MessagesState)
graph.add_node(mock_llm)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)
graph = graph.compile()
graph.invoke({"messages": [{"role": "user", "content": "hi!"}]})
```
## ​ Core benefits
LangGraph provides low-level supporting infrastructure for *any* long-running, stateful workflow or agent.
LangGraph does not abstract prompts or architecture, and provides the following central benefits: - Durable execution: Build agents that persist through failures and can run for extended periods, resuming from where they left off.
- Human-in-the-loop: Incorporate human oversight by inspecting and modifying agent state at any point.
- Comprehensive memory: Create stateful agents with both short-term working memory for ongoing reasoning and long-term memory across sessions.
- Debugging with LangSmith: Gain deep visibility into complex agent behavior with visualization tools that trace execution paths, capture state transitions, and provide detailed runtime metrics.
- Production-ready deployment: Deploy sophisticated agent systems confidently with scalable infrastructure designed to handle the unique challenges of stateful, long-running workflows.
## ​ LangGraph ecosystem
While LangGraph can be used standalone, it also integrates seamlessly with any LangChain product, giving developers a full suite of tools for building agents.
To improve your LLM application development, pair LangGraph with:
...
LangGraph is inspired by Pregel and Apache Beam.
The public interface draws inspiration from NetworkX.
LangGraph is built by LangChain Inc, the creators of LangChain, but can be used without LangChain.
Edit this page on GitHub or file an issue.

# LangGraph
Trusted by companies shaping the future of agents – including Klarna, Replit, Elastic, and more – LangGraph is a low-level orchestration framework for building, managing, and deploying long-running, stateful agents.
…
Then, create an agent using prebuilt components:
...
# pip install -qU "langchain[anthropic]" to call the model
from langgraph.prebuilt import create_react_agent
def get_weather(city: str) -> str:
"""Get weather for a given city."""
return f"It's always sunny in {city}!"
agent = create_react_agent(
model="anthropic:claude-3-7-sonnet-latest",
tools=[get_weather],
prompt="You are a helpful assistant"
# Run the agent
agent.invoke(
{"messages": [{"role": "user", "content": "what is the weather in sf"}]}
```
...
LangGraph provides low-level supporting infrastructure for
*any* long-running, stateful workflow or agent.
LangGraph does not abstract prompts or architecture, and provides the following central benefits:
- Durable execution: Build agents that persist through failures and can run for extended periods, automatically resuming from exactly where they left off.
- Human-in-the-loop: Seamlessly incorporate human oversight by inspecting and modifying agent state at any point during execution.
- Comprehensive memory: Create truly stateful agents with both short-term working memory for ongoing reasoning and long-term persistent memory across sessions.
- Debugging with LangSmith: Gain deep visibility into complex agent behavior with visualization tools that trace execution paths, capture state transitions, and provide detailed runtime metrics.
- Production-ready deployment: Deploy sophisticated agent systems confidently with scalable infrastructure designed to handle the unique challenges of stateful, long-running workflows.
## LangGraph’s ecosystem¶
While LangGraph can be used standalone, it also integrates seamlessly with any LangChain product, giving developers a full suite of tools for building agents.
To improve your LLM application development, pair LangGraph with:
- LangSmith — Helpful for agent evals and observability.
...
The public interface draws inspiration from NetworkX.
LangGraph is built by LangChain Inc, the creators of LangChain, but can be used without LangChain.

# 1. LangChain & LangGraph Cheat Sheet

- 1. LangChain & LangGraph Cheat Sheet

- 1.1 Quick Start (LCEL minimal chain)

- 1.2 Important Links

- 1.3 Getting Started

- 1.4 Core LangChain Components

- 1.5 Prompt Templates (String, Chat, Few-Shot)
- 1.6 LCEL (LangChain Expression Language)

- 1.7 Output Parsers (Pydantic, JSON, Structured)

- 1.8 Memory Systems

- 1.9 Agents & Tools

- 1.10 Agent Execution (loops, errors)

- 1.11 RAG - Retrieval Augmented Generation
- 1.12 Vector Stores (FAISS, Chroma, Pinecone, Weaviate)

- 1.13 Document Processing (Loaders, Splitters)

- 1.14 Embeddings (OpenAI, HF, Cohere, local)

- 1.15 LangGraph Basics (state)
- 1.16 LangGraph Construction (nodes/edges)

- 1.17 LangGraph Execution (invoke, stream, checkpoint)

- 1.18 Conditional Routing

- 1.19 Multi-Agent Patterns

- 1.20 Human-in-the-Loop

- 1.21 Serving & Deployment (LangServe + FastAPI)
- 1.22 Production Deployment (Docker, scaling)

- 1.23 LangSmith Monitoring

- 1.24 Caching & Optimization

- 1.25 RAG with LCEL (Modern Pattern)

- 1.26 Conversational RAG

- 1.27 Structured Output with Pydantic
- 1.28 Async Operations

- 1.29 Error Handling & Retries

- 1.30 Multi-Query Retrieval

- 1.31 Hybrid Retrieval (Dense + Sparse)

- 1.32 Contextual Compression

- 1.33 Streaming Responses

- 1.34 Function/Tool Calling
- 1.35 Batch Processing

- 1.36 Advanced Patterns (Reflection, ReAct, tools in graphs)

- 1.37 Best Practices

This cheat sheet provides a deep, end-to-end reference for LangChain and LangGraph: core components, LCEL, memory, agents, RAG, embeddings, graph construction, routing, serving/deployment, and monitoring. Each concept is shown with a concise explanation, ASCII/Unicode box-drawing diagram, practical code, and actionable tips.

## 1.1 Quick Start (LCEL minimal chain)

```

from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([

("system", "You are concise."),

("user", "Question: {question}")

])

chain = prompt | llm | StrOutputParser()

print(chain.invoke({"question": "What is LangChain?"}))

```

…

## 1.3 Getting Started

**Brief:** Install core packages, set API keys, and verify environment.

**Diagram:**

…

│ │

↓ ↓

┌────────────────┐ ┌────────────┐

│ OPENAI_API_KEY │ │ python -c │

│ HUGGINGFACE_* │ │ "import │

└────────────────┘ │ langchain"│

└────────────┘

```

**Code:**
```

pip install "langchain>=0.3" "langgraph>=0.2" langchain-openai langchain-community langchain-core

# Optional extras: vector stores, parsers, serving

pip install faiss-cpu chromadb pinecone-client weaviate-client pydantic openai fastapi uvicorn redis

```

…

## 1.4 Core LangChain Components

**Brief:** Models (LLMs vs Chat), Prompts, Output Parsers, Chains.

**Diagram:**

…

**Code:**

```

from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([

("system", "You are concise."),

("user", "Question: {question}")

])

chain = prompt | llm | StrOutputParser()

print(chain.invoke({"question": "What is LangChain?"}))

```

…

## 1.5 Prompt Templates (String, Chat, Few-Shot)

**Brief:** Parameterized prompts to control style and context.

**Diagram:**
```

┌─────────────┐ variables ┌─────────────────┐

│ Base Prompt │ ───────────→ │ Rendered Prompt │

└─────┬───────┘ └────────┬────────┘

│ few-shot examples │ to model

↓ ↓

┌─────────────┐ ┌───────────────┐

│ Example 1 │ │ Chat Messages │

├─────────────┤ └───────────────┘

│ Example 2 │

└─────────────┘

```
**Code:**

```

from langchain_core.prompts import (PromptTemplate, ChatPromptTemplate,

FewShotPromptTemplate)

string_prompt = PromptTemplate.from_template("Translate to French: {text}")

chat_prompt = ChatPromptTemplate.from_messages([

("system", "You are a translator."),

("user", "Translate: {text}")
])

examples = [

{"text": "hello", "translation": "bonjour"},

{"text": "good night", "translation": "bonne nuit"},



example_prompt = PromptTemplate.from_template("Input: {text}\nOutput: {translation}")

few_shot = FewShotPromptTemplate(

examples=examples,

example_prompt=example_prompt,

prefix="Use examples to guide style.",

suffix="Input: {text}\nOutput:",

input_variables=["text"],



print(few_shot.format(text="thank you"))

```

…

## 1.6 LCEL (LangChain Expression Language)

**Brief:** Compose chains with

`|`, parallel branches, passthrough, streaming, async.

**Diagram (LCEL Pipe Flow):**
```

Input



├─→ ┌──────────┐ → ┌────────────┐ → ┌──────────────┐ → Output

│ │ Transform │ │ Transform │ │ Transform │

│ └──────────┘ └────────────┘ └──────────────┘



└─→ ┌───────────────┐

│ RunnableParallel│ (fan-out, then merge)

└───────────────┘

```
**Code:**

```

from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([

("system", "Summarize and extract keywords."),

("user", "{text}")

])

branch = RunnableParallel(

summary=prompt | llm | StrOutputParser(),

keywords=prompt | llm | StrOutputParser(),



chain = RunnablePassthrough.assign(text=lambda x: x["text"]) | branch

result = chain.invoke({"text": "LangChain simplifies LLM orchestration."})

print(result)

```
**Tips:** - Use

`assign` to enrich inputs without losing originals. -

`astream()`/

`astream_events()` for streaming tokens/events. - Compose sync/async seamlessly; prefer async for I/O-heavy pipelines.

…

**Code:**

```

from pydantic import BaseModel, Field

from langchain.output_parsers import PydanticOutputParser

from langchain_core.prompts import ChatPromptTemplate

class Answer(BaseModel):

summary: str = Field(..., description="Brief answer")

sources: list[str]

parser = PydanticOutputParser(pydantic_object=Answer)
prompt = ChatPromptTemplate.from_messages([

("system", "Return JSON matching the schema."),

("user", "Question: {question}\n{format_instructions}")

]).partial(format_instructions=parser.get_format_instructions())

chain = prompt | llm | parser

print(chain.invoke({"question": "What is LangGraph?"}))

```

**Tips:** - Use

`OutputFixingParser` to auto-correct near-misses. - Prefer

`StructuredOutputParser`/

`PydanticOutputParser` for reliability. - Validate early before persisting to DBs.

…

```

**Code:**

```

from langchain.memory import (ConversationBufferMemory,

ConversationBufferWindowMemory, ConversationSummaryMemory,

ConversationEntityMemory)

from langchain.vectorstores import FAISS

from langchain.embeddings import OpenAIEmbeddings

buffer = ConversationBufferMemory(return_messages=True)

window = ConversationBufferWindowMemory(k=3, return_messages=True)

summary = ConversationSummaryMemory(llm=llm, return_messages=True)

entity = ConversationEntityMemory(llm=llm)

# Vector store memory

embedding = OpenAIEmbeddings()

vs = FAISS.from_texts(["Hello world"], embedding)

```
**Tips:** - Pick memory based on cost vs fidelity: window for short chats; summary for long. - Vector memory helps retrieve semantic context; tune chunk size/overlap. - Clear memory per session to avoid leakage across users.

…

**Code:**

```

from langchain.agents import AgentExecutor, create_tool_calling_agent

from langchain.tools import tool

@tool

def multiply(a: float, b: float) -> float:

"""Multiply two numbers."""

return a * b

llm_tools = ChatOpenAI(model="gpt-4o-mini", temperature=0)

…

## 1.10 Agent Execution (loops, errors)

**Brief:**

`AgentExecutor` orchestrates reasoning, tool calls, retries.

**Diagram:**

…

**Code:**

```

result = agent_executor.invoke({"input": "Plan weekend: check weather in NYC and suggest indoor/outdoor."})

# For streaming thoughts

for event in agent_executor.astream_events({"input": "..."}):

print(event)

```

**Tips:** - Set

`handle_parsing_errors=True` or custom handler for robust runs. - Cap

`max_iterations`; log intermediate steps. - Include tool observation snippets in prompts to avoid loops.

## 1.11 RAG - Retrieval Augmented Generation

**Brief:** Retrieve relevant chunks then generate grounded answers.

**Diagram (RAG Full Pipeline):**

…

│ Map-Reduce │ Map chunks -> │ Scales, summaries │ More LLM calls │

│ │ partial, then │ │ │

│ │ reduce │ │ │

│ Refine │ Iterative add │ Keeps detail │ Sequential latency │

│ Map-Rerank │ Score each │ Better precision │ Costly reranking │

└────────────┴───────────────┴────────────────────┴──────────────────────┘

```

…

qa_chain = RetrievalQA.from_chain_type(

llm=llm,

chain_type="map_reduce", # or "stuff", "refine", "map_rerank"

retriever=retriever,



print(qa_chain.invoke({"query": "How does LCEL work?"}))

```

**Tips:** - Tune

`chunk_size` to ~200-1000 tokens; overlap ~10-20%. - Choose chain type per corpus size:

`stuff` for small,

`map_reduce` for large. - Add citations by returning source metadata in prompt.

…

**Code:**

```

from langchain_openai import OpenAIEmbeddings

from langchain_community.embeddings import HuggingFaceEmbeddings, CohereEmbeddings

openai_emb = OpenAIEmbeddings(model="text-embedding-3-small")

hf_emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

cohere_emb = CohereEmbeddings(model="embed-english-light-v3.0", cohere_api_key="...")

```

…

## 1.15 LangGraph Basics (state)

**Brief:** Build graphs where nodes are steps; state carried via typed dicts/reducers.

**Diagram (StateGraph Execution):**

```

┌────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐

│ START │ → │ Node A │ → │ Node B │ → │ END │

└────────┘ └────┬─────┘ └────┬─────┘ └────────┘

│ │

└─────→──────┘ (conditional edge)

```

…

return {"message": state["message"], "steps": ["start"]}

def finish(state: GraphState):

return {"message": state["message"], "steps": state["steps"] + ["finish"]}

graph.add_node("start", start)

graph.add_node("finish", finish)

graph.add_edge("start", "finish")

graph.set_entry_point("start")

graph.set_finish_point("finish")

compiled = graph.compile()

print(compiled.invoke({"message": "hi", "steps": []}))

```

…

```

from langgraph.graph import StateGraph, END

g = StateGraph(GraphState)

g.add_node("decide", lambda s: {"route": "a" if "math" in s["message"] else "b"})

g.add_node("tool_a", lambda s: {"result": "used A"})

…

## 1.17 LangGraph Execution (invoke, stream, checkpoint)

**Brief:** Run graphs sync/async with streaming and persistence.

**Diagram:**

```

┌────────┐ invoke() ┌──────────┐ stream tokens ┌────────────┐

│ Client │────────────→│ Graph │────────────────→ │ Responses │

└────────┘ └──────────┘ └────────────┘

│ checkpoint

└────────────→ storage (Redis/S3/DB)

```
**Code:**

```

compiled = graph.compile(checkpointer=None) # or Redis/S3 checkpointer

# Single call

compiled.invoke({"message": "hi", "steps": []})

# Streaming

for event in compiled.astream_events({"message": "hi", "steps": []}):

print(event)

# Checkpointing with Redis (resume later)
from langgraph.checkpoint.redis import RedisCheckpointSaver

import redis

r = redis.Redis(host="localhost", port=6379, db=0)

checkpointer = RedisCheckpointSaver(r)

compiled_ckpt = graph.compile(checkpointer=checkpointer)

run = compiled_ckpt.invoke({"message": "hi", "steps": []})

# ... later

compiled_ckpt.resume(run["checkpoint_id"])

```

**Tips:** - Use a checkpointer (e.g., Redis) for resumable flows. - Prefer streaming for chat UX; buffer for batch jobs. - Persist state for human handoffs or crash recovery.

…

**Code:**

```

def router(state):

if "finance" in state["message"]:

return "finance"

return "general"

add_conditional_edges(g, "decide", {"finance": "tool_b", "general": "tool_a"})

```

**Tips:** - Keep routing functions pure and deterministic when possible. - For LLM-based routing, constrain outputs (JSON labels) and validate. - Add default fallbacks to avoid dead ends.

…

**Code:**

```

# Pseudocode skeleton

supervisor = compiled # a LangGraph coordinating agents

# Each specialist is a tool-calling chain; supervisor routes tasks

```

**Tips:** - Give each agent narrow scope + tools; supervisor merges. - Prevent loops with max hops/iterations. - Log per-agent traces for debugging.

…

**Code:**

```

# Use a checkpointer; pause on specific node

state = compiled.invoke(...)

# Later, resume with stored checkpoint id

compiled.resume(checkpoint_id="abc123")

```

**Tips:** - Define explicit pause points (e.g., before external actions). - Store human feedback in state for auditability. - Timebox approvals to avoid stale sessions.

## 1.21 Serving & Deployment (LangServe + FastAPI)

**Brief:** Expose chains/graphs as REST endpoints.

**Diagram (LangServe Deployment):**

```

Client → API Gateway → LangServe (FastAPI) → Chain/Graph → Response

```

**Code (LangServe):**
```

# app.py

from fastapi import FastAPI

from langserve import add_routes

from my_chains import chain, graph

app = FastAPI()

add_routes(app, chain, path="/chain")

add_routes(app, graph, path="/graph")

# Run

# uvicorn app:app --reload --host 0.0.0.0 --port 8000

```

…

```

services:

app:

build: .

environment:

- OPENAI_API_KEY=${OPENAI_API_KEY}

ports: ["8000:8000"]

depends_on: [chroma]

chroma:

image: ghcr.io/chroma-core/chroma:latest

ports: ["8001:8000"]

prometheus:

image: prom/prometheus:latest

ports: ["9090:9090"]

```

…

## 1.24 Caching & Optimization

**Brief:** Reduce latency/cost via caching and prompt/model choices.

**Diagram:**

```

┌──────────┐ ┌──────────┐ ┌──────────┐

│ Request │→→│ Cache? │→→│ Response │

└────┬─────┘ └────┬─────┘ └────┬─────┘

│ miss │ hit │

↓ ↓ ↓

Call LLM Return cached Store result

```

…

llm = ChatOpenAI(model="gpt-4o-mini")

embeddings = OpenAIEmbeddings()

vectorstore = FAISS.from_texts(

["LangChain simplifies LLM apps", "LCEL enables composition"],

embeddings



retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# Build RAG chain with LCEL

template = """Answer based on context:

Context: {context}

Question: {question}

Answer:"""

prompt = ChatPromptTemplate.from_template(template)

rag_chain = (

{"context": retriever, "question": RunnablePassthrough()}

| prompt
| llm
| StrOutputParser()


# Use

answer = rag_chain.invoke("What is LangChain?")

```

…

**Code:**

```

from langchain.chains import create_history_aware_retriever, create_retrieval_chain

from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_core.prompts import MessagesPlaceholder

# Contextualize question based on chat history

contextualize_prompt = ChatPromptTemplate.from_messages([

…

("system", "Answer using context:\n{context}"),

MessagesPlaceholder("chat_history"),

("human", "{input}"),

])

qa_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

# Use with history

from langchain_core.messages import HumanMessage, AIMessage
chat_history = [

HumanMessage(content="What is LangChain?"),

AIMessage(content="LangChain is a framework for LLM apps."),



result = rag_chain.invoke({

"input": "What does it simplify?",

"chat_history": chat_history

})

```

**Tips:** - Store

`chat_history` in session/database for multi-turn conversations - Limit history to last 10 messages to control context window - Use

`ConversationBufferMemory` for automatic history management

# Class StateGraph<SD, S, U, N, I, O, C, NodeReturnType, InterruptType, WriterType>

A graph whose nodes communicate by reading and writing to a shared state.
Each node takes a defined `State` as input and returns a `Partial<State>`.

Each state key can optionally be annotated with a reducer function that
will be used to aggregate the values of that key received from multiple nodes.
The signature of a reducer function is (left: Value, right: UpdateValue) => Value.
See Annotation for more on defining state.

After adding nodes and edges to your graph, you must call `.compile()` on it before
you can use it.

#### Example

```
import {
 type BaseMessage,
 AIMessage,
 HumanMessage,
} from "@langchain/core/messages";
import { StateGraph, Annotation } from "@langchain/langgraph";

// Define a state with a single key named "messages" that will
// combine a returned BaseMessage or arrays of BaseMessages
const StateAnnotation = Annotation.Root({
 sentiment: Annotation<string>,
 messages: Annotation<BaseMessage[]>({
 reducer: (left: BaseMessage[], right: BaseMessage | BaseMessage[]) => {
 if (Array.isArray(right)) {
 return left.concat(right);
 }
 return left.concat([right]);
 },
 default: () => [],
 }),
});

const graphBuilder = new StateGraph(StateAnnotation);

// A node in the graph that returns an object with a "messages" key
// will update the state by combining the existing value with the returned one.
const myNode = (state: typeof StateAnnotation.State) => {
 return {
 messages: [new AIMessage("Some new response")],
 sentiment: "positive",
 };
};

const graph = graphBuilder
 .addNode("myNode", myNode)
 .addEdge("__start__", "myNode")
 .addEdge("myNode", "__end__")
 .compile();

await graph.invoke({ messages: [new HumanMessage("how are you?")] });

// {
// messages: [HumanMessage("how are you?"), AIMessage("Some new response")],
// sentiment: "positive",
// }

```

#### Type Parameters
- SD extends SDZod | unknown
- S = SD extends SDZod ? StateType<ToStateDefinition<SD>> : SD
- U = SD extends SDZod ? UpdateType<ToStateDefinition<SD>> : Partial<S>
- N extends string = typeof START
- I extends SDZod = SD extends SDZod ? ToStateDefinition<SD> : StateDefinition
- O extends SDZod = SD extends SDZod ? ToStateDefinition<SD> : StateDefinition
- C extends SDZod = StateDefinition
- NodeReturnType = unknown
- InterruptType = unknown
- WriterType = unknown

#### Hierarchy ( View Summary )
- Graph<N, S, U, StateGraphNodeSpec<S, U>, ToStateDefinition<C>> - StateGraph

##### Index

### Constructors

constructor

### Properties

branches channels compiled edges entryPoint? Node nodes waitingEdges

### Accessors

allEdges

### Methods

_addSchema addConditionalEdges addEdge addNode addSequence compile validate warnIfCompiled

…

I extends
  SDZod = SD extends SDZod ? ToStateDefinition<SD<SD>> : StateDefinition,
  O extends
  SDZod = SD extends SDZod ? ToStateDefinition<SD<SD>> : StateDefinition,
  C extends SDZod = StateDefinition,
  NodeReturnType = unknown,
  InterruptType = unknown,
  WriterType = unknown,
>(
  state: SD extends StateDefinition ? AnnotationRoot<SD<SD>> : never,
  options?: {
  context?: C | AnnotationRoot<ToStateDefinition<C>>;
  input?: I | AnnotationRoot<ToStateDefinition<I>>;
  interrupt?: InterruptType;
  nodes?: N[];
  output?: O | AnnotationRoot<ToStateDefinition<O>>;
  writer?: WriterType;
  },
  ): StateGraph<
  SD,
  S,
  U,
  N,
  I,
  O,
  C,
  NodeReturnType,
  InterruptType,
  WriterType,
  >

…

- S = SD extends SDZod ? StateType<ToStateDefinition<SD<SD>>> : SD
  - U = SD extends SDZod ? UpdateType<ToStateDefinition<SD<SD>>> : Partial<S>
  - N extends string = "__start__"
  - I extends SDZod = SD extends SDZod ? ToStateDefinition<SD<SD>> : StateDefinition
- O extends SDZod = SD extends SDZod ? ToStateDefinition<SD<SD>> : StateDefinition
  - C extends SDZod = StateDefinition
  - NodeReturnType = unknown
  - InterruptType = unknown
  - WriterType = unknown
  #### Parameters
  - state: SD extends StateDefinition ? AnnotationRoot<SD<SD>> : never
  - `Optional`options: {
  context?: C | AnnotationRoot<ToStateDefinition<C>>;
  input?: I | AnnotationRoot<ToStateDefinition<I>>;
  interrupt?: InterruptType;
  nodes?: N[];
  output?: O | AnnotationRoot<ToStateDefinition<O>>;
  writer?: WriterType;
  }

…

new StateGraph<
  SD extends unknown,
  S = SD extends SDZod ? StateType<ToStateDefinition<SD<SD>>> : SD,
  U = SD extends SDZod ? UpdateType<ToStateDefinition<SD<SD>>> : Partial<S>,
  N extends string = "__start__",
I extends
  SDZod = SD extends SDZod ? ToStateDefinition<SD<SD>> : StateDefinition,
  O extends
  SDZod = SD extends SDZod ? ToStateDefinition<SD<SD>> : StateDefinition,
  C extends SDZod = StateDefinition,
  NodeReturnType = unknown,
  InterruptType = unknown,
  WriterType = unknown,
>(
  state: SD extends InteropZodObject ? SD<SD> : never,
  options?: {
  context?: C | AnnotationRoot<ToStateDefinition<C>>;
  input?: I | AnnotationRoot<ToStateDefinition<I>>;
  interrupt?: InterruptType;
  nodes?: N[];
  output?: O | AnnotationRoot<ToStateDefinition<O>>;
  writer?: WriterType;
  },
  ): StateGraph<
  SD,
  S,
  U,
  N,
  I,
  O,
  C,
  NodeReturnType,
  InterruptType,
  WriterType,
  >

…

- S = SD extends SDZod ? StateType<ToStateDefinition<SD<SD>>> : SD
  - U = SD extends SDZod ? UpdateType<ToStateDefinition<SD<SD>>> : Partial<S>
  - N extends string = "__start__"
  - I extends SDZod = SD extends SDZod ? ToStateDefinition<SD<SD>> : StateDefinition
- O extends SDZod = SD extends SDZod ? ToStateDefinition<SD<SD>> : StateDefinition
  - C extends SDZod = StateDefinition
  - NodeReturnType = unknown
  - InterruptType = unknown
  - WriterType = unknown
  #### Parameters
  - state: SD extends InteropZodObject ? SD<SD> : never
  - `Optional`options: {
  context?: C | AnnotationRoot<ToStateDefinition<C>>;
  input?: I | AnnotationRoot<ToStateDefinition<I>>;
  interrupt?: InterruptType;
  nodes?: N[];
  output?: O | AnnotationRoot<ToStateDefinition<O>>;
  writer?: WriterType;
  }

…

new StateGraph<
  SD extends unknown,
  S = SD extends SDZod ? StateType<ToStateDefinition<SD<SD>>> : SD,
  U = SD extends SDZod ? UpdateType<ToStateDefinition<SD<SD>>> : Partial<S>,
  N extends string = "__start__",
I extends
  SDZod = SD extends SDZod ? ToStateDefinition<SD<SD>> : StateDefinition,
  O extends
  SDZod = SD extends SDZod ? ToStateDefinition<SD<SD>> : StateDefinition,
  C extends SDZod = StateDefinition,
  NodeReturnType = unknown,
  InterruptType = unknown,
  WriterType = unknown,
>(
  fields: SD extends StateDefinition
  ? StateGraphArgsWithInputOutputSchemas<SD<SD>, ToStateDefinition<O>>
  : never,
  contextSchema?: C | AnnotationRoot<ToStateDefinition<C>>,
  ): StateGraph<
  SD,
  S,
  U,
  N,
  I,
  O,
  C,
  NodeReturnType,
  InterruptType,
  WriterType,
  >

…

- S = SD extends SDZod ? StateType<ToStateDefinition<SD<SD>>> : SD
  - U = SD extends SDZod ? UpdateType<ToStateDefinition<SD<SD>>> : Partial<S>
  - N extends string = "__start__"
  - I extends SDZod = SD extends SDZod ? ToStateDefinition<SD<SD>> : StateDefinition

…

>(
  fields: SD extends StateDefinition
  ? | AnnotationRoot<SD<SD>>
  | StateGraphArgsWithStateSchema<
  SD<SD>,
  ToStateDefinition<I>,
  ToStateDefinition<O>,
  >
  : never,
  contextSchema?: C | AnnotationRoot<ToStateDefinition<C>>,
  ): StateGraph<
  SD,
  S,
  U,
  N,
  I,
  O,
  C,
  NodeReturnType,
  InterruptType,
  WriterType,

…

>(
  fields: SD extends StateDefinition
  ? SD<SD>
  | StateGraphArgs<S>
  : StateGraphArgs<S>,
  contextSchema?: C | AnnotationRoot<ToStateDefinition<C>>,
  ): StateGraph<
  SD,
  S,
  U,
  N,
  I,
  O,
  C,
  NodeReturnType,
  InterruptType,
  WriterType,
  >

…

  #### Returns StateGraph < SD , S , U , N , I , O , C , NodeReturnType , InterruptType , WriterType >

## Properties

### branches

branches: Record<string, Record<string, Branch<RunInput, N, any>>>

### channels

channels: Record<string, BaseChannel>

…

### Node

Node: StrictNodeAction<S, U, C, N, InterruptType, WriterType>

…

## Accessors

### all Edges
- get allEdges(): Set<[string, string]>
  #### Returns Set < [ string , string ] >

## Methods

### _ add Schema
- _addSchema(stateDefinition: SDZod): void

…

  #### Returns void

### add Conditional Edges
- addConditionalEdges(
  source: BranchOptions<
  S,
  N,
  LangGraphRunnableConfig<StateType<ToStateDefinition<C>>>,
  >,
  ): this

…

  #### Returns this

### add Node
- addNode<
  K extends string,
  NodeMap extends Record<K, NodeAction<S, U, C, InterruptType, WriterType>>,
  >(
  nodes: NodeMap,
  ): StateGraph<
  SD,
  S,
  U,
  N
  | K,
  I,
  O,
  C,
  MergeReturnType<
  NodeReturnType,
  {
  [key in string
  | number
  | symbol]: NodeMap[key] extends NodeAction<
  S,
  U,
  C,
  InterruptType,
  WriterType,
  >

…

  #### Type Parameters
  - K extends string
  - NodeMap extends Record<K, NodeAction<S, U, C, InterruptType, WriterType>>

…

  #### Returns StateGraph < SD , S , U , N | K , I , O , C , MergeReturnType < NodeReturnType , { [ key in string | number | symbol ] : NodeMap [ key ] extends NodeAction < S , U , C , InterruptType , WriterType , > ? U : never } , > , >
- addNode<K extends string, NodeInput = S, NodeOutput = U>(
  nodes: [
  key: K,
  action: NodeAction<NodeInput, NodeOutput, C, InterruptType, WriterType>,
  options?: StateGraphAddNodeOptions<string>,
  ][],
  ): StateGraph<
  SD,
  S,
  U,
  N
  | K,
  I,
  O,
  C,
  MergeReturnType<NodeReturnType, { [key in string]: NodeOutput }>,
  >

…

  #### Parameters
  - nodes: [
  key: K,
  action: NodeAction<NodeInput, NodeOutput, C, InterruptType, WriterType>,
  options?: StateGraphAddNodeOptions<string>,
  ][]
  #### Returns StateGraph < SD , S , U , N | K , I , O , C , MergeReturnType < NodeReturnType , { [ key in string ] : NodeOutput } > , >
- addNode<K extends string, NodeInput = S, NodeOutput = U>(
  key: K,
  action: NodeAction<NodeInput, NodeOutput, C, InterruptType, WriterType>,
  options?: StateGraphAddNodeOptions<string>,
  ): StateGraph<
  SD,
  S,
  U,
  N
  | K,
  I,
  O,
  C,
  MergeReturnType<NodeReturnType, { [key in string]: NodeOutput }>,
  >

…

  #### Parameters
  - key: K
  - action: NodeAction<NodeInput, NodeOutput, C, InterruptType, WriterType>
  - `Optional`options: StateGraphAddNodeOptions<string>
  #### Returns StateGraph < SD , S , U , N | K , I , O , C , MergeReturnType < NodeReturnType , { [ key in string ] : NodeOutput } > , >
- addNode<K extends string, NodeInput = S>(
  key: K,
  action: NodeAction<NodeInput, U, C, InterruptType, WriterType>,
  options?: StateGraphAddNodeOptions<string>,
  ): StateGraph<SD, S, U, N | K, I, O, C, NodeReturnType>

…

  #### Returns StateGraph < SD , S , U , N | K , I , O , C , NodeReturnType >

### add Sequence
- addSequence<K extends string, NodeInput = S, NodeOutput = U>(
  nodes: [
  key: K,
  action: NodeAction<NodeInput, NodeOutput, C, InterruptType, WriterType>,
  options?: StateGraphAddNodeOptions<string>,
  ][],
  ): StateGraph<
  SD,
  S,
  U,
  N
  | K,
  I,
  O,
  C,
  MergeReturnType<NodeReturnType, { [key in string]: NodeOutput }>,
  >

…

  #### Parameters
  - nodes: [
  key: K,
  action: NodeAction<NodeInput, NodeOutput, C, InterruptType, WriterType>,
  options?: StateGraphAddNodeOptions<string>,
  ][]
  #### Returns StateGraph < SD , S , U , N | K , I , O , C , MergeReturnType < NodeReturnType , { [ key in string ] : NodeOutput } > , >
- addSequence<
  K extends string,
  NodeMap extends Record<K, NodeAction<S, U, C, InterruptType, WriterType>>,
  >(
  nodes: NodeMap,
  ): StateGraph<
  SD,
  S,
  U,
  N
  | K,
  I,
  O,
  C,
  MergeReturnType<
  NodeReturnType,
  {
  [key in string
  | number
  | symbol]: NodeMap[key] extends NodeAction<
  S,
  U,
  C,
  InterruptType,
  WriterType,
  >
? U
  : never
  },
  >,
  >
  #### Type Parameters
  - K extends string
  - NodeMap extends Record<K, NodeAction<S, U, C, InterruptType, WriterType>>
  #### Parameters
  - nodes: NodeMap
  #### Returns StateGraph < SD , S , U , N | K , I , O , C , MergeReturnType < NodeReturnType , { [ key in string | number | symbol ] : NodeMap [ key ] extends NodeAction < S , U , C , InterruptType , WriterType , > ? U : never } , > , >

### compile
- compile(
  __namedParameters?: {
  cache?: BaseCache<unknown>;
  checkpointer?: boolean | BaseCheckpointSaver<number>;
  description?: string;
  interruptAfter?: "*" | N[];
  interruptBefore?: "*" | N[];
  name?: string;
  store?: BaseStore;
  },
  ): CompiledStateGraph<
  { [K in string
  | number
  | symbol]: S[K] },
  { [K in string | number | symbol]: U[K] },
  N,
  I,
  O,
  C,
  NodeReturnType,
  InterruptType,
  WriterType,

…

  #### Parameters
  - `Optional`__namedParameters: {
  cache?: BaseCache<unknown>;
  checkpointer?: boolean | BaseCheckpointSaver<number>;
  description?: string;
  interruptAfter?: "*" | N[];
  interruptBefore?: "*" | N[];
  name?: string;
  store?: BaseStore;
  }
  #### Returns CompiledStateGraph < { [ K in string | number | symbol ] : S [ K ] } , { [ K in string | number | symbol ] : U [ K ] } , N , I , O , C , NodeReturnType , InterruptType , WriterType , >

### validate
- validate(interrupt?: string[]): void

…

  #### Returns this

  #### Deprecated

  use `addEdge(key, END)` instead