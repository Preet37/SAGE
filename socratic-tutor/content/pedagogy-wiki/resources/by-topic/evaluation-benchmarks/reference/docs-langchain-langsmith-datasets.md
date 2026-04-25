# Source: https://docs.langchain.com/langsmith/datasets
# Title: Manage datasets (Docs by LangChain)
# Fetched via: search
# Date: 2026-04-10

LangSmith provides tools for managing and working with your *datasets*.
This page describes dataset operations including: - Versioning datasets to track changes over time.
- Filtering and splitting datasets for evaluation.
- Sharing datasets publicly.
- Exporting datasets in various formats.
You’ll also learn how to export filtered traces from experiments back to datasets for further analysis and iteration.
## ​ Version a dataset
In LangSmith, datasets are versioned.
This means that every time you add, update, or delete examples in your dataset, a new version of the dataset is created.
### ​ Create a new version of a dataset
Any time you add, update, or delete examples in your dataset, a new version of your dataset is created.
This allows you to track changes to your dataset over time and understand how your dataset has evolved.
By default, the version is defined by the timestamp of the change.
When you click on a particular version of a dataset (by timestamp) in the **Examples** tab, you will find the state of the dataset at that point in time.
Note that examples are read-only when viewing a past version of the dataset.
You will also see the operations that were between this version of the dataset and the latest version of the dataset.
By default, the latest version of the dataset is shown in the **Examples** tab and experiments from all versions are shown in the **Tests** tab.
In the **Tests** tab, you will find the results of tests run on the dataset at different versions.
### ​ Tag a version
You can also tag versions of your dataset to give them a more human-readable name, which can be useful for marking important milestones in your dataset’s history.
For example, you might tag a version of your dataset as “prod” and use it to run tests against your LLM pipeline.
You can tag a version of your dataset in the UI by clicking on **+ Tag this version** in the **Examples** tab.
You can also tag versions of your dataset using the SDK.
Here’s an example of how to tag a version of a dataset using the Python SDK:
```
from langsmith import Client
from datetime import datetime
client = Client()
initial_time = datetime(2024, 1, 1, 0, 0, 0) # The timestamp of the version you want to tag
# You can tag a specific dataset version with a semantic name, like "prod"
client.update_dataset_tag(
dataset_name=toxic_dataset_name, as_of=initial_time, tag="prod"
)
```
To run an evaluation on a particular tagged version of a dataset, refer to the Evaluate on a specific dataset version section.
## ​ Evaluate on a specific dataset version
...
You can use `evaluate` / `aevaluate` to pass in an iterable of examples to evaluate on a particular version of a dataset.
Use `list_examples` / `listExamples` to fetch examples from a particular version tag using `as_of` / `asOf` and pass that into the `data` argument.
```
from langsmith import Client
ls_client = Client()
# Assumes actual outputs have a 'class' key.
# Assumes example outputs have a 'label' key.
def correct(outputs: dict, reference_outputs: dict) -> bool:
return outputs["class"] == reference_outputs["label"]
results = ls_client.evaluate(
lambda inputs: {"class": "Not toxic"},
# Pass in filtered data here:
data=ls_client.list_examples(
dataset_name="Toxic Queries",
as_of="latest", # specify version here
),
evaluators=[correct],
)
```
Learn more about how to fetch views of a dataset on the Create and manage datasets programmatically page.
## ​ Evaluate on a split / filtered view of a dataset
...
You can use the `list_examples` / `listExamples` method to fetch a subset of examples from a dataset to evaluate on.
One common workflow is to fetch examples that have a certain metadata key-value pair.
```
from langsmith import evaluate
results = evaluate(
lambda inputs: label_text(inputs["text"]),
data=client.list_examples(dataset_name=dataset_name, metadata={"desired_key": "desired_value"}),
evaluators=[correct_label],
experiment_prefix="Toxic Queries",
)
```
For more filtering capabilities, refer to this how-to guide.
### ​ Evaluate on a dataset split
You can use the `list_examples` / `listExamples` method to evaluate on one or multiple splits of your dataset.
The `splits` parameter takes a list of the splits you would like to evaluate.
```
from langsmith import evaluate
results = evaluate(
lambda inputs: label_text(inputs["text"]),
data=client.list_examples(dataset_name=dataset_name, splits=["test", "training"]),
evaluators=[correct_label],
experiment_prefix="Toxic Queries",
)
```
For more details on fetching views of a dataset, refer to the guide on fetching datasets.
## ​ Share a dataset
### ​ Share a dataset publicly
From the **Dataset & Experiments** tab, select a dataset, click **⋮** (top right of the page), click **Share Dataset**.
This will open a dialog where you can copy the link to the dataset.
### ​ Unshare a dataset
1. Click on **Unshare** by clicking on **Public** in the upper right hand corner of any publicly shared dataset, then **Unshare** in the dialog.
2. Navigate to your organization’s list of publicly shared datasets, by clicking on **Settings** -> **Shared URLs** or this link, then click on **Unshare** next to the dataset you want to unshare.
## ​ Export a dataset
You can export your LangSmith dataset to a CSV, JSONL, or OpenAI’s fine tuning format from the LangSmith UI.
From the **Dataset & Experiments** tab, select a dataset, click **⋮** (top right of the page), click **Download Dataset**.
…
### ​ View experiment traces
To do so, first click on the arrow next to your experiment name.
This will direct you to a project that contains the traces generated from your experiment.
From there, you can filter the traces based on your evaluation criteria.
In this example, we’re filtering for all traces that received an accuracy score greater than 0.5.
After applying the filter on the project, we can multi-select runs to add to the dataset, and click **Add to Dataset**.

