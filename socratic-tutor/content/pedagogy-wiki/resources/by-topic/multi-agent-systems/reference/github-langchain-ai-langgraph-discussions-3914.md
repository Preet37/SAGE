# Source: https://github.com/langchain-ai/langgraph/discussions/3914
# Author: LangChain
# Author Slug: langchain
# Title: Cannot get messages merged after two parallel nodes (langgraph discussion #3914)
# Fetched via: search
# Date: 2026-04-10

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
- LangChain Academy: Learn the basics of LangGraph in our free, structured course.
...
The public interface draws inspiration from NetworkX.
LangGraph is built by LangChain Inc, the creators of LangChain, but can be used without LangChain.

- ### Discussions are moving to the LangChain Forum!

Define sub-graph as separate StateGraph: from langgraph.graph import StateGraph; def create_researcher(): graph = StateGraph(ResearchState); graph.add_node('search', search_node); graph.add_node('summarize', summarize_node); graph.add_edge('search', 'summarize'); graph.set_entry_point('search'); return graph.compile().
Use sub-graph as node in parent graph: parent = StateGraph(MainState); researcher = create_researcher(); parent.add_node('researcher', researcher); parent.add_node('writer', writer_node); parent.add_edge('researcher', 'writer'). State mapping: use transform functions for different schemas: def map_state(parent_state): return {'query': parent_state['topic']}; parent.add_node('researcher', researcher, input_transform=map_state).
Benefits: modular testing, reusable components, team collaboration. Sub-graphs inherit checkpointer from parent. Use for: specialized agents (research, writing, analysis), microservice-style architectures, complex workflows. Each sub-graph can have independent state schema and conditional logic.

## unknown

25 questions
Use stream() with stream_mode parameter: for event in graph.stream(inputs, config, stream_mode='values'): process(event). Stream modes: 'values' = full state after each node, 'updates' = only node output deltas, 'messages' = individual messages added to MessagesState, 'events' = low-level events (on_chain_start, on_tool_end).
For token streaming from LLM: async for event in graph.astream_events(inputs, version='v2'): if event['event'] == 'on_chat_model_stream': token = event['data']['chunk'].content; yield token. Combine modes: graph.stream(inputs, stream_mode=['values', 'updates']) returns dict with both.
Production pattern: use 'updates' for incremental UI updates, 'messages' for chat interfaces, 'events' for debugging. With FastAPI SSE: async def stream_endpoint(): async for chunk in graph.astream(input, stream_mode='messages'): yield f'data: {json.dumps(chunk)}\n\n'. Stream mode 'debug' includes timing and metadata for performance analysis.
The pipe operator | chains LangChain components in sequence: chain = prompt | model | parser. Each component's .invoke() output becomes the next component's input. Example: from langchain_core.prompts import ChatPromptTemplate; from langchain_openai import ChatOpenAI; from langchain_core.output_parsers import StrOutputParser; prompt = ChatPromptTemplate.from_template('Explain {topic}'); model = ChatOpenAI(model='gpt-4'); parser = StrOutputParser(); chain = prompt | model | parser; result = chain.invoke({'topic': 'LCEL'}).
Benefits: composable, supports async (.ainvoke()), streaming (.astream()), batching (.abatch()). LCEL provides streaming, parallel execution, and retry capabilities out of the box without code changes. All LCEL chains automatically inherit async methods. Use for production LLM workflows requiring streaming and low latency.
Use @tool decorator for simple tools: from langchain_core.tools import tool; @tool def search_database(query: str) -> str: '''Search the product database for matching items.''' return db.query(query). Docstring is REQUIRED - becomes tool description for LLM. Function name becomes tool name by default.
For advanced customization: from pydantic import BaseModel, Field; class SearchInput(BaseModel): query: str = Field(description='Search query string'); max_results: int = Field(default=10, description='Maximum results to return'); @tool('product-search', args_schema=SearchInput, return_direct=False) def search(query: str, max_results: int = 10) -> str: '''Search products with configurable result limit.''' return db.query(query, limit=max_results).

…

Define reducer function and annotate field: from typing import Annotated; from operator import add; def merge_dicts(existing: dict, new: dict) -> dict: return {**existing, **new}; class State(TypedDict): count: Annotated[int, add]; data: Annotated[dict, merge_dicts]; messages: Annotated[list, add_messages].
Built-in reducers: add (sum numbers, concatenate lists), operator.or_ (merge dicts, overwrite conflicts). Custom reducer signature: def reducer(existing_value, new_value) -> updated_value. Example - keep max: def keep_max(existing: int, new: int) -> int: return max(existing, new); score: Annotated[int, keep_max].
Reducer called when node returns state update: def node(state): return {'count': 5} # add reducer: count += 5. Without reducer, updates overwrite existing value. Use add_messages for chat history (handles duplicates by ID). Common patterns: accumulate logs, merge configs, track max/min metrics. Reducers run before passing state to next node.

