# Source: https://docs.langchain.com/langsmith/trace-with-api
# Title: Trace with API - Docs by LangChain
# Fetched via: trafilatura
# Date: 2026-04-10

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Dict, List
import requests
from requests_toolbelt import MultipartEncoder
from uuid_utils.compat import uuid7
def create_dotted_order(
start_time: datetime | None = None,
run_id: uuid.UUID | None = None
) -> str:
"""Create a dotted order string for run ordering and hierarchy.
The dotted order is used to establish the sequence and relationships between runs.
It combines a timestamp with a unique identifier to ensure proper ordering and tracing.
"""
st = start_time or datetime.now(timezone.utc)
id_ = run_id or uuid7()
return f"{st.strftime('%Y%m%dT%H%M%S%fZ')}{id_}"
def create_run_base(
name: str,
run_type: str,
inputs: dict,
start_time: datetime
) -> dict:
"""Create the base structure for a run."""
run_id = uuid7()
return {
"id": str(run_id),
"trace_id": str(run_id),
"name": name,
"start_time": start_time.isoformat(),
"inputs": inputs,
"run_type": run_type,
}
def construct_run(
name: str,
run_type: str,
inputs: dict,
parent_dotted_order: str | None = None,
) -> dict:
"""Construct a run dictionary with the given parameters.
This function creates a run with a unique ID and dotted order, establishing its place
in the trace hierarchy if it's a child run.
"""
start_time = datetime.now(timezone.utc)
run = create_run_base(name, run_type, inputs, start_time)
current_dotted_order = create_dotted_order(start_time, uuid.UUID(run["id"]))
if parent_dotted_order:
current_dotted_order = f"{parent_dotted_order}.{current_dotted_order}"
run["trace_id"] = parent_dotted_order.split(".")[0].split("Z")[1]
run["parent_run_id"] = parent_dotted_order.split(".")[-1].split("Z")[1]
run["dotted_order"] = current_dotted_order
return run
def serialize_run(operation: str, run_data: dict) -> List[tuple]:
"""Serialize a run for the multipart request.
This function separates the run data into parts for efficient transmission and storage.
The main run data and optional fields (inputs, outputs, events) are serialized separately.
"""
run_id = run_data.get("id", str(uuid7()))
# Separate optional fields
inputs = run_data.pop("inputs", None)
outputs = run_data.pop("outputs", None)
events = run_data.pop("events", None)
parts = []
# Serialize main run data
run_data_json = json.dumps(run_data).encode("utf-8")
parts.append(
(
f"{operation}.{run_id}",
(
None,
run_data_json,
"application/json",
{"Content-Length": str(len(run_data_json))},
),
)
)
# Serialize optional fields
for key, value in [("inputs", inputs), ("outputs", outputs), ("events", events)]:
if value:
serialized_value = json.dumps(value).encode("utf-8")
parts.append(
(
f"{operation}.{run_id}.{key}",
(
None,
serialized_value,
"application/json",
{"Content-Length": str(len(serialized_value))},
),
)
)
return parts
def batch_ingest_runs(
api_url: str,
api_key: str,
posts: list[dict] | None = None,
patches: list[dict] | None = None,
) -> None:
"""Ingest multiple runs in a single batch request.
This function handles both creating new runs (posts) and updating existing runs (patches).
It's more efficient for ingesting multiple runs compared to individual API calls.
"""
boundary = uuid.uuid4().hex
all_parts = []
for operation, runs in zip(("post", "patch"), (posts, patches)):
if runs:
all_parts.extend(
[part for run in runs for part in serialize_run(operation, run)]
)
encoder = MultipartEncoder(fields=all_parts, boundary=boundary)
headers = {"Content-Type": encoder.content_type, "x-api-key": api_key}
try:
response = requests.post(
f"{api_url}/runs/multipart",
data=encoder,
headers=headers
)
response.raise_for_status()
print("Successfully ingested runs.")
except requests.RequestException as e:
print(f"Error ingesting runs: {e}")
# In a production environment, you might want to log this error or handle it more robustly
# Configure API URL and key
# For production use, consider using a configuration file or environment variables
api_url = "https://api.smith.langchain.com"
api_key = os.environ.get("LANGSMITH_API_KEY")
if not api_key:
raise ValueError("LANGSMITH_API_KEY environment variable is not set")
# Create a parent run
parent_run = construct_run(
name="Parent Run",
run_type="chain",
inputs={"main_question": "Tell me about France"},
)
# Create a child run, linked to the parent
child_run = construct_run(
name="Child Run",
run_type="llm",
inputs={"question": "What is the capital of France?"},
parent_dotted_order=parent_run["dotted_order"],
)
# First, post the runs to create them
posts = [parent_run, child_run]
batch_ingest_runs(api_url, api_key, posts=posts)
# Then, update the runs with their end times and any outputs
child_run_update = {
**child_run,
"end_time": datetime.now(timezone.utc).isoformat(),
"outputs": {"answer": "Paris is the capital of France."},
}
parent_run_update = {
**parent_run,
"end_time": datetime.now(timezone.utc).isoformat(),
"outputs": {"summary": "Discussion about France, including its capital."},
}
patches = [parent_run_update, child_run_update]
batch_ingest_runs(api_url, api_key, patches=patches)
# Note: This example requires the `requests` and `requests_toolbelt` libraries.
# You can install them using pip:
# pip install requests requests_toolbelt