*Datasets* enable you to perform repeatable evaluations over time using consistent data.
Datasets are made up of *examples*, which store inputs, outputs, and optionally, reference outputs.
This page outlines the various methods for creating and managing datasets in the UI.
## ​ Create a dataset and add examples
The following sections explain the different ways you can create a dataset in LangSmith and add examples to it.
Depending on your workflow, you can manually curate examples, automatically capture them from tracing, import files, or even generate synthetic data: - Manually from a tracing project
- Automatically from a tracing project
- From examples in an annotation queue
- From the Playground
- Import a dataset from a CSV or JSONL file
- Create a new dataset from the dataset page
- Add synthetic examples created by an LLM via the Datasets UI
### ​ Manually from a tracing project
A common pattern for constructing datasets is to convert notable traces from your application into dataset examples.
This approach requires that you have configured tracing to LangSmith.
A technique to build datasets is to filter the most interesting traces, such as traces that were tagged with poor user feedback, and add them to a dataset.
For tips on how to filter traces, refer to the Filter traces guide.
There are two ways to add data manually from a tracing project to datasets.
Navigate to **Tracing Projects** and select a project.
1. Multi-select runs from the runs table.
On the **Runs** tab, multi-select runs.
At the bottom of the page, click **Add to Dataset**.
2. On the **Runs** tab, select a run from the table.
On the individual run details page, select **Add to** -> **Dataset** in the top right corner.
When you select a dataset from the run details page, a modal will pop up letting you know if any transformations were applied or if schema validation failed.
You can then optionally edit the run before adding it to the dataset.
### ​ Automatically from a tracing project
You can use run rules to add traces automatically to a dataset based on certain conditions.
For example, you could add all traces that are tagged with a specific use case or have a low feedback score.
### ​ From examples in an annotation queue
If you rely on subject matter experts to build meaningful datasets, use annotation queues to provide a streamlined view for reviewers.
Human reviewers can optionally modify the inputs/outputs/reference outputs from a trace before it is added to the dataset.
You can optionally configure annotation queues with a default dataset, though you can add runs to any dataset by using the dataset switcher on the bottom of the screen.
Once you select the right dataset, click **Add to Dataset** or hit the hot key `D` to add the run to it.
Any modifications you make to the run in your annotation queue will carry over to the dataset, and all metadata associated with the run will also be copied.
### ​ From the Playground
On the **Playground** page: 1.
Select **Set up Evaluation**.
2. Click **+New** if you’re starting a new dataset or select from an existing dataset.
Creating datasets inline in the Playground is not supported for datasets that have nested keys.
In order to add/edit examples with nested keys, you must edit from the datasets page.
3. Edit the examples: - Use **+Row** to add a new example to the dataset.
- Delete an example using the **⋮** dropdown on the right-hand side of the table.
- If you’re creating a reference-free dataset, remove the **Reference Output** column using the **x** button in the column.
Note that this action is not reversible.
### ​ Import a dataset from a CSV or JSONL file
On the **Datasets & Experiments** page, click **+New Dataset**, then **Import** an existing dataset from CSV or JSONL file.
### ​ Create a new dataset from the datasets & experiments page
1. Navigate to the **Datasets & Experiments** page from the left-hand menu.
2. Click **+ New Dataset**.
3. On the **New Dataset** page, select the **Create from scratch** tab.
4. Add a name and description for the dataset.
5. (Optional) Create a dataset schema to validate your dataset.
6. Click **Create**, which will create an empty dataset.
7. To add examples inline, on the dataset’s page, go to the **Examples** tab.
Click **+ Example**.
8. Define examples in JSON and click **Submit**.
For more details on dataset splits, refer to Create and manage dataset splits.
### ​ Add synthetic examples created by an LLM
If you have existing examples and a schema defined on your dataset, when you click **+ Example** there is an option to **Add AI-Generated Examples**.
This will use an LLM to create synthetic examples.
In **Generate examples**, do the following: 1.
Click **API Key** in the top right of the pane to set your OpenAI API key as a workspace secret.
If your workspace already has an OpenAI API key set, you can skip this step.
2. Select : Toggle **Automatic** or **Manual** reference examples.
You can select these examples manually from your dataset or use the automatic selection option.
3. Enter the number of synthetic examples you want to generate.
4.
Click **Generate**.
5. The examples will appear on the **Select generated examples** page.
Choose which examples to add to your dataset, with the option to edit them before finalizing.
Click **Save Examples**.
6. Each example will be validated against your specified dataset schema and tagged as **synthetic** in the source metadata.
## ​ Manage a dataset
### ​ Create a dataset schema
LangSmith datasets store arbitrary JSON objects.
We recommend (but do not require) that you define a schema for your dataset to ensure that they conform to a specific JSON schema.
Dataset schemas are defined with standard JSON schema, with the addition of a few prebuilt types that make it easier to type common primitives like messages and tools.
Certain fields in your schema have a `+ Transformations` option.
Transformations are preprocessing steps that, if enabled, update your examples when you add them to the dataset.
...
For an overview of when and why to use splits, refer to Dataset organization.
To create and manage splits in the UI: 1.
Select examples in your dataset.
2. Click **Add to Split**.
3. From the resulting popup menu, you can select and unselect splits for the selected examples, or create a new split.
### ​ Edit example metadata
To add metadata to your examples: 1.
Click on an example and then click **Edit** on the top right-hand side of the popover.
2. From this page, update or delete existing metadata, or add new metadata.
You may use this to store information about your examples, such as tags or version info, which you can then group by when analyzing experiment results or filter by when you call `list_examples` in the SDK.
### ​ Filter examples
You can filter examples by split, metadata key/value or perform full-text search over examples.
These filtering options are available to the top left of the examples table: - **Filter by split**: Select split > Select a split to filter by.
- **Filter by metadata**: Filters > Select **Metadata** from the dropdown > Select the metadata key and value to filter on.
- **Full-text search**: Filters > Select **Full Text** from the dropdown > Enter your search criteria.
You may add multiple filters, and only examples that satisfy all of the filters will be displayed in the table.

