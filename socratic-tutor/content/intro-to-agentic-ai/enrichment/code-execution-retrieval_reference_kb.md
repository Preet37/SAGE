## Key Facts & Specifications

### OpenAI function/tool calling (JSON Schema)
- Function calling (tool calling) lets OpenAI models “interface with external systems and access data outside their training data.” Tools can be **function tools** (defined by a JSON schema) or **custom tools** (free-form text inputs/outputs). (OpenAI Function calling guide: https://platform.openai.com/docs/guides/function-calling)
- A **function** is “a specific kind of tool, defined by a JSON schema.” (OpenAI Function calling guide: https://platform.openai.com/docs/guides/function-calling)
- Function definition fields include: `type` (always `function`), `name`, `description`, `parameters` (JSON Schema), and `strict` (enforce strict mode). (OpenAI Function calling guide: https://platform.openai.com/docs/guides/function-calling)
- Example schema features shown in the guide include: `type: "object"`, `properties`, `required`, `enum`, and `additionalProperties: false`, with `strict: true`. (OpenAI Function calling guide: https://platform.openai.com/docs/guides/function-calling)

### OpenAI Code Interpreter tool (containers, memory tiers, expiry)
- Code Interpreter allows models to “write and run Python code in a sandboxed environment” for data analysis, coding, and math; it can process files and generate files (including images/graphs). (OpenAI Code Interpreter guide: https://developers.openai.com/api/docs/guides/tools-code-interpreter)
- Code Interpreter requires a **container object**; a container is “a fully sandboxed virtual machine” that can run Python and contain uploaded/generated files. (OpenAI Code Interpreter guide: https://developers.openai.com/api/docs/guides/tools-code-interpreter)
- Container creation modes:
  - **Auto mode**: pass `container: { "type": "auto", "memory_limit": "4g", "file_ids": [...] }` in tool configuration; it “automatically creates a new container, or reuses an active container” from prior context. (OpenAI Code Interpreter guide: https://developers.openai.com/api/docs/guides/tools-code-interpreter)
  - **Explicit mode**: create via `v1/containers` endpoint and then reference its `id` in the tool configuration. (OpenAI Code Interpreter guide: https://developers.openai.com/api/docs/guides/tools-code-interpreter)
- Memory tiers: `1g` (default), `4g`, `16g`, `64g`. Leaving out `memory_limit` keeps the default **1 GB** tier. (OpenAI Code Interpreter guide: https://developers.openai.com/api/docs/guides/tools-code-interpreter)
- Container lifecycle:
  - A container “expires if it is not used for **20 minutes**”; after expiry, using it in `v1/responses` fails and “all data… will be discarded… and not recoverable.” (OpenAI Code Interpreter guide: https://developers.openai.com/api/docs/guides/tools-code-interpreter)
  - You “can’t move a container from an expired state to an active one”; must create a new container and re-upload files; in-memory state (Python objects) is lost. (OpenAI Code Interpreter guide: https://developers.openai.com/api/docs/guides/tools-code-interpreter)
  - “Any container operation… will automatically refresh” `last_active_at`. (OpenAI Code Interpreter guide: https://developers.openai.com/api/docs/guides/tools-code-interpreter)

### E2B sandboxes (timeouts, defaults, max runtime, network controls)
- Sandbox continuous runtime limits: “up to **24 hours (Pro)** or **1 hour (Base)**.” (E2B Sandbox lifecycle docs: https://e2b.dev/docs/sandbox)
- E2B JS SDK defaults:
  - `timeoutMs` default is **300_000 ms (5 minutes)**. (E2B JS SDK reference: https://e2b.dev/docs/sdk-reference/js-sdk/v1.0.1/sandbox)
  - `requestTimeoutMs` default is **30_000 ms (30 seconds)**. (E2B JS SDK reference: https://e2b.dev/docs/sdk-reference/js-sdk/v1.0.1/sandbox)
- Max keep-alive via `setTimeout`: **86_400_000 ms (24h)** for Pro and **3_600_000 ms (1h)** for Hobby users. (E2B JS SDK reference: https://e2b.dev/docs/sdk-reference/js-sdk/v1.0.1/sandbox)
- Internet access:
  - `allowInternetAccess` defaults to `true`; can be disabled. (E2B Internet access docs: https://e2b.dev/docs/sandbox/internet-access)
  - Setting `allowInternetAccess: false` is equivalent to `network.denyOut: ['0.0.0.0/0']`. (E2B Internet access docs: https://e2b.dev/docs/sandbox/internet-access)
- Fine-grained egress rules:
  - `allowOut` entries can be CIDR (e.g. `"8.8.8.8/32"`), bare IP, or domain (e.g. `"example.com"`, `"*.example.com"`). (E2B PUT network API: https://e2b.dev/docs/api-reference/sandboxes/put-sandboxes-network)
  - `denyOut` supports CIDR/IP only; “Domain names are not supported for deny rules.” (E2B PUT network API: https://e2b.dev/docs/api-reference/sandboxes/put-sandboxes-network)
  - Priority: “allow rules always take precedence” over deny rules. (E2B Internet access docs: https://e2b.dev/docs/sandbox/internet-access)
- Public URL access:
  - “By default, sandbox URLs are publicly accessible.”
  - If `network.allowPublicTraffic: false`, requests must include header `e2b-traffic-access-token` with `sandbox.trafficAccessToken`; otherwise 403. (E2B Internet access docs: https://e2b.dev/docs/sandbox/internet-access)

### Docker resource constraints (CPU/memory flags)
- By default, a container has **no resource constraints** and can use as much as the host scheduler allows. (Docker Docs, Resource constraints: https://docs.docker.com/engine/containers/resource_constraints/)
- CPU limit flag: `--cpus=<value>`; example: host has 2 CPUs, `--cpus="1.5"` guarantees at most 1.5 CPUs; equivalent to `--cpu-period="100000"` and `--cpu-quota="150000"`. (Docker Docs, Resource constraints: https://docs.docker.com/engine/containers/resource_constraints/)
- CPU pinning: `--cpuset-cpus` uses comma-separated list or hyphen range; “The first CPU is numbered 0.” Example values: `0-3` or `1,3`. (Docker Docs, Resource constraints: https://docs.docker.com/engine/containers/resource_constraints/)
- Memory limits:
  - Docker can enforce **hard** and **soft** memory limits. (Docker Docs, Resource constraints: https://docs.docker.com/engine/containers/resource_constraints/)
  - If using `--memory-reservation`, it “must be set lower than `--memory`.” (Docker Docs, Resource constraints: https://docs.docker.com/engine/containers/resource_constraints/)
  - `--oom-kill-disable`: “Only disable the OOM killer… where you have also set `-m/--memory`.” If `-m` isn’t set, host can run out of memory and kernel may kill host processes. (Docker Docs, Resource constraints: https://docs.docker.com/engine/containers/resource_constraints/)

### Docker security (daemon, namespaces/cgroups, capabilities)
- Docker security areas include kernel namespaces/cgroups, Docker daemon attack surface, container configuration loopholes, and kernel hardening features. (Docker Engine security: https://docs.docker.com/engine/security/)
- Docker daemon “requires `root` privileges unless you opt-in to Rootless mode.” (Docker Engine security: https://docs.docker.com/engine/security/)
- Exposing Docker daemon API over HTTP without TLS is “not permitted” and causes the daemon to “fail early on startup.” (Docker Engine security: https://docs.docker.com/engine/security/)
- Capabilities: Docker “drops all capabilities except those needed” (allowlist approach); best practice is to “remove all capabilities except those explicitly required.” (Docker Engine security: https://docs.docker.com/engine/security/)

### Firecracker microVMs (limits, performance, architecture)
- Firecracker microVMs:
  - Combine “security and workload isolation properties of traditional VMs” with “speed, agility and resource efficiency enabled by containers.” (Firecracker design.md: https://github.com/firecracker-microvm/firecracker/blob/main/docs/design.md)
  - Support vCPU “up to **32**” and configurable memory. (Firecracker design.md)
  - With minimal kernel, single-core CPU, and **128 MiB RAM**, supports “steady mutation rate of **5 microVMs per host core per second**” (example: **180 microVMs/sec** on 36 cores). (Firecracker design.md)
  - Each microVM exposes a host-facing API via an in-process HTTP server. (Firecracker design.md)
  - Each Firecracker process encapsulates “one and only one microVM.” Threads: API, VMM, and vCPU thread(s). (Firecracker design.md)
- Sandboxing/defense-in-depth:
  - Firecracker uses seccomp filters by default; recommends running with `jailer` to apply cgroups/namespaces and drop privileges. (Firecracker design.md)
- Note on third-party Firecracker performance claims:
  - A Northflank blog claims boot “as little as **125 ms**,” “< **5 MiB** memory overhead,” and “up to **150 microVMs/sec**.” (Northflank blog: https://northflank.com/blog/what-is-aws-firecracker)
  - These numbers **do not match** the Firecracker design doc’s cited example rate (5 microVMs/core/sec; 180/sec on 36 cores). Treat as separate, non-official claims. (Northflank blog vs Firecracker design.md)

### RAG chunking experiment results (NVIDIA)
- NVIDIA reports experiments with:
  - Embedding model: `nvidia/llama-3.2-nv-embedqa-1b-v2`
  - Reranking model: `nvidia/llama-3.2-nv-rerankqa-1b-v2`
  - Retrieval `top-k`: **10** contexts for generation. (NVIDIA blog: https://developer.nvidia.com/blog/finding-the-best-chunking-strategy-for-accurate-ai-responses/)
- Reported results across datasets:
  - Page-level chunking highest average accuracy **0.648** with std dev **0.107**.
  - Token-based approaches between **0.603** and **0.645**. (NVIDIA blog)

### Vector similarity metrics (cosine/dot/L2)
- Rule of thumb: “match [index similarity metric] to the one used to train your embedding model.” (Pinecone: https://www.pinecone.io/learn/vector-similarity/; Zilliz: https://zilliz.com/blog/similarity-metrics-for-vector-search)
- Cosine similarity range: **-1 to 1**; 1 means angle 0°, 0 means orthogonal, -1 opposite direction. (Pinecone: https://www.pinecone.io/learn/vector-similarity/; Zilliz: https://zilliz.com/blog/similarity-metrics-for-vector-search)
- If model trained with cosine similarity, you can “either use cosine similarity or normalize and use dot product” (mathematically equivalent). (Pinecone: https://www.pinecone.io/learn/vector-similarity/)

### Text-to-SQL schema linking (RSL-SQL paper)
- RSL-SQL reports:
  - Bidirectional schema linking achieves “strict recall of **94%**” and reduces number of input columns by **83%**. (RSL-SQL arXiv HTML v2: https://arxiv.org/html/2411.00073v2)
- Risks of schema linking noted:
  - Risk 1: missing necessary tables/columns → erroneous SQL.
  - Risk 2: even with required elements identified, schema linking can degrade performance. (RSL-SQL arXiv)

### PostgreSQL information_schema caveat + FK query
- PostgreSQL note: standard-compliant constraint queries expecting one row can return several because SQL standard requires constraint names unique within a schema, but PostgreSQL does not enforce this; can affect views including `referential_constraints`. (PostgreSQL docs: https://www.postgresql.org/docs/current/information-schema.html and older version note: https://www.postgresql.org/docs/9.2/information-schema.html)
- Example query to list columns with foreign key references uses `information_schema.columns`, `key_column_usage`, `table_constraints`, `referential_constraints`. (Dataedo: https://dataedo.com/kb/query/postgresql/list-table-columns-with-their-foreign-keys)

### Playwright navigation behavior
- `page.goto(url)` “waits for the web page to fire the load event,” which fires when the whole page has loaded including dependent resources (scripts, iframes, images). (Playwright docs: https://playwright.dev/docs/navigations; Python version: https://playwright.dev/python/docs/navigations)
- Clicking auto-waits for element visibility and actionability checks. (Playwright docs)
- For multiple navigations, recommended to explicitly `page.waitForURL('**/login')`. (Playwright docs)

---

## Technical Details & Procedures

### OpenAI function/tool calling: end-to-end workflow (Responses API)
From the OpenAI guide’s Python example (abridged to the essential steps): (https://platform.openai.com/docs/guides/function-calling)
1. Define tools (functions) with JSON Schema in `tools=[{type:"function", name, description, parameters...}]`.
2. Call `client.responses.create(model="gpt-5", tools=tools, input=[...])`.
3. Inspect `response.output` for items where `item.type == "function_call"`.
4. Execute your local function using `item.arguments` (JSON string).
5. Append a `function_call_output` item with:
   - `type: "function_call_output"`
   - `call_id: item.call_id`
   - `output: json.dumps({...})`
6. Send the expanded `input` back to `client.responses.create(...)` to get the final natural-language answer.
- Important note: “for reasoning models like GPT-5 or o4-mini, any reasoning items returned in model responses with tool calls must also be passed back with tool call outputs.” (OpenAI Function calling guide)

### OpenAI Code Interpreter: container configuration
- Auto container configuration example includes:
  ```json
  "container": { "type": "auto", "memory_limit": "4g", "file_ids": ["file-1", "file-2"] }
  ```
  (OpenAI Code Interpreter guide: https://developers.openai.com/api/docs/guides/tools-code-interpreter)
- Default memory tier is **1g** if `memory_limit` omitted. (same source)
- To reuse/track container: “Look for the `code_interpreter_call` item in the output… to find the `container_id`.” (same source)
- Explicit mode: create container via `v1/containers` endpoint, then pass its `id` as the `container` value in tool configuration. (same source)

### E2B sandbox lifecycle and timeout management (JS)
- Create with explicit timeout (milliseconds): (https://e2b.dev/docs/sandbox)
  ```ts
  import { Sandbox } from '@e2b/code-interpreter'
  const sandbox = await Sandbox.create({ timeoutMs: 60_000 })
  ```
- Extend/modify timeout during runtime: (https://e2b.dev/docs/sandbox)
  ```ts
  await sandbox.setTimeout(30_000) // 30 seconds from now
  ```
- SDK reference confirms `setTimeout(timeoutMs)` and max keep-alive by plan (Pro 86_400_000 ms; Hobby 3_600_000 ms). (https://e2b.dev/docs/sdk-reference/js-sdk/v1.0.1/sandbox)

### E2B internet access controls
- Disable all outbound internet at creation: (https://e2b.dev/docs/sandbox/internet-access)
  ```ts
  const isolatedSandbox = await Sandbox.create({ allowInternetAccess: false })
  ```
- Deny all except specific IPs/CIDRs: (https://e2b.dev/docs/sandbox/internet-access)
  ```ts
  import { Sandbox, ALL_TRAFFIC } from '@e2b/code-interpreter'
  const sandbox = await Sandbox.create({
    network: { denyOut: [ALL_TRAFFIC], allowOut: ['1.1.1.1', '8.8.8.0/24'] }
  })
  ```
- Domain allowlisting requires `denyOut: [ALL_TRAFFIC]` to block everything else; domains not supported in deny list. (https://e2b.dev/docs/sandbox/internet-access)
- Update network rules via API (PUT): (https://e2b.dev/docs/api-reference/sandboxes/put-sandboxes-network)
  ```bash
  curl --request PUT \
    --url https://api.e2b.app/sandboxes/{sandboxID}/network \
    --header 'Content-Type: application/json' \
    --header 'X-API-Key: <api-key>' \
    --data '{"allowOut":["<string>"],"denyOut":["<string>"]}'
  ```

### E2B restricting public access to sandbox URLs
- Set `allowPublicTraffic: false` and then include header `e2b-traffic-access-token` with `sandbox.trafficAccessToken` for requests; without it returns 403. (https://e2b.dev/docs/sandbox/internet-access)

### Docker: applying CPU/memory limits (docker run)
From Docker docs (https://docs.docker.com/engine/containers/resource_constraints/):
- CPU:
  - `docker run -it --cpus=".5" ubuntu /bin/bash`
  - Equivalent quota/period: `docker run -it --cpu-period=100000 --cpu-quota=50000 ubuntu /bin/bash`
  - Pin cores: `--cpuset-cpus` (e.g., `0-3`, `1,3`)
- Memory:
  - Use `--memory` and optionally `--memory-reservation` (must be lower than `--memory`).
  - OOM killer: only disable with `--oom-kill-disable` when `-m/--memory` is set.

### PostgreSQL: list columns and their foreign keys (information_schema)
- Dataedo provides a full query joining `information_schema.columns`, `key_column_usage`, `table_constraints`, `referential_constraints` to list each column and its referenced primary table/column. (https://dataedo.com/kb/query/postgresql/list-table-columns-with-their-foreign-keys)

### Playwright: navigation + click + explicit wait
- JS/TS pattern: (https://playwright.dev/docs/navigations)
  ```js
  await page.goto('https://example.com');
  await page.getByText('Click me').click();
  await page.waitForURL('**/login');
  ```
- Python pattern: (https://playwright.dev/python/docs/navigations)
  ```py
  await page.goto("https://example.com")
  await page.get_by_text("Click me").click()
  await page.wait_for_url("**/login")
  ```

---

## Comparisons & Trade-offs

### VM-level isolation products: Vercel Sandbox vs E2B (network + secrets)
- Both provide VM-level isolation and “each sandbox its own Linux kernel.” (Vercel KB: https://vercel.com/kb/guide/vercel-sandbox-vs-e2b)
- Credential handling:
  - Vercel Sandbox: “Secret injection proxy outside sandbox boundary (Pro/Enterprise).”
  - E2B: “Environment variables stored inside sandbox.” (Vercel KB)
- Network firewall precedence:
  - Vercel Sandbox: “deny takes precedence.”
  - E2B: “allow takes precedence.” (Vercel KB; aligns with E2B docs stating allow overrides deny)
- Compliance:
  - Vercel: “SOC 2 Type II (Vercel infrastructure)”
  - E2B: “Not publicly documented” (per that guide). (Vercel KB)

### Firecracker microVMs vs containers (design intent)
- Firecracker aims to combine VM isolation with container-like speed/efficiency. (Firecracker design.md)
- Firecracker adds defense-in-depth by sandboxing the **VMM process** itself using seccomp (default), and recommending cgroups/namespaces + privilege dropping via `jailer`. (Firecracker design.md)
- Containers (Docker) rely on namespaces/cgroups and kernel hardening; Docker daemon is a key attack surface and typically runs with root privileges unless rootless mode is used. (Docker Engine security)

### RAG chunking strategies (measured vs heuristic)
- Measured (NVIDIA): page-level chunking had highest average accuracy **0.648** (std **0.107**) vs token-based **0.603–0.645** under their setup (top-k=10, specified embed/rerank models). (NVIDIA blog)
- Heuristic starting ranges (StackAI): test chunk sizes **256/512/1024 tokens** and overlap **10–20%**; suggests retrieving **50–200** candidates then reranking to **5–12** for context. (StackAI: https://www.stackai.com/insights/retrieval-augmented-generation-(rag)-best-practices-for-enterprise-ai-chunking-embeddings-reranking-and-hybrid-search-optimization)
  - Note: these are recommendations, not benchmarked results in the excerpt.

### Similarity metric choice (cosine vs dot vs L2)
- Both Pinecone and Zilliz emphasize matching the metric to the embedding model’s training metric. (Pinecone; Zilliz)
- Cosine ignores magnitude (direction only); dot product and L2 consider magnitude and direction (per Zilliz table). (Zilliz)

### Text-to-SQL schema linking: noise reduction vs omission risk
- RSL-SQL frames schema linking as a trade-off:
  - Benefit: reduces noise and computational overhead by selecting relevant schema elements.
  - Risks: omission of necessary elements (Risk 1) and potential performance degradation even when elements are present (Risk 2). (RSL-SQL arXiv)
- RSL-SQL reports strict recall **94%** while reducing input columns **83%**, aiming to mitigate omission risk while shrinking prompts. (RSL-SQL arXiv)

---

## Architecture & Design Rationale

### Tool calling as a control-plane pattern (OpenAI)
- The OpenAI function calling guide’s loop (tool definitions → model tool call → external execution → tool call output → final model response) is designed so the model can request external actions/data and then incorporate results into a grounded response. (OpenAI Function calling guide)

### Code execution sandboxes: why containers/VMs + limits
- Docker docs emphasize that without constraints, containers can consume host resources without limit; resource flags exist to prevent this. (Docker resource constraints)
- Firecracker design describes multi-tenant threat containment: vCPU threads are treated as malicious and contained via layered trust zones; plus process-level sandboxing (seccomp, cgroups/namespaces, privilege dropping). (Firecracker design.md)
- E2B and Vercel both position VM-level isolation as protection against prompt-injection-driven malicious code inheriting credentials/network/filesystem from the host app environment. (Vercel KB)

### Network boundary design: precedence rules matter
- E2B: allow rules override deny rules (documented explicitly). (E2B Internet access docs)
- Vercel Sandbox: deny overrides allow; rationale given is preventing accidental bypass where a broad deny could be overridden. (Vercel KB)

### RAG pipeline rationale: chunking and reranking as primary levers
- NVIDIA: chunking is critical; their experiments show page-level chunking yields best average accuracy and consistency across datasets in their evaluation. (NVIDIA blog)
- StackAI: frames retrieval stack as ingestion → chunking → embeddings → indexing → retrieval → reranking → context construction → generation; argues “fastest wins usually come earlier,” especially chunking and metadata filtering. (StackAI)

### Text-to-SQL: bidirectional schema linking rationale
- RSL-SQL uses forward schema linking (identify relevant elements from question) plus backward schema linking (parse preliminary SQL to recall referenced elements) to improve recall and reduce omission risk; then uses binary selection and multi-turn self-correction with execution feedback. (RSL-SQL arXiv)

---

## Common Questions & Answers

### Q1) What JSON format do OpenAI function tools use for parameters?
- Function tools define `parameters` as a **JSON Schema object**; the function itself is “defined by a JSON schema.” (OpenAI Function calling guide: https://platform.openai.com/docs/guides/function-calling)

### Q2) What fields are in an OpenAI function definition?
- The guide lists: `type` (always `function`), `name`, `description`, `parameters`, `strict`. (OpenAI Function calling guide)

### Q3) How do I return tool results back to the model?
- The OpenAI guide shows appending an item of type `function_call_output` with the original `call_id` and an `output` payload (JSON string in the example), then calling the API again with the expanded input list. (OpenAI Function calling guide)

### Q4) What is an OpenAI Code Interpreter “container,” and how long does it last?
- It’s “a fully sandboxed virtual machine” used to run Python and store files. It expires if unused for **20 minutes**; after expiry, data is discarded and not recoverable. (OpenAI Code Interpreter guide: https://developers.openai.com/api/docs/guides/tools-code-interpreter)

### Q5) What memory sizes can I choose for OpenAI Code Interpreter containers?
- `1g` (default), `4g`, `16g`, `64g`. (OpenAI Code Interpreter guide)

### Q6) How long can an E2B sandbox run?
- “Up to **24 hours (Pro)** or **1 hour (Base)**” continuously. (E2B Sandbox lifecycle: https://e2b.dev/docs/sandbox)  
- SDK reference also states max keep-alive for `setTimeout`: **86_400_000 ms** (Pro) and **3_600_000 ms** (Hobby). (E2B JS SDK reference: https://e2b.dev/docs/sdk-reference/js-sdk/v1.0.1/sandbox)

### Q7) Can I disable internet access in E2B? What does it do?
- Yes: `allowInternetAccess: false`. When disabled, the sandbox “cannot make outbound network connections.” It’s equivalent to `network.denyOut = ['0.0.0.0/0']`. (E2B Internet access docs: https://e2b.dev/docs/sandbox/internet-access)

### Q8) In E2B, if an IP is both allowed and denied, what happens?
- “Allow rules always take precedence” over deny rules. (E2B Internet access docs)

### Q9) How do Docker CPU limits work with `--cpus`?
- `--cpus=<value>` caps CPU usage; e.g., `--cpus="1.5"` is equivalent to `--cpu-period="100000"` and `--cpu-quota="150000"`. (Docker resource constraints: https://docs.docker.com/engine/containers/resource_constraints/)

### Q10) Why is exposing the Docker daemon API risky?
- Docker notes the daemon requires root unless rootless; exposing the daemon API over HTTP without TLS is “not permitted” and causes startup failure; endpoints should be secured with HTTPS/certs and reachable only from trusted networks/VPN. (Docker Engine security: https://docs.docker.com/engine/security/)

### Q11) What performance numbers does Firecracker’s official design doc claim?
- With minimal kernel, 1 vCPU, **128 MiB RAM**, Firecracker supports “steady mutation rate of **5 microVMs per host core per second**” (example **180 microVMs/sec** on 36 cores). (Firecracker design.md)

### Q12) What chunking strategy performed best in NVIDIA’s RAG experiments?
- Page-level chunking: average accuracy **0.648**, std dev **0.107**; token-based approaches **0.603–0.645** under their setup (top-k=10). (NVIDIA blog: https://developer.nvidia.com/blog/finding-the-best-chunking-strategy-for-accurate-ai-responses/)

### Q13) How should I choose cosine vs dot product vs L2 for vector search?
- Pinecone and Zilliz both recommend matching the similarity metric to the one used to train the embedding model. (Pinecone: https://www.pinecone.io/learn/vector-similarity/; Zilliz: https://zilliz.com/blog/similarity-metrics-for-vector-search)

### Q14) What’s a known caveat when using PostgreSQL `information_schema` for constraints?
- Queries expecting one row can return several because PostgreSQL doesn’t enforce unique constraint names within a schema (though SQL standard expects it). This can affect `referential_constraints` and other views. (PostgreSQL docs: https://www.postgresql.org/docs/current/information-schema.html)

### Q15) In Playwright, what does `page.goto()` wait for by default?
- It waits for the page to fire the **load** event, after dependent resources (stylesheets, scripts, iframes, images) load. (Playwright docs: https://playwright.dev/docs/navigations)