# Source: https://temporal.io/blog/prototype-to-prod-ready-agentic-ai-grid-dynamics
# Title: From prototype to production-ready agentic AI solution: A use case ...
# Fetched via: trafilatura
# Date: 2026-04-10

What happens when a promising AI agent prototype hits the real world? We found out the hard way.
Building a production-ready AI agent is a significant challenge. At Grid Dynamics, we've developed dozens of agentic solutions, and through that work, we've gained a deep understanding of what it takes to build a durable, scalable system. This case study shares our journey of building a deep research agent using LangGraph, the unexpected challenges we encountered, and why we ultimately migrated to Temporal.
Why is a deep research agent required?[#](#why-is-a-deep-research-agent-required)
Our client, a Fortune 500 manufacturer, runs 100+ plants worldwide and thousands of processes, but its incredibly vast and sophisticated knowledge base is disjointed, unactionable, and has no clear way to browse data.
Our goal was to build a deep‑research agent that searches across internal databases, shared drives, and local repositories. When the agent can’t find a relevant answer from internal data, it expands the search online and cites sources. It clearly labels what’s sourced internally vs. from the open web. Teams now surface the right information in seconds or minutes, sharply reducing time to insight.
LangGraph solution[#](#langgraph-solution)
While our deep research agent quickly evolved from a LangGraph prototype to a production solution, running it in the real world exposed significant challenges that forced us to re-evaluate our architecture.
We found that the LangGraph-based solution, which initially seemed stable and easy to scale, had hidden costs related to development and support. The key issues we faced included:
- Implementing and supporting robust error handling and retry mechanisms.
- Managing internal state, keeping it up-to-date, and debugging issues related to caching.
- The high resource cost of scaling the solution.
- The expense of supporting custom workflows.
The need for 'human-in-the-loop' interactions — where a workflow waits for input — forced us to build a custom error-handling and retry mechanism. While this might seem straightforward, we quickly learned that it required maintaining the workflow’s state manually. This custom implementation often left the workflow in an inconsistent state, making debugging and recovery difficult. This was a significant drain on our development team's resources, shifting their focus from delivering new business value to simply maintaining the existing system.
LangGraph's reliance on Redis for state management created a new set of problems. We had to carefully manage the lifecycle and expiration of state, ensuring common requests weren't accidentally wiped out by newer cache updates. This was not only complex to implement but also costly to support and debug. For instance, an engineer trying to reproduce a bug related to expired state could spend a significant amount of time on a single issue, significantly increasing the overall cost of development and maintenance. As the solution scaled in production, we needed to guarantee that every user request was processed exactly once, with no duplicated agents racing for the same task. To achieve this, our initial implementation used Apache Kafka, where user requests landed and were consumed by a pool of executors.
While this architecture seemed promising, it introduced a new set of 'exactly once' challenges. Our team faced an endless stream of issues, including race conditions, stale state, and agents getting stuck without clear reporting. The solution became extremely costly to support, with no clear path to reducing that burden. It was at this point that we began our search for a new solution — one that could handle workflow management, durability, and flexible retries out of the box since other message brokers add similar implementation concerns.
Temporal as a solution[#](#temporal-as-a-solution)
Our initial architecture, which combined LangGraph with Redis for persistence, was powerful in concept but incredibly brittle in practice. We found ourselves constantly fighting the limitations of our tooling instead of focusing on core business logic. Our migration, therefore, had two clear goals: move away from Redis-based state management and eliminate the need for custom-built workflow orchestration and retry logic.
State management transformation[#](#state-management-transformation)
With Temporal, we experienced a fundamental paradigm shift. Instead of treating state as a separate, fragile object that needed to be carefully managed — like a baton being passed between runners — Temporal allowed us to make state an integral part of the workflow itself. In our new architecture, we defined a Python class that represents our workflow’s state and made it a core variable within the workflow function, eliminating the baton entirely.
This change had a transformative effect. While our LangGraph agent had to manually fetch its state from a Redis key at the beginning of each step, our Temporal Workflow now seamlessly passes the state directly into each activity as an argument. As an Activity completes its work — whether fetching sources, analyzing content, or generating insights — it returns the updated state, which Temporal automatically and durably persists in its event history.
Here is a simplified example using Temporal Workflow:
# ============================================================================
# TEMPORAL APPROACH: State as Integral Part of Workflow
# ============================================================================
@dataclass
class ResearchWorkflowState:
#State as a Python class - core variable within workflow
query: str
sources_found: list
analysis_results: str
@activity.defn
async def fetch_sources_activity(current_state: ResearchWorkflowState) -> ResearchWorkflowState:
# State passed directly as argument - no external fetching
sources = ["source1", "source2"]
# Return updated state (automatically persisted by Temporal)
return ResearchWorkflowState(
query=current_state.query,
sources_found=sources,
analysis_results=current_state.analysis_results
)
@activity.defn
async def analyze_content_activity(current_state: ResearchWorkflowState) -> ResearchWorkflowState:
# State received directly - no Redis lookup needed
analysis = f"Analysis of {len(current_state.sources_found)} sources"
# Return updated state
return ResearchWorkflowState(
query=current_state.query,
sources_found=current_state.sources_found,
analysis_results=analysis
)
@workflow.defn
class ResearchWorkflow:
@workflow.run
async def run(self, initial_query: str) -> ResearchWorkflowState:
# State as a core variable within the workflow
workflow_state = ResearchWorkflowState(
query=initial_query,
sources_found=[],
analysis_results=""
)
# Pass state to activity, get updated state back
workflow_state = await workflow.execute_activity(
fetch_sources_activity,
workflow_state # State passed as argument
)
# Pass updated state to next activity
workflow_state = await workflow.execute_activity(
analyze_content_activity,
workflow_state # Updated state passed as argument
)
return workflow_state
The high-level architecture of the Temporal-based solution is illustrated below: Temporal's implementation helped us overcome the most critical challenges of our Kafka-based architecture, including our custom retry logic, stale state issues, and the inability to gracefully resume execution after a long pause.
By adopting Temporal, our solution became leaner and more efficient, allowing our team to focus on core business logic rather than on complex, low-level system operations like state management.
With that in mind, let's take a closer look at the key changes we made when moving away from LangGraph.
Simplified error handling and retry logic[#](#simplified-error-handling-and-retry-logic)
One of the most satisfying aspects of the migration was the opportunity to delete thousands of lines of custom retry and error handling code. In our LangGraph implementation, every external service call was wrapped in painstaking, hand-crafted try-catch blocks and retry loops designed to handle different types of failures.
Temporal’s approach to resilience is fundamentally different. Instead of embedding complex retry logic throughout our business code, we simply attach RetryPolicy
configurations to our Activity executions within the Workflow.
This declarative approach allowed us to specify backoff intervals, maximum retry attempts, and which types of errors should be retryable — all without cluttering our core research logic. This means our code is now focused solely on what the agent should do, not how to handle every possible failure.
Example:
# Temporal implementation with declarative retry policies
@dataclass
class ResearchState:
sources: List[str]
analysis: str
error_count: int = 0
# Clean activities without embedded retry logic
@activity.defn
async def fetch_sources() -> List[str]:
"""Clean business logic - no retry code needed"""
...
@activity.defn
async def analyze_content(sources: List[str]) -> str:
"""Clean business logic - no retry code needed"""
...
@activity.defn
async def fallback_analysis(sources: List[str]) -> str:
"""Fallback activity for when main analysis fails"""
...
# Advanced retry policies for different scenarios
class RetryPolicies:
"""Centralized retry policy configurations"""
fetch_sources = RetryPolicy(
initial_interval=timedelta(seconds=1),
backoff_coefficient=2.0, # Exponential backoff
maximum_interval=timedelta(seconds=60),
maximum_attempts=4,
non_retryable_error_types=["builtins.ValueError"] # Only retry on specific exceptions
)
analyze_content = RetryPolicy(
initial_interval=timedelta(seconds=5),
backoff_coefficient=1.0, # Linear backoff
maximum_interval=timedelta(seconds=15),
maximum_attempts=3,
# Custom retryable error types
non_retryable_error_types=["builtins.ValueError", "builtins.TypeError"]
)
# Workflow with declarative retry policies
@workflow.defn
class ResearchWorkflow:
@workflow.run
async def run(self) -> ResearchState:
# Fetch sources with declarative retry policy
try:
fetch_sources,
# Declarative retry configuration - no code in business logic!
retry_policy=RetryPolicies.fetch_sources,
start_to_close_timeout=timedelta(minutes=5)
)
except Exception:
# Fallback if all retries exhausted
# Analyze content with different retry policy
try:
analyze_content,
# Different retry policy for analysis
retry_policy=RetryPolicies.analyze_content,
start_to_close_timeout=timedelta(minutes=10)
)
except Exception:
# Fallback analysis with no retries
fallback_analysis,
start_to_close_timeout=timedelta(minutes=2)
# No retry policy = single attempt
)
return state
Effortless scaling[#](#effortless-scaling)
Our original scaling approach with Apache Kafka was a significant engineering undertaking. It required a custom solution where workers would scale based on queue length — a massive, non-reusable investment that we would have had to replicate for every new application.
Temporal’s approach to scalability is elegantly simple and requires minimal configuration. We just configured our Kubernetes deployment to run multiple replicas of our Temporal Worker. These Workers are identical and completely stateless; they simply poll the same task queue on the Temporal server, which automatically handles all load balancing and task distribution.
This fundamental change transformed scaling from a complex engineering project into a simple operational task. If we experience a surge of research requests, we no longer need to panic or initiate emergency engineering projects. Instead, we simply adjust the replica count of our Worker deployment in Kubernetes, and the system scales automatically to meet the demand.
The operational benefits extend beyond just handling traffic spikes. This architecture provided true horizontal scalability that was built once at the platform level. Now, all of our current and future services can leverage this capability without any additional engineering investment.
Architectural decoupling[#](#architectural-decoupling)
The most architecturally significant change in our migration was deconstructing our monolithic LangGraph agent. In our original system, each "node" in the research graph was a Python function that operated on a shared, in-memory state object. These nodes were tightly coupled and often relied on common context, like a single, pre-initialized language model client or shared configuration objects.
To migrate to Temporal, we had to convert each of these tightly coupled nodes into self-contained [Temporal Activities](https://docs.temporal.io/activities). This transformation required us to explicitly define all the data a node needed as serializable arguments for the activity function. Any shared clients or resources could no longer be assumed to exist; their initialization had to be moved inside the activity itself to ensure it could run independently on any worker.
In this transformation, we had to ensure that all inputs and outputs for our Activities were serializable. Our LangGraph state object had evolved to contain complex, in-memory Python objects that couldn’t be sent over the network, making this a non-trivial challenge.
The transition also required us to completely rethink how we managed dependencies like API clients and configuration objects. In the LangGraph system, we could maintain a single, shared client instance for the entire research process. In Temporal, because Activities must be self-contained, our initial, naive approach was to re-initialize clients at the start of every activity, which proved to be both inefficient and slow.
We solved this by implementing intelligent client management within Activities, using techniques like client pooling and lazy initialization. This required us to move from a shared context model to one where each activity was responsible for its own setup, but it resulted in much more predictable and testable code.
Conclusion[#](#conclusion)
Our journey from a LangGraph prototype to a powerful, production-ready Temporal solution has been a masterclass in building scalable agentic systems.
We learned that almost all AI applications and agents require key capabilities: intelligent state management, the ability to retry failed steps without restarting the entire pipeline, and an architecture that scales easily and supports new features.
While many agentic frameworks are excellent for prototyping, turning them into stable, production-ready applications requires significant effort. We've used this article to describe the common pitfalls we faced with our LangGraph implementation and the reasons why Temporal provided a superior path forward.
So, where do you start? Before you write a single line of code, our strong recommendation is to begin by defining the production requirements for your application. Ask yourself critical questions about scalability, inter-agent communication, agent orchestration, and how to integrate guardrails into the workflow. Having solid answers to these questions upfront will help you avoid a costly re-architecture down the line.