…

For validation errors: from langchain_core.runnables import RunnablePassthrough; def validate(x): if not x.get('required_field'): raise ValueError('Missing required field'); return x; chain = input_chain | RunnableLambda(validate) | process_chain. Use with_fallbacks for automatic fallback: primary = expensive_llm | parser; fallback = cheap_llm | RunnablePassthrough(); chain = primary.with_fallbacks([fallback]).

…

Add interrupt_before or interrupt_after when compiling graph: graph = graph_builder.compile(checkpointer=checkpointer, interrupt_before=['approval_node']). When interrupt triggers, execution pauses and saves state via checkpointer (required dependency). Resume with updated state: config = {'configurable': {'thread_id': 'thread1'}}; graph.invoke(None, config) to continue.
For user input: state = graph.get_state(config); state.values['user_approval'] = True; graph.update_state(config, state.values); graph.invoke(None, config). Use interrupt_before for pre-approval (review before action), interrupt_after for post-approval (review results). Common patterns: content moderation, transaction approval, form validation. Interrupts pause indefinitely until manual resume - ideal for workflows requiring human judgment. Must use checkpointer (SqliteSaver/PostgresSaver) - interrupts fail without persistence.
Use FakeListLLM for deterministic testing: from langchain_community.llms.fake import FakeListLLM; responses = ['Response 1', 'Response 2']; fake_llm = FakeListLLM(responses=responses); chain = prompt | fake_llm | parser; result = chain.invoke(input).
Responses returned in order, raises IndexError when exhausted. For chat models: from langchain_community.chat_models import FakeChatModel; fake_chat = FakeChatModel(responses=['Hello', 'Goodbye']). Mock with pytest: import pytest; from unittest.mock import MagicMock; @pytest.fixture; def mock_llm(): llm = MagicMock(); llm.invoke.return_value = 'Mocked response'; return llm; def test_chain(mock_llm): chain = prompt | mock_llm; assert chain.invoke({'input': 'test'}) == 'Mocked response'.
For integration tests: use real LLM with caching to avoid repeated API calls. Test error paths: fake_llm.responses = [Exception('API Error')]. Validate: prompt rendering, parser logic, error handling, state management. Unit test individual components, integration test full chains.
Use astream() or astream_events() with SSE response format: from fastapi import FastAPI; from fastapi.responses import StreamingResponse; async def stream_endpoint(): async def event_stream(): async for chunk in chain.astream(input): yield f'data: {chunk}\n\n'; return StreamingResponse(event_stream(), media_type='text/event-stream').
For token-level streaming: async for event in chain.astream_events(input, version='v2'): if event['event'] == 'on_chat_model_stream': token = event['data']['chunk'].content; yield f'data: {token}\n\n'. Set headers: {'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive'}. Use stream_mode='messages' for LangGraph agent streaming. Benefits: real-time user feedback, lower perceived latency. Production: handle disconnects, add heartbeat comments, close streams properly. Compatible with EventSource API in browsers.
Production checklist: (1) Use retry with exponential backoff: chain.with_retry(stop_after_attempt=3, wait_exponential_jitter=True), (2) Add fallback models: primary.with_fallbacks([cheap_llm]), (3) Enable caching: set_llm_cache(RedisCache(redis_client)), (4
) Set timeouts: llm.invoke(input, config={'timeout': 30}), (5) Monitor with callbacks: from langchain.callbacks import OpenAICallbackHandler; with OpenAICallbackHandler() as cb: chain.invoke(input); log_cost(cb.total_cost), (6) Use async for concurrency: await
chain.abatch(inputs, config={'max_concurrency': 10}), (7) Validate inputs: use Pydantic models, (8) Handle rate limits: implement token bucket or use with_retry, (9) Structured logging: log chain_id, trace_id, latency, (10) Graceful degradation: return cached/default responses on total failure.

…

