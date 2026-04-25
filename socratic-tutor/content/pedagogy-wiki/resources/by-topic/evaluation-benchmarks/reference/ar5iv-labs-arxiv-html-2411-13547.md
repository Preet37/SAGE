# Source: https://ar5iv.labs.arxiv.org/html/2411.13547
# Author: Shirley Kokane et al.
# Title: SpecTool: A Benchmark for Characterizing Errors in Tool-Use LLMs
# Fetched via: trafilatura
# Date: 2026-04-10

SpecTool: A Benchmark for Characterizing Errors in Tool-Use LLMs
Abstract
Evaluating the output of Large Language Models (LLMs) is one of the most critical aspects of building a performant compound AI system. Since the output from LLMs propagate to downstream steps, identifying LLM errors is crucial to system performance. A common task for LLMs in AI systems is tool use. While there are several benchmark environments for evaluating LLMs on this task, they typically only give a success rate without any explanation of the failure cases. To solve this problem, we introduce SpecTool, a new benchmark to identify error patterns in LLM output on tool-use tasks. Our benchmark data set comprises of queries from diverse environments that can be used to test for the presence of seven newly characterized error patterns. Using SpecTool , we show that even the most prominent LLMs exhibit these error patterns in their outputs. Researchers can use the analysis and insights from SpecTool to guide their error mitigation strategies.
*skokane@salesforce.com
Salesforce AI Research, USA
1 Introduction
An emerging use case for LLMs in AI systems is tool use. When LLMs are equipped with context and a list of tools, such as APIs, databases, and applications, LLMs can generate a sequence of calls to the available tools to solve a given task. Using LLMs to perform tasks via APIs involves more complex reasoning and instruction following abilities of LLMs, and there are several emerging methods that aim to improve those abilities in order to help LLMs adapt to new tasks and situations. These methods (Zhang et al., [2024](#bib.bib22); Li et al., [2023](#bib.bib9)) help enhance the model’s understanding of user preferences, along with its skills in logical reasoning, with the goal of increasing their overall effectiveness. The basic technique involves using guiding prompts to provide LLMs with instructions and information about the context, enabling them to generate actions to solve complex tasks. Besides, some techniques (Rafailov et al., [2024](#bib.bib15); Jing et al., [2019](#bib.bib8)) focus on dedicated training methods to turn LLMs into highly capable agents.
Significant progress has been made in evaluating LLMs on tool use tasks, as demonstrated by several benchmarks such as ToolBench (Guo et al., [2024](#bib.bib5)), AgentBoard (Ma et al., [2024](#bib.bib12)), MintBench (Wang et al., [2023](#bib.bib18)), and AgentLite (Liu et al., [2024](#bib.bib10)). Collectively, the currently available benchmarks span tool use scenarios in a broad range of environments such as weather ([Open-Meteo, ](#bib.bib13)) and movie ([The-Movie-DB, ](#bib.bib17)). However, most evaluation benchmarks typically only calculate the success rate, measuring how often the final output of the LLMs aligns with the expected output. The AgentBoard benchmark includes a success rate metric that specifically evaluates the model’s final output against the expected ground truth. Moreover, the tool-related dataset within this benchmark is limited in scope. Conversely, the ToolBench benchmark features a more extensive dataset, encompassing a wide range of tasks across different instructions, tools, and categories. Nevertheless, ToolBench is similarly restricted to assessing whether the final outcome has been achieved. Although leading LLMs demonstrate similar overall performance as reported in (Guo et al., [2024](#bib.bib5)), a closer analysis reveals distinct underlying errors in their behavior. To drive continuous improvements in LLM performance, it is essential to thoroughly understand these failure cases.
In an effort to address the limitations of the existing benchmarks, we present SpecTool , a benchmark created to characterize common errors in tool-use LLMs and provide detailed diagnostic feedback to help improve them. SpecTool comprises of 10 distinct environment categories, including Tools, Movies, Travel, Sports, Entertainment, Data, Social, Media, Weather and Video Images, making it one of the most comprehensive evaluation environments. It also incorporates over 30 different tasks specifically aimed at tool agents, such as entertainment, sports, and weather tasks.
During this study, we delineate seven commonly occurring error patterns displayed by LLMs when engaged in tool-use tasks. In order to bring consistency to the evaluation of these error patterns across varying LLMs, we build a comprehensive evaluation framework. The framework comprises a comprehensive error pattern analysis and feedback mechanism tailored for various agents operating in diverse environments, all within a unified format. The feedback mechanism enables agents to refine their actions based on fundamental tool-calling criteria. This setup offers valuable insights into the different error patterns encountered by the models.
Furthermore, the SpecTool evaluation dataset comprised of 150 queries can be employed to identify these error patterns in the output of LLMs during tool-use tasks. These queries have been annotated by humans to highlight multiple pathways to reach a given objective. Subsequently, we showcase the capacity of SpecTool to identify error patterns in a case study involving various leading LLMs.
The contributions of this paper can be summarized as follows:
-
•
We introduce SpecTool , a comprehensive benchmark covering 10 environment categories and over 30 tasks, specifically designed to provide detailed diagnostic feedback on tool-use tasks in LLMs.
-
•
We identify seven common error patterns in LLM tool-use tasks and create an evaluation framework that analyzes these errors consistently across different agents and environments.
-
•
We provide a 150-query human-annotated dataset to detect error patterns in LLM outputs and demonstrate SpecTool ’s effectiveness through a case study involving several leading LLMs.
| Points | Toolbench | Agentboard | MintBench | Gorilla | SpecTool |
| Multi-Turn Interactions | ✓ | ✓ | ✓ | ✗ | ✓ |
| Varied Unique APIs | ✓ | ✓ | ✗ | ✗ | ✓ |
| Query diversity | ✓ | ✗ | ✗ | ✓ | ✓ |
| Error Pattern Analysis | ✗ | ✗ | ✗ | ✓ | ✓ |
| Feedback Mechanism | ✗ | ✓ | ✓ | ✗ | ✓ |
| Multiple Ground Truth Trajectories | ✗ | ✗ | ✗ | ✗ | ✓ |
2 Related Work
The current benchmarks exhibit notable strengths and weaknesses in evaluating model performance as a tool-use agent. Benchmarks like Gorilla (Patil et al., [2023](#bib.bib14)), AgentBoard (Ma et al., [2024](#bib.bib12)), ToolBench (Guo et al., [2024](#bib.bib5)), ToolEyes (Ye et al., [2024](#bib.bib21)), and MintBench (Wang et al., [2023](#bib.bib18)) are remarkably utilised in examining model interaction ability, reasoning and planning ability. While some benchmarks like ToolBench , AgentBoard , and MintBench are effective in managing multi-turn interactions, others such as Gorilla excel in handling diverse queries, especially when dealing with constraints and irrelevant information. Gorilla also offers detailed error pattern analysis and are well-suited for complex queries that require a wide range of API capabilities but is limited to single-turn interactions only.
However, these evaluations often fail to consider the model’s existing knowledge, leading to unnecessary and repetitive API calls without specific prompt instructions. Furthermore, the benchmarks like AgentBoard place undue emphasis on the sequence of subgoals, sometimes misjudging a model’s progress when redundant subgoals are involved. This rigid focus can result in an inaccurate assessment of the model’s true capabilities in task completion.
We address all these current issues in the existing benchmark, where our focus is more on assessing the quality of the action generated by the model given the constraints in the query. Our emphasis is on understanding some critical errors of the model such as hallucinations in actions w.r.t API names or argument names, performing redundant repetitive calls, invalid format issues. These issues are commonly experienced during training or fine-tuning of an LLM for agentic tasks and it is critically important to quantify such issues to get a deeper insight into the improvements required in the model.
3 Error Patterns in Tool-Use
It’s widely understood that LLMs are prone to output errors such as hallucinations, inconsistencies, errors, etc (Wei et al., [2022](#bib.bib19), [2024](#bib.bib20); Lu et al., [2024](#bib.bib11)). What is less studied are the errors exhibited in tool-use scenarios. In tool-use scenarios, typically the LLM outputs one or more function calls, including necessary arguments for the execution of the functions. For example, an LLM output for using a web search API to learn about the latest fashion can be as the following:
,
where indicates the tool and and are the context-specific arguments for executing the tool call.
Note that these tool calls are particularly brittle - even a slight change to an argument, a missing argument, or incorrect tool call can produce drastically different and incorrect results downstream. Given the importance of catching these output errors, in this work, we characterize systematic errors generated by LLMs on tool-use tasks into seven critical error types.
Insufficient API Calls (IAC): The LLM is unable to generate sufficient API calls, hence unable to completely fulfill the tasks provided in a query.
Incorrect Argument Value (IAV): The LLM generates incorrect argument values. This also includes exclusion of necessary arguments.
Incorrect Argument Name (IAN): The LLM hallucinates argument names.
Incorrect Argument Type (IAT): The LLM generates incorrect argument type.
Repeated API Calls (RAC): The LLM generates the exact same API Call repeatedly, leading to redundant calls.
Incorrect Function Name (IFN) : The LLM hallucinates function names, that are not included in the API list.
Invalid Format Error (IFE) : The LLM is incapable of following the appropriate format instructions provided for parsing.
4 SpecTool Dataset
The brittle nature of LLM-generated tool calls highlights the need to quickly discover errors in LLM-generated outputs. To quickly discover tool-calling errors in LLMs, we propose a new dataset, SpecTool . It is created through a series of effective steps aimed at generating complex queries.
The process begins by gathering seed queries for each API environment, sourced from benchmark tests conducted on toolsets like ToolBench (Guo et al., [2024](#bib.bib5)) and AgentBoard (Ma et al., [2024](#bib.bib12)). These initial seed queries are then augmented using the following methods. See figure [1](#S3.F1) for an overview.
Constraint based Query Generation: We employ a deterministic method to discern the options available for each argument within every API call. Utilizing prompt engineering techniques, we introduce detailed descriptions of each argument and its corresponding options to enhance the original query within GPT-4. First, we include one argument along with its option to create a more detailed query. Then, we improve our method by adding multiple arguments and their options, making the query even more complex.
Sentence Transformation based Query Generation: On seed queries, we instruct GPT-4 to modify sentences while maintaining the same context. This means keeping the contextual requirements unchanged while altering the sentences.
Relevance Data based Query Generation: On seed queries, we instruct GPT-4 to introduce additional, unnecessary information around the keywords while keeping the context of the query unchanged.
We collected around 150 augmented queries and annotated the expected API calls. Evaluating these queries across different models will help us better understand the error patterns generated by LLMs.
The table [2](#S4.T2) describes the distribution of queries across different environment APIs. We also list down the average number of interactions alongwith the queries sampled per environment after augmentation.
| Environments | Sampled Queries | Avg. Interactions | Avg. APIs |
| Patent | 20 | 6 | 7.2 |
| Movies | 30 | 11 | 11.5 |
| Travel | 5 | 8 | 5.6 |
| Sports | 8 | 4 | 4.4 |
| Tools | 12 | 5 | 4.8 |
| Data | 14 | 7 | 4.0 |
| Social | 16 | 7 | 3.0 |
| Media | 11 | 6 | 5.5 |
| Spaceflight | 25 | 9 | 10 |
| Video Images | 9 | 5 | 6.0 |
| SpecTool | 150 | 6.8 | 6.2 |
| Query | Error | Model | Output |
| I need jokes sorted by score in ascending order of the category food? Can you provide me with that? | IAV | MLlama | GT: getJokeCategory(category=‘food’, sortby= ‘asc’) MO: getJokeCategory(category=‘workplace’, sortby = ‘asc’) |
| Can you provide me with the genre, runtime, IMDb rating, language for the movie ‘Endgame’? Also, please include the streaming platforms available in the US. | IAN | GPT-4 | GT: getMovieAdvance(genre = ‘horror’, startyear = 1970, endyear = 2020, minimdb = 7) MO: getMovieAdvance(genre=‘horror’, releasestart=1970 , releaseend = 2020, imdbrating = 7) |
| I need the titles and their release years for horror movies with a minimum IMDb rating of 7 that were released between 1970 and 2020. | IAC | GPT-3.5 | GT: getMovie(title = ‘Endgame’, type= ‘movie’), getMovieProvider(region = ‘US’) MO: getMovie(title = ‘Endgame’, type=‘movie’) |
| I need to check if the domain ‘business.com’ is available or not | IAT | xLAM | GT: checkDomainAvailability(domain = ‘business.com’, availableonly=True) MO: checkDomainAvailability(domain= ‘business.com’ , availableonly=”True”) |
5 Method
In the evaluation benchmark we propose for tool use, we ensure that the environments are deterministic. This allows the trajectory of the agents to depend solely on the policy and actions selected by the language model. Agents are given a description of the available tools and task instructions, including format requirements. The actions generated by the agents are reviewed by an inbuilt feedback mechanism designed to detect prominent errors. These include formatting issues, incorrect function names, incorrect argument names, and incorrect argument types. If no such errors are found, the action is executed within the corresponding environment and the feedback it generates is collected. This feedback offers insights into both the changes in state and any potential action errors.
As described in the AgentBoard paper (Ma et al., [2024](#bib.bib12)), tool use interaction with an environment can be conceptualized as a finite-horizon Partially Observable Markov Decision Process (POMDP) (Bellman, [1957](#bib.bib2)), starting with a known initial state, described by the tuple , where is the goal, represents the set of possible states, comprises the available actions, is the transition model , and includes the observation space (along with feedback from the environment). An agent, guided by policy , makes decisions at every iteration x based on the goal g and a memory sequence = , , , , …, where , which records the sequence of past actions and observations. The resulting agent’s path, = [, , , , …], emerges from the policy and the environment’s state transitions.
As shown in figure [2](#S4.F2), our benchmark follows a deterministic framework where the agent will begin with Instruction i, Query q, and a sequence of api-list (resembling to the action space) provided to successfully solve the provided query. The agent then based on the policy of the language model will perform an action in the current , leading to a determined state transition .
A constructive feedback mechanism f is also incorporated to help assist the agent for the following issues:
-
•
Verify whether the generated action is correctly parsed and adheres to the format instructions provided in the prompt.
-
•
Determine if the generated action is included in the specified action space. If it is not, enumerate the list of available actions that can be used to resolve the query.
-
•
Assess whether the generated action is invoked with the appropriate arguments. If the arguments are incorrect, provide a detailed list of the available arguments for the chosen action, along with their respective descriptions.
-
•
Ensure that the generated action is called with arguments of the correct type. If any discrepancies are found, specify the correct argument type required for proper execution of the function.
Upon determining that the feedback is positive and no errors are detected in the action, the action is executed within the environment e to obtain a new observation, denoted as . This observation is then fed back into the model to facilitate the subsequent set of appropriate actions.
6 Metrics
Current benchmarks tend to emphasize the final outcome of models, often overlooking the errors that occur during intermediate steps. Benchmarks such as AgentBoard and MintBench attempt to address this by imposing constraints on the expected outcomes at each step and the sequence in which goals should be achieved. For instance, AgentBoard defines subgoals for each query set in a prescribed order, with these subgoals representing the expected API responses based on the agent’s actions. However, these benchmarks do not consider that the model might possess prior information allowing it to skip certain subgoals, potentially leading to an inaccurate assessment of the model’s performance due to its deviation from the prescribed subgoal sequence. Additionally, these benchmarks lack detailed analysis of specific errors in the action execution, thus failing to provide comprehensive insights into the minor mistakes made by the model.
In this study, we concentrate our efforts on offering deeper insights into specific model inefficiencies. We do this by providing critical metrics related to API Call, thus fostering a comprehensive understanding of the necessary improvements in the models. At present, we have accurately verified and labeled a compilation of 150 queries. These queries are unique, stemming from diverse environments as shown in table [2](#S4.T2), and each boasting multiple expected API Call trajectories. We employ these queries to subsequently compute metrics for a variety of models, thereby identifying their respective error patterns. Each metric is defined as follows: N represents the total number of maximum steps the model is permitted to effectively process the query, while GT denotes the Ground Truth labels for each individual query. Our calculation of these metrics strictly follows the sequence outlined above.
-
•
For error patterns IFN, IAN, IAT, IFE and RAC we calculate each error’s accuracy as: , where is the number of API calls executing the error pattern.
-
•
For error patterns IAC and IAV, we use the labeled ground truths of each query and calculate these metrics across each labeled trajectory: , where is the number of API calls with errors w.r.t. the ground truth g.
It is crucial to emphasize that while the metrics indicate error patterns, their calculations are designed to be directly proportional to the success rate. Higher scores on the error metrics represent fewer issues generated by a model in that respective error pattern. We calculate the success rate of each query by comparing its final output with the ground truth. If a quantitative ground truth is unavailable, success is determined by the model’s ability to conclude using the finish API with a correct response. Error metrics are then incorporated with appropriate weightage in both cases.
| Model | Success Rate | IAC | RAC | IAV | IFE | IAT | IAN | IFN |
| GPT-4-0125-preview | 0.71 | 0.84 | 1.00 | 0.94 | 1.00 | 0.93 | 0.94 | 0.94 |
| xLAM-8x22b | 0.68 | 0.87 | 0.96 | 0.92 | 1.00 | 0.94 | 0.91 | 0.93 |
| xLAM-7b | 0.64 | 0.78 | 0.98 | 0.93 | 0.98 | 0.95 | 0.86 | 0.91 |
| xLAM-8x7b | 0.63 | 0.78 | 0.95 | 0.92 | 1.00 | 0.95 | 0.93 | 0.91 |
| Code-Llama-13b | 0.54 | 0.61 | 0.89 | 0.92 | 0.91 | 0.78 | 0.79 | 0.81 |
| GPT-4o-turbo-2024-05-13 | 0.53 | 0.83 | 0.82 | 0.95 | 1.00 | 0.88 | 0.87 | 0.89 |
| GPT-3.5-turbo-1106 | 0.53 | 0.67 | 0.84 | 0.89 | 0.99 | 0.79 | 0.77 | 0.81 |
| Mixtral-8x22b-Instruct-v0.1 | 0.4 | 0.7 | 0.92 | 0.62 | 0.99 | 0.6 | 0.81 | 0.78 |
| Meta-Llama3-8b | 0.27 | 0.58 | 0.4 | 0.92 | 0.71 | 0.49 | 0.42 | 0.64 |
| Mistral-7b-Instruct-v0.1 | 0.24 | 0.49 | 0.54 | 0.91 | 0.93 | 0.52 | 0.67 | 0.7 |
| Vicuna-13b-16k | 0.16 | 0.27 | 0.26 | 0.61 | 0.69 | 0.39 | 0.4 | 0.5 |
| Mixtral-8x7b-Instruct-v0.1 | 0.1 | 0.11 | 0.42 | 0.41 | 0.43 | 0.43 | 0.42 | 0.2 |
7 Experiments
We perform an in-depth assessment of widely used large language models, encompassing both proprietary, API-based systems and models with publicly accessible weights. This evaluation covers a broad range of models to examine performance, versatility, and the impact of architectural variations across both closed and open-source platforms.
We incorporate a one-shot in-context example along with task-specific instructions in our prompt setup. Our benchmarking includes a selection of high-performing proprietary models as well as open-weight models. For each open-weight model, we evaluate the chat-optimized version when available, unless otherwise indicated.
For models without a dedicated chat version, we apply standardized prompt templates tailored for publicly accessible versions. We ensure that each prompt includes precise format instructions to enable the model to generate API calls in a structured and parsable format. To account for server inconsistencies, we execute multiple rounds per API call, thus minimizing potential disruptions and ensuring consistent evaluation outcomes.
7.1 Results
One goal of our SpecTool benchmark is to quantify various error patterns critical for understanding model fallacies. For that,
we’ve conducted a comprehensive assessment of several performant LLMs, including GPT-4 (Achiam et al., [2023](#bib.bib1)), GPT-3.5-Turbo from OpenAI, Meta-Llama-3-8b (Dubey et al., [2024](#bib.bib4)), Code-Llama-13b (Rozière et al., [2024](#bib.bib16)), Vicuna-13b-16k (Chiang et al., [2023](#bib.bib3)), Mistral and Mixtral models from Mistral AI (Jiang et al., [2023](#bib.bib6)) (Jiang et al., [2024](#bib.bib7)), and xLAM (Zhang et al., [2024](#bib.bib22)). Interestingly, while these models all perform well on ToolBench (Guo et al., [2024](#bib.bib5)), their failure patterns are different. Details of the error patterns discovered using SpecTool are shown in table [3](#S4.T3). The table [3](#S4.T3) qualitatively explains the how each error pattern is exhibited in common model outputs.
One discovery is that models specifically tuned to focus on API calling mechanisms are generally less likely to produce false information, often known as “hallucinating” when dealing with function names and argument names. On the contrary, models like Vicuna (Chiang et al., [2023](#bib.bib3)) (Zheng et al., [2024](#bib.bib23)) that are designed for chat-based interactions do have a higher rate of inaccuracies, particularly within incorrect argument names and function names. It suggests that the tuning process, specifically for API calls, can lead to a substantial reduction in these hallucination problems.
Our results indicate that both proprietary and open-weight models fine-tuned for API-calling tasks show strong performance in reducing ”Insufficient API Calls.” This metric suggests these models are particularly effective at selecting the correct tools from the available API options, demonstrating a high proficiency in expected tool utilization.
This research constitutes a parallel and complementary pursuit in tandem with the development of the xLAM model (Zhang et al., [2024](#bib.bib22)). The techniques applied within this study have been successfully incorporated into the xLAM data pipeline, evidence of which can be discerned from the resultant table [4](#S6.T4). Most striking is the superior performance of GPT-4, achieving the highest success rate amongst all models evaluated. This could potentially suggest that larger models harnessing the power of the scaling law and quality pretraining in the base model remain critical to the success of agent applications. Another noteworthy observation is the exemplary performance of the Code-Llamma-13b model (Rozière et al., [2024](#bib.bib16)), surpassing many other generically-purposed models. Our hypothesis is that there may be some inherent similarity between coding-associated tasks and function calls. And that could be beneficial for models designed for coding purposes, thereby enhancing their performance on function-calling tasks.
7.1.1 Impact of Feedback on Model Performance
7.2 Ablation Study
We performed an ablation study to assess the importance of the constructive feedback mechanism introduced in the SpecTool benchmark. This analysis aimed to highlight the contribution of the feedback process to the model’s decision-making capabilities. As shown in Figure [4](#S7.F4), the feedback mechanism plays a pivotal role in enabling the model to refine its actions by concentrating on essential aspects, such as correctly identifying API names, selecting appropriate API arguments, and adhering to the expected data types for those arguments.
In scenarios where the feedback mechanism was absent, the model frequently repeated errors, such as incorrect function names, leading to a significant reduction in its task completion effectiveness. Without guidance, the model struggled to recover from initial mistakes, which compounded its challenges in achieving desired outcomes. Conversely, with the feedback mechanism in place, the model exhibited immediate improvements in subsequent interactions. For example, it was able to adjust argument types or incorrect/mismatched argument names efficiently in response to errors. These results underscore the critical role of feedback in enhancing the adaptability and accuracy of models, particularly in iterative and error-prone processes.
7.2.1 Impact of Irrelevance on Model Performance
In a complementary analysis, we conducted an in-depth examination of a subset of queries drawn from two distinct API environments to investigate the propensity of models to generate fabricated API calls when presented with unexpected or irrelevant requests. In this context, irrelevance was specifically defined as the inclusion of an additional requirement or constraint that was entirely unrelated to the functionality or parameters supported by the given API environment. By doing so, we sought to measure the extent to which these irrelevant constraints influenced the model’s ability to generate accurate, relevant outputs versus its tendency to hallucinate fictitious API calls that were not part of the original environment.
Our findings show that most models tend to produce more errors related to incorrect function names, posing a challenge to deploying them effectively in real-world applications. This highlights the need for better handling of unexpected inputs to improve stability and accuracy across various requests. Figure [5](#S7.F5) illustrates the performance decline on the subset of queries both in the presence and absence of irrelevant inputs, highlighting the impact of query relevance on model performance. In the figure we particularly focus on the accuracy drop for the metric IFN, hence showcasing how we can segregate model fallacies using this benchmark.
7.2.2 Impact of API Complexity on Model Performance
The following study investigated how structural similarities between different APIs affect model decision-making and accuracy across various environments. To conduct this analysis, we isolated unique, descriptive tokens in each API function name by removing tokens shared across all names within an environment. This approach enabled us to compute a more accurate similarity measure using the Jaccard metric, which reflects how structurally similar API names are within each environment. This metric is advantageous as it assigns higher similarity scores to structurally similar APIs, which may differ only slightly, while scoring dissimilar, functionally distinct APIs lower.
The findings, shown in Figure [3](#S7.F3), align with our hypothesis that environments with structurally similar API names are associated with lower model accuracy. Specifically, we observed a pronounced effect on the Insufficient API Calls metric, illustrating that models tend to misinterpret similar API names and, as a result, frequently select incorrect APIs. This study highlights the significance of breaking down error patterns to pinpoint the specific types of errors models make, ultimately improving transparency and guiding strategies to increase robustness in API-driven tasks.
8 Conclusion
This paper introduced SpecTool , a benchmark for evaluating LLMs on tool-use tasks with a focus on error patterns and feedback. Our findings highlight the importance of task-specific fine-tuning, as models optimized for API calls perform more reliably and reduce hallucinations compared to chat-oriented models. Larger models, like GPT-4, demonstrate superior performance, affirming the significance of scaling and quality pretraining. Additionally, we showed that the feedback mechanism in SpecTool plays a crucial role in improving model accuracy, guiding models to correct their function-calling behavior. Overall, this study provides valuable insights for refining LLMs in tool-use applications.
In this work, we recognize the importance of capturing the significant error patterns of the model, as addressing these failures in planning and function-calling can lead to long-term improvements in the model effectiveness, hence enhancing the reasoning capabilities of LLMs. By analyzing these metrics, developers can identify specific weaknesses in language models and focus on improvements in those key areas. This targeted approach can help enhance the overall performance and reliability of the models.
Our benchmark SpecTool is a continuously developed pipeline for better use cases. Presently, we have tested on tasks belonging to only a single family of actions, for example a task would be estimating weather details with API actions only related to weather. Future work involves analyzing more complex tasks with real-world queries and APIs, along with large-scale testing across different LLMs.
References
- Achiam et al. [2023] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. arXiv preprint arXiv:2303.08774, 2023.
- Bellman [1957] Richard Bellman. A markovian decision process. Journal of mathematics and mechanics, pages 679–684, 1957.
-
Chiang et al. [2023]
Wei-Lin Chiang, Zhuohan Li, Zi Lin, Ying Sheng, Zhanghao Wu, Hao Zhang, Lianmin Zheng, Siyuan Zhuang, Yonghao Zhuang, Joseph E. Gonzalez, Ion Stoica, and Eric P. Xing.
Vicuna: An open-source chatbot impressing gpt-4 with 90%* chatgpt quality, March 2023.
URL
[https://lmsys.org/blog/2023-03-30-vicuna/](https://lmsys.org/blog/2023-03-30-vicuna/). - Dubey et al. [2024] Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, et al. The llama 3 herd of models. arXiv preprint arXiv:2407.21783, 2024.
- Guo et al. [2024] Zhicheng Guo, Sijie Cheng, Hao Wang, Shihao Liang, Yujia Qin, Peng Li, Zhiyuan Liu, Maosong Sun, and Yang Liu. Stabletoolbench: Towards stable large-scale benchmarking on tool learning of large language models. arXiv preprint arXiv:2403.07714, 2024.
-
Jiang et al. [2023]
Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, Lélio Renard Lavaud, Marie-Anne Lachaux, Pierre Stock, Teven Le Scao, Thibaut Lavril, Thomas Wang, Timothée Lacroix, and William El Sayed.
Mistral 7b, 2023.
URL
[https://arxiv.org/abs/2310.06825](https://arxiv.org/abs/2310.06825). -
Jiang et al. [2024]
Albert Q. Jiang, Alexandre Sablayrolles, Antoine Roux, Arthur Mensch, Blanche Savary, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Emma Bou Hanna, Florian Bressand, Gianna Lengyel, Guillaume Bour, Guillaume Lample, Lélio Renard Lavaud, Lucile Saulnier, Marie-Anne Lachaux, Pierre Stock, Sandeep Subramanian, Sophia Yang, Szymon Antoniak, Teven Le Scao, Théophile Gervet, Thibaut Lavril, Thomas Wang, Timothée Lacroix, and William El Sayed.
Mixtral of experts, 2024.
URL
[https://arxiv.org/abs/2401.04088](https://arxiv.org/abs/2401.04088). - Jing et al. [2019] Mingxuan Jing, Xiaojian Ma, Wenbing Huang, Fuchun Sun, and Huaping Liu. Task transfer by preference-based cost learning. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 33, pages 2471–2478, 2019.
- Li et al. [2023] Yuan Li, Yixuan Zhang, and Lichao Sun. Metaagents: Simulating interactions of human behaviors for llm-based task-oriented coordination via collaborative generative agents. arXiv preprint arXiv:2310.06500, 2023.
- Liu et al. [2024] Zhiwei Liu, Weiran Yao, Jianguo Zhang, Liangwei Yang, Zuxin Liu, Juntao Tan, Prafulla K Choubey, Tian Lan, Jason Wu, Huan Wang, et al. Agentlite: A lightweight library for building and advancing task-oriented llm agent system. arXiv preprint arXiv:2402.15538, 2024.
- Lu et al. [2024] Pan Lu, Baolin Peng, Hao Cheng, Michel Galley, Kai-Wei Chang, Ying Nian Wu, Song-Chun Zhu, and Jianfeng Gao. Chameleon: Plug-and-play compositional reasoning with large language models. Advances in Neural Information Processing Systems, 36, 2024.
- Ma et al. [2024] Chang Ma, Junlei Zhang, Zhihao Zhu, Cheng Yang, Yujiu Yang, Yaohui Jin, Zhenzhong Lan, Lingpeng Kong, and Junxian He. Agentboard: An analytical evaluation board of multi-turn llm agents. arXiv preprint arXiv:2401.13178, 2024.
-
[13]
Open-Meteo.
Open-meteo: Free weather api.
URL
[https://open-meteo.com/](https://open-meteo.com/). - Patil et al. [2023] Shishir G Patil, Tianjun Zhang, Xin Wang, and Joseph E Gonzalez. Gorilla: Large language model connected with massive apis. arXiv preprint arXiv:2305.15334, 2023.
- Rafailov et al. [2024] Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D Manning, Stefano Ermon, and Chelsea Finn. Direct preference optimization: Your language model is secretly a reward model. Advances in Neural Information Processing Systems, 36, 2024.
-
Rozière et al. [2024]
Baptiste Rozière, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi, Jingyu Liu, Romain Sauvestre, Tal Remez, Jérémy Rapin, Artyom Kozhevnikov, Ivan Evtimov, Joanna Bitton, Manish Bhatt, Cristian Canton Ferrer, Aaron Grattafiori, Wenhan Xiong, Alexandre Défossez, Jade Copet, Faisal Azhar, Hugo Touvron, Louis Martin, Nicolas Usunier, Thomas Scialom, and Gabriel Synnaeve.
Code llama: Open foundation models for code, 2024.
URL
[https://arxiv.org/abs/2308.12950](https://arxiv.org/abs/2308.12950). -
[17]
The-Movie-DB.
The movie db: Open source movie database.
URL
[https://www.themoviedb.org/](https://www.themoviedb.org/). - Wang et al. [2023] Xingyao Wang, Zihan Wang, Jiateng Liu, Yangyi Chen, Lifan Yuan, Hao Peng, and Heng Ji. Mint: Evaluating llms in multi-turn interaction with tools and language feedback. arXiv preprint arXiv:2309.10691, 2023.
- Wei et al. [2022] Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel, Barret Zoph, Sebastian Borgeaud, Dani Yogatama, Maarten Bosma, Denny Zhou, Donald Metzler, et al. Emergent abilities of large language models. arXiv preprint arXiv:2206.07682, 2022.
- Wei et al. [2024] Jerry Wei, Chengrun Yang, Xinying Song, Yifeng Lu, Nathan Hu, Dustin Tran, Daiyi Peng, Ruibo Liu, Da Huang, Cosmo Du, et al. Long-form factuality in large language models. arXiv preprint arXiv:2403.18802, 2024.
- Ye et al. [2024] Junjie Ye, Guanyu Li, Songyang Gao, Caishuang Huang, Yilong Wu, Sixian Li, Xiaoran Fan, Shihan Dou, Qi Zhang, Tao Gui, et al. Tooleyes: Fine-grained evaluation for tool learning capabilities of large language models in real-world scenarios. arXiv preprint arXiv:2401.00741, 2024.
- Zhang et al. [2024] Jianguo Zhang, Tian Lan, Rithesh Murthy, Zhiwei Liu, Weiran Yao, Juntao Tan, Thai Hoang, Liangwei Yang, Yihao Feng, Zuxin Liu, et al. Agentohana: Design unified data and training pipeline for effective agent learning. arXiv preprint arXiv:2402.15506, 2024.
- Zheng et al. [2024] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric Xing, et al. Judging llm-as-a-judge with mt-bench and chatbot arena. Advances in Neural Information Processing Systems, 36, 2024.
9 Appendix
9.1 Prompts for Query Augmentation
In the following section, we list all the prompts used in the process of query generation. All
9.1.1 Constraint Based Augmentation
Table LABEL:fig:table-5 here describes the constraint based query generation prompt with a sample fewshot examples from the spaceflight environment. For every new environment we have its specific set of fewshot examples.
9.1.2 Sentence Transform Based Augmentation
Table LABEL:fig:table-6 here describes the sentence transform based query generation prompt.
9.1.3 Irrelevance Based Augmentation
Table LABEL:fig:table-7 here describes the irrelevance based query generation prompt.
9.2 Query Selection for SpecTool
Based on the feasibility of solving the query given the provided APIs, we randomly select 150 base queries. We make sure that we dont introduce any duplicate or closely related queries generated by the augmentation.
9.2.1 Queries Selected for Feedback Ablation Study
For the feedback vs no feedback ablation study we use the same 150 queries to analyse the impact of the specific feedback provided to the model for executing the query successfully. Within, the average model score the major impact is caused on incorrect argument name, incorrect argument type and incorrect function name.
9.2.2 Queries Selected for Irrelevance Ablation Study
For the irrelevance ablation study, we specifically gather queries from the irrelevance augmentation. We do this for the base queries from 3 environments (Spaceflight, Movie and Patent). In total, this ablation study is done using 60 queries.
9.2.3 Queries Selected for API Complexity Ablation Study
For this study, we randomly collect 10 queries per environment to maintain unanimous averaging of scores across all the provided environments. The queries are selected from out original 150 base queries.
9.3 Prompt for Benchmark Inference
Table LABEL:fig:table-8 describes a sample prompt used during the inference in the Benchmark.
9.4 Sample Trajectory of the Benchmark
Table LABEL:fig:table-9 describes a sample trajectory and highlights over the specific feedback provided to execute the query.
| You are an expert in augmenting agent’s queries for given parameters. You will be given some few shot examples and a list of tools, with their descriptions and their required parameters and based on your knowledge you have to generate queries with constraints based on the tools provided. |
| Each of the answer is expected to follow the format below: |
| Query1: (constraint added query) |
| Query2: (constraint added query) |
| Queryn: …. |
| Your task is providing the queries with 3 or 4 constraints based on the list of tool calls available, using the following criteria: |
| 1. Add additional constraints to the query but make sure the query has single fixed answer instead of a worded description. |
| 2. Focus on making significant use of arguments of each tool call in an innovative way. Pay close attention on each Argument’s Description and their input requirements while using them in the query. |
| 3. Answer does not hallucinate and is relevant to the given tools list. |
| 4. Innovate around using functions that are similar but have a very distinct difference. |
| 5. Correctly follow the provided format. |
| FEWSHOT EXAMPLES: |
| Query1: Find articles from NASA or SpaceNews related to Artemis missions, not including those from European Spaceflight, limited to 2 results published between January 1st, 2021, and December 31st, 2021. |
| Query2: Retrieve the most recent article related to SpaceX from Spaceflight Now and the corresponding report with a summary mentioning F̈alcon Heavy,̈ both published after January 1st, 2020. |
| You are an expert at refining an agent’s queries by rephrasing sentences for clarity and precision without altering their intended meaning. |
| Each of the answer is expected to follow the format below: |
| Query1: (sentence transformed query) |
| Query2: (sentence transformed query) |
| Queryn: …. |
| You will receive some queries along with a list of tools, including their descriptions and required parameters. You will also be provided with an example of original vs augmented query. Your task is to transform each query’s sentence structure, ensuring that the revised sentence preserves the same context and intent as the original. Follow these criteria to guide your rephrasing: |
| 1. Maintain the query’s original context and aim, ensuring that the rephrased sentence yields the same single, definitive answer as the original. |
| 2. Keep the rephrased sentence relevant to the tools provided, without introducing any additional information or hallucination. |
| 3. Pay close attention to each tool’s specific parameters and descriptions, making sure the rephrased query aligns with the tools’ intended use. |
| 4. Follow the provided format precisely for each rephrased query. |
| ONE-SHOT EXAMPLE: |
| Original Query: Retrieve two articles focused on the Artemis missions, sourced only from NASA or SpaceNews, ensuring that no content originates from European Spaceflight, and limit the publication date to between January 1, 2021, and December 31, 2021. |
| Augmented Query: Find articles from NASA or SpaceNews related to Artemis missions, not including those from European Spaceflight, limited to 2 results published between January 1st, 2021, and December 31st, 2021. |
| You are an expert at creating modified queries with intentional irrelevance while maintaining the core context of the tools and arguments provided. |
| Each of the answer is expected to follow the format below: |
| Query1: (irrelevance added query) |
| Query2: (irrelevance added query) |
| Queryn: …. |
| You will receive some queries along with a list of tools, including their descriptions and required parameters. You will also be provided with an example of original vs augmented query. Your task is to introduce irrelevance by creating queries that either: |
| 1. Include a constraint or condition not relevant to any of the listed arguments, or |
| 2. Request execution of one function but provide parameters meant for a different function. |
| 3. Make a completely new request which is unrelated all the list of functions provided. |
| When modifying each query, follow these guidelines: 1. Ensure that the added irrelevance does not alter the core meaning but introduces a new element or mismatch that makes the query more challenging to interpret. |
| 2. On the original query section, the response should not hallucinate; it should remain constrained to the parameters available, even if they don’t perfectly match. |
| 3. Innovate by intentionally introducing subtle conflicts in argument requirements or irrelevant requests. |
| 4. Maintain the provided format for each modified query. |
| ONE-SHOT EXAMPLE: |
| Original Query: Find articles from NASA or SpaceNews related to Artemis missions, not including those from European Spaceflight, limited to 2 results published between January 1st, 2021, and December 31st, 2021. |
| Augmented Query: Retrieve two articles specifically with summary title containing Artemis missions, exclusively from NASA or SpaceNews, excluding any pieces from European Spaceflight. Ensure the publication dates fall within January 1, 2021, to December 31, 2021. Set an offset of 4 for the search results. |
Based on the previous context and API request history,
generate an API request or a response as an AI assistant.
We detail the available tools with their respective name,
description, input(parameters) of each action as follows:[ { "name": "get_joke_of_the_day_by_category", "description": "Get the joke of the day of a specific category", "parameters": { "category": { "type": "string", "description": "Category of the joke from the jokes categories API.", "required": true }, "limit": { "type": "number", "description": "Number of jokes to output.", "required": false }}}, ... { "name": "finish", "description": "Return an answer and finish the task.", "parameters": { "answer": { "type": ["string", "number", "array"], "description": "Finish task using the answer parameter.", "required": true }}} ]ONE-SHOT EXAMPLE: Goal: Please List all the categories of jokes available and provide me with 2 jokes of the day. Trajectory: Action: get_categories_of_joke with Action Input: {} Observation: [’food’, ’politics’, ’art’, ’sports’] Action: get_joke_of_the_day with Action Input: {limit: 2} Observation: [{’id’ : 1, ’result’: A man staggers into an emergency room with two black eyes and a five iron wrapped tightly around his throat. Naturally the doctor asks him what happened. } ...]Your output should follow the provided format which specifies the specific function to call along with its respective input. The example format is as follows. |
| Action: [your action] with Action Input: [your action input] If no function call is required additionally, please conclude the response using the finish function. |
|
|