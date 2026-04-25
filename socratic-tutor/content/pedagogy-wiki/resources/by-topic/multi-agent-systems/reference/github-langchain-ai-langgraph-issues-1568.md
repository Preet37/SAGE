# Source: https://github.com/langchain-ai/langgraph/issues/1568
# Author: LangChain
# Author Slug: langchain
# Title: Problem with add_messages, message didn't get merged (langgraph issue #1568)
# Fetched via: browser
# Date: 2026-04-10

langchain-ai
/
langgraph
Public
Notifications
Fork 5k
 Star 28.9k
Problem with add_messages, message didn't get merged #1568
New issue
Closed
Description
Yuxuan Wu (CalendulaED)
opened 
Checked other resources
I added a very descriptive title to this issue.
I searched the LangGraph/LangChain documentation with the integrated search.
I used the GitHub search to find a similar question and didn't find it.
I am sure that this is a bug in LangGraph/LangChain rather than my code.
I am sure this is better as an issue rather than a GitHub discussion, since this is a LangGraph bug and not a design question.
Example Code
from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    model = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo")
    print(state)
    return {"messages": [model.invoke(state["messages"])]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    for event in graph.stream({"messages": ("user", user_input)}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)
Error Message and Stack Trace (if applicable)
python my_agent/agent.py
User: Do you know Calculus?
{'messages': [HumanMessage(content='Do you know Calculus?', id='05425ee6-2c31-4c0b-8843-2ca88596e420')]}
Assistant: Yes, I am familiar with Calculus. Calculus is a branch of mathematics that deals with rates of change and accumulation of quantities. It includes topics such as differentiation, integration, limits, and infinite series.
User: Can you make an example?
{'messages': [HumanMessage(content='Can you make an example?', id='e7aee16b-f51d-4dd1-b7d3-ee606278369d')]}
Assistant: Sure! Here is an example:

Sentence: "The cat chased the mouse around the house."

Example: The cat, a sleek and agile tabby with bright green eyes, darted after the small grey mouse as it scurried through the various rooms of the house, knocking over vases and skidding around corners in a frantic attempt to escape.
Description

I follow the first example in quickstart here: https://langchain-ai.github.io/langgraph/tutorials/introduction/#setup
and I try to print the state, and I realized that the message is being replaced rather than appended.
But on the website, it states: "The messages key is annotated with the add_messages reducer function, which tells LangGraph to append new messages to the existing list, rather than overwriting it."

System Info

Name: langgraph
Version: 0.2.15
Summary: Building stateful, multi-actor applications with LLMs
Home-page: https://www.github.com/langchain-ai/langgraph
Author:
Author-email:
License: MIT
Location: /Users/yuxuanwu/opt/anaconda3/envs/langchain/lib/python3.11/site-packages
Requires: langchain-core, langgraph-checkpoint
Required-by:

👍
React with 👍
5
Activity
gbaian10 commented 
gbaian10
 · edited by gbaian10
Edits
Contributor

Insert a checkpoint,
Otherwise, your graph will restart after each run.

from langgraph.checkpoint.memory import MemorySaver

# ...

graph = graph_builder.compile(checkpointer=MemorySaver())
thread_config = {"configurable": {"thread_id": "1"}}

# ...

for event in graph.stream({"messages": ("user", user_input)}, thread_config):

# ...
👍
React with 👍
5
CalendulaED commented 
Yuxuan Wu (CalendulaED)
Author

Insert a checkpoint, Otherwise, your graph will restart after each run.

from langgraph.checkpoint.memory import MemorySaver

# ...

graph = graph_builder.compile(checkpointer=MemorySaver())
thread_config = {"configurable": {"thread_id": "1"}}

# ...

for event in graph.stream({"messages": ("user", user_input)}, thread_config):

# ...

Thank you so much!

🎉
React with 🎉
1
Yuxuan Wu (CalendulaED)
closed this as completed
2BitSalute commented 
2BitSalute (2BitSalute)
 · edited by 2BitSalute
Edits

Thank you for asking the question. I also had the same one while reading the quickstart.

The quickstart says: "This bot can engage in basic conversation by taking user input and generating responses using an LLM."

This is really misleading because it makes it sound like you can actually have a conversation taking turns, but every turn, the LLM only gets the latest message from the user.

The thread thing is required, otherwise you get the following error from graph.stream:

"Checkpointer requires one or more of the following 'configurable' keys: ['thread_id', 'checkpoint_ns', 'checkpoint_id']"

Sign up for free
 to join this conversation on GitHub. Already have an account? Sign in to comment
Metadata
Assignees
No one assigned
Labels
No labels
Type
No type
Fields
Give feedback
No fields configured for issues without a type.
Projects
No projects
Milestone
No milestone
Relationships
None yet
Development
Code with agent mode
No branches or pull requests
Participants
Issue actions