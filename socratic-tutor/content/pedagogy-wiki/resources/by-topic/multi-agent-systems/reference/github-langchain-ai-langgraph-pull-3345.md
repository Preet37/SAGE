# Source: https://github.com/langchain-ai/langgraph/pull/3345
# Author: LangChain
# Author Slug: langchain
# Title: feature: Dynamic Workflow Mode Implementation for Conditional Edges (PR #3345)
# Fetched via: trafilatura
# Date: 2026-04-10

feature:Dynamic Workflow Mode Implementation for Conditional Edges#3345
[Wenpan Li (WenPulse)](/WenPulse)wants to merge 1 commit into
[langchain-ai:main](/langchain-ai/langgraph/tree/main)from
[feature:Dynamic Workflow Mode Implementation for Conditional Edges](#top)#3345[Wenpan Li (WenPulse)](/WenPulse) wants to merge 1 commit into[langchain-ai:main](/langchain-ai/langgraph/tree/main)from
[feature:Dynamic Workflow Mode Implementation for Conditional Edges](#top)#3345
[Wenpan Li (WenPulse)](/WenPulse)wants to merge 1 commit into
[langchain-ai:main](/langchain-ai/langgraph/tree/main)from
Conversation
|
The latest updates on your projects. Learn more about 1 Skipped Deployment
| Feb 10, 2025 3:25am |
|
[Wenpan Li (WenPulse)](/WenPulse)
[force-pushed](/langchain-ai/langgraph/compare/2a4acb6c29181fe40f815d654045e23377900682..7a9bbe974763db7c9480a99d49d6cc87deb9dec6)the lwp/feature/add_workflow_mode branch from
[to](/langchain-ai/langgraph/commit/2a4acb6c29181fe40f815d654045e23377900682)
2a4acb6
7a9bbe9
[Compare](/langchain-ai/langgraph/compare/2a4acb6c29181fe40f815d654045e23377900682..7a9bbe974763db7c9480a99d49d6cc87deb9dec6)
February 7, 2025 03:14
[Wenpan Li (WenPulse)](/WenPulse)changed the title
Feb 7, 2025
[Wenpan Li (WenPulse)](/WenPulse)
[force-pushed](/langchain-ai/langgraph/compare/7a9bbe974763db7c9480a99d49d6cc87deb9dec6..98bd6438e83c125dc1fa2f29257efac66649ee2c)the lwp/feature/add_workflow_mode branch from
[to](/langchain-ai/langgraph/commit/7a9bbe974763db7c9480a99d49d6cc87deb9dec6)
7a9bbe9
98bd643
[Compare](/langchain-ai/langgraph/compare/7a9bbe974763db7c9480a99d49d6cc87deb9dec6..98bd6438e83c125dc1fa2f29257efac66649ee2c)
February 7, 2025 08:16
[Nuno Campos (nfcampos)](/nfcampos)
left a comment
[Nuno Campos (nfcampos)](/nfcampos)left a comment
There was a problem hiding this comment.
Hi, this would change langgraph to be a library for DAGs, which is very much the opposite of what we want, as we started langgraph with the explicit goal of supporting graphs with cycles
My goal is to provide clients with low-code workflow configuration capabilities, offering functional nodes that users can freely arrange and combine as needed, without requiring programmers to manually write specific processes. In my practical tests, I found that only condition_edges had discrepancies with the actual execution results. To address this, I temporarily fixed the issue using a monkey patch. However, I recognize that this is not a long-term solution, which is why I submitted this PR to provide a more robust fix. For example, as shown in my previous example, I simply added a D node after the B node. This does not change the overall execution logic of the workflow, yet it results in completely different execution outcomes. Specifically, whether the E node executes once or twice depends not on the actual execution logic but on whether the number of nodes following the B and C nodes is consistent. I believe this execution behavior is not rigorous. These changes aim to provide a clearer and more reliable execution path for workflows. In fact,in my usage scenario, both langgraph with workflow_mode and langgraph without workflow_mode coexist simultaneously. The workflow is inherently a tool for user-defined processes, functioning similarly to other tools by providing output based on given input data. The PR I submitted is solely intended to fix issues in the original langgraph during workflow execution. Ultimately, the tools are invoked within agents, where the timing and repetition of calls are managed by the agent's langgraph (langgraph without workflow_mode). These two versions of langgraph can exist concurrently and operate completely independently without interfering with each other. |
[Wenpan Li (WenPulse)](/WenPulse)
[force-pushed](/langchain-ai/langgraph/compare/d37f07d513c24a8a44990f225c37bc79d55db0b6..7b725f873a022ea86de326bbfc851840c29a7730)the lwp/feature/add_workflow_mode branch from
[to](/langchain-ai/langgraph/commit/d37f07d513c24a8a44990f225c37bc79d55db0b6)
d37f07d
7b725f8
[Compare](/langchain-ai/langgraph/compare/d37f07d513c24a8a44990f225c37bc79d55db0b6..7b725f873a022ea86de326bbfc851840c29a7730)
February 10, 2025 03:21
[Wenpan Li (WenPulse)](/WenPulse)
[force-pushed](/langchain-ai/langgraph/compare/7b725f873a022ea86de326bbfc851840c29a7730..263bbd9bbbe7e8a4e5904fd596fb79b6806adf17)the lwp/feature/add_workflow_mode branch from
[to](/langchain-ai/langgraph/commit/7b725f873a022ea86de326bbfc851840c29a7730)
7b725f8
263bbd9
[Compare](/langchain-ai/langgraph/compare/7b725f873a022ea86de326bbfc851840c29a7730..263bbd9bbbe7e8a4e5904fd596fb79b6806adf17)
February 10, 2025 03:24
|
Given Nuno's comment above, I don't think it makes sense to keep this open. Feel free to open an issue if you'd like to discuss this feature further! |
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)
[Sign up for free](/join?source=comment-repo)to join this conversation on GitHub. Already have an account?
[Sign in to comment](/login?return_to=https%3A%2F%2Fgithub.com%2Flangchain-ai%2Flanggraph%2Fpull%2F3345)
Overview
Building upon the existing LangGraph framework, I developed and implemented a complete workflow in my project. I discovered that using
add_conditional_edges
in the workflow had certain flaws in executing subsequent nodes. By applying monkey patch, I temporarily fixed the issues related to conditional node execution within the workflow and designed an Analyzer to maintain the directed graph of execution paths. This improvement allows users to enable the new execution mode by settingworkflow_mode=True
during compilation. If not set or set toFalse
, the original execution mode is used by default. I hope this approach can be adopted.Problem Description
Prerequisite: In the workflow, each node should execute only once unless special handling logic is set.
When handling conditional branches with LangGraph, the following execution issues were discovered:
Set up a selector node (A) with two executable branches, Type 1 and Type 2:
When the results of both types point to Node E, LangGraph's parallel processing mechanism causes Node E to execute only once.
Attempts in Existing LangGraph:
Since each node is dynamically generated, specific branch paths cannot be determined before workflow execution. Therefore, it is necessary to dynamically choose the appropriate path during execution.
Solution
Added an Analyzer to LangGraph's source code to achieve the aforementioned requirements. Its main functionalities include:
Execution in this Case:
Through these improvements, each node executes only once within the workflow. The trigger conditions for subsequent nodes are dynamically adjusted based on the actual execution paths, catering to different types of text processing requirements.
Usage
To use the improved execution mode in LangGraph, set
workflow_mode=True
incompile
. The specific steps are as follows:Set the Option:
Add
workflow_mode=True
in the compilation configuration to enable the dynamic workflow mode.Note: When
workflow_mode=True
, either thepath_map
parameter or aLiteral
return is required. Only one of them is needed. Thepath_map
orLiteral
must cover all possible execution paths.Default Behavior:
If not set or if
workflow_mode
is set toFalse
, the original execution mode of LangGraph is used, maintaining backward compatibility.