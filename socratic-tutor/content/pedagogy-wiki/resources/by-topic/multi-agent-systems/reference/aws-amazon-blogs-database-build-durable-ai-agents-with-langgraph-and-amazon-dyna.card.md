# Card: Durable LangGraph Agents w/ DynamoDBSaver
**Source:** https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/  
**Role:** explainer | **Need:** DEPLOYMENT_CASE  
**Anchor:** End-to-end durable agent architecture using LangGraph + DynamoDB as checkpoint store (schema/flow for resume/replay)

## Key Content
- **Why LangGraph (graph control flow):** Define **nodes** (tasks) and **edges** (control flow) that can **branch, merge, and loop** (cyclic graphs), enabling complex, stateful workflows beyond linear chains.
- **Core persistence concepts (LangGraph):**
  - **Thread** = unique identifier for accumulated state across runs; must pass `thread_id` in config:  
    **Eq. 1 (Thread config):** `{"configurable": {"thread_id": "1"}}`
  - **Checkpoint** = snapshot saved each **super-step** as a `StateSnapshot` containing: config, metadata, state channel values, next nodes to execute, and task info (errors/interrupts).
  - Example: a **2-node graph** yields **4 checkpoints**: empty at `START`, after user input (before `node_a`), after `node_a` output (before `node_b`), final after `node_b` at `END`.
- **Why persistence matters (production rationale):** In-memory checkpoints are **ephemeral + local** → lost on restart; multi-worker runs have isolated state → cannot resume across workers or recover mid-run. Persistent store enables **resume, replay, human-in-the-loop, time travel debugging, audit**.
- **DynamoDBSaver design (langgraph-checkpoint-aws):**
  - **Small checkpoint threshold:** `< 350 KB` stored directly in **DynamoDB** (serialized item + metadata: `thread_id`, `checkpoint_id`, timestamps, state).
  - **Large checkpoints:** `≥ 350 KB` state stored in **S3**; DynamoDB stores an S3 pointer; retrieval transparently loads from S3.
  - **Cost/lifecycle knobs:** `ttl_seconds` (auto-expire checkpoints) and `enable_checkpoint_compression` (serialize+compress to reduce DynamoDB/S3 costs).
- **Required DynamoDB table schema:** partition key **`PK` (String)** and sort key **`SK` (String)**.
- **IAM permissions (minimum):**
  - DynamoDB: `GetItem`, `PutItem`, `Query`, `BatchGetItem`, `BatchWriteItem`
  - S3 (large checkpoints): `PutObject`, `GetObject`, `DeleteObject`, `PutObjectTagging`, plus bucket lifecycle `GetBucketLifecycleConfiguration`, `PutBucketLifecycleConfiguration`.

## When to surface
Use when students ask how to make LangGraph agents **durable in production** (resume after failure, multi-worker scaling, long-running threads) or how **DynamoDBSaver** stores checkpoints (350 KB split, PK/SK schema, TTL/compression, required IAM).