Compile graph with checkpointer: graph = graph_builder.compile(checkpointer=checkpointer). Use thread_id for conversation isolation: config = {'configurable': {'thread_id': 'user123'}}; result = graph.invoke(input, config). Each super-step auto-saves checkpoint snapshot. For production: use AsyncSqliteSaver to prevent bottlenecks, or PostgresSaver (pip install langgraph-checkpoint-postgres) for high-traffic apps. MemorySaver suitable only for tutorials/local dev. Checkpointing required for human-in-the-loop, time travel debugging, and error recovery.
Define Pydantic model and parser: from langchain_core.output_parsers import PydanticOutputParser; from pydantic import BaseModel, Field; class Person(BaseModel): name: str = Field(description='Person full name'); age: int = Field(description='Person age in years'); city: str; parser = PydanticOutputParser(pydantic_object=Person).
Add format instructions to prompt: prompt = ChatPromptTemplate.from_messages([('system', 'Extract person info.\n{format_instructions}'), ('human', '{query}')]); chain = prompt | model | parser; result = chain.invoke({'query': 'John is 30 and lives in NYC', 'format_instructions': parser.get_format_instructions()}).

…

Use LangGraph for: (1) Multi-agent systems requiring coordination, (2) Complex workflows with conditional branching, (3) Human-in-the-loop approval steps, (4) State persistence across sessions, (5) Production apps needing fine-grained control. Use legacy AgentExecutor for: simple single-agent prototypes (<10 lines code).
As of 2025, LangChain recommends LangGraph for ALL new agent implementations. Key differences: LangGraph uses explicit StateGraph with checkpointing, AgentExecutor uses implicit loop with deprecated memory classes. LangGraph provides: interrupt_before/after for pausing, time-travel debugging with get_state(), sub-graphs for modular agents, conditional_edges for routing. Migration: Replace AgentExecutor.from_llm_and_tools() with StateGraph + MessagesState + ToolNode pattern. LangGraph production-ready, AgentExecutor maintenance mode only.

…

Initialize with API keys: openai = ChatOpenAI(model='gpt-4-turbo', api_key=os.getenv('OPENAI_API_KEY')); anthropic = ChatAnthropic(model='claude-3-5-sonnet-20241022', api_key=os.getenv('ANTHROPIC_API_KEY')); google = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=os.getenv('GOOGLE_API_KEY')).
Use with fallbacks: chain = prompt | openai.with_fallbacks([anthropic, google]). Or route by task: def route_model(input): return openai if input['complex'] else google; chain = RunnableLambda(route_model) | prompt. All implement BaseChatModel interface - drop-in replacements. Model-specific features: OpenAI parallel tools, Anthropic prompt caching, Gemini 2M token context. Use Anthropic for reasoning tasks, OpenAI for tool calling, Google for long context. Monitor costs per provider with callbacks. Production: A/B test models, route based on latency/cost/quality.

…

Context propagates through: chains, graphs, parallel operations, nested calls. Use for: user permissions, tenant isolation, request tracing, audit logs. Combine with contextvars for global state: from contextvars import ContextVar; request_id_var = ContextVar('request_id'); config = RunnableConfig(metadata={'request_id': request_id_var.get()}). Tags flow to LangSmith/callbacks for filtering. Production: attach auth context, trace IDs, feature flags to config. Config merges when passed through chain levels.

…

For streaming as results complete: async for result in chain.abatch_as_completed(inputs, config={'max_concurrency': 10}): process(result). Benefits: prevent rate limit errors, manage API quota, control resource usage. Common values: 5-20 for API calls, 50-100 for local operations. Example: from langchain_core.runnables import RunnableConfig; config = RunnableConfig(max_concurrency=10, tags=['batch']); results = await llm.abatch(prompts, config=config). Works with all LCEL chains - applies recursively to nested components.

…

LLM responses cached by exact prompt match. For semantic caching: from langchain_community.cache import RedisSemanticCache; from langchain_openai import OpenAIEmbeddings; set_llm_cache(RedisSemanticCache(redis_url='redis://localhost:6379', embedding=OpenAIEmbeddings(), score_threshold=0.95)).
Matches prompts by embedding similarity (0.95 = 95% similar). Alternative: SQLite cache for persistence: from langchain_community.cache import SQLiteCache; set_llm_cache(SQLiteCache(database_path='.langchain.db')). For granular control: llm = ChatOpenAI(cache=True). Disable for specific calls: llm.invoke(prompt, config={'cache': False}). Savings: 80-95% cost reduction for repeated queries. Use semantic cache for FAQ systems, exact cache for deterministic workflows.

…