The notebook demonstrates how to create a **dataset for evaluating Retrieval-Augmented Generation (RAG) models using LangSmith.** It includes steps for setting up environment variables, creating datasets with questions and answers, and uploading examples to LangSmith for testing.
Additionally, it provides instructions on using HuggingFace datasets and updating datasets with new examples.
### Table of Contents
### References
...
Setting up your environment is the first step.
See the Environment Setup guide for more details.
...
You can set API keys in a
```
.env
```
file or set them manually.
[Note] If you’re not using the
```
.env
```
file, no worries!
Just enter the keys directly in the cell below, and you’re good to go.
You can alternatively set API keys such as
```
OPENAI_API_KEY
```
in a
```
.env
```
file and load them.
[Note] This is not necessary if you've already set the required API keys in previous steps.
...
Let's learn how to build a custom RAG evaluation dataset.
To construct a dataset, you need to understand three main processes:
Case: Evaluating whether the retrieval is relevant to the question
> Question - Retrieval
Case: Evaluating whether the answer is relevant to the question
> Question - Answer
Case: Checking if the answer is based on the retrieved documents (Hallucination Check)
> Retrieval - Answer
Thus, you typically need
```
Question
```
```
Retrieval
```
, and
```
Answer
```
information.
However, it is practically challenging to construct ground truth for
```
Retrieval
```
If ground truth for
```
Retrieval
```
exists, you can save and use it all in your dataset.
Otherwise, you can create and use a dataset with only
```
Question
```
and
```
Answer
```
## Creating Examples for LangSmith Dataset
Use
```
inputs
```
and
```
outputs
```
to create a dataset.
The dataset consists of
```
questions
```
and
```
answers
```
0
What is the name of the generative AI created ...## Creating a Dataset for LangSmith Testing
- Create a new dataset under
```
Datasets & Testing
```
.
You can also create a dataset directly using the LangSmith UI from a CSV file.
For more details, refer to the documentation below:
You can add examples to the dataset later.
Congratulations!
The dataset is now ready.
Last updated

