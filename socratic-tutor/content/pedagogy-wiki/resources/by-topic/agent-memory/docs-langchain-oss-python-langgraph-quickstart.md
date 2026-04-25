# Source: https://docs.langchain.com/oss/python/langgraph/quickstart
# Title: Quickstart - Docs by LangChain
# Fetched via: browser
# Date: 2026-04-10

This quickstart demonstrates how to build a calculator agent using the LangGraph Graph API or the Functional API.
Using an AI coding assistant?
Install the LangChain Docs MCP server to give your agent access to up-to-date LangChain documentation and examples.
Install LangChain Skills to improve your agent’s performance on LangChain ecosystem tasks.
Use the Graph API if you prefer to define your agent as a graph of nodes and edges.
Use the Functional API if you prefer to define your agent as a single function.
For conceptual information, see Graph API overview and Functional API overview.
For this example, you will need to set up a Claude (Anthropic) account and get an API key. Then, set the ANTHROPIC_API_KEY environment variable in your terminal.
Use the Graph API
Use the Functional API
​
1. Define tools and model
In this example, we’ll use the Claude Sonnet 4.5 model and define tools for addition, multiplication, and division.
from langchain.tools import tool
from langchain.chat_models import init_chat_model


model = init_chat_model(
    "claude-sonnet-4-6",
    temperature=0
)


# Define tools
@tool
def multiply(a: int, b: int) -> int:
    """Multiply `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a * b


@tool
def add(a: int, b: int) -> int:
    """Adds `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a + b


@tool
def divide(a: int, b: int) -> float:
    """Divide `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a / b


# Augment the LLM with tools
tools = [add, multiply, divide]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)

​
2. Define state
The graph’s state is used to store the messages and the number of LLM calls.
State in LangGraph persists throughout the agent’s execution.
The Annotated type with operator.add ensures that new messages are appended to the existing list rather than replacing it.
from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int

​
3. Define model node
The model node is used to call the LLM and decide whether to call a tool or not.
from langchain.messages import SystemMessage


def llm_call(state: dict):
    """LLM decides whether to call a tool or not"""

    return {
        "messages": [
            model_with_tools.invoke(
                [
                    SystemMessage(
                        content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
                    )
                ]
                + state["messages"]
            )
        ],
        "llm_calls": state.get('llm_calls', 0) + 1
    }

​
4. Define tool node
The tool node is used to call the tools and return the results.
from langchain.messages import ToolMessage


def tool_node(state: dict):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}

​
5. Define end logic
The conditional edge function is used to route to the tool node or end based upon whether the LLM made a tool call.
from typing import Literal
from langgraph.graph import StateGraph, START, END


def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "tool_node"

    # Otherwise, we stop (reply to the user)
    return END

​
6. Build and compile the agent
The agent is built using the StateGraph class and compiled using the compile method.
# Build workflow
agent_builder = StateGraph(MessagesState)

# Add nodes
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)

# Add edges to connect nodes
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node", END]
)
agent_builder.add_edge("tool_node", "llm_call")

# Compile the agent
agent = agent_builder.compile()

# Show the agent
from IPython.display import Image, display
display(Image(agent.get_graph(xray=True).draw_mermaid_png()))

# Invoke
from langchain.messages import HumanMessage
messages = [HumanMessage(content="Add 3 and 4.")]
messages = agent.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()

To learn how to trace your agent with LangSmith, see the LangSmith documentation.
Congratulations! You’ve built your first agent using the LangGraph Graph API.

Full code example

Edit this page on GitHub or file an issue.
Connect these docs to Claude, VSCode, and more via MCP for real-time answers.