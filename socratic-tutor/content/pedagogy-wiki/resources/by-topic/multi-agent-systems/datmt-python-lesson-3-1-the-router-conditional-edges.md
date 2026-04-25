# Source: https://datmt.com/python/lesson-3-1-the-router-conditional-edges/
# Title: Lesson 3.1: The Router (Conditional Edges) - datmt
# Fetched via: jina
# Date: 2026-04-10

Title: Lesson 3.1: The Router (Conditional Edges)



# Lesson 3.1: The Router (Conditional Edges) - datmt

[datmt](https://datmt.com/)

Menu

Menu

*   [Home](https://datmt.com/)
*   [Tutorials](https://datmt.com/python/lesson-3-1-the-router-conditional-edges/#)
    *   [backend](https://datmt.com/category/backend/)
        *   [java](https://datmt.com/category/backend/java/)
            *   [spring](https://datmt.com/category/backend/java/spring/)
            *   [JPA](https://datmt.com/category/backend/java/jpa/)
            *   [javaee](https://datmt.com/category/backend/java/javaee/)

    *   [devops](https://datmt.com/category/devops/)
    *   [frontend](https://datmt.com/category/frontend/)
    *   [Linux](https://datmt.com/category/linux/)
    *   [NoSQL Databases](https://datmt.com/category/databases/nosql-databases/)

*   [Cookie Policy (EU)](https://datmt.com/cookie-policy-eu/)

Discover more

Routers

router

Router

![Image 2](https://datmt.com/wp-content/uploads/2024/05/datmt-youtube-thumbnail.jpg-bc-at-4010.avif)

# Lesson 3.1: The Router (Conditional Edges)

January 31, 2026 by [Đạt Trần](https://datmt.com/author/mtdat171_c/ "View all posts by Đạt Trần")

Networking Equipment

Table of Contents [[hide](https://datmt.com/python/lesson-3-1-the-router-conditional-edges/#)]

*   [1 The Scenario](https://datmt.com/python/lesson-3-1-the-router-conditional-edges/#The_Scenario)
*   [2 The Code](https://datmt.com/python/lesson-3-1-the-router-conditional-edges/#The_Code)
*   [3 Output](https://datmt.com/python/lesson-3-1-the-router-conditional-edges/#Output)

A standard edge (`add_edge`) is like a train track; the train _must_ go there. A conditional edge (`add_conditional_edges`) is like a junction. The graph pauses, looks at the State, and decides which track to take.

Discover more

Software

Scripting Languages

Java (Programming Language)

To implement this, we need a special **Routing Function**. This function doesn’t update the state; it simply returns the _name_ of the next node.

### The Scenario

We are building a Customer Support bot.

*   If the user asks about “Refunds”, send them to the `Refund_Agent`.
*   If they ask about “Tech”, send them to the `Tech_Support`.

### The Code

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END

# --- 1. State ---
class SupportState(TypedDict):
    query: str

# --- 2. Nodes ---
def refund_agent(state):
    print("--- REFUND AGENT: Processing refund request ---")
    return {}

def tech_support(state):
    print("--- TECH AGENT: Have you tried turning it off and on? ---")
    return {}

# --- 3. The Router Logic ---
# This function analyzes the state and returns the NAME of the next node.
def route_query(state) -> Literal["refund_node", "tech_node"]:
    user_query = state["query"].lower()
    if "money" in user_query:
        return "refund_node"
    else:
        return "tech_node"

# --- 4. Build Graph ---
builder = StateGraph(SupportState)

builder.add_node("refund_node", refund_agent)
builder.add_node("tech_node", tech_support)

# Start immediately with the decision
builder.set_entry_point("refund_node") # Just for initialization, see below

# WAIT! We usually need a "Start" node to trigger the router.
# Let's add a dummy start node for clarity.
def classify_node(state):
    print(f"--- CLASSIFYING: {state['query']} ---")
    return {}

builder.add_node("classifier", classify_node)
builder.set_entry_point("classifier")

# ADD CONDITIONAL EDGE
# Syntax: add_conditional_edges(source_node, decision_function, path_map)
builder.add_conditional_edges(
    "classifier",      # After this node runs...
    route_query,       # Run this logic...
    {                  # Map the logic's output to actual Nodes
        "refund_node": "refund_node",
        "tech_node": "tech_node"
    }
)

builder.add_edge("refund_node", END)
builder.add_edge("tech_node", END)

app = builder.compile()

# --- 5. Run ---
print("Run 1:")
app.invoke({"query": "I want my money back"})

print("\nRun 2:")
app.invoke({"query": "My screen is broken"})

Python

65

1

from typing import TypedDict, Literal

2

from langgraph.graph import StateGraph, END

3

​

4

# --- 1. State ---

5

class SupportState(TypedDict):

6

 query: str

7

​

8

# --- 2. Nodes ---

9

def refund_agent(state):

10

 print("--- REFUND AGENT: Processing refund request ---")

11

 return {}

12

​

13

def tech_support(state):

14

 print("--- TECH AGENT: Have you tried turning it off and on? ---")

15

 return {}

16

​

17

# --- 3. The Router Logic ---

18

# This function analyzes the state and returns the NAME of the next node.

19

def route_query(state) -> Literal["refund_node", "tech_node"]:

20

 user_query = state["query"].lower()

21

 if "money" in user_query:

22

 return "refund_node"

23

 else:

24

 return "tech_node"

25

​

26

# --- 4. Build Graph ---

27

builder = StateGraph(SupportState)

28

​

29

builder.add_node("refund_node", refund_agent)

30

builder.add_node("tech_node", tech_support)

31

​

32

# Start immediately with the decision

33

builder.set_entry_point("refund_node") # Just for initialization, see below

34

​

35

# WAIT! We usually need a "Start" node to trigger the router.

36

# Let's add a dummy start node for clarity.

37

def classify_node(state):

38

 print(f"--- CLASSIFYING: {state['query']} ---")

39

 return {}

40

​

41

builder.add_node("classifier", classify_node)

42

builder.set_entry_point("classifier")

43

​

44

# ADD CONDITIONAL EDGE

45

# Syntax: add_conditional_edges(source_node, decision_function, path_map)

46

builder.add_conditional_edges(

47

 "classifier", # After this node runs...

48

 route_query, # Run this logic...

49

 { # Map the logic's output to actual Nodes

50

 "refund_node": "refund_node",

51

 "tech_node": "tech_node"

52

 }

53

)

54

​

55

builder.add_edge("refund_node", END)

56

builder.add_edge("tech_node", END)

57

​

58

app = builder.compile()

59

​

60

# --- 5. Run ---

61

print("Run 1:")

62

app.invoke({"query": "I want my money back"})

63

​

64

print("\nRun 2:")

65

app.invoke({"query": "My screen is broken"})

### Output

Run 1:
--- CLASSIFYING: I want my money back ---
--- REFUND AGENT: Processing refund request ---

Run 2:
--- CLASSIFYING: My screen is broken ---
--- TECH AGENT: Have you tried turning it off and on? ---

Plain Text

7

1

Run 1:

2

--- CLASSIFYING: I want my money back ---

3

--- REFUND AGENT: Processing refund request ---

4

​

5

Run 2:

6

--- CLASSIFYING: My screen is broken ---

7

--- TECH AGENT: Have you tried turning it off and on? ---

![Image 4](https://datmt.com/wp-content/uploads/2025/09/profile-512x512-1.avif)

[Đạt Trần](https://datmt.com/author/mtdat171_c/)

I build [softwares](https://datmt.com/python/lesson-3-1-the-router-conditional-edges/#) that solve problems. I also love writing/documenting things I learn/want to learn.

Networking

[](https://twitter.com/dat_tm24 "Twitter")[](https://github.com/datmt "Github")[](https://www.youtube.com/@datmt_dev "Youtube")

Categories [python](https://datmt.com/category/python/)Tags [conditional node](https://datmt.com/tag/conditional-node/), [langgraph](https://datmt.com/tag/langgraph/), [python](https://datmt.com/tag/python/)

[Lesson 2.2 The Solution: Reducers](https://datmt.com/python/lesson-2-2-the-solution-reducers/)

[Lesson 3.2: The Loop (Cycles)](https://datmt.com/python/lesson-3-2-the-loop-cycles/)

Discover more

opensource

Open Source

Freeware & Shareware

### Leave a Comment [Cancel reply](https://datmt.com/python/lesson-3-1-the-router-conditional-edges/#respond)

Comment

Name Email Website 

Δ



### In this series

This post is a part of the mini series: [Hands-On Langgraph](https://datmt.com/?post_type=bc_mini_series&p=3972)

*   [The LangGraph Architect – Module 1: The Skeleton](https://datmt.com/module/the-langgraph-architect-module-1-the-skeleton/)
    *   [Lesson 1.1: The "Hello World" Graph](https://datmt.com/?p=3986)
    *   [Lesson 1.2: The "Broken Telephone" (Why State Matters)](https://datmt.com/?p=3990)

*   [Module 2: The Memory (Solving Amnesia)](https://datmt.com/module/module-2-the-memory-solving-amnesia/)
    *   [Lesson 2.1 The Problem: The "Overwrite" Bug](https://datmt.com/?p=3998)
    *   [Lesson 2.2 The Solution: Reducers](https://datmt.com/?p=4004)

*   [Module 3: The Brain (Logic & Loops)](https://datmt.com/module/module-3-the-brain-logic-loops/)
    *   [Lesson 3.1: The Router (Conditional Edges)](https://datmt.com/?p=4010)
    *   [Lesson 3.2: The Loop (Cycles)](https://datmt.com/?p=4011)

*   [Architecture](https://datmt.com/category/architecture/)
*   [backend](https://datmt.com/category/backend/)
*   [Clean Code](https://datmt.com/category/clean-code/)
*   [Cloud Computing](https://datmt.com/category/cloud-computing/)
*   [Databases](https://datmt.com/category/databases/)
*   [devops](https://datmt.com/category/devops/)
*   [frontend](https://datmt.com/category/frontend/)
*   [fundamental](https://datmt.com/category/fundamental/)
*   [General Tips](https://datmt.com/category/general-tips/)
*   [git](https://datmt.com/category/software-development/git/)
*   [java](https://datmt.com/category/backend/java/)
*   [javaee](https://datmt.com/category/backend/java/javaee/)
*   [JPA](https://datmt.com/category/backend/java/jpa/)
*   [kubernetes](https://datmt.com/category/devops/kubernetes/)
*   [Linux](https://datmt.com/category/linux/)
*   [management](https://datmt.com/category/management/)
*   [mobile development](https://datmt.com/category/mobile-development/)
*   [network](https://datmt.com/category/network/)
*   [NoSQL Databases](https://datmt.com/category/databases/nosql-databases/)
*   [opensource](https://datmt.com/category/opensource/)
*   [python](https://datmt.com/category/python/)
*   [quarkus](https://datmt.com/category/backend/java/javaee/quarkus/)
*   [rag](https://datmt.com/category/rag/)
*   [RAG Application](https://datmt.com/category/rag-application/)
*   [Relational Databases](https://datmt.com/category/databases/relational-databases/)
*   [scala](https://datmt.com/category/scala/)
*   [Security](https://datmt.com/category/security/)
*   [spring](https://datmt.com/category/backend/java/spring/)
*   [SQL](https://datmt.com/category/databases/sql/)
*   [System Design](https://datmt.com/category/system-design/)
*   [WordPress Development](https://datmt.com/category/wordpress-development/)

Copyright Ⓒ [datmt](https://datmt.com/)

© 2026 datmt • Built with [GeneratePress](https://generatepress.com/)