Bind tool choice to model: from langchain_openai import ChatOpenAI; tools = [search_tool, calculator_tool]; llm = ChatOpenAI(model='gpt-4'); llm_with_tools = llm.bind_tools(tools, tool_choice='auto'). Options: 'auto' = model decides (default), 'required' = must call tool, 'none' = never call tools, {'type': 'function', 'function': {'name': 'search_tool'}} = force specific tool.
For OpenAI parallel function calling: llm.bind_tools(tools, parallel_tool_calls=True) (default since GPT-4-turbo). Use 'required' for: structured extraction, guaranteed action execution. Use 'none' for: pure chat turns, chain-of-thought reasoning. Force specific tool: llm.bind_tools(tools, tool_choice={'type': 'function', 'function': {'name': 'calculator_tool'}}).

…

For tool-calling agents: from langgraph.prebuilt import tools_condition; graph.add_conditional_edges('agent', tools_condition, {'tools': 'tool_node', '**end**': END}). Router receives current state, returns string matching node name. Alternative with path map: graph.add_conditional_edges('node', router, {'path1': 'dest1', 'path2': 'dest2'}). Common patterns: tool execution check, sentiment routing, confidence thresholds, error handling branches. Router must be deterministic for predictable flows. Use END constant for terminal paths. Conditional edges enable dynamic workflows vs static add_edge().
Create few-shot prompt with FewShotChatMessagePromptTemplate: from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate; examples = [{'input': 'happy', 'output': 'sad'}, {'input': 'tall', 'output': 'short'}]; example_prompt = ChatPromptTemplate.from_messages
([('human', '{input}'), ('ai', '{output}')]); few_shot_prompt = FewShotChatMessagePromptTemplate(example_prompt=example_prompt, examples=examples); final_prompt = ChatPromptTemplate.from_messages([('system', 'You are a helpful assistant'), few_shot_prompt, ('human', '{input}')]); chain = final_prompt | model.
For dynamic example selection: from langchain_core.example_selectors import SemanticSimilarityExampleSelector; from langchain_openai import OpenAIEmbeddings; from langchain_community.vectorstores import FAISS; selector = SemanticSimilarityExampleSelector.from_examples(examples, OpenAIEmbeddings(), FAISS, k=2); few_shot = FewShotChatMessagePromptTemplate(example_prompt=example_prompt, example_selector=selector). Benefits: improved task performance, consistent output format. Use semantic selector when >20 examples.
RunnablePassthrough passes input unchanged to next component: chain = RunnablePassthrough() | model (input flows through unmodified). RunnableParallel runs multiple runnables concurrently with same input, returns dictionary of outputs: parallel = RunnableParallel(summary=summarizer, sentiment=classifier); results = await parallel.ainvoke(text).
Use RunnablePassthrough for preserving original input in parallel branches or adding input to chain output. Use RunnableParallel (or dict syntax) for concurrent execution: chain = {'context': retriever, 'question': RunnablePassthrough()} | prompt. Parallel execution uses asyncio.gather internally. Control concurrency with config: parallel.invoke(input, config={'max_concurrency': 5}). Ideal for RAG where retrieval + question pass to prompt simultaneously. RunnableParallel.abatch_as_completed() yields results as they finish.
Use MessagesState pre-built schema for conversations: from langgraph.graph import StateGraph, MessagesState; from langgraph.prebuilt import ToolNode; def agent(state: MessagesState): response = model.invoke(state['messages']); return {'messages': [response]}; graph = StateGraph(MessagesState); graph.add_node('agent', agent); graph.add_node('tools', ToolNode(tools)); graph.set_entry_point('agent'); compiled = graph.compile().
MessagesState includes messages field (list) with automatic reducer that appends new messages (not overwrites). For custom state: from typing_extensions import TypedDict; from typing import Annotated; from operator import add; class State(TypedDict): messages: Annotated[list, add_messages]; count: int. Reducer functions control update behavior - without reducer, updates overwrite. Use StateGraph for workflow orchestration, MessagesState for chat apps.
Get checkpoint history: config = {'configurable': {'thread_id': 'thread1'}}; states = graph.get_state_history(config). Iterate checkpoints: for state in states: print(state.values, state.next, state.checkpoint_id). Load specific checkpoint: checkpoint = states[2]; loaded_state = graph.get_state(config={'configurable': {'thread_id': 'thread1', 'checkpoint_id': checkpoint.checkpoint_id}}).
Update past state: graph.update_state(config, {'approval': True}, as_node='approval_node'); graph.invoke(None, config) # resume from updated state. Use cases: (1) Replay from any point, (2) Fix failed executions, (3) A/B test different paths, (4) Audit decision trails. Requires checkpointer (SqliteSaver/PostgresSaver). Production: store checkpoint_id in database for replay links. Checkpoint includes: state values, next node(s), parent checkpoint, timestamp. Time travel creates branch - original history preserved. Use for: debugging agent reasoning, reproducing bugs, regulatory compliance.