### Real-time monitoring and visualization
LangSmith uses traces to log almost every aspect of LLM runs.
These include metrics such as latency, token count, price of runs, and all types of metadata.
The Web UI allows you to quickly filter runs based on error percentage, latency, date, or even by text content using natural language.
This means that if, for instance, an AI tutor starts glitching in its responses to actual students, you can push out a fix in a few hours.
### Integration with LangChain
LangChain is the parent framework of LangSmith focused specifically on the development phase of LLMs.
It offers modular software design to chain multiple LLMs (agents) and integrate them with other APIs such as YouTube, Google Search and so on.
LangSmith is the cherry on top, ensuring that prototypes built with LangChain perform as expected by using its powerful evaluation and monitoring tools.
…
### Datasets
Another great feature of LangSmith is datasets.
They can be used to improve LangChain chains, agents or models against a set of standardized examples before deployment.
For example, we may have a CSV file containing two columns — questions and answers for flashcards in a specific format.
By converting this file into a reference dataset, we can instruct LLMs to evaluate their own output using the quality assurance metrics mentioned earlier.
We will now see all these features through examples one-by-one.
…
...
## LangSmith Platform Overview
We will begin with understanding the web UI.
It is available through smith.langchain.com link.
For access, you have to sign up and get cleared from the waitlist, as it is currently in closed beta.
But once you are in, the landing page will look like this:
The two main sections are projects and datasets & testing, and both sections can be manipulated through Python SDK.
The platform also has tabs for deployment and annotation queues, but they are beyond the scope of this article.
…
## Creating an Unlabeled Dataset in LangSmith
As I mentioned in the “LLM application development workflow” section, you will likely need to create or collect thousands of prompts to evaluate your LLM model, chain, or agent.
So, running those one-by-one as we did above isn’t best practice.
For this reason, LangSmith offers datasets in three types:
…
) - default: Defines inputs as arbitrary key-value pairs.
They are useful when evaluating chains and agents that require multiple inputs or return multiple outputs.
- LLM datasets (
…
): These are datasets converted from LLM chats and defined using structured inputs and serialized messages.
First, let’s see how to create a key-value dataset with no outputs.
We will use the
…
```
create_dataset function of the client:
dataset_name = "deep_learning_fundamentals"
# Creating a blank dataset
dl_dataset = client.create_dataset(
dataset_name=dataset_name,
description="A deck containing flashcards on NNs and PyTorch",
data_type="kv", # default
```
…
```
# Storing only inputs into a dataset
example_inputs = [
"Generate a single flashcard on backpropagation",
"Generate a single flashcard on the use of torch.no_grad",
"Generate a single flashcard on how Adam optimizer",
for ex in example_inputs:
# Each example input must be unique
# The output is optional
client.create_example(
inputs={"input": ex},
outputs=None,
dataset_id=dl_dataset.id,
)
```
If you go over the dataset tab of the UI, you will see each prompt listed with NULL output:
Now, let’s run all the prompts in a single line of code using run_on_dataset function:
```
from langchain.smith import run_on_dataset
results = run_on_dataset(
client=client,
dataset_name=dataset_name,
llm_or_chain_factory=llm,
project_name="unlabeled_test",
```
Once the run finishes, it will be listed on the dataset page.
Here is what it looks like:
We just did a test run on an unlabeled dataset — a dataset with example prompts but no example outputs.
Our test simply produced a response to each prompt but didn’t evaluate anything.
But we’d like to perform basic checks such as “Is the output helpful?” or “Is the response short or long”?
…
is a helpful function to run all prompts in a dataset using the provided LLM and perform any type of evaluation on the fly.
Its results will be visible on the dedicated page of each dataset:
This time, the run has coherence and conciseness metrics for each prompt.
At the bottom, you will also see an average score for each metric.
…
## Creating Labeled Datasets
Sometimes, you may decide to create a dataset of prompts with expected outputs, e.g., labeled datasets.
You can create labeled datasets in various formats, but perhaps the most common one is a CSV file.
For example, here is a file I generated with ChatGPT that contains five questions on PyTorch syntax:
To create a dataset from this, we can use the
…
The function has three required parameters: CSV path and the names of input/output columns.
Once the upload finishes, the dataset will appear in the UI:
Let’s run our custom criterion from the previous section on this dataset as well:

