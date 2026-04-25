# Source: https://arxiv.org/pdf/2506.11266.pdf
# Author: Benjamin Elder et al.
# Title: Invocable APIs derived from NL2SQL datasets for LLM Tool-Calling (Live API Bench)
# Fetched via: trafilatura
# Date: 2026-04-10

Live API-Bench: 2500+ Live APIs for Testing Multi-Step Tool Calling
Abstract
Large language models (LLMs) increasingly rely on external tools and APIs to execute complex tasks specified in natural language. Evaluating such tool-calling capabilities in realistic enterprise settings is challenging: APIs are often proprietary, heterogeneous, and difficult to share, limiting reproducible benchmarks. To address this, we introduce Live API Bench, a comprehensive benchmark constructed by transforming NL2SQL datasets into interactive API environments. Our pipeline converts SQL queries from BIRD-SQL into executable API sequences across three formulations—SLOT, SEL, and REST—covering minimal general-purpose operations, domain-specific multi-step tasks, and function-oriented RESTful interactions, respectively. The benchmark spans 11 databases with over 2,500 invocable tools, paired with human-authored queries, ground-truth API sequences, and verified final answers. Live API Bench enables systematic evaluation of core challenges in tool use, including error handling, sequential reasoning, parameter generation, response parsing, and robustness across diverse domains. We evaluate 10 LLMs and 4 ReACT agents, observing low task completion rates (7–47%), which improve modestly to 50% under interactive agent settings, highlighting substantial scope for improving LLM tool-calling performance. We release all code and data associated with this paper.
Live API-Bench: 2500+ Live APIs for Testing Multi-Step Tool Calling
Benjamin Elder††thanks: Equal contribution. IBM Research AI benjamin.elder@ibm.com Anupama Murthi* IBM Research AI anupama.murthi@ibm.com Jungkoo Kang IBM Research AI jungkoo.kang@ibm.com
Ankita Rajaram Naik IBM Research AI ankita.naik@ibm.com Kiran Kate IBM Research AI kakate@us.ibm.com Kinjal Basu IBM Research AI kinjal.basu@ibm.com
Danish Contractor IBM Research AI danish.contractor@ibm.com
1 Introduction
Large language models (LLMs) are increasingly deployed in real-world applications where they must interact with external tools and APIs to accomplish complex tasks expressed in natural language (Yao et al., [2023](https://arxiv.org/html/2506.11266v2#bib.bib19); Xu et al., [2023a](https://arxiv.org/html/2506.11266v2#bib.bib18)). Such systems are deployed with access to tools that interact with live environments to accomplish tasks, often in response to a user’s request expressed in natural language (Yoran et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib21); Drouin et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib23); Pan et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib22); Xie et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib9); Zheng et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib20)). This capability—commonly referred to as tool-calling—is critical in enterprise environments, where business workflows depend on programmatic access to databases, web services, and specialized software systems via standardized API interfaces.111[https://shorturl.at/bpsps](https://shorturl.at/bpsps),222[https://shorturl.at/daoEp](https://shorturl.at/daoEp)
| Benchmarks | Core Features | Deployment | Evaluation | |||||||
| Hand- | Invocable APIs | Nested API | Code Tools | Live API | Accessible | Real-World data | Ground Truth | # | # | |
| Crafted Queries | for Data Creation | Sequences | as Functions | endpoints | DB | powering API | Sequences | Instances | Tools | |
|
NesTools (Han et al.,
|
[2024b](https://arxiv.org/html/2506.11266v2#bib.bib26))[2023b](https://arxiv.org/html/2506.11266v2#bib.bib48))[2024](https://arxiv.org/html/2506.11266v2#bib.bib36))[2023b](https://arxiv.org/html/2506.11266v2#bib.bib24))[2023](https://arxiv.org/html/2506.11266v2#bib.bib38))[2023](https://arxiv.org/html/2506.11266v2#bib.bib34))[2023](https://arxiv.org/html/2506.11266v2#bib.bib33))[2024](https://arxiv.org/html/2506.11266v2#bib.bib35))[2024d](https://arxiv.org/html/2506.11266v2#bib.bib42))[2025](https://arxiv.org/html/2506.11266v2#bib.bib39))Evaluating LLM tool-calling in realistic deployment settings remains an open challenge: real-world APIs are proprietary, heterogeneous, and difficult to share, which hinders reproducibility. Prior benchmarks thus often rely on simulations, limited domains, or small scales (see Section [2](https://arxiv.org/html/2506.11266v2#S2)). To approximate some of the deployment challenges while retaining reproducibility, we build our benchmark from NL2SQL datasets. This design offers three advantages: (1) NL2SQL tasks involve large, diverse databases, (2) they include human-authored natural language queries with guaranteed executable interpretations, and (3) SQL queries can be systematically decomposed into semantically equivalent API-call sequences that highlight practical tool-calling difficulties.
Building on these insights, we introduce Live API Bench, a comprehensive benchmark for evaluating LLM tool-calling by transforming NL2SQL resources into interactive API environments. Our data transformation pipeline converts NL2SQL queries from BIRD-SQL (Li et al., [2023a](https://arxiv.org/html/2506.11266v2#bib.bib15))—one of the largest and most diverse permissively licensed333Licensed under CC BY-SA 4.0 NL2SQL datasets—into executable API sequences across three complementary formulations:
-
•
SLOT — A minimal set of general-purpose APIs (e.g., filter, sort, aggregate) that often require multiple sequential invocations with varying parameters.
-
•
SEL — An expanded collection combining domain-specific retrieval functions with general-purpose operations, requiring models to select tools and compose multi-step execution plans.
-
•
REST — A function-oriented formulation where queries can typically be resolved through careful function selection and parameter specification, modeling RESTful API interactions.
Live API Bench provides fully accessible APIs that can be hosted locally, allowing LLMs and agents to interact with live endpoints during evaluation. Additionally, by deriving APIs from executable SQL queries over real-world databases, our benchmark ensures deterministic, verified final answers, addressing common limitations in existing tool-calling benchmarks (see Table [1](https://arxiv.org/html/2506.11266v2#S1.T1)). This setup enables systematic evaluation of tool use with realistic challenges including:
-
•
Error handling — APIs may fail or return malformed responses, requiring models to manage failures and timeouts.
-
•
Sequential tool calls — Tasks often involve chaining dependent API calls; our dataset includes sequences of up to eight calls.
-
•
Parameter generation — Models must generate appropriate arguments, validate inputs, and infer missing information to bridge natural language queries and structured API schemas.
-
•
Response parsing — Successful tool use requires interpreting complex outputs, extracting relevant information (frequently from large API outputs), and recognizing mismatches with intended requests.
-
•
Scale and diversity — To avoid overfitting, models are evaluated across diverse domains, API types, and query complexities.
Contributions. In summary, this paper makes the following contributions: (1) We develop novel data transformation pipelines that repurpose existing NL2SQL tasks for evaluating LLM tool-calling, (2) We generate three distinct API formulations—SLOT, SEL, and REST—to study different aspects of tool-calling. Using the 11 publicly available NL2SQL databases from the BIRD-SQL dev set (Li et al., [2023a](https://arxiv.org/html/2506.11266v2#bib.bib15)), we create over 2,500 invocable tools backed by real databases. Each tool is paired with human-authored natural language queries, a ground-truth API sequence, and a verified final answer. To our knowledge, this is the largest publicly available collection of live, invocable APIs with these characteristics. (3) Finally, we evaluate 10 LLMs and 4 ReACT agents (Yao et al., [2023](https://arxiv.org/html/2506.11266v2#bib.bib19)) on these collections, finding extremely low task completion rates (7–47%) that improve modestly to 50% when models interact with the live API environment as ReACT agents, highlighting substantial room for improvement in LLM tool-calling capabilities. We release all code and data associated with this paper.
2 Related Work
The emergence of powerful LLMs has spurred the development of data generation pipelines that produce training and evaluation datasets for tool-calling tasks. Such datasets typically consist of a collection of APIs, along with natural language queries paired with ground-truth API calls or sequences of calls (Liu et al., [2024d](https://arxiv.org/html/2506.11266v2#bib.bib42); Shi et al., [2025](https://arxiv.org/html/2506.11266v2#bib.bib1); Qin et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib35); Basu et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib40); Pereira et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib41)).
Data generation pipelines generally fall into two categories. Some repurpose existing datasets and queries, leveraging pre-existing data for tool-calling tasks (Peng et al., [2021](https://arxiv.org/html/2506.11266v2#bib.bib31); Basu et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib40)). Others use LLMs to synthesize realistic queries conditioned on API collections (Qin et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib35); Tang et al., [2023](https://arxiv.org/html/2506.11266v2#bib.bib33); Liu et al., [2024b](https://arxiv.org/html/2506.11266v2#bib.bib26); Pereira et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib41); Basu et al., [2025](https://arxiv.org/html/2506.11266v2#bib.bib39); Zhong et al., [2025](https://arxiv.org/html/2506.11266v2#bib.bib30)). Beyond queries, some work also focuses on generating APIs themselves from structured sources such as textbooks or documentation, which can then be used in tool-calling tasks (Liu et al., [2025](https://arxiv.org/html/2506.11266v2#bib.bib2)).
Methods for data generation are often tailored to the function-calling scenario. Some pipelines generate queries that invoke a single function, potentially multiple times (Tang et al., [2023](https://arxiv.org/html/2506.11266v2#bib.bib33); Xu et al., [2023b](https://arxiv.org/html/2506.11266v2#bib.bib24)), others focus on queries requiring the invocation of multiple functions including sequencing, and nested function calls (Liu et al., [2024b](https://arxiv.org/html/2506.11266v2#bib.bib26); Yan et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib37); Basu et al., [2025](https://arxiv.org/html/2506.11266v2#bib.bib39); Zhong et al., [2025](https://arxiv.org/html/2506.11266v2#bib.bib30)).
To assess the planning and task-resolution capabilities of tool-calling LLMs, recent benchmarks that provide live environments for agents to interact with have also been developed (Ruan et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib27); Yao et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib28); Cao et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib7); Xie et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib9); Zhou et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib29)).
While existing work sometimes includes queries and APIs that were created using live APIs available from proprietary sources (Chen et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib25); Qin et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib35); Basu et al., [2025](https://arxiv.org/html/2506.11266v2#bib.bib39); Yan et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib37); Zhong et al., [2025](https://arxiv.org/html/2506.11266v2#bib.bib30)), such APIs are usually either unavailable for live agents attempting to answer queries at test time or are only available as paid services by the providers hosting the APIs (eg: RapidAPI Hub).444[http://www.rapidapi.com](http://www.rapidapi.com) In contrast, our work expands on these prior efforts by generating APIs that can be hosted locally either as endpoints or python tools for use by LLMs (and agents). Further, since our method for API construction relies on the executable SQL queries from the original NL2SQL datasets, we’re also able to provide a deterministic and verified ground-truth final-answer, which can be lacking in some tool-calling datasets (Qin et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib35); Liu et al., [2024b](https://arxiv.org/html/2506.11266v2#bib.bib26)).
Recently, benchmarks that assess the capabilities of LLMs on Data Science tasks have been created (Jing et al., [2025](https://arxiv.org/html/2506.11266v2#bib.bib13)). In contrast to our work such benchmarks require models to solve tasks by generating structured query languages or code (Liu et al., [2024c](https://arxiv.org/html/2506.11266v2#bib.bib12); Li et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib11)).
To the best of our knowledge, our work is the first to demonstrate how NL2SQL datasets can be used to study LLM tool-calling by re-purposing them to provide a collection of invocable APIs backed by real-world data and reusing real-world natural language queries available in the original datasets.
3 Dataset
We construct three NL2API datasets—SLOT, SEL, and REST—using 11 databases from the BIRD development set (Li et al., [2023a](https://arxiv.org/html/2506.11266v2#bib.bib15)). Each dataset includes: (i) OpenAPI specifications for available APIs, (ii) Live API implementations, (iii) natural language (NL) questions paired with ground-truth API invocation sequences (with slot values), and (iv) the corresponding databases. We only retain samples where the generated API sequences produce results identical to the original SQL queries, Figure [1](https://arxiv.org/html/2506.11266v2#S2.F1) (top) shows an example of an NL2SQL instance.
BIRD Collection: BIRD is one of the largest collections of real-world databases paired with crowd-sourced NL queries and their SQL statements. The development set averages 7 tables, 73 columns, and 358K rows per database. Queries are often complex, involving multiple joins, aggregations, comparisons, and matches, which translate into multi-step API sequences with challenging sequencing and nesting. Many queries also require reasoning over domain knowledge, synonyms, and numeric values.
3.1 SLOT-BIRD (Slot-Filling Version)
The SLOT-BIRD version of the dataset was constructed by decomposing generic SQL SELECT queries into their constituent parts and mapping each part to an API implemented as a Python function (tool). The design of these APIs is motivated by similar collections used in enterprise applications, such as Tableau555[https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_concepts_filtering_and_sorting.htm](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_concepts_filtering_and_sorting.htm) or Google Analytics.666[https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/FilterExpression](https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/FilterExpression)
Functions: Joins in the SQL query are handled collectively during an initialization step, implemented programmatically at evaluation time. This step produces a single table, which serves as the starting point for a model or agent to access via APIs when answering the query.777While it would be possible to require models to perform JOINs themselves, our experiments show that they already struggle on this dataset without this added complexity. The SLOT-BIRD setup focuses on planning a sequence of data manipulation and access operations using seven APIs:
aggregate_data, filter_data, group_data_by, retrieve_data, select_unique_values, sort_data, transform_data
Each function corresponds to a specific part of an SQL query, such as WHERE, ORDER BY, or COUNT.
Slot Values: The functions in the SLOT-BIRD API pool have two types of parameters (slots) that must be filled:
-
1.
Schema-agnostic slots: Control operations on the data, e.g., the type of condition in a WHERE clause or the sort order (ascending/descending).
-
2.
Column-specific slots: Specify which columns to use for operations such as filtering, sorting, and selecting after manipulations. These slots are categorical, corresponding to the columns in the joined table from the initialization step. Each column includes a brief description of its contents.
When a tool argument must be chosen from the column set, the OpenAPI specification includes an enum of allowed names and their descriptions. Correctly understanding these names and descriptions constitutes the primary challenge for a tool-calling model or agent on this dataset.
Ground-Truth API Sequence:
In the example in Listing [2](https://arxiv.org/html/2506.11266v2#LST2), filter_data (Lines 1, 5) and retrieve_data (Line 9) are two functions. The first invocation of filter_data takes two slot values: the first (Line 2) is a domain-specific slot schools_Magnet, and the second (Line 3) is a control operation that executes an equal_to comparison on the other slot. This is followed by another filter_data call and finally a retrieve_data call.
In addition to the function name and arguments, a label is provided, referencing the output of the tool call. This allows subsequent steps to access previous outputs, since models cannot reliably manipulate large data objects across function calls. As shown in Line 4 of Listing [2](https://arxiv.org/html/2506.11266v2#LST2), we use files to pass payloads and reference them as input arguments. Models are not responsible for reading or writing these files; this is handled automatically by our evaluation framework. For SLOT-BIRD, all tools except retrieve_data save the results of their data manipulation operations into CSV files and return the file path as a string.
Ground-truth API sequences were constructed programmatically for each NL2SQL instance by parsing the SQL query with the Sqlglot Python library888[https://github.com/tobymao/sqlglot](https://github.com/tobymao/sqlglot) and mapping nodes in the resulting syntax tree to tools from the SLOT-BIRD API pool. The output of each ground-truth API sequence is equivalent (up to minor reformatting) to executing the original SQL query on the underlying databases. This output gold answer enables measuring the completion rate of a model or agent, i.e., the proportion of times it produces a sequence of tool calls that leads to the correct result.
| Dataset | # Queries | # Tools | #Tools Avail./ | # Tool Calls/ | # Slots/ |
| Query | Query | Query | |||
| SLOT-BIRD | 665 | 7 | 7 | 2.7 | 3.29 |
| SEL-BIRD | 651 | 1256 | 49 | 2.9 | 0.05 |
| REST-BIRD | 1257 | 1250 | 125 | 1 | 1.38 |
3.2 SEL-BIRD (Selection Version)
The SEL-BIRD variant is derived from SLOT-BIRD by expanding categorical function arguments into separate functions. Specifically, each possible value of a categorical argument is bound to create a new function with one fewer input parameter.
For example, in the SLOT-BIRD API pool, the function ‘filter_data‘ has a categorical argument ‘condition‘, which can take values such as ‘equal_to‘ (Listing [2](https://arxiv.org/html/2506.11266v2#LST2): Line ) or ‘greater_than‘ (Listing [2](https://arxiv.org/html/2506.11266v2#LST2): Line ). In the SEL-BIRD pool, these become distinct functions—‘select_data_equal_to‘ (Listing [3](https://arxiv.org/html/2506.11266v2#LST3): Line ) and ‘select_data_greater_than‘ (Listing [3](https://arxiv.org/html/2506.11266v2#LST3): Line )—which no longer require a ‘condition‘ argument. This transformation yields a substantially larger set of tools for data manipulation.
Additional Domain-Specific Functions: The expansion is even greater for data retrieval. Rather than passing a column name as an argument (as in SLOT-BIRD), the SEL-BIRD pool provides a dedicated ‘get‘ function for each column key (Listing [3](https://arxiv.org/html/2506.11266v2#LST3): Line ). Consequently, the available toolset varies across instances, since the columns in the initialized table depend on the JOINs specified in the underlying SQL query.
3.3 REST-BIRD Version
API Design: The REST-BIRD dataset extends the expansion strategy of SEL-BIRD to the extreme, assigning a dedicated REST endpoint to every instance in the NL2SQL dataset. We adopt a RESTful design to leverage meaningful path parameters, resulting in highly specific and interpretable endpoints. For example, in Listing [4](https://arxiv.org/html/2506.11266v2#LST4), the original NL query is mapped directly to a single API endpoint (Line ).
Since BIRD contains only ‘SELECT‘ queries, all requests in REST-BIRD are GET; no POST, PUT, or DELETE requests are included.
Data Generation: REST-BIRD produces a very large number of database-specific endpoints, with each user query answered by exactly one API call.
Instead of manually authoring these endpoints, we employ Mistral-Large999[https://huggingface.co/mistralai/Mistral-Large-Instruct-2411](https://huggingface.co/mistralai/Mistral-Large-Instruct-2411) within an agentic pipeline consisting of four stages:
(i) Code Generation Agent — synthesizes FastAPI server code,
(ii) De-duplication Agent — merges functionally equivalent endpoints (e.g., getEmployees vs. getAllEmployees),
(iii) API Execution Module, and
(iv) Verifier and Filtering Agent — ensures that the generated endpoint produces results identical to the original SQL query. Any instances where the results do not match are discarded and excluded from the dataset. Complete details of this component and the overall data generation process are provided in the Appendix.
The pipeline outputs Python-based FastAPI server code, dockerized and deployed as microservices, resulting in hosted, executable REST APIs.
4 Experiments
We use our three datasets to answer the following research questions (i) Do models find the automatically generated API collections challenging?, (ii) How are models affected by the size of the API tool set provided for the task of function selection?, (iii) To what extent do models rely on semantic signals from the function name to solve the task?, (iv) How does the performance improve when models are employed as ReACT agents that can interact with live APIs?
4.1 Models and Prompt Formats
We experiment with the following models: Llama 3.1-8B-Instruct and Llama 3.3-70b-instruct (Grattafiori et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib44)), Qwen2.5-7b-instruct and Qwen2.5-72b-instruct (Yang et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib43)), DeepSeek-v3 (Liu et al., [2024a](https://arxiv.org/html/2506.11266v2#bib.bib45)), GPT4o-2024-08-06 (Hurst et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib46)), Granite 3.1-8b-instruct101010[https://huggingface.co/ibm-granite/granite-3.1-8b-instruct](https://huggingface.co/ibm-granite/granite-3.1-8b-instruct), as well as Hammer-7b (Lin et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib47)), and Watt-8b111111[https://huggingface.co/watt-ai/watt-tool-8B](https://huggingface.co/watt-ai/watt-tool-8B) which are specialized tool-calling models.
For all evaluations on SLOT and SEL, we adopt a prompting format similar to that used in NESTful (Basu et al., [2025](https://arxiv.org/html/2506.11266v2#bib.bib39)), as these datasets involve multiple nested API sequences. For evaluations on REST, we follow a prompting format similar to that used in BFCL Yan et al. ([2024](https://arxiv.org/html/2506.11266v2#bib.bib37)). GPT4o limits tool names to 64 characters121212[https://community.openai.com/t/function-call-description-max-length/529902](https://community.openai.com/t/function-call-description-max-length/529902), so we experiment with two settings: providing APIs as ‘tools’131313[https://platform.openai.com/docs/assistants/tools](https://platform.openai.com/docs/assistants/tools) or embedding them directly in the prompts. All LLM prompt templates are included in Appendix E.
Our input data is formatted to ensure a structured and reliable mechanism for referencing tool outputs, a crucial aspect of tool calling, that allows subsequent tool calls to utilize the results of previous execution. This is achieved by assigning a unique variable name to each tool call that ensures that each tool’s output can be distinctly identified and referenced. This approach is particularly important and prevents ambiguity when multiple instances of the same tool, with different arguments, appear within the same tool call sequence (e.g., parallel tool call). With the help of unique identifiers for each tool call, we facilitate clear and efficient tool chaining that ensures the tool dependencies are correctly resolved. All models are required to follow a specified format included in the prompt (Appendix E).
Output Parsing: Although models are instructed to produce outputs in JSON format, they often deviate, leading to instruction-alignment errors that reflect genuine deployment failures. Since proper tool-formatting is essential for functional tool calling, these deviations highlight a critical gap in current models’ ability to reliably interface with API systems. To ensure fair evaluation while preserving parseable outputs, we employ robust, model-specific output parsers, as described in Appendix G.
ReACT Agents: ReACT agents (Yao et al., [2023](https://arxiv.org/html/2506.11266v2#bib.bib19)) use LLMs to plan one tool call at a time, execute the tool and use the observation to plan the next step. We chose to experiment with larger architecture models over smaller ones, as in early experiments even larger models performed poorly when invoked directly as LLMs without an agent.
4.1.1 Metrics
Intent: For evaluating all models, we report a position-aware intent precision, recall, and metrics using a ground-truth API sequence as reference. When a tool call needs to be called more than once but with different slot-values, it is important to track each instance of a function invocation thus, its sequence of invocation.
Slots: Additionally, we report precision, recall and metrics for slots - i.e., the arguments for each function. The slot metrics are conditional on the correct ground-truth intent being predicted but slots are not penalized for missing ground-truth intents. Overall performance, should therefore always be studied along with the Intent metrics.
Completion Rate (Compl. Rate): Finally, we report the completion rate i.e., the proportion of all instances where the the models were able to return the ground-truth response.
| Model | Intent | Slot | Compl. | ||||
| P | R | F1 | P | R | F1 | Rate | |
| SLOT-BIRD | |||||||
| DeepSeek-V3 | 0.82 | 0.54 | 0.65 | 0.67 | 0.67 | 0.67 | 0.07 |
| GPT4o-2024-08-06 (Prompt) | 0.31 | 0.15 | 0.20 | 0.71 | 0.71 | 0.71 | 0.03 |
| GPT4o-2024-08-06 (Tools) | 0.90 | 0.52 | 0.66 | 0.43 | 0.42 | 0.42 | 0.03 |
| Granite-8b-instruct | 0.63 | 0.53 | 0.58 | 0.44 | 0.41 | 0.43 | 0.00 |
| Hammer2.1-7b | 0.88 | 0.35 | 0.50 | 0.67 | 0.67 | 0.67 | 0.03 |
| Llama-3.1-8B-instruct | 0.58 | 0.09 | 0.16 | 0.61 | 0.62 | 0.61 | 0.00 |
| Llama-3.3-70b-instruct | 0.75 | 0.22 | 0.34 | 0.65 | 0.03 | 0.05 | 0.00 |
| Mixtral-8x22B-instruct | 0.78 | 0.63 | 0.70 | 0.63 | 0.62 | 0.62 | 0.02 |
| Qwen2.5-7b-instruct | 0.65 | 0.67 | 0.66 | 0.63 | 0.63 | 0.63 | 0.03 |
| Qwen2.5-72b-instruct | 0.80 | 0.63 | 0.71 | 0.61 | 0.61 | 0.61 | 0.06 |
| Watt-tool-8b | 0.43 | 0.20 | 0.27 | 0.51 | 0.52 | 0.52 | 0.01 |
| SEL-BIRD | |||||||
| DeepSeek-V3 | 0.44 | 0.28 | 0.34 | 0.45 | 0.44 | 0.44 | 0.09 |
| GPT4o-2024-08-06 (Prompt) | 0.42 | 0.39 | 0.4 | 0.47 | 0.46 | 0.46 | 0.09 |
| GPT4o-2024-08-06 (Tools) | 0.47 | 0.30 | 0.36 | 0.62 | 0.57 | 0.59 | 0.0 |
| Granite-3.1-8b-Inst | 0.05 | 0.05 | 0.05 | 0.21 | 0.18 | 0.2 | 0.0 |
| Hammer2.1-7b | 0.29 | 0.16 | 0.21 | 0.47 | 0.4 | 0.43 | 0.03 |
| Llama-3.1-8B-Inst | 0.11 | 0.01 | 0.02 | 0.28 | 0.26 | 0.27 | 0.0 |
| Llama-3-3-70b-Inst | 0.41 | 0.11 | 0.17 | 0.25 | 0.01 | 0.02 | 0.0 |
| Mixtral-8x22B-Inst | 0.6 | 0.5 | 0.55 | 0.45 | 0.44 | 0.44 | 0.04 |
| Qwen2.5-7b-Inst | 0.16 | 0.29 | 0.2 | 0.39 | 0.39 | 0.39 | 0.04 |
| Qwen2.5-72b-Inst | 0.55 | 0.48 | 0.51 | 0.46 | 0.46 | 0.46 | 0.16 |
| Watt-tool-8b | 0.46 | 0.1 | 0.16 | 0.43 | 0.45 | 0.44 | 0.01 |
| REST-BIRD | |||||||
| DeepSeek-V3 | 0.65 | 0.50 | 0.57 | 0.77 | 0.74 | 0.76 | 0.31 |
| GPT4o-2024-08-06 (Prompt) | 0.82 | 0.54 | 0.65 | 0.79 | 0.79 | 0.79 | 0.38 |
| Granite-8b-instruct | 0.45 | 0.58 | 0.50 | 0.77 | 0.76 | 0.77 | 0.34 |
| Hammer2.1-7b | 0.70 | 0.22 | 0.34 | 0.89 | 0.86 | 0.87 | 0.17 |
| Llama-3.1-8B-instruct | 0.22 | 0.57 | 0.31 | 0.76 | 0.76 | 0.76 | 0.32 |
| Llama-3.3-70b-instruct | 0.57 | 0.67 | 0.61 | 0.76 | 0.76 | 0.76 | 0.42 |
| Mixtral-8x22B-instruct | 0.46 | 0.39 | 0.42 | 0.78 | 0.77 | 0.77 | 0.24 |
| Qwen2.5-7b-instruct | 0.53 | 0.52 | 0.53 | 0.80 | 0.80 | 0.80 | 0.37 |
| Qwen2.5-72b-instruct | 0.66 | 0.65 | 0.66 | 0.82 | 0.82 | 0.82 | 0.47 |
| Watt-tool-8b | 0.60 | 0.64 | 0.62 | 0.78 | 0.76 | 0.77 | 0.43 |
4.2 Performance of Models
SLOT-BIRD: Recall that this dataset has general tools and the models need to populate appropriate slot for each invocation of a general tool and also sequence them correctly to accomplish the task. As can be seen from Table [3](https://arxiv.org/html/2506.11266v2#S4.T3), this is very challenging task for all models. While the set of APIs to choose from is small, they need to be invoked more than once - this is reflected in the relatively high precision as compared to recall in intent metrics. We find that Qwen2.5-72b-instruct performs best on the intent selection task though DeepSeek-V3 manages to pair them with the most correct slot-values and reports the highest completion rate (%).
SEL-BIRD: This dataset has domain specific tools available that reduce the need to invoke general tools repeatedly. As can be seen from Table [3](https://arxiv.org/html/2506.11266v2#S4.T3), models have lower precision and recall as compared to SLOT-BIRD suggesting that models do not select and sequence right set of tools. As compared to SLOT-BIRD, all models have lower scores when comparing slots. Notably Granite, has a severe drop in performance on this dataset while the others drop by approx. (absolute) F1 points. As before, based on the completion rates Qwen-72b-instruct and DeepSeek-v3 are the top two performing models.
REST-BIRD: Finally, in this version of the dataset every query uniquely maps to one invocation and the primary task is of intent selection and then correctly populating the slots. Of the three datasets, this appears to be the one where models have most success with significantly higher intent selection rates (no sequencing needed). While the Qwen-2.5-72b-instruct model continues to be a top-performer, smaller models such as Granite-3.1-8b-instruct and Watt-tool-8b perform better than DeepSeek-v3 and GPT-4o. A closer investigation reveals that for this dataset DeepSeek generates chain-of-thought texts that is relatively harder to standardize for parsing and GPT-4o tends to answer the question instead of picking the function call. Refer to Appendix [G](https://arxiv.org/html/2506.11266v2#A7) for examples from our evaluation.
Task Completion Rates: Models struggle on multi-step function-sequencing tasks, achieving near-zero completion on SLOT-BIRD and SEL-BIRD, and only modest rates on REST-BIRD, far below levels needed for practical deployment. GPT-4o (2024-08-06) reaches 38% on REST-BIRD, 9% on SEL-BIRD, and 3% on SLOT-BIRD. For comparison, GPT-4-0613 evaluated on API-Bank attains 60.24%, GPT-4 evaluated on ToolBench with a depth-first search-based decision tree (DFSDT) prompting strategy achieves 70.4%, and GPT-4o evaluated on NESTful reaches 60.0%, highlighting the relative difficulty of our benchmarks.
We hypothesize that agentic architectures incorporating planning and reflection could substantially increase completion rates. A primary challenge for tool-calling models is accurately interpreting the database schema to populate function slot values. Although schema information is provided via enum descriptions in the tools’ OpenAPI specifications and included in the model prompts, effectively leveraging it typically requires multi-step reasoning.
Error Analysis : We employ the BFCL error categories to categorize the errors made by models on the API task (Yan et al., [2024](https://arxiv.org/html/2506.11266v2#bib.bib37)). Errors are classified into the first type encountered in the list (See Figure [2](https://arxiv.org/html/2506.11266v2#S4.F2)), so that they are non-overlapping by design.
Notably, on the SLOT-BIRD dataset, most failures occur when models struggle to produce outputs in the structured format required for sequencing APIs. On the SEL-BIRD dataset, this issue is less pronounced, and on REST-BIRD, other types of errors predominate. This suggests that the complexity of tasks involving multiple function calls and the processing of their outputs challenges models, leading to additional failures such as tool-format issues. While structured decoding could potentially mitigate these errors, prior work has shown that it can also impair model reasoning Tam et al. ([2024](https://arxiv.org/html/2506.11266v2#bib.bib6)). Together, these patterns highlight the challenges of multi-step reasoning and accurate function selection in complex tool-calling tasks, and our dataset’s characteristics provide a valuable benchmark for studying these nuanced aspects of model behavior.
4.3 Performance of ReACT agents
| Model | Base | Agent | Avg. | OOB | Stuck | Unclassified |
| Comp. | Comp. | Loops | Errors | |||
| SLOT-BIRD | ||||||
| Mixtral-8x22B-instruct | 0.02 | 0.08 | 5.91 | 0.27 | 0.60 | 0.07 |
| Llama-3.3-70b-instruct | 0.00 | 0.06 | 3.28 | 0.05 | 0.32 | 0.59 |
| Qwen2.5-72b-instruct | 0.06 | 0.14 | 5.58 | 0.25 | 0.50 | 0.14 |
| GPT4o-2024-08-06 | 0.03 | 0.15 | 5.45 | 0.10 | 0.54 | 0.23 |
| SEL-BIRD | ||||||
| Mixtral-8x22B-instruct | 0.04 | 0.05 | 6.40 | 0.40 | 0.27 | 0.29 |
| Llama-3.3-70b-instruct | 0.00 | 0.08 | 8.20 | 0.66 | 0.58 | 0.00 |
| Qwen2.5-72b-instruct | 0.16 | 0.17 | 4.93 | 0.17 | 0.24 | 0.47 |
| GPT4o-2024-08-06 | 0.09 | 0.12 | 6.94 | 0.30 | 0.33 | 0.29 |
| REST-BIRD | ||||||
| Mixtral-8x22B-instruct | 0.24 | 0.32 | 3.16 | 0.00 | 0.02 | 0.65 |
| Llama-3.3-70b-instruct | 0.42 | 0.42 | 3.37 | 0.00 | 0.05 | 0.52 |
| Qwen2.5-72b-instruct | 0.47 | 0.49 | 3.26 | 0.00 | 0.02 | 0.48 |
| GPT4o-2024-08-06 | 0.38 | 0.50 | 2.54 | 0.00 | 0.01 | 0.49 |
As experimenting with all models as ReACT agents would become very expensive due to think-act-observe (TAO) loops we choose models from our experiments to serve as ReACT agents. We choose Mixtral-8x22B-instruct which is large mixture-of-expert model that surprisingly performs poorly on our data and wanted to see how the performance changes when it is used as an agent. Additionally, we choose the LLama 3.3-70B-instruct, Qwen2.5-72b-instruct, and GPT4o models for their widespread use. We configure our ReACT agents with a fixed TAO loop budget of turns.
As can be seen from Table [4](https://arxiv.org/html/2506.11266v2#S4.T4), the task completion rates for the agents do not exceed % and 17% for the SLOT-BIRD and SEL-BIRD datasets respectively, though performance on REST-BIRD is much higher (% completion rate by GPT4o). Additionally, agents almost never run out of TAO-loop budget or get stuck repeating the same step on the REST-BIRD dataset but face both problems on the SLOT-BIRD and SEL-BIRD datasets.
4.3.1 Effect of Obfuscation on tool calling
To investigate whether models can make use of function descriptions and other meta-data, we repeated experiments shown in Table. [4](https://arxiv.org/html/2506.11266v2#S4.T4) using non-informative function and argument names. Each API name was replaced by “func_N” where N is a unique integer (Paul et al., [2025](https://arxiv.org/html/2506.11266v2#bib.bib8)).
We found that agent performance dropped slightly ( 3%) for REST-BIRD, but for SLOT-BIRD and SEL-BIRD fell to nearly zero (see Appendix B).
This is likely due to large amount of descriptive information available in REST-BIRD, with function descriptions for each of the 1200 APIs. In contrast, tools in SLOT-BIRD and SEL-BIRD are much more generic, and therefore their descriptions were correspondingly more challenging to interpret.
4.3.2 Effect of the number of tools available
Since every query in the REST-BIRD dataset only requires a single API, we experiment by shrinking candidate set size, while ensuring ground-truth intent is always present. The ability of agents to select correct intent does indeed go up as number of choices shrinks. Interestingly, even with % of the tools removed, the best performing GPT4-o based ReACT agent has a task completion-rate of just % (see Appendix B).
5 Conclusion
In this paper, we presented Live API Bench, a benchmark that transformed NL2SQL datasets into interactive APIs for evaluating LLM tool-calling capabilities. Spanning 11 databases across diverse domains and including over 2,500 invocable APIs paired with human-authored queries, the benchmark covered three styles—SLOT, SEL, and REST. These tasks exposed models to realistic challenges such as multi-step reasoning, sequential tool calls, parameter generation, and complex response parsing. Our experiments showed that even state-of-the-art LLMs struggled with these tasks, highlighting substantial gaps in current tool-calling abilities and the need for further research on robust API interaction.
This presentation of SLOT-BIRD, SEL-BIRD, and REST-BIRD dataset only included versions packaged as either Python functions or REST APIs. We are currently preparing to release a public benchmark and leaderboard based on an expanded version of this dataset. This benchmark also incorporates RAG tasks, more complex reasoning requirements, policy/instruction following, and multi-turn dialogues. It will be based on a Model Context Protocol (MCP) implementation of all tools and APIs.
6 Limitations
Most NL2SQL datasets, including WikiSQL (Zhong et al., [2017](https://arxiv.org/html/2506.11266v2#bib.bib5)), Spider (Yu et al., [2018](https://arxiv.org/html/2506.11266v2#bib.bib4)), and the BIRD-SQL dataset (Li et al., [2023a](https://arxiv.org/html/2506.11266v2#bib.bib15)) used in this work, contain only SELECT queries. Data manipulation commands such as INSERT, UPDATE, and DELETE are not included. Consequently, our benchmark inherits this limitation: all generated APIs and evaluation tasks are based on SELECT queries. In addition, we note that supporting data-manipulation commands using live APIs would require additional infrastructure, such as containerized database environments or managed services, to ensure safe and deterministic execution, introducing substantial operational complexity.
Furthermore, to guarantee reliable ground-truth verification, the current dataset excludes queries involving nested SELECT statements, CASE expressions, and complex logical compositions of WHERE clauses. Nested and conditional constructs greatly complicate the mapping from SQL syntax trees to tool sequences, as in the SLOT-BIRD formulation, where multiple alternatives make it difficult to track intent and slot metrics. In these cases, the abstract syntax tree is no longer linear but contains hierarchical subqueries or conditional branches, introducing ambiguity in the canonical decomposition into tool calls. By excluding such constructs from this initial version of the dataset, we ensure high-quality, deterministic ground-truth sequences for evaluation. Ongoing work is expanding the scope and complexity of SQL syntax included in this work.
Due to limitations on computing resources, these exploratory investigations were carried out using only the dev set from the BIRD dataset. The much larger train set has since also been processed and will be included in the public data release, greatly expanding the overall size of the dataset.
References
-
API-BLEND: a comprehensive corpora for training and benchmarking API LLMs.
In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), L. Ku, A. Martins, and V. Srikumar (Eds.),
Bangkok, Thailand, pp. 12859–12870.
External Links:
[Link](https://aclanthology.org/2024.acl-long.694/),[Document](https://dx.doi.org/10.18653/v1/2024.acl-long.694)Cited by:[§2](https://arxiv.org/html/2506.11266v2#S2.p1.1),[§2](https://arxiv.org/html/2506.11266v2#S2.p2.1). -
NESTFUL: a benchmark for evaluating llms on nested sequences of api calls.
External Links: 2409.03797,
[Link](https://arxiv.org/abs/2409.03797)Cited by:[Table 1](https://arxiv.org/html/2506.11266v2#S1.T1.1.1.14.1.1),[§2](https://arxiv.org/html/2506.11266v2#S2.p2.1),[§2](https://arxiv.org/html/2506.11266v2#S2.p3.1),[§2](https://arxiv.org/html/2506.11266v2#S2.p4.1),[§4.1](https://arxiv.org/html/2506.11266v2#S4.SS1.p2.1). -
Spider2-v: how far are multimodal agents from automating data science and engineering workflows?.
External Links: 2407.10956,
[Link](https://arxiv.org/abs/2407.10956)Cited by:[§2](https://arxiv.org/html/2506.11266v2#S2.p3.1). -
Octopus: on-device language model for function calling of software apis.
External Links: 2404.01549,
[Link](https://arxiv.org/abs/2404.01549)Cited by:[§2](https://arxiv.org/html/2506.11266v2#S2.p4.1). -
WorkArena: how capable are web agents at solving common knowledge work tasks?.
In Proceedings of the 41st International Conference on Machine Learning,
pp. 11642–11662.
Cited by:
[§1](https://arxiv.org/html/2506.11266v2#S1.p1.1). -
The llama 3 herd of models.
arXiv preprint arXiv:2407.21783.
Cited by:
[§4.1](https://arxiv.org/html/2506.11266v2#S4.SS1.p1.1). -
NesTools: a dataset for evaluating nested tool learning abilities of large language models.
arXiv preprint arXiv:2410.11805.
Cited by:
[Table 1](https://arxiv.org/html/2506.11266v2#S1.T1.1.1.4.1). -
Gpt-4o system card.
arXiv preprint arXiv:2410.21276.
Cited by:
[§4.1](https://arxiv.org/html/2506.11266v2#S4.SS1.p1.1). -
DSBench: how far are data science agents from becoming data science experts?.
In The Thirteenth International Conference on Learning Representations,
External Links:
[Link](https://openreview.net/forum?id=DSsSPr0RZJ)Cited by:[§2](https://arxiv.org/html/2506.11266v2#S2.p5.1). -
Can LLM already serve as a database interface? a BIg bench for large-scale database grounded text-to-SQLs.
In Thirty-seventh Conference on Neural Information Processing Systems Datasets and Benchmarks Track,
External Links:
[Link](https://openreview.net/forum?id=dI4wzAE6uV)Cited by:[§1](https://arxiv.org/html/2506.11266v2#S1.p3.1),[§1](https://arxiv.org/html/2506.11266v2#S1.p7.1),[§3](https://arxiv.org/html/2506.11266v2#S3.p1.1),[§6](https://arxiv.org/html/2506.11266v2#S6.p1.1). -
Api-bank: a comprehensive benchmark for tool-augmented llms.
arXiv preprint arXiv:2304.08244.
Cited by:
[Table 1](https://arxiv.org/html/2506.11266v2#S1.T1.1.1.6.1). -
AutoKaggle: a multi-agent framework for autonomous data science competitions.
External Links: 2410.20424,
[Link](https://arxiv.org/abs/2410.20424)Cited by:[§2](https://arxiv.org/html/2506.11266v2#S2.p5.1). -
Hammer: robust function-calling for on-device language models via function masking.
arXiv preprint arXiv:2410.04587.
Cited by:
[§4.1](https://arxiv.org/html/2506.11266v2#S4.SS1.p1.1). -
Deepseek-v3 technical report.
arXiv preprint arXiv:2412.19437.
Cited by:
[§4.1](https://arxiv.org/html/2506.11266v2#S4.SS1.p1.1). -
Toolace: winning the points of llm function calling.
arXiv preprint arXiv:2409.00920.
Cited by:
[Table 1](https://arxiv.org/html/2506.11266v2#S1.T1.1.1.5.1),[§2](https://arxiv.org/html/2506.11266v2#S2.p2.1),[§2](https://arxiv.org/html/2506.11266v2#S2.p3.1),[§2](https://arxiv.org/html/2506.11266v2#S2.p4.1). -
RefTool: enhancing model reasoning with reference-guided tool creation.
arXiv preprint arXiv:2505.21413.
Cited by:
[§2](https://arxiv.org/html/2506.11266v2#S2.p2.1). -
A survey of nl2sql with large language models: where are we, and where are we going?.
arXiv preprint arXiv:2408.05109.
Cited by:
[§2](https://arxiv.org/html/2506.11266v2#S2.p5.1). -
APIGen: automated pipeline for generating verifiable and diverse function-calling datasets.
In Advances in Neural Information Processing Systems, A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang (Eds.),
Vol. 37, pp. 54463–54482.
External Links:
[Document](https://dx.doi.org/10.52202/079017-1725),[Link](https://proceedings.neurips.cc/paper_files/paper/2024/file/61cce86d180b1184949e58939c4f983d-Paper-Datasets_and_Benchmarks_Track.pdf)Cited by:[Table 1](https://arxiv.org/html/2506.11266v2#S1.T1.1.1.13.1),[§2](https://arxiv.org/html/2506.11266v2#S2.p1.1). -
WebCanvas: benchmarking web agents in online environments.
In Agentic Markets Workshop at ICML 2024,
Cited by:
[§1](https://arxiv.org/html/2506.11266v2#S1.p1.1). -
Gorilla: large language model connected with massive apis.
Advances in Neural Information Processing Systems 37, pp. 126544–126565.
Cited by:
[Table 1](https://arxiv.org/html/2506.11266v2#S1.T1.1.1.7.1). -
ObscuraCoder: powering efficient code LM pre-training via obfuscation grounding.
In The Thirteenth International Conference on Learning Representations,
External Links:
[Link](https://openreview.net/forum?id=VYvxrD7aS0)Cited by:[§B.1.2](https://arxiv.org/html/2506.11266v2#A2.SS1.SSS2.p1.1),[§B.2.2](https://arxiv.org/html/2506.11266v2#A2.SS2.SSS2.p1.1),[§4.3.1](https://arxiv.org/html/2506.11266v2#S4.SS3.SSS1.p1.1). -
Revisiting, benchmarking and exploring api recommendation: how far are we?.
External Links: 2112.12653
Cited by:
[§2](https://arxiv.org/html/2506.11266v2#S2.p2.1). -
APITestGenie: automated api test generation through generative ai.
arXiv preprint arXiv:2409.03838.
Cited by:
[§2](https://arxiv.org/html/2506.11266v2#S2.p1.1),[§2](https://arxiv.org/html/2506.11266v2#S2.p2.1). -
ToolLLM: facilitating large language models to master 16000+ real-world APIs.
In The Twelfth International Conference on Learning Representations,
External Links:
[Link](https://openreview.net/forum?id=dHng2O0Jjr)Cited by:[Table 1](https://arxiv.org/html/2506.11266v2#S1.T1.1.1.12.1),[§2](https://arxiv.org/html/2506.11266v2#S2.p1.1),[§2](https://arxiv.org/html/2506.11266v2#S2.p2.1),[§2](https://arxiv.org/html/2506.11266v2#S2.p4.1). -
Identifying the risks of lm agents with an lm-emulated sandbox.
In The Twelfth International Conference on Learning Representations,
Cited by:
[§2](https://arxiv.org/html/2506.11266v2#S2.p3.1). -
Taskcraft: automated generation of agentic tasks.
arXiv preprint arXiv:2506.10055.
Cited by:
[§2](https://arxiv.org/html/2506.11266v2#S2.p1.1). -
Restgpt: connecting large language models with real-world restful apis.
arXiv preprint arXiv:2306.06624.
Cited by:
[Table 1](https://arxiv.org/html/2506.11266v2#S1.T1.1.1.9.1.1). -
Let me speak freely? a study on the impact of format restrictions on large language model performance..
In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: Industry Track, F. Dernoncourt, D. Preoţiuc-Pietro, and A. Shimorina (Eds.),
Miami, Florida, US, pp. 1218–1236.
External Links:
[Link](https://aclanthology.org/2024.emnlp-industry.91/),[Document](https://dx.doi.org/10.18653/v1/2024.emnlp-industry.91)Cited by:[§4.2](https://arxiv.org/html/2506.11266v2#S4.SS2.p7.1). -
ToolAlpaca: generalized tool learning for language models with 3000 simulated cases.
External Links: 2306.05301,
[Link](https://arxiv.org/abs/2306.05301)Cited by:[Table 1](https://arxiv.org/html/2506.11266v2#S1.T1.1.1.11.1),[§2](https://arxiv.org/html/2506.11266v2#S2.p2.1),[§2](https://arxiv.org/html/2506.11266v2#S2.p3.1). -
OSWorld: benchmarking multimodal agents for open-ended tasks in real computer environments.
External Links: 2404.07972
Cited by:
[§1](https://arxiv.org/html/2506.11266v2#S1.p1.1),[§2](https://arxiv.org/html/2506.11266v2#S2.p3.1). -
ReWOO: decoupling reasoning from observations for efficient augmented language models.
External Links: 2305.18323,
[Link](https://arxiv.org/abs/2305.18323)Cited by:[§1](https://arxiv.org/html/2506.11266v2#S1.p1.1). -
On the tool manipulation capability of open-source large language models.
External Links: 2305.16504,
[Link](https://arxiv.org/abs/2305.16504)Cited by:[Table 1](https://arxiv.org/html/2506.11266v2#S1.T1.1.1.8.1),[§2](https://arxiv.org/html/2506.11266v2#S2.p3.1). -
Berkeley function calling leaderboard.
Note:
[https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html](https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html)Cited by:[§E.2](https://arxiv.org/html/2506.11266v2#A5.SS2.p1.1),[§G.1.1](https://arxiv.org/html/2506.11266v2#A7.SS1.SSS1.p1.1),[§2](https://arxiv.org/html/2506.11266v2#S2.p3.1),[§2](https://arxiv.org/html/2506.11266v2#S2.p4.1),[§4.1](https://arxiv.org/html/2506.11266v2#S4.SS1.p2.1),[§4.2](https://arxiv.org/html/2506.11266v2#S4.SS2.p6.1). -
Qwen2. 5 technical report.
arXiv preprint arXiv:2412.15115.
Cited by:
[§4.1](https://arxiv.org/html/2506.11266v2#S4.SS1.p1.1). -
-Bench: a benchmark for tool-agent-user interaction in real-world domains.
External Links: 2406.12045,
[Link](https://arxiv.org/abs/2406.12045)Cited by:[§2](https://arxiv.org/html/2506.11266v2#S2.p3.1). -
ReAct: synergizing reasoning and acting in language models.
In The Eleventh International Conference on Learning Representations,
External Links:
[Link](https://openreview.net/forum?id=WE_vluYUL-X)Cited by:[§1](https://arxiv.org/html/2506.11266v2#S1.p1.1),[§1](https://arxiv.org/html/2506.11266v2#S1.p7.1),[§4.1](https://arxiv.org/html/2506.11266v2#S4.SS1.p5.1). -
AssistantBench: can web agents solve realistic and time-consuming tasks?.
External Links: 2407.15711,
[Link](https://arxiv.org/abs/2407.15711)Cited by:[§1](https://arxiv.org/html/2506.11266v2#S1.p1.1). -
Spider: a large-scale human-labeled dataset for complex and cross-domain semantic parsing and text-to-sql task.
In Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing,
pp. 4206–4216.
Cited by:
[§6](https://arxiv.org/html/2506.11266v2#S6.p1.1). -
WebOlympus: an open platform for web agents on live websites.
In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: System Demonstrations, D. I. Hernandez Farias, T. Hope, and M. Li (Eds.),
Miami, Florida, USA, pp. 187–197.
External Links:
[Link](https://aclanthology.org/2024.emnlp-demo.20/),[Document](https://dx.doi.org/10.18653/v1/2024.emnlp-demo.20)Cited by:[§1](https://arxiv.org/html/2506.11266v2#S1.p1.1). -
ComplexFuncBench: exploring multi-step and constrained function calling under long-context scenario.
External Links: 2501.10132,
[Link](https://arxiv.org/abs/2501.10132)Cited by:[§2](https://arxiv.org/html/2506.11266v2#S2.p2.1),[§2](https://arxiv.org/html/2506.11266v2#S2.p3.1),[§2](https://arxiv.org/html/2506.11266v2#S2.p4.1). -
Seq2SQL: generating structured queries from natural language using reinforcement learning.
arXiv preprint arXiv:1709.00103.
Cited by:
[§6](https://arxiv.org/html/2506.11266v2#S6.p1.1). -
WebArena: a realistic web environment for building autonomous agents.
External Links: 2307.13854,
[Link](https://arxiv.org/abs/2307.13854)Cited by:[§2](https://arxiv.org/html/2506.11266v2#S2.p3.1). -
Toolqa: a dataset for llm question answering with external tools.
Advances in Neural Information Processing Systems 36, pp. 50117–50143.
Cited by:
[Table 1](https://arxiv.org/html/2506.11266v2#S1.T1.1.1.10.1).
Appendix A Overview
We include additional experiments by studying the effect of obfuscation on ReACT agents in section [B.1](https://arxiv.org/html/2506.11266v2#A2.SS1) and the effect of the size of the universe in Section [B.2](https://arxiv.org/html/2506.11266v2#A2.SS2). We describe the artifacts generated by our API generation pipelines in Section [C](https://arxiv.org/html/2506.11266v2#A3) and include more details about our data generation pipelines in Section [D](https://arxiv.org/html/2506.11266v2#A4). We include all LLM prompt templates in Section [E](https://arxiv.org/html/2506.11266v2#A5) and agent prompt templates in Section [F](https://arxiv.org/html/2506.11266v2#A6). Finally, we include additional details on output parsing in Section [G](https://arxiv.org/html/2506.11266v2#A7) and how we conducted the error analysis in Section [G.1.1](https://arxiv.org/html/2506.11266v2#A7.SS1.SSS1).
Appendix B Additional Experiments
B.1 Effect of Obfuscation
B.1.1 Data Construction
As described in the main paper, our goal was to study the impact of function descriptions and function names. To this end, we obfuscated both API and slot names, replacing them with placeholders such as FUNC_0, FUNC_1, …, FUNC_N and ARG_1, ARG_2, …, ARG_N. An example is shown in Fig. [4](https://arxiv.org/html/2506.11266v2#A2.F4), where an API name and argument gets obfuscated and the obfuscated tool name and slots will be passed to the Agent.
[5](https://arxiv.org/html/2506.11266v2#LST5)) and post-obfuscation (Listing
[6](https://arxiv.org/html/2506.11266v2#LST6)) API specification for an example API endpoint from REST-BIRD.
B.1.2 Results
We re-emphasize a significant contribution of our work: the ability to generate a substantial collection of invocable APIs. We leverage this aspect to investigate the extent to which models can rely on function descriptions and other meta-data when completing tasks with non-informative function names that provide no insight into their intended purpose. To achieve this, we obfuscate each API by assigning a unique integer to the prefix “func” (Paul et al., [2025](https://arxiv.org/html/2506.11266v2#bib.bib8)). We evaluate performance using the three ReACT agents as before, as they are capable of exploring the environment based on observations (feedback). Unsurprisingly, the performance of models with obfuscated function names is lower across all datasets (Appendix Figure [4](https://arxiv.org/html/2506.11266v2#A2.F4)) with a slight drop in performance on the REST-BIRD dataset but with severe failures on the SLOT-BIRD and SEL-BIRD datasets. This result underscores the importance of employing domain-specific vocabularies to construct tools that enhance agents’ ability to improve their tool calling performance.
| Dataset | 10% | 25% | 50% | 75% | 100% |
| formula_1 | 12 | 31 | 63 | 94 | 126 |
| card_games | 15 | 38 | 77 | 115 | 154 |
| superhero | 10 | 27 | 54 | 81 | 109 |
| codebase_community | 15 | 39 | 78 | 117 | 156 |
| thrombosis_prediction | 13 | 33 | 67 | 101 | 135 |
| toxicology | 9 | 23 | 47 | 71 | 95 |
| financial | 9 | 22 | 45 | 68 | 91 |
| california_schools | 7 | 18 | 37 | 56 | 75 |
| student_club | 13 | 32 | 65 | 97 | 130 |
| european_football_2 | 11 | 29 | 59 | 88 | 118 |
| debit_card_specializing | 6 | 15 | 30 | 45 | 61 |
B.2 Effect of the number of tools available
As described in the main paper, we also examine the effect of varying the number of tools provided to the agent. The REST dataset features a large API universe, and in some cases, over 100 tools are passed to the model—making the selection task significantly more challenging.
B.2.1 Data Construction
To study the impact of toolset size, we introduce a best-effort shortlisting mechanism. Given a total of N tools, we reduce the candidate set to 10 percent, 25 percent, 50 percent, or 75 percent of the original size to simulate different levels of tool availability.
We employ a best-effort shortlister that always includes the ground-truth tool and supplements it with N - 1 additional (random) tools, resulting in a set of N tools that is then provided to the model.
For this experiment, we used the REACT agent and the prompt described in the previous section.
The below table shows the list of datasets along with the distribution.
B.2.2 Results
We re-emphasize a significant contribution of our work: the ability to generate a substantial collection of invocable APIs. We leverage this aspect to investigate the extent to which models can rely on function descriptions and other meta-data when completing tasks with non-informative function names that provide no insight into their intended purpose. To achieve this, we obfuscate each API by assigning a unique integer to the prefix “func” (Paul et al., [2025](https://arxiv.org/html/2506.11266v2#bib.bib8)). We evaluate performance using the three ReACT agents as before, as they are capable of exploring the environment based on observations (feedback). Unsurprisingly, the performance of models with obfuscated function names is lower across all datasets (Appendix Figure [4](https://arxiv.org/html/2506.11266v2#A2.F4)) with a slight drop in performance on the REST-BIRD dataset but with severe failures on the SLOT-BIRD and SEL-BIRD datasets. This result underscores the importance of employing domain-specific vocabularies to construct tools that enhance agents’ ability to improve their tool calling performance.
B.3 Comparison to NL2SQL
| Model | SLOT-BIRD | SEL-BIRD | REST-BIRD | |||
| API | SQL | API | SQL | API | SQL | |
| Llama-3.1-8B-instruct | 0.00 | 0.35 | 0.0 | 0.35 | 0.32 | 0.24 |
| Llama-3.3-70b-instruct | 0.00 | 0.45 | 0.0 | 0.45 | 0.42 | 0.35 |
| Granite-8b-instruct | 0.00 | 0.13 | 0.0 | 0.13 | 0.34 | 0.09 |
| Hammer2.1-7b | 0.03 | – | 0.03 | – | 0.17 | – |
| Watt-tool-8b | 0.01 | – | 0.01 | – | 0.43 | – |
| Mixtral-8x22B-instruct | 0.02 | 0.29 | 0.04 | 0.29 | 0.24 | 0.22 |
| DeepSeek-V3 | 0.07 | 0.40 | 0.09 | 0.40 | 0.31 | 0.29 |
| GPT4o-2024-08-06 (Prompt) | 0.03 | 0.39 | 0.09 | 0.39 | 0.38 | 0.29 |
| GPT4o-2024-08-06 (Tools) | 0.03 | – | 0.0 | – | – | – |
| Qwen2.5-7b-instruct | 0.03 | – | 0.04 | – | 0.37 | – |
| Qwen2.5-72b-instruct | 0.06 | 0.38 | 0.16 | 0.38 | 0.47 | 0.27 |
Since most LLMs have also been trained to generate SQL queries; we also report the baseline task completion rate when models are prompted to function as SQL-querying systems with direct access to the original database. Interestingly, except on the REST-BIRD dataset, we find that most models report higher completion rates when tasked with generating SQL as opposed to invoking functions.
Appendix C Artifacts
Each data generation pipeline produces the following three artifacts:
-
1.
OpenAPI tool/API specifications: These specifications include both the names and parameters needed to invoke the tools, as well as descriptions with the semantic content needed to understand the purpose and behavior of the tools.
-
2.
Invocable API/function implementation: The SLOT-BIRD and SEL-BIRD tools are provided as python functions which can be invoked programmatically or bound to a function calling LLM. The REST-BIRD APIs are provided as endpoints in a FastAPI server which has been containerized with Docker for easy deployment.
-
3.
Evaluation set: The natural language, tool/API sequence pairs that form the evaluation set can be used to benchmark tool-calling LLMs or Agents.
C.1 OpenAPI Functions / Tools
The OpenAPI tool/API specifications include the intent (API) name, description, and input and output parameters. For each parameter, a name, description, and data type is provided. The subset of input parameters that are required in each specification is also provided. For experiments with tool calling LLMs or agents, these specifications can be provided in the model prompt. The model must understand the specifications in order to successfully call the tools.
Below are some sample tool specifications from each of the three data generation pipelines.
SLOT-BIRD: The ‘sort_data’ tool from the SLOT-BIRD dataset includes a required ‘key_name’ parameter which takes values from a domain-specific enum. The possible values and their descriptions are provided as part of the tool specification (see Listing [7](https://arxiv.org/html/2506.11266v2#LST7)).
SEL-BIRD: The ‘sort_data_ascending’ tool from the SEL-BIRD dataset (see Listing [8](https://arxiv.org/html/2506.11266v2#LST8)) is equivalent to ‘sort_data’ in SLOT-BIRD, with the ‘ascending’ argument fixed to True. There is also a corresponding ‘sort_data_descending’ tool.
REST-BIRD: The REST-BIRD pipeline generates much more specific tools, which were constructed to answer a specific question, rather than perform manipulations on the underlying data, (see Listing [9](https://arxiv.org/html/2506.11266v2#LST9)).
C.2 Evaluation Dataset
Our data processing pipeline will also provide us with an evaluation set (in JSON format) or the test set will contain the following
-
•
Utterance: Natural Language Utterance (from BIRD-SQL dataset)
-
•
SQL Query: SQL Query from the BIRD-SQL dataset
-
•
Gold Answer: Ground truth obtained by executing the SQL query on the BIRD SQL databases
-
•
Output: Dictionary that contains the API (in OpenAI Function format) that will lead to the gold answer
-
•
Output from executing the API: The output from executing the API will have the same data as the Gold Answer but it maybe in a different format
During our evaluation, we benchmark various models on the eval-set that we generated using our data generation pipeline.
Refer to Figure 1 for additional details about the eval-set.
C.3 Invocable APIs (Python Code or Microservices)
In addition to the previously described components, our data generation pipeline also produces invocable code.
From the REST-BIRD pipeline, we obtain a FastAPI server, which is dockerized and deployed as a microservice.
From the SEQ-BIRD and SEL-BIRD pipelines, we receive a suite of Python tools. These can be invoked by installing the accompanying invocable-api codebase (included with this submission) as a Python library.
Appendix D Data Generation Pipeline
The BIRD SQL dataset provides a rich source of structured information that can be leveraged to construct a high-quality API-centric dataset. Specifically, it includes the following components:
-
1.
Natural language input utterances (questions)
-
2.
Corresponding SELECT-SQL queries that yield correct answers
-
3.
Real-world databases
-
4.
Detailed database schemas, including table names, column names, and descriptions
-
5.
Ground truth answers (obtainable by executing the associated SQL queries)
We get the below information from the BIRD SQL dataset
For this work, we utilize the DEV set, which encompasses 11 domains: California Schools, Card Games, Code Base Community, Debit Card Specializing, European Football, Financial, Formula 1, Student Club, Superhero, Thrombosis Prediction, and Toxicology. The BIRD-SQL dataset contains exclusively SELECT statements and does not include UPDATE or INSERT queries. Consequently, the associated tools primarily function as data retrievers, effectively serving as getters.
D.1 SLOT-BIRD and SEL-BIRD Data Generation Pipelines
The SLOT-BIRD and SEL-BIRD datasets were constructed by first writing a set of python tools that could perform the same data manipulations as various parts of an SQL SELECT query. The Sqlglot python library was then used to parse each SQL query into an abstract syntax tree. The data generation pipeline then processed the parsed query components in the following order:
-
1.
JOIN statements
-
2.
WHERE statements
-
3.
GROUPBY statements
-
4.
ORDERBY statements
-
5.
SELECT statements
-
6.
AGGREGATE statements
JOIN Statements These were collectively combined into a single step, carried out by the ‘initialize_active_data’ function. This function is not included in the tool specifications provided to the models and agents in the experiments, due to the complex nature of its required arguments. Instead, it is called in the experiment scripts as a setup or data processing step while looping through the data instances. The output of this function is a single table on which the rest of the tool calls will operate. It is saved to a temporary csv file which is pointed to in the model prompts.
WHERE Statements Currently any number of WHERE statements are supported as long as they are connected only by ANDs. The conditions on which the WHERE statements can be performed are: ’equal_to’, ’not_equal_to’, ’greater_than’, ’less_than’, ’greater_than_equal_to’, ’less_than_equal_to’, ’contains’, and ’like’. Additional conditions such as BETWEEN as well as clauses connected by OR will be included in future versions.
GROUPBY Statements Groupby statements are supported with a parameter to control aggregation type.
SELECT Statements The select statements are handled differently in SLOT-BIRD and SEL-BIRD. In SLOT-BIRD, the ‘retrieve_data’ function performs this task, returning a subset of the columns of the table provided to it. This function also includes optional parameters: ‘distinct’ which controls whether to only return a list of the distinct elements in the column and ‘limit’ which truncates the returned results.
In SEL-BIRD, each column is used to create a unique ‘get_table_and_column_name’ function, which returns only that column. So in this version, selecting N columns requires N tool calls instead of one. The distinct and limit parameters are not available, and instead these are handled by separate functions that must be applied to the output of the ‘get’.
A typical example from the student_club database that illustrates this procedures is shown in Listing [10](https://arxiv.org/html/2506.11266v2#LST10).
The example shown in Listing [11](https://arxiv.org/html/2506.11266v2#LST11) is exceptionally difficult because in order to correctly choose the initial tool in the sequence, a model must not only understand the content of the ‘Player_Attributes_date’ column, but also examine the contents to see that it is required to choose a substring from the string value in each cell. This is not evident from the description provided:
The need for this transformation can only be inferred by examining the data, which an agent capable of multi-round planning and reflection could accomplish.
D.1.1 Comparison to Enterprise API Collections
The SLOT-BIRD API design reflects common patterns found in enterprise analytics platforms. For instance, the Google Analytics Data API uses FilterExpression operations that require specifying field names, operators (equal_to, greater_than), and values—directly paralleling our filter_data function structure.141414[https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/FilterExpression](https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/FilterExpression) Similarly, Tableau’s REST API provides generic filtering operations through their Filter class, where users specify field names and comparison operators.151515[https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_concepts_filtering_and_sorting.htm](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_concepts_filtering_and_sorting.htm) These enterprise examples demonstrate that our generic API formulation mirrors real-world tool-calling scenarios rather than being artificially constructed.
Example 1: Tableau APIs, from the filter_sort_groups.py example: 161616[https://github.com/tableau/server-client-python/blob/master/samples/filter_sort_groups.py#L62](https://github.com/tableau/server-client-python/blob/master/samples/filter_sort_groups.py#L62)
This example has a very similar structure to the filter_data tool in the SLOT-BIRD dataset, where the field name (key name) and operator (condition) need to be specified.
Similar construction from the Google Analytics APIs:171717[https://developers.google.com/analytics/devguides/reporting/data/v1/basics#python_3](https://developers.google.com/analytics/devguides/reporting/data/v1/basics#python_3)
D.2 REST-BIRD Data Generation Pipeline
The 11 dev set domains mentioned above yield a total of 1267 tools and 1250 evaluation data points (test set). Note that our pipeline is easy to extend, and using the train set as well, we will be able to expand our dataset to at least 12,000 tools.
From the data generation pipeline, we expect the following results
-
•
Domain-specific API server code — For each domain (e.g., California Schools, Formula 1), we generate FastAPI server code. This code is then containerized using Docker and deployed to a server, enabling easy access and sharing. We are also relying on the LLM to come up with a description for the API, which is critical as the models rely heavily on the API’s description during intent classification. See some sample API implementations in Fig.
[6](https://arxiv.org/html/2506.11266v2#A4.F6). -
•
Evaluation dataset (JSON) — A structured JSON file serves as our evaluation dataset, capturing input queries, expected outputs, and metadata. A sample datapoint from the evaluation dataset is shown in Listing
[14](https://arxiv.org/html/2506.11266v2#LST14) -
•
API/tool definitions in OpenAPI format — A list of API endpoints represented in OpenAPI function format, mirroring the generated RESTful endpoints.
In the example in Listing [14](https://arxiv.org/html/2506.11266v2#LST14), we extend the original BIRD-SQL fields by including an additional field, output, which represents the target API endpoint serving as the ground truth. We then execute this API using the FastAPI server code generated by the LLM, and the resulting response is captured in the output_after_executing_api field.
The universe of tools we generate, per dataset (domain) will look like this snippet below. We get the description of the APIs and the description of the SLOTS from the OPEN API Spec (which is auto generated from the FAST API Server Code which we obtain from the Code Generation Agent).
Building on this foundation, we investigate the use of large language models (LLMs) to generate realistic, executable REST APIs. To that end, we developed an agentic data generation pipeline composed of several stages as seen below. Some of the stages use a large language models. Some of them use python code to finish a task.
-
1.
A Code Generation Agent, powered by mistral-large, synthesizes FastAPI server code based on the input utterance, the corresponding SQL query, and the desired API endpoint structure (e.g., /v1/bird/formula1/surname?raceid=19).
-
2.
A Deduplication Agent ensures that functionally equivalent endpoints (e.g., get_Employees vs get_All_Employees) are consolidated, avoiding redundant implementations in the generated API.
-
3.
The generated API is then executed, and each endpoint is invoked with representative inputs to collect the output.
-
4.
A Judge Agent: The output is compared against the expected ground truth results derived from the original SQL query. We employ a simple judge for this as the output from the REST end point (FAST API Server implementation) maybe different from the output obtained by executing the SQL query.
-
5.
If the generated output aligns with the expected answer, the API endpoint is considered valid and included in the dataset. Otherwise, the corresponding tool is discarded after a couple of iterative attempts.
This pipeline enables the creation of a reliable and verifiable dataset of REST APIs grounded in real-world databases and driven by natural language intent.
D.2.1 Code Generation Agent
Leveraging an LLM to generate RESTful endpoints offers significant advantages. Key design decisions—such as identifying appropriate query parameters (i.e., input slots), generating descriptive API documentation, and determining standardized output formatting—are effectively automated through the model’s capabilities. Furthermore, the data generation pipeline demonstrates strong extensibility, enabling scalable and efficient synthesis of a large number of APIs with minimal manual intervention.
The input to the Code Generation Agent will include a set of SQL queries and the output will be Fast API Server Code.
Refer to the prompt below.
The above prompt results in LLM-generated FastAPI server code. A snippet of the server code derived from the California Schools domain is shared in Listing [16](https://arxiv.org/html/2506.11266v2#LST16). While this example showcases a few representative endpoints, our pipeline generates at least one endpoint per SQL query in the dataset.
D.2.2 Judge Agent
In order to verify the output coming from executing the API vs the output obtained by executing the SQL query, we employ a simple Judge agent (that uses Mixtral 8X22B)
Here is the prompt
Appendix E Direct LLM Invocation Experiments - Prompt Templates
We conducted experiments using ten different models, including a mix of small- and large-parameter architectures. The following section presents the prompts used in our evaluation. Each prompt instructs the language model to select the appropriate sequence of tools, correctly populate the corresponding slots, and produce a well-formed, machine-parsable JSON output.
E.1 Prompt Templates for SLOT-BIRD and SEL-BIRD Datasets
The SLOT-BIRD and SEL-BIRD prompts used in our non-agentic function-calling experiments are derived from the BFCL prompts, but also include the addition of three ICL examples and an instruction to utilize the initial table created to set up the problem.
-
•
QUERY: input natural language question to answer
-
•
FUNCTION_STR list of OpenAPI-format specifications for the functions/APIs available to the model
-
•
ICL_EXAMPLES: The three ICL examples provided to the model
Llama family of models Prompt (Llama 3.3 70B, Llama 3.1 8B)
watt-tool-8B
Mixtral 8X22B Prompt
DeepSeek V3 Prompt
Qwen family of models Prompt (Qwen 2.5 7B, Qwen 2.5 72B)
Granite 3.1 8B Instruct prompt
GPT-4o prompt
Hammer prompt
E.2 Prompt Templates for REST-BIRD Dataset
To the best of our knowledge, for experiments that involve directly querying the LLM using the REST datasets, we have adopted the same prompt format as used in the experiments presented on the BFCL leaderboard Yan et al. ([2024](https://arxiv.org/html/2506.11266v2#bib.bib37)).
The prompt requires specific components to be filled in. It is important to note that, consistent with the BFCL setup, we do not use in-context learning examples in these experiments involving the REST datasets.
-
•
Query (refers to the input utterance)
-
•
Tools (refers to the list of functions / api’s)
Llama family of models Prompt (Llama 3.3 70B, Llama 3.1 8B, Watt-tools 8B)
Mixtral 8X22B Prompt
DeepSeek V3 Prompt
Qwen family of models Prompt (Qwen 2.5 7B, Qwen 2.5 72B)
Granite 3.1 8B prompt
GPT-4o prompt
Hammer prompt
Appendix F Agent Experiments - Prompt Templates
In our experiment, we use a REACT-style agent capable of both tool invocation and self-reflection. The agent operates within a Think-Act-Observe (TAO) loop and is allowed a maximum of 10 iterations. Its objective is to select the appropriate sequence of tools along with their corresponding slot arguments, execute the final API call, and retrieve the resulting response.
The prompt requires the following components to be filled in.
-
•
Query/Input (refers to the input utterance)
-
•
Tools (refers to the list of functions / api’s)
-
•
Previous Runs (the TAO loops from the previous iterations)
F.1 REACT prompt template
Appendix G Output Parsing and Error Analysis
For the SLOT-BIRD and SEL-BIRD experiments, we employed a four stage parsing procedure. First we assume that the input is valid JSON or JSONL format and attempt a json.loads(). If this fails, we attempt to parse using the Python ast library. If this fails as well, we attempt an xml parsing strategy to handle tool calls in xml brackets(<tool_call/>). Common formatting errors such as prepending text to the JSON body and enclosing the body in extra sets of brackets are handled.
For the REST-BIRD experiments, in most cases, after we receive an output from the model, we use a REGEX-based parser to extract sequences of APIs and their arguments from the model’s generated text. However, even with custom parsers in place, some failures persist. We believe these are instruction alignment failures as the model is unable to adhere to the prompt.
Here are some REGEX patterns we look for, across various models
G.1 REST-BIRD analysis on Direct LLM invocation experiments
As discussed in the main paper, Qwen2.5-72B-instruct achieves the highest win rate, followed by watt-tool-8b and Llama3-3-70B-instruct. Interestingly, even larger models like DeepSeek-V3, GPT-4o, Mixtral-8x22B show lower win rates, despite having reasonably strong Intent F1 and Slot F1 scores. This drop in win rate is largely due to model’s instruction alignment failures.
For our evaluation, we used BFCL prompts. While we employed best-effort parsing, incorporating ICL examples and further prompt engineering could help mitigate some of these issues. That said, we believe it’s reasonable to penalize models that fail to follow the prompt format or return poorly structured outputs that are difficult to parse.
Here is an example where Mixtral-8X22B’s generated text cannot be parsed successfully. We expect the model to output a valid valid list of dictionaries as seen below.
But, the model does not adhere to the instruction and seems to continue generating function calls continuously until it runs out of context length, leading to response that cannot be parsed, Listing [32](https://arxiv.org/html/2506.11266v2#LST32).
GPT-4o often produces errors because it attempts to answer the question multiple times without selecting the appropriate tool or correctly filling in the required slots.
Here is an example where we expect the model to output the following valid response (a list of dictionaries which contain the function calls)
But, the model tries to answer the question and in turn, we will penalize the model.
Deepseek-V3 has similar issues.
While, we expect an output like the below,
The model responds back with Listing [33](https://arxiv.org/html/2506.11266v2#LST33).
One could argue that the API name is in the generated text and technically, it is a valid JSON but unfortunately, it doesn’t follow the prompt instruction and in turn, we penalize the model as extracting arbitrary outputs from text is not scalable.
In Listing [34](https://arxiv.org/html/2506.11266v2#LST34), DeepSeek generates a chain-of-thought like response, making it difficult to standardize parsing.
The Qwen2.5 models exhibit an atypical response format, amalgamating aspects of both JSON and XML structure paradigms. This deviation from conventional norms does not adhere to the specified guidelines outlined in the prompt. The unorthodox pattern can be exemplified by examining the provided example:
G.1.1 Explanation of Error Categories
We utilize the error analysis script used for the BFCL leaderboard (Yan et al. ([2024](https://arxiv.org/html/2506.11266v2#bib.bib37))) to create the categories used in the Figure [2](https://arxiv.org/html/2506.11266v2#S4.F2). Following is a brief description of each error category -
-
•
instruction_alignment_failure - Failures due to the model not adhering to the output instructions or not producing required JSON to be parsed. Examples are some of these errors are shown in section
[G](https://arxiv.org/html/2506.11266v2#A7) -
•
wrong_func_count - Failure to produce the right number of function calls.
-
•
wrong_func_format - As mentioned in prompt section
[E](https://arxiv.org/html/2506.11266v2#A5)the model is expected to return a list of dictionaries having keys ’name’ and ’arguments’. Parseable outputs not following this format are recorded here. -
•
hallucinated_func_name - If the function name is hallucinated i.e. not present in the provided tool list.
-
•
wrong_func_name - If a wrong function name if picked from the tool list.
-
•
missing_required_parameter - A required argument for the function is missing.
-
•
unexpected_param - An extra argument not required by the function is provided.
-
•
value_error - The value or DataType of an argument is incorrect.
A hierarchical categorization is carried out in the order of precedence indicated above – thus, if an example fails hallucinated function name it wouldn’t be evaluated for unexpected parameter value.
G.1.2 Explanation of ReACT agent Error Categories
Error analysis for ReAct agents [4](https://arxiv.org/html/2506.11266v2#S4.T4) concentrates on the reflection loop. We calculate three metrics for the Tao loop as follows:
-
•
Avg. Loops - Average length of Tao loops
-
•
OOB - Examples which failed due to Tao loop running out of budget (i.e. for our case 10 iterations completed)
-
•
Stuck - Examples which failed to execute and got stuck on a particular function in the Tao loop (# consecutive function calls>=2 and example failed).
-
•
Unclassified - Any example which failed except for OOB and Stuck error.
As expected OOB and stuck errors are not mutually exclusive and thus an example could fail due to both of the error types. Unlike the error categories in Section [G.1.1](https://arxiv.org/html/2506.11266v2#A7.SS1.SSS1) these error categories are not hierarchically calculated.