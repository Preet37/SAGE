# Source: https://reference.langchain.com/javascript/langchain-langgraph/index/ConditionalEdgeRouter
# Title: ConditionalEdgeRouter | @langchain/langgraph (JavaScript Reference)
# Fetched via: search
# Date: 2026-04-10

# ConditionalEdgeRouter
> **Type Alias** in `@langchain/langgraph`
📖 [View in docs](https://reference.langchain.com/javascript/langchain-langgraph/index/ConditionalEdgeRouter)
Type for conditional edge routing functions.
Use this to type functions passed to `addConditionalEdges` for
full type safety on state, runtime context, and return values.
**Supports two patterns:**
1. **Single schema pattern** - Single schema:
`ConditionalEdgeRouter<Schema, Context, Nodes>`
2. **Type bag pattern** - Separate schemas for state, context:
`ConditionalEdgeRouter<{ Schema; ContextSchema; Nodes }>`
## Signature
```javascript
ConditionalEdgeRouter: IsConditionalEdgeRouterTypeBag<Schema> extends true ?
(state: ExtractBagInput<Schema, unknown>, config: LangGraphRunnableConfig<ExtractBagContext<Schema, Record<string, unknown>>>) => ConditionalEdgeRouterReturnValue<ExtractBagNodes<Schema, string>, ExtractBagInput<Schema, unknown>> | Promise<ConditionalEdgeRouterReturnValue<ExtractBagNodes<Schema, string>, ExtractBagInput<Schema, unknown>>> : (state: ExtractStateType<Schema>, config: LangGraphRunnableConfig<Context>) => ConditionalEdgeRouterReturnValue<Nodes, ExtractStateType<Schema>> | Promise<ConditionalEdgeRouterReturnValue<Nodes, ExtractStateType<Schema>>>
```
## Examples
### Example 1
```typescript
type MyContext = { userId: string };
const router: ConditionalEdgeRouter<typeof AgentState, MyContext, "agent" | "tool"> =
(state, config) => {
const userId = config.context?.userId;
if (state.done) return END;
return state.needsTool ? "tool" : "agent";
};
graph.addConditionalEdges("router", router, ["agent", "tool"]);
```
### Example 2
```typescript
const router: ConditionalEdgeRouter<{
Schema: typeof StateSchema;
ContextSchema: typeof ContextSchema;
Nodes: "agent" | "tool";
}> = (state, config) => {
if (state.done) return END;
return "agent";
};
```
---
[View source on GitHub](https://github.com/langchain-ai/langgraphjs/blob/9e9807523f751ddcbad8023706563a24806ef50e/libs/langgraph-core/src/graph/types.ts#L550)

## ​ Graphs
At its core, LangGraph models agent workflows as graphs.
You define the behavior of your agents using three key components: 1.
`State`: A shared data structure that represents the current snapshot of your application.
It can be any data type, but is typically defined using a shared state schema.
2. `Nodes`: Functions that encode the logic of your agents.
They receive the current state as input, perform some computation or side-effect, and return an updated state.
3. `Edges`: Functions that determine which `Node` to execute next based on the current state.
They can be conditional branches or fixed transitions.
By composing `Nodes` and `Edges`, you can create complex, looping workflows that evolve the state over time.
…
## ​ State
The first thing you do when you define a graph is define the `State` of the graph.
The `State` consists of the schema of the graph as well as `reducer` functions which specify how to apply updates to the state.
The schema of the `State` will be the input schema to all `Nodes` and `Edges` in the graph, and can be either a `TypedDict` or a `Pydantic` model.
All `Nodes` will emit updates to the `State` which are then applied using the specified `reducer` function.
…
## ​ Edges
Edges define how the logic is routed and how the graph decides to stop.
This is a big part of how your agents work and how different nodes communicate with each other.
There are a few key types of edges: - Normal Edges: Go directly from one node to the next.
- Conditional Edges: Call a function to determine which node(s) to go to next.
- Entry Point: Which node to call first when user input arrives.
- Conditional Entry Point: Call a function to determine which node(s) to call first when user input arrives.
A node can have multiple outgoing edges.
If a node has multiple outgoing edges, **all** of those destination nodes will be executed in parallel as a part of the next superstep.
…
### ​ Conditional edges
If you want to **optionally** route to one or more edges (or optionally terminate), you can use the `add_conditional_edges` method.
This method accepts the name of a node and a “routing function” to call after that node is executed:
```
graph.add_conditional_edges("node_a", routing_function)
```
Similar to nodes, the `routing_function` accepts the current `state` of the graph and returns a value.
By default, the return value `routing_function` is used as the name of the node (or list of nodes) to send the state to next.
All those nodes will be run in parallel as a part of the next superstep.
You can optionally provide a dictionary that maps the `routing_function`’s output to the name of the next node.
```
graph.add_conditional_edges("node_a", routing_function, {True: "node_b", False: "node_c"})
```
…
### ​ Conditional entry point
A conditional entry point lets you start at different nodes depending on custom logic.
You can use `add_conditional_edges` from the virtual `START` node to accomplish this.
```
from langgraph.graph import START
graph.add_conditional_edges(START, routing_function)
```
You can optionally provide a dictionary that maps the `routing_function`’s output to the name of the next node.
```
graph.add_conditional_edges(START, routing_function, {True: "node_b", False: "node_c"})
```
…
You can then access and use this context inside a node or conditional edge:

## At A Glance!
##### Apr 25, 2025 (0:20:00)
Supercharge your LangGraph workflows with Routers! 🚦 In this deep-dive tutorial, I walk you through everything you need to know about routing logic in LangGraph, from basic conditional edges to advanced tool-based routing—all with hands-on coding examples.
What you’ll learn:
🔹 What is a Router in LangGraph – Why and when to use it
🔹 Adding a Router as a Node – Step-by-step with real code
🔹 Conditional Edges – How to define and control graph flow based on state
🔹 Router in Tool Calling – Tackling real-world complexity
🔹 ToolNode & tools_condition – Explained in-depth, LangGraph-style

This video is a complete walkthrough—perfect for anyone building complex agentic workflows using LangGraph.

…

Till now
{ts:39} we have seen one node goes to the other node with the help of an edge. But what if there is a scenario where one node
{ts:48} has to move from itself to more than one number of nodes based on some conditions. So in that case router
{ts:57} comes.
So in short if I say based on a specific criteria or a condition the state defines whether to move to node A
{ts:67} or to node B. That conditional thing is nothing but a router. That node which decides this
{ts:76} particular thing is known as a router. Now we'll take the same example of what we have seen before for building a
{ts:84} simple graph that is the block generator agent. Taking that same example, we'll move on to add a simple router inside it
{ts:92} and we'll see how we can add it. Now obviously if you look at the graph below for this particular case, we have a
{ts:99} simple start node.
It goes to the blog outline generator and it generates the outline for the blog whatever query user
{ts:106} puts and then the outline with the query goes to the blog generator node and it generates
{ts:113} the final blog and then the entire flow ends. Now if I want to add one router in this particular case now let's take a
{ts:124} simple router. Basically the user will put a query and it will go to the router. The router will decide whether
{ts:130} that query is safe or not. If it is safe, then this entire execution should happen. If it is unsafe, then the
{ts:137} control should directly go to the end node.
This simple router we are going to implement in this particular flow. And
{ts:145} later on, we'll also see how we can use that router in calling a tool like we are going to simply loop a particular
{ts:152} tool to itself based on some conditions and how it works. we are going to look into that.
So obviously if you want a
{ts:160} router in this particular case you will be requiring one more node. So I'll build that particular node here. So like
{ts:166} other nodes I have given the name of this particular node as guard. So basically this guards this guard node is
{ts:173} taking the state that is the block state that we already have defined here and it returns the block state itself.
Now one
{ts:180} more thing we need to add into the block state is that the guard status that what exactly is the status is the status of
{ts:188} the query whether it is safe or unsafe we are going to store into it so I'll simply create a variable guard
{ts:195} result and that will be a string next now what I'll do is I'll simply take in the

…

If it is safe then return safe
{ts:227} otherwise just return unsafe. Strictly provide the result without any explanation at all. So this simple
{ts:233} prompt I have written and I'm going to pass this particular prompt with the query into the LLM and LLM will just
{ts:239} give me a response safe or unsafe and based on that I'll decide whether to route to the next node or to end the

…

Now that we have defined this particular node, now
{ts:301} we have to register this particular node into the graph and also we have to register the edges associated with this
{ts:308} particular node. So let's do that. So if I scroll down over here, you can see here we have defined all the nodes.
{ts:315} Similarly, I'll be defining one more node that is the guard node. I'll give the same name of the guard node as guard
{ts:322} itself as the function. Now that we have registered the node, we'll now set the edges. Now for this particular case, our
{ts:330} entry point won't be the block outline generator.
It will be the guard node itself. So first the query will hit the
{ts:337} guard node. After setting the entry point, I'll have to add a conditional edge. Now over here let me clear let me
{ts:345} clear what exactly a conditional edge is. Now whenever this scenario comes wherever you have one node uh next to
{ts:354} that you don't have a single node to route you have more than one node to route. So in that case you just use
{ts:362} the add conditional edges function inside the state graph class. So what I'll do is I'll write graph
{ts:370} dot add.
Now there is something called as conditional edge. Now inside this conditional edges
{ts:382} what we have to write is first thing is that we need to write the name of the node from where we want to route. So
{ts:391} I'll write guard node. Now that we have defined from where we have to go now we'll also

…

Now once we have got this particular value from the
{ts:439} state we now have from where to go and we also have the value of the note that it gave. Now here we can define the
{ts:447} condition. Condition can be defined in a dictionary. I'll write a simple dictionary over here.
Your keys will be
{ts:454} whatever possible classes your router is going to provide and the value will be where you have to route from that
{ts:461} particular class that you have got from the guard node. So for my guard node whatever I have defined I have two
{ts:468} classes.

…

The keys
{ts:492} will be the all possible values that is in our case it is safe and unsafe. So for safe let's say if this lambda
{ts:499} function returns safe as the output from the guard node we have to define safe as the key of the dictionary and the value
{ts:507} to it will be the name of the node where we have to route next if the output comes as safe.

…

{ts:529} all. I want the graph to end its flow. So I'll simply define the value to it as end E and D. That's
{ts:538} it. So this is how you have to write the conditional edges. First from where you have to go name that node. Next whatever
{ts:545} value you have got just fetch that and store it in the second parameter. And third is you have you can define the
{ts:553} conditions based on the condition the graph will route and that's it. Other things we
{ts:560} have as it we have to keep as it is because uh once the flow goes to the blog outline generator next it has to go

…

Next I have simply
{ts:814} created two nodes. One is the tool calling LLM node wherein it takes in the messages state. It's the default state
{ts:821} from the graph and it returns the messages and it returns the update to the messages key with the value from
{ts:832} with the value that we get from the lm for that particular query that user puts.

…

So whatever
{ts:851} state you have got updated by simply calling that particular node previously tool calling LLM. Whatever state has got
{ts:860} updated you just you will put that state again and you will pass it on to the tool node so that the tool node will
{ts:867} execute whatever message AI message you have got from the previous node and it will uh it will give it and it will
{ts:874} provide the further output whether it is a tool output or whether it is an AI message. So now we simply have created
{ts:881} the state graph. Inside that we have added the node tool calling lm and the tools node. Next we have added the edge
{ts:889} start to the tool calling lm.
So this is going to be the entry point of the graph. Next we have defined the
{ts:897} conditional edge. Now this is where the router comes. Now over here I have defined the name of the node which acts
{ts:902} as a router. So tool calling lm since it's the first node where the flow goes, it is going to act as a router.
And the
{ts:909} second parameter to this particular is nothing but the tools condition. So again this is one of the pre-built from
{ts:915} lang graph tools condition. If you look into the documentation of it uh you can simply use in conditional edge to route
{ts:922} to the tool node if the last message has tool calls otherwise the route to the end.
So basically you don't you don't
{ts:928} have to define your own custom logic in here. Just use the tools condition pre-built. So basically when
{ts:935} you define it, it will simply route your call to the LLM and whatever output it gets based on the output. Let's say if

…

If it is not a tool message, if it is an simple AI message, natural language message,
{ts:964} then it will simply return that particular natural language message as the output. So this is the function of
{ts:969} the tools condition pre-built and then we have simply added the edge tools to the end and we have
{ts:978} compiled the graph and let's execute this. So you can see how it is working. First it first the control goes to the
{ts:986} tool calling LLM. If based on the output of the tool calling LLM if it is a tool message then
{ts:993} the tools the tools node will send it to the respective tools for further processing.

…

{ts:1078} the add tool call add tool wherein the arguments were first process this whatever output you get that will be
{ts:1089} first argument and then the second argument is two. Next again what it has done is it has called the tools. Now the
{ts:1096} control goes over here in the tools state in the tools node.

# Advanced LangGraph: Implementing Conditional Edges and Tool-Calling Agents
## LangGraph Advanced Tutorial (9 Part Series)
1 Two Basic Streaming Response Techniques of LangGraph 2 Advanced Features of LangGraph: Summary and Considerations ...
5 more parts...
3 Building Complex AI Workflows with LangGraph: A Detailed Explanation of Subgraph Architecture 4 Checkpoints and Human-Computer Interaction in LangGraph 5 Advanced Techniques in LangGraph: Tips for Using Message Deletion in Graph Structure Applications 6 Advanced LangGraph: Building Intelligent Agents with ReACT Architecture 7 Advanced LangGraph: Implementing Conditional Edges and Tool-Calling Agents 8 Introduction to LangGraph: Core Concepts and Basic Components 9 Analysis of Limitations of LCEL and AgentExecutor
…
## Advanced Usage of Conditional Edges
Conditional edges are one of the most powerful features in LangGraph, allowing us to dynamically decide the execution flow based on the state.
Let's explore some advanced usages.
### 1.
Multi-condition Routing
```
from typing import List, Dict, Literal
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
class AgentState(BaseModel):
messages: List[Dict[str, str]] = []
current_input: str = ""
tools_output: Dict[str, str] = {}
status: str = "RUNNING"
error_count: int = 0
def route_by_status(state: AgentState) -> Literal["process", "retry", "error", "end"]:
"""Complex routing logic"""
if state.status == "SUCCESS":
return "end"
elif state.status == "ERROR":
if state.error_count >= 3:
return "error"
return "retry"
elif state.status == "NEED_TOOL":
return "process"
return "process"
# Build the graph structure
workflow = StateGraph(AgentState)
# Add conditional edges
workflow.add_conditional_edges(
"check_status",
route_by_status,
{
"process": "execute_tool",
"retry": "retry_handler",
"error": "error_handler",
"end": END
}
)
```
### 2.
Parallel Execution
LangGraph supports parallel execution of multiple nodes, which is particularly useful for handling complex tasks:
```
async def parallel_tools_execution(state: AgentState) -> AgentState:
"""Parallel execution of multiple tools"""
tools = identify_required_tools(state.current_input)
async def execute_tool(tool):
result = await tool.ainvoke(state.current_input)
return {tool.name: result}
# Execute all tools in parallel
results = await asyncio.gather(*[execute_tool(tool) for tool in tools])
# Merge results
tools_output = {}
for result in results:
tools_output.update(result)
return AgentState(
messages=state.messages,
current_input=state.current_input,
tools_output=tools_output,
status="SUCCESS"
)
```
…
### 1.
Define State and Tools
```
from typing import List, Dict, Optional
from pydantic import BaseModel
from langchain.tools import BaseTool
from langchain.tools.calculator import CalculatorTool
from langchain.tools.wikipedia import WikipediaQueryRun
from langchain_core.language_models import ChatOpenAI
class Tool(BaseModel):
name: str
description: str
func: callable
class AgentState(BaseModel):
messages: List[Dict[str, str]] = []
current_input: str = ""
thought: str = ""
selected_tool: Optional[str] = None
tool_input: str = ""
tool_output: str = ""
final_answer: str = ""
status: str = "STARTING"
# Define available tools
tools = [
Tool(
name="calculator",
description="Used for performing mathematical calculations",
func=CalculatorTool()
),
Tool(
name="wikipedia",
description="Used for querying Wikipedia information",
func=WikipediaQueryRun()
)
]
```
### 2.
Implement Core Nodes
```
async def think(state: AgentState) -> AgentState:
"""Think about the next action"""
prompt = f"""
Based on user input and current conversation history, think about the next action.
User input: {state.current_input}
Available tools: {[t.name + ': ' + t.description for t in tools]}
Decide:
1. Whether a tool is needed
2. If needed, which tool to use
3. What parameters to call the tool with
Return in JSON format: {{"thought": "thought process", "need_tool": true/false, "tool": "tool name", "tool_input": "parameters"}}
"""
llm = ChatOpenAI(temperature=0)
response = await llm.ainvoke(prompt)
result = json.loads(response)
return AgentState(
**state.dict(),
thought=result["thought"],
selected_tool=result.get("tool"),
tool_input=result.get("tool_input"),
status="NEED_TOOL" if result["need_tool"] else "GENERATE_RESPONSE"
)
async def execute_tool(state: AgentState) -> AgentState:
"""Execute tool call"""
tool = next((t for t in tools if t.name == state.selected_tool), None)
if not tool:
return AgentState(
**state.dict(),
status="ERROR",
thought="Selected tool not found"
)
try:
result = await tool.func.ainvoke(state.tool_input)
return AgentState(
**state.dict(),
tool_output=str(result),
status="GENERATE_RESPONSE"
)
except Exception as e:
return AgentState(
**state.dict(),
status="ERROR",
thought=f"Tool execution failed: {str(e)}"
)
async def generate_response(state: AgentState) -> AgentState:
"""Generate the final response"""
prompt = f"""
Generate a response to the user based on the following information:
User input: {state.current_input}
Thought process: {state.thought}
Tool output: {state.tool_output}
Please generate a clear and helpful response.
"""
llm = ChatOpenAI(temperature=0.7)
response = await llm.ainvoke(prompt)
return AgentState(
**state.dict(),
final_answer=response,
status="SUCCESS"
)
```
### 3.
Build the Complete Workflow
```
# Create graph structure
workflow = StateGraph(AgentState)
# Add nodes
workflow.add_node("think", think)
workflow.add_node("execute_tool", execute_tool)
workflow.add_node("generate_response", generate_response)
# Add edges
workflow.add_edge("think", "execute_tool", condition=lambda s: s.status == "NEED_TOOL")
workflow.add_edge("execute_tool", "generate_response", condition=lambda s: s.status == "GENERATE_RESPONSE")
workflow.add_edge("generate_response", "think", condition=lambda s: s.status == "SUCCESS")
```

In today’s video, I’ll show you how to use conditional edges and improve the quality of the generated code by more than 200%! We will use LangGraph and Pydantic, along with structured output from LLMs.

We’ll start by building a 4-agent network with LangGraph. Then, we’ll use Pydantic and JSON to parse and validate the agent responses into structured data, and then use the values a conditional edge method. Watch the graph results improve with each code review iteration!

…

### Transcript
{ts:0} today we're going to build a simple Network composed of two agents a
{ts:4} developer agent will take input from the user and create a simple app the code reviewer agent will take the code
{ts:11} generated by developer assign a code review quality score along with comments and send it back for refinement the

…

EnV and from typing we're going to import typ deck we're going to use type Deck with our state graph later on from
{ts:133} Lang graph graph we're going to use State graph start and end nodes we're also going to use add messages so that
{ts:139} our agents can add messages from typing we're going to use annotated in our state graph for our model today we're
{ts:145} going to stick with Azure chat open AI can implement this with any llm that you like including open AI or local olama
{ts:153} models the only condition here is the model must support agent calls finally from Lang chain core messages we're
{ts:160} going to import AI message human message and system message next let's call our L EnV function so that we load our
{ts:168} environment variables now for this I've prepared an environment example where I am including the Azure open end point
{ts:176} API key version and deployment names as well as the the Lang chain tracing endpoint as well as the Lang chain API
{ts:183} key these are optional and in your case you may need to provide your open AI keys and if you're using a different llm
{ts:189} you may want to provide their respective keys back to our file here we load our environment variables and now let's
{ts:196} define a constant that will hold the maximum tokens for our llm here we're going to Define that we're going to use
{ts:203} max tokens as 500 next let's define our state and in this case we're going to use type dect passing into the graph
{ts:210} State and our messages list will be just from annotated in basic messages next we're going to create the graph and the
{ts:217} graph will be just as before State graph and passing the state to the state graph object now let's define our llm and for
{ts:226} this we're going to use the Azure chat open AI by passing various environment variables from our environment file once
{ts:233} our llm is defined now let's define our agents for today's example we're going to have a graph with four agents we're
{ts:241} going to start with an initialization state which will basically just print in it and the state and just return the
{ts:248} messages in this case the initialization State doesn't do much but it's a good practice to start your graph with an

…

{ts:298} you'll see that separating human AI in system messages produces better results overall okay so we have the messages
{ts:305} ready now let's invoke our llm and we'll print the code generated at the same time we're going to return the generated
{ts:312} code as a message to the graph so that's our developer agent very simple code generation agent next let's add a
{ts:320} summary agent the job of the summary agent will be just to summarize what's been done in the graph and print the end
{ts:327} State now that we've defined three agents let let's add them to the graph we're going to do that by builder. add
{ts:334} node and then passing the name of the agent in this case we'll have initialization developer and summary a
{ts:341} very simple graph next let's define our edges and for this we're going to Define our entry point as the init from init it
{ts:349} will go to developer from developer to summary and from summary to end before we can run the graph we have to compile
{ts:355} it and to do that we just use builder. compile method we're not not passing any memories or configs we're just going to
{ts:362} do a simple builder. compile now we're going to draw a picture of the graph and we're going to use a mermaid format to
{ts:369} Output the visualization of the graph once that's done we're ready to run the graph we're going to create a main Loop
{ts:375} function here and then we're going to call the main Loop function later on while the user input is anything but
{ts:382} quit exit or Q the loop will continue and the graph will invoke with messages and the human message from the user
{ts:389} input so that's as simple as it gets let's get a quick overview one more time we're starting with three agents
{ts:396} starting with the init then the developer then the summary agent then there's a sequential execution of the
{ts:402} graph and this should just generate a code based on the user input I'm going to save the file open the integrated
{ts:408} terminal and run our first graph okay so now the prompt is awaiting input from user so let's just give it a simple
{ts:416} input The Prompt is write a simple Hello World app in JavaScript as we can see the init agent kicked in and reset our
{ts:423} state and now the developer agent is starting with developer start and then the developer agent has ended and the
{ts:431} summary state is printing our messages and this is the code generated so let's take a look at the code basically here
{ts:439} is the content of the message certainly below is a simple example heror application in JavaScript which is

…

{ts:469} add a code review agent which which will execute right after the developer agent and print code review feedback for the
{ts:477} developer agent to do that we're going to Define reviewer agent right after developer and add it to our graph and
{ts:485} add an age for it so let's just go ahead and do that first let's add our reviewer agent it will print reviewer start and

…

{ts:518} separating the system message for the reviewer agent and finally we'll invoke the llm with messages and return
{ts:526} messages now let's just add the node here under developer okay so now we've added the node and now we need to change
{ts:534} our edges so from developer it should go to reviewer so let's come here and copy this and we're going to

…

{ts:624} code Reviewer is analyzing the code structure the naming convention code quality overall score is assigned a
{ts:631} score 950 on a scale of thousand so it's excellently serves and that's the code reviewer finally the summary agent kicks
{ts:640} in and just prints out the state all in all it's again a pretty simple graph with two main nodes developer and the
{ts:648} reviewer and now what we'd like to do here is add a little bit more logic if the code reviewer's quality score is
{ts:658} below a certain threshold we'd like the graph to redirect back to developer so that the node can rewrite the code and
{ts:666} send it to the code reviewer we'd like to add a conditional logic to our graph execution whereby certain nodes can
{ts:674} execute based on a condition code reviewer agent will check the quality of the code generated and if it does not
{ts:681} meet the criteria which will be defined by a threshold score it will be sent back to the developer and this will
{ts:689} iterate a number of times in our case we're going to use a threshold of 850 and we're going to execute the loop
{ts:699} three times so for three times the code reval agent will send the code back execution back to the developer and the
{ts:708} developer will rewrite the code at the end of the third iteration the code quality score is still below the
{ts:714} threshold then we'll end the graph so let's add that logic for this we're going to use structure Ed output and
{ts:720} we're going to use llm from structured output we're also going to use pantic classes so let's change our application
{ts:727} by adding this logic as well as the conditional edges to our graph we're going to start by importing certain
{ts:734} classes from pantic those are going to be base model and field and from typing we're going to import literal we're
{ts:742} going to add two constants one will be for the number of iterations so we're going to call this number iterations and
{ts:748} we're going to set this to two and the next one will be for the quality threshold let's define two pantic models
{ts:755} that we will use for the structured output for our llms the first pantic model will represent our developer
{ts:762} output and we're going to call that generate code and the second one will represent the code reviewer output and
{ts:768} we're going to call that quality score here we're going to define the pantic model generate code with two parameters
{ts:776} code will hold the generated code and number of words we're just going to use this field to hold the number of tokens

…

{ts:804} like to change our graph state to hold quality and the number of iterations between agents we're just going to add
{ts:812} the quality as an integer as well as the number of iterations that the coder viewer has requested reviews let's
{ts:819} define our structured llm and for this we're going to create two variables the first one we're going to call developer

…

{ts:898} invocation how we invoke the llm and we're going to change what we print so instead of message. content we're going
{ts:905} to use message. code now and then returning instead of message. content again we're going to return message.
{ts:914} code and the number of iterations in our state as you can see here we're printing message. code and what we're returning
{ts:926} is message. code in the messages so we only want to return the code as a message but then we're also setting the
{ts:933} iterations variable inside our state to the state variable plus one so we're just incrementing iterations here by one
{ts:942} this is important because later on we'll check the N iterations the number of iterations to determine when to pass the
{ts:951} control back to the developer node okay that's all the changes we need to make for the developer node now we also need
{ts:957} to make similar changes our reviewer node let's start with changing our system prompt here and for this we're
{ts:964} just going to again instruct the agent to respond with Json and in this case with the score and the comment keys in
{ts:973} the Json so that's one change secondly we're going to change the invocation of the llm so instead of this llm we're
{ts:980} going to use the new llm that we created this variable and we're going to change that
{ts:986} and here uh instead of do content we're just going to print the review and the score as defined in our pantic model so
{ts:997} let's go ahead and delete these and here we're going to call the reviewer structured lm.
{ts:1003} invoke and we're going to create two variables one for the score which will be the returned message. score the other
{ts:1009} one for the comment which will be the message.com we're going to print both of them and here we're going to add a

…

{ts:1042} that's all we need to do in our reviewer now let's add a conditional Edge to our reviewer note this will add a
{ts:1049} conditional Edge by using add conditional Edge to our viewer node and with the method called quality gate
{ts:1056} condition we're going to write this method next next change we need to make is remove this Edge from reviewer to
{ts:1062} summary because our conditional Edge will determine the next node the reviewer may choose based on the output
{ts:1070} of this quality gate to send the execution logic to summary or back to developer so we need to remove this Edge
{ts:1080} now let's write our method so this will be a method to determine based on the number of iterations and the quality
{ts:1088} threshold whether to return the execution logic back to developer or to summary and here in the add conditional
{ts:1097} edges method our reviewer node will use this to determine as the output whether to send it to developer or summary and
{ts:1107} by the way it goes to developer and then it checks for the number of iterations so we'll see how many
{ts:1115} iterations this has been passed and based on that this constant we've defined up here currently we said two
{ts:1123} but since it starts from zero it's actually three time execution and then it will look at the
{ts:1130} Quality score and if the quality threshold is not met it will send the execution flow to developer and if the
{ts:1137} quality gate is met it will send it to summary but if number of iterations is equal to the constant defined then it
{ts:1146} will go straight to summary that means we've tried a number of times to improve the code and no more Improvement is
{ts:1153} possible this is our conditional Edge and keep in mind that these methods can be quite flexible and by utilizing State

…

{ts:1376} standard of expectation we're going to go back to our terminal clear and execute our graph with these new
{ts:1383} parameters and let's give it another example here create a react component to calculate the mass of the Earth this
{ts:1390} time we ask the graph to run five times so this is iteration one and let's see what our agent came up with import react