This page explains the core components of LangSmith's evaluation framework: datasets and evaluators.
These are the fundamental building blocks for evaluating and improving LLM applications.
If you're looking for information about testing framework integration, see Testing Framework Integration, and for multimodal evaluation specifics, see Multimodal Evaluation.
...
The quality and development speed of AI applications is often limited by the availability of high-quality evaluation datasets and metrics.
LangSmith makes building robust evaluations easy through its evaluation framework.
The two key building blocks of this framework are:
- **Datasets**: Collections of test inputs and reference outputs
- **Evaluators**: Functions for scoring application outputs
…
## Datasets
A dataset is a collection of examples used for evaluating an application.
An example is a test input and reference output pair.
### Examples Structure
Each example in a dataset consists of:
- **Inputs**: A dictionary of input variables to pass to your application
- **Reference outputs** (optional): A dictionary of reference outputs used for evaluation (not passed to your application)
- **Metadata** (optional): Additional information that can be used to create filtered views of a dataset
…
#### Manually Curated Examples
...
To determine which runs are valuable to add to a dataset, you can use:
- **User feedback**: Collect end user feedback to identify problematic runs
- **Heuristics**: Use metrics like completion time to identify "interesting" datapoints
- **LLM feedback**: Use another LLM to detect noteworthy runs, such as conversations where users had to rephrase questions
#### Synthetic Data
Once you have a few examples, you can artificially generate more.
It's generally advised to have a few good hand-crafted examples first, as synthetic data will often resemble them.
...
Datasets are versioned such that every time you add, update, or delete examples in your dataset, a new version is created.
This makes it easy to inspect and revert changes to your dataset if you make a mistake.
You can also tag versions of your dataset to give them a more human-readable name.
You can run evaluations on specific versions of a dataset.
This can be useful when running evaluations in CI, to make sure that dataset updates don't accidentally break your CI pipelines.
...
**Inputs:**
- **Example**: The example from your dataset, containing inputs, reference outputs, and metadata
- **Run**: The actual outputs and intermediate steps from passing the example inputs to your application
**Outputs:** An evaluator returns one or more metrics as a dictionary or list of dictionaries with:
- `key`: The name of the metric
- `score` | `value`: The value of the metric (use `score` for numerical metrics, `value` for categorical)
- `comment` (optional): The reasoning or additional information justifying the score
…
### Defining Evaluators
There are several ways to define and run evaluators:
- **Custom code**: Define custom evaluators as Python or TypeScript functions and run them client-side using the SDKs or server-side via the UI
- **Built-in evaluators**: LangSmith has built-in evaluators that you can configure and run via the UI
You can run evaluators using the LangSmith SDK (Python and TypeScript), via the Prompt Playground, or by configuring Rules to automatically run them on particular tracing projects or datasets.
Sources: docs/evaluation/concepts/index.mdx94-101
...
LangSmith's annotation queues make it easy to get human feedback on your application's outputs.
...
In LangSmith, you can easily view all the experiments associated with your dataset and compare multiple experiments in a comparison view.